# Cross-Pollination: a-into-b — Exploration Sanity Pass

**File:** `modules/cross-pollination/a-into-b.md`
**Type:** cross_pollination
**Source category:** A (Exploration)
**Injects into category:** B (Extraction)
**Mandatory:** YES when category routing = B (paired by category, locked at 2 cross-pollinations)

## Purpose

Injects one Exploration-style sanity pass into an Extraction prompt.
Guards against B's core failure mode: "the list of items is complete
and the schema is right" being **silently wrong**.

Two specific checks land in the rendered prompt:
1. Hidden-items query — orthogonal search for missing list members
2. Schema-gap hypothesis — orthogonal check for missing fields

Both surface candidates as **Out-of-Scope** items for user review,
without changing the locked input list or schema.

## Slot inventory

| Slot name | Type | Filled by | Required | Notes |
|-----------|------|-----------|----------|-------|
| (none) | — | — | — | Frontmatter: `slots: {}` |

The module has no template slots. All variables in the body are
**agent-runtime instruction examples** (Category 1 in
`_BRACKET-INVENTORY.md`).

**Structural markers (agent-runtime examples, NOT slots):**

| Bracket | Meaning |
|---------|---------|
| `[i.a]` | Step number placeholder — agent fills with actual step number |
| `[item type]` | Example variable in query template — agent substitutes with actual extraction item type ("regulations", "components", etc.) |
| `[trait that would make it qualify]` | Example variable — agent fills based on extraction context |
| `[NAME]` | Placeholder for the actual hidden item the agent finds |
| `[FIELD]` | Placeholder for the actual missing schema field |
| `[REASON]` | Placeholder for the agent's hypothesis rationale |

## Body composition

- **Section anchor:** `### Step [i.a] — Exploration Sanity Pass (cross-pollination from Category A)`
- **Order constraint:** appears in the Steps section of the rendered
  prompt, ALWAYS as the **last sub-step before any batch finalization**.
  Cross-pollinations are guard-rails — they go at exit gates, not
  entry gates.
- **Composition partner:** when injected into a B-prompt, this CP
  pairs with **c-into-b** (the other locked-pair member). Together
  they cover (a) hidden items / schema gaps and (b) lifecycle drift
  in extraction inputs.

## Pairing logic — why a-into-b + c-into-b for Category B

Category B's `cross_pollination_pair` is `[a-into-b, c-into-b]`.
Both injected; user cannot swap individually. Reasoning:

- **a-into-b (this module):** prevents silent input/schema completeness
  failures (Exploration-style "have I missed something?")
- **c-into-b:** prevents silent input-staleness failures (Lifecycle-
  style "is this list still valid?")

Together they cover the two primary "extraction looked fine but was
wrong" failure paths.

## Split decision

**Currently:** single file
**Should it split?** No — both checks (hidden-items + schema-gap) are
small (~20 lines combined) and conceptually unified ("Exploration
discipline applied to Extraction").
**Trigger that would force a split:** if a future intent demanded
hidden-items WITHOUT schema-gap (e.g., extraction with locked schema
guarantee), splitting into `a-into-b-items.md` and `a-into-b-schema.md`
would let Phase 2 select per-check. Not currently planned.

## Future extension points

1. **Cost knob** — currently both checks always run. Add slot
   `cp_check_budget` (default `both`, options `items-only` /
   `schema-only` / `both`) for cost-constrained intents.
2. **Co-pilot mode** — current checks produce Out-of-Scope candidates
   for user review. Could add `mode: surface | auto-include` flavour
   where `auto-include` adds candidates to the result with a flag.
   Default stays `surface` (safer).
3. **Domain-specific query templates** — the example phrasings
   ("[item type] that [trait...]") are generic. Could specialize
   per-intent-domain via `intent.domain_context`. New optional
   partial `a-into-b-query-templates-<domain>.md` per domain.

## Open questions

- [ ] The body's example-bracket count is high (6 unique). Although
      they're agent-instruction-examples, future readers may
      mis-classify them as slot candidates. Worth a brief inline
      comment in the body? Defer — concept doc covers it.

## Catalog cross-reference

- Catalog entry: `catalog.yaml` → `modules.a-into-b`
- Triggered by signals: n/a (forced when category = B)
- Default for category: B (paired with c-into-b)
- Self-applied hook: no

## Change log

- `2026-05-02` (v3.0-phase2): initial concept doc; body unchanged
  (all 6 unique brackets are agent-runtime instruction examples,
  no slot conversion).
