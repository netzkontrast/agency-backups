---
type: index
status: active
slug: task-091-subtasks-index
summary: "Subtask index for Task 091 Epic. Two sequential subtasks: ST-1 (corpus) → ST-2 (hookup) per ADR-0011 + OQ1 resolution."
created: 2026-05-12
updated: 2026-05-12
---

# Task 091 — Subtask Index

Per ADR-0011 + OQ1 resolution (`../references/full-plan-part-3.md` §9.7), Phase 1 ships as **two sequential subtasks**. The corpus lands first (skills + validator); the root-spec hookup lands after corpus merges to `main`. This shape matches the Agency precedent for two-PR feature work where the second PR depends on real local files materialised by the first.

## Phase 1 — Sequential

| ID | File | Depends on | Recommended agent | Effort |
|---|---|---|---|---|
| ST-1 | [`01-phase-1-corpus.md`](./01-phase-1-corpus.md) | ADR-0011 Accepted | claude-code with `/sc:implement` | M (14 skills + validator + tests) |
| ST-2 | [`02-phase-1-hookup.md`](./02-phase-1-hookup.md) | ST-1 merged to `main` | claude-code with `/sc:implement` | XS (2 small file edits) |

Each subtask file links to the canonical spec in [`../references/full-plan-part-4.md` §10.5](../references/full-plan-part-4.md) and inlines its Gherkin AC anchors (`TA.1.*` for ST-1, `TB.1.*` for ST-2).

## Out of scope at the subtask level

The following are out of scope for both subtasks (covered in parent Epic [`../task.md`](../task.md) §"Plan" steps 6 / 7 / 8 and in the planning record's §8 / §9.8):

- Phase 2 (workflow loops: TDD discipline, systematic debugging, writing-plans, reflect-into-friction-log) — sequenced after this Epic.
- Phase 3 (remaining must-haves + Superpowers corpus) — sequenced after Phase 2.
- Auto-sync from upstream — future ADR.
- MCP installer packaging — Agency does not ship installers.
