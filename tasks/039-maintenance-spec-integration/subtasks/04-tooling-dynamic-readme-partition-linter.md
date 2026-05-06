---
type: note
status: draft
slug: task-039-st4-tooling-dynamic-readme-partition-linter
summary: "Subtask ST-4: ship tools/maintenance/dynamic-readme-partition.py implementing the static/dynamic partition rule from research/repo-maintenance-protocol-spec/output/SPEC.md §3.1."
created: 2026-05-06
updated: 2026-05-06
---

# ST-4: `dynamic-readme-partition` — Operationalizes repo-maintenance-protocol-spec §3.1

**Executor:** maintenance-agent
**Insertion point:** `[opt]` WARN-tier — runs over operational-folder readmes only; advisory.

**Parallelism:** Phase A (parallel) — runs concurrently with ST-1, ST-2, ST-3, ST-5. No inter-dependencies.

**Prompt:** [`/prompts/tooling-dynamic-readme-partition-linter/prompt.md`](../../../prompts/tooling-dynamic-readme-partition-linter/prompt.md) — the executable instruction set for this subtask. The Goal, Falsification, Inputs, Acceptance Criteria, Dependencies, and Estimated Effort sections that previously lived inline have moved to that prompt's [`brief.md`](../../../prompts/tooling-dynamic-readme-partition-linter/brief.md) per Task 041 (PR #70 review C.3 audit-graph repair).
