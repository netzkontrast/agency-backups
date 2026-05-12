---
name: sc-save
description: >-
  Session lifecycle management with Serena MCP integration for session context persistence. Use when the user invokes /sc:save or asks to checkpoint session state before ending a run.
skill_kind: orchestrator
skill_target_agents: [claude-code]
skill_references_skills: [sc-pm-agent, sc-load]
skill_references_research: []
skill_references_prompts: []
skill_bootstrap_required: false
skill_source: "superclaude@v4.3.0"
---

# sc-save — `/sc:save` (imported from SuperClaude v4.3.0)

## What

Imported `/sc:save` command from SuperClaude_Framework. Persists session state at run completion so the next session's `/sc:load` can reconstruct it. Body adapted per ADR-0011 D.8: **frontmatter mutation + friction-log append + git commit** replace Serena MCP memory writes.

## When to use

Use when the user invokes `/sc:save`, asks to "checkpoint" or "stash" progress, or at the end of any session that produced state worth preserving (status transitions, FL≥1 friction, partial deliverables).

## How to use

1. **Identify** the active task slug from the working branch or most recent `tasks/<NNN>-*/task.md` write.
2. **Mutate `task_status` / `updated`** via `tools/fm/edit.py --set task_status=<new> --set updated=<ISO>` per CLAUDE.md §14.6 — never `sed`/`awk`. New status follows TASK.md §3 transition rules.
3. **Append friction-log**: write a `Highest Frustration Level: FL[0-3]` block to `research/<slug>/reflection/friction-log.md` (research runs) or to the commit-message `## Frustration Log` section (standard tasks) per FRUSTRATED.md.
4. **Sync the index**: if `task_status` changed, regenerate `tasks/readme.md` via `tools/fm/index_diff.py`.
5. **Commit by name**: `git add` the touched files explicitly (no `-A`), then create a NEW commit (never `--amend`) per CLAUDE.md §11.
6. **Hand off** to `sc-load` (next session) or `sc-createPR` (closing-run step 4) as appropriate.

The verbatim upstream body (which assumes Serena MCP `write_memory` APIs) is archived at `references/upstream-sc-save.md` per ADR-0011 D.8.

## Adaptations from upstream

Upstream `/sc:save` mandates Serena MCP for `write_memory`, `read_memory`, and `summarize_changes`. Agency's substitution per ADR-0011 D.8: **Serena-MCP calls are replaced with Agency filesystem patterns** — frontmatter `updated:` bumps via `tools/fm/edit.py` provide the durable checkpoint; `friction-log.md` provides the cross-session learning archive; git commits provide the recovery checkpoint. No Serena calls appear in the Agency body.

## References

- Upstream: [`src/superclaude/commands/save.md@22ad3f4`](https://github.com/SuperClaude-Org/SuperClaude_Framework/blob/22ad3f483a6fe6c626834e1c9a3573126644a058/src/superclaude/commands/save.md) — verbatim mirror at [`references/upstream-sc-save.md`](./references/upstream-sc-save.md) (ADR-0011 D.3).
- Agency anchor: TASK.md §3 — `task_status` transitions; FRUSTRATED.md — friction-log format; CLAUDE.md §14.6 — `tools/fm/edit.py` mutation rule; CLAUDE.md §11 — branch & commit conventions.
- Import policy: [`decisions/0011-external-skill-corpora-import.md`](../../decisions/0011-external-skill-corpora-import.md) (D.8 adaptation clause).

## Compatibility

- Target agent: `claude-code` (this repo's primary surface).
- MCP servers used: none required. **Serena MCP** is OPTIONAL — when present, MAY substitute for filesystem-based session persistence; absent, Agency's `task/<NNN>/task.md` + `friction-log.md` provide equivalent capability (ADR-0011 D.8).
- Known limitation: imported one-shot snapshot at SuperClaude_Framework `v4.3.0` — re-syncs require a new Task per ADR-0011 D.9.
