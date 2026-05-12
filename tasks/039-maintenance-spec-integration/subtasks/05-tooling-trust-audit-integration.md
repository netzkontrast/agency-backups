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

**Parallelism:** Phase A (parallel-grouped, hard-blocked) — runs alongside ST-1/ST-3/ST-4 but hard-depends on Task 035 ST-4 (GATE) which exports the DIAGNOSTIC_SCHEMA this AGGREGATOR imports. **C3 partition: AGGREGATOR only**; never duplicates per-workspace logic.

**Prompt:** [`/prompts/tooling-trust-audit-integration/prompt.md`](../../../prompts/tooling-trust-audit-integration/prompt.md) — the executable instruction set for this subtask. The Goal, Falsification, Inputs, Acceptance Criteria, Dependencies, and Estimated Effort sections that previously lived inline have moved to that prompt's [`brief.md`](../../../prompts/tooling-trust-audit-integration/brief.md) per Task 041 (PR #70 review C.3 audit-graph repair).
