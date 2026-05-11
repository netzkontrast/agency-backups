---
type: index
status: active
slug: novel-architect-v110-epic
summary: "Directory index for Task 070 — epic umbrella for novel-architect@1.1.0 release. Orchestrates 7 sub-tasks (071-077) covering Sub-Module Refactor + Dramatica-Native Integration + selective Dual-Kernel Patterns."
created: 2026-05-11
updated: 2026-05-11
---

# Task 070 — novel-architect@1.1.0 Epic

**What:** Epic umbrella for the v1.1.0 release of the `novel-architect` skill. Coordinates 7 linked sub-tasks (071-077) that implement Sub-Module Refactor, deeper Dramatica integration, and selective Dual-Kernel patterns. Contains no code diffs itself — diffs land via sub-tasks.

**Why here:** Per [TASK.md §2](../../TASK.md), every coordination unit lives in `/tasks/<NNN>-<slug>/`. The v1.1.0 work touches multiple phases, methods, and external schemas; splitting into 7 sub-tasks with explicit `task_blocked_by` chains keeps each unit independently reviewable while preserving the dependency DAG (066 foundation → 067-072 parallel).

## Navigation

- [task.md](./task.md) — Epic spec: Goal, Context, Sub-Tasks table, Plan, Todo, Links.

## Assumptions Log

- (none)
