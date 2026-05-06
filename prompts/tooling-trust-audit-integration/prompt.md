---
type: prompt
status: active
slug: tooling-trust-audit-integration
summary: "Ship `tools/maintenance/trust-audit.py` implementing the cross-research AGGREGATOR per the spec-panel C3 partition. Imports the per-workspace GATE module from Task 035 ST-4; iterates `/research/<slug>/` workspaces; rolls per-workspace fi..."
created: 2026-05-06
updated: 2026-05-06
prompt_kind: task-spec
prompt_framework: RISEN+ReAct
prompt_target_agent: "Claude Code"
prompt_relates_to_task: maintenance-spec-integration
---

# ST-5: `trust-audit` AGGREGATOR (C3 Partition) — Task-Spec Prompt

## Framework

RISEN+ReAct. The prompt declares the framework in frontmatter (`prompt_framework: RISEN+ReAct`) and restates it here for `fm-validate` header conformance. The R/I/S/E sections below carry the canonical roles; a final **Constraints** section groups normative scope/failure rules per repo convention.

## R — Role

You are the **maintenance-agent** dispatched to execute subtask ST-5 of [Task maintenance-spec-integration](../../tasks/039-maintenance-spec-integration/task.md). Your remit is bounded by the Acceptance Criteria in [`brief.md`](./brief.md); you MUST NOT expand scope beyond those criteria without surfacing the divergence in `friction-log.md`.

**Parallelism:** Phase A (parallel-grouped, hard-blocked) — runs alongside ST-1/ST-3/ST-4 but hard-depends on Task 035 ST-4 (GATE) which exports the DIAGNOSTIC_SCHEMA this AGGREGATOR imports. **C3 partition: AGGREGATOR only**; never duplicates per-workspace logic..

## I — Input

- Task 035 ST-4 implementation: `tools/check-trust-audit.py` (must export `run_workspace_gate(workspace_path) -> List[Diagnostic]`).
- `research/agentic-eval-trust-improvement-spec/output/SPEC.md`.
- `MAINTENANCE.md` §3.2 (friction-aggregation contract).
- `tools/adr/runlog.py` (run-log persistence pattern).
- `tasks/039-maintenance-spec-integration/task.md` — parent task chain-level context.

## S — Steps

1. The agent MUST produce the artefact required by acceptance criterion: **Surface.** `python3 tools/maintenance/trust-audit.py [--threshold-mode=strict|advisory]`.
2. The agent MUST produce the artefact required by acceptance criterion: **Behaviour.** Imports `tools.check_trust_audit`; iterates research workspaces; emits aggregated diagnostics.
3. The agent MUST produce the artefact required by acceptance criterion: **Output.** Markdown report appended to `maintenance/run-log.md`; JSON via `--format json`.
4. The agent MUST produce the artefact required by acceptance criterion: **Tests.** `tests/maintenance/test_trust_audit_aggregator.py` covers: 0 workspaces, 3 clean, 1 failing, mixed; partition guard.
5. The agent MUST produce the artefact required by acceptance criterion: **Integration.** Invoked by nightly run; cross-references Task 035 ST-4.
6. The agent MUST verify every Acceptance Criterion enumerated in [`brief.md`](./brief.md) holds against the produced artefacts; on any failure the agent MUST iterate the relevant implementation step rather than weakening the criterion.
7. The agent MUST run `tools/check-governance.sh` and resolve every ERROR before committing; a non-zero exit MUST block the commit.
8. The agent SHOULD author or update `tasks/039-maintenance-spec-integration/friction-log.md` per FRUSTRATED.md FL[0-3] when frictions arise; absence of frictions MAY be recorded as `FL: 0`.
9. The agent MUST commit with a message that names `Task 039 ST-5` in its trailer; the agent MUST NOT push (the maintainer pushes after review).

## E — Expectations

- **Surface.** `python3 tools/maintenance/trust-audit.py [--threshold-mode=strict|advisory]`.
- **Behaviour.** Imports `tools.check_trust_audit`; iterates research workspaces; emits aggregated diagnostics.
- **Output.** Markdown report appended to `maintenance/run-log.md`; JSON via `--format json`.
- **Tests.** `tests/maintenance/test_trust_audit_aggregator.py` covers: 0 workspaces, 3 clean, 1 failing, mixed; partition guard.
- **Integration.** Invoked by nightly run; cross-references Task 035 ST-4.
- `tools/check-governance.sh` exits 0 on the produced commit.
- Commit message follows the parent task's convention; the commit cites `Task 039 ST-5` in its trailer.

## Constraints

- Dependency: Task 035 ST-4 MUST land first.
- MUST NOT trigger the subtask's Falsification clause: Wrong cut **iff** ST-5 reimplements per-workspace gating (would violate the C3 partition). Mitigation: the implementation imports `tools.check_trust_audit.run_workspace_gate` and calls it; any per-workspace logic added directly here triggers a CI guard `tests/maintenance/test_aggregator_partition.py` that asserts no `def *workspace*(self...)` methods exist on the AGGREGATOR class.
- MUST NOT inline this prompt's Goal/Inputs/Acceptance back into the subtask file — the subtask body is now a thin pointer per Task 041.
- MUST run `tools/check-governance.sh` before pushing; a non-zero exit MUST block the push.
- SHOULD cite the parent task's `task_id` in any commit-message trailer for traceability.
