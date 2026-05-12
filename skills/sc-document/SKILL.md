---
name: sc-document
description: >-
  Generate focused documentation for components, functions, APIs, and features. Use when the user invokes /sc:document or asks for inline docs, API references, user guides, or component-level external documentation.
skill_kind: tool
skill_target_agents: [claude-code]
skill_references_skills: [sc-explain]
skill_references_research: []
skill_references_prompts: []
skill_bootstrap_required: false
skill_source: "superclaude@v4.3.0"
---

# sc-document — `/sc:document` (imported from SuperClaude v4.3.0)

## What

Imported `/sc:document` command from SuperClaude_Framework. Produces focused documentation — inline docstrings, external references, API specs, or user guides — based on target type and desired style.

## When to use

Use when the user invokes `/sc:document` or asks for inline code comments/docstrings, API reference generation, user guides, or external documentation for specific components.

## How to use

1. **Analyze** the target component's structure, interfaces, and functionality.
2. **Identify** documentation requirements and target audience.
3. **Generate** documentation content matching the chosen `--type` (inline/external/api/guide) and `--style` (brief/detailed).
4. **Format** consistently and integrate cross-references.
5. **Integrate** with the project's existing documentation ecosystem; pair with `sc-explain` when conceptual context is needed.

Full behavioural specification at `references/upstream-sc-document.md`.

## References

- Upstream: [`src/superclaude/commands/document.md@22ad3f4`](https://github.com/SuperClaude-Org/SuperClaude_Framework/blob/22ad3f483a6fe6c626834e1c9a3573126644a058/src/superclaude/commands/document.md) — verbatim mirror at [`references/upstream-sc-document.md`](./references/upstream-sc-document.md) (ADR-0011 D.3).
- Agency anchor: CLAUDE.md §13 — `/sc:*` skill invocation policy.
- Import policy: [`decisions/0011-external-skill-corpora-import.md`](../../decisions/0011-external-skill-corpora-import.md).

## Compatibility

- Target agent: `claude-code` (this repo's primary surface)
- Known limitation: one-shot snapshot at v4.3.0 — re-syncs require a new Task per ADR-0011 D.9.
