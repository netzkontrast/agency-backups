# Partial — Synthesis Schema

**File:** `modules/partials/synthesis-schema.md`
**Type:** partial
**Used by:** Phase 3 render — emitted as the final Synthesis section
of every rendered research prompt
**Self-applied in Phase 2:** no

## Purpose

Defines the schema the executing agent fills at the end of every
research run, AFTER the M4 Pre-Synthesis Integrity Check passes.
The schema is **category-specific** for the main body sub-template
(Cat-A → Hypothesis Tree, Cat-B → Output Matrix, Cat-C → Periodic
Brief), but the surrounding sections (Executive Summary, Key
Findings, Methodology Note, Contradictions Encountered, Query
Expansion Log, Cross-Pollination Log, Open Questions) are
universal.

## Slot inventory (consumed by Phase 3)

| Slot | Filled by | Notes |
|------|-----------|-------|
| `category_specific_main_body` | `fill_from` selected category sub-template | One of: hypothesis_tree (A), output_matrix (B), periodic_brief (C) |
| `executive_summary` | agent runtime | 3-5 bullets |
| `key_findings` | agent runtime | Numbered list of confirmed findings with sources |
| `methodology_note` | agent runtime | Brief description of methods applied and source quality |
| `contradictions_encountered` | agent runtime | From M07 Contradiction Log |
| `query_expansion_log` | agent runtime | From M13 invocations during the run |
| `cross_pollination_log` | agent runtime | From active cross-pollination modules' findings |
| `open_questions` | agent runtime | What remains unresolved |

## Body composition

- **Position:** very last section of every rendered prompt, AFTER
  the Pre-Synthesis Integrity Check section (M4)
- **Order constraint:** universal sections come in fixed order:
  Executive Summary → Key Findings → main-body (category-specific)
  → Methodology Note → Contradictions → Query Expansion Log →
  Cross-Pollination Log → Open Questions. The agent fills top-to-
  bottom.
- **Composition partner:** consumes outputs from M07 (contradictions),
  M13 (query expansion), every active cross-pollination module. M4
  Pre-Synthesis is the gate that must pass before this partial is
  filled.

## Split decision

**Currently:** single file
**Should it split?** Maybe in the future — the three category-
specific sub-templates (hypothesis_tree, output_matrix,
periodic_brief) could become standalone files in
`partials/synthesis-subtemplates/`. Currently inlined for
ease-of-reading; split when one sub-template grows past 30 lines.

## Future extension points

1. **Category-sub-template split.** As above — when sub-templates
   grow, split into `synthesis-hypothesis-tree.md` /
   `synthesis-output-matrix.md` / `synthesis-periodic-brief.md`.
2. **Confidence aggregation.** Currently agent reports findings
   without aggregate confidence. Add `{{aggregate_confidence}}`
   slot driven by M3-Batch's per-iteration `confidence_label`
   distribution.
3. **Output-format-driven schema variation.** When
   `intent.output_format == 'json'` the schema should emit JSON-
   parseable structure. Add output-format conditional rendering
   logic to Phase 3.
4. **Reproducibility section.** For Cat-B and Cat-C, future
   `{{reproducibility_notes}}` could capture seeds, source
   versions, retrieval timestamps — enabling later audit.

## Open questions

- [ ] The Cross-Pollination Log section is universal but only
      meaningful when cross-pollination modules were active. Render
      empty section anyway (for schema consistency) or omit?
      Currently universal.
- [ ] The Query Expansion Log can grow large. Should there be a
      summary-vs-detail split (top-level Query Log + appendix with
      full M13 trail)?

## Catalog cross-reference

- Catalog: referenced from `verification/final-checklist.md` (the
  checklist verifies the synthesis schema was filled)
- Mandatory: yes (every prompt ends with synthesis)
- Self-applied hook: no

## Change log

- `2026-05-02` (v3.0-phase2): initial concept doc.
