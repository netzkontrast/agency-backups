# ralph-skill

## What
"Use when generating Ralph agentic-loop files (loop.sh, PROMPT_build.md, PROMPT_plan.md, AGENTS.md, IMPLEMENTATION_PLAN.md), customizing or extending an existing Ralph workflow, auditing a Ralph setup for playbook compliance, or when research-prompt-optimizer output needs conversion into Ralph specs and an implementation plan. Triggers on: ralph, ralph loop, ralph playbook, loop.sh, PROMPT_build, PROMPT_plan, AGENTS.md, IMPLEMENTATION_PLAN.md, build loop, agentic coding loop, autonomous build agent, subagent orchestration, backpressure, JTBD specs, specs from research, loop instructions, implementation loop, git worktrees parallel, context isolation agentic, incremental verification loop."

## Why here
Snapshot of the user-skill `/mnt/skills/user/ralph-skill/` from a Claude.ai
session (taken 2026-05-04). Version-controlled here so that other agents
(Claude Code, Jules, gemini-cli) can read, audit, and propose changes via PR.
The session-side copy under `/mnt/skills/user/` remains the live runtime
"upstream" until a sync-back protocol is defined.

## Top-level navigation
- [SKILL.md](./SKILL.md)
- [references/](./references/)

## Assumptions Log
- Skill-internal subfolders (e.g. `references/`, `scripts/`, `agents/`) are
  NOT given their own `readme.md`. Rationale: skills are governed by `SKILL.md`
  and Anthropic's skill-creator conventions; adding per-subfolder readmes would
  trigger "Structural Bloat" per `FRUSTRATED.md` (FL2 special-trigger). This
  drift is logged once here and once globally in the PR Frustration Log.
- The `name` and `description` shown above are extracted verbatim from
  `SKILL.md` YAML frontmatter; if the skill is updated in `/mnt/skills/user/`,
  this readme drifts until the next snapshot run.
