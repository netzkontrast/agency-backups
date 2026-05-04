---
type: framework
role: structural_layer
full_name: Bespoke Synthesis (composed from catalog components)
short_anchor: BESPOKE
mandatory: false
selected_when: 'Q3-lenient: ≥2 override_triggers fire simultaneously'
requires_provenance: true
slots:
  bespoke_acronym:
    type: phase2_fill
    description: New acronym name for the bespoke framework
    required: true
    fill_strategy: claude_generates_from_components
  components:
    type: phase2_fill
    description: |
      Structured list. Each entry is {letter, name, definition,
      source_framework}. Phase 3 uses this list to render
      `components_render_block` (the bullet block) and
      `provenance_render_block` (the provenance lines).
    required: true
    fill_strategy: claude_generates
  components_render_block:
    type: fill_from
    description: |
      Phase 3 emits one Markdown bullet per component:
      `- **<letter> — <name>**: <definition>`.
      Source: the `components` slot.
    required: true
    fill_from: components
  provenance_render_block:
    type: fill_from
    description: |
      Phase 3 emits one provenance line per component:
      `- Component <letter> is adapted from the <source_framework> framework.`.
      Source: the `components` slot (uses `source_framework` field).
    required: true
    fill_from: components
  first_action_directive:
    type: phase2_fill
    description: |
      Concrete restatement directive analogous to RISEN's "restate Role
      and Narrowing" — picks the two binding components and requires the
      executing agent to restate them before starting.
    required: true
    fill_strategy: claude_generates_from_components
id: bespoke
file: modules/frameworks/synthesis.md
---

# Framework — Bespoke Synthesis (Structural Layer)

> **v2.1 addition.** When no single framework from the `prompt-optimizer`
> 27-framework catalog fits the research task cleanly, **Claude is
> explicitly encouraged to synthesize a bespoke framework** by cherry-
> picking components from multiple catalog frameworks and composing
> them under one named banner.
>
> This file defines the protocol. The output of the protocol is a paste-
> ready framework block, same format as `risen.md` / `care.md` / etc.,
> used as the **second framework** alongside the mandatory ReAct spine.

---

## When to Synthesize Instead of Picking

Trigger bespoke synthesis when **any** of the following holds:

1. The research task combines two modes that no single catalog framework
   cleanly expresses — e.g., "agentic extraction with hard Do/Don't rules
   AND strong audience/tone constraints" (ReAct + TIDD-EC + CO-STAR
   facets).
2. The research crosses categories (per Phase 2b Cross-Pollination) in a
   way that needs structural handles from more than one framework.
3. The user explicitly asks for a non-standard structure, or the topic
   has structural demands that fall in a gap between catalog frameworks.
4. You catch yourself force-fitting a catalog framework and discarding
   parts of the task to make it fit. That is the signal to synthesize.

Do **not** synthesize for novelty's sake. If RISEN fits, ship RISEN.

---

## The Synthesis Protocol — Five Steps

1. **Enumerate the task's structural demands.** Write 3–6 short bullets
   of what the prompt structure must give the executing agent. Examples:
   *"clear role scoping"*, *"explicit forbidden-actions list"*, *"per-
   item batch scaffold"*, *"audience-tone calibration"*, *"iterative
   agent loop"*, *"multi-variant output"*.

2. **Map each demand to its best-fit catalog component.** From the
   27-framework catalog referenced in the `prompt-optimizer` skill,
   identify which framework contributes each demand most cleanly. A
   demand maps to at most one framework. Accept that this will produce
   a mix (e.g., demand 1 → RISEN.R, demand 2 → TIDD-EC.D/D, demand 3 →
   CO-STAR.A+T, demand 4 → CARE.E).

3. **Name the bespoke framework.** Give it a short, honest acronym that
   reflects the cherry-picked components in their execution order. The
   name must be new — do not reuse a catalog acronym. Example for the
   above mix: **RAD-EC** (Role · Audience-Tone · Do/Don't · Examples ·
   Context) or **STEP-AUDIT** (whatever is memorable and accurate).

4. **Write the inline-expansion block** in the same format as the
   catalog frameworks in this folder: one-line preamble + component
   list (letter → name → one-sentence definition) + "Your first action"
   directive. The block is self-contained and assumes the executing AI
   has never heard the acronym. This is mandatory — no bare acronyms.

5. **Document the synthesis provenance inline.** Under the expansion
   block, include one line per component: *"Component X is adapted from
   the [CATALOG FRAMEWORK NAME] framework."* This keeps the bespoke
   framework auditable and non-magical.

---

## Template — Paste-Ready Skeleton for the Generated Prompt

```markdown
## Prompt-Engineering Framework (Structural Layer): {{bespoke_acronym}}

This prompt uses **{{bespoke_acronym}}** — a bespoke structural framework
synthesized specifically for this research task — as its structural
layer, stacked on top of the ReAct agentic spine. {{bespoke_acronym}}
stands for:

{{components_render_block}}

**Your first action:** {{first_action_directive}}

**Provenance (for auditability):**
{{provenance_render_block}}

Each section of this prompt is labeled with its {{bespoke_acronym}}
component in parentheses. Honor each component as a hard contract.
```

---

## Anti-Patterns — Bespoke Synthesis Specific

| Anti-Pattern | Why It Fails |
|--------------|--------------|
| Synthesizing to avoid thinking hard about which catalog framework fits | Usually a catalog framework does fit — synthesis is overhead when one would do |
| Acronym > 6 letters | Becomes unmemorable and unusable by the target AI |
| Reusing a catalog acronym (e.g., calling your mix "RISEN+") | Causes name collision and confusion in the target AI |
| Omitting provenance | Makes the bespoke framework look magical; blocks auditability |
| Component names that overlap semantically (e.g., "Role" and "Persona") | Creates redundancy the target AI cannot honor consistently |

---

## Relationship to the Mandatory ReAct Spine

The bespoke framework is **always** the **structural layer**, never the
agentic spine. ReAct remains the mandatory agentic spine of every
generated research prompt. The bespoke framework defines the
macro-structure of the document (sections, ordering, first-action
directive). ReAct defines the micro-structure of execution inside each
Step (reason → act → observe).
