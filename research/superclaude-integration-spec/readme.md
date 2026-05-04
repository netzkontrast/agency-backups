---
type: research
status: completed
slug: superclaude-integration-spec
summary: "Research workspace: SuperClaude v4.3.0 × Agency governance integration spec."
created: 2026-05-04
updated: 2026-05-04
research_phase: complete
research_executes_prompt: superclaude-integration-spec
research_friction_level: FL1
---

# /research/superclaude-integration-spec/

Research workspace executing the prompt at `/prompts/superclaude-integration-spec/prompt.md`.

Produces a governance spec mapping all SuperClaude Framework v4.3.0 components to Agency workflow phases.

## Structure

- [prompt.md](./prompt.md) — Immutable snapshot of the executing prompt at run-start.
- [workspace/](./workspace/) — Session logs and scratch artifacts.
- [synthesis/](./synthesis/) — Structured synthesis: methodology, tracks, state, merge log.
- [reflection/](./reflection/) — Critical-thinking reflection: friction log, methods applied.
- [output/](./output/) — Final deliverable: `SPEC.md`.

## Open Questions Surfaced

- [`/prompts/maintenance-todo-audit/`](../../prompts/maintenance-todo-audit/) — Ratify /todo/ → /prompts/ correction; scan for remaining references.

## Assumption Log

- SuperClaude v4.3.0 was confirmed installed at `~/.claude/` by running `ls ~/.claude/commands/sc/` (30 commands), `ls ~/.claude/agents/` (20 agents), `ls ~/.claude/skills/` (session-start-hook).
- `confidence-check` skill is available as a system-provided skill (visible in system-reminder) even though not present as a file in `~/.claude/skills/`.
- All command behavioral flows were read directly from installed `.md` files, not inferred.
