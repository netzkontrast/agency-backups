# TIDD-EC — Task · Instructions · Do · Don't · Examples · Context

**File:** `modules/frameworks/tidd-ec.md`
**Type:** framework
**Role:** structural_layer
**Override trigger:** `intent.known_constraints contains 'forbidden actions' OR research is compliance-focused`
**Override priority:** 2 (out of 4 — second-most-likely override)
**Self-applied in Phase 2:** no

## Purpose

Specialized structural framework for research with **explicit
forbidden actions** — compliance audits, regulatory checks, safety
reviews. The "Do / Don't" axis is what RISEN cannot express cleanly:
a list of behaviours that must NOT happen during execution. Used
when the intent contains hard prohibitions, not just expectations.

## Slot inventory

This module has **no frontmatter slots** — body is a pure paste-ready
template. The Do / Don't bullet lists are filled by Phase 2 from
`intent.known_constraints` if present, but as prose insertion, not
through a named slot. (See Future Extensions for the proposed slot
formalization.)

**Structural markers:** none.

## Body composition

- **Section anchors:** 6 fixed sections — `## Task`,
  `## Instructions`, `## Do`, `## Don't`, `## Examples`, `## Context`
- **Order constraint:** Do / Don't sections come **before** Examples
  intentionally — the executing agent reads constraints before
  worked examples
- **Composition partner:** sits above ReAct (like all structural
  frameworks). Pairs well with M07 Contradiction Log (the Don't
  list is exactly what M07 watches for) and with `categories/b-
  extraction.md` (Cat-B + compliance is the typical TIDD-EC use case)

## Split decision

**Currently:** single file
**Should it split?** No — the 6 sections are tightly interlocked,
especially Do/Don't. Splitting would break the symmetry.

## Future extension points

1. **`do_list` and `dont_list` slots.** Formalize the bullet lists
   as slots (`phase2_fill`, fill_from `intent.known_constraints
   .forbidden_actions`). Currently Phase 2 inserts them as prose at
   render time. Slot formalization would enable Phase-3 dedicated
   rendering (consistent bullet style, count enforcement, etc.).
2. **Compliance-source flag.** When TIDD-EC is selected, the source
   of the prohibition matters (regulator? internal policy? legal
   risk?). Add `{{prohibition_source}}` slot to surface this.

## Open questions

- [ ] Override trigger: should it also fire on `intent.research_type
      == 'safety_review'` (a hypothetical Phase-1 enum)? Currently
      relies on free-text scan of `known_constraints`.
- [ ] When Q3 lenient bespoke synthesis fires (≥2 override triggers),
      TIDD-EC's Do/Don't axis is the most-borrowed component. Should
      `synthesis.md` cite TIDD-EC as the canonical source of the
      Do/Don't axis explicitly?

## Catalog cross-reference

- Catalog: `modules.tidd-ec`
- Override trigger: `intent.known_constraints contains 'forbidden
  actions' OR research is compliance-focused`
- Override priority: 2
- Default for: (none — selected by override)
- Pairs well with: M07, M08, Cat-B
- Self-applied hook: no

## Change log

- `2026-05-02` (v3.0-phase2): initial concept doc.
