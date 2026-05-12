---
name: sc-task
description: >-
  Execute complex tasks with intelligent workflow management and delegation. Use when the user invokes /sc:task or asks to coordinate a discrete multi-step task with hierarchical breakdown and cross-session persistence.
skill_kind: orchestrator
skill_target_agents: [claude-code]
skill_references_skills: [sc-pm-agent, sc-workflow, sc-implement]
skill_references_research: []
skill_references_prompts: []
skill_bootstrap_required: false
skill_source: "superclaude@v4.3.0"
---

# sc-task — `/sc:task` (imported from SuperClaude v4.3.0)

## What

Imported `/sc:task` command from SuperClaude_Framework. Coordinates discrete, user-invoked task execution with hierarchical breakdown (Epic → Story → Task → Subtask) and quality gates. Adapted per ADR-0011 D.6/D.8: MCP-server bindings stripped; persistence is Agency-native through the `tasks/<NNN>-<slug>/` layer.

## When to use

Invoke when the user runs `/sc:task [action] [target]`, or asks to execute a discrete multi-step task that benefits from a `tasks/<NNN>-<slug>/task.md` scaffold (Goal / Context / Plan / Acceptance Criteria per TASK.md). Distinct from `/sc:pm`, which provides continuous session-level orchestration.

## How to use

1. **Analyze**: parse the request; pick a strategy — *systematic* (comprehensive), *agile* (iterative), or *enterprise* (governance).
2. **Scaffold**: create `tasks/<NNN>-<slug>/task.md` from `templates/task.md`; populate frontmatter (`type: task`, `task_status: in_progress`, `task_uses_prompts: […]`).
3. **Decompose**: use `TodoWrite` for the Epic → Story → Task → Subtask hierarchy; mirror in the task body's `## Plan`.
4. **Execute**: drive each Story with `Read` / `Edit` / `Bash`; delegate cross-cutting work to sibling skills (`sc-implement`, `sc-workflow`, `sc-research`).
5. **Validate**: walk the `## Acceptance Criteria` Gherkin scenarios; ensure `tools/check-governance.sh` passes.
6. **Stop**: mark `task_status: done` and report. Do NOT auto-continue to a next task — `/sc:task` is user-invoked and discrete (vs. `/sc:pm`).

Cross-session persistence: Agency uses `tasks/` frontmatter as the durable store; the bundled `MODE_Task_Management` mode (see below) describes the hierarchical-memory pattern from upstream for reference, but Agency artefacts are the source of truth.

## Active modes

- **MODE_Task_Management** (bundled): hierarchical Plan → Phase → Task → Todo state model with checkpointed memory. Activates automatically on `/sc:task` invocations with >3 steps or >2 directories of scope. Verbatim at [`references/mode-task-management.md`](./references/mode-task-management.md).

## Adaptations from upstream

- Stripped six MCP bindings (sequential, context7, magic, playwright, morphllm, serena) — all behaviours are Agency-native.
- Replaced `serena` cross-session memory with `tasks/<NNN>-<slug>/` frontmatter + `## Plan` body sections.
- Replaced `sequentialthinking` MCP with `Read` + `Bash(grep|find)` reasoning chains.
- Bundled `MODE_Task_Management` as `references/mode-task-management.md` per ADR-0011 D.5 (and per the Phase-1 precedent of `MODE_Orchestration` bundling into `sc-implement`).
- Removed the upstream "MCP Integration" + persona-router clauses; preserved the **CRITICAL BOUNDARIES** (user-invoked, discrete, stop-on-complete) and the strategy selector (systematic / agile / enterprise).

## References

- Upstream: [`src/superclaude/commands/task.md@22ad3f4`](https://github.com/SuperClaude-Org/SuperClaude_Framework/blob/22ad3f483a6fe6c626834e1c9a3573126644a058/src/superclaude/commands/task.md) — verbatim mirror at [`references/upstream-sc-task.md`](./references/upstream-sc-task.md) (ADR-0011 D.3).
- Bundled mode: [`references/mode-task-management.md`](./references/mode-task-management.md) (ADR-0011 D.5).
- Agency anchor: [TASK.md](../../TASK.md) — Task-layer four-section structure; [CLAUDE.md §1](../../CLAUDE.md) — separation of concerns.
- Import policy: [`decisions/0011-external-skill-corpora-import.md`](../../decisions/0011-external-skill-corpora-import.md).

## Compatibility

- Target agent: `claude-code`.
- MCP servers used: **none required**. Each upstream MCP is OPTIONAL:
  - **Sequential** — OPTIONAL; fallback: `Read` + `Bash(grep|find)` + Markdown reasoning.
  - **Context7** — OPTIONAL; fallback: `WebFetch` on official-docs URLs.
  - **Magic** — OPTIONAL; UI work falls back to `sc-frontend-architect`.
  - **Playwright** — OPTIONAL; testing falls back to `sc-quality-engineer`.
  - **Morphllm** — OPTIONAL; large-scale rewrites fall back to `Edit` + `tools/fm/edit.py`.
  - **Serena** — OPTIONAL; persistence fallback is `tasks/<NNN>-<slug>/` frontmatter.
- Known limitation: imported one-shot snapshot at SuperClaude_Framework `v4.3.0`. Re-syncs require a new Task per ADR-0011 D.9.
