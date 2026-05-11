# /novel-design — Phase 2 Trigger

> **Phase:** 2 (Narrative Architecture)
> **/sc:-Analog:** `sc:design` für Storyform-Architektur

## Zweck

Baut Dramatica-Storyform-Architektur. 3 Approval-Gates: Storyform-Shape →
Throughlines+Classes+Dynamics → Final Architecture. Persistiert in NCP via
`ncp-author`.

## Trigger

- „/novel-design"
- „Storyform definieren"
- „Throughlines, Dynamics"
- „Narrative Architecture"

## Pre-Conditions

- `intent.yaml` exists und approved (Phase 1 done)

## Workflow

```
Phase 2.1   Load intent.yaml + select methods                  (silent)
Phase 2.2   Storyform Count (single/dual)
            ──── GATE 1 ────                                    (askuser approve/edit)
Phase 2.3   Throughline Assignment                              (auto + dramatica-theory)
Phase 2.4   Class Assignment                                    (auto + dramatica-theory)
Phase 2.5   Dynamics Selection                                  (delegate dramatica-vocabulary)
            ──── GATE 2 ────                                    (askuser)
Phase 2.6   NCP Skeleton Write                                  (delegate ncp-author)
Phase 2.7   Render Architecture View                            (file-first)
            ──── GATE 3 ────                                    (askuser)
Phase 2.8   Write architecture.yaml + NCP Skeleton              (file + present_files)
```

## Delegations

- `dramatica-theory` für Storyform-Reasoning
- `dramatica-vocabulary` für Dynamic-Pair-Validation
- `ncp-author` für NCP-Skeleton-Erstellung
- `tools/dramatica-nav/nav.py` für Ontology-Lookups (AGENTS.md NO.2)

## Output

- `architecture.yaml` (approved)
- `canon/<slug>.ncp.json` (NCP-Skeleton, validation passed)

## Hand-off

→ Phase 3 (`/novel-characters`) für Character Architecture

## Detail

- `phases/phase2-narrative-architecture.md`
- `assets/architecture-template.yaml`
- `references/ncp-integration-contract.md`
