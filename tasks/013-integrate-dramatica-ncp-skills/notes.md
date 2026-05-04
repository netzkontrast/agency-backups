# Task 013 — Notes

> Running scratchpad for the dramatica × NCP × novel-architect ontology integration. Per the executing prompt's Step 0, this file is authored before any other file edit and grows in three sections as the run proceeds.

## ReAct Trace

<!-- One bullet per Reason → Act → Observe iteration. Format:
- **R:** what I'm about to do and why.
- **A:** what I did (file/tool).
- **O:** what came back / what I learned. -->

- **R:** Compress context and start the prompt; need notes.md skeleton before any schema work per Step 0.
- **A:** Wrote `tasks/013-integrate-dramatica-ncp-skills/notes.md` with three skeleton sections.
- **O:** File present; downstream steps will populate.

- **R:** Step 1 needs a per-term inventory of all 22 vocab files; doing this in main context would burn ~30K tokens and is read-only — perfect for an Explore subagent.
- **A:** Dispatched Explore subagent with the per-file kind heuristic baked into the brief. Subagent returned aggregate stats (293 rows) but disagreed with the kickoff (310) by 17.
- **O:** 17-row drift exceeds the ±5 tolerance — MUST verify before continuing per prompt Step 1. Re-counted in main context with `grep -c '^## '` per file: total 333 `##` headings, of which 23 are alphabetical buckets in `_synonym-lookup.md` and 0 in `dynamic-pairs-index.md` (table-shaped). True term count = **333 − 23 − 0 = 310**, exactly matching kickoff. Subagent had double-excluded one of the index files plus over-pruned. Drift verdict: **none**. Gate passes.

- **R:** Step 1 gate passed; per-term kind classification is deferred to Step 4 (ontology bootstrap) where it materially affects output. Burning tokens on a 310-row classification table here is wasteful.
- **A:** Recorded the per-file count table in § Inventory Cross-Check; left per-term kind blank with a pointer.
- **O:** Step 1 satisfied. Moving to Step 2.

- **R:** Step 2 needs four JSON Schemas. Author all four plus the readme in parallel since they're decisions, not retrieval. After authoring, `pip install jsonschema` and run `Draft202012Validator.check_schema()` on each, plus 11 fixture cases.
- **A:** Wrote `maintenance/schemas/narrative-ontology/{ontology,term-frontmatter,scenarios,theory-chunk}.schema.json` + `readme.md`. Authored 4 `allOf` cross-field invariant rules per the prompt's OQ-C resolution. Added `kind: throughline` to the enum (D-1).
- **O:** All four schemas valid Draft 2020-12; 11/11 fixture cases pass (3 positive, 8 negative). Line counts well under 200 cap (152/82/56/61). Step 2 complete.

## Inventory Cross-Check

Method: `grep -c '^## ' <file>` across `skills/dramatica-vocabulary/references/*.md` (22 files), executed 2026-05-04 in main context. Per-file term-level heading counts:

| File | `##` count | Counted as terms? | Notes |
|---|---:|:---:|---|
| `archetypes.md` | 9 | ✓ | 8 canonical archetypes + "Archetype" meta-entry |
| `character-appreciations.md` | 3 | ✓ | |
| `character-dynamics.md` | 12 | ✓ | Includes empty Resolve entry (gap filled by `dramatica-fundamentals.md`) |
| `classes.md` | 4 | ✓ | |
| `domains.md` | 3 | ✓ | |
| `dramatica-definitions.md` | 4 | ✓ | |
| `dramatica-fundamentals.md` | 4 | ✓ | extension-derived |
| `dramatica-terms.md` | 6 | ✓ | |
| `dynamic-terms.md` | 7 | ✓ | |
| `element-quads.md` | 5 | ✓ | extension-derived |
| `elements.md` | 71 | ✓ | 64 canonical + 7 concept meta-entries |
| `encoding-patterns.md` | 6 | ✓ | extension-derived |
| `essential-questions.md` | 8 | ✓ | extension-derived |
| `main-vs-impact-character.md` | 2 | ✓ | |
| `overview-appreciations.md` | 18 | ✓ | |
| `plot-dynamics.md` | 13 | ✓ | |
| `plot-structures.md` | 3 | ✓ | |
| `storyform-mechanics.md` | 5 | ✓ | extension-derived |
| `storytelling.md` | 6 | ✓ | |
| `structural-terms.md` | 16 | ✓ | |
| `types.md` | 41 | ✓ | 16 canonical + 25 concept meta-entries |
| `variations.md` | 64 | ✓ | matches canonical 64 cleanly |
| **Subtotal — term-level headings** | **310** | | |
| `_synonym-lookup.md` | 23 | ✗ | alphabetical buckets, not terms |
| `dynamic-pairs-index.md` | 0 | ✗ | uses different structure (table) |
| **Total `##` headings, all files** | **333** | | |

### Cross-check against kickoff numbers

| Source | Term-level count | Delta | Verdict |
|---|---:|---:|---|
| Kickoff `synthesis/inventory.md` total | 310 | — | baseline |
| This run | 310 | 0 | **gate passes (±5 tolerance)** |

### Auxiliary indexes (not counted as terms but in scope for the navigator)

- `_synonym-lookup.md` carries 512 rows of `query → Canonical Term` mappings; consumed in Step 4 (ontology bootstrap) to populate `aliases_en` lists.
- `dynamic-pairs-index.md` carries 75 reciprocal pairs; consumed in Step 4 to mint the standalone `kind: dynamic-pair` entries (per OQ-C resolution).

### Per-term `kind` classification

Deferred to Plan Step 4 (ontology bootstrap). Step 1's purpose is the count gate, which passes; row-by-row `kind` assignment is wasted tokens here when it gets re-examined per-term during the bootstrap. The kind heuristic is fully specified in the prompt's Step 1 and OQ-B resolution.

### Drift summary

**No corpus drift since the 2026-05-04 kickoff.** Step 1 is satisfied; proceeding to Step 2.

## Token-Cost Benchmark

<!-- Populated at Step 12 of the prompt.
     Format: 10 representative queries × {prose-only path bytes, navigator path bytes, reduction %}.
     Acceptance gate: ≥60% reduction on lookup-shaped queries. -->

_pending Step 12_

## Schema Decision Log

### Files (Step 2 complete)

| Schema | Lines | Properties | `allOf` rules | Cap (200) |
|---|---:|---:|---:|---|
| `ontology.schema.json` | 152 | 17 | 4 | ✓ |
| `term-frontmatter.schema.json` | 82 | 16 | 4 | ✓ |
| `scenarios.schema.json` | 56 | 6 | 1 | ✓ |
| `theory-chunk.schema.json` | 61 | 7 | 0 | ✓ |
| **Total** | **351** | | | |

Plus `maintenance/schemas/narrative-ontology/readme.md` (≈170 lines) — reader's guide naming the OQ-A/B/C resolutions encoded by the schemas.

### Decisions

- **D-1.** Added `kind: throughline` to the kind enum. The kickoff SPEC's three name-resolution targets (`throughline.relationship`, `throughline.influence`) need a kind; routing them through `kind: concept` would lose semantics. The four throughlines are first-class.
- **D-2.** ID prefix uses kebab-case (`character-dynamic.problem-solving-style`, not `characterdynamic.problem-solving-style`). The pattern `^[a-z][a-z-]*\.[a-z0-9][a-z0-9-]*$` allows hyphens in both halves so multi-word kind prefixes survive.
- **D-3.** `aliases_<locale>` and `deprecated_aliases_<locale>` are validated via `patternProperties` with a depth-1 ISO-639-1 suffix pattern. The schema's `additionalProperties: false` plus the `patternProperties` regex together reject the nested `aliases: { en: [...] }` form (per OQ-A). Verified by negative fixture.
- **D-4.** Four `allOf` rules encode the cross-field invariants on the term-frontmatter and ontology schemas:
  1. `ncp_appreciation_partial` requires `ncp_appreciation`.
  2. `kind: dynamic-pair` requires `pair_member_a` + `pair_member_b`; forbids `dynamic_pair_id`.
  3. Other kinds forbid `pair_member_a` / `pair_member_b`.
  4. `kind` ∈ {archetype, quad, concept, class, throughline} forbids `dynamic_pair_id`.
- **D-5.** `theory-chunk.schema.json` has no `allOf` rules. The schema is purely structural — no cross-field invariants between `covers_ontology_ids` and `serves_scenarios`.
- **D-6.** Scenarios schema rejects IDs not starting with `novel.` or `lyric.`. Verified by negative fixture (`wrong.id` → 1 error). New personas in v0.2+ extend the regex.

### Validation evidence

`pip install jsonschema` then ran `Draft202012Validator.check_schema()` on each schema (all pass) plus 11 fixture cases (3 positive + 8 negative). Every case produced the expected error count. Trace recorded in the ReAct log above.

### Defensive note

`jsonschema` is not in the repo's pinned environment yet — Task 011's plan calls for adding it. The Task 013 `validate.py` (Plan step 8) MUST declare `jsonschema` as a dependency. If Task 011 ships first, the dependency is already in scope.

## M01 Median Tag-Count Check (Step 6 contingency)

<!-- After scenario tagging in Step 6, measure median scenarios-per-tagged-term.
     If > 5, the M01 contingency from /research/integrate-dramatica-ncp-skills/reflection/M01-falsification.md
     activates and Step 8 expands to add scenario-index.py. -->

_populated in Step 6_
