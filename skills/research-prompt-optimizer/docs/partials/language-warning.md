# Partial — Language Warning Block (Q1 v1.1)

**File:** `modules/partials/language-warning.md`
**Type:** partial
**Used by:** Phase 2.8 Plan-View AND Phase 3 render (when `intent.language != "en"`)
**Self-applied in Phase 2:** no

## Purpose

Implements the Q1 v1.1 design decision: all v3.0 templates are
EN-only, but intents can be non-English. When intent.language is
not "en", this partial is injected as a callout in two places:
(a) the Plan-View shown to the user in Phase 2.8 (so they're
warned BEFORE approving the plan), and (b) the rendered
research-prompt.md itself (as a top-of-prompt note for the
executing agent who will produce mixed-language output).

## Slot inventory (consumed by Phase 2 + Phase 3)

| Slot | Filled by | Notes |
|------|-----------|-------|
| `user_language` | Phase 2 from `intent.language` | ISO code (e.g. "de") |
| `user_language_full` | Phase 2 derived | Full name (e.g. "German") for prose |

The Phase 2 mapping `intent.language` → `user_language` +
`user_language_full` is a fixed lookup (en/de/fr/es/it/...).

## Body composition

- **Position 1 — Plan-View (Phase 2.8):** rendered as a top-of-view
  callout BEFORE the plan summary. User must acknowledge before
  approving.
- **Position 2 — Rendered prompt (Phase 3):** rendered as a callout
  in the meta-header section, between the frontmatter and the
  category epistemological layer.
- **Order constraint:** in both positions, must come BEFORE any
  domain content. The warning frames everything that follows.
- **Composition partner:** consumed by `meta-header.md` via the
  `language_warning_block_or_empty` slot — the partial renders
  empty when `intent.language == "en"`.

## Split decision

**Currently:** single file
**Should it split?** No — Plan-View and prompt-injection are two
emission points of the same warning text; splitting would risk drift.

## Future extension points

1. **Per-language tone calibration.** Currently the warning text is
   the same across languages. For some target languages (formal
   register required), the prose could adapt. Add
   `{{warning_register}}` slot.
2. **Mixed-output schema slot.** The warning currently says "this
   prompt mixes EN and {user_language}". Could specify exactly which
   sections will be in which language — `{{section_language_map}}`.
3. **User-acknowledgment requirement.** Currently the Plan-View
   shows the warning but doesn't gate approval. A
   `{{require_explicit_acknowledgment}}` flag could add a
   "type 'understood' to proceed" check.

## Open questions

- [ ] The Plan-View injection uses different framing ("the plan you're
      approving will produce mixed-language output") than the
      prompt-injection ("the executing agent should produce these
      sections in this language"). Is the dual framing necessary or
      should they unify?
- [ ] When the user explicitly requests "all output in DE" via
      `intent.output_language=de` (hypothetical extension), the
      warning becomes wrong. Need a Phase-1 escape hatch.

## Catalog cross-reference

- Catalog: referenced from `partials/meta-header.md` via slot
  `language_warning_block_or_empty`
- Mandatory: conditional (rendered iff `intent.language != "en"`)

## Change log

- `2026-05-02` (v3.0-phase2): initial concept doc.
