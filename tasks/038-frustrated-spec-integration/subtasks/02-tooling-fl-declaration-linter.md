---
type: note
status: draft
slug: task-038-st2-tooling-fl-declaration-linter
summary: "Subtask ST-2: ship tools/check-fl-declaration.py — parses friction-log.md + PR descriptions for the canonical 'Highest Frustration Level: FL[0-3]' line; rejects malformed/missing on task closure."
created: 2026-05-06
updated: 2026-05-06
---

# ST-2: `check-fl-declaration` — Mechanical FL-Declaration Gate

**Executor:** main-agent
**Insertion point:** `[trust]` step — extends `tools/check-trust.py` rather than introducing a parallel pipeline.

**Parallelism:** Phase A (parallel-grouped, soft-blocked) — runs alongside ST-1 but soft-depends on ST-1 SPEC §2 (variant-form set). Phase A may ship with strict canonical form + upgrade post-ST-1.

**Prompt:** [`/prompts/tooling-fl-declaration-linter/prompt.md`](../../../prompts/tooling-fl-declaration-linter/prompt.md) — the executable instruction set for this subtask. The Goal, Falsification, Inputs, Acceptance Criteria, Dependencies, and Estimated Effort sections that previously lived inline have moved to that prompt's [`brief.md`](../../../prompts/tooling-fl-declaration-linter/brief.md) per Task 041 (PR #70 review C.3 audit-graph repair).
