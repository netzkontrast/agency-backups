---
type: index
status: active
slug: prompt-refactor-governance-from-specs
summary: "Folder index for the task-spec prompt that drives Task 001."
created: 2026-05-04
updated: 2026-05-04
---

# Prompt — Refactor Governance from Specs

**What is this folder?** The instruction set linked by [`/tasks/001-refactor-governance-from-specs/task.md`](../../tasks/001-refactor-governance-from-specs/task.md) via `task_uses_prompts`.

**Why is it here?** Per `TASK.md` §1, prompts MUST NOT be inlined inside `task.md`. This folder is the linked artifact.

## Contents

- [`brief.md`](./brief.md) — Raw request, target agent, use-case context, constraints.
- [`prompt.md`](./prompt.md) — Skeleton RISE-DX prompt; Plan step 1 of Task 001 fleshes it out.

## Workflow Assumptions

- `prompt.md` is currently a skeleton (`status: draft`). It becomes `status: active` only when fully authored per `PROMPT.md`.
- This prompt is `prompt_kind: task-spec`, not `research-proposal`. It does not produce a research workspace; it produces enforcement artifacts.
