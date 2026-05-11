---
name: novel-architect-scene
description: >-
  Scene-Level Sub-Skill von novel-architect. Übernimmt Per-Scene/Per-Moment-
  Detail für Phase 5 (Scene Matrix Detailauflösung) und Phase 6 (Drafting
  Pre-Checks). Stellt das Q1–Q5 Scene-Level-Bridge-Audit bereit (Dramatica-
  Storyform → Szenenarbeit). Trigger: "Scene-Detail", "Moment Audit",
  "Scene-Level-Bridge", Q1-Q5, /novel-draft Pre-Check. Delegiert Storyform-
  Reasoning an dramatica-theory + dramatica-vocabulary.
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
    novel-architect-scene, scene-level bridge, scene audit, moment audit,
    Q1-Q5 audit, scene matrix detail, /novel-draft pre-check
  delegates_to: >-
    novel-architect (parent orchestrator), dramatica-theory, dramatica-vocabulary,
    ncp-author
---

# novel-architect-scene v1.1.0

Sub-Skill von [`novel-architect`](../novel-architect/). Übernimmt das
*Scene-Level-Detail* zwischen abstrakter Storyform-Struktur (Phase 2/5
Akt-Ebene) und konkreter Prosa-Generierung (Phase 6 Drafting). Der
Sub-Skill ist v1.1.0 noch lean und wird in Task 075 mit dem vollen
Q1–Q5-Scene-Level-Bridge-Audit befüllt.

## Scope

| Phase | Verantwortung |
|-------|---------------|
| Phase 5 — Scene Matrix (Detail) | Per-Scene-Slot-Befüllung; `moment.id` Generation; storypoint-zu-moment Mapping |
| Phase 6 — Drafting (Pre-Check) | Q1–Q5 Audit pro Moment, bevor Prosa-Generierung startet |

## Verfügbare Methoden

| File | Methode | Status |
|------|---------|--------|
| `methods/scene-level-bridge.md` | Q1-Q5 Per-Moment Audit (dominant throughline, signpost timing, conflict flavor, character arc, thematic beat) | **TBD (Task 075)** |

Pro v1.1.0 ist dieser Sub-Skill ein **Stub** mit verbindlichem Delegation-
Contract; die Methoden-Bibliothek wird durch [Task 075](../../tasks/075-novel-architect-scene-level-bridge/task.md)
populiert.

## Delegation Contract

Dieser Sub-Skill schreibt:

- NCP `narratives[].storytelling.moments[]` (Phase 5; über `ncp-author`)
- Workspace-File `scene-matrix.md` Moment-Sektionen (über `render_scene_matrix.py` im Orchestrator)
- Workspace-File `drafts/ch-XX-precheck.md` (Phase 6 Pre-Check Output)

Q1–Q5 Audit-Resolution MUSS gegen `dramatica-theory` reasoniert werden — siehe `skills/dramatica-theory/references/12-scene-level-bridge.md`.

## Constraints

- **Stub-Status:** v1.1.0 ist dieser Sub-Skill ein Stub. Aktive Phase-5/6-Arbeit läuft (bis Task 075 schließt) direkt im Orchestrator. Trigger werden bereits hier abgefangen, damit der Skill-Loader den Sub-Skill kennt.
- **Skill ist projekt-agnostisch:** kein Genre/Plot-Default.
- **NCP-Schutz:** `moments[]` werden nur via `ncp-author` geschrieben, nie direkt.

## Integration mit novel-architect

| Skill-Call | Aktion |
|---|---|
| `/novel-scenes` (Phase 5 Detail) | Orchestrator routet Per-Moment-Arbeit zu diesem Sub-Skill |
| `/novel-draft` (Phase 6 Pre-Check) | Orchestrator triggert das Q1-Q5 Audit hier |

## Closing Note

Dieser Sub-Skill ist die **Brücke zwischen Storyform und Prosa**. Er entscheidet
nicht *was* in einer Szene passiert (das tut die Storyform / der Author), sondern
*ob* die geplante Szene mit der Storyform konsistent ist und welche Slots noch
fehlen.
