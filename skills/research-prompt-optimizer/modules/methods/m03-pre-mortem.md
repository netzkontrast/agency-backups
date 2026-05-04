---
type: method
full_name: Pre-Mortem Analysis
short_anchor: M03-PreMortem
mandatory: false
self_applicable: true
self_applied_phase2:
  sub_phase: '4.8'
  hook_role: Generate top-3 failure modes for the plan before plan-view rendering.
    Top-5 if depth=exhaustive. Output rendered into plan view.
  depth_active:
  - standard
  - exhaustive
  output_size: 3 items (standard) | 5 items (exhaustive)
applies_to_categories:
- A
- B
- C
default_for:
- C
triggered_by_signals:
- risk
- what could go wrong
- plan for failure
- fail
pairs_well_with:
- M07
- M09
escape_criterion: Run once at start + once at halfway. More than two runs → anxious
  over-planning
slots:
  topic:
    type: phase2_fill
    description: The research topic — used in the pre-mortem framing 'If my final
      report on TOPIC turns out wrong...'
    required: true
    fill_from_intent: intent.research_question
    fill_from_intent_max_chars: 100
  source_type:
    type: agent_runtime_fill
    description: A source-type the agent identifies as a likely failure cause
    required: false
  temporal_window:
    type: agent_runtime_fill
    description: A temporal-window risk the agent identifies
    required: false
id: M03
file: modules/methods/m03-pre-mortem.md
---

# M03 — Pre-Mortem Analysis

```markdown
### Method: Pre-Mortem Analysis

**What it is:** You imagine that the research has already concluded and
produced a wrong, misleading, or unusable answer. You then work backward
to enumerate all plausible causes of that failure — before the research
actually begins or at defined checkpoints during execution.

**Why it is in this prompt:** Forward planning focuses on success paths
and systematically under-weights failure modes. Pre-mortem flips this by
starting from "it failed" and forcing the enumeration of causes.

**How to apply it — step by step:**
1. At the start of the research, write: "Assume this research produced a
   wrong or misleading answer. List the top 5 most likely causes."
2. For each cause, define a **detection signal**: what would tell you, mid-
   research, that this failure mode is activating?
3. Design at least one mitigation step per cause and embed it in your
   research plan.
4. At every major checkpoint, re-check the detection signals. If any
   fires, pause and apply the mitigation.

**When to stop / escape criterion:** Run the pre-mortem **once before
starting** and **once at the halfway checkpoint**. More than two runs
tends to produce anxious over-planning without new information.

**Example trigger in this research context:** "If my final report on
{{topic}} turns out to be wrong, the most likely causes are: (1) I over-
relied on {{source_type}}; (2) I missed {{temporal_window}}; (3) ..."
```
