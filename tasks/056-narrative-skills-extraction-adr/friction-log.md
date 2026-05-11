---
type: note
status: active
slug: 056-narrative-skills-extraction-adr-friction
summary: "Friction log for Task 056 closure. Highest Frustration Level: FL1."
created: 2026-05-11
updated: 2026-05-11
---

# Task 056 — Friction Log

Highest Frustration Level: FL1

## Summary

Decision-class ADR landed at `Proposed` with five falsifier triggers. One friction item worth recording: the ADR summary-field 240-character cap is not documented in the ADR authoring instructions at `decisions/readme.md` §"Authoring an ADR", which made the cap discoverable only via a validation failure rather than upfront.

## Entries

- **FL1 — ADR summary 240-char cap not surfaced in authoring instructions.** Authored the ADR with a 390-character summary describing all six skills by name; `tools/adr/cli.py validate` failed with `ADR.A.2.2:frontmatter schema violation at summary: ... is too long`. The constraint lives in `maintenance/schemas/l2-adr.schema.json:23` (`maxLength: 240`) and in `maintenance/schemas/header-ontology.json:173`, but neither `decisions/readme.md` nor the ADR template at `templates/` mentions the cap. Resolved by trimming twice (390 → 243 → 213 chars). Suggested follow-up: add a one-line note to `decisions/readme.md` §"Authoring an ADR" that the `summary` field MUST be ≤ 240 chars (and ideally surface the cap from the schema rather than hardcoding it).

- **FL0 — Inventory mechanically derivable.** Footprint quantification (file counts, sizes, line counts of narrative sections in the four root specs) was a few `find` + `du` + `grep -c` invocations; no agent guesswork required.

- **FL0 — Decision was clear once the cost surface was measured.** The 4 % bootstrap token cost + zero migration cost + mechanical NO.5 enforcement combined to make status-quo the rational choice without ambiguity. The five falsifier triggers exist precisely so the decision is *revisitable* under evidence rather than locked.
