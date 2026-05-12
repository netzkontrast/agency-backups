---
name: sc-research
description: >-
  Deep web research with adaptive planning and intelligent search. Use when the user invokes /sc:research, asks a question beyond knowledge cutoff, or requests competitive/market/technical intelligence.
skill_kind: orchestrator
skill_target_agents: [claude-code]
skill_references_skills: [sc-deep-research-agent, prompt-optimizer, research-prompt-optimizer]
skill_references_research: []
skill_references_prompts: []
skill_bootstrap_required: false
skill_source: "superclaude@v4.3.0"
---

# sc-research — `/sc:research` (imported from SuperClaude v4.3.0)

## What

Imported `/sc:research` command from SuperClaude_Framework. Coordinates deep web research with adaptive planning and evidence-based synthesis. Body adapted per ADR-0011 D.8: **WebSearch + WebFetch are the primary surface** (see `## Compatibility` for upstream MCP notes).

## When to use

Use when the user invokes `/sc:research`, asks a question beyond the model's knowledge cutoff, or requests multi-hop investigation. Delegates execution to `sc-deep-research-agent`.

## How to use

1. **Understand** (5–10%): assess query complexity; define success criteria.
2. **Plan** (10–15%): pick a strategy — Planning-Only, Intent-Planning, or Unified (see `references/MODE_DeepResearch.md`).
3. **TodoWrite** (5%): build a 3–15-task hierarchy.
4. **Execute** (50–60%):
   - **Primary**: `WebSearch` for discovery, `WebFetch` for extraction. Batch parallel-safe queries.
   - **Multi-hop**: follow entity / concept chains up to 5 hops.
5. **Track** + **Validate** (10–15%): verify evidence chains, check source credibility, resolve contradictions.
6. **Output**: land deliverables at `/research/<slug>/output/SPEC.md` per RESEARCH.md §6.5.

The verbatim upstream body (which assumes a different MCP-server surface) is archived at `references/upstream-sc-research.md` per ADR-0011 D.8.

## References

- Upstream: [`src/superclaude/commands/research.md@22ad3f4`](https://github.com/SuperClaude-Org/SuperClaude_Framework/blob/22ad3f483a6fe6c626834e1c9a3573126644a058/src/superclaude/commands/research.md) — verbatim mirror at [`references/upstream-sc-research.md`](./references/upstream-sc-research.md) (ADR-0011 D.3).
- Agency anchor: RESEARCH.md §6 — deep-research integration flow; deliverables land at `/research/<slug>/output/SPEC.md`.
- Import policy: [`decisions/0011-external-skill-corpora-import.md`](../../decisions/0011-external-skill-corpora-import.md).
- DeepResearch mode bundle: [`references/MODE_DeepResearch.md`](./references/MODE_DeepResearch.md).

## Compatibility

- Target agent: `claude-code` (this repo's primary surface)
- MCP servers used: none required. **Tavily** MCP is OPTIONAL — when present, it MAY substitute for WebSearch/WebFetch; when absent, the built-in primitives are sufficient (ADR-0011 D.8).
- Known limitation: imported one-shot snapshot at SuperClaude_Framework `v4.3.0` — re-syncs require a new Task per ADR-0011 D.9.
