---
name: novel-architect-character
description: >-
  Character-Architektur Sub-Skill von novel-architect. Wendet TSDP/IFS, Big Five
  (OCEAN), Enneagramm und Jung-Archetypen auf Phase-3 Player-Slots an
  (NCP `players[]`, `players[].motivations[]`, `players[].perspectives[]`).
  Delegiert Dramatica-Vokabular-Lookups an dramatica-theory + dramatica-vocabulary.
  Trigger: /novel-characters, "Character-Architektur", "Charakter-Modell",
  TSDP, IFS, Big Five, OCEAN, Enneagramm, Jung Archetypen, Player-Slot.
  Implicit invocation aus novel-architect Phase 3. NICHT bei generischer
  Charakter-Brainstorming ohne Roman-Scope.
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
    novel-architect-character, character architecture, charakter-architektur,
    player-slot, tsdp, ifs, big-five, ocean, enneagramm, jung archetypes,
    psycho-model, /novel-characters
  delegates_to: >-
    novel-architect (parent orchestrator), dramatica-theory, dramatica-vocabulary,
    ncp-author
---

# novel-architect-character v1.1.0

Sub-Skill von [`novel-architect`](../novel-architect/). Wird in Phase 3
(Character Architecture) vom Orchestrator delegiert. Eigene Methoden-Bibliothek
für psychologische Modelle; eigene Trigger; eigene SKILL.md damit der Skill-
Loader ihn unabhängig laden kann.

## Scope

| Phase | Verantwortung |
|-------|---------------|
| Phase 3 — Character Architecture | Per-Charakter-Slot-Befüllung; Psycho-Modell-Auswahl; Relationship-Mapping |

## Verfügbare Methoden

| File | Modell | Wann verwenden |
|------|--------|----------------|
| [`methods/tsdp-ifs.md`](./methods/tsdp-ifs.md) | Tertiäre Strukturelle Dissoziation + IFS | Fragmentierte Identität, Trauma-Roman |
| [`methods/big-five.md`](./methods/big-five.md) | OCEAN | Realistische Hauptfiguren, Drama |
| [`methods/enneagramm.md`](./methods/enneagramm.md) | 9 Typen + Wings + Integration/Disintegration | Klar motivierte Charaktere, Ensembles |
| [`methods/jung-archetypes.md`](./methods/jung-archetypes.md) | Archetypen + Individuation | Mythische, Coming-of-Age, Fantasy |

Mehrere Modelle pro Charakter möglich (`psycho_config.primary` + `psycho_config.secondary`).

## Delegation Contract

Dieser Sub-Skill schreibt **nur** in:

- NCP `narratives[].subtext.players[]` (über `ncp-author`)
- NCP `players[].motivations[]`, `players[].perspectives[]` (über `ncp-author`)
- Workspace-File `character-architecture.yaml` (über `render/io_helpers.py` im Orchestrator)

Dramatica-Slot-Resolution MUSS vor jedem NCP-Write über `nav.py` laufen
(AGENTS.md Rule NO.2). Direct NCP-Hand-Edits sind verboten.

## Constraints

- **Skill ist projekt-agnostisch:** lädt nichts aus `/home/claude/novel-projects/<slug>/` selbst — der Orchestrator liefert die Workspace-Pfade.
- **Methoden on demand:** kein eager-load aller 4 Modelle bei Bootstrap.
- **Delegation only:** Phase-3-Logik selbst lebt in [`../novel-architect/phases/phase3-character-architecture.md`](../novel-architect/phases/phase3-character-architecture.md); dieser Sub-Skill enthält *nur* die Methoden-Bibliothek + Slot-Befüllungsregeln.

## Integration mit novel-architect

| Skill-Call | Aktion |
|---|---|
| `/novel-characters` (im Orchestrator) | Orchestrator routet zu diesem Sub-Skill |
| Direkter Trigger ("Big Five für Protagonist anwenden") | Skill-Loader lädt diesen Sub-Skill ohne Orchestrator-Umweg |

## Closing Note

Dieser Sub-Skill ist ein **Methoden-Lieferant**, nicht ein eigenständiger Roman-
Orchestrator. Roman-Projekt-Setup, Phase-Routing, NCP-State leben im Orchestrator
[`novel-architect`](../novel-architect/). Wenn diese Bibliothek wächst (5+
Modelle), wird sie zur eigenen Skill-Familie; bis dahin: 4 Modelle + delegation.
