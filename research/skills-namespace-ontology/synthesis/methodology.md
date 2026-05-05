---
type: index
status: active
slug: skills-namespace-ontology-methodology
summary: "Methods applied in the skills-namespace-ontology research run."
created: 2026-05-05
updated: 2026-05-05
---

# Methodology

## Methods Applied

### M02 — Environment Inspection
Read all 14 `skills/*/SKILL.md` frontmatter blocks and `references/` directory listings to build a ground-truth inventory of existing skill attributes and reference corpus sizes.

### M06 — Separation of Concerns
Distinguished three orthogonal design decisions: (1) value vocabulary for `skill_kind`/`skill_tier`, (2) reciprocity rule severity, (3) migration order. Treated each independently before assembling the final SPEC.md.

### M07 — Contradiction Detection
Identified a gap in the original draft's reciprocity rule: it only addressed `skill_complements` asymmetry, not broken `skill_uses` targets. Resolved by splitting the rule into two cases with different severity (error vs. warning).

### M13 — Evidence Quality Assessment
Cross-referenced three evidence sources: (a) `SPEC.md` §3.2 proposed vocabulary, (b) actual skill SKILL.md bodies, (c) `references/` directory counts. Confidence in T3 classification is high for dramatica-theory (15 ref files) and dramatica-vocabulary (18 ref files); all other T-tier assignments are inferred from body-to-reference ratio.

## Constraints Honored
- RFC 2119 keyword discipline throughout.
- No SKILL.md bodies modified.
- No nested YAML proposed.
- Reused existing namespace pattern (`task_*`, `prompt_*`, `research_*`).
