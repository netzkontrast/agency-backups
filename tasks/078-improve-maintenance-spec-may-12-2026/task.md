---
type: task
status: active
slug: improve-maintenance-spec-may-12-2026
summary: "Operationalise the MAINTENANCE.md gaps surfaced by the 2026-05-12 coherence run: post-commit end_commit backfill, dynamic-readme partition migration, staleness-audit urgency tiers, and large-delta coherence-run guidance."
created: 2026-05-12
updated: 2026-05-12
task_id: "078"
task_status: open
task_owner: "unassigned"
task_priority: P2
task_uses_prompts: []
task_spawns_research: []
task_spawns_prompts: []
task_affects_paths:
  - MAINTENANCE.md
  - prompts/repo-coherence-check/prompt.md
  - maintenance/run-log.md
  - tools/maintenance/dynamic-readme-partition.py
  - tools/maintenance/staleness-audit.py
---

# Task 078 — Improve MAINTENANCE.md from 2026-05-12 coherence-run findings

## Goal

Amend `MAINTENANCE.md` (and the coherence-check prompt) so the five concrete gaps surfaced by the 2026-05-12 maintenance run are mechanically closed: every record this Task produces MUST pass `tools/check-governance.sh` and the resulting spec MUST eliminate the `end_commit: pending` failure mode by construction (no future run-log record carries the literal token `pending` after the closing commit lands).

## Plan

1. **End-commit backfill mechanism.** Author a `tools/maintenance/run-log-backfill.py` (or fold into `tools/check-governance.sh`) that detects `end_commit: pending` in `maintenance/run-log.md`, computes the closing commit hash of the **prior** run from the git log of `maintenance/run-log.md` (the first commit *after* the malformed record's `start_commit:` that touches the run-log file is the resolvable end_commit), and rewrites the token via `tools/fm/edit.py`-style atomic mutation. **Chicken-and-egg resolution**: the backfill tool runs at the **start of each subsequent run** (or as a pre-commit hook scoped to `maintenance/run-log.md`); it repairs the *previous* record's `pending` token inside the *current* run's atomic commit, so the per-run sanction "the agent MAY write `pending` when the closing-commit hash is not yet known" is preserved while the corpus-level invariant "no record at `HEAD~1` or earlier carries `pending`" is enforced mechanically. Amend MAINTENANCE.md §2.3 to declare the literal `pending` token forbidden in any record other than the most recent (i.e. `HEAD` is the only sanctioned bearer) and to cite the new tool. Acceptance anchor: new Gherkin scenario `M.B.8 — pending end_commit backfill (HEAD-only sanction)`.
2. **Large-delta coherence-run guidance.** Amend MAINTENANCE.md §2.2 + `prompts/repo-coherence-check/prompt.md` Step 1 to define a delta-size threshold (e.g. `≥ 50 files OR ≥ 10 commits`) above which the agent MUST split the work into a Nightly Maintenance Run scope instead of a single coherence sweep. Add a "delta-bucket" classification (small / medium / large) feeding a routing decision. The 2026-05-12 run hit ~200 files since baseline 89c0aa3 with no spec guidance for that scale.
3. **Dynamic-readme partition migration plan.** The 2026-05-12 run surfaced 181 M.B.6 WARN diagnostics across operational `readme.md` files (overwhelmingly `prompts/tooling-*/readme.md`). Author a sub-Task (or `tools/maintenance/partition-migrate.py`) that mechanically inserts `<!-- BEGIN DYNAMIC --> ... <!-- END DYNAMIC -->` markers with a "(none yet — first nightly run will populate)" stub for every non-conformant file. After the corpus is clean, promote M.B.6 from WARN to ERROR per the [Toolchain Flip SPEC §3.2](../../research/toolchain-flip-criteria/output/SPEC.md) WARN→ERROR ladder.
4. **Staleness-audit urgency tiers.** Amend MAINTENANCE.md §3.4 so the audit emits a distinct severity per age bucket: `freshly-stale` (age in `[STALE_DAYS, 2*STALE_DAYS]`), `stale` (`(2*STALE_DAYS, 4*STALE_DAYS]`), `long-stale` (> `4*STALE_DAYS`). Today the audit emits a single WARN tier regardless of age; the 2026-05-12 run found Tasks 008 and 066 at 8 days (just over the 7-day window) flagged identically to a hypothetical 60-day-old Task. Implementation in `tools/maintenance/staleness-audit.py`.
5. **Single-command maintenance-run verifier.** Author `tools/maintenance/run-coherence.sh` (or a `--mode=coherence-check` flag on `tools/check-governance.sh`) that runs the composed pipeline (fm/validate + staleness-audit + dynamic-readme-partition + check-duplicate-task-id + trust-audit AGGREGATOR) and emits one summary record suitable for direct append to `maintenance/run-log.md`. The 2026-05-12 run had to compose these manually — agents will skip steps without a single entry point.

## Todo

- [ ] 1. Spec-amend MAINTENANCE.md §2.3 to forbid the literal `pending` end_commit token in any record other than `HEAD`; ship `tools/maintenance/run-log-backfill.py` invoked at run-start (or pre-commit on `maintenance/run-log.md`) so the chicken-and-egg loop closes inside the next atomic commit.
- [ ] 2. Spec-amend MAINTENANCE.md §2.2 + `prompts/repo-coherence-check/prompt.md` Step 1 with delta-size threshold + routing decision.
- [ ] 3. Author migration tool that inserts BEGIN/END DYNAMIC markers across the 181 non-conformant readmes; raise M.B.6 from WARN to ERROR once corpus is clean.
- [ ] 4. Add `freshly-stale` / `stale` / `long-stale` severity tiers to `tools/maintenance/staleness-audit.py` and amend MAINTENANCE.md §3.4 decision-tree table.
- [ ] 5. Ship `tools/maintenance/run-coherence.sh` single-command verifier; cite it in MAINTENANCE.md §4 ("Finalising Any Run").
- [ ] 6. Add Gherkin acceptance anchor `M.B.8` (and follow-ups as needed) under MAINTENANCE.md §6 for the new contracts.
- [ ] 7. Verify `tools/check-governance.sh` exits 0 against the closing commit; append a `routine_type: task-implementation` record to `maintenance/run-log.md` with the actual end_commit (NOT `pending`).

## Links

- Found by: coherence check run `maintenance/run-log.md` entry 2026-05-12
- Governing specs: [`MAINTENANCE.md`](../../MAINTENANCE.md), [`TASK.md`](../../TASK.md), [`PROMPT.md`](../../PROMPT.md), [`FOLDERS.md`](../../FOLDERS.md)
- Adjacent prior Tasks: [Task 032](../032-improve-maintenance-spec-may-2026/task.md), [Task 044](../044-improve-maintenance-spec-may-07-2026/task.md), [Task 064](../064-improve-maintenance-spec-may-08-2026/task.md), [Task 068](../068-improve-maintenance-spec-may-2026/task.md), [Task 039](../039-maintenance-spec-integration/task.md)
- Reference tooling: [`tools/maintenance/staleness-audit.py`](../../tools/maintenance/staleness-audit.py), [`tools/maintenance/dynamic-readme-partition.py`](../../tools/maintenance/dynamic-readme-partition.py), [`tools/maintenance/trust-audit.py`](../../tools/maintenance/trust-audit.py)
