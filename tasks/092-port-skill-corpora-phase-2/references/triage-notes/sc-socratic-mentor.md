---
type: note
status: active
slug: triage-note-sc-socratic-mentor
summary: "Triage note for SuperClaude agents/socratic-mentor.md. Decision adapt (D.6 + D.8): 12 KB body cites curated book corpus and binds to Sequential MCP. Extract book corpus to references/."
created: 2026-05-12
updated: 2026-05-12
---

# Triage note — `superclaude_framework/src/superclaude/agents/socratic-mentor.md`

## Why `adapt` (D.6 + D.8)

- 12.1 KB body — 2.4× D.6 cap.
- Cites Sequential MCP for multi-turn reasoning.
- Includes a curated **book corpus** (canonical programming texts referenced by the mentor when teaching) — natural extraction candidate per D.6.

## Adaptation plan (ST-3 sibling, listed under SC agents)

1. **SKILL.md body** ≤ 4 KB:
   - Socratic-method discipline.
   - Question-strategy heuristics.
   - `## Adaptations from upstream` section noting Sequential strip + book-corpus extraction.
2. **Extract book corpus** to `skills/sc-socratic-mentor/references/canonical-texts.md` — one `## <Book title>` heading per text, with the upstream commentary verbatim.
3. **Strip Sequential references.** Replace with native chain-of-thought-in-Markdown patterns.
4. Cross-reference Agency's `sc-learning-guide` (row 28, decision `port`): both are educational agents, but socratic-mentor is **discovery-driven** while learning-guide is **progression-driven**. Document the distinction in each SKILL.md.

## Landing folder

`skills/sc-socratic-mentor/SKILL.md` + `skills/sc-socratic-mentor/references/canonical-texts.md`. Tier L2.

## Audit-graph linkage

- `skill_source: "superclaude@v4.3.0"`
- `skill_references_skills: [sc-learning-guide, sc-explain]`
