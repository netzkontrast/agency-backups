# Partial — Frontmatter Template

**File:** `modules/partials/frontmatter-template.md`
**Type:** partial (no frontmatter itself — partials are pure template fragments)
**Used by:** Phase 3 render script — emitted at the very top of every rendered `research-prompt.md` file
**Self-applied in Phase 2:** no (Phase 2 produces the meta-prompt.yaml that this partial consumes; the partial itself is rendered by Phase 3)

## Purpose

Defines the YAML frontmatter block that opens every rendered
research prompt. Carries the meta-prompt's identity (slug, topic,
created date, language), category routing, framework choice, list
of active methods/CBs/cross-pollinations, and bespoke-synthesis
provenance (when applicable). The frontmatter is the
machine-readable handle for tooling that consumes the rendered
prompt.

## Slot inventory (consumed by Phase 3 render)

| Slot | Filled by | Notes |
|------|-----------|-------|
| `slug` | Phase 2 | URL-safe identifier from research_question |
| `topic` | Phase 2 from `intent.research_question` (truncated) | Display title |
| `created` | Phase 3 | ISO timestamp at render time |
| `language` | Phase 2 from `intent.language` | "en" / "de" / etc. |
| `research_category` | Phase 2 from category routing | "A" / "B" / "C" |
| `research_category_label` | Phase 2 derived | "Exploration" / "Extraction" / "Lifecycle" |
| `framework_structural` | Phase 2 from framework selection | "risen" / "tidd-ec" / "co-star" / "care" / "crispe" / "bespoke" |
| `methods_list_indented` | Phase 3 from active methods set | List rendered as YAML-indented block |
| `constraint_blocks_list_indented` | Phase 3 from active CBs | YAML-indented |
| `cross_pollination_list_indented` | Phase 3 from active cross-pollinations | YAML-indented |
| `bespoke_provenance_indented` | Phase 3 (only if framework_structural=bespoke) | YAML-indented or empty |

## Body composition

- **Position:** very top of rendered prompt (before all other content)
- **Order constraint:** must be the literal first content — frontmatter
  is parsed by line-1 `---` marker
- **Composition partner:** consumed alongside `meta-header.md`
  partial which sits immediately below the frontmatter (frontmatter
  = machine-readable; meta-header = human-readable, same info)

## Split decision

**Currently:** single file
**Should it split?** No — frontmatter is one YAML document; splitting
would require ugly merging in Phase 3.

## Future extension points

1. **Bespoke provenance always-emitted.** Currently
   `bespoke_provenance_indented` only emits if framework=bespoke.
   For consistency, always emit (empty list when not bespoke).
2. **Schema-version field.** Add `schema_version: 1` to the
   frontmatter so downstream tooling can detect future schema
   changes without breaking on every prompt.
3. **Custom-metadata slot.** Allow `intent.custom_meta` to flow
   through to a `custom_metadata:` field in frontmatter for
   organization-specific tags.

## Open questions

- [ ] The `_indented` suffix on list slots is a Phase-3 indentation
      protocol marker. Should the rendering be Phase-3 dedicated
      logic (so slot names don't carry render hints) or stay
      explicit?
- [ ] `slug` and `topic` overlap in semantics. Could collapse to
      one slot; keep separate for readability vs. URL-safety.

## Catalog cross-reference

- Catalog: not in `modules:` — partials are referenced from
  `meta-header.md`'s slot definitions.
- Mandatory: yes (every rendered prompt has frontmatter)

## Change log

- `2026-05-02` (v3.0-phase2): initial concept doc.
