---
name: sc-implement
description: >-
  Feature and code implementation with intelligent persona activation and MCP integration. Use when the user invokes /sc:implement or asks to build, ship, or wire a feature end to end.
skill_kind: orchestrator
skill_target_agents: [claude-code]
skill_references_skills: [sc-system-architect, sc-backend-architect, sc-frontend-architect, sc-security-engineer, sc-quality-engineer]
skill_references_research: []
skill_references_prompts: []
skill_bootstrap_required: false
skill_source: "superclaude@v4.3.0"
skill_bundles_tools:
  - tools/fm
---

# sc-implement — `/sc:implement` (imported from SuperClaude v4.3.0)

## What

Imported `/sc:implement` command from SuperClaude_Framework. Coordinates architect/engineer personas to ship a feature.

## When to use

Use when the user invokes `/sc:implement` or asks to build, ship, or wire a feature end to end.

## How to use

1. Decompose the feature into back/front/security/quality slices.
2. Delegate each slice to the sibling persona skill.
3. Mutate frontmatter via `tools/fm/edit.py` (bundled) — never `sed`/`awk` per CLAUDE.md §14.6.
4. Drive the loop in Orchestration mode (see `references/MODE_Orchestration.md`).

Full behavioural specification at `references/upstream-sc-implement.md`.

## References

- Upstream: [`src/superclaude/commands/implement.md@22ad3f4`](https://github.com/SuperClaude-Org/SuperClaude_Framework/blob/22ad3f483a6fe6c626834e1c9a3573126644a058/src/superclaude/commands/implement.md) — verbatim mirror at [`references/upstream-sc-implement.md`](./references/upstream-sc-implement.md) (ADR-0011 D.3).
- Agency anchor: CLAUDE.md §13 — `/sc:*` skill invocation policy.
- Import policy: [`decisions/0011-external-skill-corpora-import.md`](../../decisions/0011-external-skill-corpora-import.md).
- Orchestration mode bundle: [`references/MODE_Orchestration.md`](./references/MODE_Orchestration.md).

## Compatibility

- Target agent: `claude-code` (this repo's primary surface)
- Known limitation: imported one-shot snapshot at SuperClaude_Framework `v4.3.0` — re-syncs require a new Task per ADR-0011 D.9.
