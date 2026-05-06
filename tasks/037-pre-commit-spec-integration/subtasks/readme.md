---
type: index
status: active
slug: task-037-subtasks-index
summary: "Subtask index for Task 037 — PRE_COMMIT.md spec integration. Phase A: 1 research (shared with Task 038) + 2 tooling. Phase B: 1 spec amendment."
created: 2026-05-06
updated: 2026-05-06
---

# Task 037 — Subtask Index

## Phase A — Parallel

| ID | File | Recommended agent | Effort |
|---|---|---|---|
| ST-1 | [`01-research-pre-commit-readme-update-cadence.md`](./01-research-pre-commit-readme-update-cadence.md) | research-prompt-optimizer + deep-research | M |
| ST-2 | [`02-tooling-clean-working-directory-linter.md`](./02-tooling-clean-working-directory-linter.md) | python-expert | S |
| ST-3 | [`03-tooling-per-rule-waiver-mechanism.md`](./03-tooling-per-rule-waiver-mechanism.md) | python-expert | M |

## Phase B — Sequential

| ID | File | Depends on | Recommended agent | Effort |
|---|---|---|---|---|
| ST-4 | [`04-spec-amendment-pre-commit-md.md`](./04-spec-amendment-pre-commit-md.md) | ST-1, ST-2, ST-3, Task 038 ST-3 (joint wording) | technical-writer | M |
