---
type: note
status: completed
slug: task-034-st3-tooling-framework-declaration-validator
summary: "Subtask ST-3: ship tools/check-prompt-framework-declaration.py — verifies every /prompts/<slug>/prompt.md declares one of the canonical frameworks per PROMPT.md §4.3."
created: 2026-05-06
updated: 2026-05-07
---

# ST-3: `check-prompt-framework-declaration` — Mechanizes P.5.2

**Executor:** main-agent
**Insertion point:** `[opt]` WARN-tier — runs only on changed `/prompts/<slug>/prompt.md` files.

**Parallelism:** Phase A (parallel-grouped, soft-blocked) — runs alongside ST-2; soft-depends on ST-1 SPEC §3 framework-list extension.

**Prompt:** [`/prompts/tooling-framework-declaration-validator/prompt.md`](../../../prompts/tooling-framework-declaration-validator/prompt.md) — the executable instruction set for this subtask. The Goal, Falsification, Inputs, Acceptance Criteria, Dependencies, and Estimated Effort sections that previously lived inline have moved to that prompt's [`brief.md`](../../../prompts/tooling-framework-declaration-validator/brief.md) per Task 041 (PR #70 review C.3 audit-graph repair).
