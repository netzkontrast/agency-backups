---
type: task
status: active
slug: renumber-duplicate-task-ids-v3
summary: "Successor pattern to Tasks 013/024. Two new duplicate-task_id collisions surfaced after the May 2026 merge wave: 031 (adr-tooling-impl ↔ sync-tasks-index-status-drift) and 032 (agents-spec-integration ↔ improve-maintenance-spec-may-2026). Renumber the later-created folder of each pair into the next free slots per TASK.md §8.1."
created: 2026-05-07
updated: 2026-05-07
task_id: "043"
task_status: open
task_owner: "unassigned"
task_priority: P1
task_uses_prompts: []
task_spawns_research: []
task_spawns_prompts: []
task_blocked_by: []
task_supersedes: []
task_superseded_by: []
task_affects_paths:
  - tasks/031-adr-tooling-impl/
  - tasks/031-sync-tasks-index-status-drift/
  - tasks/032-agents-spec-integration/
  - tasks/032-improve-maintenance-spec-may-2026/
  - tasks/readme.md
  - maintenance/run-log.md
---

# Task 043 — Renumber Duplicate task_id Values (v3)

Found by coherence run 2026-05-07. The repository has two unresolved duplicate-`task_id` collisions that survived the merge wave landing Tasks 030 / 031 / 032–039 / 040 / 041 / 042: every pair below has two on-disk folders sharing the same `task_id` value, in violation of [TASK.md §8.1](../../TASK.md):

| `task_id` | Folder A (earlier-created) | Folder B (later-created — to renumber) | Rationale |
|---|---|---|---|
| `"031"` | `tasks/031-adr-tooling-impl/` (PR #67 retroactive registration; `task_status: in_progress`) | `tasks/031-sync-tasks-index-status-drift/` (filed by coherence run 2026-05-06; `task_status: open`) | Pair member with the later-flowing on-disk lineage; renumbering the open Task disturbs less downstream linkage than renumbering the in-flight ADR task. |
| `"032"` | `tasks/032-agents-spec-integration/` (filed in PR #66 spec-integration chain; `task_status: open`) | `tasks/032-improve-maintenance-spec-may-2026/` (filed by coherence run 2026-05-06; `task_status: open`) | Pair member that emerged later via the same coherence-run pathway. The spec-integration chain is referenced by Tasks 033-039 as part of a coordinated 8-task chain; renumbering it would force a multi-Task rewrite. |

Both collisions match the recurrent pattern that Tasks 013 → 024 already addressed for `006` and `009`. The pattern recurs because the §8.1 cross-branch check is an agent obligation rather than a pre-merge mechanical gate.

## Goal

Every `task_id` value across `/tasks/*/task.md` MUST be unique. Specifically:

- `tasks/031-sync-tasks-index-status-drift/` MUST be renumbered to the next free slot (proposed: `044` if `043` and `044` are unclaimed at staging time; pick the next free pair otherwise).
- `tasks/032-improve-maintenance-spec-may-2026/` MUST be renumbered to the next free slot after the previous renumber (proposed: `045`).

The slugs MUST remain stable across the renumber per TASK.md §8.1; only the folder prefix and the `task_id` field change.

## Plan

1. **Lock current free slots.** Run `ls tasks/ | sort | tail` immediately before staging. If `044`/`045` are claimed (e.g. by another open coherence-run T3 Task), pick the next free pair and proceed.
2. **Rename folders.**
   - `git mv tasks/031-sync-tasks-index-status-drift tasks/044-sync-tasks-index-status-drift`
   - `git mv tasks/032-improve-maintenance-spec-may-2026 tasks/045-improve-maintenance-spec-may-2026`
3. **Update `task_id` fields.** Use `python3 tools/fm/edit.py --set task_id="044" tasks/044-.../task.md` and the equivalent for 045; bump `updated:` on the same call.
4. **Sweep cross-references.** `grep -rn "031-sync-tasks-index-status-drift\|032-improve-maintenance-spec-may-2026"` across the tree and update every hit. Also sweep `task_supersedes`, `task_superseded_by`, `task_blocked_by` lists for any references by `task_id` value (`"031"` / `"032"`); disambiguate by surrounding context.
5. **Update `tasks/readme.md`.** Move the bullets for the two renumbered Tasks to their new slot positions; bump `tasks/readme.md`'s `updated:` field; remove the duplicate-collision annotations added by the 2026-05-07 coherence run.
6. **Re-run linters.** `python3 tools/fm/validate.py --type-check` and `tools/check-governance.sh` MUST both exit 0 against the post-renumber tree before commit.
7. **Append run-log entry.** Document the renumber in `maintenance/run-log.md` per the precedent set by run-log entries `2026-05-04 session zVZBH` (006 collision) and the still-pending Task 024 closure for the 006/009 pair.
8. **Produce `friction-log.md`.** Mandatory FL[0-3] declaration per FRUSTRATED.md and TASK.md §7.7.

## Todo

- [ ] 1. Verify `044`/`045` (or next-free pair) are unclaimed at staging time.
- [ ] 2. Rename `031-sync-tasks-index-status-drift` → `044-sync-tasks-index-status-drift`; update `task_id`.
- [ ] 3. Rename `032-improve-maintenance-spec-may-2026` → `045-improve-maintenance-spec-may-2026`; update `task_id`.
- [ ] 4. Sweep cross-references (paths, `task_blocked_by`, `task_supersedes`, `task_superseded_by`, run-log entries, prompt back-links).
- [ ] 5. Update `tasks/readme.md` bullets and bump `updated:`.
- [ ] 6. Run `tools/check-governance.sh`; confirm 0 errors.
- [ ] 7. Append `maintenance/run-log.md` entry.
- [ ] 8. Produce `friction-log.md` with FL[0-3] declaration.

## Links

- Predecessors: [`Task 013`](../013-renumber-duplicate-task-ids/task.md), [`Task 024`](../024-renumber-duplicate-task-ids-v2/task.md).
- Spec rule: [`TASK.md §8.1`](../../TASK.md), [`MAINTENANCE.md §3.5`](../../MAINTENANCE.md).
- Found by: coherence-check run 2026-05-07 (see [`maintenance/run-log.md`](../../maintenance/run-log.md) entry).
- Governing specs: [`TASK.md`](../../TASK.md), [`MAINTENANCE.md`](../../MAINTENANCE.md).
