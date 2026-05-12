---
name: sc-explain
description: "Provide clear explanations of code, concepts, and system behavior with educational clarity"
skill_kind: analysis
skill_target_agents: [claude-code]
skill_references_skills: [sc-document, sc-learning-guide]
skill_references_research: []
skill_references_prompts: []
skill_bootstrap_required: false
skill_source: "superclaude@v4.3.0"
---

# sc-explain — `/sc:explain` (imported from SuperClaude v4.3.0)

## What

Imported `/sc:explain` command from SuperClaude_Framework. Produces clear, audience-calibrated explanations of code, concepts, or system behaviour, with progressive complexity (basic → intermediate → advanced) and educational framing. Body adapted per ADR-0011 D.8: **`Read` + native chain-of-thought + `WebFetch` are the primary surface** (see `## Compatibility` for upstream MCP notes).

## When to use

Use when the user invokes `/sc:explain`, asks "how does X work?", requests a walkthrough of unfamiliar code, or needs an educational decomposition of a framework concept or architecture. Hand off to `sc-document` for durable artifact generation and to `sc-learning-guide` for structured curriculum-style learning paths.

## When NOT to use

Do NOT use to perform implementation, refactoring, or fixes — explanation only. Do NOT fabricate framework behaviour: when authority matters, cite via `WebFetch` against the official documentation URL.

## How to use

1. **Analyse**: `Read` the target file(s) or concept anchor. `Grep` for related call-sites or definitions to build a complete mental model before explaining.
2. **Assess audience**: pick a level — `basic`, `intermediate`, or `advanced` — based on the user's request and any cues in the prompt. Adjust vocabulary, depth, and assumed prerequisites accordingly.
3. **Structure**: plan the explanation sequence — start from the user's likely entry point, layer complexity progressively, and surface a concrete example before abstracting.
4. **Generate**: write the explanation using native chain-of-thought. For framework-specific accuracy (React hooks, Django ORM, Kubernetes controllers, etc.), use `WebFetch` against the official documentation URL the user provides or the project pins.
5. **Validate**: re-read the explanation against the source code or spec — flag any inference you cannot ground in the read material. Surface explicit unknowns rather than guessing.

## Adaptations from upstream

- **Dropped MCP bindings**: `sequential` and `context7` (D.8). The "Sequential MCP for complex multi-component analysis" loop collapses to native chain-of-thought over `Read`/`Grep` output; "Context7 MCP for framework documentation" becomes `WebFetch` against the official URL plus inline knowledge.
- Multi-persona coordination (educator / architect / security) survives as inline lenses applied during step 3 structuring — pick the lens that matches the user's domain question.
- All Triggers, Boundaries, and Will/Will-Not clauses are preserved.

## References

- Upstream: [`src/superclaude/commands/explain.md@22ad3f4`](https://github.com/SuperClaude-Org/SuperClaude_Framework/blob/22ad3f483a6fe6c626834e1c9a3573126644a058/src/superclaude/commands/explain.md) — verbatim mirror at [`references/upstream-sc-explain.md`](./references/upstream-sc-explain.md) (ADR-0011 D.3).
- Import policy: [`decisions/0011-external-skill-corpora-import.md`](../../decisions/0011-external-skill-corpora-import.md) §D.8.
- Companion skills: [`skills/sc-document`](../sc-document/SKILL.md), [`skills/sc-learning-guide`](../sc-learning-guide/SKILL.md).

## Compatibility

- Target agent: `claude-code` (this repo's primary surface).
- MCP servers used: **none required**.
- **Sequential MCP** is OPTIONAL — when present, MAY substitute for the native chain-of-thought used in `How to use` steps 1 and 3–4 (multi-component analysis and progressive structuring); when absent, native reasoning is sufficient (ADR-0011 D.8).
- **Context7 MCP** is OPTIONAL — when present, MAY substitute for the `WebFetch` lookup in step 4 against official framework docs; when absent, `WebFetch` plus inline knowledge is sufficient (ADR-0011 D.8).
- Known limitation: imported one-shot snapshot at SuperClaude_Framework `v4.3.0` — re-syncs require a new Task per ADR-0011 D.9.
