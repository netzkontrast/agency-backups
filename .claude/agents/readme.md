# .claude/agents/ — 17 persona sub-agent re-exports

Authored by Task 094 ST-2. Each `<slug>.md` file in this folder is a
thin Markdown wrapper that re-exports a `skill_kind: persona` (or the
single `agent-template` slug `superpowers-code-reviewer`) so Claude Code
treats it as an `@<slug>`-invocable sub-agent per
https://docs.anthropic.com/en/docs/claude-code/sub-agents.

The canonical body for every wrapper lives at
`skills/<slug>/SKILL.md` — these wrappers do not duplicate content;
they only expose the slug to the sub-agent discovery path.

## Roster (17)

- [sc-system-architect.md](./sc-system-architect.md)
- [sc-backend-architect.md](./sc-backend-architect.md)
- [sc-frontend-architect.md](./sc-frontend-architect.md)
- [sc-security-engineer.md](./sc-security-engineer.md)
- [sc-quality-engineer.md](./sc-quality-engineer.md)
- [sc-refactoring-expert.md](./sc-refactoring-expert.md)
- [sc-performance-engineer.md](./sc-performance-engineer.md)
- [sc-deep-research-agent.md](./sc-deep-research-agent.md)
- [sc-pm-agent.md](./sc-pm-agent.md)
- [sc-devops-architect.md](./sc-devops-architect.md)
- [sc-learning-guide.md](./sc-learning-guide.md)
- [sc-python-expert.md](./sc-python-expert.md)
- [sc-requirements-analyst.md](./sc-requirements-analyst.md)
- [sc-root-cause-analyst.md](./sc-root-cause-analyst.md)
- [sc-self-review.md](./sc-self-review.md)
- [sc-socratic-mentor.md](./sc-socratic-mentor.md)
- [superpowers-code-reviewer.md](./superpowers-code-reviewer.md)

## Why thin re-exports?

The 17 entries are SHA-pinned to the imported corpora (ADR-0011 D.3).
Duplicating their bodies into `.claude/agents/<slug>.md` would create a
drift surface the next time `skills/<slug>/SKILL.md` is re-synced.
The thin-wrapper pattern keeps the persona descriptions stable while
the implementation evolves under the canonical path.
