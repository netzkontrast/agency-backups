---
type: note
status: active
slug: triage-note-sc-brainstorm
summary: "Triage note for SuperClaude commands/brainstorm.md. Decision adapt (D.6 + D.8): cites sequential+morphllm+magic+playwright+context7+serena (6 MCPs). Body 5.7 KB exceeds cap. Heavy rewrite required."
created: 2026-05-12
updated: 2026-05-12
---

# Triage note — `superclaude_framework/src/superclaude/commands/brainstorm.md`

## Why `adapt` (D.6 + D.8)

The upstream body binds to **six** MCP servers (sequential, morphllm, magic, playwright, context7, serena) in its "Behavioral Flow" — the densest MCP footprint of any SC command. Agency is MCP-free per ADR-0011 D.8; verbatim port is impossible. Body also marginally over D.6 cap at 5.7 KB.

## Adaptation plan (ST-2)

1. **Strip MCP bindings.** Replace each MCP-tool reference with the equivalent Agency-native tool:
   - `sequential` → `Read` + `Bash(grep|find)` + reasoning-in-Markdown.
   - `context7` → `WebFetch` (only when the user has authorised external lookup) + `Read` on local docs.
   - `serena` → frontmatter-driven session state in `tasks/` or `research/`.
   - `morphllm`, `magic`, `playwright` → drop entirely; not relevant to brainstorming.
2. **Preserve the Socratic-discovery methodology** — the 5-phase Behavioral Flow is the core value-add; keep its phase labels and prompts.
3. **Bundle Mode reference.** Row 40 (MODE_Brainstorming) is `skip` because its content is duplicative — confirm by diffing the mode body against the command body during ST-2 and document the diff in `## Adaptations`.
4. **Body cap.** After MCP-strip, body should land ≤ 4 KB (the MCP references contribute the overflow).

## Landing folder

`skills/sc-brainstorm/` with body ≤ 5 KB. Tier L2 — depends on `sc-research` (for evidence gathering during brainstorms) and `sc-task` (for converting brainstorm output to actionable Tasks).

## Audit-graph linkage

- `skill_source: "superclaude_framework@v4.3.0"`
- `skill_references_skills: [sc-research, sc-task, sc-requirements-analyst]`
