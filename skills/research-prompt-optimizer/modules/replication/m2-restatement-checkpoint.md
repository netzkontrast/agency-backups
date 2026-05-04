---
type: replication
full_name: Per-Step Restatement Checkpoint
short_anchor: M2-RestatementCheckpoint
mandatory: true
selected_when: always (every multi-step prompt)
slots:
  active_constraint_blocks:
    type: fill_from
    description: List of CB IDs to restate verbatim
    fill_from: constraint_blocks
  active_methods:
    type: fill_from
    description: List of methods to restate verbatim
    fill_from: selected_methods
  cb_restatement_block:
    type: fill_from
    description: |
      Phase 3 emits one Markdown bullet per active constraint block:
      `- **CONSTRAINT BLOCK <id> — <title>:** [Paste the full text of the
      block here. Do not paraphrase.]`
      The "Paste verbatim" instruction is part of the rendered template —
      it instructs the executing agent at runtime, not Phase 3.
      Source: the `active_constraint_blocks` slot.
    required: true
    fill_from: active_constraint_blocks
  method_restatement_block:
    type: fill_from
    description: |
      Phase 3 emits one Markdown bullet per active method:
      `- **Method: <full_name>** — [Paste the "How to apply" bullet list
      verbatim.]`
      M13 is always first (mandatory in every prompt).
      Source: the `active_methods` slot.
    required: true
    fill_from: active_methods
  step_or_iteration_label:
    type: agent_runtime_fill
    description: |
      Filled by the executing agent at runtime. Format: "STEP N" or
      "ITERATION N" depending on whether the current pass is a sequential
      step or a batch iteration.
    required: true
  step_title:
    type: agent_runtime_fill
    description: Short title for the step the agent is about to execute.
    required: true
  step_content:
    type: agent_runtime_fill
    description: |
      The actual content of the step — what the agent does in this pass.
      The agent fills this with the relevant action / search / synthesis
      content for the current step.
    required: true
id: m2-restatement-checkpoint
file: modules/replication/m2-restatement-checkpoint.md
---

# Replication M2 — Per-Step Restatement Checkpoint · Paste-Ready Template

> Every step, iteration, or loop pass starts with a verbatim restatement
> block in this fixed template. This is non-optional.

```markdown
### Restatement Checkpoint — Before {{step_or_iteration_label}}

Before executing this step, I restate the currently-active constraints
verbatim:

{{cb_restatement_block}}

I also restate the currently-active critical-thinking methods:

{{method_restatement_block}}

I confirm these are active for the step below.

### {{step_or_iteration_label}} — {{step_title}}

{{step_content}}
```

**Critical rule:** the word "verbatim" in the template is load-bearing.
The target AI must be explicitly told that **paraphrase is not
acceptable** — the original language of the block must appear in the
restatement. This prevents silent semantic drift through summarization.

**Always include M13 (Adversarial Query Expansion) in the method list**
regardless of which 3–5 category-specific methods are active. M13 is
mandatory in every prompt per v2.1.

**CONSTRAINT BLOCK 0 (Reflection Baseline) is always the first block
restated**, since its checkpoints apply continuously and it is easiest
to forget when the step feels routine.
