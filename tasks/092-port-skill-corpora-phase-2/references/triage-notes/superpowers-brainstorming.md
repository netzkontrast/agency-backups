---
type: note
status: active
slug: triage-note-superpowers-brainstorming
summary: "Triage note for superpowers/skills/brainstorming/SKILL.md. Decision adapt (D.1): deconflict with sc-brainstorm and Agency's requirements-analyst pattern. Body 1.8 KB fits cleanly under D.6."
created: 2026-05-12
updated: 2026-05-12
---

# Triage note — `superpowers/skills/brainstorming/SKILL.md`

## Why `adapt` (D.1, not `port`)

Body is MCP-free and ≤ 5 KB — technically a clean `port` candidate. But it semantically overlaps **`sc-brainstorm`** (SuperClaude command, matrix row 5, adapt) and Agency's existing `sc-requirements-analyst` pattern. To avoid two near-duplicate `*-brainstorm*` skills, ST-3 MUST adapt the body to:

1. State explicitly: "This is the **Superpowers** variant — focused on **early ambiguity reduction** before plan-writing. For Socratic discovery during requirements elicitation, see `sc-brainstorm`."
2. Bind to Agency's Prompt layer (`prompts/<slug>/prompt.md`): a brainstorm session produces a Prompt, which spawns Research, which feeds back into a Task.
3. Cross-reference `superpowers-writing-plans` (matrix row 64) — brainstorm output → plan input is the upstream flow Agency preserves.

## Adaptation plan (ST-3)

1. Body verbatim with the deconfliction header inserted.
2. `## Relation to Agency native skills` section citing `sc-brainstorm`, `sc-requirements-analyst`, `superpowers-writing-plans`.
3. No `references/` extraction needed; body well under D.6.

## Landing folder

`skills/superpowers-brainstorming/SKILL.md`. Tier L2.

## Audit-graph linkage

- `skill_source: "superpowers@v4.0.3"`
- `skill_references_skills: [sc-brainstorm, sc-requirements-analyst, superpowers-writing-plans]`
