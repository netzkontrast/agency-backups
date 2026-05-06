---
type: index
status: active
slug: task-034-subtasks-index
summary: "Subtask index for Task 034 — RESEARCH.md spec integration. Phase A: 1 research head + 3 tooling. Phase B: 1 spec amendment."
created: 2026-05-06
updated: 2026-05-06
---

# Task 034 — Subtask Index

## Phase A — Parallel

| ID | File | Recommended agent | Effort |
|---|---|---|---|
| ST-1 | [`01-research-session-continuity-protocol-instantiation.md`](./01-research-session-continuity-protocol-instantiation.md) | research-prompt-optimizer + deep-research | L |
| ST-2 | [`02-tooling-workspace-cleanliness-linter.md`](./02-tooling-workspace-cleanliness-linter.md) | python-expert | S |
| ST-3 | [`03-tooling-external-result-downstream-task-linter.md`](./03-tooling-external-result-downstream-task-linter.md) | python-expert | S |
| ST-4 | [`04-tooling-trust-audit-gate.md`](./04-tooling-trust-audit-gate.md) | python-expert | M |

## Phase B — Sequential

| ID | File | Depends on | Recommended agent | Effort |
|---|---|---|---|---|
| ST-5 | [`05-spec-amendment-research-md.md`](./05-spec-amendment-research-md.md) | ST-1, ST-2, ST-3, ST-4 | technical-writer | M |
