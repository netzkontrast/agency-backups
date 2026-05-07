---
type: task
status: active
slug: improve-maintenance-spec-may-2026
summary: "Distil six findings (F8–F13) from the 2026-05-06 coherence run into concrete diffs against MAINTENANCE.md, prompts/repo-coherence-check/prompt.md, install.sh, and TASK.md §7.11. Companion to Task 025 (open) which carries the older F2/F3/F4/F7 findings."
created: 2026-05-06
updated: 2026-05-07
task_id: "032"
task_status: done
task_owner: "claude-code (session claude/close-maintenance-spec-task-Tx7bx)"
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
  - install.sh
  - TASK.md
  - tools/check-governance.sh
  - tools/dramatica-nav/validate.py
  - tasks/readme.md
---

# Task 032 — Improve Maintenance Spec from 2026-05-06 Coherence Run

## Goal

Each of the six findings F8–F13 below MUST land as either (a) a concrete diff against [`MAINTENANCE.md`](../../MAINTENANCE.md), [`prompts/repo-coherence-check/prompt.md`](../../prompts/repo-coherence-check/prompt.md), [`install.sh`](../../install.sh), [`TASK.md`](../../TASK.md), or [`tools/check-governance.sh`](../../tools/check-governance.sh); OR (b) a documented `won't-fix` disposition in this Task's `friction-log.md` with rationale. The Task closes only when every finding has either a landed diff or a recorded disposition. Companion (NOT successor) to [Task 025](../025-maintenance-spec-remaining-findings/task.md), which is still open with F2/F3/F4/F7 from the 2026-05-05 run.

## Findings

### F8 — `tools/check-governance.sh` reports FAIL on missing optional dependency

**Symptom.** A fresh contributor running `tools/check-governance.sh` on a clean clone sees `=== FAIL: one or more checks failed. ===` solely because `python3 -c "import jsonschema"` fails. The dramatica-nav validator (the only consumer) is OPTIONAL — it is gated behind `[ -f "$NARRATIVE_ONTOLOGY" ]` — yet a missing dependency it relies on poisons the suite-level exit code.

**Concrete diffs (one of):**

- (Preferred) Pin `jsonschema>=4.0` in [`install.sh`](../../install.sh) so a fresh setup always has it. The cost is one line in install.sh and ~2 MB of wheel.
- (Alternative) `tools/dramatica-nav/validate.py` SHOULD detect the missing dependency, emit `WARN: jsonschema not installed; narrative-ontology validator skipped`, and exit 0. The script SHOULD NOT short-circuit the suite on an optional dependency.
- (Document-only) If neither lands, [`MAINTENANCE.md §5`](../../MAINTENANCE.md) MUST be amended to call out `jsonschema` as a hard prerequisite of `tools/check-governance.sh`.

### F9 — Run-log mixes coherence runs with task-implementation records

**Symptom.** [`maintenance/run-log.md`](../../maintenance/run-log.md) holds both Repo Coherence Check entries (where `t1_fixes`, `t2_fixes`, `t3_tasks_created` are sweep counts over a delta) and "Task NNN implementation" entries (where the same fields tally artefacts produced inside one Task's scope). The two record types share the field schema but the semantics diverge:

- A coherence-run `t3_tasks_created: 1` means "the agent filed one Task for a T3 finding while sweeping the delta".
- A task-implementation `t3_tasks_created: 0` means "this Task implementation did not file any further Tasks during its work" — which is operationally always true because the work IS the Task.

The `awk` fall-forward in `prompts/repo-coherence-check/prompt.md` Step 1a happily walks past task-implementation records because they declare `end_commit`. That's the right behaviour, but the two record types should be visually distinguishable so a reading agent can compute "what was the last coherence baseline" in one glance.

**Concrete diffs:**

- Add a `routine_type:` field to the record header in [`maintenance/run-log.md`](../../maintenance/run-log.md)'s "Record Format" block. Enum: `coherence-check | nightly-maintenance | task-implementation | bootstrap`.
- Amend [`MAINTENANCE.md §2.3`](../../MAINTENANCE.md) so it explicitly lists the four record types and clarifies that task-implementation records are valid baselines for the coherence fall-forward (because they advance HEAD), but their `t1/t2/t3` fields describe Task scope, not coherence-sweep scope.
- Backfill `routine_type:` on existing records: bootstrap, three coherence runs, six task-implementations, one administrative-close.

### F10 — Coherence prompt has no post-repair linter gate

**Symptom.** [`prompts/repo-coherence-check/prompt.md`](../../prompts/repo-coherence-check/prompt.md) Step 2.5 (linter-first triage, landed by Task 017) runs `tools/fm/validate.py` BEFORE repairs. Step 5 ("Commit the Repairs") does not require the agent to re-run the linter AFTER repairs and Task creation. The agent could in principle commit a state that introduces a new diagnostic.

[Task 014 finding F7 / Task 025 §Plan-4](../025-maintenance-spec-remaining-findings/task.md) calls this out, but Task 025's `task_blocked_by: ["019"]` was set when Task 019 was open. Task 019 is now `done`, so Task 025 is unblockable; this Task SHOULD coordinate with Task 025 rather than duplicate its work.

**Concrete diffs:**

- In coordination with Task 025 §Plan-4: insert a `Step 4.5 — Verify Linters Pass` between Step 4 (T3 Task creation) and Step 5 (Commit) in the coherence prompt. The step MUST run `tools/check-governance.sh` and abort the commit (and the run) on non-zero exit.
- In [`MAINTENANCE.md §4`](../../MAINTENANCE.md) "Finalising Any Run", add a 6th bullet: "`tools/check-governance.sh` MUST exit 0 against the post-repair tree."

### F11 — TASK.md §7.11 mechanical-check promise was deferred

**Symptom.** [`TASK.md §7.0`](../../TASK.md) row §7.11 says the tasks-index sync check ships under "Task 019". Task 019 closed without it. The 2026-05-06 coherence run found 10 stale `Status:` bullets in `tasks/readme.md` purely because the agent ran a hand-rolled `awk` loop; no linter caught the drift.

**Concrete diffs:**

- Re-target the §7.0 row §7.11 cell from "(Task 019)" to "([Task 031](../031-sync-tasks-index-status-drift/task.md))". (Task 031 was filed during the 2026-05-06 run for exactly this scope.)
- Add a one-line note to [`MAINTENANCE.md §3.4`](../../MAINTENANCE.md) Stale-Task Audit section that the audit's drift signal is also detectable via the §7.11 check once Task 031 lands.

### F12 — `MAINTENANCE.md §1.1` describes a coexistence state that no longer exists

**Symptom.** §1.1 prose: "Two governance toolchains coexist while [Task 017](./tasks/017-…/) and [Task 019](./tasks/019-…/) execute the migration". Both Tasks are now `task_status: done`. `FM_TOOLCHAIN=1` is the default; legacy validators run silently with `FM_LEGACY_QUIET=1` by default. The "transition state" the prose describes ended on 2026-05-05.

§1.1 also references `tools/.frontmatter-waivers` ("waiver list … consumed by the legacy validator only … will need to be re-expressed against `tools/fm/validate.py` (tracked in Task 019)"). The waiver file does not exist on disk; Task 019 closed without re-expressing it.

**Concrete diffs:**

- Rewrite [`MAINTENANCE.md §1.1`](../../MAINTENANCE.md) to describe the post-migration state: fm-validate is canonical and gating; legacy validators are advisory shims (one-release window) at `tools/legacy/`; `FM_TOOLCHAIN=0` is a documented escape hatch but not the supported configuration.
- Drop the `tools/.frontmatter-waivers` paragraph if no waivers currently exist; OR document the `tools/fm/validate.py`-native waiver mechanism if one was added by Task 019. Verify the waiver file's existence and adjust prose to reflect reality.
- [`MAINTENANCE.md §4.1`](../../MAINTENANCE.md) Maintenance Bypass Mode: confirm the prose describes `tools/check-maintenance-bypass.py`'s actual behaviour after Task 017's re-pointing (it now harvests fm-validate's `<path>::<level>:<code>:<msg>` diagnostics and folds the legacy linters in for gaps).

### F13 — Cross-branch duplicate-task_id check is missing from the coherence prompt

**Symptom.** [`prompts/repo-coherence-check/prompt.md`](../../prompts/repo-coherence-check/prompt.md) Step 4 says "you MUST run `ls tasks/ | sort` and ensure the next free `<NNN>` is used". It does NOT instruct the agent to also check `git fetch origin main && git ls-tree -r --name-only origin/main tasks/ | grep '^tasks/<NNN>-'` per [`TASK.md §8.1`](../../TASK.md) bullet 2. The two duplicate-task_id collisions tracked by Tasks 013/024 originated exactly from this gap: each collision was on a different agent's branch.

**Concrete diffs:**

- Amend Step 4 of the coherence prompt to include the `git ls-tree origin/main` check before staging a new Task folder.
- Add an acceptance scenario to TASK.md §6 asserting the cross-branch check is part of the Task-pickup flow (or recognise that this duplicates §8.1's prose and instead add a direct cross-reference from Step 4 to TASK.md §8.1 bullet 2).

## Plan

1. **Land F8 (jsonschema dependency).** Decide between install.sh pin vs validator-degrade-to-WARN. Default to install.sh pin if the team prefers reproducible CI; degrade-to-WARN if local-dev parity matters. Land the diff and re-run `tools/check-governance.sh` from a clean venv.
2. **Land F9 (run-log routine_type field).** Add the `routine_type:` field to the record format header. Backfill the eleven existing records. Update the `awk` fall-forward in the coherence prompt only if the new field changes parsing — currently it does not, the lookup keys on `end_commit:` regardless.
3. **Land F10 (post-repair linter gate).** Coordinate with Task 025 §Plan-4 — the same change is in scope for both Tasks. Decide which Task absorbs it (recommend Task 025 since it was filed first), and reference it from this Task's friction-log without duplicating the diff.
4. **Land F11 (§7.11 retarget).** Edit `TASK.md §7.0` row §7.11 to point at Task 031.
5. **Land F12 (§1.1/§4.1 sweep).** Rewrite §1.1 prose for post-migration state; verify §4.1 reflects post-Task-017 bypass behaviour; drop or update the `tools/.frontmatter-waivers` paragraph based on whether a waiver mechanism currently exists.
6. **Land F13 (cross-branch check).** Amend the coherence prompt Step 4 with the `git ls-tree origin/main` check, OR a single-line cross-reference to TASK.md §8.1 bullet 2.
7. **Append `friction-log.md`** with FL[0-3] declaration and per-finding disposition (`landed: <commit>` or `won't-fix: <reason>` or `delegated to Task NNN`).

## Todo

- [ ] 1. Confirm Task 025's status (still `task_status: open` at file time) and decide F10 ownership.
- [ ] 2. Land F8 (jsonschema dependency or graceful-degrade).
- [ ] 3. Land F9 (run-log `routine_type:` field + backfill).
- [ ] 4. Land F10 in coordination with Task 025, OR record `delegated to Task 025` disposition.
- [ ] 5. Land F11 (TASK.md §7.0 row §7.11 retarget to Task 031).
- [ ] 6. Land F12 (MAINTENANCE.md §1.1 + §4.1 sweep; verify waiver-file claim against reality).
- [ ] 7. Land F13 (coherence-prompt Step 4 cross-branch check).
- [ ] 8. Produce `friction-log.md` with FL[0-3] declaration and per-finding disposition.

## Links

- Found by: coherence-check run 2026-05-06 (see [`maintenance/run-log.md`](../../maintenance/run-log.md) entry).
- Sibling Task (independent): [`Task 025`](../025-maintenance-spec-remaining-findings/task.md) (F2/F3/F4/F7 carry-forward).
- Companion T3 from same run: [`Task 031`](../031-sync-tasks-index-status-drift/task.md) (status-drift + §7.11 linter).
- Predecessor lineage (informational, not supersession): [`Task 014`](../014-improve-maintenance-spec-from-session/task.md) (F1–F7 from the 2026-05-05 run).
- Governing specs: [`MAINTENANCE.md`](../../MAINTENANCE.md), [`TASK.md`](../../TASK.md), [`prompts/repo-coherence-check/prompt.md`](../../prompts/repo-coherence-check/prompt.md).
