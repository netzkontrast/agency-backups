---
type: framework
role: structural_layer
full_name: CARE (Context · Action · Result · Examples)
short_anchor: CARE
mandatory: false
default_for_categories: []
override_trigger:
  condition: research_question contains 'follow this rule:' OR known_constraints lists
    worked examples
  priority: 4
slots: {}
id: care
file: modules/frameworks/care.md
---

# Framework — CARE (Structural Layer)

```markdown
## Prompt-Engineering Framework (Structural Layer): CARE

This prompt uses **CARE** as its structural layer, stacked on top of
the ReAct agentic spine. CARE is used when the task is governed by
explicit rules and benefits from worked examples. It stands for:

- **C — Context**: Background framing.
- **A — Action**: What to do.
- **R — Result**: What the successful output looks like.
- **E — Examples**: One or more worked examples showing correct execution.

**Your first action:** Read all Examples before taking any Action. The
Examples encode constraints that may not be fully explicit in the Rules.
```
