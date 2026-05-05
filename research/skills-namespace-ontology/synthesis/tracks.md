---
type: index
status: active
slug: skills-namespace-ontology-tracks
summary: "Per-track work breakdown for skills-namespace-ontology."
created: 2026-05-05
updated: 2026-05-05
---

# Tracks

## T-VOCAB — Value Vocabulary Ratification

**Goal:** Enumerate and ratify `skill_kind` and `skill_tier` allowed values.

**Work done:**
- Read `SPEC.md` §3.2 proposed values.
- Audited 14 skills against proposed values.
- Confirmed every skill maps to exactly one `skill_kind` and one `skill_tier`.
- Confirmed `bootstrap` and `adapter` values are needed (reserved; no current instances).
- Result: vocabulary ratified without additions or removals to the original draft.

## T-MAP — Skill-by-Skill Mapping

**Goal:** Produce a complete mapping table: skill → kind, tier, uses, complements.

**Work done:**
- Read each SKILL.md description for dependency signals ("routes to", "delegates to", "co-invokes", "uses").
- Identified four `skill_uses` relationships: novel-architect→{ncp-author, dramatica-theory, dramatica-vocabulary, research-prompt-optimizer, drive-markdown-converter}; ncp-author→{dramatica-theory, dramatica-vocabulary}; ralph-skill→{spec-skill}; the-agency-system-architect→{suno-lyric-writer}.
- Derived `skill_complements` as symmetric counterpart of `skill_uses`.
- Confirmed no `skill_supersedes` relationships currently exist.

## T-RECIP — Reciprocity Rule Decision

**Goal:** Finalize warning vs. error severity for reciprocity checks.

**Work done:**
- Identified the original draft conflated two distinct cases.
- Separated: broken target (error) vs. missing complement (warning).
- Documented rationale aligned with RFC 2119 MUST vs. SHOULD distinction.

## T-MIGRATE — Migration Plan

**Goal:** Plan metadata.* deprecation and trigger lifting; order batches.

**Work done:**
- Surveyed all `metadata.*` sub-keys across 14 SKILL.md files.
- Mapped deprecated keys to skill_* replacements.
- Identified keys to retain (version, status, source, provenance keys).
- Batched into three groups by risk and change type.
