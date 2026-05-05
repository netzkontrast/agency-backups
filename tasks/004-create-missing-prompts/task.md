---
type: task
status: active
slug: create-missing-prompts
summary: "Found by coherence check 2026-05-04: Tasks 001 and 002 use prompts that do not currently exist."
created: 2026-05-04
updated: 2026-05-04
task_id: "004"
task_status: open
task_owner: "unassigned"
task_priority: P2
task_uses_prompts: []
task_spawns_research: []
task_spawns_prompts: []
task_affects_paths:
  - prompts/refactor-governance-from-specs/prompt.md
  - prompts/token-efficiency-tool-suite/prompt.md
---

# Task 004 — Create Missing Prompts for Tasks 001 & 002

## Goal
Task 001 uses `refactor-governance-from-specs` but its prompt.md is missing or invalid.
Task 002 uses `token-efficiency-tool-suite` but its prompt.md is missing or invalid.

## Plan
1. Draft prompts according to `PROMPT.md` guidelines for each of the missing files.
2. Store them in the appropriate directory structure under `/prompts/`.

## Todo
- [ ] Author `/prompts/refactor-governance-from-specs/prompt.md`.
- [ ] Author `/prompts/token-efficiency-tool-suite/prompt.md`.

## Links
- Found by: coherence check run `maintenance/run-log.md` entry 2026-05-04
