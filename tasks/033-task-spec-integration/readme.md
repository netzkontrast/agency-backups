---
type: index
status: active
slug: task-033-folder
summary: "Folder index for Task 033 — TASK.md spec integration. Closes T.8.1 duplicate-task_id enforcement gap, formalizes §4.7 updated/abandoned boundary, back-ports skill_* L2 from skills-namespace-ontology, and cross-links §3.3 to flexible-frontmatter-toolchain SPEC."
created: 2026-05-06
updated: 2026-05-06
---

# Task 033 Folder

## What

Operational folder for Task 033, which addresses TASK.md's load-bearing-but-underspecified clauses, ships two enforcement linters, and adds a supersession-blocker-inheritance Gherkin scenario.

## Files

- [`task.md`](./task.md)
- [`subtasks/`](./subtasks/) — 2 research, 2 tooling, 1 spec amendment.

## Assumptions Log

- The duplicate-task_id linter (subtask 03) is expected to *immediately* surface the existing 006/006 and 009/009 collisions; that is intentional — it makes Task 024 visible as the unblocking work.
- `MAINT_STALE_DAYS` default of 7 days (referenced in MAINTENANCE.md §3.4) carries forward; subtask 02 is free to recommend a different default with rationale.
