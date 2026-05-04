# Partial — Meta-Header (Three-Layer Block)

**File:** `modules/partials/meta-header.md`
**Type:** partial
**Used by:** Phase 3 render — emitted immediately after the YAML
frontmatter at the top of every rendered research prompt
**Self-applied in Phase 2:** no

## Purpose

Defines the human-readable header that opens every rendered research
prompt. Introduces the **three independent layers** the prompt is
built from: Epistemological Layer (which category) + Agentic Spine
(ReAct, always) + Structural Layer (RISEN/TIDD-EC/CO-STAR/CARE/CRISPE/
bespoke). Counters the failure mode where the executing agent reads
the prompt linearly and conflates layers, missing that they're
**stacked, not interleaved**.

## Slot inventory (consumed by Phase 3 render)

| Slot | Filled by | Notes |
|------|-----------|-------|
| `topic` | Phase 2 from `intent.research_question` (truncated) | Header title |
| `research_question` | Phase 2 from intent | Full question text |
| `unpacked_question` | Phase 2 from `intent.research_question_unpacked` | Structured form for clarity |
| `research_category_label` | Phase 2 derived | "Exploration" / "Extraction" / "Lifecycle" |
| `framework_structural_label` | Phase 2 derived | Display name of the structural framework |
| `output_format_directive` | Phase 2 from `intent.output_format` | What the final output must look like |
| `category_label` | Phase 2 from `intent.routing_hints.category_signal` | Short category label |
| `active_methods_list` | `fill_from` active methods set | Rendered as table |
| `active_constraint_blocks_list` | `fill_from` active CBs | Rendered as numbered list |
| `language_warning_block_or_empty` | `fill_from` language-warning partial (empty if EN) | Conditional injection |
| `category_block` | `fill_from` selected category partial | The Cat-A/B/C epistemological block |
| `react_block` | `fill_from` `react.md` framework | Always |
| `structural_block` | `fill_from` selected structural framework | RISEN by default, override-driven otherwise |

## Body composition

- **Position:** immediately after frontmatter, before any other
  content
- **Order constraint:** Three-layer summary table comes BEFORE the
  individual layer blocks — reader needs orientation before details
- **Composition partner:** **assembles four downstream partials**:
  language-warning (conditional), category block, react block,
  structural block. This partial is the integration point.

## Split decision

**Currently:** single file
**Should it split?** No — meta-header is one cohesive orientation
artifact. Splitting "summary table" from "layer blocks" would lose
the assembly handle.

## Future extension points

1. **Layer-count flexibility.** Currently 3 layers (epistemological
   + agentic + structural). For research that adds an additional
   layer (e.g., "ethical layer" for medical/legal research), a
   `{{additional_layers}}` slot could append.
2. **Reading-time estimate.** Add `{{estimated_reading_time}}` for
   long prompts so the executing agent can plan its reading.
3. **Visual rendering hooks.** For HTML/Markdown rendering, callout
   styles for each layer differ. A `{{layer_callout_style}}` slot
   could enable downstream rendering customization.

## Open questions

- [ ] The summary table currently lists all 3 layers as equal. In
      bespoke synthesis, the structural layer is custom-composed —
      should the table call this out explicitly?
- [ ] `output_format_directive` is also referenced in
      `verification/final-checklist.md`. Same slot or two? Currently
      same; risk of drift if Phase 2 fills them independently.

## Catalog cross-reference

- Catalog: referenced as the assembly point for category, framework,
  and language-warning partials. The single most central partial.
- Mandatory: yes (every rendered prompt has a meta-header)

## Change log

- `2026-05-02` (v3.0-phase2): initial concept doc.
