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


def _read_index_bullets(index_path: Path) -> dict[str, BulletRow]:
    out: dict[str, BulletRow] = {}
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
        # Only retain the FIRST bullet for a given folder; later duplicates
        # become an additional diagnostic.
        if folder in out:
            continue
        out[folder] = BulletRow(
            folder=folder,
            line_no=lineno,
            status=status,
            superseded_by_id=sup_id,
        )
    return out


def _normalise_id(token: str) -> str:
    """Accept either a 3-digit `task_id` or a `<NNN>-<slug>` folder name and
    return the 3-digit prefix only. Empty input maps to ''."""
    if not token:
        return ""
    if "-" in token:
        head = token.split("-", 1)[0]
    else:
        head = token
    if head.isdigit() and len(head) == 3:
        return head
    return token  # caller handles non-conforming values verbatim


def diff(repo_root: Path, index_path: Path) -> list[str]:
    """Return the list of diagnostic strings (no trailing newlines)."""
    diagnostics: list[str] = []
    rel_index = index_path.resolve().relative_to(repo_root.resolve())
    prefix = f"{rel_index}::ERROR:{CODE}"

    tasks = _read_tasks(repo_root)
    bullets = _read_index_bullets(index_path)

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
            diagnostics.append(
                f"{prefix}:{folder} bullet status=`{bullet.status}` "
                f"but task.md task_status=`{task.task_status}`"
            )
        # Supersession suffix: when task_status == "updated", the bullet MUST
        # carry a "→ superseded by [NNN]" pointer matching task_superseded_by.
        if task.task_status == "updated":
            expected_ids = {_normalise_id(t) for t in task.superseded_by}
            expected_ids.discard("")
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
