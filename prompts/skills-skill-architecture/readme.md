---
type: index
status: active
slug: skills-skill-architecture
summary: "Research proposal prompt for the skills-skill architecture. Spawns the research workspace at /research/skills-skill-architecture/."
created: 2026-05-04
updated: 2026-05-04
---

# /prompts/skills-skill-architecture/

## What and Why

This folder holds the research-proposal prompt for the `skills-skill` architecture task. It was created by the Claude Code agent executing Stage C of the bootstrap-skills-sync mission (branch `claude/research-skills-skill-arch`).

The prompt asks a future agent to research and specify the `skills-skill` loader — a single stub skill that, when installed in `/mnt/skills/user/`, routes all skill loading through this repository's `/skills/` directory.

## Linked Navigation

| File | Purpose |
|---|---|
| [brief.md](./brief.md) | Unedited user request, context, and constraints |
| [prompt.md](./prompt.md) | The crafted, self-contained research-proposal prompt |

## Executed By

Research workspace: [`/research/skills-skill-architecture/`](../../research/skills-skill-architecture/)

## Assumptions Log

- `prompt_framework: RISEN` was chosen because this is a structured one-shot output task (spec + deliverables), not an iterative extraction task.
- The prompt verbatim replicates the brief from the mission rather than being re-crafted, because the mission explicitly required the brief to appear character-for-character in the prompt.md of the research folder. The prompt at /prompts/ is the canonical home; the snapshot in /research/skills-skill-architecture/prompt.md is a copy per RESEARCH.md §4.3.
