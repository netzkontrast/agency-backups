# M09 — Red Team / Devil's Advocate Review

**File:** `modules/methods/m09-red-team.md`
**Type:** method
**Mandatory:** no (default for Cat-C)
**Self-applied in Phase 2:** no (overlap with M03 Pre-Mortem rejected during Q6)

## Purpose

Mount a structured adversarial attack on each major conclusion: find
biased domains in the source pool, identify hidden premises,
articulate competing hypotheses. Counters the failure mode where a
research run produces internally consistent conclusions that an
adversarial reader could shred in five minutes.

## Slot inventory

| Slot name | Type | Filled by | Required | Notes |
|-----------|------|-----------|----------|-------|
| `conclusion` | `agent_runtime_fill` | agent at runtime | yes | The conclusion under attack |
| `biased_domain` | `agent_runtime_fill` | agent at runtime | no | Specific domain in the source pool with known bias (e.g., "vendor whitepapers", "single-author preprints") |
| `hidden_premise` | `agent_runtime_fill` | agent at runtime | no | An unstated assumption the conclusion depends on |
| `competing_hypothesis` | `agent_runtime_fill` | agent at runtime | no | The strongest alternative explanation for the same evidence |

**Structural markers:** none.

## Body composition

- **Section anchor:** `### Method: Red Team / Devil's Advocate Review`
- **Order constraint:** invoked **after** a major conclusion is
  stated — pre-conclusion is M03 Pre-Mortem's territory; post-
  conclusion is M09's
- **Composition partner:** pairs with M02 Steelmanning (steelman the
  attack itself before concluding the conclusion holds) and M07
  Contradiction Log (red-team findings often surface contradictions
  worth logging)

## Split decision

**Currently:** single file
**Should it split?** Possibly — the four slots represent four
distinct attack vectors. If empirical use shows agents apply only one
or two, splitting into `m9a-source-bias.md` / `m9b-hidden-premise.md`
/ `m9c-competing-hypothesis.md` could make activation more granular.
For now: single file, all four slots optional, agent picks the
relevant ones per conclusion.

## Future extension points

1. **Attack-quota slot.** `escape_criterion` says "Three attack angles
   per major conclusion." Surface as `{{attack_angles_per_conclusion}}`
   (default 3) for domain-specific calibration.
2. **Attack-history accumulator.** Like M08, accumulate red-team
   findings across the run for cross-reference at synthesis. New slot
   `{{red_team_log}}` (agent-maintained list).
3. **Pair with M02 protocol.** When both M02 and M09 are active, M02
   should be invoked on every red-team attack (steelman the attack
   first). Currently this is implicit; could be made explicit via
   `pairs_with_protocol`.

## Open questions

- [ ] If M09 splits into 3 sibling modules, what's the catalog
      naming? `m9a` / `m9b` / `m9c` or `m09a-source-bias` etc.?
      Affects all dependent docs.

## Catalog cross-reference

- Catalog: `modules.M09`
- Triggered by: `steelman the opposition`, `attack this`, `break it`
- Default for: C
- Pairs well with: M02, M07
- Self-applied hook: no

## Change log

- `2026-05-02` (v3.0-phase2): initial concept doc.
