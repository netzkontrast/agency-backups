#!/usr/bin/env python3
"""Duplicate `task_id` linter (Task 033 ST-3 — closes TASK.md §8.1 enforcement gap).

Scans `tasks/<NNN>-<slug>/task.md` files, extracts `task_id` from each
frontmatter, and exits 1 if any value appears more than once across
*active* tasks (`task_status` ∈ {open, in_progress, blocked, done}).

A duplicate is **explained** (INFO, not ERROR) when supersession reciprocity
holds across the two folders:

  - the predecessor's frontmatter MUST carry `task_status: updated`, AND
  - the predecessor's `task_superseded_by` MUST cite the successor's
    `task_id` (or slug), AND
  - the successor's `task_supersedes` MUST cite the predecessor's
    `task_id` (or slug).

Unexplained duplicates → ERROR exit 1.

This linter closes the agent-responsibility-only enforcement window
acknowledged in TASK.md §8.1 (the prose explicitly says "duplicate `task_id`
prevention is a spec-bearing rule but is not currently linter-enforced").
The 006/006, 009/009, 031/031 and 032/032 collisions tracked by Task 024 /
Task 043 demonstrate that the agent-responsibility approach failed; this
linter is the missing mechanical guard.

Usage::

    python3 tools/fm/check-duplicate-task-id.py [<paths>]

Defaults to scanning the repo's `tasks/` directory. Custom paths may be a
mix of directories (recursed for `task.md`) and individual `task.md` files.

Exit codes:
    0  — no unexplained duplicates (clean OR every duplicate is supersession-explained).
    1  — at least one unexplained duplicate found.
    2  — fatal usage error (e.g. unreadable file).
"""
from __future__ import annotations

import argparse
import sys
from collections import defaultdict
from pathlib import Path
from typing import Iterable

# Re-use the shared frontmatter parser + repo-root walker.
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))  # tools/ on path so `fm._core` resolves

from fm._core import read_fm, repo_root_from_cwd, str_list, str_val  # noqa: E402


ACTIVE_STATUSES = {"open", "in_progress", "blocked", "done"}


def _iter_task_files(paths: Iterable[Path]) -> list[Path]:
    out: list[Path] = []
    for p in paths:
        if p.is_dir():
            out.extend(sorted(p.rglob("task.md")))
        elif p.is_file() and p.name == "task.md":
            out.append(p)
    return out


def _normalise_ref(ref: str) -> str:
    """Strip surrounding quotes/whitespace from a task_id or slug reference."""
    return ref.strip().strip('"').strip("'")


def _explained_by_supersession(
    pair: tuple[Path, dict],
    other: tuple[Path, dict],
) -> bool:
    """Return True iff `pair` and `other` form a reciprocal supersession edge.

    The check is symmetric — caller invokes it once per ordered pair.
    Either folder may be the predecessor (`task_status: updated` carrying
    `task_superseded_by`) or the successor (`task_supersedes` citing the
    predecessor). The shared `task_id` is the duplicate; we resolve identity
    by matching the slug (folder name minus `<NNN>-` prefix).

    Reciprocity rule (per TASK.md §3.3, §4.7, §7.10):
      - predecessor: task_status == "updated" AND task_superseded_by ⊇ {successor.id_or_slug}
      - successor: task_supersedes ⊇ {predecessor.id_or_slug}
    """
    a_path, a_fm = pair
    b_path, b_fm = other

    a_id = _normalise_ref(str_val(a_fm, "task_id"))
    b_id = _normalise_ref(str_val(b_fm, "task_id"))
    a_slug = a_path.parent.name
    b_slug = b_path.parent.name

    a_refs = {a_id, a_slug, _strip_id_prefix(a_slug)}
    b_refs = {b_id, b_slug, _strip_id_prefix(b_slug)}

    a_status = _normalise_ref(str_val(a_fm, "task_status"))
    b_status = _normalise_ref(str_val(b_fm, "task_status"))

    a_superseded_by = {_normalise_ref(s) for s in str_list(a_fm, "task_superseded_by")}
    b_superseded_by = {_normalise_ref(s) for s in str_list(b_fm, "task_superseded_by")}
    a_supersedes = {_normalise_ref(s) for s in str_list(a_fm, "task_supersedes")}
    b_supersedes = {_normalise_ref(s) for s in str_list(b_fm, "task_supersedes")}

    # Case 1: a is predecessor (updated), b is successor.
    if a_status == "updated" and (a_superseded_by & b_refs) and (b_supersedes & a_refs):
        return True
    # Case 2: b is predecessor (updated), a is successor.
    if b_status == "updated" and (b_superseded_by & a_refs) and (a_supersedes & b_refs):
        return True
    return False


def _strip_id_prefix(folder_name: str) -> str:
    """`013-renumber-...` → `renumber-...`. Returns the input on no match."""
    parts = folder_name.split("-", 1)
    if len(parts) == 2 and parts[0].isdigit():
        return parts[1]
    return folder_name


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description="Detect unexplained duplicate task_id values.",
    )
    ap.add_argument(
        "paths",
        nargs="*",
        type=Path,
        help="task.md files or directories to scan (defaults to repo's tasks/).",
    )
    args = ap.parse_args(argv)

    if not args.paths:
        repo = repo_root_from_cwd()
        args.paths = [repo / "tasks"]

    task_files = _iter_task_files(args.paths)
    if not task_files:
        print("check-duplicate-task-id: no task.md files found", file=sys.stderr)
        return 0

    # Build {task_id: [(path, fm), ...]} across active tasks only.
    by_id: dict[str, list[tuple[Path, dict]]] = defaultdict(list)
    for f in task_files:
        fm = read_fm(f, strict=False)
        if not fm:
            continue
        status = _normalise_ref(str_val(fm, "task_status"))
        # Per TASK.md §3.3: `updated` predecessors are explicitly allowed to
        # share their original id with their successor under reciprocity.
        # `abandoned` predecessors are excluded — they did not produce a
        # successor, so id-reuse there is a true collision.
        if status not in ACTIVE_STATUSES and status != "updated":
            continue
        tid = _normalise_ref(str_val(fm, "task_id"))
        if not tid:
            continue
        by_id[tid].append((f, fm))

    unexplained = 0
    for tid, occurrences in sorted(by_id.items()):
        if len(occurrences) <= 1:
            continue
        # For >2-way collisions, every pair must be explained. Practically the
        # agency repo's collisions are always 2-way; we treat any pair that
        # is not supersession-explained as a duplicate, reporting once.
        explained_any = False
        if len(occurrences) == 2:
            explained_any = _explained_by_supersession(occurrences[0], occurrences[1])
        if explained_any:
            paths_repr = ", ".join(str(p) for p, _ in occurrences)
            print(
                f"check-duplicate-task-id: INFO: task_id={tid!r} "
                f"shared via supersession reciprocity ({paths_repr})"
            )
            continue
        unexplained += 1
        paths_repr = "\n  ".join(str(p) for p, _ in occurrences)
        print(
            f"check-duplicate-task-id: ERROR: task_id={tid!r} "
            f"appears in {len(occurrences)} active tasks without supersession "
            f"reciprocity:\n  {paths_repr}",
            file=sys.stderr,
        )

    if unexplained:
        print(
            f"check-duplicate-task-id: {unexplained} unexplained duplicate(s) "
            f"found. See TASK.md §8.1 and the renumber procedure in "
            f"MAINTENANCE.md §3.5.",
            file=sys.stderr,
        )
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
