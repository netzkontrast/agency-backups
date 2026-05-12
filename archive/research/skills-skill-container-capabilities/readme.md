---
type: research
status: archived
slug: skills-skill-container-capabilities
summary: "U1: git NOT confirmed pre-installed in claude.ai; use GitHub REST API. U2: filesystem does NOT persist between sessions; treat every conversation as fresh."
created: 2026-05-04
updated: 2026-05-12
research_phase: archived
research_executes_prompt: skills-skill-container-capabilities
research_friction_level: FL1
---

# /research/skills-skill-container-capabilities/

Research workspace resolving UNCERTAIN markers U1 (git availability) and U2 (filesystem persistence) from `research/skills-skill-architecture/output/SPEC.md`.

## Navigation

- [prompt.md](./prompt.md) — Immutable snapshot of the executing prompt.
- [workspace/](./workspace/) — Session log and raw search results.
- [synthesis/](./synthesis/) — Structured synthesis artifacts (state, tracks, methodology, merge log).
- [reflection/](./reflection/) — Friction log (FL1) and M13 evidence quality assessment.
- [output/SPEC.md](./output/SPEC.md) — **Final deliverable**: findings and RFC-2119 patch text.

## Key Findings

| Marker | Finding |
|---|---|
| U1: git binary | NOT confirmed pre-installed. Use GitHub REST API via Python requests. |
| U1: bash execution | CONFIRMED via `bash_code_execution` sub-tool. |
| U2: persistence | NOT guaranteed between conversations. Treat every session as fresh. |

## Open Questions Surfaced

- [`skills-skill-enterprise-offline`](../../prompts/skills-skill-enterprise-offline/prompt.md) — Files API offline fallback for Team/Enterprise plans where network is disabled.
- [`claude-ai-container-git-verification`](../../prompts/claude-ai-container-git-verification/prompt.md) — Empirically verify git absence by running `which git` in a live claude.ai session (upgrades U1 from (d) inference to (a) empirical).
