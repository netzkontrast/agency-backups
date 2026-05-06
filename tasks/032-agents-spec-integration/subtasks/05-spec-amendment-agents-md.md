---
type: note
status: draft
slug: task-032-st5-spec-amendment-agents-md
summary: "Subtask ST-5 (Phase B): apply the AGENTS.md edits per Tasks 032 (a)-(f). Lifts ST-1's curated ADR corpus into §0 Theoretical Foundations + §3.3 footnote; documents §6 skills container caps; references new linters (ST-2/3/4)."
created: 2026-05-06
updated: 2026-05-06
---

# ST-5: Spec Amendment — AGENTS.md

**Executor:** main-agent

**Parallelism:** Phase B (sequential) — depends on ST-1 (research SPEC) + ST-2/ST-3/ST-4 (linter implementations). MUST wait for all four to land.

**Prompt:** [`/prompts/spec-amendment-agents-md/prompt.md`](../../../prompts/spec-amendment-agents-md/prompt.md) — the executable instruction set for this subtask. The Goal, Falsification, Inputs, Acceptance Criteria, Dependencies, and Estimated Effort sections that previously lived inline have moved to that prompt's [`brief.md`](../../../prompts/spec-amendment-agents-md/brief.md) per Task 041 (PR #70 review C.3 audit-graph repair).
