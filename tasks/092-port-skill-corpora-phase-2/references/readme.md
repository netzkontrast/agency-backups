---
type: index
status: active
slug: task-092-references
summary: "References directory for Task 092 (Phase 2 skill-corpora port). Populated during ST-1 triage with the canonical decision matrix + per-skill notes; empty pre-ST-1."
created: 2026-05-12
updated: 2026-05-12
---

# Task 092 — References

**What:** Container for the ST-1 triage outputs. Two artifacts land here when ST-1 runs:

- `triage-matrix.md` — single canonical decision matrix; one row per snapshot candidate; columns: `# | Snapshot path | Proposed Agency slug | Tier | Decision | ADR-0011 clauses | Rationale`.
- `triage-notes/<vendor>-<slug>.md` — per-skill rationale longer than one line (optional; only when needed).

**Why here:** Per [TASK.md §3.4](../../../TASK.md) `task_spawns_research: []` (Task 092 does not spawn an external research workspace), so triage outputs live inside the Task folder. The decision matrix is referenced by ST-2 + ST-3 as the source of truth for which items to port.

## Contents (pre-ST-1)

This folder is currently empty apart from this readme. ST-1 ([`../subtasks/01-triage.md`](../subtasks/01-triage.md)) authors the matrix and notes.

## Assumptions Log

- Triage citations MUST resolve to local paths under `tasks/091-…/references/upstream-snapshot/` — per [Task 092 Note](../task.md#note--internal-research-only), external GitHub URLs are an anti-pattern for this Epic.
- Once ST-2 and ST-3 close, the matrix becomes historical — it documents the rationale for what shipped and what was skipped, but the source of truth for "what is a Phase 2 skill" shifts to `/skills/sc-*/` and `/skills/superpowers-*/`. The matrix MUST NOT be edited after ST-4 closes (effectively T4 once the Epic is `done`).
