---
type: note
status: completed
slug: task-034-st2-tooling-self-containedness-checker
summary: "Subtask ST-2: ship tools/check-prompt-self-containedness.py — a structural linter that checks PROMPT.md §5.1 self-containedness via heuristics derived from the research-prompt-optimizer Phase 4 reader-test prior art."
created: 2026-05-06
updated: 2026-05-07
---

# ST-2: `check-prompt-self-containedness` — Mechanizes P.5.1

**Executor:** main-agent
**Insertion point:** `[opt]` WARN-tier — runs only on changed `/prompts/<slug>/prompt.md` files.

**Parallelism:** Phase A (parallel-grouped, soft-blocked) — runs alongside ST-3 but soft-depends on ST-1 SPEC §3 heuristic recipe. Phase A may proceed with stub heuristic + upgrade post-ST-1.

**Prompt:** [`/prompts/tooling-self-containedness-checker/prompt.md`](../../../prompts/tooling-self-containedness-checker/prompt.md) — the executable instruction set for this subtask. The Goal, Falsification, Inputs, Acceptance Criteria, Dependencies, and Estimated Effort sections that previously lived inline have moved to that prompt's [`brief.md`](../../../prompts/tooling-self-containedness-checker/brief.md) per Task 041 (PR #70 review C.3 audit-graph repair).
