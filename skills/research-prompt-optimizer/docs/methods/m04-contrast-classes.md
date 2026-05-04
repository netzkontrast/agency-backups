# M04 — Contrast Classes (Making Implicit Baselines Explicit)

**File:** `modules/methods/m04-contrast-classes.md`
**Type:** method
**Mandatory:** no (default for Cat-A)
**Self-applied in Phase 2:** no

## Purpose

For every evaluative claim ("X is good / fast / scalable / risky"),
force the agent to make the implicit comparison class explicit:
*"compared to what?"*. Counters the failure mode where evaluative
language smuggles in unstated baselines that the reader must guess.

## Slot inventory

This module has **no frontmatter slots** — body is a pure prose method
description. The runtime variable is referenced via the structural
marker `[X]` below.

**Structural markers (NOT slots):**

- `[X]` — visual placeholder in the body's example showing where the
  evaluative claim sits. Not a slot in the v3.0 sense; the executing
  agent reads the example and applies the pattern to whatever
  evaluative claim is in front of them at runtime. There is no
  pre-defined `claim` slot because every evaluative claim during
  research is unique — slot extraction would not help.

## Body composition

- **Section anchor:** `### Method: Contrast Classes`
- **Order constraint:** standalone — placed in methods sequence per
  category default order
- **Composition partner:** pairs with M12 Base-Rate Anchoring (M04
  asks "compared to what?", M12 asks "and how often does that
  baseline actually occur?"). Together they kill weasel-evaluations.

## Split decision

**Currently:** single file
**Should it split?** No — the method is a one-liner discipline:
"every evaluative claim → explicit baseline". Adding structure would
dilute the move.

## Future extension points

1. **Claim-extraction slot.** If experience shows that the agent
   forgets to apply M04 mid-execution, add an `agent_runtime_fill`
   slot `claim_under_evaluation` that the agent must populate before
   stating any evaluative finding — forces the discipline structurally
   rather than relying on the prose anchor alone.
2. **Baseline-source flag.** Sometimes the contrast class itself is
   contested ("compared to GPT-3.5" vs "compared to human baseline").
   A future slot `baseline_source` could record which contrast class
   was used and surface it for reader scrutiny.
3. **Contrast-class catalogue.** For Cat-B benchmarks, the contrast
   class is often standardized (industry baseline, prior-quarter
   number, peer-group median). A future partial
   `partials/standard-contrast-classes.md` could document them.

## Open questions

- [ ] Should this method be promoted to mandatory (every category)?
      The discipline arguably applies to all research, not just Cat-A.
      Currently kept as Cat-A default to avoid prompt bloat.

## Catalog cross-reference

- Catalog entry: `catalog.yaml` → `modules.M04`
- Triggered by signals: `compared to what`, `alternatives`, `versus
  baseline`, `vs`
- Default for category: A
- Pairs well with: M12
- Self-applied hook: no

## Change log

- `2026-05-02` (v3.0-phase2): initial concept doc; body unchanged.
