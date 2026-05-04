# Partial — Meta-Header (Three-Layer Block)

> Every rendered research prompt opens with a Meta-Header that
> introduces the **three independent layers** of the prompt:
> Epistemological Layer (Category) + Agentic Spine (ReAct) +
> Structural Layer (RISEN / TIDD-EC / ... / bespoke).
>
> Each of the three is **inline-expanded verbatim** in this header —
> the executing AI must understand all three before reading the
> Research Objective.

---

## Slot Definitions

```yaml
slots:
  category_block:
    type: fill_from
    fill_from: "modules/categories/<category>.md"   # rendered inline
  react_block:
    type: fill_from
    fill_from: "modules/frameworks/react.md"        # rendered inline, with active_methods_table filled
  structural_block:
    type: fill_from
    fill_from: "modules/frameworks/<structural>.md"  # rendered inline; for bespoke, see synthesis.md
  language_warning_block:
    type: fill_from
    fill_from: "modules/partials/language-warning.md"
    required_when: "intent.language != 'en'"
```

---

## Rendered Output Template

```markdown
# Research Prompt: {{topic}}

> **For the executing AI:** This prompt is self-contained. Every
> method, framework, and constraint you need is defined inline below.
> You do not need external context, prior training on specific
> methodologies, or knowledge of the skill that generated this
> prompt. **Read the entire prompt before beginning.** Specifically,
> read the three layers in the Meta-Header below and verify you
> understand how they compose.

{{language_warning_block_or_empty}}

---

## Meta-Header — What This Prompt Is and How To Read It

This research prompt combines **three independent layers**. Each
governs a different aspect of your work:

### Layer 1 — Epistemological Layer ({{research_category_label}})

This layer defines **how to think** about the research — what kind of
question it is, what counts as success, what failure modes are likely.

{{category_block}}

### Layer 2 — Agentic Spine (ReAct)

This layer defines **how to iterate** — the micro-execution loop that
each Step in this prompt expands into.

{{react_block}}

### Layer 3 — Structural Layer ({{framework_structural_label}})

This layer defines **how the document is organized** — what sections
exist, what order they go in, and what each section is for.

{{structural_block}}

### How the Layers Compose

- **Layer 1** governs the *strategy* (exploration vs. extraction vs.
  lifecycle).
- **Layer 2** governs the *micro-execution* inside each Step (Reason
  → Act → Observe).
- **Layer 3** governs the *macro-organisation* of this document
  (sections, ordering, first-action directive).

You honor all three simultaneously. They are orthogonal, not nested.

---
```
