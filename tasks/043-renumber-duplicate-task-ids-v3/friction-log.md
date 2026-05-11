---
type: note
status: active
slug: renumber-duplicate-task-ids-v3-friction-log
summary: "Closure FL declaration for Task 043 — mechanical task_id renumber 031→067 and 032→068. Largest sweep of the three v1/v2/v3 renumbers; touched TASK.md, MAINTENANCE.md, and three live downstream tasks (044/048/064). No surprises."
created: 2026-05-11
updated: 2026-05-11
---

# Task 043 — Friction Log

Highest Frustration Level: FL0

## Notes

Mechanical execution of the prescribed plan. The original spec proposed slots `045`/`046`; both were claimed long before this Task ran (Task 045 `readme-coherence-refresh`, Task 046 `github-workflow-research`). Per the spec's "pick the next free pair" instruction, the renumbers landed at `067`/`068` (the next free pair above the `065`/`066` slots that Task 024 had just claimed in the same session).

The sweep was larger than Task 024's because the renumbered folders were referenced from:

- Two root specs (`TASK.md §7.0` row §7.11; `MAINTENANCE.md §3.4`) — both had live `[Task NNN](path)` markdown links pointing at the old slug-paths. Updated to point at the new locations; preserved the historical "Task 031/032" display text and added a parenthetical "(renumbered from NNN per Task 043)" pointer.
- One code comment (`tools/fm/index_diff.py:58`) — example folder name in a `@dataclass` doc-comment. Updated for accuracy.
- Three live downstream tasks (`044-improve-maintenance-spec-may-07-2026/`, `048-task-tooling-impl-spec/subtasks/02-*`, `064-improve-maintenance-spec-may-08-2026/`) — multiple `[Task NNN](path)` markdown link forms. Updated all path tokens via `Edit --replace_all` after a per-file `Read` to satisfy the tool's read-before-write contract; display text "Task 031" / "Task 032" preserved as historical reference.
- Two renamed folders' own self-references (`task_affects_paths`, `readme.md` slug/title). Updated.
- The `tasks/readme.md` index: bullets removed for the renumbered slugs and re-added at the bottom with `(renumbered from NNN per Task 043)` annotation; the duplicate-collision `(Note: shares task_id ...)` annotations on the surviving `031-adr-tooling-impl/` and `032-agents-spec-integration/` bullets were dropped.

## T1/T2 sweep disposition

Backtick prose mentions of `031-sync-tasks-index-status-drift` / `032-improve-maintenance-spec-may-2026` in `maintenance/run-log.md` (historical append-only record), `maintenance/pr-7{4,8}-review.md` (PR review records), `tasks/013-renumber-duplicate-task-ids/task.md` (superseded historical plan), and the four T4-immutable closed research SPECs (`friction-pattern-synthesis/output/SPEC.md`, `friction-pattern-synthesis/reflection/friction-log.md`, plus the four-collision-folders citation in `research/spec-staleness-decision-formalization/output/SPEC.md`) were left intact: they describe state at write-time and are not broken navigation links. Per MAINTENANCE.md §1.0.1, closed-research T1/T2 allowance is narrow to broken relative *Markdown* links — backtick prose mentions remain T4.

The `tasks/032-agents-spec-integration/` done-task prose mentions of `031-sync-tasks-index-status-drift` (in `task.md`, `readme.md`, `friction-log.md`) were left as historical backtick references: the task is `done`, the mentions describe scope-discipline decisions at close, and they are not markdown links. The destination folder (now `067-sync-tasks-index-status-drift`) is unambiguously findable via the now-unique `task_id: "067"` plus the slug.

## Pattern note (for F15 in Task 044)

This is the third Task in the lineage 013 → 024 → 043. Each renumber surfaces the same structural finding: parallel branches each pick the locally-next-free `<NNN>` against their own branch state, the merges land, and the collision becomes the next agent's problem. The cost of each renumber is approximately one session of focused mechanical work plus an ever-growing sweep surface (Task 013: 2 task folders; Task 024: 2 folders + 2 internal references; Task 043: 2 folders + ~12 cross-file markdown links including two root specs and a code comment). Task 044 F15 calls for a CI-time mechanical gate; this Task closure is empirical evidence supporting that finding's priority.
