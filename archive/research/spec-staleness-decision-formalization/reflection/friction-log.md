---
type: note
status: active
slug: friction-log
summary: "Friction log for the spec-staleness-decision-formalization research run (Task 033 ST-2 / Task 039 ST-2)."
created: 2026-05-07
updated: 2026-05-07
---

# Friction Log

**Highest Frustration Level: FL0**

## Summary

The research executed cleanly. Inputs (`MAINTENANCE.md §3.4`, `TASK.md §4.7`, the four worked-example tasks) were already coherent — the four-bucket symptom table in `§3.4` and the four §4.7 conditions are 1:1, so the algorithm essentially fell out of the existing spec. No backtracking, no contradictions surfaced, no tooling friction.

## Notes

- The decision tree fits in 16 lines of executable pseudocode (3 levels, 4 leaves) — well inside the falsification bound (≤5 levels, ≤12 leaves).
- The signal set converged at five (S1..S5); the temptation to add a sixth ("commit recency on `task_affects_paths`") was rejected because none of the four buckets in §4.7 needs it — it would have been instrumentation, not decision input.
- Worked examples 022/023/024/025 all classify as STILL_ACCURATE on the 2026-05-07 baseline, which initially read as a thin regression suite. On reflection it is the *correct* steady-state outcome and is documented in §3 along with the fixture recipe ST-4 needs to exercise the other three buckets.
- The Task 025 nuance (Plan items landed but Todo checkboxes still unchecked) is the most interesting design pressure. Resolved by deferring to the checkbox state mechanically rather than smuggling LLM judgement into the classifier — the §3 nuance paragraph explains the trade-off.

## Suggested Follow-ups

None blocking. Two minor optional enhancements for ST-4 to consider (already noted in §6):
1. A `--explain <NNN>` mode for human review of a single Task's trace through §1.
2. Synthetic regression fixtures exercising the three buckets unrepresented in the live worked examples.

## Pre-existing Branch State

`tools/check-governance.sh` exits 1 on this branch independent of my changes — verified by stashing my untracked workspace and re-running. The three pre-existing ERRORs are:
- `tasks/046-github-workflow-research/task.md::ERROR:F.4.2:missing required heading '## Todo'`
- `tasks/readme.md::ERROR:T.7.11:045-readme-coherence-refresh folder present on disk but no bullet in index`
- `tasks/readme.md::ERROR:T.7.11:046-github-workflow-research folder present on disk but no bullet in index`

All three concern Tasks 045/046, which are outside this Task's scope. The brief explicitly forbids touching TASK.md / governance specs ("the parent task handles that"); `tasks/readme.md` is the Tasks index governance surface and Task 046's `task.md` is another Task's body. My workspace introduces ZERO new ERRORs (verified by `bash tools/check-governance.sh 2>&1 | grep -E "spec-staleness-decision-formalization"` returning only WARN-level optional-subdir hints, all addressed by adding empty `workspace/` and `synthesis/` placeholders).
