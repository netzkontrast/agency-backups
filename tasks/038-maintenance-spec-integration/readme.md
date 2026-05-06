---
type: index
status: active
slug: task-038-folder
summary: "Folder index for Task 038 — MAINTENANCE.md spec integration. Operationalizes three orphaned research outputs (agentic-eval-trust-improvement-spec, repo-maintenance-protocol-spec, governance-specs-update-research §2) and closes five governance debts in §1.1.2, §2.3, §3.2, §3.4, §3.5."
created: 2026-05-06
updated: 2026-05-06
---

# Task 038 Folder

## What

Operational folder for Task 038. Largest payload in the 031–038 chain — six subtasks, three of which lift orphaned research into normative scope.

## Files

- [`task.md`](./task.md)
- [`subtasks/`](./subtasks/) — 2 research, 3 tooling, 1 spec amendment.

## Assumptions Log

- The §3.4 staleness algorithm formalization is shared with Task 032 — whichever task lands first authors the canonical SPEC and the second consumes it.
- The §3.5 duplicate-task_id circular dependency resolution is contingent on Task 032's subtask 03 (duplicate-task_id linter) — once that linter is gating, the coherence run no longer files Tasks for collisions; it surfaces them as ERRORs that pre-commit blocks.
