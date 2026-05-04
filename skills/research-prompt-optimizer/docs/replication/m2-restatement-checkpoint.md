# M2 — Per-Step Restatement Checkpoint

**File:** `modules/replication/m2-restatement-checkpoint.md`
**Type:** replication
**Mandatory:** YES (every multi-step prompt)
**Self-applied in Phase 2:** no (Phase 2 has 10 sub-phases — full M2 restatement at every transition would be overkill; rejected for self-application during Q6 design)

## Purpose

Forces the executing agent to restate, verbatim, all active constraint
blocks and active critical-thinking methods at the start of every
step/iteration. Prevents silent semantic drift through summarization
across long-running research.

The "verbatim" requirement is load-bearing: paraphrase is the failure
mode this module exists to prevent.

## Slot inventory

| Slot name | Type | Filled by | Required | Notes |
|-----------|------|-----------|----------|-------|
| `active_constraint_blocks` | `fill_from` | Phase 3 — iterates over `meta-prompt.constraint_blocks[]` | yes | Drives per-CB bullet generation |
| `active_methods` | `fill_from` | Phase 3 — iterates over `meta-prompt.selected_methods[]` | yes | Drives per-method bullet generation |

**Structural markers (NOT slots):**

| Bracket | Meaning |
|---------|---------|
| `[STEP N / ITERATION N]` | Agent-facing label — the executing agent fills with the actual step number at runtime |
| `[Method Name]` (×2) | Per-method placeholder in the iteration pattern; Phase 3 expands one bullet per active method |
| `[Step Title]` | Agent-facing label — runtime fill |
| `[Step content here]` | Agent-facing label — runtime fill |
| `[Paste the full text of the block here. Do not paraphrase.]` (×4) | **Agent-facing instruction**, NOT a slot. Tells the executing agent how to fill the bullet. The instruction itself is rendered into the prompt. |
| `[Paste the "How to apply" bullet list verbatim.]` | Same — agent-facing instruction, rendered as-is |

**Why none of these become `{{slots}}`:** they are instructions to the
EXECUTING AGENT inside the rendered prompt, not template variables
that Phase 2 or Phase 3 fills.

## Body composition — special Phase-3 semantics

This module has **iteration semantics** that differ from typical
modules. Phase 3 render does NOT just substitute slots — it generates
the bullet list **dynamically based on slot CONTENT**:

### Phase-3 render pseudocode for this module

```python
# Read slot content
cb_list = meta_prompt["constraint_blocks"]      # e.g., 4 blocks
method_list = meta_prompt["selected_methods"]   # e.g., 5 methods

# Render header (literal from body)
output += "### Restatement Checkpoint — Before [STEP N / ITERATION N]\n\n"
output += "Before executing this step, I restate the currently-active constraints verbatim:\n\n"

# Render CB list — ONE BULLET PER ACTIVE CB (driven by slot content)
for cb in cb_list:
    output += f"- **CONSTRAINT BLOCK {cb.id} — {cb.title}:** "
    output += f"[Paste the full text of the block here. Do not paraphrase.]\n"

output += "\nI also restate the currently-active critical-thinking methods:\n"

# Render method list — ONE BULLET PER ACTIVE METHOD
for method in method_list:
    output += f"- **Method: {method.full_name}** — "
    output += f"[Paste the \"How to apply\" bullet list verbatim.]\n"

# Render step skeleton (literal from body)
output += "\nI confirm these are active for the step below.\n\n"
output += "### [STEP N / ITERATION N] — [Step Title]\n\n"
output += "[Step content here]\n"
```

The body file functions as a **BLUEPRINT** showing the expected
structure with example entries (CB 0–3, generic Method Name). Phase 3
overrides the blueprint with the actual active slot content.

## Body composition — placement

- **Section anchor:** the rendered restatement-checkpoint block is
  prepended to EVERY step in the executing agent's loop. The module's
  body file shows ONE such block; Phase 3 doesn't rerender it
  per-step (the agent does that), but Phase 3 ensures the right
  number of CB/method bullets are inside the template.
- **Order constraint:** rendered as part of the agentic loop (alongside
  ReAct framework). Logically comes before each step's substantive
  work.
- **Composition partner:** ReAct framework (which loops); M0 Reflection
  (whose 5 checkpoints overlap with M2's per-step gate).

## Split decision

**Currently:** single file
**Should it split?** No — the CB-restatement and Method-restatement
sections are tightly coupled by the "single restatement gate per step"
concept. Splitting would break the checkpoint's atomicity.
**Trigger that would force a split:** if a future intent demanded
constraint-restatement WITHOUT method-restatement (very short,
constraint-heavy intents), a `m2-restatement-cb-only.md` variant could
emerge. Not currently planned.

## Future extension points

1. **Restatement frequency control** — currently every step. For long
   loops with many cheap steps, every-step is wasteful. Add slot
   `restatement_every_n_steps` (default 1, increase for cheap-step
   workloads).
2. **Diff-only restatement** — instead of full verbatim restatement,
   restate only what CHANGED since last checkpoint. Reduces token
   cost. Would need new partial `m2-diff-restatement.md`.
3. **Self-check on restatement quality** — add an agent-facing
   instruction "verify the restatement matches the original word-for-
   word; abort step if mismatch". Currently implicit in "verbatim";
   could be explicit.

## Open questions

- [ ] The body has hard-coded "CONSTRAINT BLOCK 0..3" in the example
      bullets, but Phase 3 generates them from slot content. Is that
      visual mismatch between body-as-blueprint and actual-output
      acceptable, or should the body be rewritten as a more abstract
      schema (e.g., "CONSTRAINT BLOCK <id>")? Pragmatic answer: keep
      as-is because example numbers help readers understand intent.
- [ ] Should `active_constraint_blocks` and `active_methods` slots
      have a `min_count` validation (e.g., must have at least 1)?
      Currently no — empty list would render an empty section. Add
      to Phase-3 integrity check.

## Catalog cross-reference

- Catalog entry: `catalog.yaml` → `modules.m2-restatement-checkpoint`
- Triggered by signals: n/a (mandatory in every prompt with multiple steps)
- Default for category: A, B, C
- Self-applied hook: no

## Change log

- `2026-05-02` (v3.0-phase2): initial concept doc; body unchanged
  (all 8 unique brackets confirmed structural — none convertible to
  slots; Phase-3 iteration semantics documented explicitly).
