---
type: note
status: draft
slug: task-035-st2-tooling-workspace-cleanliness-linter
summary: "Subtask ST-2: ship tools/check-workspace-cleanliness.py — closes the R.4.4 enforcement gap by scanning /research/<slug>/workspace/ for stragglers (.py/.sh/.log) at commit time."
created: 2026-05-06
updated: 2026-05-06
---

# ST-2: `check-workspace-cleanliness` — Closes RESEARCH.md R.4.4 Gap

**Executor:** main-agent
**Insertion point:** `[opt]` WARN-tier — runs over changed `/research/<slug>/workspace/` paths only.

**Parallelism:** Phase A (parallel) — runs concurrently with ST-1, ST-3, ST-4. No inter-dependencies.

**Prompt:** [`/prompts/tooling-workspace-cleanliness-linter/prompt.md`](../../../prompts/tooling-workspace-cleanliness-linter/prompt.md) — the executable instruction set for this subtask. The Goal, Falsification, Inputs, Acceptance Criteria, Dependencies, and Estimated Effort sections that previously lived inline have moved to that prompt's [`brief.md`](../../../prompts/tooling-workspace-cleanliness-linter/brief.md) per Task 041 (PR #70 review C.3 audit-graph repair).
