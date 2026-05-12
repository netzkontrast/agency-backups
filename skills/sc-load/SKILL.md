---
name: sc-load
description: >-
  Session lifecycle management with Serena MCP integration for project context loading. Use when the user invokes /sc:load or asks to reconstruct prior task state at session start.
skill_kind: orchestrator
skill_target_agents: [claude-code]
skill_references_skills: [sc-pm-agent, sc-save]
skill_references_research: []
skill_references_prompts: []
skill_bootstrap_required: false
skill_source: "superclaude@v4.3.0"
---

# sc-load — `/sc:load` (imported from SuperClaude v4.3.0)

## What

Imported `/sc:load` command from SuperClaude_Framework. Reconstructs prior session state at the start of a new run. Body adapted per ADR-0011 D.8: **Agency's filesystem substrate (`tasks/<NNN>-*/task.md` frontmatter + `friction-log.md`) replaces Serena MCP** as the session-persistence surface.

## When to use

Use when the user invokes `/sc:load`, asks to "resume" or "continue" prior work, or when a new session needs to reconstruct task state from the repository before acting.

## How to use

1. **Identify** the target task: derive `<NNN>-<slug>` from the user request, the current branch (`claude/<slug>-<id>`), or the most recently `updated:` task under `tasks/`.
2. **Read frontmatter** of `tasks/<NNN>-<slug>/task.md` via `tools/fm/edit.py --get` or direct Read — extract `task_status`, `task_uses_prompts`, `task_spawns_research`, `updated`.
3. **Follow audit-graph edges**: for each slug in `task_uses_prompts`, Read `prompts/<slug>/prompt.md`; for each in `task_spawns_research`, Read `research/<slug>/output/SPEC.md` (if `research_phase: complete`).
4. **Read friction history**: Read prior `friction-log.md` entries (either in `research/<slug>/reflection/` or referenced from the task) to recover unresolved blockers.
5. **Summarise to the user**: report task status, open prompts, last FL declaration, and proposed next step — do NOT mutate any file during load.
6. **Hand off** to `sc-pm-agent` (or the originating skill) with the reconstructed context.

The verbatim upstream body (which assumes Serena MCP memory APIs) is archived at `references/upstream-sc-load.md` per ADR-0011 D.8.

## Adaptations from upstream

Upstream `/sc:load` mandates Serena MCP for `activate_project`, `list_memories`, and `read_memory` calls. Agency's substitution per ADR-0011 D.8: **Serena-MCP calls are replaced with Agency filesystem patterns** — `task_status` + `task_uses_prompts` frontmatter on `tasks/<NNN>-*/task.md` is the canonical source of session state; `friction-log.md` is the canonical source of cross-session learnings. No Serena calls appear in the Agency body.

## References

- Upstream: [`src/superclaude/commands/load.md@22ad3f4`](https://github.com/SuperClaude-Org/SuperClaude_Framework/blob/22ad3f483a6fe6c626834e1c9a3573126644a058/src/superclaude/commands/load.md) — verbatim mirror at [`references/upstream-sc-load.md`](./references/upstream-sc-load.md) (ADR-0011 D.3).
- Agency anchor: TASK.md §3 — `task_status` and `task_uses_prompts` frontmatter contract; FRUSTRATED.md — friction-log format.
- Import policy: [`decisions/0011-external-skill-corpora-import.md`](../../decisions/0011-external-skill-corpora-import.md) (D.8 adaptation clause).

## Compatibility

- Target agent: `claude-code` (this repo's primary surface).
- MCP servers used: none required. **Serena MCP** is OPTIONAL — when present, MAY substitute for filesystem-based session persistence; absent, Agency's `task/<NNN>/task.md` + `friction-log.md` provide equivalent capability (ADR-0011 D.8).
- Known limitation: imported one-shot snapshot at SuperClaude_Framework `v4.3.0` — re-syncs require a new Task per ADR-0011 D.9.
