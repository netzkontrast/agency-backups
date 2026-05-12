---
type: note
status: draft
slug: task-033-st4-tooling-lifecycle-classifier
summary: "Subtask ST-4: ship tools/fm/check-task-lifecycle-classification.py — a helper that, given a Task in transition to `updated` or `abandoned`, evaluates the §4.7 four-condition test deterministically per the algorithm produced by Task 033 ST-2."
created: 2026-05-06
updated: 2026-05-06
---

# ST-4: `check-task-lifecycle-classification` — TASK.md §4.7 Helper

**Executor:** main-agent
**Insertion point:** (none) — manual helper invoked by maintenance agents only; not part of `tools/check-governance.sh`.

**Parallelism:** Phase A (parallel-grouped, soft-blocked) — sibling of ST-1/ST-2/ST-3 but blocked on ST-2 SPEC output. Runs after ST-2 (or Task 039 ST-2) lands.

**Prompt:** [`/prompts/tooling-lifecycle-classifier/prompt.md`](../../../prompts/tooling-lifecycle-classifier/prompt.md) — the executable instruction set for this subtask. The Goal, Falsification, Inputs, Acceptance Criteria, Dependencies, and Estimated Effort sections that previously lived inline have moved to that prompt's [`brief.md`](../../../prompts/tooling-lifecycle-classifier/brief.md) per Task 041 (PR #70 review C.3 audit-graph repair).
