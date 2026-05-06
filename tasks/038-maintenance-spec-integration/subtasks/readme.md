---
type: index
status: active
slug: task-038-subtasks-index
summary: "Subtask index for Task 038 — MAINTENANCE.md spec integration. Phase A: 2 research + 3 tooling. Phase B: 1 spec amendment."
created: 2026-05-06
updated: 2026-05-06
---

# Task 038 — Subtask Index

## Phase A — Parallel

| ID | File | Recommended agent | Effort |
|---|---|---|---|
| ST-1 | [`01-research-toolchain-flip-criteria.md`](./01-research-toolchain-flip-criteria.md) | research-prompt-optimizer + deep-research | M |
| ST-2 | [`02-research-staleness-decision-formalization.md`](./02-research-staleness-decision-formalization.md) | research-prompt-optimizer + deep-research | M |
| ST-3 | [`03-tooling-staleness-audit-script.md`](./03-tooling-staleness-audit-script.md) | python-expert | M |
| ST-4 | [`04-tooling-dynamic-readme-partition-linter.md`](./04-tooling-dynamic-readme-partition-linter.md) | python-expert | M |
| ST-5 | [`05-tooling-trust-audit-integration.md`](./05-tooling-trust-audit-integration.md) | python-expert | M |

## Phase B — Sequential

| ID | File | Depends on | Recommended agent | Effort |
|---|---|---|---|---|
| ST-6 | [`06-spec-amendment-maintenance-md.md`](./06-spec-amendment-maintenance-md.md) | ST-1, ST-2, ST-3, ST-4, ST-5 | technical-writer | L |
