---
type: note
status: active
slug: 014-friction-log
summary: "Friction log for Task 014 closing as 'updated' — predecessor of Task 025."
created: 2026-05-05
updated: 2026-05-05
---

# Friction Log — Task 014

## FL Declaration

**FL0** — plan obsolesced cleanly. Three of the seven captured findings have been resolved by sibling Tasks since 014 was filed, so the original "treat F1–F7 as a single batch" plan no longer reflects the work that remains. Closing as `updated` to publish a smaller, current-state-aware successor.

## Supersession Rationale

Findings absorbed since 014 was filed:

- **F1 (duplicate `task_id` not mechanically detected)** — covered by the duplicate-id pre-creation check in the coherence prompt and by `tools/fm/validate.py` (Tasks 008 + 016).
- **F5 (`task_spawns_prompts` missing from template)** — `templates/task.md` now carries every required L2 key (verified 2026-05-05).
- **F6 (run-log baseline survives squash)** — verified by Task 008's hardening of `MAINTENANCE.md §2.3`.

The remaining open findings (F2 — duplicate-key renumber tier, F3 — linter-first triage, F4 — spec-bearing vs review-bearing research, F7 — post-repair linter verification) are carried forward without modification by the successor. F2 in particular benefits from the existence of `tools/fm/edit.py` (Task 016), which was unavailable when Task 014 was authored.

The continuation lives at [`/tasks/025-maintenance-spec-remaining-findings/`](../025-maintenance-spec-remaining-findings/) with `task_blocked_by: ['019']` because the F2 / F7 phrasing depends on the post-019 linter surface.

## Pointers

- Successor: [`../025-maintenance-spec-remaining-findings/task.md`](../025-maintenance-spec-remaining-findings/task.md)
- Already-addressed siblings: [`../008-harden-coherence-baseline-protocol/task.md`](../008-harden-coherence-baseline-protocol/task.md), [`../016-flexible-frontmatter-toolchain/task.md`](../016-flexible-frontmatter-toolchain/task.md)
- Lineage governance: [`TASK.md §4.7`](../../TASK.md), [`MAINTENANCE.md §3.4`](../../MAINTENANCE.md).
