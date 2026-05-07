---
type: task
status: active
slug: migrate-lifecycle-classifier-five-signal
summary: "Migrate `tools/fm/check-task-lifecycle-classification.py` from the four-condition fallback derived from TASK.md §4.7 prose onto the ratified five-signal `classify_task` decision tree from `research/spec-staleness-decision-formalization/output/SPEC.md §1` (Task 033 ST-2 / Task 039 ST-2)."
created: 2026-05-07
updated: 2026-05-07
task_id: "049"
task_status: open
task_owner: "unassigned"
task_priority: P3
task_uses_prompts: []
task_spawns_research: []
task_spawns_prompts: []
task_affects_paths:
  - tools/fm/check-task-lifecycle-classification.py
  - tools/tests/fm/test_lifecycle_classification.py
  - tools/fm/readme.md
  - TASK.md
---

# Task 049 — Migrate Lifecycle Classifier to Five-Signal Algorithm

## Goal

Replace the four-condition fallback in `tools/fm/check-task-lifecycle-classification.py` (Task 033 ST-4) with the ratified five-signal `classify_task` decision tree from [`research/spec-staleness-decision-formalization/output/SPEC.md §1`](../../research/spec-staleness-decision-formalization/output/SPEC.md). The ST-2 SPEC defines a deterministic algorithm (3 levels, 4 leaves, 16 LOC pseudocode) consuming five git-extractable signals — `todo_satisfaction`, `affects_paths_present`, `plan_anchors_live`, `goal_endorsed`, `successor_present` — and emits exactly one of four §4.7 buckets without agent attestation. The current four-condition fallback requires two CLI-attestation flags (`--goal-still-desirable`, `--plan-drifted`) which the SPEC mechanises into signals.

The Task is `done` when:

1. The helper consumes ST-2 SPEC §1's `classify_task` algorithm directly (function signature: `classify_task(task, repo, today, stale_days) -> Bucket`).
2. The five signals defined in ST-2 SPEC §2 each have a Python implementation under `tools/fm/_lifecycle_signals.py` (or in-module equivalents); each signal is a pure function of repo state with no LLM judgement.
3. The `--goal-still-desirable` and `--plan-drifted` CLI flags are removed from the helper's surface (the signals replace them).
4. New tests in `tools/tests/fm/test_lifecycle_classification.py` cover the four worked-example walkthroughs from ST-2 SPEC §3 (Tasks 022 / 023 / 024 / 025 currently classify as `STILL_ACCURATE` per the SPEC — the migrated helper MUST produce identical bucket assignments on the live repo).
5. TASK.md §4.7 helper-paragraph + the helper docstring are updated to reflect the migration (drop the "four-condition fallback" language; describe the five-signal algorithm with a one-line example).
6. `tools/fm/readme.md` row for `check-task-lifecycle-classification` is updated.
7. `tools/check-governance.sh` exits 0 (or remaining ERRORs are documented out-of-scope per the Task 032 / Task 033 friction-log precedent).

## Context

The Task 033 ST-4 helper was implemented before ST-2 SPEC ratified — the four-condition fallback was derived directly from TASK.md §4.7 prose. Two days later (2026-05-07) ST-2 SPEC landed (commit `de03603`) with a more principled five-signal algorithm. PR #81 review M-3 escalated the migration from a docstring TODO to a filed Task per AGENTS.md AG.2.1.

## Preconditions

- **Task 033** — ST-4 helper + ST-2 SPEC are both in-tree.
- **Task 016 / 017** — flexible-frontmatter toolchain shipped + repo migrated.
- **`tools/fm/_core.py`** — frontmatter parser + path classification utilities (the signals consume these).

## Plan

1. Read [`research/spec-staleness-decision-formalization/output/SPEC.md`](../../research/spec-staleness-decision-formalization/output/SPEC.md) §1 (algorithm) + §2 (signals) + §3 (worked examples) + §6 (ST-4 implementation notes).
2. Implement the five signals as pure-function helpers (one Python function each); each function MUST match the one-line extraction recipe in SPEC §2.
3. Implement `classify_task(task, repo, today, stale_days)` per SPEC §1 pseudocode.
4. Replace the four-condition fallback in `tools/fm/check-task-lifecycle-classification.py` with `classify_task`. Drop the two attestation flags. Preserve the `--task <path> --target-status {updated,abandoned}` surface.
5. Add tests for: (a) each signal in isolation, (b) each leaf bucket, (c) the four worked-example walkthroughs from SPEC §3 against the live repo (regression guard).
6. Update TASK.md §4.7 helper-paragraph + the helper docstring + `tools/fm/readme.md` row.
7. Run `tools/check-governance.sh`; resolve every newly-introduced ERROR.
8. Author `friction-log.md` (FL[0-3]); update `tasks/readme.md` with the closure bullet; flip `task_status: done`; commit; push.

## Falsification

Wrong cut **iff**:

1. The migrated helper produces different bucket assignments for Tasks 022/023/024/025 than ST-2 SPEC §3 declares (signals would be implemented incorrectly).
2. The five-signal implementation requires LLM judgement at any point (SPEC §1 explicitly forbids this — every signal is a pure function of git/filesystem state).
3. The migration breaks any existing test in `tools/tests/fm/test_lifecycle_classification.py` without that test being explicitly retired (e.g. tests asserting the attestation-flag surface MUST be retired with rationale, not silently broken).

## Todo

- [ ] 1. Read ST-2 SPEC §1, §2, §3, §6.
- [ ] 2. Implement the five signals as pure functions.
- [ ] 3. Implement `classify_task()` per SPEC §1 pseudocode.
- [ ] 4. Migrate the helper; drop the two attestation flags.
- [ ] 5. Add tests for signals, buckets, and the four worked examples.
- [ ] 6. Update TASK.md §4.7 + helper docstring + `tools/fm/readme.md`.
- [ ] 7. Run `tools/check-governance.sh`; fix every ERROR.
- [ ] 8. Update `tasks/readme.md` with the closure bullet.
- [ ] 9. Author `friction-log.md` with FL[0-3] declaration.
- [ ] 10. Set `task_status: done`.

## Links

- Algorithm SPEC: [`research/spec-staleness-decision-formalization/output/SPEC.md`](../../research/spec-staleness-decision-formalization/output/SPEC.md) §1, §2, §3, §6.
- Current helper: [`tools/fm/check-task-lifecycle-classification.py`](../../tools/fm/check-task-lifecycle-classification.py) — four-condition fallback to be replaced.
- Existing tests: [`tools/tests/fm/test_lifecycle_classification.py`](../../tools/tests/fm/test_lifecycle_classification.py) — 9 tests; some MAY need retirement.
- Filing rationale: [PR #81 review M-3](../../maintenance/pr-81-review.md).
- Predecessor: [Task 033 ST-4](../033-task-spec-integration/subtasks/04-tooling-lifecycle-classifier.md).
- Sibling SPEC consumer: [Task 039 maintenance-spec-integration](../039-maintenance-spec-integration/) — also consumes ST-2 SPEC; coordinate to avoid duplicate work if Task 039 ST-3 is the natural home for this migration.
- Governing specs: [`TASK.md`](../../TASK.md) §4.7, [`MAINTENANCE.md`](../../MAINTENANCE.md) §3.4.
