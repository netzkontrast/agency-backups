---
type: note
status: draft
slug: task-032-st2-tooling-narrative-ontology-load-discipline
summary: "Subtask ST-2: ship tools/check-narrative-ontology-load.py — a session-trace linter that warns when an agent loads /maintenance/schemas/narrative-ontology/ during non-narrative work, closing the AGENTS.md NO.5 enforcement gap."
created: 2026-05-06
updated: 2026-05-06
---

# ST-2: `check-narrative-ontology-load` — NO.5 Enforcement

**Executor:** main-agent
**Insertion point:** `[opt]` WARN-tier — runs alongside the existing narrative-ontology validator block (does not gate).

**Parallelism:** Phase A (parallel) — runs concurrently with ST-1, ST-3, ST-4. No inter-dependencies.

**Prompt:** [`/prompts/tooling-narrative-ontology-load-discipline/prompt.md`](../../../prompts/tooling-narrative-ontology-load-discipline/prompt.md) — the executable instruction set for this subtask. The Goal, Falsification, Inputs, Acceptance Criteria, Dependencies, and Estimated Effort sections that previously lived inline have moved to that prompt's [`brief.md`](../../../prompts/tooling-narrative-ontology-load-discipline/brief.md) per Task 041 (PR #70 review C.3 audit-graph repair).
