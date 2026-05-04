# M12 — Base-Rate Anchoring

**File:** `modules/methods/m12-base-rate.md`
**Type:** method
**Mandatory:** no (default for Cat-B)
**Self-applied in Phase 2:** no (Phase 2 has no numeric claims)

## Purpose

For every numerical frequency or probability claim, demand the agent
contextualize it against the relevant base rate. Counters the
representativeness-heuristic failure mode where vivid anecdotes or
small-n samples get treated as typical without checking how often
they actually occur in the underlying population.

## Slot inventory

This module has **no frontmatter slots** — body is a pure prose method
description.

**Structural markers (NOT slots):**

- `[PLACEHOLDER]` — visual placeholder in the body example showing
  where a domain-specific frequency claim would land. Not a slot;
  reading aid.

## Body composition

- **Section anchor:** `### Method: Base-Rate Anchoring`
- **Order constraint:** invoked alongside any numerical claim, NOT
  at fixed position
- **Composition partner:** pairs with M04 Contrast Classes (M04 asks
  "compared to what?", M12 asks "and how often does that comparison
  baseline occur?") and M06 Source Triangulation (M06 confirms the
  numerical claim itself; M12 contextualizes it)

## Split decision

**Currently:** single file
**Should it split?** No — base-rate anchoring is one tight discipline.

## Future extension points

1. **Base-rate-source slot.** Currently the agent self-sources the
   base rate. Add `{{base_rate_source}}` (agent_runtime_fill) to
   require explicit attribution — sometimes the base rate itself is
   contested.
2. **Default-base-rate library.** For common research domains, base
   rates are stable across runs (industry default rates, regulatory
   compliance percentages, etc.). A future
   `partials/standard-base-rates.md` could provide a starter library.
3. **Numerical-claim auto-detection.** Currently the agent self-flags
   numerical claims. A `{{numerical_claim_pattern}}` slot could
   provide regex/heuristics for the agent to apply systematically.

## Open questions

- [ ] Should base-rate anchoring be promoted to mandatory for any
      research that produces quantitative output? Currently Cat-B
      default; Cat-A and Cat-C can omit even when they include
      numerical claims.
- [ ] When base rate is unavailable (rare event, no published
      statistics), what's the fallback? Currently agent-managed.
      Future `{{base_rate_unknown_action}}` slot could codify
      `flag_uncertainty` | `estimate_with_bounds` | `omit_claim`.

## Catalog cross-reference

- Catalog: `modules.M12`
- Triggered by: `how common is`, `typical rate`, `how often`
- Default for: B
- Pairs well with: M04, M06
- Self-applied hook: no

## Change log

- `2026-05-02` (v3.0-phase2): initial concept doc.
