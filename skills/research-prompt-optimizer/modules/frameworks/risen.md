---
type: framework
role: structural_layer
full_name: RISEN (Role · Input · Steps · Expectations · Narrowing)
short_anchor: RISEN
mandatory: false
default_for_categories:
- A
- B
- C
selected_when: no override_trigger fires (default)
override_priority: 0
slots:
  role:
    type: phase2_fill
    description: Role description for the executing agent — derived from intent.audience
    fill_from_intent: intent.audience
    fill_strategy: mirror
id: risen
file: modules/frameworks/risen.md
---

# Framework — RISEN (Structural Layer)

```markdown
## Prompt-Engineering Framework (Structural Layer): RISEN

This prompt follows the **RISEN framework** as its structural layer,
stacked on top of the ReAct agentic spine. RISEN governs how the
sections of this prompt are organized; ReAct governs how you iterate
within each step. RISEN stands for:

- **R — Role**: Who you are acting as during this task.
- **I — Input**: What materials, questions, or data you are starting with.
- **S — Steps**: The explicit ordered procedure to follow.
- **E — Expectations**: What a successful output looks like (format,
  coverage, depth).
- **N — Narrowing**: Hard constraints, exclusions, and scope limits.

**Your first action before Step 1:** Restate the Role and Narrowing
sections in your own words. Confirm you have internalized them. Do not
begin Step 1 until this restatement is written.

Each section of this prompt is labeled with its RISEN component in
parentheses, e.g., "(R — Role)". Honor each component as a hard contract.
```
