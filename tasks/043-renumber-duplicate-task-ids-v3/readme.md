---
type: index
status: active
slug: task-043-renumber-duplicate-task-ids-v3
summary: "Directory index for Task 043: third renumber Task in the lineage 013 → 024 → 043, addressing the May 2026 duplicate-task_id collisions on slots 031 and 032."
created: 2026-05-07
updated: 2026-05-07
---

# Task 043 — Renumber Duplicate task_id Values (v3)

## Files

- [`task.md`](./task.md) — Goal, Plan, Todo, Links.

## Context

Two on-disk duplicate-`task_id` collisions surfaced after the May 2026 merge wave (Tasks 030 / 031 / 032–039 / 040 / 041 / 042 landing in close sequence):

- `task_id: "031"` shared by `tasks/031-adr-tooling-impl/` and `tasks/031-sync-tasks-index-status-drift/`.
- `task_id: "032"` shared by `tasks/032-agents-spec-integration/` and `tasks/032-improve-maintenance-spec-may-2026/`.

The collisions match the same root pattern Tasks 013 and 024 addressed: parallel branches each picked the locally-next-free `<NNN>` against their own branch state without a pre-merge mechanical gate against `origin/main`. Resolved manually each time per [MAINTENANCE.md §3.5](../../MAINTENANCE.md), with the spec-bearing rule in [TASK.md §8.1](../../TASK.md) carrying agent responsibility.

## Status

`task_status: open` (filed by coherence run 2026-05-07).
