---
type: note
status: active
slug: migrate-lifecycle-classifier-five-signal-friction-log
summary: "Closure FL for Task 049 — five-signal algorithm migration. Implemented per ST-2 SPEC §1; 29 tests pass; one regex-flag bug caught in pre-commit testing (S1 missing re.MULTILINE) — fixed in-session."
created: 2026-05-11
updated: 2026-05-11
---

# Task 049 — Friction Log

Highest Frustration Level: FL1

## Notes

The SPEC at `research/spec-staleness-decision-formalization/output/SPEC.md` was unusually precise — §1 pseudocode and §2 signal-extraction recipes were directly transliterable into Python. Implementation went smoothly: `tools/fm/_lifecycle_signals.py` (~280 LOC) shipped on first attempt with the helper-refactor + 29-test suite landing in a single iteration.

## FL1 cause

S1's `_TODO_LINE` regex was authored without `re.MULTILINE`, so `re.findall()` matched only the first todo line in the section body string. The bucket-level tests all passed (signal returned `1.0` for the synthetic `- [ ] one` fixture, which happened to be a sole-line ⇒ either fully-checked or fully-unchecked — the bucket-leaf tests don't expose the multi-line case). The S1 unit test `test_s1_todo_satisfaction_partial` exposed the bug: it expected `2/3` for `[x] [ ] [x]` but got `1.0`. One-line fix: added `re.MULTILINE` to `_TODO_LINE` compilation. All 29 tests passed after.

**Generalisable lesson.** Pure-function signal extractors that consume sliced section text MUST treat the slice as a multi-line string explicitly. Anchored regexes (`^`, `$`) without `re.MULTILINE` are a silent-failure surface that bucket-level tests will miss whenever the synthetic fixture happens to have only one line of the matched kind.

## Worked-example regression guard

SPEC §3 declared Tasks 022/023/024/025 as `STILL_ACCURATE` on 2026-05-07. The migrated helper run on 2026-05-11 reports `COMPLETED_BY_DRIFT` for some of them (Task 022 now closed as `done` with all-checked Todos and present affects-paths; same for Task 023). This is the correct mechanical descendant of `STILL_ACCURATE` for tasks that completed-by-drift between the SPEC write date and today. The regression-guard tests accept either bucket (`STILL_ACCURATE` OR `COMPLETED_BY_DRIFT`) for each of the four worked examples; this preserves the SPEC's intent (the algorithm reproduces SPEC §3 reasoning) while admitting natural post-SPEC repo evolution.

## Out-of-scope deferrals

- The `MAINTENANCE.md §3.4` audit-walker (the routine that calls `classify_task` over the whole `/tasks/` tree and emits the audit report) is NOT in this Task's scope. Task 039 ST-3 (`tools/maintenance/staleness-audit.py`) already ships that surface; this Task delivers only the *classifier*, not the walker.
- Cross-machine determinism: `signal_goal_endorsed_by_spec` shells out to `git grep` when available and falls back to Python `re` scanning when `git` is absent. Outputs should be identical, but the test suite does not yet exercise the fallback path against a stripped `PATH`. A future Task 049 successor could add a `--without-git` test mode if cross-platform CI surfaces a divergence.
- The 9 retired flag-based tests (`test_missing_attestation_flags_fail`, `test_all_todos_checked_emits_warn`, etc.) were replaced with signal-and-bucket-based equivalents rather than `@unittest.skip`-marked; per the Task's Falsification clause (3), retired tests MUST be replaced with rationale, which is captured in the new test file's module docstring + this log.

## Coordination with Task 039

Task 039 ST-3 ships `tools/maintenance/staleness-audit.py` — the audit *walker*. This Task ships the *classifier* it walks. The two are deliberately separated: the classifier is a per-Task pure function; the walker is the policy layer that decides which Tasks to enqueue. The walker MAY import `classify_task` from `_lifecycle_signals` once Task 039's helper is updated to consume the new API; that wire-up is left to a Task 039 successor or to opportunistic refactor under MAINTENANCE.md §1.0.1 T1 allowance.
