---
type: note
status: draft
slug: task-036-st1-tooling-readme-frontmatter-validator
summary: "Subtask ST-1: ship tools/check-readme-frontmatter.py — promotes FOLDERS.md F.5 from SHOULD to mechanically-enforced MUST."
created: 2026-05-06
updated: 2026-05-06
---

# ST-1: `check-readme-frontmatter` — F.5 SHOULD → MUST

**Executor:** main-agent
**Insertion point:** `[2/5]` directory-structure linter — extends `tools/lint-structure.py`.

**Parallelism:** Phase A (parallel) — runs concurrently with ST-2. No inter-dependencies.

**Prompt:** [`/prompts/tooling-readme-frontmatter-validator/prompt.md`](../../../prompts/tooling-readme-frontmatter-validator/prompt.md) — the executable instruction set for this subtask. The Goal, Falsification, Inputs, Acceptance Criteria, Dependencies, and Estimated Effort sections that previously lived inline have moved to that prompt's [`brief.md`](../../../prompts/tooling-readme-frontmatter-validator/brief.md) per Task 041 (PR #70 review C.3 audit-graph repair).
