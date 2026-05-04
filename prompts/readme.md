---
type: index
status: active
slug: prompts-root
summary: "Root of /prompts/. Holds every executable instruction set: research proposals, follow-ups, tool instructions, task-specs."
created: 2026-05-02
updated: 2026-05-04
---

# Prompts Root

**What is this folder?** The single home for every executable instruction set in this repository. Prompts are the *what the agent is told to do*; Tasks coordinate, Research records what running them produced.

**Why is it here?** To enforce separation of concerns. Prompt drafting MUST NOT happen inside `/research/` (which is execution-only) and MUST NOT be inlined inside `/tasks/<NNN>-<slug>/task.md` (which only links via `task_uses_prompts`).

## Governing Specification

All work in this folder MUST conform to [`PROMPT.md`](../PROMPT.md). Frontmatter and cross-directory linkage rules live in [`TASK.md`](../TASK.md) §3 and [`FOLDERS.md`](../FOLDERS.md).

## What Belongs Here (per `PROMPT.md` §1)

1. Research proposals (`prompt_kind: research-proposal`).
2. Follow-up prompts surfaced from prior research runs (`prompt_kind: follow-up`).
3. Tool instructions (`prompt_kind: tool-instruction`).
4. Task-specs referenced by `/tasks/<NNN>-<slug>/task.md` (`prompt_kind: task-spec`).

## Contents

- [`research-prompt-from-annotations/`](./research-prompt-from-annotations/) — A prompt that scans an existing research folder for open questions and generates new research prompts from those findings.

## Workflow Assumptions

- Each subfolder corresponds to exactly one Prompt Task, identified by a kebab-case slug.
- The slug is derived from the prompt's core intent, not from a date or ticket number.
- `brief.md` is immutable once written; it records what was originally requested.
- `prompt.md` carries L1 + `prompt_*` frontmatter and MUST be executable in isolation.
- This folder was renamed from `/prompt/` (singular) to `/prompts/` (plural) on 2026-05-04 as part of the orchestration refactor that introduced `/tasks/`.
