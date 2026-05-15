---
type: friction-log
status: active
slug: task-096-friction-log
summary: "Friction log for Task 096 — manual maintenance run on 2026-05-15. FL1: the maintenance routines surfaced five spec ambiguities that required interpretation rather than mechanical execution; the run completed cleanly but the spec gaps slowed decision-making."
created: 2026-05-15
updated: 2026-05-15
---

# Task 096 — Friction Log

Highest Frustration Level: FL1

## Run Summary

Manual user invocation: "Execute Maintenance.md use /sc: skills were helpful After you Are Done, collect all Information about the current Session, that could Help to further Improve the Maintenance spec and submit a new Task (following Task.md spec) /sc:analyze then /sc:reflect then /sc:improve then /sc:Review then /sc:createPR".

Branch: `claude/peaceful-carson-SOZFe`. Baseline: `6e4859d` (most recent reachable `end_commit:` from `maintenance/run-log.md`). Delta: 756 files since baseline (a wide window covering merged PRs #116–#128).

## Friction Events

### FE-1 (FL1) — `routine_type:` enum doesn't fit a manual sweep

The §2.3 enum has four values: `bootstrap`, `coherence-check`, `nightly-maintenance`, `task-implementation`. A manual user-invoked sweep that combines a §2 Coherence Check with the §3.6 ADR falsifier-trigger audit doesn't cleanly map to any of them. The pragmatic choice for this run's run-log record is `coherence-check` because the delta computation IS the §2 routine; the §3.6 audit is logged separately per its own one-line projection format. Amendment B in Task 096 binds the answer.

### FE-2 (FL1) — §3.5 dup-id autofile predicate (4) reads "MUST escalate to a human" for manual runs

The 090 collision satisfies predicates 1+2+3 but predicate 4 says `routine_type: coherence-check` (NOT nightly), which literal-reads to "MUST escalate" for a manual invocation that the human has explicitly requested. The intent of predicate 4 (don't autofile during the broader nightly because the human reviewer is the one closing the loop) is preserved when interpreted against the SPIRIT — the operator IS present and asked for the run — but the LETTER doesn't allow it. Amendment C closes the gap.

### FE-3 (FL0→FL1) — Multi-fire ambiguity in §3.6

ADR-0008 fires F1+F2+F3+F4 in one audit. The §3.6 normative text says "When the audit reports `FIRED:<CODE>`, the maintenance agent … MUST file a Task whose Plan covers the successor ADR" (singular). Whether to file 1 Task covering all four fires or 4 Tasks (one per fire) is left to the agent. Filing 4 invites duplicate-tracking churn AND creates four ADR-0008 successors that must then themselves merge. Filing 1 is the pragmatic choice, but the spec doesn't bind it. Amendment A closes the gap.

### FE-4 (FL1) — `[opt]` linter emits ERROR-tier; gate stays green

The output below confused the initial triage:

```
--- [opt] FL declaration linter (Task 038 ST-2 — FRUSTRATED.md FR.B.4) ---
tasks/033-task-spec-integration/friction-log.md::ERROR:FR.B.4:malformed:...
tasks/030-cleanup-dramatica-skills-corpus/friction-log.md::ERROR:FR.B.4:malformed:...
=== PASS: all governance checks passed. ===
```

A reasonable reader sees `ERROR` and concludes the gate failed. The gate did not fail; the linter is `[opt]` (advisory). The orthogonality between linter level (severity of the finding) and slot (gating vs advisory) is not surfaced in §1 or §4.1. Amendment D adds a footnote.

### FE-5 (FL0→FL1) — Staleness audit produced 4 flags, no batch guidance

§3.4 authorises "ordinary 1→1 supersessions" inline. With 4 simultaneous flags spanning 3 buckets (1× COMPLETED_BY_DRIFT, 1× DRIFTED, 2× NO_LONGER_DESIRABLE), the agent has no spec text on whether to handle the batch inline or escalate. The conservative path — file ONE meta-Task surfacing all four — was chosen but isn't authorised by the literal §3.4 text. Amendment E specifies the per-bucket cap.

### FE-6 (FL0) — `tools/fm/query.py` underuse during linter-first triage

The Repo Coherence Check prompt at `prompts/repo-coherence-check/prompt.md` Step 2.5 explicitly suggests `tools/fm/query.py "missing-key=..." --format=paths` as a triage primitive. This run jumped directly from `tools/check-governance.sh` output to manual file inspection without using `query.py` to slice by missing-key. The triage worked because the gate had only one ERROR (`T.7.11`) which is precise, but for runs with broader ERROR fan-out the bypass would cost more time. Meta-lesson: **always run `query.py` against the highest-frequency `F.3.x` / `F.4.x` codes from the gate output before opening individual files**. Not a spec gap — a routine-execution lesson worth threading into the prompt's reflection-gate R2.5 narrative.

### FE-7 (FL0) — TodoWrite scaffolding skipped on a 5+-Amendment Plan

Task 096 ships with a 10-item Plan (after /sc:improve), 5 of which carry inter-dependencies (B blocks C, B blocks F). A future executor opening Task 096 without TodoWrite scaffolding from this session has only the prose dependency note. Meta-lesson: **for any Task whose Plan has ≥3 inter-dependent items, the filing session SHOULD seed an initial TodoWrite snapshot in the friction-log so the next executor can adopt-and-extend rather than re-derive ordering**. Not actioned this run because the user prompt didn't include implementation; flagged as a future Closing-Run-Procedure refinement.

## What Worked

- The bootstrap (`./install.sh` + `tools/check-governance.sh`) ran cleanly. Only one ERROR (the `T.7.11` index-drift on Task 093) needed a T1 fix; `index_diff.py` localised the diagnostic precisely and the `Edit` tool applied the one-line fix.
- The `tools/maintenance/adr-trigger-audit.py --format runlog` projection is a great primitive — one line per audit, exit code 2 when something fired, clean to grep.
- The §3.5 / §3.4 / §3.6 audits all ship with clean `--format runlog` or canonical-diagnostic output, which made the "what does the spec say to do?" lookup straightforward at decision time.

## Closure

This Task documents findings; the actual amendment work (Amendments A–E) is the Plan/Todo of Task 096 and will be executed in a follow-up session. The 2026-05-15 manual run itself completed:

- One T1 fix (tasks/readme.md drift on Task 093 — covered by `T.7.11` mechanical enforcement).
- One Task filed (this Task 096).
- Run-log record appended.
- Pre-commit gate green.

No T3/T4 changes were made directly during this run. Per the user's prompt, the `/sc:` chain follows in subsequent assistant messages.
