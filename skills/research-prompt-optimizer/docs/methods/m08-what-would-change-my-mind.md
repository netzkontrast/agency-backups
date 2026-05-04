# M08 — What Would Change My Mind (Pre-Commitment)

**File:** `modules/methods/m08-what-would-change-my-mind.md`
**Type:** method
**Mandatory:** no (default for Cat-B)
**Self-applied in Phase 2:** no (M01 + M05 cover the routing pre-commitment together)

## Purpose

Force the agent to **pre-commit** — before reaching a major
conclusion — to a specific observation that would invalidate it.
Counters motivated reasoning: an honest pre-commitment makes it
structurally hard to rationalize away disconfirming evidence after
the fact.

## Slot inventory

| Slot name | Type | Filled by | Required | Notes |
|-----------|------|-----------|----------|-------|
| `conclusion` | `agent_runtime_fill` | agent at runtime | yes | The conclusion the agent is about to commit to |
| `disconfirming_observation` | `agent_runtime_fill` | agent at runtime | yes | The specific observation that would invalidate the conclusion |

**Structural markers (NOT slots):**

- `[X]` — visual placeholder for evaluative claim under
  pre-commitment (mirrors M04's `[X]` convention)

## Body composition

- **Section anchor:** `### Method: What Would Change My Mind`
- **Order constraint:** invoked at the moment a major conclusion is
  about to be stated — not at fixed position in methods sequence
- **Composition partner:** pairs with M01 Falsification (M01 actively
  searches for the disconfirmation; M08 commits to what would count)
  and M05 Bayesian Prior (M05 sets the prior; M08 sets the update threshold)

## Split decision

**Currently:** single file
**Should it split?** No — pre-commitment is one move, not multiple.

## Future extension points

1. **Pre-commitment registry slot.** Add `{{precommitment_log}}`
   (agent-maintained list) so all pre-commitments accumulate during
   the run and are cross-referenced at synthesis. Currently each
   invocation is local.
2. **Threshold quantification.** "Specific observation" is qualitative.
   Add `{{disconfirmation_threshold_quantitative}}` (optional) for
   domains where probability/effect-size thresholds are appropriate.
3. **Auto-coupling with M05.** When M05 produces a Bayesian prior,
   M08 could consume the prior to compute a Bayes-factor threshold for
   the disconfirmation. Future protocol enhancement.

## Open questions

- [ ] Should this method become self-applied in Phase 2? Currently
      M01+M05 cover routing pre-commitment. But pre-commitment for
      module-selection or batch-detection decisions could be useful at
      sub-phases 4.3 and 4.4.

## Catalog cross-reference

- Catalog: `modules.M08`
- Triggered by: `falsifiable`, `disconfirming evidence`
- Default for: B
- Pairs well with: M01, M05
- Self-applied hook: no

## Change log

- `2026-05-02` (v3.0-phase2): initial concept doc.
