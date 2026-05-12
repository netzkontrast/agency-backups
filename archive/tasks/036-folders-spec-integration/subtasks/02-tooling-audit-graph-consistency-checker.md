---
type: note
status: draft
slug: task-036-st2-tooling-audit-graph-consistency-checker
summary: "Subtask ST-2: ship tools/check-audit-graph-consistency.py — warns when body Markdown links reference sibling folders without matching frontmatter linkage."
created: 2026-05-06
updated: 2026-05-06
---

# ST-2: `check-audit-graph-consistency` — F.6 Dual-Surface Drift

**Executor:** main-agent
**Insertion point:** `[opt]` WARN-tier — advisory only, since FOLDERS.md §6 explicitly encourages body links for human navigation.

**Parallelism:** Phase A (parallel) — runs concurrently with ST-1. No inter-dependencies.

**Prompt:** [`/prompts/tooling-audit-graph-consistency-checker/prompt.md`](../../../prompts/tooling-audit-graph-consistency-checker/prompt.md) — the executable instruction set for this subtask. The Goal, Falsification, Inputs, Acceptance Criteria, Dependencies, and Estimated Effort sections that previously lived inline have moved to that prompt's [`brief.md`](../../../prompts/tooling-audit-graph-consistency-checker/brief.md) per Task 041 (PR #70 review C.3 audit-graph repair).
