---
type: index
status: active
slug: sc-task
summary: "Directory index for the imported `/sc:task` skill (SuperClaude_Framework v4.3.0). Verbatim upstream archived in `references/`; Agency adaptations live in `SKILL.md`. Bundles MODE_Task_Management."
created: 2026-05-12
updated: 2026-05-12
---

# `skills/sc-task/`

**What:** Executes discrete, user-invoked multi-step tasks with hierarchical breakdown (Epic → Story → Task → Subtask) bound to Agency's `tasks/<NNN>-<slug>/` layer. Bundles `MODE_Task_Management` as a behavioural overlay.

**Why here:** Imported under [Task 092](../../tasks/092-port-skill-corpora-phase-2/task.md) ST-2 (heavy-adapt cluster A) per the policy ratified in [ADR-0011](../../decisions/0011-external-skill-corpora-import.md). Vendor-prefixed (`sc-`) folder per D.1; `skill_source: "superclaude@v4.3.0"` pin per D.2; SHA-pinned upstream citation per D.3 (mirror at `references/upstream-sc-task.md`, snapshot SHA `22ad3f48`). Body extraction per D.6 — six upstream MCP bindings stripped, persistence rebound to the Agency Task layer.

## Contents

- [`SKILL.md`](./SKILL.md) — Agency-facing skill body (Anthropic `name`+`description` frontmatter + Agency L2 keys).
- [`references/upstream-sc-task.md`](./references/upstream-sc-task.md) — Verbatim mirror of `src/superclaude/commands/task.md` from upstream at SHA `22ad3f48`. **Do not edit** — re-syncs require a new Task per ADR-0011 D.9.
- [`references/mode-task-management.md`](./references/mode-task-management.md) — verbatim mirror of upstream `MODE_Task_Management.md`, bundled per ADR-0011 D.5. Activates automatically on `/sc:task` invocations matching its hierarchical-state triggers.

## Assumptions Log

- The upstream "Serena MCP" cross-session persistence pattern is satisfied by `tasks/<NNN>-<slug>/` frontmatter + `## Plan` body sections; no external memory store is required.
- `/sc:task` is **user-invoked and discrete** (vs. `/sc:pm`'s continuous orchestration); the skill MUST stop on task completion and not auto-advance.
- The bundled `MODE_Task_Management` references upstream MCP tools (Sequential, Magic, Playwright, Context7) in its Tool Selection table; those references remain verbatim per D.5, but the host skill's `## How to use` is MCP-free.
