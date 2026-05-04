# Corpus Inventory

Walk of `skills/dramatica-vocabulary/references/*.md` (22 files) and `skills/dramatica-theory/references/*.md` (15 files). Counts per file are heading-level (`## <Term>` for vocabulary; chapter headings for theory).

## Dramatica Vocabulary — 22 files / 310 distinct terms / 75 dynamic pairs / 512 synonym aliases

| File | Terms | Primary kind | Provenance | Notes |
|---|---:|---|---|---|
| **Core semantic units** | | | | |
| `elements.md` | 71 | element + concept | source-original | Canonical 64 + 7 meta-entries (Crucial Element, MC Problem, OS Problem/Response/Solution/Symptom, Symptom Element, Focus). Schema MUST distinguish. |
| `types.md` | 41 | type + concept | source-original | Canonical 16 Types + 25 type-related concepts. Same `kind` separation needed. |
| `variations.md` | 64 | variation | source-original | Matches canonical 64 cleanly. |
| `archetypes.md` | 9 | archetype | source-original | 8 canonical archetypes + 1 meta-entry ("Archetype" itself). |
| **Character dynamics** | | | | |
| `character-dynamics.md` | 12 | character-dynamic | source-original | Includes Resolve, Growth, Approach, Mental Sex; **Resolve entry is empty** (gap filled by `dramatica-fundamentals.md`). |
| `character-appreciations.md` | 3 | character-frame | source-original | Higher-order character categories. |
| `overview-appreciations.md` | 18 | story-level appreciation | source-original | Story-wide structural appreciations (Goal, Outcome, etc.). |
| `main-vs-impact-character.md` | 2 | character-relation | source-original | MC↔IC relationship specifics. |
| **Plot dynamics & structure** | | | | |
| `plot-dynamics.md` | 13 | plot-dynamic | source-original | Driver, Limit, Outcome, Judgment + variants. |
| `plot-structures.md` | 3 | structural-term | source-original | Plot patterns. |
| **Concept & meta-language** | | | | |
| `structural-terms.md` | 16 | structural-term | source-original | Act, Signpost, Journey, Quad. |
| `dramatica-definitions.md` | 4 | dramatica-term | source-original | Foundational meta. |
| `dramatica-fundamentals.md` | 4 | dramatica-term | extension-derived | Fills source gaps: Universe + Mind as Class, Resolve substantive, Linear/Holistic. |
| `dramatica-terms.md` | 6 | dramatica-term | source-original | Theme, Vocabulary Item etc. |
| `dynamic-terms.md` | 7 | dynamic-pair | source-original | Theory-internal dynamics. |
| **Supporting ref & encoding** | | | | |
| `element-quads.md` | 5 | structural-term | extension-derived | Lists the 16 Element-Quads (absent from source). |
| `encoding-patterns.md` | 6 | storytelling-term | extension-derived | Casablanca + Star Wars worked examples. |
| `essential-questions.md` | 8 | concept | extension-derived | The ~14 Storyform-aufbau questions in workflow order. |
| `storyform-mechanics.md` | 5 | concept | extension-derived | Distribution rules, MC↔IC diametrality, Type-sequences. |
| `storytelling.md` | 6 | storytelling-term | source-original | Storyform↔Storytelling layer. |
| `classes.md` | 4 | class | source-original | Class entries — **Universe + Mind missing here**, supplied by `dramatica-fundamentals.md`. |
| `domains.md` | 3 | class | source-original | Throughline-domain definitions. |
| **Semantic indexes** | | | | |
| `_synonym-lookup.md` | 512 rows | alias-index | source-original | EN-only flat alias index; per-locale extension required for schema's `aliases.de`. |
| `dynamic-pairs-index.md` | 75 pairs | reciprocal-pair-index | source-original | Mixes hierarchy levels (Element-pairs adjacent to Variation-pairs); the SKILL.md notes encoding work is better served by `element-quads.md`. |

**Vocabulary totals:** 310 distinct term entries · 75 reciprocal pairs · 512 synonym aliases · 6 of 22 files marked `extension-derived`.

## Dramatica Theory — 15 chapters / ~1010 KB / ~2700 lines

| File | Size | Chapter focus | Concept scope |
|---|---:|---|---|
| `00-storyform-validation.md` | 8.2 KB | Validation checklist | structural-validation |
| `00-storyform-worksheet.md` | 7.3 KB | Decision template | storyform-framework |
| `01-foundations.md` | 15 KB | Story Mind & throughlines; Star Wars + *Mockingbird* worked | meta-architecture |
| `02-characters.md` | 99 KB | Archetypes, character dimensions, Driver/Passenger | all-8-archetypes + growth-axis |
| `03-deep-theory.md` | 30 KB | Justification, problem-solving structure | philosophical-grounding |
| `04-theme.md` | 74 KB | Concerns/Issues/Problems hierarchy | thematic-structure |
| `05-plot-genre.md` | 60 KB | Acts, Sequences, Scenes, Events, Genre | narrative-hierarchy |
| `06-storyforming.md` | 107 KB | Character + Plot Dynamics, story points, Crucial Element | all-dynamics + decision-logic |
| `07-storyencoding.md` | 78 KB | Encoding archetypes, Mental Sex, Signposts + Journeys | craft-binding |
| `08-storyweaving-reception.md` | 96 KB | Storyweaving + audience | audience-integration |
| `09-reference.md` | 296 KB | Glossary + canonical lists (16 Types / 64 Variations / 64 Elements) | complete-reference |
| `10-decision-heuristics.md` | 11 KB | Decision support for hard choices | author-guidance |
| `11-anti-patterns.md` | 12 KB | 14 named anti-patterns | error-prevention |
| `12-scene-level-bridge.md` | 7.5 KB | Storyform→scene translation | craft-bridge |
| `13-worked-storyforms.md` | 7.7 KB | Star Wars + *Mockingbird* worked storyforms | case-reference |

**Theory totals:** 15 chapters · ~1010 KB raw text · ~2700 lines.

## Numbers that drive the schema

| Metric | Value | Implication |
|---|---:|---|
| Total ontology entries needed (canonical only) | ≈ 140 | 4 Classes + 16 Types + 64 Variations + 64 Elements + 8 Archetypes + 4 character-dynamics + 4 plot-dynamics + 8 storypoints + 4 throughlines (rounded) |
| Meta-entries needing `kind: concept` | ≈ 35 | Crucial Element, Symptom, Focus, Direction, Solution, etc. — atop the canonical 140 |
| Provenance distribution | 16 source / 6 extension (vocab files) | Drives `provenance` enum split |
| Scenario tags allocatable | 11 categorical | 6 novel + 5 lyric scenarios from `task.md` |
| Frontmatter blocks to write (Plan step 6) | 310 | One per term entry; bootstrap helper required (Plan step 5) |

## Contradictions found while walking the corpus

(Detail in [`id-audit.md`](./id-audit.md). Surfaced here as a heads-up.)

- **Element/Type overshoot is meta-entries, not theory drift.** Vocab `elements.md` carries 7 entries beyond the canonical 64; vocab `types.md` carries 25 entries beyond the canonical 16. All extras are concept-class meta-entries about specific structural slots (e.g. "Crucial Element" is itself a *concept about* Elements, not an Element).
- **Resolve / Universe / Mind gaps are documented and patched.** Source `character-dynamics.md` carries an empty Resolve entry; source `classes.md` lists only 2 of the 4 Classes. The Extension files (`dramatica-fundamentals.md`) supply the missing definitions — already declared in the vocab SKILL.md's "Wenn Source-File und Extension-File widersprechen" rule. Schema's `provenance` field will encode the resolution.
- **Synonym index is EN-only.** 512 rows, all English. Schema MUST allow `aliases.de` so the DE→canonical lookup the user runs is symmetric to EN.

## Source

The corpus comes from Phillips & Huntley, *Dramatica: A New Theory of Story* (4th ed., 2001, Screenplay Systems Inc.). The walk does not reproduce source prose — only file-level structure.
