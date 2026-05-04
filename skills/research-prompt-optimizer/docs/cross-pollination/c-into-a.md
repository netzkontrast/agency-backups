# Cross-Pollination — C into A (Hypothesis Half-Life Audit)

**File:** `modules/cross-pollination/c-into-a.md`
**Type:** cross-pollination
**Selected when:** `category == A` (paired with `b-into-a` per
`catalog.yaml` → `categories.A.cross_pollination_pair`)
**Self-applied in Phase 2:** no

## Purpose

Imports the Cat-C lifecycle discipline (assumption-decay) into Cat-A
exploration. For each surviving hypothesis, the agent records its
**half-life** — how long is this hypothesis likely to remain credible
before new evidence supersedes it? Counters the failure mode where
exploration treats hypotheses as timeless when many are time-bound
(regulatory landscape changes, technology matures, market shifts).

## Slot inventory

This module has **no frontmatter slots** — body is paste-ready
prose template.

**Structural markers (NOT slots):**

- `[H]` — placeholder for the hypothesis being half-life-audited
- `[PATTERN]` — pattern of decay being tracked (e.g., "vendor
  consolidation pattern", "regulatory tightening pattern")
- `[QUERY]` — agent-runtime placeholder for the M13-style query
  expansion that should detect decay signals
- `[i.c]` — cross-pollination index marker (c-into-a family)

## Body composition

- **Section anchor:** `### Cross-Pollination — C → A: Hypothesis
  Half-Life Audit`
- **Order constraint:** rendered after Methods, inside the
  Cross-Pollination block. Operates on hypotheses that survived
  M01 Falsification AND `b-into-a` triangulation.
- **Composition partner:** pairs with `b-into-a`; structurally
  couples to M01 Falsification (provides surviving hypotheses), M11
  Assumption-Decay Audit (provides the decay-checking method), M13
  Adversarial Query Expansion (provides query-expansion patterns
  for decay-signal detection).

## Split decision

**Currently:** single file
**Should it split?** No — half-life audit is one mechanism.

## Future extension points

1. **Half-life unit standardization.** Currently free-text
   ("months", "regulatory cycles", "until next election"). Add
   `{{half_life_unit}}` enum (`months | regulatory_cycles |
   technology_generations | indefinite`) for cross-research
   comparability.
2. **Decay-signal subscription.** When half-life is short, the agent
   should set up monitoring queries. A `{{decay_monitor_protocol}}`
   slot could codify "re-run query Q every K weeks; halt research
   if signal X appears".
3. **Hypothesis aging at synthesis.** At final synthesis, hypotheses
   could be sorted by remaining half-life so the reader knows which
   conclusions decay first. Add `{{aging_sort}}` flag.

## Open questions

- [ ] Half-life is inherently speculative — the agent guesses
      future-decay-rate. Should the audit require a confidence
      level (parallel to M3-Batch's `confidence_label`)?
- [ ] Hypotheses with `half_life=indefinite` (mathematical truths,
      stable definitions) — are they exempt from this audit, or do
      they get explicitly marked as such for clarity?

## Catalog cross-reference

- Catalog: `modules.c-into-a`
- Selected when: `category == A` (Cat-A cross-pollination pair)
- Pairs with: `b-into-a`
- Self-applied hook: no

## Change log

- `2026-05-02` (v3.0-phase2): initial concept doc.
