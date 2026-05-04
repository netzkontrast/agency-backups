# Cross-Pollination — A into C (Framing Re-Opening)

**File:** `modules/cross-pollination/a-into-c.md`
**Type:** cross-pollination
**Selected when:** `category == C` (paired with `b-into-c` per
`catalog.yaml` → `categories.C.cross_pollination_pair`)
**Self-applied in Phase 2:** no

## Purpose

Imports the Cat-A exploration discipline into Cat-C lifecycle
research. Specifically: every Nth session, the agent re-opens the
**framing** of the research question — not just the findings — and
checks whether an alternative frame would reinterpret the
accumulated evidence differently. Counters the failure mode where
long-running research silently locks into the original Session-1
frame even when the world or the question has shifted.

## Slot inventory

This module has **no frontmatter slots** — body is paste-ready
prose template.

**Structural markers (NOT slots — preserved as visual placeholders
for the agent to substitute at runtime):**

- `[FRAME X]` — the original framing of the research question
- `[FRAME Y]`, `[FRAME Y that reinterprets the same phenomenon
  differently]` — the alternative frame the agent must construct
- `[Nth]` — the session number at which framing re-opens fire (every
  4th session per body content; could become a slot)
- `[i.a]` — cross-pollination index marker (a-into-c family)

## Body composition

- **Section anchor:** `### Cross-Pollination — A → C: Framing Re-Opening`
- **Order constraint:** rendered after the standard Methods section,
  inside the Cross-Pollination block. Cat-C cross-pollination block
  always contains `a-into-c` + `b-into-c` paired.
- **Composition partner:** pairs with `b-into-c` (the other
  cross-pollination Cat-C uses) and structurally couples to M11
  Assumption-Decay Audit (which checks foundational assumptions;
  framing re-opening checks the question itself)

## Split decision

**Currently:** single file
**Should it split?** No — framing re-opening is one tight discipline.
The two phases (state original frame + construct alternative) are
inseparable.

## Future extension points

1. **Cadence slot.** "Every 4th session" is hard-coded in body text.
   Surface as `{{framing_reopen_cadence}}` (default 4) for cases
   where research velocity demands more or less frequent re-opens.
2. **Frame-library partial.** For domains with stable alternative
   frames (e.g., regulatory research alternates between "compliance
   lens" and "competitive-advantage lens"), a future
   `partials/standard-frame-pairs.md` could provide canonical
   alternative framings.
3. **Frame-shift action protocol.** When alternative frame produces
   materially different interpretation, current behavior is "log
   and surface". A `{{frame_shift_action}}` slot could codify
   `log_only` | `re_evaluate_findings` | `halt_for_user_review`.

## Open questions

- [ ] Should framing re-opening output land in the World-Change Log
      (mentioned in c-lifecycle.md) or in its own log section?
      Currently undocumented.
- [ ] Does framing re-opening apply to Cat-A → Cat-C only, or could
      it generalize to Cat-A → Cat-A long-running explorations? If
      the latter, this becomes a sibling cross-pollination
      `a-into-a-long`.

## Catalog cross-reference

- Catalog: `modules.a-into-c`
- Selected when: `category == C` (Cat-C cross-pollination pair)
- Pairs with: `b-into-c` (the other Cat-C cross-pollination)
- Self-applied hook: no

## Change log

- `2026-05-02` (v3.0-phase2): initial concept doc.
