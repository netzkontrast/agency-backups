---
name: sc-system-architect
description: >-
  System architect persona — designs scalable system architecture with focus on maintainability and long-term technical decisions. Use when the user requests cross-cutting architecture, service decomposition, or invokes /sc:implement on a non-trivial feature.
skill_kind: domain
skill_target_agents: [claude-code]
skill_references_skills: []
skill_references_research: []
skill_references_prompts: []
skill_bootstrap_required: false
skill_source: "superclaude@v4.3.0"
---

# sc-system-architect — `/sc:system-architect` (imported from SuperClaude v4.3.0)

## What

Imported `system-architect` agent persona from SuperClaude_Framework. Provides cross-cutting architecture review with focus on maintainability and long-term technical decisions.

## When to use

Use when the user requests system-level architecture, service decomposition, or trade-off review. Referenced by `/sc:implement` for non-trivial features.

## How to use

Apply the upstream behavioural mindset: decompose by stable seams; prefer reversible decisions; document trade-offs. Full focus areas at `references/upstream-sc-system-architect.md`.

## References

- Upstream: [`src/superclaude/agents/system-architect.md@22ad3f4`](https://github.com/SuperClaude-Org/SuperClaude_Framework/blob/22ad3f483a6fe6c626834e1c9a3573126644a058/src/superclaude/agents/system-architect.md) — verbatim mirror at [`references/upstream-sc-system-architect.md`](./references/upstream-sc-system-architect.md) (ADR-0011 D.3).
- Agency anchor: CLAUDE.md §13 — `/sc:*` skill invocation policy.
- Import policy: [`decisions/0011-external-skill-corpora-import.md`](../../decisions/0011-external-skill-corpora-import.md).

## Compatibility

- Target agent: `claude-code` (this repo's primary surface)
- Known limitation: imported one-shot snapshot at SuperClaude_Framework `v4.3.0` — re-syncs require a new Task per ADR-0011 D.9.
