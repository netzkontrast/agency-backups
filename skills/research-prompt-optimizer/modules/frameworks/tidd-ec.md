---
type: framework
role: structural_layer
full_name: TIDD-EC (Task · Instructions · Do · Don't · Examples · Context)
short_anchor: TIDD-EC
mandatory: false
default_for_categories: []
override_trigger:
  condition: intent.known_constraints contains 'forbidden actions' OR research is
    compliance-focused
  priority: 2
slots: {}
id: tidd-ec
file: modules/frameworks/tidd-ec.md
---

# Framework — TIDD-EC (Structural Layer)

```markdown
## Prompt-Engineering Framework (Structural Layer): TIDD-EC

This prompt uses **TIDD-EC** as its structural layer, stacked on top of
the ReAct agentic spine. TIDD-EC is used when explicit separation
between permitted and forbidden actions is critical. It stands for:

- **T — Task**: What you must accomplish.
- **I — Instructions**: How to accomplish it.
- **D — Do**: An explicit list of required actions.
- **D — Don't**: An explicit list of forbidden actions.
- **E — Examples**: Concrete worked examples of correct execution.
- **C — Context**: Background that frames the task.

**Your first action:** Read the **Do** and **Don't** lists twice.
Confirm in writing that you understand them before starting the Task.
```
