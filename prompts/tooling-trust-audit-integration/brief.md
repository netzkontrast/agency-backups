---
type: note
status: active
slug: tooling-trust-audit-integration-brief
summary: "Brief for prompt tooling-trust-audit-integration — extracted from tasks/039-maintenance-spec-integration/subtasks/05-tooling-trust-audit-integration.md per Task 041 (PR #70 review C.3 audit-graph repair)."
created: 2026-05-06
updated: 2026-05-06
---

# Brief — ST-5: `trust-audit` AGGREGATOR (C3 Partition)

## Raw User Request

> Extract the inlined Execution Brief from `tasks/039-maintenance-spec-integration/subtasks/05-tooling-trust-audit-integration.md` (ST-5) into a registered `/prompts/<slug>/` artefact, restoring the `task_uses_prompts ↔ prompt_relates_to_task` audit-graph edge severed in PR #70 (review finding C.3).

## Target Audience

The dispatched executor for [Task 039 `maintenance-spec-integration`](../../tasks/039-maintenance-spec-integration/task.md), specifically subtask ST-5 (05-tooling-trust-audit-integration.md). Default executor: **maintenance-agent**.

## Intended Model / Agent

Claude Code (or any agent that satisfies the executor declaration in the parent subtask file).

## Use-Case Context

This prompt drives subtask ST-5 of [Task maintenance-spec-integration](../../tasks/039-maintenance-spec-integration/task.md). The parent task's chain-level rationale lives in its `task.md`; this brief records only the subtask's local goal + inputs + acceptance + dependencies + effort, lifted verbatim from the subtask file at extraction time.

**Parallelism:** Phase A (parallel-grouped, hard-blocked) — runs alongside ST-1/ST-3/ST-4 but hard-depends on Task 035 ST-4 (GATE) which exports the DIAGNOSTIC_SCHEMA this AGGREGATOR imports. **C3 partition: AGGREGATOR only**; never duplicates per-workspace logic.

**Insertion point:** Not in `tools/check-governance.sh`; invoked by the nightly maintenance run.

## Goal (from subtask)

Ship `tools/maintenance/trust-audit.py` implementing the cross-research AGGREGATOR per the spec-panel C3 partition. Imports the per-workspace GATE module from Task 035 ST-4; iterates `/research/<slug>/` workspaces; rolls per-workspace findings into a single maintenance-run report for MAINTENANCE.md §3.2 friction-aggregation consumption. MUST NOT duplicate per-workspace logic.

## Falsification (from subtask)

Wrong cut **iff** ST-5 reimplements per-workspace gating (would violate the C3 partition). Mitigation: the implementation imports `tools.check_trust_audit.run_workspace_gate` and calls it; any per-workspace logic added directly here triggers a CI guard `tests/maintenance/test_aggregator_partition.py` that asserts no `def *workspace*(self...)` methods exist on the AGGREGATOR class.

## Inputs (from subtask)

- Task 035 ST-4 implementation: `tools/check-trust-audit.py` (must export `run_workspace_gate(workspace_path) -> List[Diagnostic]`).
- `research/agentic-eval-trust-improvement-spec/output/SPEC.md`.
- `MAINTENANCE.md` §3.2 (friction-aggregation contract).
- `tools/adr/runlog.py` (run-log persistence pattern).

## Acceptance Criteria (from subtask)

1. **Surface.** `python3 tools/maintenance/trust-audit.py [--threshold-mode=strict|advisory]`.
2. **Behaviour.** Imports `tools.check_trust_audit`; iterates research workspaces; emits aggregated diagnostics.
3. **Output.** Markdown report appended to `maintenance/run-log.md`; JSON via `--format json`.
4. **Tests.** `tests/maintenance/test_trust_audit_aggregator.py` covers: 0 workspaces, 3 clean, 1 failing, mixed; partition guard.
5. **Integration.** Invoked by nightly run; cross-references Task 035 ST-4.

## Dependencies (from subtask)

Task 035 ST-4 MUST land first.

## Estimated Effort (from subtask)

Medium (~120 LOC + 100 LOC tests; the partition-guard test is the bulk).
