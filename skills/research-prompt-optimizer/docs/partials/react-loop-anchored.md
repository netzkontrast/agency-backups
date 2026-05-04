# Partial — ReAct Loop Anchored (KEY INNOVATION v3.0)

**File:** `modules/partials/react-loop-anchored.md`
**Type:** partial
**Used by:** Phase 3 render — composed INTO `frameworks/react.md`'s
Reason phase to make the active-method palette explicit per run
**Self-applied in Phase 2:** no

## Purpose

The single biggest behavioural change v3.0 makes vs v2.1. v2.1's
ReAct Reason phase used a **generic 3-question prompt** that didn't
mention which methods were actually active for that run, so the
executing agent had to remember and apply them on its own — and
predictably forgot. v3.0 anchors the Reason phase by **rendering the
active method palette inline** in every Reason step: the agent sees
exactly `[M01]`, `[M06]`, `[M13]` etc. as labeled tools to invoke,
not as background knowledge to recall.

## Slot inventory (consumed by Phase 3)

| Slot | Filled by | Notes |
|------|-----------|-------|
| `active_method_anchors` | `fill_from` active methods set | Phase 3 substitutes `[M__]`-style placeholders with each active method's `short_anchor` from frontmatter |

## Structural markers (NOT slots — preserved)

- `[M01]`, `[M02]`, `[M06]`, `[M07]`, `[M13]`, `[M__]` — method-anchor
  placeholders. These are NOT user variables and NOT slots in the
  v3.0 sense. Phase 3 has dedicated logic for active-method-anchor
  expansion: it walks the active methods set, looks up each method's
  `short_anchor`, and substitutes the placeholders.
- `[Reason 1]`, `[Reason 2]`, `[Reason N]`, `[Act 1]`, `[Act 2]`,
  `[Observe 1]`, `[Observe 2]` — structural iteration anchors in
  the ReAct loop. Preserved as labels the executing agent uses to
  reference loop position.
- `[Synthesis]`, `[Pre-Synthesis Integrity Check]` — structural
  section anchors pointing to other modules.

## Body composition

- **Position:** composed into `frameworks/react.md` at the Reason
  phase. Not rendered standalone — always via the parent framework.
- **Order constraint:** the active-method palette appears at the
  TOP of every Reason phase, before the agent's free reasoning,
  forcing palette consultation before deliberation.
- **Composition partner:** parent framework `react.md`. Also
  structurally couples to `m2-restatement-checkpoint.md` (which
  re-emits the active methods at every step start) and to `m13-
  adversarial-query-expansion.md` (which is always in the palette).

## Split decision

**Currently:** single file
**Should it split?** No — anchoring is one mechanism; the partial is
the implementation handle for the parent framework.

## Future extension points

1. **Per-step palette refinement.** Currently the palette is the
   same across all Reason steps. Could vary by step phase: early
   steps emphasize M13 (expansion), late steps emphasize M04+M12
   (claim verification). Add `{{step_phase}}` and route palette
   accordingly.
2. **Method-fatigue tracking.** When the agent invokes the same
   method 3+ times consecutively without novel finding, the
   `escape_criterion` per method should fire. A
   `{{method_invocation_log}}` slot could track this structurally.
3. **Cross-method synergy hints.** "Pairs well with" relationships
   are in catalog frontmatter but not surfaced in the rendered
   palette. Could add `{{pair_hints}}` rendered next to each
   anchor: `[M01] (pairs with [M02], [M08])`.

## Open questions

- [ ] The `[M__]` generic placeholder is used when the body
      references "any active method". Phase 3 expands it to ALL
      active method anchors — but ordering matters. Currently
      catalog-frontmatter order. Should it be priority-ordered
      (mandatory first, then high-trigger-match)?
- [ ] When bespoke synthesis is active, the structural framework
      also has its own anchors (e.g., bespoke acronym letters).
      Should those be in the palette too, or is palette
      method-only?

## Catalog cross-reference

- Catalog: referenced as a partial inside `modules.react.partials`
- Mandatory: yes (every prompt uses ReAct, which uses this partial)
- Self-applied hook: no
- Slot it provides: `active_method_anchors` (consumed by ReAct's
  Reason-phase template)

## Change log

- `2026-05-02` (v3.0-phase2): initial concept doc.
