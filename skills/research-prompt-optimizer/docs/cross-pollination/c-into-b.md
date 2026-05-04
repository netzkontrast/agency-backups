# Cross-Pollination — C into B (World-Change Check, pre + mid-batch)

**File:** `modules/cross-pollination/c-into-b.md`
**Type:** cross-pollination
**Selected when:** `category == B` (paired with `a-into-b` per
`catalog.yaml` → `categories.B.cross_pollination_pair`)
**Self-applied in Phase 2:** no

## Purpose

Imports the Cat-C lifecycle discipline (world-change awareness) into
Cat-B extraction. Before the batch starts AND at the midpoint, the
agent runs an explicit check: did any of the items in this batch
change materially since the source data was authored? Counters the
failure mode where Cat-B comparison matrices accumulate stale
findings because items were processed at the start with old data
that's since been superseded.

## Slot inventory

This module has **no frontmatter slots** — body is paste-ready
prose template.

**Structural markers (NOT slots):**

- `[N]` — number of items in the batch (mirrors `cardinality` from
  M3 Batch — could become a slot)
- `[i.c]` — cross-pollination index marker (c-into-b family)
- `[item type]` — agent-runtime placeholder for the item category
  (e.g., "competitor", "regulation", "paper", "product release")

## Body composition

- **Section anchor:** `### Cross-Pollination — C → B: World-Change
  Check (pre + mid-batch)`
- **Order constraint:** rendered after Methods, inside the
  Cross-Pollination block. Fires twice per Cat-B run: BEFORE
  iteration 1, and at iteration ⌈N/2⌉ (midpoint).
- **Composition partner:** pairs with `a-into-b`; structurally
  couples to M3 Batch (defines the batch this hooks into), M11
  Assumption-Decay Audit (provides the change-detection method),
  M7 Contradiction Log (world-change signals often manifest as
  contradictions with prior data)

## Split decision

**Currently:** single file
**Should it split?** No — pre-check and mid-check are two firings of
one mechanism, not two mechanisms.

## Future extension points

1. **Trigger cadence flexibility.** Currently fixed at "pre + mid".
   For batches with cardinality > 20, additional checkpoints (every
   K iterations) could improve coverage. Add
   `{{world_change_check_cadence}}` slot (default `pre_mid`).
2. **Change-source slot.** Different item types have different
   freshness signals (regulations: official gazette dates; papers:
   citation count deltas; competitors: news monitoring). A
   `{{change_signal_source_per_item_type}}` slot could codify
   per-type sources.
3. **Halt protocol when world-change found mid-batch.** Currently
   the agent flags and continues. A
   `{{world_change_mid_batch_action}}` slot could enable
   `flag_only` | `re_process_completed_items` | `halt_for_user`.

## Open questions

- [ ] When the world-change check finds a change for item K (already
      processed), what happens to items 1..K-1? Currently they
      remain unflagged. Should there be retroactive re-checking?
- [ ] Should this cross-pollination output land in the
      Contradiction Log (cross-source disagreement) or in a separate
      World-Change section (when source disagrees with itself across
      time)? Currently undocumented.

## Catalog cross-reference

- Catalog: `modules.c-into-b`
- Selected when: `category == B` (Cat-B cross-pollination pair)
- Pairs with: `a-into-b`
- Self-applied hook: no

## Change log

- `2026-05-02` (v3.0-phase2): initial concept doc.
