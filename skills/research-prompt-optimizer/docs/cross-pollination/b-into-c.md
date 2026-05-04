# Cross-Pollination — B into C (Per-Session Locked Schema + Cross-Session Diff)

**File:** `modules/cross-pollination/b-into-c.md`
**Type:** cross-pollination
**Selected when:** `category == C` (paired with `a-into-c` per
`catalog.yaml` → `categories.C.cross_pollination_pair`)
**Self-applied in Phase 2:** no

## Purpose

Imports the Cat-B extraction discipline (locked output schema) into
Cat-C lifecycle research. Per-session output uses a **fixed schema
identical across sessions**, plus a session-N-vs-session-N-minus-1
diff section that surfaces what changed. Counters the failure mode
where lifecycle research output drifts in structure across sessions,
making cross-session comparison impossible.

## Slot inventory

This module has **no frontmatter slots** — body is paste-ready
prose template.

**Structural markers (NOT slots):**

- `[i.b]` — cross-pollination index marker (b-into-c family)
- `[reason]` — agent-runtime placeholder for diff entries (why a
  finding changed, e.g., "new evidence" / "world changed" /
  "previous conclusion superseded")

## Body composition

- **Section anchor:** `### Cross-Pollination — B → C: Per-Session
  Locked Schema + Cross-Session Diff`
- **Order constraint:** rendered after Methods, inside the
  Cross-Pollination block. The locked schema is referenced by every
  M3-Batch iteration (Cat-C uses per-session batches per
  `catalog.yaml` → `categories.C.typical_batches`).
- **Composition partner:** pairs with `a-into-c` (the other Cat-C
  cross-pollination); structurally couples to M3 Batch (provides
  the per-session iteration framework), M11 Assumption-Decay Audit
  (decay events feed the diff), M7 Contradiction Log (cross-session
  contradictions feed the diff).

## Split decision

**Currently:** single file
**Should it split?** No — locked schema and cross-session diff are
one mechanism. Splitting them would lose the diff's anchor.

## Future extension points

1. **Schema-template partial.** The "per-session locked schema"
   could become a sibling partial
   (`partials/lifecycle-session-schema.md`) that this cross-
   pollination references, rather than re-defining inline. Would
   share the schema with `c-lifecycle.md`.
2. **Diff-format slot.** Currently the diff format is implicit prose.
   Add `{{diff_format}}` enum (`prose | structured | both`) to
   accommodate downstream consumers (humans vs. machines).
3. **Diff-significance threshold.** Trivial diffs (typos, minor
   rephrasings) clutter the cross-session record. A
   `{{diff_significance_threshold}}` slot could filter — only
   findings with material change (definition shift, contradicted by
   new source, escalation/de-escalation).

## Open questions

- [ ] How is "previous session" identified? Currently implicit
      (immediately prior). Should there be explicit session-N
      indexing in the persistent knowledge store? Couples to
      c-lifecycle.md's persistent-store-format extension.
- [ ] Diff section vs. World-Change Log (mentioned in
      c-lifecycle.md): same thing or different? Suggest:
      cross-session diff = WHAT changed in our findings; World-
      Change Log = WHY (world moved). They feed each other.

## Catalog cross-reference

- Catalog: `modules.b-into-c`
- Selected when: `category == C` (Cat-C cross-pollination pair)
- Pairs with: `a-into-c`
- Self-applied hook: no

## Change log

- `2026-05-02` (v3.0-phase2): initial concept doc.
