---
type: note
status: draft
slug: task-037-st3-tooling-per-rule-waiver-mechanism
summary: "Subtask ST-3: refactor tools/.frontmatter-waivers from per-file to per-rule scope. Accepts ADR.A.* diagnostic codes from §7.C as valid rule scopes."
created: 2026-05-06
updated: 2026-05-06
---

# ST-3: `per-rule-waiver-mechanism` — PC.7.B Refactor

**Executor:** main-agent
**Insertion point:** `[1/5]` frontmatter linter — modifies the existing waiver-loading pathway in `tools/fm/validate.py`.

**Parallelism:** Phase A (parallel) — runs concurrently with ST-1, ST-2. No inter-dependencies.

**Prompt:** [`/prompts/tooling-per-rule-waiver-mechanism/prompt.md`](../../../prompts/tooling-per-rule-waiver-mechanism/prompt.md) — the executable instruction set for this subtask. The Goal, Falsification, Inputs, Acceptance Criteria, Dependencies, and Estimated Effort sections that previously lived inline have moved to that prompt's [`brief.md`](../../../prompts/tooling-per-rule-waiver-mechanism/brief.md) per Task 041 (PR #70 review C.3 audit-graph repair).
