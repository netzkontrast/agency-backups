# Methods Library

Wiederverwendbare Methoden-Module für Roman-Entwicklung. Selektierbar pro
Projekt via `intent.methods_preference.*`.

## Struktur

| Subdir | Funktion | Phase |
|--------|----------|-------|
| `character/` | Psychologische Modelle für Charakter-Architektur | Phase 3 |
| `structure/` | Plot-Strukturen (40-Kapitel, Hero's Journey, etc.) | Phase 2, 5 |
| `storyform/` | Dramatica Storyform Worksheet-Loop (8-Schritte) | Phase 2 |
| `conflict/` | Konflikt-Engines (Philosophie, Wissenschaft, Dual-Storyform) | Phase 2 |
| `research/` | Recherche-Strategien (Domain-Mapping, Deep-Research-Briefs) | Phase 4 |

## Progressive Disclosure

Diese Files werden NUR geladen, wenn:
- `intent.methods_preference.<category>` ein File explizit referenziert
- Die entsprechende Phase aktiv ist
- Ein Edge-Case auftritt, der das Methoden-Detail benötigt

Niemals alle Methoden bei Bootstrap eager laden — Token-Budget.

## Erweiterbarkeit

Neue Methoden hinzufügen:
1. File in entsprechendem Subdir anlegen (z.B. `methods/character/mbti.md`)
2. Im subdir-`readme.md` referenzieren
3. Schema-Slot für `psycho_config` / `structure_config` definieren
4. In Phase 3/5-Detail-File einfügen (load-when-clause)
5. Optional: `intent.methods_preference.<category>` Enum erweitern
