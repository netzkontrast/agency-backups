---
type: note
status: active
slug: 005-friction-log
summary: "Friction log for Task 005 closing as 'updated' — predecessor of Task 021."
created: 2026-05-05
updated: 2026-05-05
---

# Friction Log — Task 005

## FL Declaration

**FL1** — plan-level drift. The deferred 148 stubs are still pending, but the *mechanism* the original Plan implied ("Systematically batch-update these missing stubs") predates the canonical mutator (`tools/fm/edit.py`) and the migration plan (Task 017). Closing this Task as `updated` rather than `done` because the work has not been executed; closing as `updated` rather than carrying forward in-place because the Plan no longer reflects the current toolchain.

## Supersession Rationale

`MAINTENANCE.md §1` now mandates `tools/fm/edit.py` as the canonical T1/T2 frontmatter mutator (it preserves body bytes, takes a file lock, and rejects T3/T4 by construction). Task 005's Plan does not name this tool — it predates the toolchain shipped by Task 016. Additionally, Task 017 has scoped a repo-wide migration that will resolve a substantial fraction of the 148 stubs; the residual is what Task 021 inherits.

The continuation lives at [`/tasks/021-apply-fm-edit-to-deferred-coherence/`](../021-apply-fm-edit-to-deferred-coherence/) with `task_blocked_by: ['017']` so it cannot start until the migration completes.

## Pointers

- Successor: [`../021-apply-fm-edit-to-deferred-coherence/task.md`](../021-apply-fm-edit-to-deferred-coherence/task.md)
- Blocker on the successor: [`../017-migrate-repo-to-flexible-toolchain/task.md`](../017-migrate-repo-to-flexible-toolchain/task.md)
- Lineage governance: [`TASK.md §4.7`](../../TASK.md), [`MAINTENANCE.md §3.4`](../../MAINTENANCE.md).
