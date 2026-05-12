---
type: note
status: draft
slug: task-032-st4-tooling-assumption-log-substance
summary: "Subtask ST-4: ship tools/check-assumption-log.py — a linter that validates the substance of `## Assumptions Log` sections in operational-folder readme.md files (FOLDERS.md F.3 + AGENTS.md §60-65), enforcing minimum-substance and currency."
created: 2026-05-06
updated: 2026-05-06
---

# ST-4: `check-assumption-log` — FOLDERS.md F.3 / AGENTS.md §60-65 Enforcement

**Executor:** main-agent
**Insertion point:** `[opt]` WARN-tier — invoked over operational `readme.md` files only; never gating.

**Parallelism:** Phase A (parallel) — runs concurrently with ST-1, ST-2, ST-3. No inter-dependencies.

**Prompt:** [`/prompts/tooling-assumption-log-substance/prompt.md`](../../../prompts/tooling-assumption-log-substance/prompt.md) — the executable instruction set for this subtask. The Goal, Falsification, Inputs, Acceptance Criteria, Dependencies, and Estimated Effort sections that previously lived inline have moved to that prompt's [`brief.md`](../../../prompts/tooling-assumption-log-substance/brief.md) per Task 041 (PR #70 review C.3 audit-graph repair).
