---
type: prompt
status: active
slug: tooling-trust-audit-gate
summary: "Ship `tools/check-trust-audit.py` implementing the per-workspace trust-audit gate from `research/agentic-eval-trust-improvement-spec/output/SPEC.md`. Three thresholds: schema-conformance ≥80%, behavioral ≥90%, governance ≥95%. Owns the d..."
created: 2026-05-06
updated: 2026-05-06
prompt_kind: task-spec
prompt_framework: RISEN+ReAct
prompt_target_agent: "Claude Code"
prompt_relates_to_task: research-spec-integration
---

# ST-4: `check-trust-audit` — Per-Workspace GATE (C3 Partition) — Task-Spec Prompt

## Framework

RISEN+ReAct. The prompt declares the framework in frontmatter (`prompt_framework: RISEN+ReAct`) and restates it here for `fm-validate` header conformance. The R/I/S/E sections below carry the canonical roles; a final **Constraints** section groups normative scope/failure rules per repo convention.

## R — Role

You are the **main-agent** dispatched to execute subtask ST-4 of [Task research-spec-integration](../../tasks/035-research-spec-integration/task.md). Your remit is bounded by the Acceptance Criteria in [`brief.md`](./brief.md); you MUST NOT expand scope beyond those criteria without surfacing the divergence in `friction-log.md`.

**Parallelism:** Phase A (parallel) — runs concurrently with ST-1, ST-2, ST-3. No inter-dependencies. **C3 partition: GATE only**; Task 039 ST-5 (AGGREGATOR) imports this module's diagnostic schema and MUST be authored after ST-4 here..

## I — Input

- `research/agentic-eval-trust-improvement-spec/output/SPEC.md` (three-tier rubric).
- `tools/adr/runlog.py` (diagnostic format prior art — `<relpath>::<TIER>:<code>:<message>`).
- `tools/fm/extract.py` (workspace artefact iteration).
- `tasks/035-research-spec-integration/task.md` — parent task chain-level context.

## S — Steps

1. The agent MUST produce the artefact required by acceptance criterion: **Surface.** `python3 tools/check-trust-audit.py <workspace-path>` exits 0 / 1.
2. The agent MUST produce the artefact required by acceptance criterion: **Thresholds.** Three checks per the SPEC; per-check diagnostic on miss.
3. The agent MUST produce the artefact required by acceptance criterion: **Diagnostic format.** `<relpath>::ERROR:TRUST.<code>:<message>` (TRUST namespace; matches the `ADR.A.*` shape so MAINTENANCE.md aggregation can ingest both via one parser).
4. The agent MUST produce the artefact required by acceptance criterion: **Tests.** `tests/test_trust_audit.py` covers: passing workspace, schema-fail, behavioral-fail, governance-fail.
5. The agent MUST produce the artefact required by acceptance criterion: **Schema export.** Module exports a `DIAGNOSTIC_SCHEMA` constant Task 039 ST-5 imports.
6. The agent MUST produce the artefact required by acceptance criterion: **Single-workspace constraint.** Multi-workspace invocations exit 1 with diagnostic `TRUST.PARTITION:single-workspace-only`.
7. The agent MUST verify every Acceptance Criterion enumerated in [`brief.md`](./brief.md) holds against the produced artefacts; on any failure the agent MUST iterate the relevant implementation step rather than weakening the criterion.
8. The agent MUST run `tools/check-governance.sh` and resolve every ERROR before committing; a non-zero exit MUST block the commit.
9. The agent SHOULD author or update `tasks/035-research-spec-integration/friction-log.md` per FRUSTRATED.md FL[0-3] when frictions arise; absence of frictions MAY be recorded as `FL: 0`.
10. The agent MUST commit with a message that names `Task 035 ST-4` in its trailer; the agent MUST NOT push (the maintainer pushes after review).

## E — Expectations

- **Surface.** `python3 tools/check-trust-audit.py <workspace-path>` exits 0 / 1.
- **Thresholds.** Three checks per the SPEC; per-check diagnostic on miss.
- **Diagnostic format.** `<relpath>::ERROR:TRUST.<code>:<message>` (TRUST namespace; matches the `ADR.A.*` shape so MAINTENANCE.md aggregation can ingest both via one parser).
- **Tests.** `tests/test_trust_audit.py` covers: passing workspace, schema-fail, behavioral-fail, governance-fail.
- **Schema export.** Module exports a `DIAGNOSTIC_SCHEMA` constant Task 039 ST-5 imports.
- **Single-workspace constraint.** Multi-workspace invocations exit 1 with diagnostic `TRUST.PARTITION:single-workspace-only`.
- `tools/check-governance.sh` exits 0 on the produced commit.
- Commit message follows the parent task's convention; the commit cites `Task 035 ST-4` in its trailer.

## Constraints

- Dependency: None. Phase A. Task 039 ST-5 (AGGREGATOR) MUST be authored after ST-4 to import this module's schema.
- MUST NOT trigger the subtask's Falsification clause: Wrong cut **iff** ST-4 includes cross-workspace logic — that belongs in Task 039 ST-5 per the spec-panel C3 partition. Mitigation: ST-4's CLI accepts exactly one workspace argument; rejects multi-workspace invocations.
- MUST NOT inline this prompt's Goal/Inputs/Acceptance back into the subtask file — the subtask body is now a thin pointer per Task 041.
- MUST run `tools/check-governance.sh` before pushing; a non-zero exit MUST block the push.
- SHOULD cite the parent task's `task_id` in any commit-message trailer for traceability.
