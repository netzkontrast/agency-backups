# Category A — Exploration (Recursive Search / Tree of Thoughts)

**File:** `modules/categories/a-exploration.md`
**Type:** category
**Mandatory:** routing-dependent (only emitted if Phase 2 routes to A)
**Self-applied in Phase 2:** no (categories aren't self-applied; only methods/replication can be)

## Purpose

Category profile for **Exploration** research: tasks where the answer
is genuinely unknown at the start and must be discovered through
hypothesis generation, branching search, and backtracking. The body
ships as the **Epistemological Layer** block in the rendered prompt —
it tells the executing agent *how to think* about the research, not
*what to find*.

Triggers when intent has signal words like `why does`, `warum scheitert`,
`find gaps`, `explore`, `hypothesize`, `i suspect`, `what's really
going on`, `unbekannte ursache`, `hypothesen testen`.

## Slot inventory

**No template slots in the body.** The body is the canonical
Epistemological Layer text and is rendered verbatim. Categories don't
participate in the slot system — they're complete prose blocks with
five operational principles.

**Structural markers (NOT slots):**

- `[BRACKETED]` (in the intro prose, NOT in the rendered block) —
  a stale v2.1 instruction telling the operator to "adapt brackets to
  topic". Not rendered into output. Could be removed in a future polish
  pass; harmless for now.
- `[H1]`, `[H1 failure case]`, `[H1 null result]` (in step 2 of the
  rendered block) — pedagogical examples showing the agent how to
  formulate orthogonal queries. They stay as `[H1]` in the rendered
  prompt because they're literal examples, not slot fills.

## Body composition

- **Section anchor:** `## Epistemological Layer — Category A (Exploration)`
- **Order constraint:** ALWAYS first major section after the meta-header.
  Sets the cognitive frame before any methods, frameworks, or constraint
  blocks.
- **Composition partners:** governs which methods are added by default
  (M01 Falsification, M02 Steelmanning, M04 Contrast Classes, M05
  Bayesian Prior, M10 First-Principles), which structural framework
  is used by default (RISEN), and which cross-pollinations are paired
  (b-into-a, c-into-a).

## Frontmatter contract

| Field | Value | Used by |
|-------|-------|---------|
| `default_methods` | `[M01, M02, M04, M05, M10]` | Phase 2 sub-phase 4.3 module selection |
| `default_framework_structural` | `risen` | Phase 2 sub-phase 4.3 framework selection |
| `cross_pollination_pair` | `[b-into-a, c-into-a]` | Phase 2 sub-phase 4.3 CP selection (locked at exactly 2) |
| `typical_batches` | `[]` (empty) | Phase 2 sub-phase 4.4 batch detection — exploration is recursive, not batched |
| `signal_words` | (10 entries) | Phase 2 sub-phase 4.2 routing cascade |

## Split decision

**Currently:** single file
**Should it split?** No — the five operational principles form a
coherent epistemological doctrine. Splitting would fragment the
"how to think" message.
**Trigger that would force a split:** if a future intent demanded a
**deep-dive variant** (e.g., 8 principles for academic literature
review) vs. a **quick variant** (e.g., 3 principles for product
discovery), a split into `a-exploration-deep.md` and
`a-exploration-quick.md` would make sense, gated by `intent.depth`.
Not currently planned — the current 5 principles cover both depths
adequately.

## Future extension points

1. **Hypothesis-tree visualization directive** — add an optional
   block (gated by intent flag) that asks the agent to produce a
   Mermaid/text tree diagram of considered hypotheses, branches,
   abandonments. Would land as a new partial
   `a-exploration-hypothesis-tree.md` composed in when
   `intent.output_format` mentions diagram/tree/visualization.
2. **Backtracking budget** — the current "after three search iterations"
   is a hard-coded heuristic. Could become an intent-controlled
   parameter `intent.backtrack_threshold` with default 3.
3. **"Don't know" calibration** — step 5 says "we don't know" is valid;
   could add a calibration block requiring the agent to estimate
   confidence in the no-answer conclusion (e.g., "this is unanswerable
   given evidence ≤ 6 months old; might be answerable later").

## Open questions

- [ ] Is the v2.1-leftover `[BRACKETED]` instruction in the intro
      prose worth removing? Not user-visible, but stale. Defer to
      next polish pass.
- [ ] Should `default_methods` include M03 Pre-Mortem? Pre-mortem fits
      the exploration mindset (imagining failure modes), but it's
      currently default for Cat-C. Discuss in next iteration if
      Cat-A intents repeatedly request risk-thinking.

## Catalog cross-reference

- Catalog entry: `catalog.yaml` → `categories.A`
- Triggered by signals: see frontmatter `signal_words`
- Routed by: Phase 2 sub-phase 4.2 cascade (uses signal_words against
  `intent.research_question` + `research_question_unpacked`)

## Change log

- `2026-05-02` (v3.0-phase2): initial concept doc; body unchanged (all
  4 brackets are pedagogical examples, no conversion needed).
