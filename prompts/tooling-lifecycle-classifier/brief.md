---
type: brief
status: active
slug: tooling-lifecycle-classifier-brief
summary: "Brief for prompt tooling-lifecycle-classifier — extracted from tasks/033-task-spec-integration/subtasks/04-tooling-lifecycle-classifier.md per Task 041 (PR #70 review C.3 audit-graph repair)."
created: 2026-05-06
updated: 2026-05-06
---

# Brief — ST-4: `check-task-lifecycle-classification` — TASK.md §4.7 Helper

## Raw User Request

> Extract the inlined Execution Brief from `tasks/033-task-spec-integration/subtasks/04-tooling-lifecycle-classifier.md` (ST-4) into a registered `/prompts/<slug>/` artefact, restoring the `task_uses_prompts ↔ prompt_relates_to_task` audit-graph edge severed in PR #70 (review finding C.3).

## Target Audience

The dispatched executor for [Task 033 `task-spec-integration`](../../tasks/033-task-spec-integration/task.md), specifically subtask ST-4 (04-tooling-lifecycle-classifier.md). Default executor: **main-agent**.

## Intended Model / Agent

Claude Code (or any agent that satisfies the executor declaration in the parent subtask file).

## Use-Case Context

This prompt drives subtask ST-4 of [Task task-spec-integration](../../tasks/033-task-spec-integration/task.md). The parent task's chain-level rationale lives in its `task.md`; this brief records only the subtask's local goal + inputs + acceptance + dependencies + effort, lifted verbatim from the subtask file at extraction time.

**Parallelism:** Phase A (parallel-grouped, soft-blocked) — sibling of ST-1/ST-2/ST-3 but blocked on ST-2 SPEC output. Runs after ST-2 (or Task 039 ST-2) lands.

**Insertion point:** (none) — manual helper invoked by maintenance agents only; not part of `tools/check-governance.sh`.

## Goal (from subtask)

Ship `tools/fm/check-task-lifecycle-classification.py` that, given a Task path and a proposed `task_status` transition, evaluates the four conditions in TASK.md §4.7 (Goal still desirable / Plan-Todo drifted / successor exists / supersession reciprocity) and outputs PASS or FAIL with the missing condition(s). Built atop the algorithm SPEC produced by Task 033 ST-2.

## Falsification (from subtask)

Wrong cut **iff** the classifier cannot evaluate "Goal is still desirable?" mechanically. Mitigation: ST-2 SPEC §1 reduces this predicate to git-extractable signals (no LLM judgment).

## Inputs (from subtask)

- [`TASK.md`](../../../TASK.md) §4.7.
- `research/spec-staleness-decision-formalization/output/SPEC.md` (output of ST-2 — required input).
- `tools/fm/_core.py`.

## Acceptance Criteria (from subtask)

1. **Surface.** `python3 tools/fm/check-task-lifecycle-classification.py --task <path> --target-status {updated,abandoned}` exits 0 (transition justified) or 1 (transition unjustified, with diagnostic).
2. **Algorithm.** Implements the deterministic decision tree from ST-2 SPEC §1.
3. **Tests.** `tests/fm/test_lifecycle_classification.py` covers each of the four conditions in isolation + integration walk-throughs from ST-2 SPEC §3.
4. **Integration.** Optional helper invoked manually by maintenance agents; not part of `tools/check-governance.sh`.

## Dependencies (from subtask)

ST-2 (research) MUST land first. Phase B-within-A: blocked on ST-2 output.

## Estimated Effort (from subtask)

Small (~80 LOC + 80 LOC tests; the algorithm work is ST-2's job).
