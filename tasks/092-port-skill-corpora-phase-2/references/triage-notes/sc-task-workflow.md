---
type: note
status: active
slug: triage-note-sc-task-workflow
summary: "Combined triage note for SuperClaude commands/task.md + commands/workflow.md. Both bind to 6 MCPs (sequential+context7+magic+playwright+morphllm+serena); decision adapt (D.6 + D.8). Heavy rewrites for Agency's native Task layer."
created: 2026-05-12
updated: 2026-05-12
---

# Triage note — `sc-task` + `sc-workflow` (heavy MCP commands)

Both upstream commands list the **same six MCP servers** (sequential, context7, magic, playwright, morphllm, serena) as bindings. Adaptation strategy is shared — they differ only in entry point.

## Files

| Snapshot path | Upstream intent | Agency adaptation |
|---|---|---|
| `commands/task.md` (4.9 KB) | Execute complex tasks with intelligent workflow management | Map to Agency Task layer: every task body becomes a `tasks/<NNN>-<slug>/task.md` with frontmatter-driven state. |
| `commands/workflow.md` (5.2 KB) | Generate structured implementation workflows from PRDs | Map to Agency Prompt + Task flow: `/prompts/<slug>/prompt.md` produces a Task scaffold. |

## Adaptation plan (ST-2)

1. **Strip all 6 MCP bindings** in both bodies.
2. **Bind to Agency's existing layer specs:**
   - `sc-task` body MUST cite `TASK.md` and the `tasks/<NNN>-*/task.md` four-section structure (Goal / Context / Plan / Acceptance Criteria).
   - `sc-workflow` body MUST cite `PROMPT.md` + `TASK.md` and the prompt-spawns-research-spawns-task flow from `CLAUDE.md §1`.
3. **MODE_Task_Management bundling.** Row 39 (port `MODE_Task_Management` as bundle) lands as `skills/sc-task/references/mode-task-management.md`. Body ≤ 4 KB references/.
4. **Body cap.** Each SKILL.md body ≤ 4 KB after MCP-strip + Agency-layer-binding rewrites.

## Landing folders

- `skills/sc-task/SKILL.md` + `skills/sc-task/references/mode-task-management.md`. Tier L3.
- `skills/sc-workflow/SKILL.md`. Tier L3.

## Audit-graph linkage

- `skill_source: "superclaude@v4.3.0"` per file.
- `skill_references_skills`:
  - `sc-task`: `[sc-pm-agent, sc-implement, sc-research]`.
  - `sc-workflow`: `[sc-task, sc-brainstorm, sc-implement]`.
