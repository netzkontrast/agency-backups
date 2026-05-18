---
type: index
status: active
slug: improve-maintenance-spec-may-18-2026-prompt-readme
summary: "Prompt-folder index for improve-maintenance-spec-may-18-2026 — the executable instruction set carrying Task 096's seven findings (F27–F33) to landed diffs."
created: 2026-05-18
updated: 2026-05-18
---

# Prompt — Improve Maintenance Spec from 2026-05-18 Coherence Run

## What and Why

This prompt is the executable instruction set linked from [Task 096](../../tasks/096-improve-maintenance-spec-may-18-2026/task.md) `task_uses_prompts`. It carries the seven findings F27–F33 distilled from the 2026-05-18 Repo Coherence Check session into concrete diffs against [`MAINTENANCE.md`](../../MAINTENANCE.md), [`prompts/repo-coherence-check/prompt.md`](../../prompts/repo-coherence-check/prompt.md), and [`tools/adr/cli.py`](../../tools/adr/cli.py). Per FOLDERS.md §4.1, the three-file scaffold (`prompt.md` + `brief.md` + `readme.md`) is mandatory at prompt creation; this file is the navigation index.

## Linked Navigation

- [`prompt.md`](./prompt.md) — RISEN+ReAct prompt body (Role, Input, Steps, Expected Output, Norms, Constraints).
- [`brief.md`](./brief.md) — Gherkin acceptance contract (AC-F27 through AC-F33). The single source of truth for "is the Task done?".

## Assumptions Log

- The prompt targets a future agent (likely Claude Code) executing Task 096. The agent is expected to read `task.md`, this prompt, and `brief.md` before authoring any diff.
- The seven findings are the closed in-scope set; new findings discovered during execution MUST be filed as a separate Task or deferred to `notes.md`, never silently expanded.
- The prompt requires execution of the [TASK.md §4.9](../../TASK.md#49-planning-pipeline-for-t3-structural-tasks-sc-ladder) `/sc:*` planning ladder as a pre-condition — this is normatively MUST (not SHOULD) because the spec edits cross three root files (MAINTENANCE.md + coherence prompt + adr CLI).
