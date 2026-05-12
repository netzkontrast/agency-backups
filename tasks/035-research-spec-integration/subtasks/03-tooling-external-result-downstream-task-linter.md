---
type: note
status: draft
slug: task-035-st3-tooling-external-result-downstream-task-linter
summary: "Subtask ST-3: ship tools/check-external-result-downstream-task.py — closes R.6.5 by enforcing every /research/<provider>/<slug>/result.md has a corresponding open Task in /tasks/."
created: 2026-05-06
updated: 2026-05-06
---

# ST-3: `check-external-result-downstream-task` — Closes RESEARCH.md R.6.5 Gap

**Executor:** main-agent
**Insertion point:** `[1/5]` frontmatter linter extension — runs as part of `tools/fm/validate.py --type-check` when external-research files are staged.

**Parallelism:** Phase A (parallel) — runs concurrently with ST-1, ST-2, ST-4. No inter-dependencies.

**Prompt:** [`/prompts/tooling-external-result-downstream-task-linter/prompt.md`](../../../prompts/tooling-external-result-downstream-task-linter/prompt.md) — the executable instruction set for this subtask. The Goal, Falsification, Inputs, Acceptance Criteria, Dependencies, and Estimated Effort sections that previously lived inline have moved to that prompt's [`brief.md`](../../../prompts/tooling-external-result-downstream-task-linter/brief.md) per Task 041 (PR #70 review C.3 audit-graph repair).
