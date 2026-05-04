# Category C — Lifecycle (Long-Running Context Engineering)

**File:** `modules/categories/c-lifecycle.md`
**Type:** category
**Mandatory:** rendered when Phase 2 routes intent to Cat-C
**Self-applied in Phase 2:** no

## Purpose

Provides the **Epistemological Layer** block for research that
spans multiple sessions over weeks or months — regulatory watch,
quarterly market briefs, ongoing competitor intel, longitudinal
literature reviews. The block forces the executing agent to (a)
maintain a persistent knowledge store, (b) re-anchor at every
session start, (c) compact older material without silent deletion,
(d) distinguish "sources disagree" from "the world changed".

## Slot inventory

This module has **no frontmatter slots**. Body is a paste-ready prose
block.

**Structural markers (NOT slots):**

- `[N tokens / N entries]` (in point 3) — placeholder for the compaction
  threshold. Currently a literal example, not parameterized. See
  Future Extensions for the slot proposal.

## Body composition

- **Section anchor:** `## Epistemological Layer — Category C (Lifecycle)`
- **Order constraint:** rendered after Meta-Header, before Constraint
  Blocks
- **Composition partner:** every Cat-C prompt activates M03 Pre-Mortem,
  M07 Contradiction Log, M09 Red Team, M11 Assumption-Decay (per
  `catalog.yaml` → `categories.C.default_methods`). The Resumption
  Protocol in point 2 *requires* M11 to be active — Phase 2 should
  reject Cat-C plans that drop M11.

## Split decision

**Currently:** single file
**Should it split?** No — the 5 points form one resumable-research
behavioural contract. The Resumption Protocol (point 2) and World-
Change Log (point 4) are tightly coupled and would lose force if
separated.

## Future extension points

1. **Compaction-threshold slot.** Convert `[N tokens / N entries]` to
   `{{compaction_threshold}}` (phase2_fill, default `10000 tokens` or
   `50 entries`), filled from `intent.session_budget` if present, else
   sensible default. Phase 1 schema would need a corresponding field.
2. **Persistent-store format partial.** Point 1 mentions "format
   specified in Expectations section". A future `partials/lifecycle-
   store-schema.md` could codify the canonical store format
   (frontmatter + sections for active questions, contradictions, world-
   changes, assumption decay log).
3. **World-Change Log as standalone module.** If Cat-C usage grows,
   the World-Change Log mechanism (point 4) could become its own
   replication mechanism `m5-world-change-log.md`, sibling to M3 Batch
   and M4 Pre-Synthesis.
4. **Cadence flag.** Currently silent on session cadence. Add
   `{{session_cadence}}` (weekly / monthly / quarterly) to inform the
   compaction-threshold default and the Resumption Protocol expected
   delta.

## Open questions

- [ ] Resumption Protocol step (d) requires M11 Assumption-Decay
      Audit. Should Phase 2 enforce this dependency mechanically (auto-
      add M11 if Cat-C and M11 absent) or just warn?
- [ ] World-Change Log distinct from Contradiction Log: is the
      distinction maintainable for the executing agent without explicit
      decision tree, or does it need a sub-flowchart in the body?

## Catalog cross-reference

- Catalog entry: `catalog.yaml` → `categories.C`
- Signal words: `ongoing`, `monitor`, `track over months`, `incremental`,
  `weekly refresh`, `monthly refresh`, `quarterly refresh`, `watch list`,
  `running brief`, `intelligence feed`
- Default methods: M03, M07, M09, M11
- Default structural framework: RISEN
- Cross-pollination pair: `a-into-c`, `b-into-c`
- Typical batches: `per-session`

## Change log

- `2026-05-02` (v3.0-phase2): initial concept doc; body unchanged.
