---
type: index
status: active
slug: task-039-subtasks-index
summary: "Subtask index for Task 039 — MAINTENANCE.md spec integration. Phase A: 2 research + 3 tooling. Phase B: 1 spec amendment."
created: 2026-05-06
updated: 2026-05-06
---

# Task 039 — Subtask Index

## Phase A — Parallel

| ID | File | Recommended agent | Effort |
|---|---|---|---|
| ST-1 | [`01-research-toolchain-flip-criteria.md`](./01-research-toolchain-flip-criteria.md) | research-prompt-optimizer + deep-research | M |
| ST-2 | [`02-research-staleness-decision-formalization.md`](./02-research-staleness-decision-formalization.md) | research-prompt-optimizer + deep-research | M |
| ST-3 | [`03-tooling-staleness-audit-script.md` (briefing pending — author before dispatch) | python-expert | M |
| ST-4 | [`04-tooling-dynamic-readme-partition-linter.md` (briefing pending — author before dispatch) | python-expert | M |
| ST-5 | [`05-tooling-trust-audit-integration.md` (briefing pending — author before dispatch) | python-expert | M |

> **Trust-audit partition (per spec-panel C3):** ST-5 here owns the
> **AGGREGATOR** — cross-research roll-up of the per-workspace findings
> emitted by [Task 035 ST-4](../../035-research-spec-integration/subtasks/readme.md).
> ST-5 MUST import (not duplicate) the diagnostic-schema and per-workspace
> linter from Task 035 ST-4. Aggregator output is what MAINTENANCE.md §3.2
> consumes during the nightly run; it surfaces FL[1-3]-equivalent trust
> failures across all `research/<slug>/` workspaces and delegates them to
> the Task pipeline per the existing friction-aggregation contract.

## Phase B — Sequential

| ID | File | Depends on | Recommended agent | Effort |
|---|---|---|---|---|
| ST-6 | [`06-spec-amendment-maintenance-md.md` (briefing pending — author before dispatch) | ST-1, ST-2, ST-3, ST-4, ST-5 | technical-writer | L |
