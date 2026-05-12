---
type: research
status: archived
slug: skills-namespace-ontology
summary: "Ratified skill_* L2 namespace ontology: five skill_kind values, three skill_tier values, two-case reciprocity rule, 14-skill mapping table, deprecated metadata.* key map, and three-batch migration plan."
created: 2026-05-05
updated: 2026-05-12
research_phase: archived
research_executes_prompt: skills-namespace-ontology
research_friction_level: FL0
---

# /research/skills-namespace-ontology/

**What is this folder?** Execution workspace for the prompt at [`/prompts/skills-namespace-ontology/`](../../prompts/skills-namespace-ontology/). It ratifies the `skill_*` L2 namespace proposed by the `skills-navigation-bootstrap` research run.

**Why is it here?** Per `RESEARCH.md`, every research run lives in `/research/<slug>/` where the slug equals the executing prompt's slug.

## Linked Navigation

| Resource | Purpose |
|---|---|
| [prompt.md](./prompt.md) | Immutable snapshot of the executing prompt at run-start. |
| [workspace/](./workspace/) | Session log and scratch notes. |
| [synthesis/](./synthesis/) | Structured synthesis artifacts (methodology, tracks, state, merge log). |
| [reflection/](./reflection/) | Friction log (FL0) and assumption log. |
| [output/SPEC.md](./output/SPEC.md) | **Ratified output** — ontology, mapping, migration plan. |

## Executing Prompt

[`/prompts/skills-namespace-ontology/`](../../prompts/skills-namespace-ontology/) — follow-up from `skills-navigation-bootstrap`, spawned to resolve Open Question Q1 from that run.

## Key Results

1. `skill_kind` ∈ {`meta`, `domain`, `tool`, `bootstrap`, `adapter`} — five values, closed vocabulary.
2. `skill_tier` ∈ {`T1`, `T2`, `T3`} — T1 always-on (1 skill), T3 reference-heavy (2 skills), T2 default (11 skills).
3. All 14 existing skills mapped to kind + tier + uses + complements.
4. Reciprocity rule: broken target → ERROR; missing complement → WARNING.
5. Three deprecated `metadata.*` keys mapped to `skill_*` replacements.
6. Three-batch migration plan ordered by risk.

## Downstream Tasks

- [Task 009 — Author Skills Root Spec](../../tasks/009-author-skills-root-spec/) — Ratifies SKILLS.md §A.4–§A.6 using this output.
- [Task 011 — Skills Frontmatter Schema Files](../../tasks/011-skills-frontmatter-schema-files/) — Builds `l2-skill.schema.json` enum definitions from this output.

## Open Questions Surfaced

None. No new follow-up prompts were filed. Pre-existing open prompts (`skills-manifest-emission-tool`, `skills-skill-trigger-lifecycle`, `claude-ai-container-git-verification`) remain in `/prompts/` and are unaffected by this run.
