---
name: sc-workflow
description: >-
  Generate structured implementation workflows from PRDs and feature requirements. Use when the user invokes /sc:workflow or asks to turn a PRD/feature brief into a phased, dependency-aware implementation plan.
skill_kind: orchestrator
skill_target_agents: [claude-code]
skill_references_skills: [sc-task, sc-implement, sc-design]
skill_references_research: []
skill_references_prompts: []
skill_bootstrap_required: false
skill_source: "superclaude@v4.3.0"
---

# sc-workflow — `/sc:workflow` (imported from SuperClaude v4.3.0)

## What

Imported `/sc:workflow` command from SuperClaude_Framework. Reads a PRD or feature description and emits a structured implementation plan: phases, task decomposition, dependency map, validation checkpoints. Adapted per ADR-0011 D.6/D.8: the six upstream MCP bindings are dropped; the plan lands as Markdown synthesis inside the Agency Prompt → Task flow.

## When to use

Invoke when the user runs `/sc:workflow [prd-file|description]`, or asks for a phased plan from a brief. Pairs naturally with `sc-brainstorm` (upstream: requirements discovery) and `sc-task` / `sc-implement` (downstream: execution). The skill **plans only** — implementation is a separate `/sc:implement` step.

## How to use

1. **Analyze**: `Read` the PRD; extract goals, constraints, non-functional requirements.
2. **Strategy select**: pick *systematic* / *agile* / *enterprise* and a depth (`shallow` / `normal` / `deep`).
3. **Decompose**: phase the work; map dependencies; identify quality gates.
4. **Scaffold (optional)**: if the user wants execution-ready artefacts, draft a `prompts/<slug>/prompt.md` + `tasks/<NNN>-<slug>/task.md` pair per [CLAUDE.md §1](../../CLAUDE.md). Bootstrap from `templates/prompt.md` + `templates/task.md`.
5. **Track**: `TodoWrite` reflects the phase / task / subtask hierarchy; nothing is committed without user approval.
6. **Output**: a Markdown workflow plan (e.g. `claudedocs/workflow_<slug>.md` or inline in the Prompt body). The plan contains: implementation phases, task dependencies, execution order, validation steps, hand-off notes.
7. **Stop after plan creation.** Do NOT write code, run builds, or create implementation files — that is `/sc:implement`'s scope.

## Adaptations from upstream

- Stripped six MCP bindings (sequential, context7, magic, playwright, morphllm, serena) — Agency-native primitives only.
- Replaced `sequentialthinking` MCP with `Read` + Markdown reasoning chains; `serena` cross-session memory replaced by the Agency Prompt + Task layer.
- Replaced `context7` framework-pattern lookups with `WebFetch` on official-docs URLs (only when the user has authorised external retrieval).
- Re-anchored the "Plan only — no code execution" CRITICAL BOUNDARY to the Agency Task layer: the workflow plan lives in `prompts/<slug>/prompt.md` or `tasks/<NNN>-<slug>/task.md`, never in `research/` (which is for evidence).
- Removed the "MCP Integration" and "Cross-Session Workflow Management" sections; kept the strategy selector + behavioural flow.

## References

- Upstream: [`src/superclaude/commands/workflow.md@22ad3f4`](https://github.com/SuperClaude-Org/SuperClaude_Framework/blob/22ad3f483a6fe6c626834e1c9a3573126644a058/src/superclaude/commands/workflow.md) — verbatim mirror at [`references/upstream-sc-workflow.md`](./references/upstream-sc-workflow.md) (ADR-0011 D.3).
- Agency anchors: [PROMPT.md](../../PROMPT.md) (executable instruction set), [TASK.md](../../TASK.md) (Goal / Context / Plan / Acceptance Criteria), [CLAUDE.md §1](../../CLAUDE.md) (separation of concerns).
- Sibling skill: [`skills/sc-task/SKILL.md`](../sc-task/SKILL.md) — execution counterpart.
- Import policy: [`decisions/0011-external-skill-corpora-import.md`](../../decisions/0011-external-skill-corpora-import.md).

## Compatibility

- Target agent: `claude-code`.
- MCP servers used: **none required**. Each upstream MCP is OPTIONAL:
  - **Sequential** — OPTIONAL; fallback: `Read` + Markdown reasoning.
  - **Context7** — OPTIONAL; fallback: `WebFetch` on authorised official-docs URLs.
  - **Magic** — OPTIONAL; UI workflow falls back to `sc-frontend-architect` review.
  - **Playwright** — OPTIONAL; test-strategy phase falls back to `sc-quality-engineer`.
  - **Morphllm** — OPTIONAL; large-scale plan refactor falls back to `Edit` + `tools/fm/edit.py`.
  - **Serena** — OPTIONAL; cross-session continuity is `prompts/<slug>/` + `tasks/<NNN>-<slug>/` frontmatter.
- Known limitation: imported one-shot snapshot at SuperClaude_Framework `v4.3.0`. Re-syncs require a new Task per ADR-0011 D.9.
