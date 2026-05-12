---
name: sc-design
description: >-
  System and component design with comprehensive specifications. Use when the user invokes /sc:design or asks for an architecture / API / component-interface design.
skill_kind: specialist
skill_target_agents: [claude-code]
skill_references_skills: [sc-implement, sc-system-architect]
skill_references_research: []
skill_references_prompts: []
skill_bootstrap_required: false
skill_source: "superclaude@v4.3.0"
---

# sc-design — `/sc:design` (imported from SuperClaude v4.3.0)

## What

Imported `/sc:design` command from SuperClaude_Framework. Produces architecture / API / component-interface specifications with explicit trade-off analysis.

## When to use

Use when the user invokes `/sc:design` or asks to "design", "spec", or "lay out" an API, data model, or component boundary before implementation.

## How to use

1. Capture the design intent (what is being designed, for whom, with what constraints).
2. Enumerate ≥ 2 candidate designs and compare on quality / cost / risk axes.
3. Pick the recommended option with a one-paragraph rationale; defer the alternatives in a `## Considered alternatives` section.
4. Hand off to `sc-implement` once the user signs off on the design.

Full behavioural specification at `references/upstream-sc-design.md`.

## References

- Upstream verbatim mirror: [`references/upstream-sc-design.md`](./references/upstream-sc-design.md) (SuperClaude_Framework `src/superclaude/commands/design.md` @ SHA `22ad3f48`, v4.3.0).
- Import policy: [`decisions/0011-external-skill-corpora-import.md`](../../decisions/0011-external-skill-corpora-import.md).

## Compatibility

- Target agent: `claude-code`.
- No MCP bindings; Agency-native tools only.
- Known limitation: one-shot snapshot at SuperClaude_Framework `v4.3.0` — re-syncs require a new Task per ADR-0011 D.9.
