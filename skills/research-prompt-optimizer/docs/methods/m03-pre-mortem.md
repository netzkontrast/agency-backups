# M03 — Pre-Mortem Analysis

**File:** `modules/methods/m03-pre-mortem.md`
**Type:** method
**Mandatory:** no (default for Cat-C)
**Self-applied in Phase 2:** yes (sub-phase 4.8 — top-3 failure modes for the plan, top-5 if exhaustive)

## Purpose

Force the executing agent to imagine the research run has already
failed, then enumerate the most likely causes BEFORE starting. This
is Gary Klein's pre-mortem technique applied to research. Counters
the failure mode where agents barrel into execution without
considering structural risks (stale sources, biased domains,
contested temporal windows).

## Slot inventory

| Slot name | Type | Filled by | Required | Notes |
|-----------|------|-----------|----------|-------|
| `topic` | `phase2_fill` | `intent.research_question` (truncate 100 chars) | yes | Frames "Imagine our research on `<topic>` has failed catastrophically" |
| `source_type` | `agent_runtime_fill` | agent at runtime | no | A specific source-type identified as a failure risk (e.g., "vendor whitepapers" for biased pool) |
| `temporal_window` | `agent_runtime_fill` | agent at runtime | no | A specific temporal window identified as risky (e.g., "post-2024 EU regulatory churn") |

**Structural markers (NOT slots):**

- `[PLACEHOLDER source type]` — visual cue showing where
  `source_type` lands in the body example; rendered prompt has
  `{{source_type}}`

## Body composition

- **Section anchor:** `### Method: Pre-Mortem Analysis`
- **Order constraint:** placed **first** in the methods sequence when
  active — pre-mortem must run before other methods set the agent's
  belief-state
- **Composition partner:** pairs with M07 Contradiction Log (pre-
  mortem identifies contradictions to watch for; M07 logs them when
  encountered) and M09 Red Team (pre-mortem is silent self-criticism;
  M09 is structured adversarial review)

## Self-applied hook detail (sub-phase 4.8)

Before plan-view rendering, M03 generates the top-3 (or top-5 if
`intent.depth=exhaustive`) plan-failure modes. Items land in
`meta-prompt.self_reflection.pre_mortem[]` and are rendered into the
plan view so the user sees predicted weak points alongside the plan.

## Split decision

**Currently:** single file
**Should it split?** No — pre-mortem is one cohesive technique. The
two optional slots (`source_type`, `temporal_window`) are dimensions
of the same exercise, not separate methods.

## Future extension points

1. **Failure-mode taxonomy.** Currently free-text. A controlled
   vocabulary (`source_bias` | `temporal_gap` | `definitional_drift` |
   `scope_creep` | `confirmation_lock`) would enable cross-prompt
   trend analysis: which failure modes recur for which research types?
2. **Pre-mortem batch.** For Cat-C lifecycle research, run pre-mortem
   at session start AND at every Resumption Protocol checkpoint —
   batch it explicitly (`per-resumption` cardinality, see M3 Batch).
3. **Half-time rerun trigger.** `escape_criterion` says "Run once at
   start + once at halfway". Currently agent-managed. A
   `{{halftime_token_threshold}}` slot could make halfway objective.

## Open questions

- [ ] Self-applied output_size: 3 vs. 5 — driven by `intent.depth`.
      Should depth=standard ALSO get 5 if the pre-mortem identifies
      genuinely independent failure modes (i.e., quality > quantity
      threshold)? Currently fixed at 3 for standard.

## Catalog cross-reference

- Catalog entry: `catalog.yaml` → `modules.M03`
- Triggered by signals: `risk`, `what could go wrong`, `plan for
  failure`, `fail`
- Default for category: C
- Pairs well with: M07, M09
- Self-applied hook (catalog): `sub_phase: 4.8`, `output_size:
  '3 items (standard) | 5 items (exhaustive)'`,
  `depth_active: [standard, exhaustive]`

## Change log

- `2026-05-02` (v3.0-phase2): initial concept doc.
