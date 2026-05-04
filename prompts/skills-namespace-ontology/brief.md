# Brief: `skill_*` L2 Namespace — Value Vocabulary & Reciprocity

## Source

Follow-up question from the `skills-navigation-bootstrap` research run (2026-05-04). Corresponds to Q1 in `research/skills-navigation-bootstrap/output/SPEC.md` §7.

## Question

The `skills-navigation-bootstrap` SPEC.md proposes an L2 `skill_*` namespace (`skill_kind`, `skill_tier`, `skill_uses`, `skill_complements`, `skill_supersedes`, `skill_triggers`). The proposal specifies the keys but does not nail down:

1. The exact value vocabulary for `skill_kind` (the draft uses `meta`/`domain`/`tool`/`bootstrap`/`adapter` — is this enumeration complete?).
2. The exact value vocabulary for `skill_tier` (T1/T2/T3 — does this map cleanly onto the disclosure ladder for every host?).
3. The reciprocity rule for `skill_uses` ↔ `skill_complements` (currently warning, not error — should it be promoted?).
4. The migration path for the 14 existing skills (which already use `metadata.always_on`, prose `description`-paragraph triggers, etc.).

## Why it's blocked

The downstream Tasks 009 (root spec ratification) and 011 (JSON Schema files) cannot land without an answer to all four sub-questions.
