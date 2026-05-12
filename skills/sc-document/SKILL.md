---
name: sc-document
description: >-
  Generate focused documentation for components, functions, APIs, and features. Use when the user invokes /sc:document or asks to "document" a specific code surface.
skill_kind: specialist
skill_target_agents: [claude-code]
skill_references_skills: [sc-explain]
skill_references_research: []
skill_references_prompts: []
skill_bootstrap_required: false
skill_source: "superclaude@v4.3.0"
---

# sc-document — `/sc:document` (imported from SuperClaude v4.3.0)

## What

Imported `/sc:document` command from SuperClaude_Framework. Produces focused documentation (READMEs, API references, function/class docstrings) for a specific code surface.

## When to use

Use when the user invokes `/sc:document` or asks to "write docs for", "document the public API of", or "add a README to" a specific module / function / package.

## How to use

1. Read the target code surface; identify its public API and invariants.
2. Pick the documentation format from the trigger (README, docstring, JSDoc, OpenAPI fragment).
3. Generate the documentation in-place; never produce a free-floating `docs.md` when an inline location exists.
4. Verify by re-reading the produced doc against the source — names, signatures, types MUST match.

Full behavioural specification at `references/upstream-sc-document.md`.

## References

- Upstream verbatim mirror: [`references/upstream-sc-document.md`](./references/upstream-sc-document.md) (SuperClaude_Framework `src/superclaude/commands/document.md` @ SHA `22ad3f48`, v4.3.0).
- Import policy: [`decisions/0011-external-skill-corpora-import.md`](../../decisions/0011-external-skill-corpora-import.md).

## Compatibility

- Target agent: `claude-code`.
- No MCP bindings; Agency-native tools only.
- Known limitation: one-shot snapshot at SuperClaude_Framework `v4.3.0` — re-syncs require a new Task per ADR-0011 D.9.
