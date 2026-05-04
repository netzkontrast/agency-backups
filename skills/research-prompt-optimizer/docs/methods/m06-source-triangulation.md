# M06 — Source Triangulation

**File:** `modules/methods/m06-source-triangulation.md`
**Type:** method
**Mandatory:** no (default for Cat-B)
**Self-applied in Phase 2:** no (Phase 2 has only one source — `intent.yaml` — so triangulation does not apply)

## Purpose

For every factual claim, require ≥3 independent sources, at least
one of which is a primary source (regulator, official statistics,
research paper, manufacturer spec). Counters the failure mode where
agents accept the first plausible result, often from a content-farm
aggregator that simply rewrote one upstream source.

## Slot inventory

| Slot name | Type | Filled by | Required | Notes |
|-----------|------|-----------|----------|-------|
| `claim` | `agent_runtime_fill` | agent at runtime | yes | The factual claim being triangulated |

**Structural markers:** none. Body is pure prose.

## Body composition

- **Section anchor:** `### Method: Source Triangulation`
- **Order constraint:** standalone — placed in methods sequence per
  category default order
- **Composition partner:** pairs with M07 Contradiction Log (when
  triangulation finds disagreement instead of confirmation, M07 logs
  it) and M12 Base-Rate Anchoring (M06 confirms the claim, M12
  contextualizes it against frequency)

## Split decision

**Currently:** single file
**Should it split?** No — triangulation is one tight discipline.
Source-tier definitions could be externalized but that's an extension,
not a split (see Future Extensions).

## Future extension points

1. **Source-tier vocabulary slot.** Currently "primary source" and
   "aggregator" are defined in prose. A
   `{{source_tier_taxonomy}}` slot (fill_from `intent.known_constraints
   .sources` if present, else default) could make tier definitions
   domain-adaptable: legal research has different tiers (court > reg
   > commentary) than scientific (journal > preprint > blog).
2. **Triangulation-failure protocol.** When ≥3 independent sources
   cannot be found, current behaviour is to flag (per
   `escape_criterion`). A `{{triangulation_failure_action}}` slot
   could define `flag_only` | `degrade_confidence` | `halt_and_ask`
   per intent.
3. **Source-independence test.** Currently the agent self-judges
   independence. A `{{independence_test_protocol}}` slot could codify
   common-corpus checks (cross-citations, shared funding, etc.).

## Open questions

- [ ] The "≥3 sources" rule is opinionated and intent-agnostic.
      Should it be `{{min_independent_sources}}` (phase2_fill_or_runtime)
      with default 3, configurable per intent?
- [ ] "Aggregators count as one source" — should the rule be
      strictness-flagged (`strict` | `lenient`) for cases where
      multiple aggregators citing different upstream sources is
      genuinely confirmatory?

## Catalog cross-reference

- Catalog entry: `catalog.yaml` → `modules.M06`
- Triggered by signals: `cite sources`, `verify with multiple`,
  `cross-check`
- Default for category: B
- Pairs well with: M07, M12
- Self-applied hook: no

## Change log

- `2026-05-02` (v3.0-phase2): initial concept doc.
