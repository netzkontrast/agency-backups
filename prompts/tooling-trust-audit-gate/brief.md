---
type: brief
status: active
slug: tooling-trust-audit-gate-brief
summary: "Brief for prompt tooling-trust-audit-gate — extracted from tasks/035-research-spec-integration/subtasks/04-tooling-trust-audit-gate.md per Task 041 (PR #70 review C.3 audit-graph repair)."
created: 2026-05-06
updated: 2026-05-06
---

# Brief — ST-4: `check-trust-audit` — Per-Workspace GATE (C3 Partition)

## Raw User Request

> Extract the inlined Execution Brief from `tasks/035-research-spec-integration/subtasks/04-tooling-trust-audit-gate.md` (ST-4) into a registered `/prompts/<slug>/` artefact, restoring the `task_uses_prompts ↔ prompt_relates_to_task` audit-graph edge severed in PR #70 (review finding C.3).

## Target Audience

The dispatched executor for [Task 035 `research-spec-integration`](../../tasks/035-research-spec-integration/task.md), specifically subtask ST-4 (04-tooling-trust-audit-gate.md). Default executor: **main-agent**.

## Intended Model / Agent

Claude Code (or any agent that satisfies the executor declaration in the parent subtask file).

## Use-Case Context

This prompt drives subtask ST-4 of [Task research-spec-integration](../../tasks/035-research-spec-integration/task.md). The parent task's chain-level rationale lives in its `task.md`; this brief records only the subtask's local goal + inputs + acceptance + dependencies + effort, lifted verbatim from the subtask file at extraction time.

**Parallelism:** Phase A (parallel) — runs concurrently with ST-1, ST-2, ST-3. No inter-dependencies. **C3 partition: GATE only**; Task 039 ST-5 (AGGREGATOR) imports this module's diagnostic schema and MUST be authored after ST-4 here.

**Insertion point:** `[opt]` WARN-tier; promoted to ERROR-tier when target workspace is transitioning to `research_phase: complete`.

## Goal (from subtask)

Ship `tools/check-trust-audit.py` implementing the per-workspace trust-audit gate from `research/agentic-eval-trust-improvement-spec/output/SPEC.md`. Three thresholds: schema-conformance ≥80%, behavioral ≥90%, governance ≥95%. Owns the diagnostic-format contract that Task 039 ST-5 (AGGREGATOR) imports.

## Falsification (from subtask)

Wrong cut **iff** ST-4 includes cross-workspace logic — that belongs in Task 039 ST-5 per the spec-panel C3 partition. Mitigation: ST-4's CLI accepts exactly one workspace argument; rejects multi-workspace invocations.

## Inputs (from subtask)

- `research/agentic-eval-trust-improvement-spec/output/SPEC.md` (three-tier rubric).
- `tools/adr/runlog.py` (diagnostic format prior art — `<relpath>::<TIER>:<code>:<message>`).
- `tools/fm/extract.py` (workspace artefact iteration).

## Acceptance Criteria (from subtask)

1. **Surface.** `python3 tools/check-trust-audit.py <workspace-path>` exits 0 / 1.
2. **Thresholds.** Three checks per the SPEC; per-check diagnostic on miss.
3. **Diagnostic format.** `<relpath>::ERROR:TRUST.<code>:<message>` (TRUST namespace; matches the `ADR.A.*` shape so MAINTENANCE.md aggregation can ingest both via one parser).
4. **Tests.** `tests/test_trust_audit.py` covers: passing workspace, schema-fail, behavioral-fail, governance-fail.
5. **Schema export.** Module exports a `DIAGNOSTIC_SCHEMA` constant Task 039 ST-5 imports.
6. **Single-workspace constraint.** Multi-workspace invocations exit 1 with diagnostic `TRUST.PARTITION:single-workspace-only`.

## Dependencies (from subtask)

None. Phase A. Task 039 ST-5 (AGGREGATOR) MUST be authored after ST-4 to import this module's schema.

## Estimated Effort (from subtask)

Medium (~150 LOC + 120 LOC tests).
