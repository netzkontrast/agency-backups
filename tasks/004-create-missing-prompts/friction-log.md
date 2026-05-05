---
type: note
status: active
slug: 004-friction-log
summary: "Friction log for Task 004 closing as 'updated' — predecessor of Task 020."
created: 2026-05-05
updated: 2026-05-05
---

# Friction Log — Task 004

## FL Declaration

**FL0** — plan obsolesced cleanly. The two prompts the Task asked for (`refactor-governance-from-specs/prompt.md`, `token-efficiency-tool-suite/prompt.md`) now exist on disk; the original Goal is satisfied by drift via subsequent commits. The Task is closed as `updated` (not `done`) because the *next* concern — schema-conformant prompts under the post-Task-016 fm-validate contract — was never in scope of the original Plan.

## Supersession Rationale

Task 004's Plan ("draft prompts according to PROMPT.md guidelines") predates the canonical machine-readable contract in `maintenance/schemas/header-ontology.json` (shipped by Task 016). Today's `tools/fm/validate.py` flags `prompts/refactor-governance-from-specs/prompt.md` for missing required headings (`## I — Input`, `## S — Steps`, `## E — Expectations`, `## Constraints`) per the prompt-type heading set. The original Task gave no instruction to enforce that schema; therefore its closure does not retire the underlying drift.

The continuation lives at [`/tasks/020-audit-prompt-fm-validate-conformance/`](../020-audit-prompt-fm-validate-conformance/). Task 020 re-frames the work against the current toolchain — every prompt MUST pass `tools/fm/validate.py` cleanly, applied via `tools/fm/edit.py` for T1/T2 fixes.

## Pointers

- Successor: [`../020-audit-prompt-fm-validate-conformance/task.md`](../020-audit-prompt-fm-validate-conformance/task.md)
- Lineage governance: [`TASK.md §4.7`](../../TASK.md), [`MAINTENANCE.md §3.4`](../../MAINTENANCE.md).
