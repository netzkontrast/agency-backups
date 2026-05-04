# Partial — ReAct Loop Anchored (KEY INNOVATION v3.0)

> This partial is the **single biggest behavioural change v3.0 makes
> to the generated research prompt** versus v2.1.
>
> In v2.1 the ReAct Reason phase asked three generic questions:
>   1. What do I currently believe, and how strongly?
>   2. Which active critical-thinking method applies?
>   3. Am I at risk of local-minimum lock-in?
>
> The problem: the agent reads "which active method applies?" and has
> to recall the method palette from earlier in the prompt. Over a
> 30-minute run, that recall decays — methods drift out of awareness.
>
> v3.0 solves this by rendering the **active method palette as a
> table inside the Reason-phase template itself**. The agent doesn't
> recall — it picks from a list it sees every iteration.

---

## Slot Definition (consumed by Phase 2)

```yaml
slots:
  active_methods_table:
    type: fill_from
    fill_from: selected_methods         # plan.modules.methods
    renders_as: markdown_table
    columns:
      - anchor              # e.g. "[M06]"
      - method              # e.g. "Source Triangulation"
      - when_to_choose      # e.g. "Before committing any citation"
    rendering_rule: |
      For each method in selected_methods:
        anchor          := "[" + module.short_anchor + "]"
        method          := module.full_name
        when_to_choose  := module.when_to_choose_short
                           (1-line summary derived from module.escape_criterion
                            and module.full description; phase2 must populate)
```

---

## Rendered Output Template (Markdown)

The following block is what gets written into the rendered research
prompt as part of the ReAct framework section. `{{active_methods_table}}`
is the fill_from slot.

```markdown
## ReAct Loop — Anchored for THIS Run

This is the agentic spine of every Step in this research. Each
iteration of your work loop is one cycle: **Reason → Act → Observe**.

### The Reason Phase — Active Method Palette

In every Reason phase you choose **exactly one** of the methods below
as the governing method for the next Act. The palette is fixed for
this run; you do not invent methods, and you do not skip the choice.

{{active_methods_table}}

### The Reason Phase — Verbatim Template

Every Reason phase you write contains exactly these five lines, in
this order, before you move to Act:

> **Active method this Act:** [M__] — one sentence why this method,
>     not another, governs the next Act.
> **Constraint compliance:** CB__ — one example of how the next Act
>     honors this Constraint Block.
> **Local-minimum risk:** [low / medium / high]. If medium or high,
>     invoke [M13] Adversarial Query Expansion BEFORE the Act.
> **Reflection trigger:** [is this an M0 checkpoint?]. If yes, write
>     the reflection entry HERE before the Act, not after.
> **Plan:** [the concrete next Act in one line — search query,
>     retrieval, calculation, etc.]

A Reason phase missing any of these five lines is incomplete. Do not
advance to Act.

### The Act Phase

You execute exactly one action — typically one search query, one
document fetch, one calculation. Not a batch of three. One.

### The Observe Phase

You record:
- What the action returned (1-2 sentences).
- What it means for the active hypothesis / claim / schema row.
- The decision: **continue this branch · backtrack · expand vocabulary
  via M13 · escalate to a constraint check**.

### Loop Structure

```
[Reason 1] → [Act 1] → [Observe 1] →
[Reason 2] → [Act 2] → [Observe 2] →
...
[Reason N] → [Pre-Synthesis Integrity Check] → [Synthesis]
```

### Your Very First Action — Before Reason 1

Before the first Reason phase: restate the research objective verbatim,
restate every active Constraint Block (0 first — Reflection Baseline),
and write the Kickoff Reflection per Constraint Block 0. Only then
begin Reason 1.

This first restatement is **not** a Reason phase. It is the
initialization. Mark it explicitly: "## Initialization (before Reason 1)".
```

---

## Why This Anchoring Matters

**Failure mode in v2.1:** the agent runs for 25 minutes, has done 17
search iterations, and the Reason phases have devolved into one-line
plans without method attribution. The last 6 Acts were all silently
M06 (Source Triangulation) because that's what the agent defaulted to
when no method was named — and the rest of the palette decayed out of
working memory. M01 Falsification was never invoked once after
iteration 4 even though it was supposed to be active.

**v3.0 fix:** the method palette is rendered into the Reason template
itself. The agent doesn't recall — it picks from a table that's
literally the next thing on the page after every Observe.

**Verification hook:** at the Pre-Synthesis Integrity Check (M4 item 2),
the executing AI must confirm "Each method listed in the palette has
at least one concrete invocation visible in the Reason history." If
any method has zero invocations, that itself is data — usually a
sign that the method was inappropriate for this run; flag it in the
Methodology Note.

---

## Phase 2 Rendering Rule (programmatic)

```python
# Pseudocode for Phase 3 rendering — included here for catalog completeness.
# The actual implementation lives in render.py (Phase 3).

def render_active_methods_table(selected_methods, catalog):
    rows = []
    for method_id in selected_methods:
        m = catalog['modules'][method_id]
        rows.append({
            'anchor': f"[{m['short_anchor'].split('-')[0]}]",  # e.g. "[M06]"
            'method': m['full_name'],
            'when_to_choose': summarize_when_to_choose(m)
        })
    return render_markdown_table(rows, columns=['anchor', 'method', 'when_to_choose'])

def summarize_when_to_choose(method_module):
    # Phase 2 generates a 1-line cue for each method based on its
    # description + escape_criterion. Examples per method:
    cues = {
        'M01': "When you have a hypothesis to falsify",
        'M02': "Before dismissing a counter-position",
        'M03': "At project start and at halfway checkpoint",
        'M04': "When a claim is evaluative ('high', 'effective')",
        'M05': "At project start and at synthesis (priors → updated belief)",
        'M06': "Before committing any citation",
        'M07': "When sources disagree",
        'M08': "Before locking a tentative conclusion",
        'M09': "At pre-synthesis (attack each conclusion)",
        'M10': "When the question carries inherited vocabulary",
        'M11': "At every checkpoint (lifecycle research)",
        'M12': "Whenever a frequency / probability claim appears",
        'M13': "Always-on; minimum once per 10-minute window",
    }
    return cues.get(method_id_from(method_module), "(see method block)")
```

The cue table above is the canonical "when to choose" vocabulary. It
is identical across all rendered prompts so agents can cross-reference
between runs. Do not paraphrase it per-run.
