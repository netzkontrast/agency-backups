#!/usr/bin/env python3
"""Task lifecycle classification helper (Task 033 ST-4 — TASK.md §4.7 helper).

Given a Task path and a proposed `task_status` transition target
(`updated` or `abandoned`), evaluate the four conditions in TASK.md §4.7
deterministically and report PASS or FAIL with the missing condition(s).

This is a **manual** helper invoked by maintenance agents. It is NOT part
of `tools/check-governance.sh` — automatic gating would force the agent to
mechanise subjective predicates ("Goal still desirable?") which the §4.7
prose intentionally leaves as an agent judgement call.

The four §4.7 conditions for a `updated` transition:

  1. Goal still desirable
       — agent attestation; the helper accepts `--goal-still-desirable`
         as a CLI flag the invoking agent passes in after reading the
         predecessor's Goal section.
  2. Plan/Todo drifted
       — agent attestation; flag `--plan-drifted`. The helper additionally
         emits a heuristic WARN if the predecessor has every Todo box
         already checked (`[x]`), since that suggests `done` is the
         correct closure rather than `updated`.
  3. Successor exists
       — mechanical: `task_superseded_by` MUST be non-empty AND each
         entry MUST resolve to an existing `tasks/<NNN>-<slug>/task.md`.
  4. Supersession reciprocity
       — mechanical: every successor's frontmatter MUST cite this Task's
         `task_id` (or slug) in `task_supersedes`.

For the `abandoned` transition the helper checks (per TASK.md §8.3):

  A1. `notes.md` exists in the Task folder.
  A2. `notes.md` contains a "## Partial Artifacts" or "abandonment" reason
      paragraph (heuristic: the literal word `abandon` or a `## Partial
      Artifacts` heading).

The five-signal `classify_task` decision tree that mechanises *every* §4.7
condition (including the two attestation predicates) is ratified in
`research/spec-staleness-decision-formalization/output/SPEC.md` §1
(Task 033 ST-2 / Task 039 ST-2). This helper currently implements the
four-condition fallback derived from TASK.md §4.7 prose; a follow-up Task
migrates it onto the SPEC's `classify_task` algorithm.

Usage::

    python3 tools/fm/check-task-lifecycle-classification.py \\
        --task tasks/<NNN>-<slug>/task.md \\
        --target-status {updated,abandoned} \\
        [--goal-still-desirable] [--plan-drifted]

Exit codes:
    0  — transition is justified (every required condition met).
    1  — transition is unjustified; diagnostics name the missing condition(s).
    2  — fatal usage error (e.g. unreadable task.md).
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))  # tools/ on path so `fm._core` resolves

from fm._core import read_fm, str_list, str_val  # noqa: E402


def _normalise_ref(ref: str) -> str:
    return ref.strip().strip('"').strip("'")


def _strip_id_prefix(folder_name: str) -> str:
    parts = folder_name.split("-", 1)
    if len(parts) == 2 and parts[0].isdigit():
        return parts[1]
    return folder_name


def _resolve_successor(
    ref: str,
    tasks_root: Path,
) -> tuple[Path | None, dict | None]:
    """Resolve `ref` (a task_id like `"022"` or a slug like `"foo-bar"`)
    to a `(task.md path, frontmatter)` pair, scanning `tasks_root`.
    Returns `(None, None)` if no folder matches."""
    ref = _normalise_ref(ref)
    if not ref:
        return None, None
    for folder in sorted(tasks_root.iterdir()):
        if not folder.is_dir():
            continue
        task_md = folder / "task.md"
        if not task_md.exists():
            continue
        # Match by folder-name prefix (NNN-) or by frontmatter task_id / slug.
        folder_id = folder.name.split("-", 1)[0]
        folder_slug = _strip_id_prefix(folder.name)
        if ref in (folder_id, folder.name, folder_slug):
            return task_md, read_fm(task_md, strict=False)
        fm = read_fm(task_md, strict=False)
        if _normalise_ref(str_val(fm, "task_id")) == ref:
            return task_md, fm
    return None, None


def _check_updated(
    task_path: Path,
    fm: dict,
    *,
    goal_still_desirable: bool,
    plan_drifted: bool,
) -> list[tuple[str, str]]:
    """Return a list of (severity, message) failures for an `updated`
    transition. Empty list means PASS."""
    diags: list[tuple[str, str]] = []
    tasks_root = task_path.parent.parent

    # Condition 1 — agent attestation.
    if not goal_still_desirable:
        diags.append((
            "ERROR",
            "§4.7(1): Goal-still-desirable not attested. Re-run with "
            "--goal-still-desirable after reading the predecessor's Goal "
            "section. If the Goal is no longer desirable, the correct "
            "transition is `abandoned` (§8.3).",
        ))

    # Condition 2 — agent attestation + heuristic.
    if not plan_drifted:
        diags.append((
            "ERROR",
            "§4.7(2): Plan/Todo-drifted not attested. Re-run with "
            "--plan-drifted after confirming the Plan no longer reflects "
            "the current repo state. If the Plan executed cleanly to "
            "completion, the correct transition is `done` (§4.6).",
        ))
    body = task_path.read_text(encoding="utf-8")
    todo_lines = [l for l in body.splitlines() if l.lstrip().startswith("- [")]
    if todo_lines:
        unchecked = [l for l in todo_lines if l.lstrip().startswith("- [ ]")]
        if not unchecked:
            diags.append((
                "WARN",
                "§4.7(2) heuristic: every Todo item is already checked "
                "(`[x]`). This suggests `done` is the correct closure "
                "rather than `updated`. Verify that the *plan* (not just "
                "the todo list) has drifted before proceeding.",
            ))

    # Condition 3 — mechanical: task_superseded_by non-empty + resolvable.
    superseded_by = [_normalise_ref(s) for s in str_list(fm, "task_superseded_by")]
    successors: list[tuple[Path, dict]] = []
    if not superseded_by:
        diags.append((
            "ERROR",
            "§4.7(3): `task_superseded_by` MUST be non-empty for an "
            "`updated` transition. Add the successor's task_id or slug "
            "before re-running.",
        ))
    else:
        for ref in superseded_by:
            spath, sfm = _resolve_successor(ref, tasks_root)
            if spath is None or sfm is None:
                diags.append((
                    "ERROR",
                    f"§4.7(3): successor reference {ref!r} does not "
                    f"resolve to any tasks/<NNN>-<slug>/task.md under "
                    f"{tasks_root}.",
                ))
            else:
                successors.append((spath, sfm))

    # Condition 4 — mechanical: reciprocity. Every successor must cite this
    # Task's task_id (or slug) in its `task_supersedes`.
    self_id = _normalise_ref(str_val(fm, "task_id"))
    self_slug = task_path.parent.name
    self_slug_short = _strip_id_prefix(self_slug)
    self_refs = {self_id, self_slug, self_slug_short}
    for spath, sfm in successors:
        successor_supersedes = {
            _normalise_ref(s) for s in str_list(sfm, "task_supersedes")
        }
        if not (successor_supersedes & self_refs):
            diags.append((
                "ERROR",
                f"§4.7(4): supersession reciprocity broken. Successor "
                f"{spath} does not cite this Task's task_id ({self_id}) "
                f"or slug in its `task_supersedes`. Update the successor "
                f"frontmatter before re-running.",
            ))
    return diags


def _check_abandoned(task_path: Path, fm: dict) -> list[tuple[str, str]]:
    """Return failures for an `abandoned` transition (TASK.md §8.3)."""
    diags: list[tuple[str, str]] = []
    notes = task_path.parent / "notes.md"
    if not notes.exists():
        diags.append((
            "ERROR",
            "§8.3(A1): notes.md MUST exist in the Task folder before "
            "transitioning to `abandoned`. Author it with the abandonment "
            "reason and last reproducible state.",
        ))
        return diags
    body = notes.read_text(encoding="utf-8").lower()
    has_reason = "abandon" in body or "## partial artifacts" in body
    if not has_reason:
        diags.append((
            "ERROR",
            "§8.3(A2): notes.md does not contain an abandonment rationale "
            "(no occurrence of the word 'abandon' or a '## Partial "
            "Artifacts' heading). Append a dated entry stating the reason.",
        ))
    return diags


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description="Evaluate TASK.md §4.7 four-condition test for a "
                    "Task transitioning to `updated` or `abandoned`.",
    )
    ap.add_argument("--task", required=True, type=Path,
                    help="Path to tasks/<NNN>-<slug>/task.md")
    ap.add_argument("--target-status", required=True,
                    choices=["updated", "abandoned"],
                    help="Proposed task_status target.")
    ap.add_argument("--goal-still-desirable", action="store_true",
                    help="Agent attestation that §4.7(1) holds.")
    ap.add_argument("--plan-drifted", action="store_true",
                    help="Agent attestation that §4.7(2) holds.")
    args = ap.parse_args(argv)

    if not args.task.exists():
        print(f"check-task-lifecycle-classification: {args.task}: not found",
              file=sys.stderr)
        return 2

    fm = read_fm(args.task, strict=False)
    if not fm:
        print(f"check-task-lifecycle-classification: {args.task}: "
              f"missing or unparseable frontmatter", file=sys.stderr)
        return 2

    if args.target_status == "updated":
        diags = _check_updated(
            args.task, fm,
            goal_still_desirable=args.goal_still_desirable,
            plan_drifted=args.plan_drifted,
        )
    else:
        diags = _check_abandoned(args.task, fm)

    errors = [d for d in diags if d[0] == "ERROR"]
    warns = [d for d in diags if d[0] == "WARN"]

    for sev, msg in diags:
        stream = sys.stderr if sev == "ERROR" else sys.stdout
        print(f"check-task-lifecycle-classification: {sev}: {msg}",
              file=stream)

    if errors:
        print(
            f"check-task-lifecycle-classification: FAIL — "
            f"transition `{args.target_status}` is unjustified "
            f"({len(errors)} ERROR(s), {len(warns)} WARN(s)).",
            file=sys.stderr,
        )
        return 1
    print(
        f"check-task-lifecycle-classification: PASS — transition "
        f"`{args.target_status}` is justified ({len(warns)} WARN(s))."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
