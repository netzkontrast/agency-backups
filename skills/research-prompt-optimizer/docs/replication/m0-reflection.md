# M0 — Reflection Baseline (Constraint Block 0)

**File:** `modules/replication/m0-reflection.md`
**Type:** replication
**Mandatory:** YES — appears in every prompt as Constraint Block 0
**Self-applied in Phase 2:** yes (mini-2-Q variant) — sub-phase 4.3 (Module Selection); after module set commits, surface fragile choices and trigger validity

## Purpose

Establishes the **always-active reflection baseline** as Constraint Block 0 in every rendered prompt. Defines five reflection checkpoints (kickoff, mid-run, post-expansion, pre-synthesis, post-synthesis) and the questions to answer at each. Without this baseline, agents drift into search-only mode and lose track of the meta-question "am I still doing the right thing?".

In Phase 2 self-application, M0 runs as a 2-question mini-variant (not full 5-Q) at sub-phase 4.3 — the Phase 2 pipeline is too short for full M0.

## Slot inventory

| Slot name | Type | Filled by | Required | Notes |
|-----------|------|-----------|----------|-------|
| (none) | — | — | — | Frontmatter: `slots: {}` |

The body is a **canonical reflection-baseline text** rendered verbatim. No template variables — the agent fills the reflection answers at runtime per checkpoint.

**Structural markers:** none in body.

## Body composition

- **Section anchor:** `## CONSTRAINT BLOCK 0 — Reflection Baseline (Always Active)`
- **Order constraint:** ALWAYS Block 0 (i.e., FIRST constraint block in every prompt). Source-priority, temporal-scope, output-exclusions blocks come AFTER this one.
- **Composition partner:** M2 Restatement Checkpoint (which forces verbatim re-statement of CB 0 at every step gate).

## Split decision

**Currently:** single file (large — 131 lines)
**Should it split?** Considered. The body has 5 checkpoint definitions + 5 reflection questions per checkpoint = 25 prompts total. Splitting per-checkpoint could be tempting.
**Decision:** No split. The 5 checkpoints share a common reflection-question structure; splitting would require duplicating the structure 5 times. Better to keep coherent.
**Trigger that would force a split:** if a future intent demanded checkpoint-specific reflection question variants (e.g., post-synthesis gets a custom set of 8 questions), per-checkpoint partial files might emerge.

## Future extension points

1. **Checkpoint-cadence control** — currently the 5 checkpoints are at fixed positions (kickoff, mid-run, post-expansion, pre-synthesis, post-synthesis). Could add slot `checkpoint_positions` (`phase2_fill`) to override based on `intent.budget` or `intent.depth`.
2. **Reflection-question library** — currently fixed 5-question set per checkpoint. Could maintain a library of reflection-question sets per intent type (research vs. analysis vs. lifecycle).
3. **Mini-variant for Phase 2 self-application** — currently the self-applied variant uses a 2-question subset (defined in phase2-design-plan.md §10). Could formalize as a separate partial `m0-reflection-mini.md`.

## Open questions

- [ ] The 5-checkpoint cadence is hardcoded. For very short Cat-A intents, kickoff+post-synthesis might be enough. Consider depth-based cadence: surface=2, standard=5, exhaustive=7.
- [ ] Should Phase-2 self-applied M0 emit to a separate `meta-prompt.self_reflection.module_selection` field (per Schema 2 §2.10), keeping it distinct from runtime M0 output? Already specified — yes.

## Catalog cross-reference

- Catalog entry: `catalog.yaml` → `modules.m0-reflection`
- Triggered by: mandatory in every prompt
- Default for category: A, B, C (all)
- Self-applied hook: yes — `catalog.yaml` → `modules.m0-reflection.self_applied_phase2`

## Change log

- `2026-05-02` (v3.0-phase2): initial concept doc; body unchanged (zero brackets — body is canonical reflection-baseline text).
