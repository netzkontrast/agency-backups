---
id: m0-reflection
type: replication
file: "modules/replication/m0-reflection.md"
full_name: "Reflection Baseline (CONSTRAINT BLOCK 0)"
short_anchor: "M0-ReflectionBaseline"
mandatory: true
constraint_block_id: 0
selected_when: "always"
self_applied_phase2:
  sub_phase: "4.3"
  hook_role: "After module selection commits, run 2-Q mini-reflection variant (NOT the full 5-Q baseline): 'Which method choice in this set is most fragile?' + 'Which non-default activation has the trigger really present?'"
  depth_active: ["standard", "exhaustive"]
  variant: "2-Q mini (not full 5-Q)"
slots: {}
---

# M0 — Reflection Baseline (MANDATORY · CONSTRAINT BLOCK 0)

> **v3.0 sample module.** Demonstrates a mandatory module with
> **zero slots** — the template is fully self-contained and identical
> across all rendered prompts. Phase 2 selects it unconditionally;
> Phase 3 inserts the block verbatim as Constraint Block 0.

## Rendered Block (composed into the research prompt as CB 0)

```markdown
## CONSTRAINT BLOCK 0 — Reflection Baseline (Always Active)

Reflection is not a polish step. It is a **baseline operational
requirement** that runs in parallel to every other activity in this
research. You — the executing agent — perform targeted reflection at
every defined checkpoint, in writing, using the template below. A
checkpoint reached without a reflection entry is an incomplete
checkpoint; do not advance past it.

### Reflection Checkpoints (Minimum)

1. **Kickoff reflection** — immediately after restating the research
   objective and Constraint Blocks, before the first Reason phase.
2. **Mid-run reflection** — after the first batch of searches, once
   you have a tentative direction but before you commit to it.
3. **Post-Query-Expansion reflection** — after each Adversarial Query
   Expansion pass (Method M13).
4. **Pre-synthesis reflection** — immediately before the Pre-Synthesis
   Integrity Check (M4).
5. **Post-synthesis reflection** — after the draft synthesis, before
   delivery.

Additional checkpoints apply if the research category has its own
(e.g., per-session reflections in lifecycle research).

### Reflection Template — Use Verbatim Structure

Each reflection entry answers these five questions, in order, in
writing:

> **Q1. What do I actually believe right now, and how confident?**
> (One sentence. Use an explicit confidence band: low / medium / high.)
>
> **Q2. What is the strongest piece of evidence against my current
> belief?** (Name the specific source or the specific observation. If
> you cannot name one, that itself is the answer — and it is a warning.)
>
> **Q3. Where am I most likely wrong, and why?** (Not generic — name
> the specific claim, assumption, or inference that is weakest.)
>
> **Q4. What would I do differently if I restarted the research from
> scratch knowing what I know now?** (Forces de-anchoring from the
> path already taken.)
>
> **Q5. What is the single highest-value next action?** (Must be a
> concrete, executable next step — a specific search, a specific
> verification, a specific hypothesis branch to open or close.)

### Rules

- Reflections are **written**, not internal. They become part of the
  research notes and of the final output's Reflection History
  section in the Synthesis.
- Reflections may not be skipped "because the answer is obvious". If
  the answer feels obvious, write the obvious answer in one line and
  advance — but do not omit the entry.
- **Reflections on reflections are allowed but not required.** If a
  reflection surfaces a contradiction with an earlier reflection, log
  both in the Contradiction Log (Method M07) with a note that the
  disagreement is internal rather than inter-source.
- If a reflection produces an action item (Q5) that contradicts the
  current Step's plan, the action item **takes precedence**. Update
  the plan, note the change, and continue.

### Anti-Rationalization Guard

If you find yourself writing "N/A" or "nothing to reflect on" in a
reflection entry — stop and re-read the entry's five questions. At
least Q2 and Q3 always have a real answer. "N/A" is a signal that the
reflection is being skipped performatively; write the real answer
instead.
```

---

## Notes on the Slot Treatment (v3.0)

This module has `slots: {}` in its frontmatter — no substitution at
composition time. The rendered block above is identical across every
generated research prompt regardless of category, framework, methods,
or topic.

This is the simplest possible v3.0 module pattern: mandatory, no
slots, no per-run customization. Phase 2 selects it unconditionally;
Phase 3 inserts it verbatim.

## Phase 2 Behaviour

M0-Reflection is added unconditionally. Phase 2:

- Adds `m0-reflection` to `replication`
- Adds `id: 0` to `constraint_blocks` with
  `source: "module"` and `module_ref: "m0-reflection"`
  (signals to Phase 3: do not author content; use the module's
  rendered block)
- Does not populate any slot fills (no slots to fill)

## Phase 3 Behaviour

Phase 3 inserts this block as the very first Constraint Block in the
rendered prompt — before any user-derived constraint blocks. M0 is the
foundation everything else restates against in M2 Restatement
Checkpoints.

## Why M0 Has No Slots (Design Decision)

The five-question reflection template is deliberately uniform. If we
allowed per-run customization (e.g., domain-specific reflection
questions), three things would happen, all bad:

1. Cross-run comparability would decay — analysts reviewing two
   research outputs from the same skill would see different reflection
   structures.
2. Restatement integrity (M2) would be harder — the agent would need
   to reproduce a different template each time.
3. Drift opportunities multiply — every customized reflection question
   is a place the user might over-specify or under-specify.

Uniformity is the feature. M0 is the spine of the reflection regime
across all generated prompts; uniformity is what makes it auditable.
