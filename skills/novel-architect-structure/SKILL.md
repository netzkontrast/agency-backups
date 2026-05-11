---
name: novel-architect-structure
description: >-
  Struktur-Architektur Sub-Skill von novel-architect. Stellt Plot-Strukturen
  bereit (40-Kapitel-Matrix, Hero's Journey, Save the Cat, Dramatica Quad) und
  unterstützt Phase 2 (Narrative Architecture) + Phase 5 (Scene Matrix) bei
  Storyform-Decisions, Throughline-Assignment, Akt-Hierarchie. Delegiert
  Dramatica-Slot-Resolution an dramatica-theory + dramatica-vocabulary.
  Trigger: /novel-design, /novel-scenes, "Storyform", "Throughline",
  "Hero's Journey", "Save the Cat", "40-Kapitel-Matrix", "Dramatica Quad".
  NICHT bei generischer Plot-Brainstorming ohne Roman-Scope.
metadata:
  category: creative-writing
  parent: novel-architect
  version: "1.1.0"
  status: active
  date_added: "2026-05-11"
  date_updated: "2026-05-11"
  state_management: "ncp"
  ncp_schema_version: "1.3.0"
  triggers: >-
    novel-architect-structure, storyform, throughline, narrative architecture,
    plot structure, hero's journey, save the cat, 40-kapitel-matrix,
    dramatica-quad, /novel-design, /novel-scenes
  delegates_to: >-
    novel-architect (parent orchestrator), dramatica-theory, dramatica-vocabulary,
    ncp-author
---

# novel-architect-structure v1.1.0

Sub-Skill von [`novel-architect`](../novel-architect/). Wird in Phase 2
(Narrative Architecture) und Phase 5 (Scene Matrix) vom Orchestrator
delegiert. Stellt Strukturschablonen + Storyform-Decision-Support bereit.

## Scope

| Phase | Verantwortung |
|-------|---------------|
| Phase 2 — Narrative Architecture | Storyform-Wahl (single/dual), Throughline-Assignment, Class-Assignment, Dynamics-Selection |
| Phase 5 — Scene Matrix | Akt-Hierarchie, Kapitel-Plan-Strukturschablone (40-Chapter, Hero's-Journey, Save-the-Cat, Dramatica-Quad) |

## Verfügbare Methoden

| File | Struktur | Wann verwenden |
|------|----------|----------------|
| [`methods/40-chapter-matrix.md`](./methods/40-chapter-matrix.md) | 4×10-Kapitel-Grid | Long-form Roman, methodische Komposition |
| [`methods/heroes-journey.md`](./methods/heroes-journey.md) | Campbell / Vogler 12-Stage Monomyth | Coming-of-Age, mythische Storyforms |
| [`methods/save-the-cat.md`](./methods/save-the-cat.md) | Blake Snyder 15-Beat | Genre-Roman, Thriller, Beat-Driven |
| [`methods/dramatica-quad.md`](./methods/dramatica-quad.md) | Fractal 4-Element Recursion | Dramatica-natives Storyforming |

Strukturen sind kombinierbar (z.B. `40-chapter-matrix` als Top-Layer + `dramatica-quad` als Akt-Layer).

## Delegation Contract

Dieser Sub-Skill schreibt **nur** in:

- NCP `narratives[].subtext.perspectives[]` und `narratives[].subtext.dynamics[]` (Phase 2; über `ncp-author`)
- Workspace-File `architecture.yaml` (Phase 2; über `render/io_helpers.py` im Orchestrator)
- Workspace-File `scene-matrix.md` (Phase 5; via `render_scene_matrix.py` im Orchestrator)

Storyform-Wahl + Throughline-Assignment MÜSSEN über `dramatica-theory` reasoniert werden (AGENTS.md NO.1, NO.2). Direct Element-Coining ist verboten.

## Constraints

- **Skill ist projekt-agnostisch:** liefert *Schablonen*, nicht projekt-spezifische Plots.
- **Methoden on demand:** kein eager-load aller 4 Strukturen bei Bootstrap.
- **Hand-off via YAML:** Phase 2 schreibt `architecture.yaml`; Phase 5 liest es. Kein impliziter In-Memory-State.
- **Dual-Storyform-Integrität:** wenn `dramatica_storyform_count: dual`, dann werden Throughlines/Storybeats Throughline-für-Throughline durch BEIDE Narratives simultan geschrieben — niemals A komplett vor B.

## Integration mit novel-architect

| Skill-Call | Aktion |
|---|---|
| `/novel-design` (im Orchestrator) | Orchestrator routet Phase 2 zu diesem Sub-Skill |
| `/novel-scenes` (im Orchestrator) | Orchestrator routet Phase 5 zu diesem Sub-Skill |
| Direct Trigger ("40-Kapitel-Matrix für SF-Roman") | Skill-Loader lädt diesen Sub-Skill direkt |

## Closing Note

Dieser Sub-Skill ist die **Strukturschablonen-Bibliothek**, nicht der Storyform-
Generator. Storyform-Reasoning, Class-Assignment, Throughline-Logik leben in
`dramatica-theory`; dieser Sub-Skill stellt die *Hierarchie-Templates* bereit,
in die die Throughlines eingehängt werden.
