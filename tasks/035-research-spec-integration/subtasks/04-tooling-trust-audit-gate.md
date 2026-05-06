---
type: note
status: draft
slug: task-035-st4-tooling-trust-audit-gate
summary: "Subtask ST-4 (per spec-panel C3 = GATE only): ship tools/check-trust-audit.py — per-workspace trust-audit linter invoked at research_phase: complete transition. Diagnostic-format owner; AGGREGATOR is Task 039 ST-5."
created: 2026-05-06
updated: 2026-05-06
---

# ST-4: `check-trust-audit` — Per-Workspace GATE (C3 Partition)

**Executor:** main-agent

**Insertion point:** `[opt]` WARN-tier; promoted to ERROR-tier when target workspace is transitioning to `research_phase: complete`.

## Goal

Ship `tools/check-trust-audit.py` implementing the per-workspace trust-audit gate from `research/agentic-eval-trust-improvement-spec/output/SPEC.md`. Three thresholds: schema-conformance ≥80%, behavioral ≥90%, governance ≥95%. Owns the diagnostic-format contract that Task 039 ST-5 (AGGREGATOR) imports.

## Falsification

Wrong cut **iff** ST-4 includes cross-workspace logic — that belongs in Task 039 ST-5 per the spec-panel C3 partition. Mitigation: ST-4's CLI accepts exactly one workspace argument; rejects multi-workspace invocations.

## Inputs

- `research/agentic-eval-trust-improvement-spec/output/SPEC.md` (three-tier rubric).
- `tools/adr/runlog.py` (diagnostic format prior art — `<relpath>::<TIER>:<code>:<message>`).
- `tools/fm/extract.py` (workspace artefact iteration).

## Acceptance Criteria

1. **Surface.** `python3 tools/check-trust-audit.py <workspace-path>` exits 0 / 1.
2. **Thresholds.** Three checks per the SPEC; per-check diagnostic on miss.
3. **Diagnostic format.** `<relpath>::ERROR:TRUST.<code>:<message>` (TRUST namespace; matches the `ADR.A.*` shape so MAINTENANCE.md aggregation can ingest both via one parser).
4. **Tests.** `tests/test_trust_audit.py` covers: passing workspace, schema-fail, behavioral-fail, governance-fail.
5. **Schema export.** Module exports a `DIAGNOSTIC_SCHEMA` constant Task 039 ST-5 imports.
6. **Single-workspace constraint.** Multi-workspace invocations exit 1 with diagnostic `TRUST.PARTITION:single-workspace-only`.

## Dependencies

None. Phase A. Task 039 ST-5 (AGGREGATOR) MUST be authored after ST-4 to import this module's schema.

## Estimated Effort

Medium (~150 LOC + 120 LOC tests).
