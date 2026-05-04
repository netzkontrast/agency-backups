---
type: framework
role: structural_layer
full_name: CO-STAR (Context · Objective · Style · Tone · Audience · Response)
short_anchor: CO-STAR
mandatory: false
default_for_categories: []
override_trigger:
  condition: audience tone is decisive AND output is for external/non-expert reader
  priority: 1
slots: {}
id: co-star
file: modules/frameworks/co-star.md
---

# Framework — CO-STAR (Structural Layer)

```markdown
## Prompt-Engineering Framework (Structural Layer): CO-STAR

This prompt uses **CO-STAR** as its structural layer, stacked on top of
the ReAct agentic spine. CO-STAR is used when the output's audience,
tone, or style is decisive. It stands for:

- **C — Context**: The situation in which the output will be read.
- **O — Objective**: The functional goal of the output.
- **S — Style**: The writing style required.
- **T — Tone**: The emotional register required.
- **A — Audience**: Who will read this output.
- **R — Response format**: The physical shape of the output.

**Your first action:** Identify the intersection of Audience and Tone
before beginning. Write one sentence characterizing how this specific
audience reads this specific tone.
```
