#!/usr/bin/env python3
"""fm-rename — cross-file slug rename (T3 mechanical operation).

Spec anchors: F.5.3 (frontmatter-only invariant), F.7.2 (Repair Tier Ladder).

Slug renames are flagged as T3 in SPEC §7.2 because they touch many files at
once. `fm-edit` MUST refuse them; this tool exists as the *audited, atomic*
T3 surface so a Task author can perform a slug rename without hand-editing
every cross-reference.

Usage:
    fm-rename <old-slug> <new-slug> [--scope=<roots>] [--rename-folder]
              [--dry-run]

Behaviour summary:
    1. Pre-scan: walk the operational scope, parse each file's frontmatter,
       collect every change (slug field rename, scalar field rename when the
       scalar value equals old-slug, list-item rename when an item equals
       old-slug). Body bytes outside the frontmatter MUST stay byte-identical.
    2. Refuse (exit 4) when the slug is referenced from any *done* Task's
       `task_affects_paths` list — that history is immutable.
    3. Atomicity: if any per-file check fails, abort BEFORE writing anything.
       Only after the full plan is validated is each file written under its
       own FileLock.
    4. Idempotent: a second invocation with the same args is a no-op (the
       pre-scan returns an empty plan).
    5. --rename-folder additionally renames a single matching directory under
       /tasks/, /prompts/, /research/, or /skills/. Performed AFTER the file
       writes so a write failure does not orphan the folder name.

Exit codes:
    0  success (or no-op)
    2  usage error
    3  pre-condition not met (e.g., new slug already in use)
    4  T3 refusal (done-Task task_affects_paths reference, or other invariant)
"""
from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import _core  # type: ignore
else:
    from . import _core  # type: ignore

EXIT_OK = 0
EXIT_USAGE = 2
EXIT_PRECONDITION = 3
EXIT_REFUSED = 4

SLUG_RE = re.compile(r"^[a-z0-9][a-z0-9-]*$")
FOLDER_ROOTS = ("tasks", "prompts", "research", "skills")


# ---- Plan model -------------------------------------------------------------


@dataclass
class FileChange:
    """One file's rename plan: original text, new text, list of human-readable
    diffs for --dry-run output. The (old_text, new_text) pair is what gets
    written under FileLock; everything else is for reporting."""

    path: Path
    old_text: str
    new_text: str
    diffs: list[str] = field(default_factory=list)


@dataclass
class Plan:
    changes: list[FileChange] = field(default_factory=list)
    folder_rename: tuple[Path, Path] | None = None


# ---- Frontmatter rewriting --------------------------------------------------


def _parse_lines(fm_body: str) -> list[dict]:
    """Mirror of edit._parse_lines, kept local so this tool stays a single
    file. Round-trips unchanged when no rename touches an entry.
    """
    entries: list[dict] = []
    lines = fm_body.split("\n")
    i = 0
    while i < len(lines):
        raw = lines[i]
        stripped = raw.strip()
        if not stripped or stripped.startswith("#"):
            entries.append({"kind": "blank", "raw": [raw]})
            i += 1
            continue
        if ":" not in stripped:
            entries.append({"kind": "blank", "raw": [raw]})
            i += 1
            continue
        key, _, val = stripped.partition(":")
        key = key.strip()
        val = val.strip()
        if val == "" or val == "[]":
            list_items: list[str] = []
            raws = [raw]
            j = i + 1
            while j < len(lines):
                cont = lines[j]
                cs = cont.strip()
                if cs.startswith("- "):
                    list_items.append(cs[2:].strip().strip('"').strip("'"))
                    raws.append(cont)
                    j += 1
                elif cs == "":
                    raws.append(cont)
                    j += 1
                else:
                    break
            while raws and raws[-1].strip() == "":
                raws.pop()
            entries.append({
                "kind": "list", "key": key, "value": list_items, "raw": raws,
            })
            i = i + len(raws)
        else:
            quoted = val.startswith(('"', "'"))
            entries.append({
                "kind": "scalar", "key": key,
                "value": val.strip('"').strip("'"),
                "quoted": quoted, "raw": [raw],
            })
            i += 1
    return entries


def _render(entries: list[dict]) -> str:
    out: list[str] = []
    for e in entries:
        if e["kind"] == "blank":
            out.extend(e["raw"])
        elif e["kind"] == "scalar":
            v = e["value"]
            forced = (
                v == ""
                or any(ch in v for ch in (":", "#", "[", "]", "{", "}", ",",
                                          "&", "*", "!", "|", ">", "%", "@", "`"))
            )
            if e.get("quoted") or forced:
                escaped = v.replace("\\", "\\\\").replace('"', '\\"')
                out.append(f"{e['key']}: \"{escaped}\"")
            else:
                out.append(f"{e['key']}: {v}")
        elif e["kind"] == "list":
            items = e["value"]
            if not items:
                out.append(f"{e['key']}: []")
            else:
                out.append(f"{e['key']}:")
                for item in items:
                    out.append(f"  - {item}")
    return "\n".join(out)


def _split(text: str) -> tuple[str, str, str]:
    """Same shape as edit._split: (open_fence, fm_body, rest). rest starts at
    the closing `---` line; reusing it byte-for-byte preserves body bytes."""
    m = _core.FRONTMATTER_RE.match(text)
    if not m:
        return "", "", text
    fm_body = m.group(1)
    open_fence = "---\n"
    closing_start = m.end(1)
    rest = text[closing_start:]
    return open_fence, fm_body, rest


def _path_item_matches_slug(item: str, slug: str) -> bool:
    """An entry of `task_affects_paths` matches `slug` when:
      - the whole item equals the slug, or
      - any path component equals the slug (e.g., `prompts/{slug}/prompt.md`),
        or
      - any path component ENDS WITH `-{slug}` (e.g., `tasks/099-{slug}/`).
    Conservative on purpose: this is the T3 refusal predicate, so
    over-reporting is preferable to silent erasure of done-Task history.
    """
    if item == slug:
        return True
    parts = [p for p in item.replace("\\", "/").split("/") if p]
    if slug in parts:
        return True
    suffix = f"-{slug}"
    return any(p.endswith(suffix) for p in parts)


def _rewrite_entries(
    entries: list[dict], old: str, new: str
) -> list[str]:
    """Apply old→new rename in-place. Returns a list of human-readable
    descriptions for each change made (for --dry-run output)."""
    diffs: list[str] = []
    for e in entries:
        if e["kind"] == "scalar" and e["value"] == old:
            e["value"] = new
            e["raw"] = []  # force re-render so we don't keep stale bytes
            diffs.append(f"  scalar {e['key']}: {old} → {new}")
        elif e["kind"] == "list":
            entry_changed = False
            for idx, item in enumerate(e["value"]):
                if item == old:
                    e["value"][idx] = new
                    diffs.append(f"  list   {e['key']}[{idx}]: {old} → {new}")
                    entry_changed = True
            if entry_changed:
                e["raw"] = []  # force re-render of this list entry
    return diffs


def _plan_one_file(path: Path, old: str, new: str) -> FileChange | None:
    """Return a FileChange if `path` references `old` in its frontmatter,
    else None. Body bytes are guaranteed byte-identical by reusing `rest`."""
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    open_fence, fm_body, rest = _split(text)
    if not open_fence:
        return None
    entries = _parse_lines(fm_body)
    diffs = _rewrite_entries(entries, old, new)
    if not diffs:
        return None
    new_fm = _render(entries)
    new_text = open_fence + new_fm + rest
    # Belt-and-braces: re-split and confirm body equality. RuntimeError so
    # the guard survives `python -O`.
    _, _, new_rest = _split(new_text)
    if rest != new_rest:
        raise RuntimeError(
            f"fm-rename invariant violated for {path}: body bytes changed"
        )
    return FileChange(path=path, old_text=text, new_text=new_text, diffs=diffs)


# ---- T3 refusal --------------------------------------------------------------


def _check_done_task_refusal(
    repo_root: Path, scope: list[str] | None, old: str
) -> tuple[bool, str]:
    """Return (refused, reason). Walks every Task file; refuses when the
    target slug appears in a done Task's `task_affects_paths` list."""
    for path in _core.iter_operational_files(repo_root, scope=scope):
        fm = _core.read_fm(path, strict=False)
        if _core.str_val(fm, "type") != "task":
            continue
        if _core.str_val(fm, "task_status") != "done":
            continue
        items = _core.str_list(fm, "task_affects_paths")
        for item in items:
            if _path_item_matches_slug(item, old):
                try:
                    rel = path.resolve().relative_to(repo_root.resolve())
                except ValueError:
                    rel = path
                return True, (
                    f"slug {old!r} is referenced by done Task {rel} "
                    f"(task_affects_paths includes {item!r}); history is "
                    f"immutable — file a follow-up Task instead"
                )
    return False, ""


# ---- Plan construction -------------------------------------------------------


def _detect_folder_rename(
    repo_root: Path, old: str, new: str
) -> tuple[Path, Path] | None:
    """Find a single folder under FOLDER_ROOTS whose name *equals* old or
    whose name ends with `-{old}` (Tasks: NNN-{slug}). Returns (src, dst)
    paths or None when no match.

    Refuses (raises) when more than one match exists or when the destination
    already exists.
    """
    matches: list[Path] = []
    for root in FOLDER_ROOTS:
        d = repo_root / root
        if not d.is_dir():
            continue
        for child in d.iterdir():
            if not child.is_dir():
                continue
            name = child.name
            if name == old or name.endswith(f"-{old}"):
                matches.append(child)
    if not matches:
        return None
    if len(matches) > 1:
        raise SystemExit(
            f"fm-rename: --rename-folder ambiguous; multiple folders match "
            f"slug {old!r}: " + ", ".join(str(m) for m in matches)
        )
    src = matches[0]
    new_name = (
        src.name.removesuffix(f"-{old}") + f"-{new}"
        if src.name.endswith(f"-{old}") and src.name != old
        else new
    )
    dst = src.with_name(new_name)
    if dst.exists() and dst != src:
        raise SystemExit(
            f"fm-rename: --rename-folder destination exists: {dst}"
        )
    if dst == src:
        return None  # idempotent
    return src, dst


def build_plan(
    repo_root: Path,
    old: str,
    new: str,
    *,
    scope: list[str] | None = None,
    rename_folder: bool = False,
) -> Plan:
    """Pre-scan the tree and return a fully-validated Plan. Pure: never
    writes. Caller decides whether to execute or print."""
    plan = Plan()
    for path in _core.iter_operational_files(repo_root, scope=scope):
        change = _plan_one_file(path, old, new)
        if change is not None:
            plan.changes.append(change)
    plan.changes.sort(key=lambda c: str(c.path))
    if rename_folder:
        plan.folder_rename = _detect_folder_rename(repo_root, old, new)
    return plan


# ---- Plan execution ----------------------------------------------------------


def _write_plan(plan: Plan) -> None:
    """Apply the plan. Each file is written under its own FileLock. The
    pre-scan has already proven body-byte identity per file; this function
    simply persists the planned text."""
    for change in plan.changes:
        with _core.FileLock(change.path):
            # Re-read under lock; if the file changed since pre-scan, abort.
            current = change.path.read_text(encoding="utf-8")
            if current != change.old_text:
                raise RuntimeError(
                    f"fm-rename: {change.path} changed during write; "
                    f"aborting to preserve atomicity"
                )
            change.path.write_text(change.new_text, encoding="utf-8")
    if plan.folder_rename is not None:
        src, dst = plan.folder_rename
        src.rename(dst)


# ---- CLI --------------------------------------------------------------------


def _validate_slug(slug: str, label: str) -> None:
    if not SLUG_RE.match(slug):
        raise SystemExit(
            f"fm-rename: {label} slug {slug!r} must match [a-z0-9][a-z0-9-]*"
        )


def _format_plan(plan: Plan, repo_root: Path) -> str:
    lines: list[str] = []
    if not plan.changes and plan.folder_rename is None:
        lines.append("fm-rename: no-op (slug not referenced anywhere)")
        return "\n".join(lines) + "\n"
    lines.append(f"fm-rename: {len(plan.changes)} file(s) to update")
    for change in plan.changes:
        try:
            rel = change.path.resolve().relative_to(repo_root.resolve())
        except ValueError:
            rel = change.path
        lines.append(str(rel))
        lines.extend(change.diffs)
    if plan.folder_rename is not None:
        src, dst = plan.folder_rename
        try:
            srel = src.resolve().relative_to(repo_root.resolve())
            drel = dst.resolve().relative_to(repo_root.resolve())
        except ValueError:
            srel, drel = src, dst
        lines.append(f"folder: {srel} → {drel}")
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="fm-rename", add_help=True)
    p.add_argument("old_slug")
    p.add_argument("new_slug")
    p.add_argument("--scope", default=None,
                   help="comma-separated subset of operational roots")
    p.add_argument("--rename-folder", action="store_true",
                   help="also rename a single matching folder under "
                        "tasks/, prompts/, research/, or skills/")
    p.add_argument("--dry-run", action="store_true",
                   help="print the plan; do not write")
    args = p.parse_args(argv)

    _validate_slug(args.old_slug, "old")
    _validate_slug(args.new_slug, "new")
    if args.old_slug == args.new_slug:
        # Idempotent no-op. Still emit a diagnostic on stderr for clarity.
        print("fm-rename: old-slug == new-slug; nothing to do",
              file=sys.stderr)
        return EXIT_OK

    repo_root = _core.repo_root_from_cwd()
    scope: list[str] | None = (
        [s.strip() for s in args.scope.split(",") if s.strip()]
        if args.scope else None
    )

    refused, reason = _check_done_task_refusal(repo_root, scope, args.old_slug)
    if refused:
        print(f"fm-rename: refused — {reason}", file=sys.stderr)
        return EXIT_REFUSED

    # Detect collision: another file already owns the new slug. Exit 3.
    for path in _core.iter_operational_files(repo_root, scope=scope):
        fm = _core.read_fm(path, strict=False)
        if _core.str_val(fm, "slug") == args.new_slug:
            try:
                rel = path.resolve().relative_to(repo_root.resolve())
            except ValueError:
                rel = path
            print(
                f"fm-rename: new slug {args.new_slug!r} already owned by "
                f"{rel}; aborting", file=sys.stderr,
            )
            return EXIT_PRECONDITION

    try:
        plan = build_plan(
            repo_root, args.old_slug, args.new_slug,
            scope=scope, rename_folder=args.rename_folder,
        )
    except SystemExit as e:
        # _detect_folder_rename raises SystemExit on ambiguity / collision.
        print(str(e), file=sys.stderr)
        return EXIT_PRECONDITION

    if args.dry_run:
        sys.stdout.write(_format_plan(plan, repo_root))
        return EXIT_OK

    if not plan.changes and plan.folder_rename is None:
        # Idempotent second invocation lands here.
        return EXIT_OK

    _write_plan(plan)
    sys.stdout.write(_format_plan(plan, repo_root))
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
