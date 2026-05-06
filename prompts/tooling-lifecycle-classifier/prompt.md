---
type: prompt
status: active
slug: tooling-lifecycle-classifier
summary: "Ship `tools/fm/check-task-lifecycle-classification.py` that, given a Task path and a proposed `task_status` transition, evaluates the four conditions in TASK.md §4.7 (Goal still desirable / Plan-Todo drifted / successor exists / superses..."
created: 2026-05-06
updated: 2026-05-06
prompt_kind: task-spec
prompt_framework: RISEN+ReAct
prompt_target_agent: "Claude Code"
prompt_relates_to_task: task-spec-integration
prompt_spawned_from_research: ""
---

# ST-4: `check-task-lifecycle-classification` — TASK.md §4.7 Helper — Task-Spec Prompt

## Framework

RISEN+ReAct. The prompt declares the framework in frontmatter (`prompt_framework: RISEN+ReAct`) and restates it here for `fm-validate` header conformance. The R/I/S/E sections below carry the canonical roles; a final **Constraints** section groups normative scope/failure rules per repo convention.

## R — Role

You are the **main-agent** dispatched to execute subtask ST-4 of [Task task-spec-integration](../../tasks/033-task-spec-integration/task.md). Your remit is bounded by the Acceptance Criteria in [`brief.md`](./brief.md); you MUST NOT expand scope beyond those criteria without surfacing the divergence in `friction-log.md`.

**Parallelism:** Phase A (parallel-grouped, soft-blocked) — sibling of ST-1/ST-2/ST-3 but blocked on ST-2 SPEC output. Runs after ST-2 (or Task 039 ST-2) lands..

## I — Input

- [`TASK.md`](../../../TASK.md) §4.7.
- `research/spec-staleness-decision-formalization/output/SPEC.md` (output of ST-2 — required input).
- `tools/fm/_core.py`.
- `tasks/033-task-spec-integration/task.md` — parent task chain-level context.

## S — Steps

1. Execute the following instruction block faithfully — it is the verbatim Execution Brief from the parent subtask file:

```text
Implement tools/fm/check-task-lifecycle-classification.py.


Pre-flight check:
  test -f research/spec-staleness-decision-formalization/output/SPEC.md
If absent, abort with message "ST-2 not landed; rerun after Task 033 ST-2 completes."

Read first: research/spec-staleness-decision-formalization/output/SPEC.md §1+§3,
TASK.md §4.7, tools/fm/_core.py.

Acceptance: as documented above.

When done:
  python3 -m unittest discover -s tests/fm
  Commit "feat(tools/fm): task-lifecycle classifier (Task 033 ST-4)".
  Do NOT push.
```
2. Verify every Acceptance Criterion in [`brief.md`](./brief.md) is satisfied by the produced artefacts.
3. Run `tools/check-governance.sh` and resolve every ERROR before committing.

## E — Expectations

- **Surface.** `python3 tools/fm/check-task-lifecycle-classification.py --task <path> --target-status {updated,abandoned}` exits 0 (transition justified) or 1 (transition unjustified, with diagnostic).
- **Algorithm.** Implements the deterministic decision tree from ST-2 SPEC §1.
- **Tests.** `tests/fm/test_lifecycle_classification.py` covers each of the four conditions in isolation + integration walk-throughs from ST-2 SPEC §3.
- **Integration.** Optional helper invoked manually by maintenance agents; not part of `tools/check-governance.sh`.
- `tools/check-governance.sh` exits 0 on the produced commit.
- Commit message follows the parent task's convention; the commit cites `Task 033 ST-4` in its trailer.

## Constraints

- Dependency: ST-2 (research) MUST land first. Phase B-within-A: blocked on ST-2 output.
- MUST NOT trigger the subtask's Falsification clause: Wrong cut **iff** the classifier cannot evaluate "Goal is still desirable?" mechanically. Mitigation: ST-2 SPEC §1 reduces this predicate to git-extractable signals (no LLM judgment).
- MUST NOT inline this prompt's Goal/Inputs/Acceptance back into the subtask file — the subtask body is now a thin pointer per Task 041.
- MUST run `tools/check-governance.sh` before pushing; a non-zero exit MUST block the push.
- SHOULD cite the parent task's `task_id` in any commit-message trailer for traceability.
