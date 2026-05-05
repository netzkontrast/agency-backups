---
type: index
status: active
slug: task-017-migrate-repo-to-flexible-toolchain
summary: "Migration Task: cut over the repo from the legacy linters to the flexible-frontmatter toolchain shipped by Task 016. Three batches: mechanical, additive, structural."
created: 2026-05-05
updated: 2026-05-05
---

# Task 017 — Migration Hand-Off

**What is this folder?** The orchestration unit that retires the four legacy linters and binds the new toolchain into pre-commit + coherence checks.

**Why is it here?** Per `TASK.md`, structural changes (T3) MUST go through a Task. Three of this Task's nine steps are T3.

**Status: blocked.** This Task may not begin until Task 016 sets `task_status: done`.

## Linked Navigation

- [`task.md`](./task.md) — frontmatter, goal, three-batch plan, todo, links.
- Executing prompt: [`/prompts/migrate-repo-to-flexible-toolchain/`](../../prompts/migrate-repo-to-flexible-toolchain/).
- Implementation predecessor: [`/tasks/016-flexible-frontmatter-toolchain/`](../016-flexible-frontmatter-toolchain/).
