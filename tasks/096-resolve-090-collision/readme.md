---
type: index
status: active
slug: resolve-090-collision-folder
summary: "Folder for Task 096 — renumber one of the two colliding task_id='090' folders per MAINTENANCE.md §3.5."
created: 2026-05-17
updated: 2026-05-17
---

# Task 096 — Resolve `task_id: "090"` Collision

## What and Why

This folder holds the orchestration record for resolving a duplicate `task_id` collision discovered during the 2026-05-17 Repo Coherence Check. Two folders carry `task_id: "090"`: `tasks/090-codex-pr-review/` (`in_progress`) and `tasks/090-review-pr109-archive-spec/` (`done`). Per [MAINTENANCE.md §3.5](../../MAINTENANCE.md), the later-created folder MUST be renumbered to the next free `<NNN>` slot, and every cross-reference rewritten in a single atomic commit.

The Task was auto-filed by the coherence agent because all four §3.5 auto-fire predicates held (single collision, no covering open Task, ≥1 open colliding member, `routine_type: coherence-check`).

## Linked Navigation

- [`task.md`](./task.md) — orchestration record (Goal, Plan, Todo, Links).

## Assumptions Log

(none)
