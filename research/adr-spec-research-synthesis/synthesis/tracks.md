---
type: note
status: active
slug: adr-spec-research-synthesis-tracks
summary: "Per-track work breakdown for Task 027's research run."
created: 2026-05-05
updated: 2026-05-05
---

# Tracks

Four parallel-executable tracks. They are sequenced linearly here because each downstream track consumes the upstream output.

## Track A — Analyze (Step 1)

**Inputs:** root specs (9 files), tooling (10 files), `header-ontology.json`, Gemini draft.
**Output:** [`../workspace/analysis.md`](../workspace/analysis.md) — six sections (A: implicit ADRs; B: structural conventions; C: Gemini-vs-repo conflicts; D: reusable primitives; E: hook diagram; F: routing to Step 2).
**Method:** [M06] Source Triangulation (≥ 2 sources per finding).

## Track B — Brainstorm (Step 2)

**Inputs:** Track A output.
**Output:** [`../workspace/brainstorm.md`](../workspace/brainstorm.md) — five integration questions, each with a labelled conclusion.
**Method:** [M07] Contradiction Log (conflicts → contradictions reflection file).

## Track C — Reflect (Step 3 + CB0 checkpoints)

**Inputs:** Tracks A and B.
**Output:** four reflection files plus `friction-log.md`:
- `M06-source-triangulation.md`
- `M07-contradictions.md`
- `M08-what-would-change-my-mind.md`
- `M13-query-expansion.md`
- `friction-log.md` (highest FL1)

**Method:** five mandatory CB0 reflection checkpoints (Kickoff, Mid-run, Post-M13, Pre-synthesis, Post-synthesis) — each captured inline in `M13-query-expansion.md` § "Reflection Regime".

## Track D — Draft (Step 4)

**Inputs:** all of A, B, C.
**Output:** [`../output/SPEC.md`](../output/SPEC.md) — §0–§9 schema-locked.

**Method:** every §X.1 normative table is re-derived from the analysis findings; every §X.2 Gherkin scenario carries an `# anchor: ADR.A.<n>.<m>` comment; §X.3 rationale is lowercase prose without RFC 2119 keywords (per `AGENTS.md` Spec Language Reference R2).

## Sequencing

```text
A → B → C → D
       ╲    │
        ╲   │
         ╲  ▼
          ╲ §8 of SPEC.md surfaces every [OPEN]/[DEFERRED] from B
           ╲▼
        §9 of SPEC.md surfaces M07 contradictions + M13 axes from C
```

## Verification

- After D, [`../../../tools/check-governance.sh`](../../../tools/check-governance.sh) MUST exit 0 against the new files.
- `state.md` MUST show every step `[x]` before commit.
- `friction-log.md` MUST declare an FL value at the top.
