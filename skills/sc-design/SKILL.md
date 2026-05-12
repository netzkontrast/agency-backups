---
name: sc-design
description: >-
  Design system architecture, APIs, and component interfaces with comprehensive specifications. Use when the user invokes /sc:design or asks for architecture planning, API spec, component design, or database schema modelling.
skill_kind: orchestrator
skill_target_agents: [claude-code]
skill_references_skills: [sc-implement, sc-system-architect]
skill_references_research: []
skill_references_prompts: []
skill_bootstrap_required: false
skill_source: "superclaude@v4.3.0"
---

# sc-design — `/sc:design` (imported from SuperClaude v4.3.0)

## What

Imported `/sc:design` command from SuperClaude_Framework. Produces system architecture, API specifications, component interfaces, and database schemas with industry best practices baked in.

## When to use

Use when the user invokes `/sc:design` or asks for architecture planning, API specification, component interface design, or data-model/schema design — prior to any implementation work.

## How to use

1. **Analyze** target requirements and existing system context.
2. **Plan** the design approach by type (architecture/api/component/database) and format (diagram/spec/code).
3. **Design** comprehensive specifications, applying scalability and maintainability best practices.
4. **Validate** the design against constraints and existing architecture.
5. **Document** the result as diagrams, specs, or interface code.
6. Hand off to `sc-implement` (build) or `sc-system-architect` (deeper architectural framing) for execution.

Full behavioural specification at `references/upstream-sc-design.md`.

## References

- Upstream: [`src/superclaude/commands/design.md@22ad3f4`](https://github.com/SuperClaude-Org/SuperClaude_Framework/blob/22ad3f483a6fe6c626834e1c9a3573126644a058/src/superclaude/commands/design.md) — verbatim mirror at [`references/upstream-sc-design.md`](./references/upstream-sc-design.md) (ADR-0011 D.3).
- Agency anchor: CLAUDE.md §13 — `/sc:*` skill invocation policy.
- Import policy: [`decisions/0011-external-skill-corpora-import.md`](../../decisions/0011-external-skill-corpora-import.md).

## Compatibility

- Target agent: `claude-code` (this repo's primary surface)
- Known limitation: one-shot snapshot at v4.3.0 — re-syncs require a new Task per ADR-0011 D.9.
