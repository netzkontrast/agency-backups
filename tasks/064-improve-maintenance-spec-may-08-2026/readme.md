---
type: index
status: active
slug: improve-maintenance-spec-may-08-2026
summary: "Directory index for Task 064 — distillation of seven findings (F20–F26) from the 2026-05-08 coherence run into MAINTENANCE.md / coherence-prompt / governance-script / run-log diffs."
created: 2026-05-08
updated: 2026-05-08
---

# Task 064 — Improve Maintenance Spec from 2026-05-08 Coherence Run

**What:** Captures seven session-distilled findings (F20–F26) from the 2026-05-08 Repo Coherence Check and proposes concrete diffs against [`MAINTENANCE.md`](../../MAINTENANCE.md), [`prompts/repo-coherence-check/prompt.md`](../../prompts/repo-coherence-check/prompt.md), [`tools/check-governance.sh`](../../tools/check-governance.sh), [`maintenance/run-log.md`](../../maintenance/run-log.md), and [`CLAUDE.md`](../../CLAUDE.md).

**Why here:** Per [TASK.md §2](../../TASK.md), every coordination Task lives in `/tasks/<NNN>-<slug>/`. The Task lineage 014 → 032 → 044 → **064** is the recurring "session-distilled maintenance-spec improvement" pattern surfaced by the operator's standing instruction (per [Task 044 F18](../044-improve-maintenance-spec-may-07-2026/task.md) territory).

## Navigation

- [task.md](./task.md) — The Task spec: Goal, Findings (F20–F26), Plan, Todo, Links.
- [friction-log.md](./friction-log.md) — Per-session friction record + canonical FL declaration line + per-finding disposition.

## Linked Specs and Tooling

- [MAINTENANCE.md](../../MAINTENANCE.md) — Repository Maintenance Protocol (target of F20, F21, F23, F24, F26 diffs).
- [prompts/repo-coherence-check/prompt.md](../../prompts/repo-coherence-check/prompt.md) — Coherence-check executable prompt (target of F20, F22, F24, F26 diffs).
- [tools/check-governance.sh](../../tools/check-governance.sh) — Unified governance gate (target of F23 diff).
- [maintenance/run-log.md](../../maintenance/run-log.md) — Run record source-of-truth (target of F26 schema doc; F20 / F22 / F24 reference its 2026-05-08 entry as the originating evidence).
- [CLAUDE.md](../../CLAUDE.md) — AI-assistant entry point (target of F25's optional one-line note; cross-referenced from F20).

## Sibling Tasks (open, parallel; not blockers)

- [Task 025 — maintenance-spec-remaining-findings](../025-maintenance-spec-remaining-findings/) — F2/F3/F4/F7 (open since 2026-05-05).
- [Task 044 — improve-maintenance-spec-may-07-2026](../044-improve-maintenance-spec-may-07-2026/) — F14–F19 (open since 2026-05-07; F18/F19 absorbed from PR #74).

This is the third concurrent open Task in the lineage. Finding F21 of THIS Task records the accumulation pattern itself; resolving F21 is expected to retire the pattern of spawning a new Task per session.

## Assumptions Log

- The new findings F20–F26 are distinct from F2/F3/F4/F7 (Task 025) and F14–F19 (Task 044). Verified by reading both Tasks' `## Findings` sections at file time. F25 (`TodoWrite` case sensitivity) is the only finding likely to be `won't-fix` because it concerns the Claude Code harness, not the repo's governance surface.
- The coherence run for 2026-05-08 emitted 0 gating diagnostics across the 193-file delta; T1/T2 repairs were therefore zero. The Task is filed as the operator-instructed session distillation per the standing instruction (see [Task 044 F18](../044-improve-maintenance-spec-may-07-2026/task.md) territory) — NOT as the run's own T3 output. The run-log entry notes this distinction.
- Finding F21 (cadence rule) is meta — landing it would alter the protocol that produced this very Task. The drafting Plan-3 acknowledges that Task 064 itself remains open during the rule's transition, with the rule taking effect only after Task 064 closes (then 064 is the singular open Task).
- The closing-protocol sequence in F20 (`/sc:analyze → /sc:reflect → /sc:improve → /sc:Review → /sc:createPR`) is the operator's observed pattern at 2026-05-08; future operators may prefer different sequences. The proposed diff marks the four upstream skills RECOMMENDED (not REQUIRED) and only the terminator REQUIRED, leaving operator flexibility intact.
