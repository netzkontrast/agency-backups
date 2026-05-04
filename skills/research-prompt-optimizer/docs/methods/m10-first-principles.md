# M10 — First-Principles Decomposition

**File:** `modules/methods/m10-first-principles.md`
**Type:** method
**Mandatory:** no (default for Cat-A)
**Self-applied in Phase 2:** no (`research_question_unpacked` from Phase 1 already provides this)

## Purpose

Decompose a complex question into its irreducible primitives before
attempting answers. Force the agent to ask "what does this question
*actually* depend on?" rather than searching at the question's
surface vocabulary. Counters the failure mode where research stays
trapped at the framing level of the question, missing that the real
unknowns are one or two layers deeper.

## Slot inventory

This module has **no frontmatter slots** — body is a pure prose method
description.

**Structural markers (NOT slots):**

- `[PLATFORM]` — visual placeholder in the example showing where a
  domain-specific noun would land (e.g., "an AI hiring platform" in
  the example). Not a slot; just a reading aid.

## Body composition

- **Section anchor:** `### Method: First-Principles Decomposition`
- **Order constraint:** placed **first** in methods sequence when
  active — decomposition must run before evaluation methods bite
- **Composition partner:** pairs with M04 Contrast Classes (M10
  decomposes the question; M04 ensures every evaluative claim about
  the parts has an explicit baseline)

## Split decision

**Currently:** single file
**Should it split?** No — decomposition is one cohesive technique.

## Future extension points

1. **Decomposition-tree slot.** Currently the agent maintains the
   decomposition tree in their working notes. Add
   `{{decomposition_tree}}` (agent_runtime_fill, structured) to make
   it part of the persistent output, especially for Cat-C lifecycle
   research where the tree should survive sessions.
2. **Layer-depth flag.** `escape_criterion` says "Stop at 2-3 layers".
   Surface as `{{max_decomposition_depth}}` (default 3) for domain-
   specific calibration — some research demands deeper.
3. **Couple with intent.research_question_unpacked.** Phase 1 already
   produces a decomposition. M10 currently re-does it from scratch.
   Future: M10 could consume `intent.research_question_unpacked` as
   starting tree and extend it during research.

## Open questions

- [ ] Should the Phase-1 `research_question_unpacked` field auto-fill
      a `{{starting_decomposition}}` slot in M10, or stay separate?
      Coupling reduces redundancy but creates a silent dependency on
      Phase-1 schema.

## Catalog cross-reference

- Catalog: `modules.M10`
- Triggered by: `from first principles`, `ground up`, `why does this
  exist`
- Default for: A
- Pairs well with: M04
- Self-applied hook: no (Phase 1 already provides decomposition via
  `research_question_unpacked`)

## Change log

- `2026-05-02` (v3.0-phase2): initial concept doc.
