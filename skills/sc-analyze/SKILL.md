---
name: sc-analyze
description: >-
  Comprehensive code analysis across quality, security, performance, and architecture domains. Use when the user invokes /sc:analyze or asks for a static quality / security / perf / architecture audit.
skill_kind: specialist
skill_target_agents: [claude-code]
skill_references_skills: [sc-test, sc-improve, sc-refactoring-expert]
skill_references_research: []
skill_references_prompts: []
skill_bootstrap_required: false
skill_source: "superclaude@v4.3.0"
---

# sc-analyze — `/sc:analyze` (imported from SuperClaude v4.3.0)

## What

Imported `/sc:analyze` command from SuperClaude_Framework. Runs a structured audit across quality, security, performance, and architecture dimensions and produces a prioritised finding list.

## When to use

Use when the user invokes `/sc:analyze` or asks for a "code audit", "quality review", "security scan", or "architecture review" of an existing codebase.

## How to use

1. Read the target tree with Agency-native primitives (`Read`, `Glob`, `Grep`).
2. Score findings on a quality / security / performance / architecture axis.
3. Surface high-priority items first; defer cosmetic findings to a follow-up `sc:improve` invocation.
4. Cross-link related sibling skills via `skill_references_skills` (above) rather than inlining their bodies.

Full behavioural specification at `references/upstream-sc-analyze.md`.

## References

- Upstream verbatim mirror: [`references/upstream-sc-analyze.md`](./references/upstream-sc-analyze.md) (SuperClaude_Framework `src/superclaude/commands/analyze.md` @ SHA `22ad3f48`, v4.3.0).
- Import policy: [`decisions/0011-external-skill-corpora-import.md`](../../decisions/0011-external-skill-corpora-import.md).
- Agency anchor: CLAUDE.md §13 — `/sc:*` skill invocation policy.

## Compatibility

- Target agent: `claude-code`.
- No MCP bindings; Agency-native tools only.
- Known limitation: one-shot snapshot at SuperClaude_Framework `v4.3.0` — re-syncs require a new Task per ADR-0011 D.9.
