---
type: replication
full_name: Pre-Synthesis Integrity Check (8-item)
short_anchor: M4-PreSynthesisCheck
mandatory: true
self_applicable: true
self_applied_phase2:
  sub_phase: '4.8'
  hook_role: Before plan-view rendering, run 6-item Phase-2 variant of the integrity
    check (NOT the 8-item agent-runtime version). Failed items block rendering and
    force self-correct loop. Active for ALL depths including surface.
  depth_active:
  - surface
  - standard
  - exhaustive
  variant: 6-item Phase-2 (not 8-item agent-runtime)
selected_when: always
slots: {}
id: m4-pre-synthesis
file: modules/replication/m4-pre-synthesis.md
---

# Replication M4 — Pre-Synthesis Integrity Check · Paste-Ready Template

> Last integrity checkpoint before the target AI writes the final
> synthesis. Pasted verbatim just before the Synthesis section of the
> generated prompt.

```markdown
## PRE-SYNTHESIS INTEGRITY CHECK

Before writing the final synthesis, execute this verification pass in
writing. Each item produces a written line; "done" by memory does not
count.

1. **Re-read Constraint Blocks 0–[N] verbatim.** Confirm in writing:
   *"I have re-read each constraint block and they are all still
   active."*

2. **Re-read the critical-thinking method blocks.** Confirm in writing:
   *"Each method listed below is active and I have applied it:
   [enumerate methods, including M13 Adversarial Query Expansion]."*

3. **Reflection audit (CONSTRAINT BLOCK 0).** Count the reflection
   entries written during this run. Confirm: *"I wrote [K] reflection
   entries at the following checkpoints: [enumerate]."* If K is below
   the minimum required by CONSTRAINT BLOCK 0, write the missing
   reflections **now** before continuing.

4. **Query-expansion audit (M13).** Confirm in writing: *"Method M13
   Adversarial Query Expansion was invoked [N] times across the four
   axes (adjacent / opposing / abstraction / orthogonal). The Query
   Expansion Log contains [M] entries, of which [P] produced novel
   findings that modified tentative conclusions."* If N = 0, the
   research is incomplete — run at least one pass before proceeding.

5. **Cross-pollination audit.** Confirm in writing: *"Steps adapted
   from the two non-primary categories were executed as follows:
   [enumerate the cross-pollinated steps]."* If none were executed,
   the generated prompt did not honor Phase 2b — halt and report.

6. **Constraint-compliance audit.** For each constraint block (0
   through N), check the accumulated findings and cite one specific
   example of how you honored it. If you cannot cite a specific
   example, flag the constraint as **not-demonstrably-honored**.

7. **Scope audit.** Confirm: *"All findings are within the temporal
   scope defined in Constraint Block 2."* If any are outside, flag
   and remove.

8. **Exclusion audit.** Confirm: *"None of the findings or
   recommendations fall into the exclusion list in Constraint Block
   3."*

Only after all eight items are complete in writing may you begin the
Synthesis section.
```

**Rationale for the expanded 8-item list (v2.1):**

The v2.0 integrity check had five items. Three new items were added:
the reflection audit (item 3) and the query-expansion audit (item 4)
enforce the new v2.1 mandates (reflection baseline + adversarial query
expansion), and the cross-pollination audit (item 5) enforces Phase 2b.
Without these audits the new mandates decay silently during long runs.
