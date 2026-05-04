# M4 — Pre-Synthesis Integrity Check (8-item)

**File:** `modules/replication/m4-pre-synthesis.md`
**Type:** replication
**Mandatory:** yes (always rendered into every prompt)
**Self-applied in Phase 2:** yes (sub-phase 4.8 — 6-item Phase-2 variant, BLOCKING all depths)

## Purpose

Hard gate before the agent commits to synthesis: 8 yes/no items the
agent must explicitly answer. Failed items block synthesis and force
remediation. Counters the failure mode where the agent rolls into
synthesis while a constraint was violated, a contradiction unlogged,
or a method was silently skipped on iteration N.

## Slot inventory

This module has **no agent-runtime slots** — the 8 checklist items
are fixed yes/no anchors. The agent fills the answers inline at
runtime, but the items themselves are not parameterized.

**Structural markers (NOT slots — fixed checklist enumeration):**

- `[K]`, `[M]`, `[N]`, `[P]` — counter placeholders the agent fills at
  runtime (e.g., "queries expanded along K axes")
- `[enumerate methods, including M13 Adversarial Query Expansion]` —
  agent-runtime instruction to list active methods at synthesis
- `[enumerate]` — agent-runtime instruction for items requiring lists

## Body composition

- **Section anchor:** `## Pre-Synthesis Integrity Check`
- **Order constraint:** rendered immediately before the Synthesis
  section. Synthesis cannot begin until this check passes.
- **Composition partner:** consumes signals from M0 Reflection
  (item: did baseline reflection fire each step?), M1 Constraint
  Blocks (items: were CB-1, CB-2, CB-3 honored?), M2 Restatement
  (item: did restatement fire each step?), M7 Contradiction Log
  (item: was every contradiction logged?), M13 Query Expansion
  (item: was M13 invoked at minimum cadence?)

## Self-applied hook detail (sub-phase 4.8 — BLOCKING for all depths)

Phase 2 runs the **6-item variant** (NOT the 8-item agent-runtime
version) before plan-view rendering. The 6 items target Phase-2
plan integrity:
1. Do all selected methods have valid `triggered_by_signals` in intent?
2. Are constraint blocks complete (CB-0..3)?
3. Does the framework choice match override-trigger evaluation?
4. Are batches detected with cardinality?
5. Is the cross-pollination pair correctly resolved from category?
6. Does `self_reflection.contradictions[]` show no unresolved
   internal-intent inconsistencies?

**Failed items block plan-view render and force a self-correct
loop.** This is the only Phase-2 self-applied hook that is
**blocking** — others (M01, M03, M05, M07, M13, m0-reflection) log
but do not block.

## Split decision

**Currently:** single file
**Should it split?** No — the integrity check is one gate; splitting
defeats the "all-or-nothing pass" semantics.

## Future extension points

1. **Item-level severity tags.** Currently all 8 items block synthesis
   equally. Adding `severity: hard | soft` per item would let some
   items warn-only (e.g., "minor contradictions logged") rather than
   block.
2. **Domain-specific item extensions.** Cat-B benchmark research
   could add item 9: "every numerical claim has base-rate context per
   M12". Cat-C could add: "World-Change Log distinct from
   Contradiction Log". A `{{domain_extra_items}}` slot driven by
   category could append.
3. **Self-correction protocol details.** Current Phase-2 behavior on
   block-fail is "force self-correct loop" — undefined what that
   means exactly. Spec needs a sub-section, possibly its own partial.

## Open questions

- [ ] The 6-item Phase-2 variant vs. 8-item agent-runtime variant:
      is the 2-item gap intentional or accidental? Items 7 and 8
      (agent-runtime) are about loop completeness — Phase 2 has no
      loop to complete. So gap is intentional.
- [ ] Should the Phase-2 self-applied variant emit its own integrity
      report into `meta-prompt.self_reflection.integrity_check` even
      on success? Currently only on failure.

## Catalog cross-reference

- Catalog: `modules.m4-pre-synthesis`
- Mandatory: yes
- Self-applied hook (catalog): `sub_phase: 4.8`,
  `depth_active: [surface, standard, exhaustive]` (all depths),
  `variant: '6-item Phase-2 (not 8-item agent-runtime)'`,
  blocking: implicit (failed → blocks render)

## Change log

- `2026-05-02` (v3.0-phase2): initial concept doc.
