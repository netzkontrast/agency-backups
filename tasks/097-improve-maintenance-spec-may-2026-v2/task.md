---
type: task
status: active
slug: improve-maintenance-spec-may-2026-v2
summary: "Distil six findings (F14–F19) from the 2026-05-17 Repo Coherence Check into concrete diffs against MAINTENANCE.md and its supporting linters (`tools/fm/check-duplicate-task-id.py`, `tools/maintenance/dynamic-readme-partition.py`, `tools/maintenance/staleness-audit.py`, `tools/maintenance/adr-trigger-audit.py`). Successor to Task 068 (closed; F8–F13) which carried the prior round of maintenance-spec findings."
created: 2026-05-17
updated: 2026-05-17
task_id: "097"
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
  - tools/fm/check-duplicate-task-id.py
  - tools/maintenance/dynamic-readme-partition.py
  - tools/maintenance/staleness-audit.py
  - tools/maintenance/adr-trigger-audit.py
  - tools/check-governance.sh
---

# Task 097 — Improve Maintenance Spec from 2026-05-17 Coherence Run

## Goal

Each of the six findings F14–F19 below MUST land as either (a) a concrete diff against [`MAINTENANCE.md`](../../MAINTENANCE.md) or one of its supporting linters under `tools/maintenance/` / `tools/fm/`; OR (b) a documented `won't-fix` disposition in this Task's `friction-log.md` with rationale. The Task closes only when every finding has either a landed diff or a recorded disposition. Successor (NOT supersession) of [Task 068](../068-improve-maintenance-spec-may-2026/task.md), which closed `done` with F8–F13.

## Findings

### F14 — `check-duplicate-task-id.py` doesn't surface §3.5 auto-fire predicates

**Symptom.** When the linter reports a collision (e.g. the `090-codex-pr-review` ↔ `090-review-pr109-archive-spec` pair that surfaced in the 2026-05-17 run), the maintenance agent must manually evaluate the four §3.5 auto-fire predicates: (1) exactly one collision pair, (2) no existing open Task covers both folders, (3) ≥1 open member, (4) `routine_type: coherence-check`. Two of those (predicates 2 and 3) require additional greps across the corpus. The agent can shortcut by skipping the evaluation and unconditionally escalating, but then it does not deliver the §3.5 promise of autonomous Task filing.

**Concrete diffs (one of):**

- (Preferred) Extend [`tools/fm/check-duplicate-task-id.py`](../../tools/fm/check-duplicate-task-id.py) to also emit an `auto-fire-eligible: YES|NO (predicate <n> failed: <reason>)` diagnostic per collision. The linter already reads `task.md` frontmatter for `task_id`; reading `task_status` and `task_affects_paths` is a one-pass extension.
- (Alternative) Add a section to [`MAINTENANCE.md §3.5`](../../MAINTENANCE.md) with a `bash` block showing the exact `grep` invocations the agent SHOULD run to evaluate each predicate. Lower mechanical value but a low-friction documentation fix.

### F15 — Stale §3.5 prose about `FM_DUPLICATE_TASK_ID_STRICT` default flip

**Symptom.** [`MAINTENANCE.md §3.5`](../../MAINTENANCE.md) currently states: *"After Task 043 lands and the corpus is dup-free, the env-var default flips to `1` and the toggle is removed in the next release window."* Task 043 has landed (corpus survey shows the prior `006/006`, `009/009`, `031/031`, `032/032` collisions are resolved), but the default in [`tools/check-governance.sh:250`](../../tools/check-governance.sh) is still `0` AND the corpus is not dup-free (the 090 collision was committed after Task 043 closed). The spec's promised flip never happened, and the spec text gives no recovery path.

**Concrete diffs (one of):**

- (Preferred) Amend §3.5 to bind the flip to a *predicate* (e.g. "the default flips to `1` when `tools/fm/check-duplicate-task-id.py tasks/` has exited `0` in three consecutive nightly maintenance runs"). This is mechanically verifiable from the run-log.
- (Alternative) Flip the default to `1` in [`tools/check-governance.sh:250`](../../tools/check-governance.sh) *after* Task 096 resolves the 090 collision and update §3.5 to reflect the new gate posture.
- (Document-only) Add an explicit "Open dup-id collisions defer the flip" sentence to §3.5 so future agents understand why the env var is still `0`.

### F16 — `dynamic-readme-partition.py` lacks a "corpus clean" promotion threshold

**Symptom.** [`MAINTENANCE.md §3.2`](../../MAINTENANCE.md) says: *"The linter is advisory-tier today; promotion to gating requires the corpus to be clean (per the Toolchain Flip SPEC §3.2 WARN→ERROR sequencing rule)."* "Corpus clean" is not defined. Is it zero `missing-marker` advisories? Zero ERROR diagnostics? A ratio? The agent has no falsification target.

**Concrete diffs (one of):**

- (Preferred) Add a numeric threshold to §3.2 (e.g. "Zero `missing-marker` advisories across every operational `readme.md` under `tasks/`, `research/`, `prompts/`") + a paired Gherkin scenario under `M.B.<n>`.
- (Alternative) Cite the Toolchain Flip SPEC §3.2 WARN→ERROR sequencing rule with the specific predicate row that applies to dynamic-readme-partition; the SPEC may already define this.

### F17 — `MAINT_STALE_DAYS` per-routine binding is illustrative-only

**Symptom.** [`MAINTENANCE.md §3.4`](../../MAINTENANCE.md) shows the env var's per-routine override pattern: `MAINT_STALE_DAYS=3` for daily coherence sweeps, `MAINT_STALE_DAYS=14` for weekly nightlies. The examples are illustrative — neither routine *binds* the value, so a coherence-run agent executing `tools/check-governance.sh` inherits the default `7` and may classify recently-filed Tasks as stale when the operator intended a 3-day window.

**Concrete diffs (one of):**

- (Preferred) Amend §3.4 to bind the routine: the Repo Coherence Check MUST export `MAINT_STALE_DAYS=3` before invoking `staleness-audit.py`; the Nightly Maintenance Run MUST export `MAINT_STALE_DAYS=14`. The bindings move from "examples" to "normative".
- (Alternative) Add a `--routine={coherence,nightly}` flag to [`tools/maintenance/staleness-audit.py`](../../tools/maintenance/staleness-audit.py) that selects the window without env-var ceremony.

### F18 — §1.0.1 commit-message rationale rule has no mechanical enforcement

**Symptom.** [`MAINTENANCE.md §1.0.1`](../../MAINTENANCE.md) says: *"Every T1 / T2 repair commit on closed research MUST carry a one-line rationale in the commit message naming the trigger."* No linter walks `git log` to verify that commits touching `research/<slug>/` paths (where `research_phase: complete`) carry the rationale. The MUST is socially enforced only.

**Concrete diffs (one of):**

- (Preferred) Ship `tools/check-closed-research-commit-rationale.py` walking commits in the run-log delta whose touched paths intersect `research/<slug>/` (`research_phase: complete`), and verifying the commit message contains either a `closed-research T1/T2:` prefix or a citation of the upstream rename/move trigger. Advisory-tier on landing; promote to gating per the standard WARN→ERROR ladder.
- (Alternative) Document the rule's social-enforcement-only status in §1.0.1 with a "Future work" pointer to a tracked Task.

### F19 — §3.6 ADR-trigger audit cadence lacks over-sampling guard

**Symptom.** [`MAINTENANCE.md §3.6`](../../MAINTENANCE.md) says: *"The Repo Coherence Check (§2) MAY invoke the audit but is NOT required to; the audit's data refreshes slowly (bundle size, skill counts, friction over a 14-day window) and the coherence-check cadence is per-session, which over-samples the predicate space."* The spec acknowledges over-sampling risk but does not enforce a guard. An over-eager coherence agent invoking the audit every session pollutes the run-log with redundant projections.

**Concrete diffs (one of):**

- (Preferred) Add a "last-invocation timestamp" check to [`tools/maintenance/adr-trigger-audit.py`](../../tools/maintenance/adr-trigger-audit.py): if the last `adr-trigger-audit` line in `maintenance/run-log.md` is < 24h old, the script exits `0` with a `skipped: rate-limited` note rather than re-running. Override via `--force` for nightly invocation.
- (Alternative) Restrict §3.6 invocation to nightly-only by binding the audit to the `nightly-maintenance` routine type and removing the "Repo Coherence Check MAY invoke" sentence.

## Plan

1. Read each finding F14–F19 above and pick one of the listed concrete diffs (or land a documented `won't-fix` in `friction-log.md`).
2. For each landed diff, update [`MAINTENANCE.md`](../../MAINTENANCE.md) prose first (the spec is the contract), then mutate the linter implementation, then add the paired Gherkin scenario under `M.B.<n>` per §6 acceptance-criteria convention.
3. For each `won't-fix`, write a one-paragraph rationale in `friction-log.md` citing the conflicting constraint.
4. Verify `tools/check-governance.sh` exits `0` after each finding lands.
5. Close the Task with `task_status: done` + a friction-log noting per-finding disposition.

## Todo

- [ ] 1. F14 — extend `check-duplicate-task-id.py` to emit auto-fire-eligibility diagnostic (OR document the eval shortcut in §3.5).
- [ ] 2. F15 — flip `FM_DUPLICATE_TASK_ID_STRICT` default to a predicate-bound trigger (OR document why it stays `0`).
- [ ] 3. F16 — define "corpus clean" threshold for `dynamic-readme-partition.py` promotion.
- [ ] 4. F17 — bind `MAINT_STALE_DAYS` per-routine (or add `--routine` flag).
- [ ] 5. F18 — ship commit-message-rationale verifier for closed-research T1/T2 repairs (OR document social-only enforcement).
- [ ] 6. F19 — add over-sampling guard to `adr-trigger-audit.py` (OR restrict §3.6 to nightly-only).
- [ ] 7. Verify `tools/check-governance.sh` exits `0`.
- [ ] 8. Close Task with friction-log per-finding disposition.

## Links

- Predecessor: [`tasks/068-improve-maintenance-spec-may-2026/`](../068-improve-maintenance-spec-may-2026/task.md) (F8–F13, closed `done`).
- Earlier predecessor: [`tasks/025-maintenance-spec-remaining-findings/`](../025-maintenance-spec-remaining-findings/task.md) (F2/F3/F4/F7).
- Companion: [Task 096](../096-resolve-090-collision/task.md) — resolves the dup-id collision that surfaced F14 and F15.
- Governing specs: [`MAINTENANCE.md`](../../MAINTENANCE.md), [`TASK.md`](../../TASK.md), [`FRUSTRATED.md`](../../FRUSTRATED.md).
- Source: 2026-05-17 Repo Coherence Check (see [`maintenance/run-log.md`](../../maintenance/run-log.md)).
