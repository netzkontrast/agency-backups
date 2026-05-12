---
type: research
status: archived
slug: skills-skill-architecture
summary: "Research workspace for the skills-skill loader architecture. Preliminary spec covering R1-R7 with six UNCERTAIN markers deferred to Gemini Deep Research."
created: 2026-05-04
updated: 2026-05-12
research_phase: archived
research_executes_prompt: skills-skill-architecture
research_friction_level: FL1
---

# /research/skills-skill-architecture/

Research workspace for the `skills-skill` architecture task. Executes the prompt at `/prompts/skills-skill-architecture/`.

## What and Why

This workspace exists to produce a preliminary architecture spec for `skills-skill`: a stub installed in the claude.ai container that, on activation, clones this repository and routes all skill requests to versioned skill bodies. It is Stage C of the bootstrap-skills-sync mission.

The research is preliminary by design — a Gemini Deep Research pass is planned to fill six empirical gaps (U1–U6). The integration plan for folding that PDF back is at `output/integration-plan.md`.

## Linked Navigation

| Path | Purpose |
|---|---|
| [prompt.md](./prompt.md) | Immutable snapshot of the executing prompt |
| [workspace/](./workspace/) | Session log and scratch notes |
| [synthesis/](./synthesis/) | Structured synthesis: methodology, tracks, merge log, state |
| [reflection/](./reflection/) | Friction log (FL1) |
| [output/](./output/) | Final deliverables: SPEC.md, gemini-prompt.md, integration-plan.md |

## Key Findings

1. Claude Code skill format (`~/.claude/skills/<name>/SKILL.md`) is **identical** to claude.ai's format. No adapter needed.
2. Read/write topology is unambiguous: repo is canonical, `/mnt/skills/user/` is read-only, `~/.claude/skills/` is synced by Stage B.
3. Two-tier routing model: host activates stub → stub selects skill body. Complement, not replace.
4. Three-tier disclosure: summary → full body → references. No persistent state assumed.
5. Six UNCERTAIN markers (U1–U6) deferred to Gemini Deep Research. See output/SPEC.md §9.

## Open Questions Surfaced

Three follow-up prompts filed per RESEARCH.md §4.9:

| Prompt slug | Question |
|---|---|
| [skills-skill-trigger-lifecycle](../../prompts/skills-skill-trigger-lifecycle/) | How does claude.ai's host select which skill to activate? (U3) |
| [skills-skill-jules-portability](../../prompts/skills-skill-jules-portability/) | Jules skill-loading conventions (U4) |
| [skills-skill-gemini-cli-portability](../../prompts/skills-skill-gemini-cli-portability/) | gemini-cli skill-loading conventions (U4) |

## Assumptions Log

- This research workspace was created on branch `claude/research-skills-skill-arch` before Stage A merged. Therefore Stage A's 14 skills were NOT present in `origin/main:skills/` during the research run. The spec references them by convention but was written against the anticipated post-Stage-A state.
- No web search was performed. All synthesis is from direct environment inspection and reasoning. Gemini Deep Research is the planned empirical complement.
