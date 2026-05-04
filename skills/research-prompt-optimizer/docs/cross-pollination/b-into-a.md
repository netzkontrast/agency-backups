# Cross-Pollination — B into A (Surviving-Branch Triangulation)

**File:** `modules/cross-pollination/b-into-a.md`
**Type:** cross-pollination
**Selected when:** `category == A` (paired with `c-into-a` per
`catalog.yaml` → `categories.A.cross_pollination_pair`)
**Self-applied in Phase 2:** no

## Purpose

Imports the Cat-B extraction discipline (source triangulation) into
Cat-A exploration. After exploration generates competing hypothesis
branches, the surviving branches must be triangulated against ≥3
independent sources before being elevated to candidate conclusions.
Counters the failure mode where exploratory hypotheses get treated
as findings just because they survived internal coherence checks —
without external source verification.

## Slot inventory

This module has **no frontmatter slots** — body is paste-ready
prose template.

**Structural markers (NOT slots):**

- `[LOW / MEDIUM / HIGH]` — confidence enum the agent fills per
  surviving branch (parallel to M3 Batch's `confidence_label`)
- `[concrete future observation]` — agent-runtime placeholder for
  the M08-style pre-commitment on each surviving branch
- `[i.b]` — cross-pollination index marker (b-into-a family)

## Body composition

- **Section anchor:** `### Cross-Pollination — B → A: Surviving-Branch
  Triangulation`
- **Order constraint:** rendered after Methods, inside the
  Cross-Pollination block. Fires AFTER M01 Falsification has pruned
  the hypothesis tree — operates only on surviving branches.
- **Composition partner:** pairs with `c-into-a` (the other Cat-A
  cross-pollination) and structurally couples to M01 Falsification
  (provides surviving branches), M06 Source Triangulation (provides
  the triangulation method), and M08 What Would Change My Mind
  (provides the pre-commitment template)

## Split decision

**Currently:** single file
**Should it split?** No — surviving-branch triangulation is one
mechanism, even though it imports techniques from three methods.

## Future extension points

1. **`confidence_label` slot.** Promote `[LOW / MEDIUM / HIGH]` from
   structural marker to formal slot (mirroring M3-Batch's pattern).
2. **Branch-pruning threshold.** Currently every surviving branch is
   triangulated. For exploration with many branches, a
   `{{triangulation_priority_rule}}` slot could prioritize branches
   by current-likelihood × decision-impact.
3. **Cross-link to M01 falsification log.** Surviving branches imply
   a falsification log exists. A future protocol could chain M01
   output → `b-into-a` input explicitly via Phase-3 data flow.

## Open questions

- [ ] When all branches fail triangulation (no ≥3 source support),
      what's the protocol? Currently undocumented. Options:
      `degrade_to_speculation` | `halt_and_request_more_sources` |
      `widen_M13_axes_and_retry`.
- [ ] Should this cross-pollination be auto-active OR
      override-conditional? Currently always active for Cat-A.

## Catalog cross-reference

- Catalog: `modules.b-into-a`
- Selected when: `category == A` (Cat-A cross-pollination pair)
- Pairs with: `c-into-a` (the other Cat-A cross-pollination)
- Self-applied hook: no

## Change log

- `2026-05-02` (v3.0-phase2): initial concept doc.
