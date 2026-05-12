---
type: note
status: active
slug: friction-log-task-078
summary: "Friction log for Task 078 filing — operator-instructed session distillation from the 2026-05-12 coherence run. FL1 (canonical no-separator form per Task 044 F14)."
created: 2026-05-12
updated: 2026-05-12
---

# Friction Log — Task 078 Filing

Highest Frustration Level: FL1

## Context

Task 078 was filed in response to the operator's standing instruction at session close: *"After you Are Done, collect all Information about the current Session, that could Help to further Improve the Maintenance spec and submit a new Task."* The 2026-05-12 coherence run itself was largely clean — 0 ERROR-tier `fm/validate` diagnostics across the ~200-file delta from baseline `89c0aa3` — but two advisory linters surfaced concrete gaps:

- `tools/maintenance/staleness-audit.py`: 2 stale Tasks (008 `completed_by_drift` at 8d, 066 `no_longer_desirable` at 8d).
- `tools/maintenance/dynamic-readme-partition.py`: 181 M.B.6 WARN diagnostics for missing `<!-- BEGIN DYNAMIC -->` / `<!-- END DYNAMIC -->` markers, concentrated in `prompts/tooling-*/readme.md`.

Plus the run-log itself carries the literal token `end_commit: pending` on lines 915 and 947 — two `task-implementation` records from 2026-05-11 (Tasks 024+043 and Task 049 closures) never backfilled.

Per the operator's closing instruction, the session also invokes `/sc:analyze`, `/sc:reflect`, `/sc:improve`, `/sc:review`, and `/sc:createPR` in sequence.

## Per-Finding Disposition (at file time)

All five Plan items are `proposed: pending Plan execution`. None has a landed diff yet; this Task's Plan-1 through Plan-5 are the diff-landing steps. The friction-log will be updated at Task close with `landed: <commit>` or `won't-fix: <reason>` per finding.

- Plan-1 (end_commit backfill mechanism): proposed; /sc:reflect surfaced the chicken-and-egg loop in the original Goal; /sc:improve amended Plan-1 to specify run-start (or pre-commit on `maintenance/run-log.md`) invocation so the previous record's `pending` is repaired inside the current run's atomic commit. The Goal predicate now reads "HEAD is the only sanctioned bearer of `pending`".
- Plan-2 (large-delta routing): proposed; the 2026-05-12 run hit ~200 files since baseline 89c0aa3 with no spec guidance.
- Plan-3 (M.B.6 corpus migration): proposed; 181 WARN diagnostics is a concrete migration scope.
- Plan-4 (staleness urgency tiers): proposed; the 2026-05-12 run found Tasks 008 + 066 at 8d (just over the 7d window) flagged identically to a hypothetical 60d-old Task.
- Plan-5 (single-command verifier): proposed; the 2026-05-12 run composed 5 tools manually.

## Friction Encountered During This Session

1. **`end_commit: pending` chicken-and-egg (FL1).** The run-log's prior two records carry `pending` end_commits that were never backfilled, but the current spec sanctions writing `pending` per Step 6 of the coherence-check prompt when the closing-commit hash isn't pre-computable. The contradiction between "MAY write pending" and "no record SHOULD remain pending" is unresolved in the spec. Recorded as Plan-1; the /sc:reflect pass amended Plan-1 to close the loop via run-start invocation of the backfill tool.

2. **Stale baseline → unmanageable delta (FL1).** Baseline `89c0aa3` predates ~25 commits and ~200 files of merged work. The coherence-check prompt is designed for small deltas (the §3 triage assumes per-file inspection); at 200 files the routine effectively collapses to "trust the linter outputs and skip the manual triage". Recorded as Plan-2 (delta-size threshold + routing decision).

3. **Skill orchestration ceremony (FL0).** The closing-protocol skills (`/sc:analyze` → `/sc:reflect` → `/sc:improve` → `/sc:review` → `/sc:createPR`) each return a self-describing instruction block rather than autonomous work. The agent provides the substance; the skill provides the scaffold. This is by design (per the SuperClaude framework definition), but a first-time agent may expect each skill to perform the work autonomously and waste tool budget waiting. Documented for future-agent context; not a maintenance-spec issue.

4. **TodoWrite enum case (FL1).** First `TodoWrite` call used title-cased status values (`"In Progress"`); the tool's enum requires lowercase `pending|in_progress|completed`. One-edit retry. Same friction logged by Task 064 F25; the disposition is likely `won't-fix` because it's a Claude Code harness constraint, not a repo governance issue. NOT recorded as a new Plan item for Task 078 — duplicates Task 064 F25.

5. **Stale-task lifecycle borderline (FL0).** Tasks 008 (`completed_by_drift`) and 066 (`no_longer_desirable`) fired at exactly age 8d (one day past the 7d gate). MAINTENANCE.md §3.4 sanctions 1→1 mechanical lifecycle transitions during a coherence run, but at the borderline of the staleness window the audit-emitted signals are weak. Chose NOT to autonomously close either Task; flagged in run-log notes for human reviewer. Recorded as Plan-4 (urgency tiers will distinguish freshly-stale from long-stale, lowering the false-positive risk on borderline cases).

## Next Actions (delegated)

The Task's Plan items 1–5 + administrative items 6–7 are the diff-landing surface. This filing closes when:
- The closing commit lands and pushes.
- The `maintenance/run-log.md` carries a fresh `coherence-check` record with the real end_commit (NOT `pending`).
- The draft PR is open and cites Task 078 + FL1.

## Friction Level Rationale

**FL1** — one identified protocol contradiction (Plan-1 chicken-and-egg), three secondary frictions, no blockers. The session completed all requested skill invocations and produced a conformant Task spec. Frustration was non-zero (the run-log `pending` failure mode required real reasoning to disentangle) but well below FL2 (which would imply spec failure or unrecoverable contradiction).
