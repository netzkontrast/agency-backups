# M01 — Falsification (Karl Popper's Disconfirmation Principle)

**File:** `modules/methods/m01-falsification.md`
**Type:** method
**Mandatory:** no (default for Cat-A)
**Self-applied in Phase 2:** yes (sub-phase 4.2 — counter-pass on routing decision)

## Purpose

Force the executing agent to actively try to **disprove** the current
top hypothesis on every iteration, not merely accumulate confirmation.
Counters the failure mode where research agents drift into
confirmation theater because confirming evidence is easier to find
than disconfirming.

## Slot inventory

| Slot name | Type | Filled by | Required | Notes |
|-----------|------|-----------|----------|-------|
| `hypothesis` | `agent_runtime_fill` | agent at runtime | yes | The current top hypothesis being tested as a falsifiable statement |
| `disprove_phrase` | `agent_runtime_fill` | agent at runtime | yes | Search phrase designed to surface counter-evidence |
| `failure_mode_phrase` | `agent_runtime_fill` | agent at runtime | yes | The failure-case framing — what observation would constitute disconfirmation |

**Structural markers (NOT slots):**

- `[BRACKETED]` (referenced in body example) — meta-mention of the
  v2.1 bracket convention, not a real placeholder
- `[HYPOTHESIS PLACEHOLDER]` — visual example showing where the
  `hypothesis` slot lands; the actual rendered prompt has
  `{{hypothesis}}`
- `[M01]` — method-anchor placeholder (Phase 3 substitutes
  `short_anchor` from frontmatter)

## Body composition

- **Section anchor:** `### Method: Falsification (Popper Principle)`
- **Order constraint:** standalone — placed in methods sequence per
  category default order
- **Composition partner:** pairs with M02 Steelmanning (steelman the
  hypothesis first, THEN try to falsify it) and M08 What Would Change
  My Mind (M01 finds the disconfirmation, M08 pre-commits to acting
  on it)

## Self-applied hook detail (sub-phase 4.2)

When Phase 2 has decided a routing category via the cascade, M01
fires as a counter-pass: *"What signals would falsify this routing?"*
If non-trivial counter-signals are found AND the cascade did not
already escalate to the askuser branch, the hook forces the askuser.
Output lands in `meta-prompt.self_reflection.routing.falsification_check`.

## Split decision

**Currently:** single file
**Should it split?** No — falsification is one tight loop. The three
slots all describe one ongoing hypothesis-test cycle.

## Future extension points

1. **Hypothesis-pool slot.** Currently `hypothesis` is singular. If
   research domains demand multi-hypothesis falsification (Cat-C
   lifecycle research often), a `hypothesis_pool` (list) slot with
   per-hypothesis falsification status could replace the singular form.
2. **Disconfirmation threshold flag.** `escape_criterion` says "≥3
   orthogonal disconfirmations OR contra-evidence >20%". Hard-coded.
   Surface as `{{disconfirmation_threshold}}` (phase2_fill_or_runtime)
   for domain-specific calibration.
3. **Bayesian-prior coupling.** When M05 is also active, the prior
   should inform what counts as "non-trivial" disconfirmation. Future
   pairing protocol could chain M05 → M01 with explicit data flow.

## Open questions

- [ ] Should the self-applied hook use a different `disprove_phrase`
      than the agent-runtime hook? Phase-2-internal: "what would
      falsify this routing?" vs. agent-runtime: "what would falsify
      this hypothesis?". Currently both share the slot semantics.

## Catalog cross-reference

- Catalog entry: `catalog.yaml` → `modules.M01`
- Triggered by signals: `prove`, `show that`, `validate`
- Default for category: A
- Pairs well with: M02, M08
- Self-applied hook (catalog index): `sub_phase: 4.2`,
  `depth_active: [standard, exhaustive]`

## Change log

- `2026-05-02` (v3.0-phase2): initial concept doc; frontmatter
  `self_applied_phase2:` block added to sync with catalog index.
