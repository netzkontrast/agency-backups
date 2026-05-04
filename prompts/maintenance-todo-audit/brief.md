---
type: note
status: active
slug: maintenance-todo-audit-brief
summary: "Context: MAINTENANCE.md §3 references /todo/ which contradicts FOLDERS.md §7."
created: 2026-05-04
updated: 2026-05-04
---

# Brief

## Context

During the `superclaude-integration-spec` research run (2026-05-04), a structural contradiction was identified:

- `MAINTENANCE.md §3` instructs maintenance agents to place delegation prompts in `/todo/` (e.g., `/todo/fix-api-rate-limits/prompt.md`).
- `FOLDERS.md §7` explicitly states: "MUST NOT create operational folders outside `/tasks/`, `/prompts/`, `/research/`."

The research run corrected this in the updated `MAINTENANCE.md §3` (reference changed to `/prompts/`), but a full audit has not been conducted to ensure no other `/todo/` references remain.

## Spawned From

Research run: `superclaude-integration-spec`
