---
type: note
status: completed
slug: task-035-friction-log
summary: "FL1 — Task 035 closure friction log. Three linters + one research workspace + RESEARCH.md amendment landed cleanly; only friction was scope-discipline against the C3 partition (cross-workspace logic kept out of ST-4 in favour of Task 039 ST-5)."
created: 2026-05-07
updated: 2026-05-07
---

# Friction Log — Task 035 RESEARCH.md Spec Integration

Highest Frustration Level: FL1

## What was done in one session

- ST-2 `tools/check-workspace-cleanliness.py` (104 LOC) + 9 unit tests — passes against the live `/research/` tree.
- ST-3 `tools/check-external-result-downstream-task.py` (143 LOC) + 7 unit tests — surfaces the existing `/research/gemini/agency-adr-governance-spec/` legacy-unlinked case, kept as advisory.
- ST-4 `tools/check-trust-audit.py` (227 LOC) + 8 unit tests — exports `DIAGNOSTIC_SCHEMA` for the Task 039 ST-5 AGGREGATOR; multi-workspace invocation rejected per the C3 partition.
- ST-1 `research/session-continuity-protocol-instantiation/output/SPEC.md` — concrete `state.md` format (frontmatter + event-stream body + staleness-probe list), cadence rule (synthesis-step boundaries), resume protocol pseudocode, and the verbatim §4.10 amendment for ST-5 to lift.
- ST-5 RESEARCH.md amendments: §2.2 spec-chunking rule (50k token threshold), §4.10 pause-and-resume, §5.0 enforcement-mapping table refresh, §5.3 + §5.7 + §5.9 + §5.10 mechanical-enforcement language, R.4.3 prompt-snapshot lock-at-start disambiguation, six Gherkin scenarios under §5.11 covering R.B.1–R.B.6.
- All three linters wired into `tools/check-governance.sh` with strict-gate environment variables, mirroring the existing `FM_DUPLICATE_TASK_ID_STRICT` precedent.
- Linter table refreshed in `README.md §6`.

## Why FL1 (not FL0, not FL2)

- **Why not FL0**: there was a non-trivial scope-discipline beat. The `check-trust-audit.py` design briefly drifted toward including a "scan all workspaces" mode for convenience; the C3 partition in [`tasks/035-research-spec-integration/subtasks/readme.md`](./subtasks/readme.md) is explicit that cross-workspace aggregation belongs to Task 039 ST-5. I caught the drift before writing code, but it was a real moment of "is this really out of scope?" that warrants logging.
- **Why not FL2**: the plan from `task.md` Phase 1/2/3 survived intact. No re-plans. No subtasks were merged or split. No falsification clauses were triggered.

## Migration-window note

Three of the new linters intentionally run advisory (`FM_*_STRICT=0`) for one release window:

- `check-workspace-cleanliness.py` — existing closed workspaces may carry historical stragglers (none observed in the current scan, but the migration window is precautionary).
- `check-external-result-downstream-task.py` — `research/gemini/agency-adr-governance-spec/` reaches Task 027 only via body-text references, not via frontmatter back-link. A follow-up Task SHOULD repair the back-link by adding the result.md path to Task 027's `task_affects_paths` (Task 027 is `done`, so this is a T3 repair filed as a fresh Task per MAINTENANCE.md §1).
- `check-trust-audit.py` — many existing closed workspaces miss the synthesis-folder discipline (no `methodology.md`, no method files in `reflection/`) that the rubric requires. Strict-mode gating SHOULD wait until Task 039 ST-5 (AGGREGATOR) lands so the maintenance run can backfill.

## Followup Tasks suggested

- Repair the `research/gemini/agency-adr-governance-spec/` ↔ Task 027 frontmatter back-link.
- Author Task 039 ST-5 importing `DIAGNOSTIC_SCHEMA` from `tools/check-trust-audit.py`.
- Once both above land, flip `FM_EXTERNAL_RESULT_STRICT=1` and `FM_TRUST_AUDIT_STRICT=1` in `tools/check-governance.sh`.

## PR #88 review response (2026-05-07)

Reviewer: `claude/brave-darwin-byPwb`. Review file: [`review-pr88-claude-brave-darwin.md`](./review-pr88-claude-brave-darwin.md). Four findings; resolution in commit `fix(pr-88)`:

- **D1 (structural — was merge-blocker)** — Took Option B: lowered `DIAGNOSTIC_SCHEMA["thresholds"]["behavioral"]` from 0.90 to 0.80 in `tools/check-trust-audit.py`. Updates the corresponding sentence in RESEARCH.md §5.7 and the threshold-assertion test. The DIAGNOSTIC_SCHEMA carries an inline comment naming the migration-window: raise to 0.90 once Task 039 ST-5 (AGGREGATOR) lands AND `synthesis/methodology.md` is normatively required by RESEARCH.md §5.
- **D3 (advisory)** — Added a `# migration-window:` annotation above the R.B.2 Gherkin scenario in RESEARCH.md §5.11 noting that WARN→ERROR promotion is gated on the strict-mode flip.
- **D4 (advisory)** — Rephrased the R.B.5 `When`-clause from "stages a frontmatter edit setting `research_phase: complete`" to "any commit touches files under the workspace AND the workspace `readme.md` declares `research_phase: complete`" so the scenario matches the actual gate trigger in `tools/check-governance.sh`.
- **D2 (advisory)** — Provider-list DRY violation deferred to a Task 039 follow-up per the reviewer's recommendation. Not addressed on this branch.

The review session itself is FL0 friction (no re-plans); the closure FL stays at FL1.
