---
type: index
status: active
slug: task-096-maintenance-spec-friction-log-declaration-hardening
summary: "Index for Task 096 (MAINTENANCE.md hardening) — folder contents and rationale for the four-item improvement bundle filed during the 2026-05-14 coherence run."
created: 2026-05-14
updated: 2026-05-14
---

# Task 096 — MAINTENANCE.md hardening

## What and Why

This folder owns Task 096, filed by the 2026-05-14 Repo Coherence Check after
three ERROR-tier governance diagnostics surfaced that all reduced to the same
class of repair: malformed or missing friction-log declaration lines on Tasks
already at `task_status: done`. The task captures four MAINTENANCE.md
improvement opportunities that reduce the same class of friction at the source
rather than re-firing once per quarter.

Filed as P3 (low priority); no work in flight blocks on the hardening landing
because the coherence run successfully completed via in-place T1 repairs.

## Linked Navigation

- [`task.md`](./task.md) — Task spec (Goal, Plan, Todo, Links).
- [`readme.md`](./readme.md) — this file.

## Assumptions Log

- The friction-log files under `tasks/030-…/` and `tasks/033-…/` (which the
  parent coherence run repaired) are *not* in scope for Task 096 itself; the
  in-place fix already landed in the coherence-run commit and the Task targets
  only the MAINTENANCE.md spec amendments + tooling extensions. The successor
  Task does NOT re-touch those files.
- The four §Plan items are independent; each can land in a separate commit and
  satisfy the Goal incrementally. Closing the Task requires all four to land
  (the Goal is conjunctive). Per-phase milestones are NOT introduced (Task 030
  FE-EX-2 pattern) because the items are small enough to land in one PR.
- `tools/fm/edit.py --bump-updated` batch semantics are a backwards-compatible
  extension: today's single-path callers continue to work unchanged after the
  change.
