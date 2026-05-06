---
type: index
status: active
slug: extract-subtask-prompts-prompt-readme
summary: "Index for prompt extract-subtask-prompts — task-spec prompt that drives Task 041 (audit-graph repair extracting 35 inlined subtask Execution Briefs to /prompts/<slug>/). Authored retroactively to close PR #72 review F-D (Task 041 task_uses_prompts: [] irony)."
created: 2026-05-06
updated: 2026-05-06
---

# Prompt — extract-subtask-prompts

- [`brief.md`](./brief.md) — Raw user request + use-case context.
- [`prompt.md`](./prompt.md) — The executable RISEN+ReAct task-spec prompt.

## Usage

Drives [Task 041](../../tasks/041-extract-subtask-prompts/task.md). Reciprocity binds via the parent task's `task_uses_prompts: [extract-subtask-prompts, ...]` and this prompt's `prompt_relates_to_task: extract-subtask-prompts`.

## Source

Authored retroactively as part of the F-D fix from PR #72 review. The original Task 041 closure (PR #72) shipped with `task_uses_prompts: []`, which the reviewer flagged as ironic (the policy-enforcement task exempt from its own policy). This prompt closes that gap; it documents what the executing agent actually did when running the bulk extraction on `2026-05-06`.
