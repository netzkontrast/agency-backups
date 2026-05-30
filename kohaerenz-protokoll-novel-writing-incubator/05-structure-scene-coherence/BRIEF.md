# Jules Brief — Slice 5: Structure, Scene & Coherence

- **alias:** `kp-incubator-structure-coherence`
- **repo:** `netzkontrast/agency-backups`
- **starting branch:** `claude/dreamy-galileo-06exy`
- **write only here:** `kohaerenz-protokoll-novel-writing-incubator/05-structure-scene-coherence/`

## Dispatch prompt

```
Self-contained task. Do NOT clone any repo. Work language: English; never
translate German prose. Full autonomy — finish and open a PR.

STEP 1 — read the plugin model (one file only):
  kohaerenz-protokoll-novel-writing-incubator/PLUGIN-CONCEPTS.md

STEP 2 — read the source material in THIS repo (read-only):
  skills/novel-architect-structure/** (40-chapter matrix, Hero's Journey, Save
                                       the Cat, Dramatica Quad)
  skills/novel-architect-scene/**     (scene matrix, Q1-Q5 scene-level bridge
                                       audit, drafting pre-checks)
  tasks/073-novel-architect-hard-rules-validation,
  tasks/074-novel-architect-anti-patterns,
  tasks/075-novel-architect-scene-level-bridge,
  tasks/084-novel-architect-storyform-integrity-linter,
  tasks/085-novel-architect-phase-flow-linters,
  tasks/086-novel-architect-canon-status-linter,
  tasks/087-novel-architect-render-architecture-wiring,
  tasks/090-novel-architect-render-pipeline
  decisions/0010-novel-architect-error-tier-linter-policy.md

STEP 3 — write ONLY into
  kohaerenz-protokoll-novel-writing-incubator/05-structure-scene-coherence/ :
    CONCEPTS.md   — plot-structure primitives, the scene matrix as a data
                    structure, and the render pipeline (state -> rendered
                    chapters/scenes), mapped onto the plugin's four concepts.
    COHERENCE.md  — the key coherence call: classify each coherence check as
                    DECIDABLE (a pure `transform`/linter with deterministic
                    pass/fail) vs JUDGEMENT (needs an LLM/human call), grounded in
                    what the source actually supports. Cite the source per item.
    PROPOSAL.md   — a coherence_check verb (decidable subset) + a pre_drafting
                    gate, the scene-matrix artefacts, and the render architecture
                    (graph/NCP state -> Markdown view; flag the graph-vs-disk
                    tension at the render step).

Concise, evidence-cited. Open a PR into claude/dreamy-galileo-06exy. Touch nothing
outside your slice dir.
```
