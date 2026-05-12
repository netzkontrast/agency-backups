---
type: index
status: active
slug: improve-maintenance-spec-may-12-2026
summary: "Directory index for Task 078 — five gaps surfaced by the 2026-05-12 coherence run distilled into MAINTENANCE.md / coherence-prompt / staleness-audit / dynamic-readme-partition diffs."
created: 2026-05-12
updated: 2026-05-12
---

# Task 078 — Improve Maintenance Spec from 2026-05-12 Coherence Run

**What:** Captures five session-distilled gaps in `MAINTENANCE.md` surfaced by executing the spec on a stale baseline (89c0aa3) against `claude/peaceful-carson-TUvMW`:
1. The literal `end_commit: pending` failure mode in `maintenance/run-log.md` (two prior records never backfilled).
2. No spec guidance for large-delta coherence runs (~200 files since baseline).
3. 181 M.B.6 WARN diagnostics for missing `<!-- BEGIN DYNAMIC -->` / `<!-- END DYNAMIC -->` markers — corpus-wide non-compliance with a rule that the spec has never operationalised.
4. Staleness audit emits a single WARN severity regardless of age (Tasks 008 + 066 flagged at 8 days look identical to a hypothetical 60-day-old Task).
5. No single-command verifier for the composed coherence-run pipeline — agents must hand-compose `fm/validate` + `staleness-audit` + `dynamic-readme-partition` + `check-duplicate-task-id` + `trust-audit`.

**Why here:** Per [TASK.md §2](../../TASK.md), every coordination Task lives in `/tasks/<NNN>-<slug>/`. This continues the Task lineage 032 → 044 → 064 → 068 → **078** — the recurring "session-distilled maintenance-spec improvement" cadence captured by Task 064 F21.

## Navigation

- [task.md](./task.md) — The Task spec: Goal, Plan, Todo, Links.
- [friction-log.md](./friction-log.md) — Session friction record + canonical FL declaration line.

## Linked Specs and Tooling

- [MAINTENANCE.md](../../MAINTENANCE.md) — Repository Maintenance Protocol (target of all five proposed amendments).
- [prompts/repo-coherence-check/prompt.md](../../prompts/repo-coherence-check/prompt.md) — Coherence-check executable prompt (targets large-delta routing).
- [maintenance/run-log.md](../../maintenance/run-log.md) — Source of truth for the `end_commit: pending` failure-mode evidence.
- [tools/maintenance/staleness-audit.py](../../tools/maintenance/staleness-audit.py) — Target of urgency-tier amendment.
- [tools/maintenance/dynamic-readme-partition.py](../../tools/maintenance/dynamic-readme-partition.py) — Target of corpus-migration tool authorship.

## Sibling / Predecessor Tasks (informational; not blockers)

- [Task 032 — improve-maintenance-spec-may-2026](../032-improve-maintenance-spec-may-2026/) — Initial improvement pass.
- [Task 044 — improve-maintenance-spec-may-07-2026](../044-improve-maintenance-spec-may-07-2026/) — F14–F19.
- [Task 064 — improve-maintenance-spec-may-08-2026](../064-improve-maintenance-spec-may-08-2026/) — F20–F26 (introduced the lineage-cadence finding F21).
- [Task 068 — improve-maintenance-spec-may-2026](../068-improve-maintenance-spec-may-2026/) — Subsequent pass.

## Assumptions Log

- The five gaps in this Task are distinct from F2–F26 in the predecessor Tasks. Verified by grepping the predecessor `task.md` files for `end_commit: pending`, `delta-size threshold`, `BEGIN DYNAMIC`, and `urgency tiers` — none of the matches show those phrases proposed as concrete amendments.
- The 2026-05-12 coherence run hit a stale baseline (89c0aa3) — the actual delta since that hash is ~200 files spanning many already-merged PRs. The accumulated-delta pattern is itself part of finding #2 (large-delta guidance).
- This Task does NOT propose to autonomously close the two stale Tasks (008, 066) flagged by the staleness audit. Per MAINTENANCE.md §3.4 the agent MAY perform 1→1 lifecycle transitions directly, but at 8 days (just over the 7-day boundary) the signals are borderline; the human reviewer SHOULD confirm before closing.
- The closing-protocol skill sequence on this session was `/sc:analyze → /sc:reflect → /sc:improve → /sc:review → /sc:createPR` per operator instruction; the same RECOMMENDED-not-REQUIRED stance proposed by Task 064 F20 still holds.

<!-- BEGIN DYNAMIC -->

## Current State

- task_status: open. Awaiting assignment.
- No artefacts shipped yet — this Task is the session-distillation deliverable from the 2026-05-12 coherence run.

## Latest Synthesised Learnings

- The literal `end_commit: pending` token survived in `maintenance/run-log.md` across two `task-implementation` records from 2026-05-11 (Tasks 024+043 and Task 049 closures). The fall-forward `awk` in `prompts/repo-coherence-check/prompt.md` Step 1a recovered the baseline anyway because it walks past malformed records, but the spec has no enforcement mechanism for backfill.
- The 181 M.B.6 diagnostics overwhelmingly concentrate in `prompts/tooling-*/readme.md` files authored as part of the Task-039 tooling backlog. A pattern-based migration (template-driven insertion of an empty DYNAMIC block) would clear the corpus in a single commit.

## Open Blockers

- None. Implementation is unblocked.

<!-- END DYNAMIC -->
