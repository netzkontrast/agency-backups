# Methodology

## Scope

This is the **kickoff** research phase. It collects evidence required by Task 015 plan steps 2–11 (schemas, ontology bootstrap, frontmatter annotation, scenario tagging) but does not author any of those artefacts itself. Authoring is downstream and out of scope for this run.

## Methods applied

### M01 — Falsification (Karl Popper's disconfirmation principle)

Applied to the central design hypothesis from `task.md`:

> *"Per-term frontmatter is sufficient to power scenario-keyed lookup without a separate scenario index."*

What would falsify it:
- Median scenarios-per-term > 8 → frontmatter becomes large; navigator MUST also build an offline `scenario-index.json`.
- Scenarios cross-reference each other → per-term frontmatter cannot capture; index needs a second key.

Findings logged in [`/research/integrate-dramatica-ncp-skills/reflection/M01-falsification.md`](../reflection/M01-falsification.md). Verdict: hypothesis survives the kickoff evidence (median scenarios-per-term ≈ 2.4 in the first-pass survey, well under cap).

### M07 — Contradiction Log

Scanned the four primary skills (`dramatica-theory`, `dramatica-vocabulary`, `ncp-author`, `novel-architect`) for contradictions in: throughline naming, character-dynamic naming, structural-model cardinality, NCP enum closure. Findings logged in [`/research/integrate-dramatica-ncp-skills/reflection/M07-contradiction-log.md`](../reflection/M07-contradiction-log.md). Three concrete contradictions surface; all are resolvable by the canonical-ID-plus-aliases pattern proposed in `task.md § Target Architecture`.

### Corpus walk via Explore subagent

The vocabulary corpus (22 files) and theory corpus (15 chapters) were enumerated by an `Explore` subagent invoked in parallel with the cross-skill audit work. The subagent returned heading-level inventories without loading file bodies into the main session — preserving token budget for synthesis. Subagent results were cross-checked by direct `grep -c` on synonym + dynamic-pair indexes (512 / 75 confirmed); numerical disagreement on element count (71 vs canonical 64) was resolved by inspection: the seven extras are meta-entries, not Element overshoot. Documented in [`inventory.md`](./inventory.md) and [`id-audit.md`](./id-audit.md).

## Methods deliberately deferred to downstream phases

- **M03 Pre-Mortem** — already authored as part of `task.md § Pre-Work`; re-running here would be redundant.
- **M13 Adversarial Query Expansion** — relevant when the Task 015 prompt body is authored (step 14). Not relevant to a corpus-walk kickoff.
- **M0 Reflection** — runs at session-end of the *full* Task 015 run, not at the kickoff sub-run.

## Honest framing

This kickoff is intentionally narrow. It answers three concrete questions (*what's in the corpus?*, *do the skills agree on names?*, *which scenarios attach where?*) and stops. The schema-authoring, ontology-bootstrap, and navigator-implementation work in Task 015's plan downstream of this kickoff is a different shape of work and benefits from a different methodology — that's why the prompt at `/prompts/integrate-dramatica-ncp-skills/prompt.md` will use `RISEN+ReAct` while this kickoff used corpus-walk + targeted greps.
