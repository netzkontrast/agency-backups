# M03 — Post-Implementation Pre-Mortem

The kickoff `task.md` ran a Pre-Mortem ahead of design (`task.md § Pre-Work § Pre-Mortem (M03) — Top 5 Failure Modes`). This file revisits those five predicted failures **after** the implementation landed, asking the discipline-question: *which ones actually happened, which didn't, and what does the difference teach?*

## Kickoff predictions vs reality

| # | Predicted failure | Mitigation that was committed | Did it happen? | What we learned |
|---|---|---|---|---|
| 1 | **Schema bloat** — ontology absorbs every edge case, grows past 30 fields | "Freeze schema at v0.1 with the minimum fields … reject in-flight additions" | **No.** Final ontology entry has ≤17 fields (per `ontology.schema.json`). Cap held. | Discipline of declaring the freeze upfront worked — when D-1 (adding `kind: throughline`) tempted me toward broader expansion, the freeze rule kept the addition surgical. |
| 2 | **Scenario explosion** — 11 categorical scenarios → per-document IDs → state index | "Scenarios are categories, not project artefacts. Reserve `scenario_id` for categorical IDs only" | **No.** 11 scenarios in v0.1, no growth. Per-term frontmatter median 1 scenario, max 4. M01 contingency never activated. | The categorical-vs-instance distinction was the right line. Scenarios survived as a small bounded vocabulary. |
| 3 | **Navigator becomes a god-tool** — single Python tool absorbs nav + validate + extract + build | "Ship four small scripts (`nav`, `extract`, `validate`, `ontology-build`) with shared lib" | **No.** Final shape is exactly 4 scripts + 3 lib modules, each ≤ 514 lines. | Decomposition before code was the right call. Each script tested independently in `tests/`. |
| 4 | **Skills tightly coupled to navigator** — `dramatica-vocabulary/SKILL.md` references navigator paths, breaks in environments without Python | "Skills MUST keep prose lookup as primary; navigator is *complement*, not replacement" | **Mostly no, with caveat.** SKILL.md sections (Step 10) document navigator as a *fast path* for structural questions; prose remains primary for conceptual questions. The token-economy benchmark (83.4%) means agents will gravitate toward the navigator anyway. | The "complement, not replacement" framing held — but the benchmark margin is so large that in practice the navigator IS the primary path. The conceptual-vs-structural distinction in the SKILL.md sections is what protects environments without Python (or with stale ontology). |
| 5 | **Cross-skill ontology drift** — `ncp-author`, `novel-architect`, dramatica skills update separately, IDs drift | "Single ontology file. Skills reference IDs; they do not coin new ones. CI check verifies." | **No, by enforcement.** `validate.py` (Step 8) + `tools/check-governance.sh` integration (Step 11) make drift a CI gate. The 5 hard-error invariants catch drift before commit. | The CI integration was the load-bearing piece. Without `tools/check-governance.sh` calling `validate.py`, this prediction would have come true within 1–2 sessions. |

**Score: 0 of 5 predicted failures materialized.** The mitigations committed at task time were all retained in the final design.

## Failures that DID happen (not predicted)

Three classes of issue arose during execution that the kickoff Pre-Mortem missed:

### F1 — Sonnet C populated `ncp_appreciation` on character-dynamic + plot-dynamic entries with values that aren't NCP enum strings

The Sonnet brief asked C to set `ncp_appreciation = canonical_label` for these kinds. That was the wrong instruction — per kickoff SPEC §2.5, character-dynamics and plot-dynamics map to NCP slot-name patterns (e.g. `main_character_resolve`) that compose with the throughline at storypoint-fill time, not to single appreciation values.

**Caught by:** the validate.py NCP enum closure check during Step 8 verification.
**Fix:** stripped `ncp_appreciation` + `ncp_appreciation_partial` from the 8 affected entries (per commit `e5fde19`).
**Lesson:** when delegating ontology population to a sub-agent, the brief MUST explicitly enumerate which kinds get which fields — "use `canonical_label`" is too generic.

### F2 — `dynamic-pairs-index.md` contains pairs that conflict with canonical Dramatica

The source file lists 75 reciprocal pairs but at least one (`Destiny ↔ Fantasy`) contradicts canonical Dramatica geometry (Destiny pairs with Fate per `element-quads.md`'s Universe-Fate Quad). Sonnet D faithfully transcribed the source list.

**Caught by:** the validate.py reciprocity check (entity Destiny couldn't have two simultaneous dynamic-pair partners).
**Fix:** dropped `dp.destiny-fantasy` during Step 4b merge (per commit `2d6007c`).
**Lesson:** source-of-truth files in legacy corpora may carry historical errors. Validate.py's reciprocity check IS the hedge against this.

### F3 — Slug-format mismatch between Sonnet C's hand-authored `term_file` anchors and Step 5's heading-derived slugs

Sonnet C populated some `term_file` pointers with semantic anchors (e.g. `term_file: archetypes.md#contents`) that don't match the `## <Term>` heading slugify. Step 5's bulk frontmatter insertion couldn't auto-match those entries.

**Caught by:** Step 5's coverage report — 187 of 293 `## ` headings matched (64% coverage).
**Mitigation:** documented as a v0.1 known limitation; validate.py emits `term_file-anchor-mismatch` warnings (8 cases) for mechanical cleanup in v0.2.
**Lesson:** when one agent produces a pointer that another agent consumes for matching, the matching algorithm must be explicit upfront. (My Step 5 brief said "match by slug derived from heading" but didn't enumerate the slugify variants.)

## Net assessment

The Kickoff M03 Pre-Mortem covered the **structural** failure modes well (schema/scenario/tool/skill/drift). It missed the **delegation-protocol** failure modes (sub-agent briefs being too loose for ontology population, source-corpus errors propagating through faithful transcription, slug-format collisions in cross-agent consumption).

For v0.2 / future similar projects: **add a sixth Pre-Mortem dimension — *agent-coordination protocol failures*.** The mitigation is briefs that are explicit about (a) per-kind field semantics, (b) slug-derivation algorithms when one agent's output feeds another agent's matching, (c) which source-corpus claims to verify against canonical sources before transcribing.

## Friction during execution

Recorded in [`/research/integrate-dramatica-ncp-skills/reflection/friction-log.md`](./friction-log.md). Highlights of friction at FL > 0 during the synthesis phase:
- One Sonnet sub-agent dispatch hit a quota limit during Step 9 (test authoring); fell back to main-context authoring with no quality loss.
- One stop-hook fired on uncommitted changes during Step 11; resolved by squashing the wire-CI commit.
- One merge conflict against main (PRs #41 + #43 added overlapping `tools/check-governance.sh` content); resolved by keeping both stages in numerical order.

None of these reached FL2 — all were tractable in the same session.

## Next phase

Plan Step 15: friction log final entry, flip `task_status: done`, close PR #39 (or update its description with the as-built summary). No new work needed.
