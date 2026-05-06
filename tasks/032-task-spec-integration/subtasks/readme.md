---
type: index
status: active
slug: task-032-subtasks-index
summary: "Subtask index for Task 032 — TASK.md spec integration. Phase A (parallel): 2 research heads + 2 tooling. Phase B: 1 spec amendment."
created: 2026-05-06
updated: 2026-05-06
---

# Task 032 — Subtask Index

## Phase A — Parallel

| ID | File | Recommended agent | Effort |
|---|---|---|---|
| ST-1 | [`01-research-friction-pattern-synthesis.md`](./01-research-friction-pattern-synthesis.md) | research-prompt-optimizer + deep-research | L |
| ST-2 | [`02-research-spec-staleness-decision-formalization.md`](./02-research-spec-staleness-decision-formalization.md) | research-prompt-optimizer + deep-research | M |
| ST-3 | [`03-tooling-duplicate-task-id-linter.md`](./03-tooling-duplicate-task-id-linter.md) | python-expert | S |
| ST-4 | [`04-tooling-lifecycle-classifier.md`](./04-tooling-lifecycle-classifier.md) | python-expert | S |

## Phase B — Sequential

| ID | File | Depends on | Recommended agent | Effort |
|---|---|---|---|---|
| ST-5 | [`05-spec-amendment-task-md.md`](./05-spec-amendment-task-md.md) | ST-1, ST-2, ST-3 | technical-writer | M |
