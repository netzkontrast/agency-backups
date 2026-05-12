---
type: note
status: draft
slug: task-033-st3-tooling-duplicate-task-id-linter
summary: "Subtask ST-3: ship tools/fm/check-duplicate-task-id.py — a pre-commit gating linter that closes the TASK.md §8.1 acknowledged-but-unenforced gap. Detects duplicate task_id values (currently 006/006 and 009/009) and exits 1."
created: 2026-05-06
updated: 2026-05-06
---

# ST-3: `check-duplicate-task-id` — Closes TASK.md §8.1 Enforcement Gap

**Executor:** main-agent
**Insertion point:** `[1/5]` frontmatter linter — extends `tools/fm/validate.py --type-check`. Default OFF in legacy mode; ERROR-tier when `FM_TOOLCHAIN=1`.

**Parallelism:** Phase A (parallel) — runs concurrently with ST-1, ST-2, ST-4. No inter-dependencies.

**Prompt:** [`/prompts/tooling-duplicate-task-id-linter/prompt.md`](../../../prompts/tooling-duplicate-task-id-linter/prompt.md) — the executable instruction set for this subtask. The Goal, Falsification, Inputs, Acceptance Criteria, Dependencies, and Estimated Effort sections that previously lived inline have moved to that prompt's [`brief.md`](../../../prompts/tooling-duplicate-task-id-linter/brief.md) per Task 041 (PR #70 review C.3 audit-graph repair).
