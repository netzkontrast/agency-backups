---
id: react
type: framework
role: agentic_spine
file: "modules/frameworks/react.md"
full_name: "ReAct (Reason + Act + Observe)"
short_anchor: "ReAct"
mandatory: true
selected_when: "always"
slots:
  active_methods_table:
    type: fill_from
    description: "Programmatic table of active methods with anchors and escape criteria"
    fill_from: "selected_methods"
    renders_as: "markdown_table"
    columns: [anchor, method, when_to_choose]
---

# Framework — ReAct (MANDATORY agentic spine, every prompt)

> **v3.0 sample module.** Demonstrates the `fill_from` slot type: the
> `active_methods_table` is generated programmatically from the
> `selected_methods` list at composition time — it is not from intent
> and not from agent runtime, but from another part of the meta-prompt
> plan itself.
>
> This module also pulls in the `react-loop-anchored.md` partial,
> which contains the KEY INNOVATION of v3.0 (anchored Reason phase).

## Rendered Block (composed into the research prompt)

```markdown
## Prompt-Engineering Framework — Agentic Spine: ReAct

This prompt uses the **ReAct framework** as its agentic spine. Every
autonomous research loop in this prompt follows the ReAct cycle. Each
iteration of your work loop consists of three phases:

- **Reason** — You articulate your current understanding and plan the
  next action in plain language. You select exactly one of the active
  critical-thinking methods (see palette below) as the governing
  method for the next Act.
- **Act** — You execute exactly one action — typically one search,
  one retrieval, one calculation. Not three. One.
- **Observe** — You record what the action returned and what it means.
  You decide: continue this branch, backtrack, or expand vocabulary
  via M13 Adversarial Query Expansion.

{{active_methods_table}}

### The Reason Phase — Verbatim Template (used in every Reason)

In every Reason phase you write, fill these five lines verbatim,
in this order, before you move to Act:

> **Active method this Act:** [M__] — one sentence why this method,
>     not another, governs the next Act.
> **Constraint compliance:** CB__ — one example of how the next Act
>     honors this Constraint Block.
> **Local-minimum risk:** [low / medium / high]. If medium or high,
>     invoke [M13] Adversarial Query Expansion BEFORE the Act.
> **Reflection trigger:** [is this an M0 checkpoint?]. If yes, write
>     the reflection entry HERE before the Act, not after.
> **Plan:** [the concrete next Act in one line].

A Reason phase missing any of the five lines is incomplete; do not
advance to Act.

### Loop Structure

```
[Reason 1] → [Act 1] → [Observe 1] →
[Reason 2] → [Act 2] → [Observe 2] →
...
[Reason N] → [Pre-Synthesis Integrity Check] → [Synthesis]
```

### Your Very First Action — Before Reason 1

Before the first Reason phase: restate the research objective verbatim,
restate every active Constraint Block (Block 0 — Reflection Baseline —
first), and write the Kickoff Reflection per Constraint Block 0. Only
then begin Reason 1.

This first restatement is **not** a Reason phase. It is the
initialization. Mark it: "## Initialization (before Reason 1)".

### Why the Active-Method Anchoring Exists

The active-method palette above is rendered into this prompt
verbatim — it is not something you must recall from earlier sections.
This is intentional. Over a 30-minute autonomous run, methods named
only once near the top of the prompt drift out of working attention.
By the 17th Reason phase, the method palette has decayed.

The anchored palette breaks that decay. You don't recall the methods —
you pick from a table that's literally inside the Reason-phase
template. Every Reason phase invokes a named method. A Reason phase
without a named method is incomplete and must be repaired before
Act.

The Pre-Synthesis Integrity Check (M4 item 2) verifies that **every
method listed in this palette has at least one concrete invocation
visible in your Reason history**. A method with zero invocations is
data — usually a sign that the method was inappropriate for this
specific run; flag it in your Methodology Note.
```

---

## Notes on the Slot Treatment (v3.0)

The single slot `active_methods_table` is `fill_from: selected_methods`.
This means Phase 2 (or Phase 3 at render time) reads
`meta-prompt.yaml.modules.methods` and renders a Markdown table:

```markdown
| Anchor  | Method                          | When to choose                         |
|---------|---------------------------------|----------------------------------------|
| [M01]   | Falsification                   | When you have a hypothesis to falsify  |
| [M02]   | Steelmanning                    | Before dismissing a counter-position   |
| [M06]   | Source Triangulation            | Before committing any citation         |
| [M07]   | Contradiction Log               | When sources disagree                  |
| [M13]   | Adversarial Query Expansion     | Always-on; min once per 10-minute window |
```

The `when_to_choose` column is filled from each method's
`when_to_choose_short` field in the catalog. The cue table is
canonical — Phase 2 does not paraphrase per-run. This keeps the
language stable across runs so an agent reading two different runs
sees the same anchors.

## Phase 2 Behaviour

ReAct is mandatory and selected unconditionally. Phase 2:

- Adds `react` as `framework_agentic_spine` (always)
- Computes the `active_methods_table` slot value from `selected_methods`
- Stores it in `slot_fills.react.active_methods_table` as a rendered
  Markdown table string

The fill happens after method selection (Phase 2.3), since
`selected_methods` must be finalized before the table can be
generated. If methods are edited in the Approval Loop (Phase 2.9),
the table is re-rendered.

## Phase 3 Behaviour

Phase 3 substitutes `{{active_methods_table}}` with the rendered table
from `slot_fills`. No re-derivation at render time — the value is
locked in `meta-prompt.yaml`.
