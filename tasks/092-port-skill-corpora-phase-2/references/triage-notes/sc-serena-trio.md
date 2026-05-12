---
type: note
status: active
slug: triage-note-sc-serena-trio
summary: "Combined triage note for the three Serena-MCP-bound SC commands: load.md, save.md, reflect.md. All three adapt per D.8 by rewriting Serena session-persistence to Agency frontmatter + filesystem patterns."
created: 2026-05-12
updated: 2026-05-12
---

# Triage note — Serena-bound trio (`load`, `save`, `reflect`)

Three SC commands bind exclusively to **Serena MCP** for session persistence and project context. Agency MUST adapt each per ADR-0011 D.8 by replacing Serena calls with Agency's existing filesystem-based session model.

## Files

| Snapshot path | Upstream intent | Agency replacement |
|---|---|---|
| `commands/load.md` | "Initialize Serena MCP connection and session context" | Read `tasks/<NNN>-*/task.md` frontmatter + `friction-log.md`; reconstruct task state from `task_status` + `task_uses_prompts`. |
| `commands/save.md` | "Persist session context via Serena memory" | Update `tasks/<NNN>-*/task.md` `updated:`, append to `friction-log.md`, commit via Bash. |
| `commands/reflect.md` | "Task reflection via Serena memory analysis" | Use TodoWrite + frontmatter-driven `task_status` review; read `friction-log.md` and prior `task_status` transitions. |

## Adaptation plan (ST-2)

1. Each SKILL.md gets its own `skills/sc-<load|save|reflect>/` folder.
2. Body content: strip all Serena references; replace with the Agency-native pattern in the table above. Each body ≤ 3 KB (no `references/` extraction needed).
3. Cross-reference `sc-pm-agent` (already ported in Phase 1) — the PM agent already orchestrates these patterns.
4. Document the substitution explicitly in each SKILL.md's `## Adaptations from upstream` section so downstream agents understand why Serena does not appear.

## Tier

L2 for all three — they depend on the Task / Prompt / Research substrate to read.

## Audit-graph linkage

- `skill_source: "superclaude@v4.3.0"` per file.
- `skill_references_skills: [sc-pm-agent]` per file.
- Optional: `sc-load` ↔ `sc-save` reciprocal `skill_references_skills` edge.
