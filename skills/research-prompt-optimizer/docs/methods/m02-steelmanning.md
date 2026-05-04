# M02 — Steelmanning (Strongest-Version Reconstruction)

**File:** `modules/methods/m02-steelmanning.md`
**Type:** method
**Mandatory:** no (default for Cat-A)
**Self-applied in Phase 2:** no

## Purpose

Force the executing agent to construct the strongest possible version
of every claim/position before evaluating or rejecting it. Counters
the failure mode where research agents dismiss counter-intuitive
positions because the first few sources present them weakly.

## Slot inventory

| Slot name | Type | Filled by | Required | Notes |
|-----------|------|-----------|----------|-------|
| `mainstream_position` | `agent_runtime_fill` | agent during execution | yes | The position being steelmanned against — agent identifies it from research context |

**Structural markers:** none (body is pure prose).

## Body composition

- **Section anchor:** `### Method: Steelmanning (Strongest-Version Reconstruction)`
- **Order constraint:** standalone — placed in the methods sequence
  according to category default order
- **Composition partner:** pairs with M01 Falsification (steelman first,
  THEN try to falsify the strongest version) and M09 Red Team

## Split decision

**Currently:** single file
**Should it split?** No — the method is self-contained. Steps 1–3 form
a tight conceptual unit.

## Future extension points

1. **Steelman vs. devil's-advocate distinction** — currently conflated.
   Could add a flavour flag (`mode: charitable | adversarial`) if the
   research domain demands one or the other emphasis.
2. **Source-thinness threshold** — the `escape_criterion` mentions
   "after two iterations" but doesn't quantify "thin sources". A
   sibling slot `min_supporting_sources_for_steelman` (default 2)
   could make the abort condition objective.

## Open questions

- [ ] Should `mainstream_position` move from `agent_runtime_fill` to
      `phase2_fill_or_runtime`? If the user has explicit knowledge of
      which position to steelman against (occasional Cat-A intents),
      Phase 2 could pre-fill from a new intent field
      `intent.positions_to_steelman`. Currently the field doesn't
      exist; would need Phase-1 schema extension. Keep as runtime-fill
      for now.

## Catalog cross-reference

- Catalog entry: `catalog.yaml` → `modules.M02`
- Triggered by signals: `challenge the view`, `is it really`, `i suspect`, `skeptical`
- Default for category: A (Compare/Decide)
- Self-applied hook: no (rejected during Q6 — overlap with M01 Falsification)

## Change log

- `2026-05-02` (v3.0-phase2): initial concept doc; body unchanged (no brackets to convert).
