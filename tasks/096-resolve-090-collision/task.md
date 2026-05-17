---
type: task
status: active
slug: resolve-090-collision
summary: "Renumber one of the two colliding task_id='090' folders (`090-codex-pr-review` in_progress, `090-review-pr109-archive-spec` done) per MAINTENANCE.md §3.5. The later-created folder takes the next free `<NNN>` slot; `tasks/readme.md` and any reciprocal `task_blocked_by`/`task_supersedes` references are rewritten atomically."
created: 2026-05-17
updated: 2026-05-17
task_id: "096"
task_status: open
task_owner: "unassigned"
task_priority: P2
task_uses_prompts: []
task_spawns_research: []
task_spawns_prompts: []
task_affects_paths:
  - tasks/090-codex-pr-review/
  - tasks/090-review-pr109-archive-spec/
  - tasks/readme.md
  - MAINTENANCE.md
---

# Task 096 — Resolve `task_id: "090"` Collision

## Goal

`tools/fm/check-duplicate-task-id.py` exits `0` against `HEAD` after this Task closes; the two colliding folders are renumbered so each `task_id` is unique; `tasks/readme.md` bullets match the new folder paths; and every reciprocal cross-reference (`task_blocked_by`, `task_supersedes`, `task_superseded_by`) in sibling Tasks is rewritten atomically. The Task is `done` when `python3 tools/fm/check-duplicate-task-id.py tasks/` exits `0` and `tools/check-governance.sh` exits `0`.

## Context — Surfaced by 2026-05-17 Coherence Run

`tools/fm/check-duplicate-task-id.py` (currently advisory under `FM_DUPLICATE_TASK_ID_STRICT=0`) emits:

```
check-duplicate-task-id: ERROR: task_id='090' appears in 2 active tasks without supersession reciprocity:
  /home/user/agency/tasks/090-codex-pr-review/task.md
  /home/user/agency/tasks/090-review-pr109-archive-spec/task.md
```

Both folders were created on `2026-05-12` on independent branches and merged without renumber-on-commit per [TASK.md §8.1](../../TASK.md). `090-codex-pr-review` is `task_status: in_progress`, `090-review-pr109-archive-spec` is `task_status: done`.

This satisfies all four §3.5 auto-fire predicates for a coherence-run agent to file this Task (single collision, no covering open Task, ≥1 colliding folder is open, `routine_type: coherence-check`).

## Plan

1. Pick the renumber target. Per §3.5, "the later-created colliding folder" is renumbered; both Tasks were created same-day, so pick by git commit time: the one merged second is renumbered. Run `git log --diff-filter=A --pretty=format:"%h %ci %s" -- tasks/090-codex-pr-review/task.md tasks/090-review-pr109-archive-spec/task.md` to determine order.
2. Pick the next free `<NNN>` slot — at this Task's filing time, `096` is taken by this Task and `097` by Task 097 (filed in the same coherence run). The renumber target lands at `098` (or the lowest unallocated slot at execution time).
3. Rename the folder (`git mv tasks/090-<later>/ tasks/098-<later>/`).
4. Mutate `task_id: "090"` → `task_id: "098"` in the renamed `task.md` via `python3 tools/fm/edit.py --set task_id='"098"' tasks/098-<later>/task.md`.
5. Grep the corpus for cross-references to the renamed `<NNN>` and rewrite each: `grep -rn '"090"' tasks/*/task.md` AND `grep -rn 'tasks/090-<later>' tasks/ research/ prompts/ decisions/ -l`.
6. Update `tasks/readme.md` bullet path + number per [TASK.md §4.8](../../TASK.md).
7. Bump `updated:` on every touched file via `tools/fm/edit.py --bump-updated`.
8. Verify `tools/check-governance.sh` exits `0` and `tools/fm/check-duplicate-task-id.py tasks/` exits `0` against the post-renumber state.
9. Commit atomically with message `Task 096: renumber 090-<later> → 098-<later> (MAINTENANCE.md §3.5 dup-id resolution)`.

## Todo

- [ ] 1. Determine which 090 folder was merged later (git log inspection).
- [ ] 2. Allocate the next free `<NNN>` (likely `098` at execution time).
- [ ] 3. `git mv` the renumber-target folder.
- [ ] 4. Mutate `task_id` via `tools/fm/edit.py --set`.
- [ ] 5. Rewrite every cross-reference (grep + edit).
- [ ] 6. Update `tasks/readme.md` bullet.
- [ ] 7. Bump `updated:` on every touched file.
- [ ] 8. Verify governance check passes.
- [ ] 9. Commit atomically with §3.5 citation.

## Links

- Governing specs: [`MAINTENANCE.md §3.5`](../../MAINTENANCE.md), [`TASK.md §8.1`](../../TASK.md).
- Linter: [`tools/fm/check-duplicate-task-id.py`](../../tools/fm/check-duplicate-task-id.py).
- Renumber procedure (prior art): [Task 043](../043-renumber-duplicate-task-ids-v3/task.md), [Task 067](../067-sync-tasks-index-status-drift/task.md).
- Filed by: 2026-05-17 Repo Coherence Check (this session); see [`maintenance/run-log.md`](../../maintenance/run-log.md) for the run record.
