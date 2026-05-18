---
type: task
status: active
slug: improve-maintenance-spec-may-18-2026
summary: "Distil seven findings (F27–F33) from the 2026-05-18 coherence run into concrete diffs against MAINTENANCE.md, prompts/repo-coherence-check/prompt.md, and tools/adr/cli.py. Companion (not successor) to open Tasks 025 / 044 / 064 in the same lineage; cites Task 064 F21 (one-open-Task cadence rule) as recognised pre-condition that has not yet landed."
created: 2026-05-18
updated: 2026-05-18
task_id: "096"
task_status: open
task_owner: "unassigned"
task_priority: P2
task_uses_prompts:
  - improve-maintenance-spec-may-18-2026
task_spawns_research: []
task_spawns_prompts: []
task_blocked_by: []
task_supersedes: []
task_superseded_by: []
task_affects_paths:
  - MAINTENANCE.md
  - prompts/repo-coherence-check/prompt.md
  - tools/adr/cli.py
  - tasks/096-improve-maintenance-spec-may-18-2026/
  - prompts/improve-maintenance-spec-may-18-2026/
---

# Task 096 — Improve Maintenance Spec from 2026-05-18 Coherence Run

## Goal

Each of the seven findings F27–F33 below MUST land as either (a) a concrete diff against [`MAINTENANCE.md`](../../MAINTENANCE.md), [`prompts/repo-coherence-check/prompt.md`](../../prompts/repo-coherence-check/prompt.md), or [`tools/adr/cli.py`](../../tools/adr/cli.py); OR (b) a documented `won't-fix` disposition in this Task's `friction-log.md` with rationale. The Task closes when every finding has either a landed diff or a recorded disposition. Companion (NOT successor) to [Task 025](../025-maintenance-spec-remaining-findings/task.md), [Task 044](../044-improve-maintenance-spec-may-07-2026/task.md), and [Task 064](../064-improve-maintenance-spec-may-08-2026/task.md) — three sibling improve-maintenance Tasks are now open. Per Task 064 F21 (proposed one-open-Task cadence rule, not yet landed), this Task's filing IS itself evidence that the cadence rule needs adoption.

## Findings

### F27 — §1 tier table does not enumerate FL-declaration syntax repairs

**Symptom.** Today's coherence run hit two ERROR-tier FR.B.4 failures: `tasks/033-task-spec-integration/friction-log.md` used `**FL: 1**` (non-canonical syntax); `tasks/030-cleanup-dramatica-skills-corpus/friction-log.md` had FL tokens inside per-event headings only (no top-level declaration). Both repairs were mechanical: Task 033 was a value-preserving syntax normalisation; Task 030 added a top-level `**Highest Frustration Level: FL3**` line whose level is mechanically derivable from FE-EX-2's "FL3, Blocking" label. The repairs land cleanly as T1/T2 — but [`MAINTENANCE.md §1`](../../MAINTENANCE.md) enumerates only `updated:` / `slug:` / broken-link / readme-stub as T1 examples and "missing L1/L2 key with unambiguous value" as T2. A maintenance agent reading §1 strictly would refuse the fix and over-scope to T3.

Task 044 F14 ratifies the *canonical form* (FRUSTRATED.md + template + linter message); F27 is the orthogonal *tier classification* in MAINTENANCE.md §1. The shipped `tools/check-fl-declaration.py` (15 accepted variants) makes the decision space finite — agents need spec permission to act on it.

**Concrete diffs:**

- [`MAINTENANCE.md §1`](../../MAINTENANCE.md) T1 row SHOULD add: "Non-canonical FL declaration syntax (e.g. `**FL: 2**` → `**FL2**`) where the surface form fails one of the 15 accepted variants in [`tools/check-fl-declaration.py`](../../tools/check-fl-declaration.py) but the *value* is unambiguous."
- [`MAINTENANCE.md §1`](../../MAINTENANCE.md) T2 row SHOULD add: "Missing top-level FL declaration line in a closed Task's `friction-log.md` where the value is mechanically derivable from per-event FL tags (e.g. headings of the form `### FE-N (FL3, Blocking)` yield Highest = FL3)."
- Cross-link Task 044 F14 in §1's prose so the canonicalisation and tier-classification rules are discoverable together.

### F28 — §3.3 lacks dedup-against-open-Tasks predicate before AGGREGATOR-driven Task filing

**Symptom.** Today's trust-audit AGGREGATOR emitted 13 `WARN:MAINT.TRUST.FRICTION:FL[1|3]:...:recommend-task` lines (e.g. `research/adr-corpus-extraction-from-governance-specs::WARN:MAINT.TRUST.FRICTION:FL3:...`). [`MAINTENANCE.md §3.3`](../../MAINTENANCE.md) reads as "for each FL1+ issue, create a Task" — but the AGGREGATOR's output is workspace-stable. The same 13 recommendations would surface tomorrow. Running maintenance daily would multiply duplicate Tasks; running it weekly would file 13 every Monday.

[`MAINTENANCE.md §3.5`](../../MAINTENANCE.md) already encodes the analogous predicate for the dup-id linter: "agent MUST grep `tasks/*/task.md` for the colliding `<NNN>` strings before filing." §3.3 needs the same shape against `task_affects_paths`.

**Concrete diffs:**

- [`MAINTENANCE.md §3.3`](../../MAINTENANCE.md) bullet 2 SHOULD insert a "Dedup precondition" sentence: "Before filing the Task, the agent MUST grep open `tasks/*/task.md` files for any `task_affects_paths` entry that covers the friction source path. If a match is found, the agent MUST skip-with-citation (per §3, see F26 follow-up) rather than file a duplicate."
- Cross-reference Task 064 F26 so the skip-with-citation convention is the canonical resolution.
- (Optional) Ship a `tools/maintenance/aggregator-dedup-preview.py` helper that prints the would-file vs. would-skip set against current HEAD; spec change is the gate, tooling is a follow-up.

### F29 — §2.3 fall-forward ambiguous when last record is `adr-synthesize` or `task-implementation`

**Symptom.** Today's most-recent run-log record is `Run 2026-05-12 — adr-synthesize` (`end_commit: 6e4859d`). The last `coherence-check` is `Run 2026-05-08` (`end_commit: 89c0aa3`). The Step-1a awk fall-forward in [`prompts/repo-coherence-check/prompt.md`](../../prompts/repo-coherence-check/prompt.md) picks 6e4859d — but the *semantic* coherence baseline is 10 days of un-swept commits behind. The §2.3 note acknowledges this ambiguity but ratifies no rule.

**Concrete diffs:**

- [`MAINTENANCE.md §2.3`](../../MAINTENANCE.md) SHOULD promote the existing prose note to a normative rule: "When the most-recent run-log record's `routine_type` is `adr-synthesize` or `task-implementation`, the agent MUST recover the most-recent `coherence-check` baseline (skipping intervening non-sweep records). The `end_commit` of an `adr-synthesize` or `task-implementation` record MUST NOT be used as the coherence delta baseline."
- [`prompts/repo-coherence-check/prompt.md`](../../prompts/repo-coherence-check/prompt.md) Step 1a awk SHOULD be amended to filter on `routine_type: coherence-check` before extracting `end_commit:`. Document the fall-forward order: most-recent `coherence-check` → most-recent `nightly-maintenance` → fail loudly.

### F30 — §3.4 staleness audit lacks N-hits → triage-vs-individual escalation rule

**Symptom.** Today's staleness audit flagged 4 Tasks (008 `completed_by_drift`; 048 + 066 `no_longer_desirable`; 053 `drifted`). §3.4 says the agent "MAY perform the transition directly because every step is mechanical (frontmatter mutations + a one-paragraph friction log)" — but provides no threshold for when to fork into N individual lifecycle Tasks versus ONE triage Task. With 4 hits per sweep, filing 4 individual Tasks per run risks open-Task explosion; filing 1 triage Task loses determinism on the per-Task bucket assignment.

**Concrete diffs:**

- [`MAINTENANCE.md §3.4`](../../MAINTENANCE.md) closing paragraph SHOULD add: "When `tools/maintenance/staleness-audit.py` emits ≥3 non-`still_accurate` buckets in a single run, the maintenance agent MUST file ONE triage Task naming all affected paths in `task_affects_paths` rather than N individual lifecycle Tasks. The triage Task's body MUST preserve the per-Task bucket assignment as a table so the deterministic classifier output is not lost."
- The 3-hit threshold SHOULD be tunable via `MAINT_STALENESS_TRIAGE_THRESHOLD` (default `3`); document the env var.

### F31 — §1 T3 row does not cross-link to TASK.md §4.9 `/sc:*` planning ladder

**Symptom.** A T3 structural Task (like this very meta-Task) crosses the [TASK.md §4.9](../../TASK.md#49-planning-pipeline-for-t3-structural-tasks-sc-ladder) threshold (>3 files, root spec edit) and benefits from `/sc:analyze → /sc:brainstorm → /sc:design → /sc:workflow`. [`MAINTENANCE.md §1`](../../MAINTENANCE.md) T3 row says "Write a Task" but never points the agent at the ladder. The cross-link saves a fresh agent ~30 minutes of spec-reading per T3 finding.

**Concrete diffs:**

- [`MAINTENANCE.md §1`](../../MAINTENANCE.md) T3 row "Permitted action" cell SHOULD append: "(when filing the T3 Task, see [TASK.md §4.9](../../TASK.md#49-planning-pipeline-for-t3-structural-tasks-sc-ladder) for the `/sc:analyze → /sc:brainstorm → /sc:design → /sc:workflow` planning ladder)."

### F32 — §4.1 maintenance-bypass prose silent on advisory-tier linters

**Symptom.** Today's gate passed despite ~13 trust-audit AGGREGATOR ERRORs and 1 R.6.5 ERROR because those diagnostics come from `[opt]` advisory steps whose exit codes do NOT fold into the final gate exit. [`MAINTENANCE.md §4.1`](../../MAINTENANCE.md) describes the bypass as the mechanism that admits commits "if and only if every file causing an error has a corresponding open Task whose `task_affects_paths` covers the offending file." A reader who sees ERROR lines + a PASS summary could conclude the bypass admitted them — when in fact the diagnostics never entered the bypass calculation at all (they don't gate).

This is the same observability gap Task 064 F23 flags (gating-vs-advisory output mixing); F32 is the spec-side complement.

**Concrete diffs:**

- [`MAINTENANCE.md §4.1`](../../MAINTENANCE.md) SHOULD add a closing sentence: "Advisory-tier `[opt]` diagnostics (including the trust-audit AGGREGATOR, the staleness audit, the dup-id linter, and the prompt-* linters) emit `<path>::ERROR:CODE:msg` lines that are NOT subject to the bypass calculation because they do not contribute to the gate's exit code. Bypass applies only to the gating steps `[1/6]–[6/6]`."
- Cross-link Task 064 F23 so the output-format fix and the bypass-clarification ship together.

### F33 — No-op `adr-synthesize` records pollute `maintenance/run-log.md`

**Symptom.** [`maintenance/run-log.md`](../../maintenance/run-log.md) lines 978–1037 contain four `Run 2026-05-12 — adr-synthesize` records with identical `start_commit == end_commit == 6e4859d` and zero counters. They add no maintenance signal — the synthesize run was a no-op (no ADR added or rewritten). Each record nonetheless becomes a fall-forward target for the Step 1a awk (which is the F29 root cause).

**Concrete diffs:**

- [`tools/adr/cli.py`](../../tools/adr/cli.py) `synthesize` command SHOULD skip appending a run-log record when `start_commit == end_commit` AND `t1_fixes + t2_fixes + t3_tasks_created == 0` AND the synthesis output is byte-identical to the pre-existing `AGENTS.md` guarded block. Log the suppression to stderr so the action is observable.
- (Alternative) Keep the record but flag it `routine_type: adr-synthesize-noop`; the F29 awk filter would already skip it because it filters on `coherence-check`.

## Plan

1. **Confirm Task 025 / 044 / 064 statuses.** All three are `task_status: open` at file time. Per Task 064 F21, this Task's filing IS the falsification evidence the cadence rule needs. The Task 096 owner SHOULD cite this dynamic in F27/F28's resolution and decide whether to land F21 ahead of F27–F33 (closing 064 first) or in parallel.
2. **Execute the [TASK.md §4.9](../../TASK.md#49-planning-pipeline-for-t3-structural-tasks-sc-ladder) `/sc:*` planning ladder.** Crosses T3 threshold (root-spec edit, >3 files). Produce `workflow.md` artefact per T.4.9.2 before authoring the Plan-detail subtasks.
3. **Land F27 (tier classification of FL-declaration repairs).** Amend MAINTENANCE.md §1 T1 + T2 rows; cross-link Task 044 F14.
4. **Land F28 (AGGREGATOR dedup predicate).** Amend MAINTENANCE.md §3.3 bullet 2; cross-link Task 064 F26.
5. **Land F29 (run-log baseline filter).** Promote §2.3 prose note to MUST; amend `prompts/repo-coherence-check/prompt.md` Step 1a awk.
6. **Land F30 (staleness triage threshold).** Amend MAINTENANCE.md §3.4 closing paragraph; document `MAINT_STALENESS_TRIAGE_THRESHOLD`.
7. **Land F31 (T3 → §4.9 cross-link).** One-line MAINTENANCE.md §1 amendment.
8. **Land F32 (bypass advisory clarification).** One-sentence MAINTENANCE.md §4.1 amendment; cross-link Task 064 F23.
9. **Land F33 (adr-synthesize no-op suppression).** Either suppress the record or introduce the `adr-synthesize-noop` `routine_type` value (decide in `/sc:design`).
10. **Append `friction-log.md`** with `**Highest Frustration Level: FL[0-3]**` declaration and per-finding disposition.

## Todo

- [ ] 1. Confirm Task 025 / 044 / 064 statuses; document the F21 falsification dynamic in `notes.md`.
- [ ] 2. Execute `/sc:analyze → /sc:brainstorm → /sc:design → /sc:workflow`; commit `workflow.md`.
- [ ] 3. Land F27 (MAINTENANCE.md §1 T1+T2 row additions).
- [ ] 4. Land F28 (MAINTENANCE.md §3.3 dedup predicate).
- [ ] 5. Land F29 (MAINTENANCE.md §2.3 + coherence prompt Step 1a awk filter).
- [ ] 6. Land F30 (MAINTENANCE.md §3.4 triage threshold + env var).
- [ ] 7. Land F31 (MAINTENANCE.md §1 T3 → TASK.md §4.9 cross-link).
- [ ] 8. Land F32 (MAINTENANCE.md §4.1 advisory clarification).
- [ ] 9. Land F33 (`tools/adr/cli.py` no-op record suppression).
- [ ] 10. Produce `friction-log.md` with canonical FL declaration and per-finding disposition.

## Links

- Found by: coherence-check run 2026-05-18 (see [`maintenance/run-log.md`](../../maintenance/run-log.md) entry for `Run 2026-05-18`).
- Sibling Tasks (independent, not predecessors): [`Task 025`](../025-maintenance-spec-remaining-findings/task.md), [`Task 044`](../044-improve-maintenance-spec-may-07-2026/task.md), [`Task 064`](../064-improve-maintenance-spec-may-08-2026/task.md).
- Cross-cutting precedents: Task 044 F14 (FL canonicalisation), Task 064 F21 (one-open-Task cadence), Task 064 F23 (gating vs advisory output), Task 064 F26 (skip-with-citation).
- Governing specs: [`MAINTENANCE.md`](../../MAINTENANCE.md), [`prompts/repo-coherence-check/prompt.md`](../../prompts/repo-coherence-check/prompt.md), [`TASK.md`](../../TASK.md), [`CLAUDE.md`](../../CLAUDE.md).
- Linked prompt: [`prompts/improve-maintenance-spec-may-18-2026/prompt.md`](../../prompts/improve-maintenance-spec-may-18-2026/prompt.md).
