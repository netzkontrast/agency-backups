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

**Parallelism:** Phase A (parallel) — runs concurrently with ST-1, ST-2, ST-3. No inter-dependencies. **C3 partition: GATE only**; Task 039 ST-5 (AGGREGATOR) imports this module's diagnostic schema and MUST be authored after ST-4 here.

**Prompt:** [`/prompts/tooling-trust-audit-gate/prompt.md`](../../../prompts/tooling-trust-audit-gate/prompt.md) — the executable instruction set for this subtask. The Goal, Falsification, Inputs, Acceptance Criteria, Dependencies, and Estimated Effort sections that previously lived inline have moved to that prompt's [`brief.md`](../../../prompts/tooling-trust-audit-gate/brief.md) per Task 041 (PR #70 review C.3 audit-graph repair).
