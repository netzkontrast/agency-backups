---
type: note
status: draft
slug: task-039-st5-tooling-trust-audit-integration
summary: "Subtask ST-5 (per spec-panel C3 = AGGREGATOR only): ship tools/maintenance/trust-audit.py — cross-research roll-up. Imports Task 035 ST-4's per-workspace GATE; rolls findings into nightly maintenance output for §3.2 friction aggregation."
created: 2026-05-06
updated: 2026-05-06
---

# ST-5: `trust-audit` AGGREGATOR (C3 Partition)

**Executor:** maintenance-agent

**Insertion point:** Not in `tools/check-governance.sh`; invoked by the nightly maintenance run.

## Goal

Ship `tools/maintenance/trust-audit.py` implementing the cross-research AGGREGATOR per the spec-panel C3 partition. Imports the per-workspace GATE module from Task 035 ST-4; iterates `/research/<slug>/` workspaces; rolls per-workspace findings into a single maintenance-run report for MAINTENANCE.md §3.2 friction-aggregation consumption. MUST NOT duplicate per-workspace logic.

## Falsification

Wrong cut **iff** ST-5 reimplements per-workspace gating (would violate the C3 partition). Mitigation: the implementation imports `tools.check_trust_audit.run_workspace_gate` and calls it; any per-workspace logic added directly here triggers a CI guard `tests/maintenance/test_aggregator_partition.py` that asserts no `def *workspace*(self...)` methods exist on the AGGREGATOR class.

## Inputs

- Task 035 ST-4 implementation: `tools/check-trust-audit.py` (must export `run_workspace_gate(workspace_path) -> List[Diagnostic]`).
- `research/agentic-eval-trust-improvement-spec/output/SPEC.md`.
- `MAINTENANCE.md` §3.2 (friction-aggregation contract).
- `tools/adr/runlog.py` (run-log persistence pattern).

## Acceptance Criteria

1. **Surface.** `python3 tools/maintenance/trust-audit.py [--threshold-mode=strict|advisory]`.
2. **Behaviour.** Imports `tools.check_trust_audit`; iterates research workspaces; emits aggregated diagnostics.
3. **Output.** Markdown report appended to `maintenance/run-log.md`; JSON via `--format json`.
4. **Tests.** `tests/maintenance/test_trust_audit_aggregator.py` covers: 0 workspaces, 3 clean, 1 failing, mixed; partition guard.
5. **Integration.** Invoked by nightly run; cross-references Task 035 ST-4.

## Dependencies

Task 035 ST-4 MUST land first.

## Estimated Effort

Medium (~120 LOC + 100 LOC tests; the partition-guard test is the bulk).
