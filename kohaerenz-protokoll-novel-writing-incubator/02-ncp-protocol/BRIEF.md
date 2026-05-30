# Jules Brief — Slice 2: Narrative Context Protocol (NCP)

- **alias:** `kp-incubator-ncp`
- **repo:** `netzkontrast/agency-backups`
- **starting branch:** `claude/dreamy-galileo-06exy`
- **write only here:** `kohaerenz-protokoll-novel-writing-incubator/02-ncp-protocol/`

## Dispatch prompt

```
Self-contained task. Do NOT clone any repo. Work language: English; never
translate German prose. Full autonomy — finish and open a PR.

STEP 1 — read the plugin model (one file only):
  kohaerenz-protokoll-novel-writing-incubator/PLUGIN-CONCEPTS.md

STEP 2 — read the NCP source material in THIS repo (read-only):
  skills/ncp-author/**                (schema cheatsheet, canonical vocabulary:
                                       463 appreciations + 144 narrative_functions,
                                       validator, 10-stage workflow)
  research/ncp-novel-co-authoring-spec/**
  maintenance/schemas/narrative-ontology/**
  Measure, don't guess: find the NCP schema file; confirm its JSON-Schema draft,
  schema_version, and top-level shape; assert the real vocabulary counts. Cite paths.

STEP 3 — write ONLY into
  kohaerenz-protokoll-novel-writing-incubator/02-ncp-protocol/ :
    CONCEPTS.md   — NCP as a data model mapped onto the plugin: what the schema
                    constrains, the canonical vocabulary, validation rules, and
                    NCP's relationship to the Dramatica storyform.
    COHERENCE.md  — coherence check: is NCP state canonical in the graph or on
                    disk? Where does the "graph is the store, files are a view"
                    rule fit, and where does hand-authored JSON fight it?
    PROPOSAL.md   — an ncp_validate transform verb, where schema + vendored
                    vocabulary live, the per-work ncp.json skeleton, and what is a
                    graph node vs a rendered file.

Concise, evidence-cited. Open a PR into claude/dreamy-galileo-06exy. Touch nothing
outside your slice dir.
```
