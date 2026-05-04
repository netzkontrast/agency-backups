---
type: replication
full_name: Constraint Block Anchors
short_anchor: M1-ConstraintBlocks
mandatory: true
selected_when: always
slots:
  source_priority_rules:
    type: phase2_fill
    description: Block 1 content
    fill_from_intent: priors_and_constraints.known_constraints
    fill_strategy: merge_with_default
  temporal_scope_text:
    type: phase2_fill
    description: Block 2 content
    fill_from_intent: intent.temporal_scope
    fill_strategy: render_as_sentence
  output_exclusions:
    type: phase2_fill
    description: Block 3 content
    fill_from_intent: intent.research_question_unpacked
    fill_strategy: extract_exclusions
id: m1-constraint-blocks
file: modules/replication/m1-constraint-blocks.md
---

# Replication M1 — Constraint Block Anchors · Paste-Ready Template

> Every critical constraint gets a stable, numbered, uniquely-anchored
> heading that later steps reference by anchor.

```markdown
## CONSTRAINT BLOCK 1 — Source Priority Rules

The following rules govern all source selection throughout this research.
They remain active at every step; you will restate them before each major
step.

1. Primary sources (peer-reviewed papers, official filings, government
   datasets) take precedence over all others.
2. Aggregators (Wikipedia, summaries, secondary analyses) may be used for
   discovery but may not serve as the sole citation for any factual claim.
3. Social media and blog posts may be used only as **lead indicators**,
   never as primary evidence.
4. When sources conflict, you apply Method: Contradiction Log (defined
   below) — you do not silently pick one side.

---

## CONSTRAINT BLOCK 2 — Temporal Scope

Research covers the period {{temporal_scope_text}}. Sources
outside this window are excluded **unless** they establish a baseline
that is explicitly referenced from within the window.

---

## CONSTRAINT BLOCK 3 — Output Exclusions

You must NOT include:
{{output_exclusions}}
```

**Numbering rules:**

- Number every block sequentially. Block 0 is reserved for the
  Reflection Baseline (see `m0-reflection-baseline.md`).
- Never re-use a number. Never change a block's text mid-prompt.
- If a rule changes, create a new block with a higher number and
  deprecate the old one explicitly in a line like:
  *"CONSTRAINT BLOCK 2 is superseded by CONSTRAINT BLOCK 2b below."*
- Block anchors must be plain ASCII so the target AI can match them in
  its restatements without Unicode-normalization drift.
