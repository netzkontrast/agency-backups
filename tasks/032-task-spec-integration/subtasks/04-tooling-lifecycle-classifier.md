---
type: note
status: draft
slug: task-032-st4-tooling-lifecycle-classifier
summary: "Subtask ST-4: ship tools/fm/check-task-lifecycle-classification.py — a helper that, given a Task in transition to `updated` or `abandoned`, evaluates the §4.7 four-condition test deterministically per the algorithm produced by Task 032 ST-2."
created: 2026-05-06
updated: 2026-05-06
---

# ST-4: `check-task-lifecycle-classification` — TASK.md §4.7 Helper

## Goal

Ship `tools/fm/check-task-lifecycle-classification.py` that, given a Task path and a proposed `task_status` transition, evaluates the four conditions in TASK.md §4.7 (Goal still desirable / Plan-Todo drifted / successor exists / supersession reciprocity) and outputs PASS or FAIL with the missing condition(s). Built atop the algorithm SPEC produced by Task 032 ST-2.

## Falsification

Wrong cut **iff** the classifier cannot evaluate "Goal is still desirable?" mechanically. Mitigation: ST-2 SPEC §1 reduces this predicate to git-extractable signals (no LLM judgment).

## Inputs

- [`TASK.md`](../../../TASK.md) §4.7.
- `research/spec-staleness-decision-formalization/output/SPEC.md` (output of ST-2 — required input).
- `tools/fm/_core.py`.

## Acceptance Criteria

1. **Surface.** `python3 tools/fm/check-task-lifecycle-classification.py --task <path> --target-status {updated,abandoned}` exits 0 (transition justified) or 1 (transition unjustified, with diagnostic).
2. **Algorithm.** Implements the deterministic decision tree from ST-2 SPEC §1.
3. **Tests.** `tests/fm/test_lifecycle_classification.py` covers each of the four conditions in isolation + integration walk-throughs from ST-2 SPEC §3.
4. **Integration.** Optional helper invoked manually by maintenance agents; not part of `tools/check-governance.sh`.

## Dependencies

ST-2 (research) MUST land first. Phase B-within-A: blocked on ST-2 output.

## Estimated Effort

Small (~80 LOC + 80 LOC tests; the algorithm work is ST-2's job).

## Agent Prompt

```text
Implement tools/fm/check-task-lifecycle-classification.py.

Repo root: /home/user/agency
Branch: claude/integrate-repo-specs-cIWtI

Pre-flight check:
  test -f research/spec-staleness-decision-formalization/output/SPEC.md
If absent, abort with message "ST-2 not landed; rerun after Task 032 ST-2 completes."

Read first: research/spec-staleness-decision-formalization/output/SPEC.md §1+§3,
TASK.md §4.7, tools/fm/_core.py.

Acceptance: as documented above.

When done:
  python3 -m unittest discover -s tests/fm
  Commit "feat(tools/fm): task-lifecycle classifier (Task 032 ST-4)".
  Do NOT push.
```
