# Jules Brief — Slice 1: Dramatica Engine (PILOT)

- **alias:** `kp-incubator-dramatica`
- **repo:** `netzkontrast/agency-backups`
- **starting branch:** `claude/dreamy-galileo-06exy`
- **write only here:** `kohaerenz-protokoll-novel-writing-incubator/01-dramatica-engine/`

## Dispatch prompt

```
Self-contained task. Do NOT clone any repo. Work language: English; never
translate German prose. Full autonomy — finish and open a PR.

STEP 1 — read the plugin model (one file only):
  kohaerenz-protokoll-novel-writing-incubator/PLUGIN-CONCEPTS.md

STEP 2 — read the Dramatica source material in THIS repo (read-only):
  skills/dramatica-theory/**          (the theory: 4 Classes / 16 Types /
                                       64 Variations / 64 Elements; throughlines)
  skills/dramatica-vocabulary/**      (active vocabulary; the 75 dynamic pairs)
  tools/dramatica-nav/**              (the lookup/navigation tool)
  maintenance/schemas/narrative-ontology/**  (novel.dual-storyform etc.)
  Measure, don't guess: count the real ontology entries and the kind breakdown
  (Class/Type/Variation/Element) and the dynamic-pair table size; cite paths.

STEP 3 — write ONLY into
  kohaerenz-protokoll-novel-writing-incubator/01-dramatica-engine/ :
    CONCEPTS.md   — the irreducible Dramatica primitives (storyform, throughline,
                    dynamic pair, the lookup operation), each mapped onto the
                    plugin's four concepts + wire contract. Which operations are
                    `transform` (pure lookups) vs `act` vs `effect`?
    COHERENCE.md  — coherence check: where this material fits the plugin model
                    cleanly, where it fights it, what would have to change. Is the
                    storyform a graph subgraph? Is the ontology vendored data?
    PROPOSAL.md   — how Dramatica should live as part of the novel capability:
                    proposed verbs (e.g. a dramatica_lookup transform), where the
                    ontology data lives, what is a graph node vs a rendered file.

Keep it concise and evidence-cited (paths + numbers). Then open a PR into
claude/dreamy-galileo-06exy. Touch nothing outside your slice dir.
```
