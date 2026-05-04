# Bracket Inventory & Classification

> Central reference: every `[BRACKET]` in every module body, classified
> by what kind of marker it is. Read this before "fixing" any bracket.

## Rule of three: brackets fall into THREE categories

### Category 1: STRUCTURAL MARKERS (preserve as-is)

These represent iteration, ordinal position, or schema slots in the
RENDERED PROMPT'S structure — not user-supplied variables. They stay
as `[…]` because the agent reading the rendered prompt needs to see
them as literal labels.

Examples: `[Reason 1]`, `[Act 2]`, `[ITEM N]`, `[STEP 1 applied to ITEM i]`,
`[Pre-Synthesis Integrity Check]`, `[Synthesis]`

**Rule:** if removing the bracket would lose a structural anchor that
the executing agent needs, it's structural. Keep it.

### Category 2: METHOD-ANCHOR PLACEHOLDERS (preserve as-is, but document)

These are dynamic anchors that get composed in by Phase 3 from the
ACTIVE METHOD SET. They look like `[M01]`, `[M__]`, `[M13]` etc. The
render script substitutes them with the actual short_anchor of each
active method.

Examples (in `react.md` and `react-loop-anchored.md`):
  `[M01]`, `[M02]`, `[M06]`, `[M07]`, `[M13]`, `[M__]`

**Rule:** these are NOT user variables and NOT slots in the v3.0
sense. They are documented as such in the partial's concept doc.
Phase 3 has dedicated logic for active-method-anchor expansion.

### Category 3: TRUE VARIABLES (convert to `{{slot}}`)

These ARE user-supplied or pipeline-supplied variables. They map to
slot defs in the module's frontmatter.

Examples: `[Method Name]` → `{{method_name}}`,
          `[H_1]` → `{{hypothesis}}`,
          `[CATALOG FRAMEWORK]` → `{{base_framework}}`

**Rule:** if frontmatter has a slot with a matching name, the bracket
is a slot. If frontmatter doesn't have a slot but logically should,
add the slot to frontmatter, then convert.

## Per-file classification (top-down by bracket density)

### High-bracket files (need most thought)

#### `frameworks/react.md` (15 unique brackets)
| Bracket | Category | Action | Slot name (if cat 3) |
|---------|----------|--------|----------------------|
| `[Act 1]`, `[Act 2]` | 1 (structural) | preserve | — |
| `[Reason 1]`, `[Reason 2]`, `[Reason N]` | 1 (structural) | preserve | — |
| `[Observe 1]`, `[Observe 2]` | 1 (structural) | preserve | — |
| `[Synthesis]` | 1 (structural section anchor) | preserve | — |
| `[Pre-Synthesis Integrity Check]` | 1 (structural) | preserve | — |
| `[M01]`, `[M02]`, `[M06]`, `[M07]`, `[M13]`, `[M__]` | 2 (method anchors) | preserve, documented as Phase-3 substitution | — |

**Verdict:** zero true variables. ALL brackets preserve. The frontmatter
has slot `active_method_anchors` of type `fill_from` that Phase 3
uses to expand `[M__]`-style placeholders.

#### `partials/react-loop-anchored.md` (12 unique brackets)
Same as `react.md` — this partial is composed INTO the react template at
render time, identical bracket landscape. All preserve.

#### `frameworks/synthesis.md` (7 unique brackets)
| Bracket | Category | Action | Slot name |
|---------|----------|--------|-----------|
| `[CATALOG FRAMEWORK]`, `[CATALOG FRAMEWORK NAME]` | 3 | convert | `{{base_framework}}` |
| `[LETTER 1]`–`[LETTER 4]` | 1 (structural — letters of acronym) | preserve OR slot? | discuss in module concept doc |
| `[Name]` | 3 | convert | `{{name_of_bespoke}}` |

#### `replication/m2-restatement-checkpoint.md` (8 unique brackets)
| Bracket | Category | Action | Slot |
|---------|----------|--------|------|
| `[Method Name]` | 3 | convert | `{{method_name}}` |
| `[STEP N / ITERATION N]` | 1 | preserve | — |
| `[Step Title]` | 3 (per-step) | convert | `{{step_title}}` (in iteration ctx) |
| `[Step content here]` | 3 | convert | `{{step_content}}` |
| `[Paste the "How to apply" bullet list verbatim.]` | 3 (instruction text) | convert OR rewrite as Phase-3 directive | `{{howtoapply_block}}` |
| `[Paste the full text of the block here. Do not paraphrase.]` | similar | similar | `{{block_full_text}}` |

#### `replication/m3-batch.md` (7 unique brackets)
| Bracket | Category | Action | Slot |
|---------|----------|--------|------|
| `[ITEM 1]`, `[ITEM 2]`, `[ITEM N]`, `[ITEM i]` | 1 (iteration) | preserve | — |
| `[STEP 1 applied to ITEM i]`, `[STEP 2 applied to ITEM i]` | 1 (iteration) | preserve | — |
| `[LOW / MEDIUM / HIGH]` | 3 (enum) | convert | `{{cardinality_label}}` |

### Medium-bracket files

#### `methods/m05-bayesian-prior.md` (4 unique)
| Bracket | Category | Slot |
|---------|----------|------|
| `[H_1]`, `[H_2]`, `[H_n]` | 1 (iteration over hypotheses) | preserve |
| `[X]` | 3 | `{{prior_value_format}}` (or stays — see concept doc) |

#### `replication/m1-constraint-blocks.md` (5 unique)
Mostly enum/structural — see per-module concept doc.

#### `categories/a-exploration-block.md` (4 unique)
Mostly structural anchors — see per-module concept doc.

#### `cross-pollination/a-into-c.md` (4 unique)
3 are paste-instruction blocks — convert to Phase-3 directives.

### Low-bracket files (1–3 brackets each)

These mostly need a single slot conversion or are structural; details
in per-module concept docs.

`cross-pollination/a-into-b.md`, `methods/m01-falsification.md`,
`cross-pollination/c-into-a.md`, `methods/m03-pre-mortem.md`,
`categories/c-lifecycle.md`, `cross-pollination/b-into-a.md`,
`methods/m07-contradiction-log.md`, `methods/m08-what-would-change-my-mind.md`,
`methods/m10-first-principles.md`, `methods/m11-assumption-decay.md`,
`methods/m12-base-rate.md`

### Zero-bracket files (already clean)

22 files. Body uses no `[BRACKETS]`. Either:
- They're pure prose modules (e.g., `frameworks/care.md`), OR
- They've already been converted to `{{slots}}` (e.g.,
  `methods/m13-adversarial-query-expansion.md` has 7 slots),  OR
- They are partials that take all input from frontmatter (e.g.,
  `partials/frontmatter-template.md` has 11 slots)

These need only concept docs, no body fixes.

## Open question (logged for review before sweep) — RESOLVED 2026-05-02

- **`frameworks/synthesis.md` `[LETTER 1]`–`[LETTER 4]`:** structural
  acronym placeholders OR true slots? If bespoke synthesis is composed
  from 4 catalog frameworks, the letters represent ordinal positions
  in the resulting acronym. Argument for slot: the actual letters
  vary per-bespoke-instance and Phase 2 needs to capture them.
  Argument for structural: the acronym is generated, not user-supplied.
  → **DECISION (executed):** the 4 LETTER lines + provenance lines are
  rendered by Phase 3 from the structured `components` slot via two
  derived `fill_from` slots: `components_render_block` (the bullet
  block) and `provenance_render_block` (the provenance lines). The
  individual `[LETTER N]` brackets no longer appear in the body.
  Plus a new `first_action_directive` (`phase2_fill`) replaces the
  old "[A concrete restatement directive...]" placeholder. See
  `docs/frameworks/synthesis.md` for full slot inventory.

- **`replication/m2-restatement-checkpoint.md` paste-instruction blocks:**
  These say things like "Paste the full text of the block here. Do not
  paraphrase." That's an instruction to whoever fills the slot, not a
  template marker. Two options:
  (a) Convert to slots whose `description:` carries the "paste verbatim"
      instruction.
  (b) Rewrite body so Phase 3 render emits the directive automatically
      via slot definition metadata.
  → **DECISION (executed) — (b) hybrid:** the body now uses two
  `fill_from` slots — `cb_restatement_block` and
  `method_restatement_block` — that Phase 3 fills with the verbatim
  restatement lines (each carrying the "paste verbatim" instruction
  in the rendered template, where it instructs the EXECUTING agent at
  runtime, not Phase 3). Plus three `agent_runtime_fill` slots
  formalize the inner step variables: `step_or_iteration_label`,
  `step_title`, `step_content`. See
  `docs/replication/m2-restatement-checkpoint.md` for full inventory.

- **`replication/m3-batch.md` `[LOW / MEDIUM / HIGH]`:** clear true
  variable.
  → **DECISION (executed):** added `confidence_label` slot
  (`agent_runtime_fill`, enum LOW/MEDIUM/HIGH). Body uses
  `{{confidence_label}}`. All other brackets in m3-batch
  (`[ITEM N]`, `[STEP N applied to ITEM i]`, etc.) are confirmed
  Category-1 structural iteration markers and remain as-is. See
  `docs/replication/m3-batch.md`.

## Sweep status

- Sweep complete: 2026-05-02 (v3.0-phase2-modules → v3.0.1)
- Total slot conversions executed: 14 (driven by frontmatter
  slot definitions per module)
- Total new slots defined during template-fix Phase A: 9
  (synthesis: 3, m2-restatement: 5, m3-batch: 1)
- Total `self_applied_phase2:` frontmatter blocks synced with
  catalog index: 3 (M01, M13, m0-reflection)
- All 40 module-files have a corresponding concept doc in
  `docs/<type>/<id>.md`
