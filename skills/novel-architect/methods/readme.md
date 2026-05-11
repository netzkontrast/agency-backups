# Methods Library — Orchestrator-Local Methods

Wiederverwendbare Methoden-Module, die im Orchestrator-Skill verbleiben.
Die meisten domain-spezifischen Methoden sind ab v1.1.0 in **Sub-Skills**
ausgelagert (Task 071 Sub-Module Refactor):

| Domain | Sub-Skill | Methods Path |
|--------|-----------|--------------|
| Character | [`novel-architect-character`](../../novel-architect-character/) | `novel-architect-character/methods/` |
| Structure | [`novel-architect-structure`](../../novel-architect-structure/) | `novel-architect-structure/methods/` |
| World / Research | [`novel-architect-world`](../../novel-architect-world/) | `novel-architect-world/methods/` |
| Scene-level | [`novel-architect-scene`](../../novel-architect-scene/) | `novel-architect-scene/methods/` (Task 075) |

Cross-cutting konflikt-Methoden, die mehrere Domains überspannen
(Philosophie als Engine, Wissenschaft als Engine, Dual-Storyform), bleiben
im Orchestrator unter `methods/conflict/`. Sie sind keinem einzelnen
Sub-Skill eindeutig zuzuordnen — die Konflikt-Engine prägt sowohl
Throughline-Architektur (Phase 2) als auch Charakter-Motivationen
(Phase 3).

## Struktur

| Subdir | Funktion | Phase |
|--------|----------|-------|
| `conflict/` | Konflikt-Engines (Philosophie, Wissenschaft, Dual-Storyform) | Phase 2, 3 |

## Progressive Disclosure

Diese Files werden NUR geladen, wenn:
- `intent.methods_preference.conflict` ein File explizit referenziert
- Die entsprechende Phase aktiv ist
- Ein Edge-Case auftritt, der das Methoden-Detail benötigt

Niemals alle Methoden bei Bootstrap eager laden — Token-Budget.

## Erweiterbarkeit

Neue cross-cutting Konflikt-Methode hinzufügen:
1. File in `methods/conflict/` anlegen (z.B. `methods/conflict/mythic-engine.md`)
2. Hier in der Tabelle eintragen
3. Schema-Slot für `conflict_config` definieren
4. In Phase-Detail-File die load-when-clause hinzufügen
5. Optional: `intent.methods_preference.conflict` Enum erweitern

Domain-spezifische Methoden (Character, Structure, World, Scene) NICHT mehr
hier — direkt im jeweiligen Sub-Skill anlegen.
