---
type: index
status: active
slug: skills-namespace-ontology-synthesis
summary: "Structured synthesis artifacts for the skills-namespace-ontology research run."
created: 2026-05-05
updated: 2026-05-05
---

# synthesis/

Per `RESEARCH.md` §2 the synthesis layer is flat. Four tracks were run sequentially.

## Hard Results

1. **skill_kind vocabulary ratified:** {meta, domain, tool, bootstrap, adapter} — all five values from the draft confirmed; no additions or removals.
2. **skill_tier vocabulary ratified:** {T1, T2, T3} — T1 is always-on (1 skill); T3 is reference-heavy (2 skills); T2 is the default (11 skills).
3. **14 skills fully mapped** to kind, tier, uses[], complements[], and trigger_source.
4. **Reciprocity rule upgraded:** broken target → ERROR; missing complement → WARNING only. Two-case rule replaces original single-case draft.
5. **3 metadata.* keys deprecated:** `metadata.always_on`, `metadata.category`, `metadata.triggers` — replaced by `skill_tier`, `skill_kind`, `skill_triggers` respectively.
6. **11 metadata.* keys retained** (version, status, source, provenance, project-specific).
7. **3 migration batches** ordered by risk — add-only first; deprecate-and-add second; highest-risk prompt-optimizer last.

## Files

- [`methodology.md`](./methodology.md) — Methods applied (M02, M06, M07, M13).
- [`tracks.md`](./tracks.md) — Per-track work breakdown (T-VOCAB, T-MAP, T-RECIP, T-MIGRATE).
- [`state.md`](./state.md) — Checklist of synthesis steps with completion markers.
- [`post-synthesis-log.md`](./post-synthesis-log.md) — Chronological merge log (track outputs → SPEC.md sections).
