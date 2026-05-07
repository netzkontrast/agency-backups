#!/usr/bin/env python3
"""check-assumption-log — validate the substance of `## Assumptions Log` sections.

Spec anchors:
    AGENTS.md §60-65 (assumption-logging rule)
    FOLDERS.md F.3 (required content for readme.md)

Usage:
    python3 tools/check-assumption-log.py [PATH ...]

Each PATH may be either a single readme.md or a directory containing
operational `<NNN>-<slug>/readme.md` (or `<slug>/readme.md`) folders.
The linter walks recursively and inspects every `readme.md`.

Checks (all WARN-tier — this linter is advisory, never gating):
  ASSUMPTION.LOG.MISSING — `## Assumptions Log` heading absent.
  ASSUMPTION.LOG.EMPTY   — section body has no substantive content
                           (and does not declare `(none)`).
  ASSUMPTION.LOG.STALE   — readme `updated:` is older than the parent
                           task.md `updated:` (currency drift).

Exit codes:
    0 — no diagnostics
    2 — at least one WARN diagnostic surfaced (advisory)
    1 — usage error
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Iterable

# Reuse the shared frontmatter / section-finding library.
_TOOLS = Path(__file__).resolve().parent
if str(_TOOLS) not in sys.path:
    sys.path.insert(0, str(_TOOLS))
_FM = _TOOLS / "fm"
if str(_FM) not in sys.path:
    sys.path.insert(0, str(_FM))

try:
    import _core  # type: ignore  # noqa: E402
except ImportError:
    # Graceful degradation per repo's advisory-linter convention: if the
    # frontmatter parser is unavailable (e.g. mid-toolchain-migration window
    # per MAINTENANCE.md §1), exit clean rather than crash. check-governance.sh
    # invokes this linter advisory-tier (`|| true`), so an unhandled crash
    # would silently no-op and rob the operator of any signal.
    print(
        "check-assumption-log: tools/fm/_core.py not importable — "
        "skipping (advisory linter, exit 0).",
        file=sys.stderr,
    )
    raise SystemExit(0)


HEADING = "Assumptions Log"
DIAG_PREFIX = "ASSUMPTION.LOG"
NONE_RE = re.compile(r"^\s*\(none\)\s*$", re.IGNORECASE)
HTML_COMMENT_RE = re.compile(r"<!--.*?-->", re.DOTALL)


def _strip_comments(text: str) -> str:
    return HTML_COMMENT_RE.sub("", text)


def _is_substantive(body: str) -> bool:
    """Return True iff the section body contains at least one non-blank,
    non-comment line that is not the explicit `(none)` declaration."""
    cleaned = _strip_comments(body)
    for raw in cleaned.splitlines():
        line = raw.strip()
        if not line:
            continue
        if NONE_RE.match(line):
            # `(none)` is acknowledged as substantive — see _has_none_marker.
            continue
        return True
    return False


def _has_none_marker(body: str) -> bool:
    cleaned = _strip_comments(body)
    return any(NONE_RE.match(ln) for ln in cleaned.splitlines())


def _parse_iso_date(value: str) -> tuple[int, int, int] | None:
    """Return a (Y, M, D) tuple for ISO-8601 dates of the form YYYY-MM-DD,
    or None if `value` does not parse. Tolerates quoted strings."""
    if not value:
        return None
    v = value.strip().strip('"').strip("'")
    m = re.match(r"^(\d{4})-(\d{2})-(\d{2})", v)
    if not m:
        return None
    return int(m.group(1)), int(m.group(2)), int(m.group(3))


def _sibling_task_md(readme: Path) -> Path | None:
    """Return the task.md sibling of `readme` if one exists, else None."""
    candidate = readme.parent / "task.md"
    return candidate if candidate.is_file() else None


def diagnostics_for(readme: Path) -> list[str]:
    """Return a list of rendered WARN diagnostic strings for `readme`."""
    diags: list[str] = []
    try:
        text = readme.read_text(encoding="utf-8")
    except OSError as exc:
        diags.append(
            f"{readme}::WARN:{DIAG_PREFIX}.READ:cannot read file ({exc})"
        )
        return diags

    fm = _core.parse_frontmatter(text, strict=False)

    bodies = _core.find_all_section_bodies(text, HEADING)
    if not bodies:
        diags.append(
            f"{readme}::WARN:{DIAG_PREFIX}.MISSING:"
            f"required `## {HEADING}` section absent (FOLDERS.md F.3 / AGENTS.md §60-65)"
        )
        return diags

    body = bodies[0]
    if not (_is_substantive(body) or _has_none_marker(body)):
        diags.append(
            f"{readme}::WARN:{DIAG_PREFIX}.EMPTY:"
            f"`## {HEADING}` section is empty; add at least one entry "
            f"or the explicit line `(none)` (AGENTS.md §60-65)"
        )

    # Currency check: compare against sibling task.md's `updated:` if present.
    task_md = _sibling_task_md(readme)
    if task_md is not None:
        readme_updated = _parse_iso_date(_core.str_val(fm, "updated"))
        task_fm = _core.read_fm(task_md)
        task_updated = _parse_iso_date(_core.str_val(task_fm, "updated"))
        if readme_updated and task_updated and readme_updated < task_updated:
            diags.append(
                f"{readme}::WARN:{DIAG_PREFIX}.STALE:"
                f"readme `updated:` ({_fmt(readme_updated)}) is older than "
                f"sibling task.md `updated:` ({_fmt(task_updated)}) — "
                f"reconfirm or refresh assumptions"
            )

    return diags


def _fmt(d: tuple[int, int, int]) -> str:
    return f"{d[0]:04d}-{d[1]:02d}-{d[2]:02d}"


def _iter_readmes(target: Path) -> Iterable[Path]:
    """Yield every operational readme.md under `target`.

    If `target` is itself a readme.md, yield it.
    If `target` is a directory, walk one level of operational subfolders
    (matches both `<NNN>-<slug>/readme.md` and `<slug>/readme.md`) but
    also walks recursively to be tolerant of layout drift.
    """
    if target.is_file():
        if target.name.lower() == "readme.md":
            yield target
        return
    if not target.is_dir():
        return
    for path in sorted(target.rglob("readme.md")):
        # Skip nested readmes inside provider/result/output sub-trees — those
        # are not operational-folder readmes per FOLDERS.md F.3.
        rel_parts = path.relative_to(target).parts
        # Top-level readme (e.g. tasks/readme.md) is an index, not operational.
        if len(rel_parts) <= 1:
            continue
        # Operational readmes live exactly one level deep under the target
        # (`<slug>/readme.md`). Anything deeper is a sub-artefact (workspace,
        # output, subtasks, etc.).
        if len(rel_parts) > 2:
            continue
        yield path


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        prog="check-assumption-log",
        description=(
            "Advisory linter for `## Assumptions Log` sections "
            "(AGENTS.md §60-65 / FOLDERS.md F.3)."
        ),
    )
    parser.add_argument(
        "paths",
        nargs="*",
        default=["tasks", "research"],
        help="readme.md files or directories to scan (default: tasks/ research/)",
    )
    args = parser.parse_args(argv)

    targets = [Path(p) for p in args.paths]
    if not targets:
        parser.error("no paths supplied")
        return 1

    all_diags: list[str] = []
    for target in targets:
        if not target.exists():
            print(
                f"check-assumption-log: warning: path does not exist: {target}",
                file=sys.stderr,
            )
            continue
        for readme in _iter_readmes(target):
            all_diags.extend(diagnostics_for(readme))

    for d in all_diags:
        print(d)

    print(
        f"check-assumption-log: {len(all_diags)} WARN diagnostic(s) "
        f"across {sum(1 for _ in (Path(p) for p in args.paths))} target(s).",
        file=sys.stderr,
    )
    return 2 if all_diags else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
