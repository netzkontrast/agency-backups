# M13 — Adversarial Query Expansion

**File:** `modules/methods/m13-adversarial-query-expansion.md`
**Type:** method
**Mandatory:** yes (active for every category, every prompt)
**Self-applied in Phase 2:** yes (sub-phase 4.6 — adjust auto-axis direction before bundled askuser)

## Purpose

Force the agent to systematically expand the seed query along **four
orthogonal axes** — adjacent, opposing, abstraction, orthogonal — to
escape the local-minimum lock-in that vanilla search induces. Single
biggest counter-mechanism against research that "stays in its lane".
This method is mandatory for every research prompt, not just one
category default.

## Slot inventory

| Slot name | Type | Filled by | Required | Notes |
|-----------|------|-----------|----------|-------|
| `seed_vocabulary` | `phase2_fill` | Phase 2.6 (auto from intent + bundled askuser approval) | yes | The 5-10 starting queries |
| `orthogonal_lens` | `phase2_fill` | Phase 2.6 (bundled askuser, Q4 v1.1) | yes | The fourth axis — explicitly chosen by user, not auto-generated |
| `adjacent_term` | `agent_runtime_fill` | agent at runtime | no | Synonyms, neighbouring sub-fields |
| `opposing_term` | `agent_runtime_fill` | agent at runtime | no | Failure case, opposite school |
| `higher_level_term` | `agent_runtime_fill` | agent at runtime | no | One abstraction level UP |
| `lower_level_term` | `agent_runtime_fill` | agent at runtime | no | One abstraction level DOWN |

**Structural markers:** none.

## Body composition

- **Section anchor:** `### Method: Adversarial Query Expansion`
- **Order constraint:** **mandatory inclusion in every prompt** —
  per `mandatory: true` in frontmatter
- **Composition partner:** pairs with `partials/react-loop-anchored.md`
  (which references M13's active state in its Reason phase) and
  `replication/m2-restatement-checkpoint.md` (which always includes
  M13 first in the method-restatement block)

## Self-applied hook detail (sub-phase 4.6)

Before Phase 2 auto-generates the three non-orthogonal axes
(adjacent / opposing / abstraction), M13 fires self-reflectively:
*"In which conceptual direction does the initial seed-vocabulary
push me? Where is the genuine opposite? Is my abstraction direction
(up vs. down) actually the under-served one for this intent?"*

Without this hook, all four axes drift toward Claude's local
minimum and the bundled askuser becomes cosmetic. Findings land in
`meta-prompt.self_reflection.expansion_axes_plan_reflection` and
the auto-axes are adjusted before being shown to the user.

## Split decision

**Currently:** single file
**Should it split?** No — the four axes are conceptually one method
(each axis is a different angle of the same orthogonality
discipline). Splitting would dilute the "always run all four" force.

## Future extension points

1. **Per-axis termination tracking.** `escape_criterion` says "Stop
   expanding an axis when 2 consecutive expansions produce no novel
   findings". Currently agent-managed. Add
   `{{axis_termination_log}}` (per-axis counter) to make it
   structural.
2. **Fifth-axis support.** Some research domains may benefit from a
   fifth or sixth axis (chronological, geographic). Frontmatter
   `axis_count` flag could parameterize this; currently hard-coded
   at 4.
3. **Cross-pollination handoff.** When cross-pollination modules
   activate, the orthogonal lens often comes from the partner
   category. Future protocol could explicitly couple M13's
   `orthogonal_lens` with the active cross-pollination module.

## Open questions

- [ ] The `triggered_by_signals: []` is empty — M13 is mandatory
      regardless of signals. Should the field be removed entirely or
      kept empty as documentation?
- [ ] Self-applied hook variant for `intent.depth=surface`: currently
      surface skips the M13 self-application entirely. But surface
      research is exactly where lock-in is most likely. Reconsider in
      a future iteration?

## Catalog cross-reference

- Catalog: `modules.M13`
- Triggered by: (none — mandatory)
- Default for: A, B, C (all)
- Pairs well with: (n/a — paired with everything via mandatory status)
- Self-applied hook (catalog): `sub_phase: 4.6`,
  `depth_active: [standard, exhaustive]`

## Change log

- `2026-05-02` (v3.0-phase2): initial concept doc; frontmatter
  `self_applied_phase2:` block added to sync with catalog index.
