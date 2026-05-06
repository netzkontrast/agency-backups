---
type: note
status: active
slug: tooling-staleness-audit-script-brief
summary: "Brief for prompt tooling-staleness-audit-script — extracted from tasks/039-maintenance-spec-integration/subtasks/03-tooling-staleness-audit-script.md per Task 041 (PR #70 review C.3 audit-graph repair)."
created: 2026-05-06
updated: 2026-05-06
---

# Brief — ST-3: `staleness-audit` — MAINTENANCE.md §3.4 Mechanization

## Raw User Request

> Extract the inlined Execution Brief from `tasks/039-maintenance-spec-integration/subtasks/03-tooling-staleness-audit-script.md` (ST-3) into a registered `/prompts/<slug>/` artefact, restoring the `task_uses_prompts ↔ prompt_relates_to_task` audit-graph edge severed in PR #70 (review finding C.3).

## Target Audience

The dispatched executor for [Task 039 `maintenance-spec-integration`](../../tasks/039-maintenance-spec-integration/task.md), specifically subtask ST-3 (03-tooling-staleness-audit-script.md). Default executor: **maintenance-agent**.

## Intended Model / Agent

Claude Code (or any agent that satisfies the executor declaration in the parent subtask file).

## Use-Case Context

This prompt drives subtask ST-3 of [Task maintenance-spec-integration](../../tasks/039-maintenance-spec-integration/task.md). The parent task's chain-level rationale lives in its `task.md`; this brief records only the subtask's local goal + inputs + acceptance + dependencies + effort, lifted verbatim from the subtask file at extraction time.

**Parallelism:** Phase A (parallel-grouped, soft-blocked) — runs alongside ST-1/ST-4/ST-5 but soft-depends on ST-2 SPEC. May ship with stub algorithm + upgrade post-ST-2.

**Insertion point:** Not in `tools/check-governance.sh`; invoked by the nightly maintenance run only.

## Goal (from subtask)

Ship `tools/maintenance/staleness-audit.py` that, given the active task corpus, assigns each open task to one of {still-accurate, drifted, completed-by-drift, no-longer-desirable} per the deterministic algorithm in ST-2's SPEC. Configurable via `MAINT_STALE_DAYS` (default 7).

## Falsification (from subtask)

Wrong cut **iff** the algorithm's signal-extractor recipes (from ST-2 SPEC §2) cannot be implemented in stdlib + git. Mitigation: ST-2's "≤5 signals; mechanically extractable" constraint is verified during ST-2 authoring.

## Inputs (from subtask)

- ST-2 output: `research/spec-staleness-decision-formalization/output/SPEC.md` §1 algorithm + §2 signals.
- `tools/fm/_core.py`, `tools/fm/query.py`.
- `tools/adr/graph.py` (cycle detection prior art for blocker chains).
- All `tasks/*/task.md` (test corpus).

## Acceptance Criteria (from subtask)

1. **Surface.** `python3 tools/maintenance/staleness-audit.py [--stale-days N]`.
2. **Algorithm.** Implements ST-2 SPEC §1 decision tree.
3. **Output.** Table of (task_id, current_status, bucket, evidence) — markdown for human; JSON via `--format json` for tooling.
4. **Tests.** `tests/maintenance/test_staleness_audit.py` covers each bucket using ST-2 SPEC §3 walkthroughs as fixtures.
5. **Integration.** Invoked by the nightly run; output appended to `maintenance/run-log.md`.

## Dependencies (from subtask)

ST-2 (research) MUST land first.

## Estimated Effort (from subtask)

Medium (~150 LOC + 100 LOC tests).
