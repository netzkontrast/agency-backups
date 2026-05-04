---
type: readme
status: active
slug: integrate-dramatica-ncp-skills
summary: "Synthesis folder — flattened evidence from the kickoff run: corpus inventory, cross-skill ID audit, scenario-tag survey, methodology, and synthesis state."
created: 2026-05-04
updated: 2026-05-04
---

# Synthesis

The kickoff produced three evidence files; together they unblock Task 013 plan steps 2–11.

## Hard results

- **Corpus is large but bounded.** 22 vocabulary files / 310 terms / 75 dynamic pairs / 512 synonym aliases; 15 theory chapters / ~1010 KB / ~2700 lines (per [`inventory.md`](./inventory.md)).
- **Three concrete cross-skill ID contradictions** must be resolved before any JSON Schema is authored (per [`id-audit.md`](./id-audit.md)):
  1. `Subjective Story` (theory) vs `Relationship` (vocab) vs `Relationship Story` (NCP) — three labels, one entity.
  2. `Impact Character` (theory + vocab) vs `Influence Character` (NCP).
  3. `Mental Sex` (theory + vocab) vs `Problem-solving Style` (NCP canonical vocabulary).
- **Scenario taxonomy is tractable.** The eleven persona scenarios (six Novel-Author, five Organist) map to bounded subsets of the term universe — typically 6–25 candidate terms per scenario, well below the per-term `scenarios: ≤8` cap (per [`scenario-survey.md`](./scenario-survey.md)).
- **Element/Type overshoot is annotation-shaped, not theory-shaped.** Vocabulary `elements.md` ships 71 entries vs canonical 64; the seven extras are *meta-entries* (Crucial Element, MC Problem, OS Problem/Response/Solution/Symptom, Symptom Element). The schema MUST distinguish `kind: element` (canonical) from `kind: concept` (meta-entry); silent merging would corrupt downstream Dynamic-Pair logic.
- **Source-vs-extension provenance is already documented.** Six vocabulary files (`dramatica-fundamentals`, `storyform-mechanics`, `element-quads`, `encoding-patterns`, `essential-questions`, `_synonym-lookup`) are explicitly marked as Extensions; the rest are Source. The schema's `provenance` field maps cleanly onto this existing distinction.

## Files

- [`methodology.md`](./methodology.md) — methods applied (M01, M07; corpus walk via Explore subagent).
- [`tracks.md`](./tracks.md) — the three evidence streams as tracks.
- [`state.md`](./state.md) — checklist of synthesis steps; all `[x]` for the kickoff phase.
- [`post-synthesis-log.md`](./post-synthesis-log.md) — chronological merge log.
- [`inventory.md`](./inventory.md) — corpus inventory.
- [`id-audit.md`](./id-audit.md) — cross-skill identifier audit.
- [`scenario-survey.md`](./scenario-survey.md) — first-pass scenario-tag survey.
