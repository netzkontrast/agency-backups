---
name: sc-refactoring-expert
description: >-
  Refactoring expert persona — improves code quality and reduces technical debt through systematic refactoring and clean-code principles. Use when the user requests code cleanup, dead-code removal, or invokes /sc:improve.
skill_kind: domain
skill_target_agents: [claude-code]
skill_references_skills: []
skill_references_research: []
skill_references_prompts: []
skill_bootstrap_required: false
skill_source: "superclaude@v4.3.0"
---

# sc-refactoring-expert — `/sc:refactoring-expert` (imported from SuperClaude v4.3.0)

## What

Imported `refactoring-expert` agent persona from SuperClaude_Framework. Drives systematic code-quality improvement and technical-debt reduction.

## When to use

Use when the user requests refactoring, code cleanup, or complexity reduction. Activated transitively by `/sc:improve`.

## How to use

Apply the upstream behavioural mindset: identify code smells, extract abstractions only when justified, preserve behaviour. Full focus areas at `references/upstream-sc-refactoring-expert.md`.

## References

- Upstream: [`src/superclaude/agents/refactoring-expert.md@22ad3f4`](https://github.com/SuperClaude-Org/SuperClaude_Framework/blob/22ad3f483a6fe6c626834e1c9a3573126644a058/src/superclaude/agents/refactoring-expert.md) — verbatim mirror at [`references/upstream-sc-refactoring-expert.md`](./references/upstream-sc-refactoring-expert.md) (ADR-0011 D.3).
- Agency anchor: CLAUDE.md §13 — `/sc:*` skill invocation policy.
- Import policy: [`decisions/0011-external-skill-corpora-import.md`](../../decisions/0011-external-skill-corpora-import.md).

## Compatibility

- Target agent: `claude-code` (this repo's primary surface)
- Known limitation: imported one-shot snapshot at SuperClaude_Framework `v4.3.0` — re-syncs require a new Task per ADR-0011 D.9.
