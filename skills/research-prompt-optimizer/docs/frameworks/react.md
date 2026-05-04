# `react` — ReAct (Reason / Act / Observe Loop)

**File:** `modules/frameworks/react.md`
**Type:** framework (agentic, mandatory)
**Mandatory:** YES — appears in every rendered prompt regardless of category
**Self-applied in Phase 2:** no

## Purpose

Provides the agentic execution loop for the executing research agent.
Unlike structural frameworks (RISEN, TIDD-EC, etc.) which shape the
*output*, ReAct shapes the *process*: the iterative Reason → Act →
Observe cycle that drives every agentic research turn.

In v3.0 ReAct is **anchored**: every Reason phase is rendered with an
inline table of currently-active methods plus their escape criteria.
This is the KEY INNOVATION over v2.1, where ReAct was generic and
agents would drift away from the active method set in long runs.

## Slot inventory

| Slot name | Type | Filled by | Required | Notes |
|-----------|------|-----------|----------|-------|
| `active_methods_table` | `fill_from` | Phase 3 render script — composes a Markdown table from `meta-prompt.selected_methods[]` | yes | columns: `anchor`, `method`, `when_to_choose` |

**Structural markers (NOT slots):**

The body contains MANY `[BRACKETS]` that are NOT user variables. They
are documented here exhaustively so future edits don't accidentally
"fix" them into slots:

### Iteration markers (preserve)

| Bracket | Meaning |
|---------|---------|
| `[Reason 1]`, `[Reason 2]`, `[Reason N]` | Ordinal label of each Reason phase in the loop |
| `[Act 1]`, `[Act 2]` | Ordinal label of each Act phase |
| `[Observe 1]`, `[Observe 2]` | Ordinal label of each Observe phase |
| `[Pre-Synthesis Integrity Check]` | Named checkpoint at end of loop |
| `[Synthesis]` | Final section anchor |

### Method-anchor placeholders (preserve, but documented)

| Bracket | Meaning |
|---------|---------|
| `[M01]`, `[M02]`, `[M06]`, `[M07]`, `[M13]` | Concrete method anchors — these are LITERAL labels in the active-methods table that gets composed in via `active_methods_table` slot |
| `[M__]` | Generic placeholder in instructional text — means "the active method this Act"; agent fills based on which method is being applied in the current iteration |

These are NOT `phase2_fill` or `agent_runtime_fill` slots. They are
**display anchors** that mirror the short_anchor field of the
catalog method entries. The actual table content is filled
programmatically by Phase 3 from `meta-prompt.selected_methods[]`,
which is why the only TRUE slot is `active_methods_table`.

## Body composition

- **Section anchor:** `## Agentic Loop — ReAct (Reason / Act / Observe)`
- **Order constraint:** ALWAYS appears AFTER all structural framework
  blocks (RISEN/TIDD-EC/CO-STAR/CARE/CRISPE/synthesis) and BEFORE
  the methods reference table. ReAct is the EXECUTION layer; structural
  frameworks shape the OUTPUT layer.
- **Composition partner:** the `partials/react-loop-anchored.md`
  partial is composed INTO this framework — it provides the actual
  loop template with anchored Reason phases. ReAct framework is
  effectively `react.md` (intro + active_methods_table) + partial
  (loop template).

## Split decision

**Currently:** main framework file + `react-loop-anchored.md` partial
**Should it stay split?** YES — current split is correct:
  - `react.md`: framework metadata, intro, the active_methods_table slot
  - `partials/react-loop-anchored.md`: the loop body template with all
    iteration markers
**Why split:** the partial can be reused outside the framework (e.g.,
if a future bespoke synthesis wants the anchored loop without the
framework intro). The framework file declares the slot contract;
the partial provides the rendered structure.

## How `[M__]` substitution actually works

This is the part most likely to confuse future readers. Step by step:

1. Phase 2 commits to a method set, e.g. `[M01, M02, M07, M13]`.
2. Phase 2 writes this to `meta-prompt.selected_methods[]`.
3. Phase 3 render script:
   a. Reads `meta-prompt.selected_methods[]`.
   b. Reads each method's frontmatter from `catalog.yaml` to get its
      `short_anchor` and `when_to_choose_short` fields.
   c. Composes a Markdown table with one row per method.
   d. Substitutes the `{{active_methods_table}}` slot with this table.
4. The `[M__]` placeholders inside the partial body STAY AS LITERAL
   `[M__]` text in the rendered prompt — they are agent-facing
   instruction text saying "fill this with whichever method you are
   applying right now in this Act phase".

In other words: `[M__]` is NOT a slot. It is a directive to the
**executing agent** to label its work, similar to how `<your name>`
in a fillable form is not a "slot" but an instruction.

## Future extension points

1. **ReAct-with-Tools variant** — current ReAct is research-search-
   centric (Act = search). For tool-using agents, an Act phase might
   be a tool call. Could extend with a flavour flag in frontmatter:
   `react_flavour: search-only | tool-using | hybrid`. Body would
   condition on flavour.
2. **Loop budget** — currently the loop runs until "no novel
   evidence". Some intents need a hard cap (e.g., 5 iterations max).
   Add slot `max_loop_iterations` (type: `phase2_fill_or_runtime`,
   filled from `intent.budget.max_loop_iterations` if present).
3. **Reflection cadence** — currently reflection happens via M0 at
   5 fixed checkpoints. Could expose `reflection_every_n_acts` as
   slot for finer control.

## Open questions

- [ ] Should the partial path be referenced explicitly in
      `react.md`'s frontmatter (e.g., `composed_with: [partials/react-loop-anchored]`)?
      Currently the relationship is implicit (Phase 3 knows to inline
      it). Making it explicit would make composition visible in the
      catalog. Defer to Phase 3 design.
- [ ] What happens if the active method set is empty (impossible in
      v3.0, but theoretically)? Render-time fallback should produce
      a single-row table saying "(no active methods — generic ReAct)".
      Add as integrity check in Phase 3 render.

## Catalog cross-reference

- Catalog entry: `catalog.yaml` → `modules.react`
- Triggered by signals: n/a (mandatory in every prompt)
- Default for category: A, B, C (all)
- Self-applied hook: no

## Change log

- `2026-05-02` (v3.0-phase2): initial concept doc; body unchanged
  (all 15 brackets confirmed structural or method-anchors, none
  convertible to slots). Composition with
  `partials/react-loop-anchored.md` documented explicitly.
