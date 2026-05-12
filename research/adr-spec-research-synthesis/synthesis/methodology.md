---
type: note
status: active
slug: adr-spec-research-synthesis-methodology
summary: "Methods applied during the research run: M06 (Source Triangulation), M07 (Contradiction Log), M08 (What Would Change My Mind), M13 (Adversarial Query Expansion), M12 (Base-Rate Anchoring)."
created: 2026-05-05
updated: 2026-05-05
---

# Methodology

The methods below are inherited from the originating Gemini research prompt (`research/gemini/agency-adr-governance-spec/research-prompt_agency-adr-governance-spec.md`) and re-applied against the *repo itself* rather than the external literature.

## [M06] Source Triangulation

Every finding in `workspace/analysis.md §A` and §B is confirmed in ≥ 2 source files. The triangulation matrix is recorded in [`../reflection/M06-source-triangulation.md`](../reflection/M06-source-triangulation.md).

**Why:** prevents single-source assumptions from sneaking into the spec. Especially relevant for the Frontmatter Ontology, which is described in three places (`AGENTS.md`, `TASK.md §3`, `header-ontology.json`) that historically drift.

## [M07] Contradiction Log

Conflicting conclusions between the Gemini draft and the repo's existing conventions are catalogued in [`../reflection/M07-contradictions.md`](../reflection/M07-contradictions.md). Each row carries (a) Gemini claim, (b) repo evidence, (c) resolution as adopted in `output/SPEC.md`.

**Why:** the Gemini draft is theoretically sound but repo-ungrounded; without explicit contradiction tracking, repo-violating claims would silently survive into the spec.

## [M08] What Would Change My Mind

Applied to four high-stakes claims. Each claim has its falsifier recorded in [`../reflection/M08-what-would-change-my-mind.md`](../reflection/M08-what-would-change-my-mind.md):

1. "ADRs belong at `decisions/` rather than `docs/decisions/` or `research/adr/`."
2. "The synthesis pipeline writes a guarded section, not the whole `AGENTS.md`."
3. "`tools/adr/` is the right co-location, not `tools/fm/adr.py`."
4. "Token-limit 2000 is aspirational, not strict, against the current `AGENTS.md` size."

**Why:** these are the four decisions whose reversal would force a rewrite of the spec. M08 makes the falsifier observable now, rather than discovered late by Task 028.

## [M13] Adversarial Query Expansion

Run across four axes — adjacent, opposing, abstraction, orthogonal — recorded in [`../reflection/M13-query-expansion.md`](../reflection/M13-query-expansion.md). Highlights:

- **Adjacent:** `adr-tools` and `log4brains` use sequential numbering and static-site rendering; we adopt sequential numbering (B7) but reject static-site rendering as scope creep.
- **Opposing:** the spec fails if agents never author ADRs; we mitigate via Task 029's migration recommendation seeding the corpus from implicit decisions.
- **Abstraction:** the spec rests on the principle that *normative governance can be both human-narrative and machine-extractable*; the repo culture honours this (every existing root spec is RFC 2119 + Gherkin), so the principle holds.
- **Orthogonal (MDL):** with current `AGENTS.md` ≈ 4.8 KT and a 2 KT guarded-section budget, ≈ 50 ADRs of average MDL contribution `≤ 40` tokens each fit. This is documented in §3 of the M13 file.

## [M12] Base-Rate Anchoring

Reference: per Gemini's `### Cross-Pollination Log`, MADR + `AGENTS.md` are the industry base rates for ADR + agent-instruction file conventions respectively. The repo-native spec adopts MADR's section structure (Context / Decision Outcome / Consequences) and `AGENTS.md` as the synthesis target. Departures from base rate (the guarded-section convention; the `adr_*` L2 namespace) are explicitly rationalised in `output/SPEC.md §2.3` and `§7.3`.

## Pre-Synthesis Integrity Check (M4)

Before drafting `output/SPEC.md`, the eight-item M4 check was completed:

| # | Item | Status |
|---|---|---|
| 1 | Restatement of CONSTRAINT BLOCK 0 (mandatory reflection regime) | done — see `tracks.md` |
| 2 | All five reflection checkpoints (CB0) honoured | done — see `tracks.md` |
| 3 | Every active method has at least one concrete invocation | done (M06, M07, M08, M12, M13) |
| 4 | M13 invoked on all four axes | done |
| 5 | Cross-pollination steps logged | done — `analysis.md §F`, `brainstorm.md "Cross-Pollination"` |
| 6 | Source triangulation applied | done — `M06-source-triangulation.md` |
| 7 | Contradiction log populated | done — `M07-contradictions.md` |
| 8 | Temporal scope honoured (2011-01-01 → 2026-05-05) | done |

## Friction Declaration

Highest friction experienced: **FL1** — a minor ambiguity in how the prompt instructed `/sc:analyze` to be invoked when no live `/sc:` skill is loaded in the session. Mitigation: the analysis was performed by reading the listed files directly and recording findings in `workspace/analysis.md` with the `/sc:analyze` semantics (structured tables, triangulated claims). This is documented in [`../reflection/friction-log.md`](../reflection/friction-log.md).
