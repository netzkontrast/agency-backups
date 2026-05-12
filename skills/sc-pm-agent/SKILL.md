---
name: sc-pm-agent
description: >-
  Project Manager agent — coordinates SuperClaude /sc:* workflows. Use when the user invokes /sc:pm or asks to orchestrate a multi-stage delivery.
skill_kind: meta
skill_target_agents: [claude-code]
skill_references_skills: []
skill_references_research: []
skill_references_prompts: []
skill_bootstrap_required: false
skill_source: "superclaude@v4.3.0"
---

# sc-pm-agent — `/sc:pm-agent` (imported from SuperClaude v4.3.0)

## What

Imported `pm-agent` from SuperClaude_Framework. Orchestrates multi-stage Claude Code deliveries and coordinates the rest of the `/sc:*` skill set.

## When to use

Use when the user invokes `/sc:pm` or explicitly asks for a Project Manager persona to coordinate other `/sc:*` skills (implement, test, improve, research, createPR). Inert by default; Agency does not auto-load this skill at SessionStart per ADR-0011 D.7.

## How to use

1. Read the user's request and decompose into stages.
2. Delegate stages to the relevant sibling skill (e.g. `/sc:implement` for code, `/sc:test` for verification, `/sc:createPR` for closure).
3. Track progress via TodoWrite per CLAUDE.md §10 closing-run procedure.

Full upstream behavioural specification at `references/upstream-sc-pm-agent.md`.

## References

- Upstream: [`src/superclaude/agents/pm-agent.md@22ad3f4`](https://github.com/SuperClaude-Org/SuperClaude_Framework/blob/22ad3f483a6fe6c626834e1c9a3573126644a058/src/superclaude/agents/pm-agent.md) — verbatim mirror at [`references/upstream-sc-pm-agent.md`](./references/upstream-sc-pm-agent.md) (ADR-0011 D.3).
- Agency anchor: CLAUDE.md §13 — `/sc:*` skill invocation policy.
- Import policy: [`decisions/0011-external-skill-corpora-import.md`](../../decisions/0011-external-skill-corpora-import.md).

## Compatibility

- Target agent: `claude-code` (this repo's primary surface)
- Known limitation: imported one-shot snapshot at SuperClaude_Framework `v4.3.0` — re-syncs require a new Task per ADR-0011 D.9.
