#!/usr/bin/env python3
"""fm-index-diff — gate `tasks/readme.md` against per-Task `task_status` frontmatter.

Spec anchor: TASK.md §7.11 (Tasks-Index Freshness).

Reads every `tasks/<NNN>-<slug>/task.md` and parses every
`^- [\\`<NNN>-<slug>/\\`]…` bullet in `tasks/readme.md`. Emits one diagnostic
per disagreement, orphan bullet, missing bullet, or supersession-suffix
mismatch.

Usage:
    fm index-diff [<index-path>]
    fm index-diff --json [<index-path>]

If <index-path> is omitted, defaults to `tasks/readme.md`.

Exit codes:
    0 — no drift
    1 — at least one diagnostic emitted
    2 — usage / IO error

Diagnostic format (text):
    <index>::ERROR:T.7.11:<NNN>-<slug> <reason>
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import _core  # type: ignore
else:
    from . import _core  # type: ignore

CODE = "T.7.11"
TASK_FOLDER_RE = re.compile(r"^\d{3}-[a-z0-9-]+$")

# Bullet forms we accept:
#   - [`<NNN>-<slug>/`](./<NNN>-<slug>/) — … Status: `<status>` …
# The Status token may be followed by " → superseded by [<NNN>](...)" for
# rows whose task_status is `updated`.
BULLET_RE = re.compile(
    r"^- \[`(?P<folder>\d{3}-[a-z0-9-]+)/?`\]"
    r"\(\.?/?(?P<href>[^)]+)\)"
    r"(?P<rest>.*)$"
)
STATUS_RE = re.compile(r"Status:\s*`(?P<status>[a-z_]+)`")
SUPERSEDED_RE = re.compile(r"superseded by\s*\[(?P<id>\d{3})\]")


@dataclass(frozen=True)
class TaskRow:
    folder: str            # "031-sync-tasks-index-status-drift"
    task_id: str           # "031"
    slug: str              # "sync-tasks-index-status-drift"
    task_status: str       # "open" / "in_progress" / "done" / ...
    superseded_by: list[str]  # task_ids/slugs from frontmatter


@dataclass(frozen=True)
class BulletRow:
    folder: str
    line_no: int           # 1-based
    status: str | None     # parsed Status: token, or None if absent
    superseded_by_id: str | None  # NNN extracted from "superseded by [NNN]"


def _read_tasks(repo_root: Path) -> dict[str, TaskRow]:
    out: dict[str, TaskRow] = {}
    tasks_dir = repo_root / "tasks"
    if not tasks_dir.is_dir():
        return out
    for child in sorted(tasks_dir.iterdir()):
        if not child.is_dir() or not TASK_FOLDER_RE.match(child.name):
            continue
        task_md = child / "task.md"
        if not task_md.is_file():
            continue
        fm = _core.read_fm(task_md, strict=False)
        out[child.name] = TaskRow(
            folder=child.name,
            task_id=_core.str_val(fm, "task_id"),
            slug=_core.str_val(fm, "slug"),
            task_status=_core.str_val(fm, "task_status"),
            superseded_by=_core.str_list(fm, "task_superseded_by"),
        )
    return out


def _read_index_bullets(
    index_path: Path,
) -> tuple[dict[str, BulletRow], list[tuple[str, int, int]]]:
    """Return (first-bullet-per-folder, duplicate-rows).

    Each duplicate-row is `(folder, first_line_no, dup_line_no)` so the caller
    can emit one T.7.11 diagnostic per duplicated bullet. The first occurrence
    populates the primary dict; later occurrences land in the duplicates list.
    """
    out: dict[str, BulletRow] = {}
    duplicates: list[tuple[str, int, int]] = []
    text = index_path.read_text(encoding="utf-8")
    for lineno, raw in enumerate(text.splitlines(), start=1):
        m = BULLET_RE.match(raw)
        if not m:
            continue
        folder = m.group("folder")
        rest = m.group("rest")
        sm = STATUS_RE.search(rest)
        status = sm.group("status") if sm else None
        sup = SUPERSEDED_RE.search(rest)
        sup_id = sup.group("id") if sup else None
        if folder in out:
            duplicates.append((folder, out[folder].line_no, lineno))
            continue
        out[folder] = BulletRow(
            folder=folder,
            line_no=lineno,
            status=status,
            superseded_by_id=sup_id,
        )
    return out, duplicates


def _normalise_id(token: str) -> str | None:
    """Map a `task_superseded_by` token to its canonical 3-digit `task_id`.

    Accepts either a bare 3-digit id (`"031"`) or a `<NNN>-<slug>` folder name
    (`"031-foo-bar"`). Returns the 3-digit prefix on success, `None` for
    malformed input (empty, slug-only without NNN prefix, non-numeric head).
    The caller MUST treat `None` as a dedicated frontmatter-malformed signal.
    """
    if not token:
        return None
    head = token.split("-", 1)[0] if "-" in token else token
    if head.isdigit() and len(head) == 3:
        return head
    return None


def diff(repo_root: Path, index_path: Path) -> list[str]:
    """Return the list of diagnostic strings (no trailing newlines)."""
    diagnostics: list[str] = []
    try:
        rel_index = index_path.resolve().relative_to(repo_root.resolve())
    except ValueError:
        rel_index = index_path
    prefix = f"{rel_index}::ERROR:{CODE}"

    tasks = _read_tasks(repo_root)
    bullets, duplicates = _read_index_bullets(index_path)

    # 1. Status disagreement + supersession-suffix check.
    for folder, task in tasks.items():
        bullet = bullets.get(folder)
        if bullet is None:
            diagnostics.append(
                f"{prefix}:{folder} folder present on disk but no bullet in index"
            )
            continue
        if bullet.status is None:
            diagnostics.append(
                f"{prefix}:{folder} bullet has no `Status:` token"
            )
        elif task.task_status and bullet.status != task.task_status:
            # NOTE: when task_status is empty (unparseable frontmatter), the
            # short-circuit above makes this branch silent on purpose — the
            # F.3.1/F.3.2 frontmatter linter at check-governance step [1/6]
            # is the canonical surface for that failure.
            diagnostics.append(
                f"{prefix}:{folder} bullet status=`{bullet.status}` "
                f"but task.md task_status=`{task.task_status}`"
            )
        # Supersession suffix: when task_status == "updated", the bullet MUST
        # carry a "→ superseded by [NNN]" pointer matching task_superseded_by.
        if task.task_status == "updated":
            normalised = [_normalise_id(t) for t in task.superseded_by]
            if any(n is None for n, raw in zip(normalised, task.superseded_by)
                   if raw):
                bad = [raw for raw, n in zip(task.superseded_by, normalised)
                       if raw and n is None]
                diagnostics.append(
                    f"{prefix}:{folder} task_superseded_by carries malformed "
                    f"entries (no 3-digit `<NNN>` prefix): {bad}"
                )
            expected_ids = {n for n in normalised if n}
            if not expected_ids:
                diagnostics.append(
                    f"{prefix}:{folder} task_status=`updated` but "
                    f"task_superseded_by is empty"
                )
            elif bullet.superseded_by_id is None:
                diagnostics.append(
                    f"{prefix}:{folder} task_status=`updated` but bullet "
                    f"is missing `→ superseded by [NNN]` pointer"
                )
            elif bullet.superseded_by_id not in expected_ids:
                diagnostics.append(
                    f"{prefix}:{folder} bullet supersession pointer "
                    f"`[{bullet.superseded_by_id}]` not in task_superseded_by="
                    f"{sorted(expected_ids)}"
                )

    # 2. Orphan bullets (in index, no folder on disk).
    for folder, bullet in bullets.items():
        if folder not in tasks:
            diagnostics.append(
                f"{prefix}:{folder} bullet present at line {bullet.line_no} "
                f"but no `tasks/{folder}/` folder on disk"
            )

    # 3. Duplicate bullets in the index — silent fallback was a Task-008 hazard.
    for folder, first_line, dup_line in duplicates:
        diagnostics.append(
            f"{prefix}:{folder} duplicate bullet at line {dup_line} "
            f"(first at line {first_line})"
        )

    diagnostics.sort()
    return diagnostics


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="fm-index-diff", add_help=True)
    p.add_argument(
        "index",
        nargs="?",
        default=None,
        help="path to tasks/readme.md (default: tasks/readme.md under repo root)",
    )
    p.add_argument(
        "--json",
        action="store_true",
        help="emit JSON {diagnostics: [...]} instead of one line per diagnostic",
    )
    args = p.parse_args(argv)

    repo_root = _core.repo_root_from_cwd()
    index_path = (
        Path(args.index).resolve()
        if args.index else (repo_root / "tasks" / "readme.md").resolve()
    )
    if not index_path.is_file():
        print(f"fm-index-diff: index not found: {index_path}", file=sys.stderr)
        return 2

    diagnostics = diff(repo_root, index_path)
    if args.json:
        sys.stdout.write(json.dumps({"diagnostics": diagnostics}, indent=2))
        sys.stdout.write("\n")
    else:
        for d in diagnostics:
            sys.stdout.write(d + "\n")
    return 1 if diagnostics else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
