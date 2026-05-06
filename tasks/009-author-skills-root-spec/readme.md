---
type: index
status: active
slug: 009-author-skills-root-spec
summary: "Index for Task 009 — author SKILLS.md, the missing root governance spec for /skills/."
created: 2026-05-04
updated: 2026-05-04
---

# Task 009 — Author Skills Root Spec

## What and Why

This folder coordinates the authoring of `SKILLS.md` at the repository root. Today, `/skills/` is the only top-level operational concern without a root governance file; this Task closes that gap so future skill work can fail-closed against an explicit spec.

## Linked Navigation

- [`task.md`](./task.md) — Goal, Plan, Todo, Links.
- [`friction-log.md`](./friction-log.md) — Friction log (FL0).
- [`notes.md`](./notes.md) — Claude Code review of PR #73 (post-task governance review).
- Executing prompt: [`/prompts/author-skills-root-spec/prompt.md`](../../prompts/author-skills-root-spec/prompt.md).
- Sibling tasks: [`../010-skills-frontmatter-index-suite/`](../010-skills-frontmatter-index-suite/), [`../011-skills-frontmatter-schema-files/`](../011-skills-frontmatter-schema-files/).

## Assumptions Log

- We assume `SKILLS.md` should live at the repository root, mirroring `TASK.md` / `PROMPT.md` / `RESEARCH.md`. An alternative ("skills are content, not orchestration; the root spec belongs in `skills/SKILLS.md`") was considered and rejected: the routing table in `AGENTS.md` is the agent's first read, and that table consults files at the repository root.
- We assume the L2 `skill_*` namespace can be added without breaking the existing 14 skills, because none of them currently carry L1+L2 frontmatter — the linter is silent on `skills/`. This is verified by a run of `tools/validate-frontmatter.py` on the current tree before edits begin.
- We assume the bootstrap clone path `$AGENCY_SKILLS_ROOT` is a workspace-level convention that does NOT collide with Claude Code's `~/.claude/skills/`. The Code-side path remains the rendered runtime; `$AGENCY_SKILLS_ROOT` is the *source* a tool reads to render that runtime, identical for Jules and Gemini.
