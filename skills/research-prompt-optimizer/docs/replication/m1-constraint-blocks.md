# M1 — Constraint Blocks (Source Priority + Temporal Scope + Output Exclusions)

**File:** `modules/replication/m1-constraint-blocks.md`
**Type:** replication
**Mandatory:** YES — appears in every prompt as Constraint Blocks 1, 2, 3
**Self-applied in Phase 2:** no (intent.yaml is the constraint, no need for additional blocks at Phase-2 level)

## Purpose

Defines the three standard authored constraint blocks that follow CB 0 (Reflection Baseline) in every rendered prompt:

- **CB 1 — Source Priority Rules:** what kinds of sources to prioritize / accept / reject
- **CB 2 — Temporal Scope:** the time window the research covers
- **CB 3 — Output Exclusions:** what NOT to include in the output

These blocks are authored from `intent.known_constraints` content. When the intent has constraints in those categories, Phase 2 lifts them into the corresponding block; when not, the block uses a sensible default.

## Slot inventory

| Slot name | Type | Filled by | Required | Notes |
|-----------|------|-----------|----------|-------|
| `source_priority_rules` | `phase2_fill` | Phase 2 from `intent.known_constraints.sources` if present, else canonical default | yes | Block 1 content |
| `temporal_scope_text` | `phase2_fill` | Phase 2 from `intent.temporal_scope` (full sentence form) | yes | Block 2 content (substitutes the full date sentence) |
| `output_exclusions` | `phase2_fill` | Phase 2 from `intent.known_constraints.exclusions` (list, formatted as bullet block) | yes | Block 3 content (Phase 3 expands list into bullets) |

**Structural markers:** `[CONSTRAINT BLOCK 1]`, `[CONSTRAINT BLOCK 2]`, `[CONSTRAINT BLOCK 3]` — section header anchors. Stay as labels.

## Body composition — Phase-3 expansion semantics

The slot `output_exclusions` is a **list**, not a string. Phase 3 expands it into a bullet block:

```python
# Pseudocode
exclusions_list = meta_prompt["constraint_blocks"][3]["output_exclusions"]  # list of strings
output_exclusions_block = "\n".join(f"- {ex}" for ex in exclusions_list)
body = body.replace("{{output_exclusions}}", output_exclusions_block)
```

The other two slots (`source_priority_rules`, `temporal_scope_text`) are strings — direct substitution.

## Body composition — placement

- **Section anchor:** three sub-anchors `## CONSTRAINT BLOCK 1 — Source Priority Rules`, `## CONSTRAINT BLOCK 2 — Temporal Scope`, `## CONSTRAINT BLOCK 3 — Output Exclusions`
- **Order constraint:** CB 1, 2, 3 always come AFTER CB 0 (M0 Reflection Baseline) and BEFORE methods/structural framework.
- **Composition partner:** M0 Reflection (preceding), M2 Restatement Checkpoint (which forces verbatim restatement of all CBs at every step).

## Split decision

**Currently:** single file with three sections (CB 1, 2, 3)
**Should it split?** Considered — could split into three files (one per block).
**Decision:** No split. The three blocks share a common purpose (intent-derived constraints) and are always rendered together.
**Trigger that would force a split:** if a future intent type demanded CB 4+ (additional constraint categories beyond source/temporal/exclusions), an extensible split into `m1-cb-base.md` + `m1-cb-extended.md` could emerge.

## Future extension points

1. **CB 4+ for domain-specific constraints** — currently fixed at CB 1/2/3. Add support for `intent.known_constraints.domain_specific[]` which renders as additional numbered blocks.
2. **Source-priority taxonomy** — current CB 1 is free-form. Could constrain via slot `source_priority_taxonomy` (e.g., "academic-first", "primary-source-first", "regulator-first") with auto-generated bullet rules.
3. **Auto-derived temporal scope** — `temporal_scope_text` currently asks Phase 2 to format the full sentence. Could expose `temporal_scope_start` and `temporal_scope_end` as separate slots with template "from {{start}} through {{end}}" for cleaner Phase-2 fill.

## Open questions

- [ ] Should `output_exclusions` enforce a minimum count (e.g., must have at least 1 exclusion)? Empty list currently renders an empty bullet block. Add Phase-3 integrity check.
- [ ] When `intent.known_constraints` is empty, the canonical defaults in CB 1 apply — but those defaults aren't currently captured anywhere as a constant. Add `default_source_priority_rules` constant to catalog.

## Catalog cross-reference

- Catalog entry: `catalog.yaml` → `modules.m1-constraint-blocks`
- Triggered by: mandatory in every prompt
- Default for category: A, B, C (all)
- Self-applied hook: no

## Change log

- `2026-05-02` (v3.0-phase2): initial concept doc; body fix converted `[START DATE] through [END DATE]` → `{{temporal_scope_text}}` (single string slot for full sentence) and `[EXCLUSION 1..3]` → `{{output_exclusions}}` (Phase 3 expands list into bullet block).
