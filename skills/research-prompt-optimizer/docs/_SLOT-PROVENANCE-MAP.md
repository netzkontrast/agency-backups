# Slot Provenance Map

> Cross-module index: every slot type in v3.0 grouped by FILL SOURCE.
> Used to verify that intent fields actually exist for every
> `phase2_fill from intent` slot, and to spot duplicate / divergent
> slot-naming across modules.

## Slot types (recap from `meta-prompt-spec.md` §6)

- **`phase2_fill`** — filled by Phase 2 from `intent.yaml` field
- **`phase2_fill_or_runtime`** — filled by Phase 2 if intent has it,
  else left for the executing agent
- **`agent_runtime_fill`** — left as `{{slot}}` in rendered prompt;
  agent fills during execution
- **`fill_from`** — programmatically computed by Phase 3 render script
  (e.g., from a list of active modules)

## Slots filled from `intent.research_question`

| Slot | Module | Truncate? | Notes |
|------|--------|-----------|-------|
| `topic` | `methods/m03-pre-mortem.md` | 100 chars | framing of pre-mortem |
| `topic` | `methods/m02-steelmanning.md` | — | (TBD: concept doc) |
| `topic` | `methods/m04-contrast-classes.md` | — | (TBD) |
| `research_question` | `partials/meta-header.md` | — | full text in header |
| `research_question` | `frameworks/react.md` | — | shown in observe phase |

## Slots filled from `intent.research_question_unpacked`

| Slot | Module | Notes |
|------|--------|-------|
| `unpacked_question` | `partials/meta-header.md` | structured form |
| `category_signal` | (n/a — used for routing, not slot) | — |

## Slots filled from `intent.priors_and_constraints.known_priors`

| Slot | Module | Notes |
|------|--------|-------|
| `known_priors_block` | `methods/m05-bayesian-prior.md` | conditional on field present |

## Slots filled from `intent.temporal_scope`

| Slot | Module | Notes |
|------|--------|-------|
| `temporal_scope_text` | `replication/m1-constraint-blocks.md` (Block 2) | direct copy |

## Slots filled from `intent.output_format`

| Slot | Module | Notes |
|------|--------|-------|
| `output_format_directive` | `partials/meta-header.md` | — |
| `output_format_directive` | `verification/final-checklist.md` | for end-of-run check |

## Slots filled from `intent.known_constraints`

| Slot | Module | Notes |
|------|--------|-------|
| `source_priority_block` | `replication/m1-constraint-blocks.md` (Block 1) | adapted from constraints.sources if present |
| `output_exclusions_block` | `replication/m1-constraint-blocks.md` (Block 3) | adapted from constraints.exclusions |

## Slots filled programmatically (`fill_from`)

| Slot | Module | Source | Notes |
|------|--------|--------|-------|
| `active_method_anchors` | `frameworks/react.md` | active method short_anchors | substitutes `[M__]` placeholders |
| `active_method_anchors` | `partials/react-loop-anchored.md` | (same) | partial inherits |
| `active_methods_list` | `partials/meta-header.md` | active methods set | rendered as table |
| `active_constraint_blocks_list` | `partials/meta-header.md` | active CBs | rendered as numbered list |
| `category_label` | `partials/meta-header.md` | `intent.routing_hints.category_signal` | "Compare/Decide" etc. |

## Slots filled by askuser (Phase 2 specific)

| Slot | Module | Phase 2 sub-phase | Notes |
|------|--------|---------|-------|
| `orthogonal_axis` | `methods/m13-adversarial-query-expansion.md` | 2.6 (bundled askuser) | Q4 v1.1 decision |

## Slots filled at agent runtime (`agent_runtime_fill`)

| Slot | Module | What the agent fills |
|------|--------|---------------------|
| `hypothesis` | `methods/m01-falsification.md` | the hypothesis to falsify |
| `disprove_phrase` | `methods/m01-falsification.md` | the search phrase for counter-evidence |
| `failure_mode_phrase` | `methods/m01-falsification.md` | the failure case framing |
| `source_type` | `methods/m03-pre-mortem.md` | a source-type identified as risk |
| `temporal_window` | `methods/m03-pre-mortem.md` | a temporal-window risk |
| `current_assumption` | `methods/m11-assumption-decay.md` | the assumption being tested |
| `current_claim` | `methods/m07-contradiction-log.md` | the claim under contradiction-check |
| `mind_change_threshold` | `methods/m08-what-would-change-my-mind.md` | the evidence threshold |

## Slots that need attention / TBD

The slot-fix sweep is complete (2026-05-02). Below are the slots
that were newly defined during the sweep, with their final
provenance:

### Finalized in `frameworks/synthesis.md` (template-fix Phase A)

| Slot | Type | Filled by | Notes |
|------|------|-----------|-------|
| `bespoke_acronym` | `phase2_fill` | Claude generates from components | unchanged from v3.0 |
| `components` | `phase2_fill` | Claude generates (structured list) | unchanged from v3.0 |
| `components_render_block` | `fill_from` `components` | Phase 3 emits one bullet per component: `- **<letter> — <name>**: <definition>` | NEW |
| `provenance_render_block` | `fill_from` `components` | Phase 3 emits one provenance line per component: `- Component <letter> is adapted from the <source_framework> framework.` | NEW |
| `first_action_directive` | `phase2_fill` | Claude generates from components | NEW |

### Finalized in `replication/m2-restatement-checkpoint.md` (template-fix Phase A)

| Slot | Type | Filled by | Notes |
|------|------|-----------|-------|
| `active_constraint_blocks` | `fill_from` `constraint_blocks` | Phase 3 from active CB set | unchanged |
| `active_methods` | `fill_from` `selected_methods` | Phase 3 from active method set | unchanged |
| `cb_restatement_block` | `fill_from` `active_constraint_blocks` | Phase 3 emits CB restatement lines with verbatim instruction | NEW |
| `method_restatement_block` | `fill_from` `active_methods` | Phase 3 emits method restatement lines with verbatim instruction | NEW |
| `step_or_iteration_label` | `agent_runtime_fill` | Agent at runtime ("STEP N" or "ITERATION N") | NEW |
| `step_title` | `agent_runtime_fill` | Agent at runtime | NEW |
| `step_content` | `agent_runtime_fill` | Agent at runtime | NEW |

### Finalized in `replication/m3-batch.md` (template-fix Phase A)

| Slot | Type | Filled by | Notes |
|------|------|-----------|-------|
| `confidence_label` | `agent_runtime_fill` (enum: LOW/MEDIUM/HIGH) | Agent at runtime per iteration | NEW (was inline `[LOW / MEDIUM / HIGH]` bracket) |

### Frontmatter sync (Phase A.5)

These modules had `self_applied_phase2:` blocks listed in
`catalog.yaml`'s `self_applied_phase2_index` but missing from their
own file frontmatter. Synced:

- `methods/m01-falsification.md` (sub_phase 4.2)
- `methods/m13-adversarial-query-expansion.md` (sub_phase 4.6)
- `replication/m0-reflection.md` (sub_phase 4.3, variant: 2-Q mini)

### Per-module slot extension proposals (parked for future iteration)

Each per-module concept doc in `docs/<type>/<id>.md` carries a
"Future extension points" section with proposed slot additions.
None are mandatory for v3.0; they document where the system can
grow without breaking existing contracts. Common patterns:

- **Threshold slots** (M01 disconfirmation, M06 source count, M11
  audit cadence) — convert hard-coded constants to
  `phase2_fill_or_runtime` slots driven by intent.
- **Aggregator slots** (M08 precommitment log, M09 red-team log) —
  per-method runtime accumulators surfaced at synthesis.
- **Cadence slots** (a-into-c framing reopen, c-into-b world-change
  check) — convert hard-coded "every Nth" to configurable cadence.

## Naming conventions in v3.0

- All slot names: `lower_snake_case`
- Iteration-context slots use singular: `step_title` not `steps_title`
- Boolean-ish slots use yes/no fragments: `is_…`, `has_…`
- Block-content slots end in `_block`: `source_priority_block`
- List-content slots end in `_list`: `active_methods_list`

Naming violations across modules will be flagged here as the sweep proceeds.
