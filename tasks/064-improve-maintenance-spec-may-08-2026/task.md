---
type: task
status: active
slug: improve-maintenance-spec-may-08-2026
summary: "Distil seven findings (F20–F26) from the 2026-05-08 coherence run into concrete diffs against MAINTENANCE.md, prompts/repo-coherence-check/prompt.md, tools/check-governance.sh, and maintenance/run-log.md. Companion to Task 044 (open) and Task 025 (open) carrying earlier findings."
created: 2026-05-08
updated: 2026-05-08
task_id: "064"
task_status: open
task_owner: "unassigned"
task_priority: P2
task_uses_prompts: []
task_spawns_research: []
task_spawns_prompts: []
task_blocked_by: []
task_supersedes: []
task_superseded_by: []
task_affects_paths:
  - MAINTENANCE.md
  - prompts/repo-coherence-check/prompt.md
  - tools/check-governance.sh
  - maintenance/run-log.md
  - CLAUDE.md
---

# Task 064 — Improve Maintenance Spec from 2026-05-08 Coherence Run

## Goal

Each of the seven findings F20–F26 below MUST land as either (a) a concrete diff against [`MAINTENANCE.md`](../../MAINTENANCE.md), [`prompts/repo-coherence-check/prompt.md`](../../prompts/repo-coherence-check/prompt.md), [`tools/check-governance.sh`](../../tools/check-governance.sh), [`maintenance/run-log.md`](../../maintenance/run-log.md), or [`CLAUDE.md`](../../CLAUDE.md); OR (b) a documented `won't-fix` disposition in this Task's `friction-log.md` with rationale. The Task closes when every finding has either a landed diff or a recorded disposition. Companion (NOT successor) to [Task 044](../044-improve-maintenance-spec-may-07-2026/task.md) (F14–F19, open) and [Task 025](../025-maintenance-spec-remaining-findings/task.md) (F2/F3/F4/F7, open).

## Findings

### F20 — Operator-driven `/sc:*` closing sequence is undocumented in the spec

**Symptom.** The 2026-05-08 operator instruction at session close was an explicit ordered sequence: `/sc:analyze → /sc:reflect → /sc:improve → /sc:Review → /sc:createPR`. This sequence is observably stable across recent sessions (the operator's standing closing protocol). [`CLAUDE.md §10`](../../CLAUDE.md) documents only the `/sc:createPR` terminator; [`prompts/repo-coherence-check/prompt.md`](../../prompts/repo-coherence-check/prompt.md) Step 5 stops at `commit`. Neither MAINTENANCE.md nor the coherence prompt documents the four upstream skill invocations.

The gap matters because future agents lack a known-good closing protocol; they SHOULD either replicate the operator's sequence or have a spec-blessed alternative. Today the sequence is implicit operator memory.

**Concrete diffs:**

- [`prompts/repo-coherence-check/prompt.md`](../../prompts/repo-coherence-check/prompt.md) SHOULD add a Step 7 "Post-Commit Closing Protocol" listing the recommended sequence: `/sc:analyze` (delta sanity), `/sc:reflect` (validation against governance), `/sc:improve` (any latent T1/T2 the linter missed), `/sc:Review` (self-review), `/sc:createPR` (terminator). Mark the four upstream skills RECOMMENDED, the terminator REQUIRED (per [CLAUDE.md §10](../../CLAUDE.md)).
- [`MAINTENANCE.md §4`](../../MAINTENANCE.md) "Finalising Any Run" SHOULD reference the closing-protocol section in the prompt rather than duplicate it.
- (Won't-fix candidate) If the team prefers the `/sc:*` skill catalogue stay decoupled from the maintenance spec (skill catalogue evolves), record that disposition with rationale.

### F21 — `improve-maintenance-spec-*` Task accumulation lacks an enforcing function

**Symptom.** Tasks 014 (updated → 025), 025 (open), 032 (done), 044 (open), and now 064 are all in the same lineage. F16 from the 2026-05-07 run already flagged "the maintenance-spec improvement Tasks (025, 032, 044) are accumulating in parallel without a forcing function for landing their diffs." The same shape repeated this session. The lineage now has **three open Tasks** (025, 044, 064) carrying overlapping but non-identical finding sets.

The accumulation is structural: every coherence run produces session-distilled findings; the operator's standing instruction asks for a fresh Task per session; without a merge cadence the open-Task count grows monotonically. Three open improve-maintenance Tasks is already the threshold where finding ownership becomes ambiguous (F15/F16 ownership in Task 044's Plan-1 is a symptom).

**Concrete diffs (one of):**

- (Preferred) [`MAINTENANCE.md`](../../MAINTENANCE.md) SHOULD add a §6 "Self-Improvement Cadence Rule": at most ONE open `improve-maintenance-spec-*` Task at a time. New session insights MUST be appended to the open Task's `notes.md` rather than spawning a new Task. The new-Task spawn is permitted only when the existing Task transitions to `task_status: done` or `updated`.
- (Alternative) Add a `tools/fm/query.py` recipe that lists open `improve-maintenance-spec-*` Tasks; surface in the coherence prompt's Step 4 dedup gate (R4) so an agent cannot file a new one without first checking the open count.
- (Won't-fix candidate) Accept the accumulation as the cost of session-bounded distillation; record rationale ("each session's findings are time-stamped and traceable, the open-count is its own audit signal").

### F22 — `tasks/readme.md` index discipline only triggers at commit time

**Symptom.** [Task 031](../031-sync-tasks-index-status-drift/task.md) shipped `tools/fm/index_diff.py` as `[6/6] Tasks-index freshness` in `tools/check-governance.sh`. The linter runs at pre-commit but provides no in-session signal: a long-running session that creates multiple Tasks pre-commit invalidates the index N times before the gate runs. The agent has no surface to confirm "the index is in sync after Task NNN was filed" without running the full governance suite.

In this run, Task 064 (this Task) is filed mid-session; the pre-commit gate will catch a missing bullet, but the gate runs at the END of the session. An author who batches Task creation can lose track of which bullets they have/haven't added.

**Concrete diffs:**

- [`prompts/repo-coherence-check/prompt.md`](../../prompts/repo-coherence-check/prompt.md) Step 4 (Writing a Task for a T3 Finding) SHOULD add a final substep: "After staging the new Task folder, run `python3 tools/fm/index_diff.py` and stage any required `tasks/readme.md` bullet update in the same commit-stage."
- [`MAINTENANCE.md §3.4`](../../MAINTENANCE.md) Stale-Task Audit SHOULD cross-reference [Task 031](../031-sync-tasks-index-status-drift/task.md)'s linter as the canonical mid-session check, not just the pre-commit gate.
- (Optional) `tools/fm/index_diff.py` SHOULD support a `--quick` flag (NOT a new subcommand — the existing dispatcher path `python3 tools/fm/fm.py index-diff --quick` MUST be the single surface) that exits 0 for in-sync state without printing anything, suitable for an in-session sanity check.

### F23 — `tools/check-governance.sh` output mixes gating and advisory errors visually

**Symptom.** Running `tools/check-governance.sh` on this session emitted ~50 lines containing the literal token `ERROR:` (e.g. `research/...::ERROR:TRUST.SCHEMA:...`, `tasks/...::ERROR:FR.B.4:malformed:...`, `research/gemini/...::ERROR:R.6.5:no-downstream-task`) and concluded with `=== PASS: all governance checks passed. ===`. The PASS is correct: the ERROR lines are emitted by `[opt]` advisory linters whose exit codes are not folded into the final gate. But a reader (human or AI) who skims the output could conclude the repo is in violation when it is not.

The gating-vs-advisory distinction is encoded in section headers (`--- [opt] ... ---`) but NOT in the per-line diagnostic format. Every advisory ERROR line looks identical in shape to a gating ERROR line.

**Concrete diffs:**

- [`tools/check-governance.sh`](../../tools/check-governance.sh) SHOULD prepend `[advisory] ` to every diagnostic line emitted from an `[opt]` step (e.g. `tasks/...::ERROR:FR.B.4:malformed:...` becomes `[advisory] tasks/...::ERROR:FR.B.4:malformed:...`). Gating diagnostics retain their current format. Implementation note: the script currently aggregates only one final exit code; achieving the count summary requires capturing each step's exit code into per-step counters (e.g. `step_exit=$?` after each invocation, accumulated into `gating_errors` / `advisory_errors` shell variables) before the final summary line.
- The final PASS / FAIL summary SHOULD include counts: e.g. `=== PASS: all gating checks passed (0 gating errors, 53 advisory errors). ===`.
- [`MAINTENANCE.md §6` (new)](../../MAINTENANCE.md) (or §1.1) SHOULD document the gating-vs-advisory line-format convention so readers know what to grep for.

### F24 — Coherence prompt does not declare linter-first as the canonical path on large deltas

**Symptom.** This session's delta is 193 files. Step 2 of [`prompts/repo-coherence-check/prompt.md`](../../prompts/repo-coherence-check/prompt.md) instructs the agent to triage every changed file individually; Step 2.5 ("Linter-First Triage") was added post-Task-014/017 as a refinement *after* Step 2. The current prose presents 2.5 as supplementary. In practice, on this 193-file delta, the agent ran 2.5 first and never executed the file-by-file triage of Step 2 — the linter pre-classified all 193 files as conformant.

The same pattern held on the 2026-05-06 run (51 files in delta, 12 scanned) and the 2026-05-07 run (297 files in delta, 8 scanned). Linter-first IS the canonical path for any delta > ~20 files. The prompt should reflect this.

**Concrete diffs:**

- [`prompts/repo-coherence-check/prompt.md`](../../prompts/repo-coherence-check/prompt.md) SHOULD reorder: rename Step 2 to "Step 2 — Linter-First Triage" and fold the current Step 2.5 content into it; rename the current Step 2 manual-classification table to "Step 2b — Per-File Triage Fallback" and mark it conditional ("invoke ONLY for files that the linter could not classify, e.g. non-Markdown files in the delta or paths outside the linter's scope"). Keep the reflection gate count.
- The reordered Step 2 SHOULD state explicitly: "When `tools/check-governance.sh` exits 0 against the delta, no per-file triage is required; proceed to Step 3 with an empty triage table." This eliminates the agent's ambiguity on a clean delta.
- [`MAINTENANCE.md §2.2`](../../MAINTENANCE.md) "What it Does" bullet 3 ("Scans only the changed files in the delta") SHOULD be amended to "Pre-classifies the delta via `tools/check-governance.sh`; per-file inspection is only required for paths the linter could not classify."

### F25 — `TodoWrite` enum is case-sensitive but the constraint is undocumented

**Symptom.** The `TodoWrite` deferred tool's status enum requires lower-case `pending|in_progress|completed`. An initial call with mixed-case status values (the natural form an agent might emit when constructing a list) failed with an `InputValidationError` listing valid options. Minor friction; non-blocking once the constraint is known.

This is an agent-tool friction (Claude Code harness), not a maintenance-spec issue per se. The disposition is most likely `won't-fix: out of scope for MAINTENANCE.md (tool harness, not repo governance)`. Recorded for completeness.

**Concrete diffs (won't-fix candidate):**

- (Won't-fix) Out of scope for `MAINTENANCE.md`; the Claude Code harness owns `TodoWrite` schema documentation. Recorded in this Task's `friction-log.md` for traceability.
- (Alternative) Add a one-line note to [`CLAUDE.md §Using your tools`](../../CLAUDE.md) reminding agents that `TodoWrite` enum values are lower-case.

### F26 — "Covered by existing open Task" skip pattern is unspecified

**Symptom.** The 2026-05-07 run-log entry recorded `issues_skipped: 1` with prose rationale "already captured in [Task 032 §F8](../tasks/032-improve-maintenance-spec-may-2026/task.md)". This run encountered the same pattern: the persistent advisory ERRORs (FR.B.4 friction-log format, R.6.5 downstream-Task gap) are already filed under Task 044 / Task 038 territory. The right disposition is **skip-with-citation**, not refile.

[`MAINTENANCE.md §3`](../../MAINTENANCE.md) and the coherence prompt's Step 4 R4 reflection gate touch on dedup ("Is any Task redundant with an existing open Task in `/tasks/`?") but do not formalize the "covered-by-existing-open-Task → skip + cite" pattern as the canonical disposition. The maintenance-bypass mechanism (§4.1) handles a related but distinct case (errors covered by a Task's `task_affects_paths`); F26 is about issues NOT yet errors but already filed as findings in another open Task's `## Findings` section.

**Concrete diffs:**

- [`MAINTENANCE.md §3`](../../MAINTENANCE.md) (or §3.4) SHOULD add a "Skip-with-Citation Disposition" subsection: a coherence-run finding MAY be skipped (not refiled) when a currently-open Task lists the finding in its `## Findings` section by code. The run-log `notes:` block MUST cite the absorbing Task and finding code.
- [`prompts/repo-coherence-check/prompt.md`](../../prompts/repo-coherence-check/prompt.md) Step 4 R4 SHOULD enumerate the dedup check: (a) summary substring match, (b) `## Findings` heading match, (c) `task_affects_paths` overlap. If any matches, skip-with-citation rather than file a new Task.
- [`maintenance/run-log.md`](../../maintenance/run-log.md) record format SHOULD document `issues_skipped: <count>` semantics: "issues found by triage but covered by an existing open Task's findings; cite the Task in `notes:`."

## Plan

1. **Confirm Task 044 / Task 025 statuses.** Both are open at file time. Decide F20 ownership: this Task documents the closing-protocol, Task 044 documents single-finding F18 (operator-instructed commit carve-out). The two are complementary, not duplicative.
2. **Land F20 (closing-protocol documentation).** Amend the coherence prompt with Step 7; cross-reference from MAINTENANCE.md §4. Decide whether to mention `/sc:*` skill names verbatim or use a generic "self-review → improvement → review → PR" pattern.
3. **Land F21 (self-improvement cadence rule).** Amend MAINTENANCE.md with the §6 "Self-Improvement Cadence Rule" section. Coordinate with Task 044's outcome — if Task 044 closes first, the rule comes into effect when Task 064 closes (then Task 064 IS the open Task and no parallel one MAY be filed).
4. **Land F22 (in-session index_diff hook).** Coordinate with Task 031's already-shipped linter; the diff is purely a prompt amendment plus a `--quick` mode option.
5. **Land F23 (gating-vs-advisory line format).** Edit `tools/check-governance.sh` to prepend `[advisory] ` to advisory-step output. Compute and emit the count summary. Verify no downstream parser breaks.
6. **Land F24 (linter-first as canonical Step 2).** Reorder the coherence prompt's Steps 2 / 2.5; renumber reflection gates if needed. Amend MAINTENANCE.md §2.2 bullet 3.
7. **Land F25 (TodoWrite case sensitivity).** Default disposition: `won't-fix` with rationale (out of scope). Optional: one-line note in CLAUDE.md §Using your tools.
8. **Land F26 (skip-with-citation pattern).** Amend MAINTENANCE.md §3.4 with the disposition subsection; amend coherence prompt Step 4 R4 with the three-axis dedup check; document `issues_skipped:` semantics in `maintenance/run-log.md` record format header.
9. **Append `friction-log.md`** with FL[0-3] declaration (canonical no-separator form per [Task 044 F14](../044-improve-maintenance-spec-may-07-2026/task.md)) and per-finding disposition (`landed: <commit>` or `won't-fix: <reason>` or `delegated to Task NNN`).

## Todo

- [ ] 1. Confirm Task 044 / Task 025 statuses; verify F20–F26 do not duplicate prior findings.
- [ ] 2. Land F20 (coherence prompt Step 7 closing protocol + MAINTENANCE.md §4 cross-ref).
- [ ] 3. Land F21 (MAINTENANCE.md §6 self-improvement cadence rule).
- [ ] 4. Land F22 (coherence prompt Step 4 substep + optional `index_diff --quick` mode).
- [ ] 5. Land F23 (`tools/check-governance.sh` `[advisory]` prefix + count summary).
- [ ] 6. Land F24 (coherence prompt Step 2 reorder + MAINTENANCE.md §2.2 amendment).
- [ ] 7. Land F25 (won't-fix disposition or one-line CLAUDE.md note).
- [ ] 8. Land F26 (MAINTENANCE.md §3.4 skip-with-citation + coherence prompt R4 + run-log header).
- [ ] 9. Produce `friction-log.md` with canonical FL declaration and per-finding disposition.

## Links

- Found by: coherence-check run 2026-05-08 (see [`maintenance/run-log.md`](../../maintenance/run-log.md) entry for `Run 2026-05-08`).
- Sibling Tasks (independent, not predecessors):
  - [`Task 025`](../025-maintenance-spec-remaining-findings/task.md) (F2/F3/F4/F7 from 2026-05-05).
  - [`Task 044`](../044-improve-maintenance-spec-may-07-2026/task.md) (F14–F19 from 2026-05-07; F18/F19 absorbed from PR #74).
- Predecessor lineage (informational, not supersession): [`Task 014`](../014-improve-maintenance-spec-from-session/task.md), [`Task 032`](../032-improve-maintenance-spec-may-2026/task.md).
- Governing specs: [`MAINTENANCE.md`](../../MAINTENANCE.md), [`prompts/repo-coherence-check/prompt.md`](../../prompts/repo-coherence-check/prompt.md), [`CLAUDE.md`](../../CLAUDE.md), [`TASK.md`](../../TASK.md).
