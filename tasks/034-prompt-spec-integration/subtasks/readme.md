---
type: index
status: completed
slug: task-034-subtasks-index
summary: "Subtask index for Task 034 — PROMPT.md spec integration. Phase A: 1 research head + 2 tooling. Phase B: 1 spec amendment."
created: 2026-05-06
updated: 2026-05-07
---

# Task 034 — Subtask Index

## Phase A — Parallel

| ID | File | Recommended agent | Effort |
|---|---|---|---|
| ST-1 | [`01-research-prompt-engineering-principle-mechanizability.md`](./01-research-prompt-engineering-principle-mechanizability.md) | research-prompt-optimizer + deep-research | M |
| ST-2 | [`02-tooling-self-containedness-checker.md`](./02-tooling-self-containedness-checker.md) | python-expert | M |
| ST-3 | [`03-tooling-framework-declaration-validator.md`](./03-tooling-framework-declaration-validator.md) | python-expert | S |

## Phase B — Sequential

| ID | File | Depends on | Recommended agent | Effort |
|---|---|---|---|---|
| ST-4 | [`04-spec-amendment-prompt-md.md`](./04-spec-amendment-prompt-md.md) | ST-1, ST-2, ST-3 | technical-writer | M |
