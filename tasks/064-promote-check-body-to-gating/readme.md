---
type: index
status: active
slug: task-064-promote-check-body-to-gating
summary: "Index for Task 064: promote --check-body to gating, codify body-shape repair tier."
created: 2026-05-10
updated: 2026-05-10
---

# Task 064 — Index

## What and Why

This folder coordinates Task 064: promote `tools/fm/validate.py --check-body` from advisory to gating inside `tools/check-governance.sh`, drop the stale `(Task 019)` forward reference in the coherence-check prompt, and codify body-shape repairs on closed Tasks as T3 in `MAINTENANCE.md §1`.

The Task was filed by the 2026-05-10 coherence run after discovering that two F.B.1 diagnostics on `tasks/039-maintenance-spec-integration/task.md` survived pre-commit because `--check-body` is not wired into the gate.

## Linked Navigation

- [task.md](./task.md) — Goal, Plan, Todo, Links.
- [../../prompts/repo-coherence-check/prompt.md](../../prompts/repo-coherence-check/prompt.md) — executing prompt.
- [../../MAINTENANCE.md](../../MAINTENANCE.md) — repair-tier spec being amended.
- [../../tools/check-governance.sh](../../tools/check-governance.sh) — gate to be amended.

## Assumptions Log

(none)

<!-- BEGIN DYNAMIC -->
## Current State

`task_status: open`. Filed 2026-05-10 by the coherence run. No subtasks yet.

## Latest Synthesised Learnings

- `tools/fm/validate.py --check-body` exists and emits stable diagnostics; the only remaining work is wiring it into the gate.
- The `(Task 019)` parenthetical in `prompts/repo-coherence-check/prompt.md §Step 2.5` is stale; Task 019 closed and the promotion never landed.
- Body-shape repairs on `task_status: done` files sit in a gap between the T1/T2 (frontmatter) and T3 (heading rewrite) tier classifications in `MAINTENANCE.md §1`.

## Open Blockers

(none)
<!-- END DYNAMIC -->
