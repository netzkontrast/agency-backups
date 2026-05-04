# Category B — Extraction (Plan-and-Execute / Deterministic Collection)

**File:** `modules/categories/b-extraction.md`
**Type:** category
**Mandatory:** rendered when Phase 2 routes intent to Cat-B
**Self-applied in Phase 2:** no (categories are routing targets, not skill-internal hooks)

## Purpose

Provides the **Epistemological Layer** block that ships into the
rendered prompt whenever the research intent is "the answer exists,
go retrieve it in structured form" — comparison matrices, due-
diligence inventories, regulatory taxonomies, benchmarks. The block
locks the executing agent into a *plan-and-execute* mode (no
hypothesis generation, no improvisation), and enforces source
triangulation + contradiction-logging as hard contracts.

## Slot inventory

This module has **no frontmatter slots**. It is a paste-ready prose
block — the body is the rendered output verbatim.

**Structural markers (NOT slots):** none. Body is pure prose.

## Body composition

- **Section anchor:** `## Epistemological Layer — Category B (Extraction)`
- **Order constraint:** rendered immediately after the Meta-Header
  (intent restatement) and before the Constraint Blocks
- **Composition partner:** every Cat-B prompt also activates M06
  Source Triangulation, M07 Contradiction Log, M08 What Would Change
  My Mind, M12 Base-Rate Anchoring (per `catalog.yaml` →
  `categories.B.default_methods`)

## Split decision

**Currently:** single file
**Should it split?** No — the 5 numbered points form one tight
behavioural contract. Splitting would dilute the "extraction is not
interpretation" thrust.

## Future extension points

1. **Output-schema partial.** Point 2 mentions "the locked schema
   specified in the Expectations section". A future `partials/output-
   schema-template.md` could provide a canonical schema skeleton that
   Cat-B prompts include by default, parameterized by
   `intent.output_format`.
2. **Source-tier vocabulary.** Point 3 says "primary source" without
   defining the term. A future inline glossary slot
   (`{{source_tier_definitions}}`) could be filled from
   `intent.known_constraints.sources` if present.
3. **Sub-category split.** If empirical use shows that "comparison
   matrix" and "due diligence inventory" demand structurally different
   blocks, split into `b1-comparison.md` / `b2-inventory.md` and add a
   B-subtype slot to `intent.routing_hints`.

## Open questions

- [ ] Should "at least three independent sources" be a configurable
      threshold? Some intents (e.g., legal reg-watch) demand higher;
      some (creative briefings) lower. Currently hard-coded as
      universal default.
- [ ] The "aggregators count as one source" rule is opinionated —
      surface as a flag (`{{aggregator_dedup_strict: true|false}}`)?

## Catalog cross-reference

- Catalog entry: `catalog.yaml` → `categories.B`
- Signal words: `compare`, `vergleichen`, `list all`, `aggregate`,
  `matrix`, `comparison table`, `due diligence`, `summarize the
  field`, `benchmark`, `inventory`, `catalog`
- Default methods: M06, M07, M08, M12
- Default structural framework: RISEN
- Cross-pollination pair: `a-into-b`, `c-into-b`
- Typical batches: `per-item`

## Change log

- `2026-05-02` (v3.0-phase2): initial concept doc; body unchanged.
