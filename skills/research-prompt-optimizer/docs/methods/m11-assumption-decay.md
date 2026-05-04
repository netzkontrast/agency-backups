# M11 — Assumption-Decay Audit

**File:** `modules/methods/m11-assumption-decay.md`
**Type:** method
**Mandatory:** no (default for Cat-C)
**Self-applied in Phase 2:** no (Phase 2 is single-shot — no decay dimension)

## Purpose

For long-running (Cat-C lifecycle) research, periodically audit
whether the foundational assumptions still hold. Counters the failure
mode where an ongoing research stream silently inherits assumptions
from session 1 that have since been invalidated by world changes,
new evidence, or shifted scope.

## Slot inventory

| Slot name | Type | Filled by | Required | Notes |
|-----------|------|-----------|----------|-------|
| `foundational_assumptions` | `phase2_fill_or_runtime` | `intent.priors_and_constraints.known_priors` if present, else agent enumerates at runtime | no | The list of assumptions to audit |
| `concrete_check` | `agent_runtime_fill` | agent at runtime | yes | The specific evidence-based check the agent performs to verify each assumption still holds |

**Structural markers:** none.

## Body composition

- **Section anchor:** `### Method: Assumption-Decay Audit`
- **Order constraint:** invoked at fixed checkpoints (Cat-C
  Resumption Protocol step (d) per `c-lifecycle.md`), NOT per search
- **Composition partner:** pairs with M03 Pre-Mortem (pre-mortem
  identifies risks ahead of time; assumption-decay catches them when
  they actually decay) and M07 Contradiction Log (decayed assumptions
  often surface as contradictions with newer findings)

## Split decision

**Currently:** single file
**Should it split?** No — audit is one mechanism with two slots.

## Future extension points

1. **Assumption-registry persistence.** For Cat-C, the
   `foundational_assumptions` should persist across sessions. Define
   a `partials/lifecycle-assumption-registry.md` partial that
   `c-lifecycle.md` includes; M11 reads from it.
2. **Decay-rate-per-assumption.** Some assumptions decay faster
   (regulatory state) than others (mathematical truths). Add
   `{{audit_cadence_per_assumption}}` (dict mapping assumption →
   audit interval) for differential checking.
3. **Audit-failure protocol.** When an audit fails, the c-lifecycle
   block says "Mark as AUDIT FAILURE in the knowledge store. Re-
   evaluate previous conclusions." Currently prose. Future protocol
   slot `{{audit_failure_action}}` could codify the re-evaluation
   procedure.

## Open questions

- [ ] Should `foundational_assumptions` migrate from
      `phase2_fill_or_runtime` to pure `phase2_fill`? If Phase 1
      schema gains a `lifecycle_assumptions` field, Phase 2 could
      always pre-fill. Currently hybrid because Phase-1 schema lacks
      the field.
- [ ] Audit cadence: currently per-checkpoint (agent decides). Should
      `intent.session_cadence` (proposed for c-lifecycle) drive a
      mechanical audit-frequency, e.g., every Nth session?

## Catalog cross-reference

- Catalog: `modules.M11`
- Triggered by: `ongoing`, `monitor`, `still valid`
- Default for: C
- Pairs well with: M03, M07
- Self-applied hook: no

## Change log

- `2026-05-02` (v3.0-phase2): initial concept doc.
