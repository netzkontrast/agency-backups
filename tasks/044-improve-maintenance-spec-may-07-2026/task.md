---
type: task
status: active
slug: improve-maintenance-spec-may-07-2026
summary: "Distil six findings (F14–F19) from the 2026-05-07 coherence run and PR #74 review into concrete diffs against MAINTENANCE.md, FRUSTRATED.md, prompts/repo-coherence-check/prompt.md, tools/check-trust.py, maintenance/run-log.md, and templates/. Companion to Task 025 (open) and Task 032 (open) which carry earlier findings."
created: 2026-05-07
updated: 2026-05-11
task_id: "044"
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
  - FRUSTRATED.md
  - TASK.md
  - prompts/repo-coherence-check/prompt.md
  - tools/check-trust.py
  - templates/
---

# Task 044 — Improve Maintenance Spec from 2026-05-07 Coherence Run

## Goal

Each of the six findings F14–F19 below MUST land as either (a) a concrete diff against [`MAINTENANCE.md`](../../MAINTENANCE.md), [`FRUSTRATED.md`](../../FRUSTRATED.md), [`TASK.md`](../../TASK.md), [`prompts/repo-coherence-check/prompt.md`](../../prompts/repo-coherence-check/prompt.md), [`tools/check-trust.py`](../../tools/check-trust.py), [`maintenance/run-log.md`](../../maintenance/run-log.md), or [`templates/`](../../templates/); OR (b) a documented `won't-fix` disposition in this Task's `friction-log.md` with rationale. The Task closes only when every finding has either a landed diff or a recorded disposition. Companion (NOT successor) to [Task 025](../025-maintenance-spec-remaining-findings/task.md) (F2/F3/F4/F7 from 2026-05-05) and [Task 032](../068-improve-maintenance-spec-may-2026/task.md) (F8–F13 from 2026-05-06). Findings F18 and F19 absorbed from PR #74 review (R-3 and G-1 respectively); see [`maintenance/pr-74-review.md`](../../maintenance/pr-74-review.md).

## Findings

### F14 — Friction-log FL declaration format is not canonicalised

**Symptom.** [`tasks/041-extract-subtask-prompts/friction-log.md`](../041-extract-subtask-prompts/friction-log.md) was authored with `**FL: 2**` (with a colon-space separator). The corpus convention is `FL2` (no separator), and [`tools/check-trust.py`](../../tools/check-trust.py) line 33 enforces a `\bFL[0-3]\b` regex that the colon-form fails. Trust check rejected the friction-log; the 2026-05-07 coherence run had to apply a T1 mechanical fix.

The author intent was correct — they declared FL2 with a clear stylistic flourish — but the linter has no recovery for sympathetic variants. Future authors will keep tripping the same wire because:

- [`FRUSTRATED.md`](../../FRUSTRATED.md) does not pin a single canonical surface form for the FL declaration.
- The friction-log template (if any exists under `templates/`) does not show the declaration line in the canonical form.
- The linter's failure message is a flat "does not contain an FL[0-3] declaration" without suggesting the canonical surface form.

**Concrete diffs (one or more):**

- [`FRUSTRATED.md`](../../FRUSTRATED.md) MUST add a "Canonical Declaration Form" subsection: the declaration line MUST match the regex `\bFL[0-3]\b` (case-sensitive, no separator, optionally surrounded by Markdown emphasis). Provide three accepted examples and three rejected examples.
- [`templates/`](../../templates/) SHOULD ship a `friction-log.md` template (if it does not already) with the canonical declaration line at the top.
- [`tools/check-trust.py`](../../tools/check-trust.py) line 67-71 SHOULD widen the failure message to suggest the canonical form (e.g. `... does not contain an FL[0-3] declaration. Expected literal pattern: 'FL0', 'FL1', 'FL2', or 'FL3' (no separator).`).

### F15 — Duplicate task_id collisions recur because there is no pre-merge mechanical gate

**Symptom.** The 2026-05-07 coherence run filed [Task 043](../043-renumber-duplicate-task-ids-v3/task.md) — the third in the lineage [Task 013](../013-renumber-duplicate-task-ids/) → [Task 024](../024-renumber-duplicate-task-ids-v2/) → Task 043. Each renumber Task captures the same structural finding: parallel branches each picked the locally-next-free `<NNN>` against their own branch state, the merges landed, and the collision became the next agent's problem.

[TASK.md §8.1](../../TASK.md) places the cross-branch check on the agent ("Run `git fetch origin main && git ls-tree -r --name-only origin/main tasks/ | grep '^tasks/<NNN>-' || true`"). [Task 032 finding F13](../068-improve-maintenance-spec-may-2026/task.md) calls for adding the same check to the coherence prompt's Step 4. Both are agent-side mitigations; neither is a forcing function.

The May 2026 merge wave produced two collisions despite the spec carrying the rule for two years. The pattern is now stable enough that a CI-time mechanical gate is warranted — relying on agent obligation has not worked.

**Concrete diffs (one of):**

- (Preferred) Add a CI workflow check (`.github/workflows/`) that, on every PR, runs `python3 tools/fm/validate.py --type-check` (or a new `tools/fm/validate.py --check-task-ids` mode) which scans the union of `git ls-tree origin/main tasks/` ∪ `git ls-tree HEAD tasks/` and rejects the PR if any `<NNN>` slot has two folders. The check MUST run before merge.
- (Alternative) Add a `tools/fm/preflight.py` script that the pre-commit hook calls; on a duplicate detection, it offers the next free slot and a one-command rename suggestion.
- (Document-only) If neither lands, [`MAINTENANCE.md §3.5`](../../MAINTENANCE.md) MUST be amended to record the recurring failure mode as an accepted operational cost and the renumber Task pattern as a permanent fixture rather than a transient remediation.

### F16 — `tasks/readme.md` membership drift is not blocked at commit time

**Symptom.** [Task 042](../042-dramatica-nav-followups/task.md) was committed without a corresponding bullet in [`tasks/readme.md`](../readme.md), in violation of [TASK.md §4.8 / §6 Gherkin "New Task folder appears in the index immediately"](../../TASK.md). The 2026-05-07 coherence run added the bullet manually while authoring the Task 043 entry. The drift surfaced incidentally; no mechanical surface caught it.

This is the same shape as the 10-bullet status-drift that the 2026-05-06 coherence run found and filed as [Task 031](../067-sync-tasks-index-status-drift/task.md), but on the *membership* axis rather than the *status* axis. Task 031's plan covers both axes ("ship `fm.py index-diff` or `fm-query --diff tasks/readme.md`"). The risk is that Task 031's scope is so broad it stalls — this finding raises the priority of the membership half.

**Concrete diffs:**

- Confirm Task 031's Plan covers both axes (membership + status); if not, amend its Plan to explicitly list both. Do NOT split the work — keep one Task per [TASK.md §7.11](../../TASK.md).
- Pending Task 031 landing, the coherence prompt's Step 2.5 SHOULD include a diff-friendly `awk` recipe that lists every `tasks/<NNN>-<slug>/` on disk and every `[<NNN>-<slug>/](./...)` bullet in `tasks/readme.md`, then highlights the symmetric difference. Treat any non-empty diff as a T1/T2 issue.
- [`MAINTENANCE.md §4`](../../MAINTENANCE.md) "Finalising Any Run" SHOULD add a 7th bullet: "tasks/readme.md MUST list every `tasks/<NNN>-<slug>/` folder on disk and no orphan bullets, per `TASK.md §4.8`".

### F17 — /sc: skill family fit for coherence runs is undocumented

**Symptom.** The 2026-05-07 operator instruction was "use /sc: skills if helpful" during the coherence run. The /sc:* skill family (visible in this session's skill list) is designed for /sc:implement, /sc:design, /sc:research, /sc:troubleshoot, etc. — flavours that do not match the coherence routine's intentionally mechanical "linter-first → tier-classified repairs → Task creation" loop. The skill list is large enough that an agent unfamiliar with the routine might over-invoke skills that don't help, or under-invoke ones that do.

The maintenance protocol is silent on this. The coherence prompt's Constraints section (§6) calls out what NOT to do (no content rewriting, no T3/T4 direct edits) but does not say which skill flavour fits the work. /sc:reflect (task reflection / validation), /sc:cleanup (systematic cleanup), and /sc:analyze (comprehensive code analysis) plausibly map to subgoals of the coherence routine but have not been tried.

**Concrete diffs:**

- [`MAINTENANCE.md §2`](../../MAINTENANCE.md) "Repo Coherence Check" SHOULD add a one-paragraph "Skill Fit" subsection: the routine is primarily mechanical and does NOT benefit from /sc:implement, /sc:design, or /sc:research; /sc:cleanup and /sc:analyze MAY be invoked as supplementary lenses but their output MUST NOT replace the linter-first triage; /sc:reflect MAY be useful at the end of the run as a validation gate alongside the post-repair linter check (cf. [Task 032 finding F10](../068-improve-maintenance-spec-may-2026/task.md)).
- [`prompts/repo-coherence-check/prompt.md`](../../prompts/repo-coherence-check/prompt.md) Constraints section SHOULD add a constraint: "/sc: skills MAY be invoked as supplementary lenses but MUST NOT bypass the Step 2.5 linter-first triage."
- (Won't-fix candidate) If the team prefers the spec stay silent on per-skill fit (skill catalogue evolves), record that disposition in this Task's friction-log with rationale.

### F18 — Coherence prompt has no carve-out for operator-instructed post-run commits

**Symptom.** Absorbed from [PR #74 review R-3](../../maintenance/pr-74-review.md). [`prompts/repo-coherence-check/prompt.md`](../../prompts/repo-coherence-check/prompt.md) Step 5 mandates: *"All T1 and T2 repairs, any new Tasks, and the run-log entry (Step 6) MUST be committed together in a single atomic commit."* The 2026-05-07 PR (#74) ships two commits — one for the coherence-run output (`9172de7`) and one for the operator-instructed Task 044 distillation (`ad53c05`). The split is a reasonable operational distinction: Task 044 was filed in response to a separate operator instruction (*"After you Are Done, collect all Information about the current Session, that could Help to further Improve the Maintenance spec and submit a new Task"*), not as part of the coherence run's own T3 output.

The protocol currently makes no provision for this category. Future agents and reviewers cannot distinguish a legitimate operator-instructed follow-up commit from a protocol violation without reading the PR body.

**Concrete diffs:**

- [`prompts/repo-coherence-check/prompt.md`](../../prompts/repo-coherence-check/prompt.md) Step 5 SHOULD add: *"If the operator issues an additional instruction after the coherence commit (e.g. to distil session findings into a follow-up Task), that action MAY be committed separately with a `feat(task-NNN):` prefix commit message distinct from the `chore(coherence):` commit."*
- [`MAINTENANCE.md §4`](../../MAINTENANCE.md) "Finalising Any Run" SHOULD mirror the carve-out so the spec and the prompt agree.

### F19 — Run-log lacks distinction between confirmed-conformant and skipped-as-conformant files

**Symptom.** Absorbed from [PR #74 review G-1](../../maintenance/pr-74-review.md). The 2026-05-07 run-log entry records `files_in_delta: 297`, `files_scanned: 8`, `t4_skipped: 2`. That leaves 287 files whose disposition is documented only in the prose `notes:` block as "already conformant per Task 041 closure" / "already conformant per the chain authoring". The prose is accurate but mechanically opaque: a future audit cannot verify that the 287 unscanned files were actually inspected and found clean, vs silently ignored.

The current run-log schema treats "scanned" and "skipped" as the only two categories. The linter-first triage approach (Step 2.5) introduces a third category — files that the linter pre-cleared, which the agent counted but did not open. Without a field to capture this third category the run-log under-reports the agent's actual inspection coverage.

**Concrete diffs:**

- [`maintenance/run-log.md`](../../maintenance/run-log.md) record format SHOULD add a `files_linter_cleared:` field. Definition: count of files in the delta that the canonical linter (`tools/check-governance.sh`) reported clean and the agent therefore did not need to open. Adjust the implicit identity `files_scanned + files_linter_cleared + t4_skipped + non_markdown_skipped == files_in_delta`.
- [`MAINTENANCE.md §2.3`](../../MAINTENANCE.md) Run-Log Protocol SHOULD list the new field alongside the existing schema.
- Backfill the new field on existing records is OPTIONAL (the field is additive); only the record format header MUST be updated.

## Plan

1. **Confirm Task 031 / Task 032 status.** Both Tasks are still open at file time. F15 (cross-branch task_id check) overlaps Task 032 finding F13; F16 (readme.md membership drift) overlaps Task 031 scope. Decide F15 / F16 ownership: this Task records `delegated to Task NNN` if the existing Task absorbs the work, or files an additive diff if it does not.
2. **Land F14 (FL declaration canonicalisation).** Amend FRUSTRATED.md with the canonical surface form section. Optionally: ship a `templates/friction-log.md` (verify whether one exists first) and widen the trust-check failure message.
3. **Land F15 (cross-branch duplicate-task_id mechanical gate).** Coordinate with Task 032 finding F13. Decide between CI workflow vs pre-commit `tools/fm/preflight.py`. Default to CI workflow if the team prefers reproducible enforcement; pre-commit if local-loop responsiveness matters.
4. **Land F16 (readme.md membership drift).** Defer to Task 031 if its Plan already covers the membership axis. If not, amend Task 031's Plan to add the membership check; do NOT split the work.
5. **Land F17 (/sc: skill fit subsection).** Amend MAINTENANCE.md §2 and the coherence prompt Constraints section. Be terse — the spec should not enumerate the full skill catalogue, only the high-level fit.
6. **Land F18 (operator-instructed commit carve-out).** Amend coherence prompt Step 5 and MAINTENANCE.md §4 to allow an operator-instructed follow-up commit with a `feat(task-NNN):` prefix distinct from the `chore(coherence):` commit.
7. **Land F19 (run-log linter-cleared field).** Add `files_linter_cleared:` to the run-log record format; update MAINTENANCE.md §2.3.
8. **Append `friction-log.md`** with FL[0-3] declaration and per-finding disposition (`landed: <commit>` or `won't-fix: <reason>` or `delegated to Task NNN`). Use the canonical FL declaration form (per F14's outcome) regardless of whether F14 has landed by then.

## Todo

- [ ] 1. Confirm Task 031 / Task 032 statuses and decide F15 / F16 ownership.
- [ ] 2. Land F14 (FRUSTRATED.md canonical FL declaration form; optional template + trust-check message widening).
- [ ] 3. Land F15 (cross-branch task_id mechanical gate) OR record `delegated to Task 032 §F13`.
- [ ] 4. Land F16 (readme.md membership check) OR record `delegated to Task 031`.
- [ ] 5. Land F17 (MAINTENANCE.md §2 + coherence prompt Constraints "Skill Fit" amendment).
- [ ] 6. Land F18 (operator-instructed commit carve-out in coherence prompt Step 5 + MAINTENANCE.md §4).
- [ ] 7. Land F19 (run-log `files_linter_cleared:` field + MAINTENANCE.md §2.3 schema doc).
- [ ] 8. Produce `friction-log.md` with FL[0-3] declaration (canonical form) and per-finding disposition.

## Links

- Found by: coherence-check run 2026-05-07 (see [`maintenance/run-log.md`](../../maintenance/run-log.md) entry).
- F18 / F19 absorbed from: [PR #74 review](../../maintenance/pr-74-review.md) findings R-3 and G-1.
- Sibling Tasks (independent, not predecessors):
  - [`Task 025`](../025-maintenance-spec-remaining-findings/task.md) (F2/F3/F4/F7 from 2026-05-05).
  - [`Task 032`](../068-improve-maintenance-spec-may-2026/task.md) (F8–F13 from 2026-05-06).
- Companion T3 from same run: [`Task 043`](../043-renumber-duplicate-task-ids-v3/task.md) (031/032 collision renumber).
- Predecessor lineage (informational, not supersession): [`Task 014`](../014-improve-maintenance-spec-from-session/task.md), [`Task 032`](../068-improve-maintenance-spec-may-2026/task.md).
- Governing specs: [`MAINTENANCE.md`](../../MAINTENANCE.md), [`FRUSTRATED.md`](../../FRUSTRATED.md), [`TASK.md`](../../TASK.md), [`prompts/repo-coherence-check/prompt.md`](../../prompts/repo-coherence-check/prompt.md).
