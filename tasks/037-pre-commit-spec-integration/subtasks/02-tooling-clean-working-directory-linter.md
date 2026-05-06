---
type: note
status: draft
slug: task-037-st2-tooling-clean-working-directory-linter
summary: "Subtask ST-2: ship tools/check-clean-working-directory.py — closes PC.1.1 by scanning for stray .py/.sh scratchpads at commit time. Exempts /decisions/ per FOLDERS.md §8."
created: 2026-05-06
updated: 2026-05-06
---

# ST-2: `check-clean-working-directory` — Closes PRE_COMMIT.md PC.1.1 Gap

**Executor:** main-agent
**Insertion point:** `[2/5]` directory-structure linter extension.

**Parallelism:** Phase A (parallel) — runs concurrently with ST-1, ST-3. No inter-dependencies.

**Prompt:** [`/prompts/tooling-clean-working-directory-linter/prompt.md`](../../../prompts/tooling-clean-working-directory-linter/prompt.md) — the executable instruction set for this subtask. The Goal, Falsification, Inputs, Acceptance Criteria, Dependencies, and Estimated Effort sections that previously lived inline have moved to that prompt's [`brief.md`](../../../prompts/tooling-clean-working-directory-linter/brief.md) per Task 041 (PR #70 review C.3 audit-graph repair).
