---
name: sc-improve
description: >-
  Apply systematic improvements to code quality, performance, and maintainability. Use when the user invokes /sc:improve, asks for refactoring, performance tuning, or quality cleanup.
skill_kind: orchestrator
skill_target_agents: [claude-code]
skill_references_skills: [sc-quality-engineer, sc-refactoring-expert, sc-performance-engineer]
skill_references_research: []
skill_references_prompts: []
skill_bootstrap_required: false
skill_source: "superclaude@v4.3.0"
---

# sc-improve — `/sc:improve` (imported from SuperClaude v4.3.0)

## What

Imported `/sc:improve` command from SuperClaude_Framework. Coordinates quality, refactoring, and performance personas to improve an existing codebase.

## When to use

Use when the user invokes `/sc:improve` or asks for refactoring, performance tuning, or quality cleanup.

## How to use

1. Triage the request into quality / refactor / performance buckets.
2. Delegate to the sibling persona skill that owns each bucket.
3. Aggregate findings into a single improvement plan.

Full behavioural specification at `references/upstream-sc-improve.md`.

## References

- Upstream: [`src/superclaude/commands/improve.md@22ad3f4`](https://github.com/SuperClaude-Org/SuperClaude_Framework/blob/22ad3f483a6fe6c626834e1c9a3573126644a058/src/superclaude/commands/improve.md) — verbatim mirror at [`references/upstream-sc-improve.md`](./references/upstream-sc-improve.md) (ADR-0011 D.3).
- Agency anchor: CLAUDE.md §13 — `/sc:*` skill invocation policy.
- Import policy: [`decisions/0011-external-skill-corpora-import.md`](../../decisions/0011-external-skill-corpora-import.md).

## Compatibility

- Target agent: `claude-code` (this repo's primary surface)
- Known limitation: imported one-shot snapshot at SuperClaude_Framework `v4.3.0` — re-syncs require a new Task per ADR-0011 D.9.
