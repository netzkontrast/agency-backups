# M3 — Batch Procedure (Per-Item Iteration Template)

**File:** `modules/replication/m3-batch.md`
**Type:** replication
**Mandatory:** YES when batches are detected (typical for Cat-B per-item, Cat-C per-session); not present for pure Cat-A
**Self-applied in Phase 2:** no (Phase 2 has no batches itself)

## Purpose

Provides the **per-item iteration template** for batch research: research that processes a list of items (regulations, products, candidates, etc.) by applying the same procedure to each. Forces the agent to use a fixed iteration structure with restatement + reflection per item, preventing silent drift across the batch.

## Slot inventory

| Slot name | Type | Filled by | Required | Notes |
|-----------|------|-----------|----------|-------|
| `batch_name` | `phase2_fill` | Phase 2 from intent (e.g., "regulations", "candidates") | yes | Human-readable name of the batch |
| `cardinality` | `phase2_fill` | Phase 2 — `LOW` (≤5), `MEDIUM` (6–20), `HIGH` (>20) | yes | Enum used for cost-budget hints |
| `items` | `phase2_fill` | Phase 2 from intent if known list, else askuser | yes | The actual list of items to iterate over |
| `iteration_steps` | `phase2_fill` | Phase 2 from category-default step set | yes | The procedure applied per item |
| `output_schema_per_iteration` | `phase2_fill` | Phase 2 from `intent.output_format` | yes | What each iteration produces |
| (one more slot in catalog — see catalog entry for full list) | | | | |

**Structural markers (NOT slots):**

| Bracket | Meaning |
|---------|---------|
| `[N]` | Total iteration count — agent fills, OR Phase 3 substitutes from `len(items)` |
| `[ITEM 1]`, `[ITEM 2]`, `[ITEM N]` | Iteration markers — Phase 3 expands per item via `items` slot iteration |
| `[i]`, `[ITEM i]` | Loop-variable placeholders — agent fills at runtime per iteration |
| `[STEP 1 applied to ITEM i]`, `[STEP 2 applied to ITEM i]` | Iteration markers for the per-item steps — Phase 3 expands via `iteration_steps` slot |
| `[LOW / MEDIUM / HIGH]` (in body) | Enum example showing cardinality format — structural |

## Body composition — special Phase-3 semantics

This module has **dual iteration semantics** (items × steps). Phase 3 must:

```python
# Pseudocode — m3 batch render
items = meta_prompt["batches"][i]["items"]              # list of strings
iter_steps = meta_prompt["batches"][i]["iteration_steps"]  # list of step descriptions

# 1. Replace [N] with item count
output = output.replace("[N]", str(len(items)))

# 2. Expand [ITEM 1], [ITEM 2], [ITEM N] block into actual numbered list
items_block = "\n".join(f"{i+1}. {item}" for i, item in enumerate(items))
output = re.sub(r"1\. \[ITEM 1\].*?[N]\. \[ITEM N\]", items_block, output, flags=re.DOTALL)

# 3. Expand [STEP 1..N applied to ITEM i] block similarly
steps_block = "\n".join(f"{j+1}. {step}" for j, step in enumerate(iter_steps))
# ... (substitute into the loop body section)

# 4. Loop variable [i], [ITEM i] stay as-is — agent fills per iteration
```

The body file functions as a **double-loop blueprint** showing both the item list and the per-item step list.

## Body composition — placement

- **Section anchor:** `## Batch Procedure: {{batch_name}} ({{cardinality}}; [N] items)`
- **Order constraint:** appears in the Steps section — after methods are defined but before the first batch step.
- **Composition partner:** M2 Restatement Checkpoint (which prepends to each iteration), M0 Reflection (per-item reflection at the start of each iteration).

## Split decision

**Currently:** single file
**Should it split?** No — the items × steps double-iteration is conceptually unified.
**Trigger that would force a split:** if future intents demanded different per-item procedures (heterogeneous batches), per-procedure variants like `m3-batch-quick.md` and `m3-batch-thorough.md` could emerge.

## Future extension points

1. **Per-batch parallelism control** — currently sequential iteration. Add slot `parallel_iterations` (default 1) for cases where items can be processed in parallel.
2. **Cardinality-driven detail level** — when `cardinality=HIGH` (>20 items), per-item depth could automatically reduce. Add slot `per_item_depth_by_cardinality` (e.g., `{LOW: full, MEDIUM: standard, HIGH: surface}`).
3. **Batch-result aggregation template** — currently the per-item outputs are emitted; aggregation across the batch is left to the agent. Could add a `m3-batch-aggregation.md` partial that templates the batch-level summary.

## Open questions

- [ ] If the `items` list is very long (HIGH cardinality), expanding all items into the prompt blows up token cost. Consider a `items_render_strategy` slot (`enumerate-all` / `sample-N` / `count-only`) for HIGH cardinality.
- [ ] Should `iteration_steps` reuse the same step set across all items, or allow per-item step overrides? Currently uniform; per-item override would be a future extension.

## Catalog cross-reference

- Catalog entry: `catalog.yaml` → `modules.m3-batch`
- Triggered by: detected batch presence in intent
- Default for category: B (per-item batch almost always), C (per-session batch with `cardinality=indefinite`)
- Self-applied hook: no

## Change log

- `2026-05-02` (v3.0-phase2): initial concept doc; body unchanged (all 10 unique brackets confirmed structural — Phase-3 dual-iteration semantics documented in pseudocode).
