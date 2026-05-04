# RISEN — Role · Input · Steps · Expectations · Narrowing

**File:** `modules/frameworks/risen.md`
**Type:** framework
**Role:** structural_layer (sits on top of the ReAct agentic spine)
**Default for category:** A, B, C (all three — RISEN is the catalog default whenever no override fires)
**Self-applied in Phase 2:** no

## Purpose

The default structural framework for v3.0. RISEN gives the executing
agent a 5-section macro-structure: **R**ole (who am I), **I**nput
(what data am I given), **S**teps (what procedure do I follow),
**E**xpectations (what must the output contain), **N**arrowing (what
constraints bound this). Used as the structural layer for ~80% of
generated prompts; only overridden when a more specialized framework
(TIDD-EC, CO-STAR, CARE, CRISPE) better matches the intent's
structural demand.

## Slot inventory

| Slot name | Type | Filled by | Required | Notes |
|-----------|------|-----------|----------|-------|
| `role` | `phase2_fill` | mirror from `intent.routing_hints` (typically) | yes | The agent role for this run, e.g. "regulatory analyst" — the only slot RISEN itself defines |

**Structural markers:** none. Body is the paste-ready RISEN
template with the 5 section anchors.

## Body composition

- **Section anchors:** 5 fixed sections — `## Role`, `## Input`,
  `## Steps`, `## Expectations`, `## Narrowing`
- **Order constraint:** RISEN's section ordering is binding — the
  executing agent must restate Role + Narrowing first (per RISEN
  protocol), then proceed to Steps
- **Composition partner:** RISEN sits as the structural layer **above**
  the always-active ReAct agentic spine. Inside each Step (the "S"
  in RISEN), ReAct fires its reason → act → observe loop.

## Split decision

**Currently:** single file
**Should it split?** No — RISEN is a 5-letter acronym; the sections
are interlocked. Splitting would lose the "restate Role and Narrowing
first" enforceable protocol.

## Future extension points

1. **Per-section slot expansion.** Currently only `role` is a slot.
   Could expand to `{{narrowing}}` (filled from
   `intent.known_constraints`), `{{expectations}}` (filled from
   `intent.output_format`). Currently these flow as prose because
   Phase 2 generates them inline; making them slots would enable
   sub-section overrides.
2. **RISEN-N variant.** RISEN-N adds an explicit "Negative Examples"
   section. If empirical use shows Cat-B benchmarks need this
   regularly, sibling module `risen-n.md` could provide it.

## Open questions

- [ ] The catalog has `override_trigger: None` for RISEN, marking it
      as the default. Should it have an explicit
      `default_trigger: 'no other framework override fires'` for
      symmetry with the others?

## Catalog cross-reference

- Catalog: `modules.risen`
- Override trigger: none (default)
- Default for: A, B, C
- Pairs well with: ReAct (always), every other framework when bespoke
  synthesis combines them
- Self-applied hook: no

## Change log

- `2026-05-02` (v3.0-phase2): initial concept doc.
