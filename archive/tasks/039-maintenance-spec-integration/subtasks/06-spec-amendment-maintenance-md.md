---
type: note
status: draft
slug: task-039-st6-spec-amendment-maintenance-md
summary: "Subtask ST-6 (Phase B): apply MAINTENANCE.md edits — §1.1.2 three-way Legacy/Flexible/ADR table, §2.3 trust-audit gate, §3.2 dynamic-readme partition, §3.4 deterministic algorithm, §3.5 dup-id resolution, §1 ADR T4-immutability, ≥7 Gherkin per M.B.1-M.B.7."
created: 2026-05-06
updated: 2026-05-06
---

# ST-6: Spec Amendment — MAINTENANCE.md

**Executor:** main-agent

**Parallelism:** Phase B (sequential) — depends on ST-1, ST-2, ST-3, ST-4, ST-5. MUST wait for all five Phase A subtasks to land.

**Prompt:** [`/prompts/spec-amendment-maintenance-md/prompt.md`](../../../prompts/spec-amendment-maintenance-md/prompt.md) — the executable instruction set for this subtask. The Goal, Falsification, Inputs, Acceptance Criteria, Dependencies, and Estimated Effort sections that previously lived inline have moved to that prompt's [`brief.md`](../../../prompts/spec-amendment-maintenance-md/brief.md) per Task 041 (PR #70 review C.3 audit-graph repair).
