---
type: index
status: active
slug: task-048-subtasks-index
summary: "Subtask index for Task 048 — Task Tooling Implementation SPEC. Phase A (parallel): 2 research subtasks. Phase B (sequential): 1 SPEC synthesis."
created: 2026-05-07
updated: 2026-05-07
---

# Task 048 — Subtask Index

## Phase A — Parallel

| ID | File | Recommended agent | Effort |
|---|---|---|---|
| ST-1 | [`01-research-skills-corpus-inspiration.md`](./01-research-skills-corpus-inspiration.md) | deep-research | M |
| ST-2 | [`02-research-existing-task-tooling-inventory.md`](./02-research-existing-task-tooling-inventory.md) | deep-research | M |

## Phase B — Sequential

| ID | File | Depends on | Recommended agent | Effort |
|---|---|---|---|---|
| ST-3 | [`03-spec-task-tooling-impl.md`](./03-spec-task-tooling-impl.md) | ST-1, ST-2 | system-architect or technical-writer | L |

## Assumptions Log

- ST-1 and ST-2 are independent and SHOULD run concurrently; ST-3 waits for both Phase-A SPECs to land.
- Each subtask points to a `/prompts/<slug>/` artefact (per the Task 041 audit-graph repair pattern). The prompts MAY be authored at dispatch time rather than upfront — TASK.md §7.3 enforces `task_uses_prompts` resolution only on closure.
