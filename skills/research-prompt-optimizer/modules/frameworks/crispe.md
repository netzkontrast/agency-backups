---
type: framework
role: structural_layer
full_name: CRISPE (Capacity · Request · Insight · Style · Personality · Experiment)
short_anchor: CRISPE
mandatory: false
default_for_categories: []
override_trigger:
  condition: output_format == 'multiple_variants' OR research_question contains 'alternatives'
  priority: 3
slots:
  experiment_axis_count:
    type: phase2_fill
    description: How many output variants (default 3)
    required: false
id: crispe
file: modules/frameworks/crispe.md
---

# Framework — CRISPE (Structural Layer)

```markdown
## Prompt-Engineering Framework (Structural Layer): CRISPE

This prompt uses **CRISPE** as its structural layer, stacked on top of
the ReAct agentic spine. CRISPE is used when the task requires multiple
alternative outputs or comparative variants. It stands for:

- **C — Capacity and role**: Who you are.
- **R — Request**: What to produce.
- **I — Insight**: Key background information.
- **S — Style**: Voice and tone.
- **P — Personality**: Character of the output.
- **E — Experiment**: Produce multiple variants for comparison.

**Your first action:** Confirm the number of variants requested and the
axis along which they should differ.
```
