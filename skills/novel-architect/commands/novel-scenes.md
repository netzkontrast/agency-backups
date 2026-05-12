# /novel-scenes — Phase 5 Trigger

> **Phase:** 5 (Scene & Chapter Matrix)
> **/sc:-Analog:** `sc:workflow` + `sc:design`

## Zweck

Baut Scene-Matrix (40-Kapitel oder gewählte Struktur), persistiert Storybeats +
Moments in NCP. 3 Approval-Gates: Akt-Outline → Chapter-Outline → Final Scene Matrix.

## Trigger

- „/novel-scenes"
- „Akt-Struktur"
- „Kapitel-Plan"
- „Scene Matrix"
- „Storybeats, Moments"

## Pre-Conditions

- `architecture.yaml` approved (Phase 2 done)
- `character-architecture.yaml` (Phase 3 done)
- `world-bible.md` (Phase 4 sinnvoll done für betroffene Akte)

## Workflow

```
Phase 5.1   Load architecture + character + world             (silent)
Phase 5.2   Select structure template                          (askuser if [→ novel-architect-structure] offers multiple options)
Phase 5.3   Fill act-level structure                           (4 Akte, storypoints)
            ──── GATE 1 (act outline) ────                     (askuser)
Phase 5.4   Per act: fill chapter-level                        (storybeats per chapter)
            ──── GATE 2 (chapter outline) ────                 (askuser)
Phase 5.5   Per chapter: fill scene-level                      (moments per scene)
Phase 5.6   Write NCP storybeats[] + moments[]                 (delegate ncp-author)
Phase 5.7   Render scene-matrix.md                             (file-first)
            ──── GATE 3 (final scene matrix) ────              (askuser)
Phase 5.8   Persist + present_files
```

## Delegations

- `dramatica-theory` für Storyweaving-Pattern
- `dramatica-vocabulary` für Element-Encoding
- `ncp-author` für storybeats + moments
- [→ novel-architect-structure] for `<template>` selection (load on demand)

## Output

- `scene-matrix.md`
- NCP `narratives[].subtext.storybeats[]` + `narratives[].storytelling.moments[]`

## Hand-off

→ Phase 6 (`/novel-draft`) für per-Kapitel Drafting

## Detail

- `phases/phase5-scene-matrix.md`
- `assets/scene-matrix-template.md`
- [`novel-architect-structure/methods/`](../../novel-architect-structure/methods/) (lazy-loaded per `intent.methods_preference.structure`)
