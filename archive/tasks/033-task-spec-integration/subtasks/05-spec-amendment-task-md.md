---
type: note
status: draft
slug: task-033-st5-spec-amendment-task-md
summary: "Subtask ST-5 (Phase B): apply the TASK.md edits — §3.3 cross-reference + skill_*/adr_* L2 subsections, §6 supersession-blocker Gherkin, §4.7 algorithm refinement, §8.1 enforcement note."
created: 2026-05-06
updated: 2026-05-06
---

# ST-5: Spec Amendment — TASK.md

**Executor:** main-agent

**Parallelism:** Phase B (sequential) — depends on ST-1, ST-2, ST-3 (and soft-depends on ST-4). MUST wait for Phase A converge.

**Prompt:** [`/prompts/spec-amendment-task-md/prompt.md`](../../../prompts/spec-amendment-task-md/prompt.md) — the executable instruction set for this subtask. The Goal, Falsification, Inputs, Acceptance Criteria, Dependencies, and Estimated Effort sections that previously lived inline have moved to that prompt's [`brief.md`](../../../prompts/spec-amendment-task-md/brief.md) per Task 041 (PR #70 review C.3 audit-graph repair).
