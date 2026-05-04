---
type: replication
full_name: Batch-Explicit Framing
short_anchor: M3-Batch
mandatory: false
selected_when: len(plan.batches.domain) >= 1 OR category in [B, C]
slots:
  batch_name:
    type: phase2_fill
    description: Human-readable name for this batch
    required: true
  cardinality:
    type: phase2_fill
    description: int OR 'indefinite' (Cat-C)
    required: true
  items:
    type: phase2_fill
    description: Concrete items list, OR null if cardinality='indefinite'
    required: false
  iteration_steps:
    type: phase2_fill
    description: Steps to execute per iteration
    required: true
  output_schema_per_iteration:
    type: phase2_fill
    description: Schema each iteration must populate
    required: true
  confidence_label:
    type: agent_runtime_fill
    description: |
      Per-iteration confidence assessment. Enum: LOW | MEDIUM | HIGH.
      The agent fills this at the end of each batch iteration as part of
      the per-iteration output schema.
    required: true
    enum: [LOW, MEDIUM, HIGH]
  items_render_block:
    type: fill_from
    description: |
      Phase 3 emits one numbered Markdown line per item from the `items`
      slot. Source: the `items` slot.
    required: true
    fill_from: items
  iteration_steps_render_block:
    type: fill_from
    description: |
      Phase 3 emits the per-iteration steps as a numbered list. Source:
      the `iteration_steps` slot.
    required: true
    fill_from: iteration_steps
  output_schema_render_block:
    type: fill_from
    description: |
      Phase 3 emits one bullet per output-schema field with `[...]`
      placeholders for the agent to fill at runtime. Source: the
      `output_schema_per_iteration` slot.
    required: true
    fill_from: output_schema_per_iteration
id: m3-batch
file: modules/replication/m3-batch.md
---

# Replication M3 — Batch-Explicit Framing · Paste-Ready Template

> Where a sequence of steps is repeated (for each competitor / each paper /
> each regulation / each market), the generated prompt must (a) frame the
> repetition explicitly as a batch with cardinality, (b) embed the
> constraint + method blocks *inside* the loop body, not only before it,
> and (c) provide a per-iteration output schema the target AI fills before
> advancing.

```markdown
## BATCH PROCEDURE — {{batch_name}}

You will execute the following procedure **exactly {{cardinality}} times**,
once per item in this list:

{{items_render_block}}

For each iteration, you execute the steps below **in full**, including
the Restatement Checkpoint and the Reflection entry. Do not batch-skip
either. Do not summarize across items until all iterations are complete.

---

### Iteration Template — Apply to Each Item in Turn

**Restatement Checkpoint — Before Iteration [i] for Item [ITEM i]**

[Paste the full Restatement Checkpoint template from
`m2-restatement-checkpoint.md`.]

**Reflection Entry — Iteration [i]**

[Paste the five-question reflection template from CONSTRAINT BLOCK 0.
Minimum: Q1, Q3, Q5 per iteration. Q2 and Q4 at least every third
iteration.]

**Iteration [i] Steps:**

{{iteration_steps_render_block}}

**Iteration [i] Output Schema (fill all fields):**

{{output_schema_render_block}}
- Confidence: {{confidence_label}}

You may not proceed to Iteration [i+1] until Iteration [i]'s output
schema is fully populated.
```

**Three independent drift-guards in this mechanism:**

1. Explicit cardinality ("exactly N times") — the target AI cannot
   silently shorten the loop.
2. Per-iteration restatement + reflection — the constraints and the
   agent's own belief-state are refreshed every pass.
3. Fully-populated per-iteration schema — premature progression triggers
   a visible gap.
