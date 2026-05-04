# M05 — Bayesian Prior Surfacing

**File:** `modules/methods/m05-bayesian-prior.md`
**Type:** method
**Mandatory:** no (auto-added if `intent.priors_and_constraints.known_priors != null`)
**Self-applied in Phase 2:** yes — sub-phase 4.2 (Routing), hook role: write down prior + confidence BEFORE category cascade runs

## Purpose

Force the executing agent to state, before evidence-gathering, what it
expects to find and with what confidence. After research, state the
updated belief and the magnitude of update. This turns research into a
**legible update process** instead of confirmation theatre.

## Slot inventory

| Slot name | Type | Filled by | Required | Notes |
|-----------|------|-----------|----------|-------|
| `expected_finding` | `phase2_fill` | `intent.priors_and_constraints.known_priors` (if present) | yes | If intent doesn't have a prior, Phase 2 leaves slot for `agent_runtime_fill` |
| `prior_reason` | `phase2_fill` | askuser if missing (free_text "Warum dieser Prior?") | yes | One-line justification |

**Structural markers (NOT slots):**

- `[X]`, `[Y]` in the howto — schema examples showing the agent the
  prior-statement format. They are pedagogy, not template slots.
- `[LOW / MEDIUM / HIGH]` — confidence enum that the agent picks from.
  Stays as structural enum; not a `phase2_fill` because the agent
  decides confidence after their own reflection.
- `[MINOR / MODERATE / MAJOR]` — same as above but for update magnitude.

## Body composition

- **Section anchor:** `### Method: Bayesian Prior Surfacing`
- **Order constraint:** appears AFTER the constraint-blocks section
  (so the prior statement comes after the agent has internalized
  the constraints) and BEFORE the ReAct loop (so it sets up the
  baseline that the loop updates).
- **Composition partner:** pairs with M07 Contradiction Log — when
  evidence contradicts a stated prior, M07 logs it; M05 supplies
  the prior to contradict.

## Split decision

**Currently:** single file
**Should it split?** No — the prior-statement and updated-belief steps
are too tightly coupled to separate. They share the same conceptual
unit "auditable update".
**Trigger that would force a split:** if we ever wanted prior-only
(no updated-belief) variant for short Cat-A explorations, that would
become a sibling `m05b-prior-only.md`. Not currently planned.

## Future extension points

1. **Confidence calibration scale** — add `confidence_scale` slot
   that takes a calibration table (e.g., Tetlock's 9-point scale) for
   teams that want stricter quantification. Stays optional.
2. **Multi-hypothesis prior** — extend slot inventory with
   `expected_finding_alternatives[]` for cases where the user has
   competing priors (currently single prior only).
3. **Bayesian update math** — for quantitative work, an optional
   block that computes posterior odds explicitly. Would land as a
   new partial `m05-bayes-math.md` included only when intent flags
   `quantification: numeric`.

## Open questions

- [ ] Does `prior_reason` need a length cap (currently unbounded)?
      Would 200 chars suffice? Discuss when first long-form intent
      surfaces.

## Catalog cross-reference

- Catalog entry: `catalog.yaml` → `modules.M05`
- Triggered by signals: `prior`, `expectation`, `before evidence`, `update belief`
- Default for category: none — auto-added by signal/intent presence
- Self-applied hook: yes — see `catalog.yaml` → `modules.M05.self_applied_phase2`

## Change log

- `2026-05-02` (v3.0-phase2): initial concept doc; converted `[PLACEHOLDER expected finding]` → `{{expected_finding}}`, `[PLACEHOLDER reason]` → `{{prior_reason}}`. Preserved structural examples `[X]`, `[Y]`, enum brackets.
