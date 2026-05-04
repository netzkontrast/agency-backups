---
id: final-checklist
type: verification
file: "modules/verification/final-checklist.md"
full_name: "Self-Verification Checklist for the Executing AI"
short_anchor: "FinalChecklist"
items_count: 11
slots: {}
---

# Final Checklist (11-item) — Self-Verification for the Executing AI

> Inserted at the very end of every rendered research prompt, just
> before the synthesis is delivered. The executing AI runs through
> this checklist in writing; any failing item blocks delivery until
> repaired.
>
> This checklist is the **last verification gate** before the
> synthesis goes back to the user.

## Rendered Block (composed into the research prompt)

```markdown
## SELF-VERIFICATION CHECKLIST (11 items)

Before you deliver the Synthesis, verify each of these in writing.
A "done" by memory does not count — write one line per item
confirming you completed it.

- [ ] **1. Restatement integrity.** Every major step began with a
      verbatim Restatement Checkpoint that included CONSTRAINT BLOCK 0
      first, followed by all other active CBs and all active methods
      (with M13 always present).

- [ ] **2. Reflection regime (CONSTRAINT BLOCK 0).** All five mandatory
      reflection checkpoints were honored in writing: Kickoff, Mid-run,
      Post-Query-Expansion, Pre-synthesis, Post-synthesis. Confirm:
      *"I wrote [N] reflection entries at the following checkpoints:
      [enumerate]."* If N is below 5, write the missing reflections
      now before continuing.

- [ ] **3. Method invocation audit.** Every method listed in the active
      methods palette has at least one concrete invocation visible in
      the Reason history. Methods with zero invocations are flagged
      in the Methodology Note as "active but not invoked — likely
      inappropriate for this run".

- [ ] **4. Adversarial Query Expansion (M13).** M13 was invoked along
      all four axes (adjacent / opposing / abstraction / orthogonal)
      at least once each. The Query Expansion Log is populated with
      ≥ 4 entries. Confirm: *"M13 was invoked [N] times; the orthogonal
      axis (`{{orthogonal_lens}}`) was used [M] times."* If N=0 or M=0,
      run a final pass before proceeding.

- [ ] **5. Cross-pollination audit.** Both cross-pollinated steps
      (Phase 2b — one from each non-primary category) were executed
      and logged. Confirm: *"Cross-pollination steps adapted from
      Categories X and Y were executed as follows: [enumerate]."* If
      none were executed, the generated prompt did not honor Phase 2b —
      halt and report.

- [ ] **6. Source triangulation (where M06 active).** Every factual
      claim has been through Source Triangulation with ≥ 3 independent
      sources, or is explicitly flagged as **single-source**. Aggregator-
      chains do not count as multiple sources.

- [ ] **7. Contradiction Log populated.** The Contradiction Log section
      of the Synthesis has been written. If no contradictions were
      encountered, the section explicitly states *"No contradictions
      encountered during this research"* — written only after a
      verification pass, never as a default placeholder.

- [ ] **8. Temporal scope honored.** All findings are within the
      temporal scope defined in CONSTRAINT BLOCK 2. Anything outside
      has been removed.

- [ ] **9. Output exclusions honored.** None of the findings or
      recommendations fall into the exclusion list in CONSTRAINT
      BLOCK 3. Verify by reading each finding against the exclusion
      list.

- [ ] **10. Pre-Synthesis Integrity Check (M4) executed in writing.**
      All 8 items of the M4 check were completed before the Synthesis
      was drafted. The check is in the working notes; it is not
      retrofitted after the fact.

- [ ] **11. Synthesis sections complete.** The Synthesis contains:
      Executive Summary · Key Findings · category-specific main body ·
      Contradictions · Query Expansion Log · Reflection History ·
      Cross-Pollination Log · Open Questions · Sources · Methodology
      Note. Any missing section is a blocker; write it before delivery.

If any checkbox fails, repair before delivery. Do not deliver a
Synthesis with failing items. The user will read this checklist
state in the Methodology Note — partial completion is visible.
```

---

## Notes on the Slot Treatment (v3.0)

This checklist has no `phase2_fill` slots — items are uniform across
all generated prompts. Two items reference `{{orthogonal_lens}}`
(item 4), which is filled by M13's slot at composition time; if M13
is in the plan (always — mandatory), this slot is always populated.

## Why 11 Items (vs. v2.1's count)

v2.1 had a similar but less comprehensive checklist. v3.0 expanded it
to cover the new mandates:

- Item 2 (reflection regime, M0) — new in v3.0
- Item 3 (method invocation audit) — new in v3.0; verifies the
  anchored-ReAct innovation
- Item 4 (M13 four-axis verification) — new in v3.0
- Item 5 (cross-pollination audit) — new in v3.0

Items 1, 6, 7, 8, 9, 10, 11 are inherited from v2.1's check with
minor updates.

The number 11 is a side effect, not a target — adding more items
without the failure-mode rationale would dilute the checklist.

## Phase 2 + 3 Behaviour

This module is selected unconditionally (every prompt has it). Phase 2
adds it to the plan; Phase 3 inserts it verbatim near the end of the
rendered prompt, just before the closing marker.
