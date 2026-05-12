---
name: sc-deep-research-agent
description: >-
  Deep research specialist — comprehensive research with adaptive strategies, multi-hop reasoning, and evidence chains. Use when the user invokes /sc:research or requests a deep-research run beyond a single search.
skill_kind: domain
skill_target_agents: [claude-code]
skill_references_skills: []
skill_references_research: []
skill_references_prompts: []
skill_bootstrap_required: false
skill_source: "superclaude@v4.3.0"
---

# sc-deep-research-agent — `/sc:deep-research-agent` (imported from SuperClaude v4.3.0)

## What

Imported `deep-research-agent` from SuperClaude_Framework. Specialist for comprehensive research with adaptive strategies and intelligent exploration.

## When to use

Use when the user invokes `/sc:research` or asks for a multi-hop investigation. Body adapted per ADR-0011 D.8: WebSearch + WebFetch are the primary surface; Tavily is OPTIONAL.

## How to use

1. Apply Adaptive Planning (Planning-Only / Intent-Planning / Unified).
2. Use **WebSearch** for primary discovery, **WebFetch** for extraction; Tavily MCP is OPTIONAL when present.
3. Track hop genealogy ≤ 5 levels; replan when confidence < 60%.
4. Land deliverables at `/research/<slug>/output/SPEC.md` per RESEARCH.md §6.5.

Full behavioural specification at `references/upstream-sc-deep-research-agent.md`.

## References

- Upstream: [`src/superclaude/agents/deep-research-agent.md@22ad3f4`](https://github.com/SuperClaude-Org/SuperClaude_Framework/blob/22ad3f483a6fe6c626834e1c9a3573126644a058/src/superclaude/agents/deep-research-agent.md) — verbatim mirror at [`references/upstream-sc-deep-research-agent.md`](./references/upstream-sc-deep-research-agent.md) (ADR-0011 D.3).
- Agency anchor: RESEARCH.md §6 — deep-research integration flow.
- Import policy: [`decisions/0011-external-skill-corpora-import.md`](../../decisions/0011-external-skill-corpora-import.md).

## Compatibility

- Target agent: `claude-code` (this repo's primary surface)
- MCP servers used: none required. **Tavily**, **Sequential**, **Playwright**, **Serena** MCPs are OPTIONAL upstream dependencies; the Agency runtime uses WebSearch + WebFetch as the primary surface per ADR-0011 D.8.
- Known limitation: imported one-shot snapshot at SuperClaude_Framework `v4.3.0` — re-syncs require a new Task per ADR-0011 D.9.
