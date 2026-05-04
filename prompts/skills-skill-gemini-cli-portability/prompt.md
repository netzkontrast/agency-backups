---
type: prompt
status: active
slug: skills-skill-gemini-cli-portability
summary: "Research gemini-cli instruction loading to determine SKILL.md compatibility or required adapter."
created: 2026-05-04
updated: 2026-05-04
prompt_kind: follow-up
prompt_framework: RISEN
prompt_target_agent: Claude Code
prompt_relates_to_task: ""
prompt_spawned_from_research: skills-skill-architecture
---

# Research: gemini-cli Skill-Loading Convention

## Context

The `skills-skill` architecture must serve skill content to four agents. gemini-cli compatibility is unknown. This follows up on R2-Q2 in the Gemini Deep Research prompt (see `research/skills-skill-architecture/output/gemini-prompt.md`).

## Research Question

1. Does gemini-cli support custom instruction files (e.g., `GEMINI.md`)?
2. If yes: what path, format, trigger?
3. Is the format compatible with SKILL.md?
4. If not: what adapter is needed?

## Required Output

If compatible: update `research/skills-skill-architecture/output/SPEC.md` Section 7.1 R6 table.
If adapter needed: create `skills/skills-skill/adapters/gemini-cli/` with specification.

## Prerequisite

Check Gemini PDF R2-Q2 first.
