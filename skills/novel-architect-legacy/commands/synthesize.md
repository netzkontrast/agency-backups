# /synthesize — Canon-Update-Workflow

> **Status**: Stub. Voller Prompt-Template ausstehend.

## Zweck

Eine Entscheidung oder ein Research-Befund wird in den Canon eingearbeitet.

**Source-of-Truth**: NCP-Datei (strukturell) + canon-meta.md (nicht-strukturell). Diese MÜSSEN updaten.
**Optional**: Memory (auf User-Wunsch broadcasten), Drive-Reset-Doc (auf User-Wunsch spiegeln).

Memory ist NICHT Teil des Canon-Pfads. /synthesize updated Memory nur, wenn der User explizit „auch in Memory updaten" / „Memory broadcasten" sagt.

## Decision-Rule strukturell vs. nicht-strukturell

Vor dem /synthesize-Lauf entscheiden, wo der Entscheid hingehört:

**Geht in NCP** (via ncp-author):
- Player-Detail (name, role, visual, audio, bio, motivations, perspectives)
- Storyform-Slot-Verfeinerung (dynamic.summary, dynamic.storytelling)
- Storypoint-Encoding (Class/Type/Variation/Element-Slot mit appreciation + narrative_function)
- Storybeat-Position (signpost/progression/event scope, sequence, throughline)
- Moment-Definition (chapter mit setting/timing/imperatives/synopsis)
- Cross-narrative-Beat-Reference (Slot-16-Mechanik in moment.storybeats[])

**Geht in canon-meta.md**:
- DKT-Regel (Persistenzgleichung, Coherons/Erasonen-Definition)
- Alter-DKT-Korrelat oder Somatik (Tabelle)
- Riss-Mandat
- Computational-Class oder Style-Regel
- Prosa-Regel
- Mandate-Update
- Vortex-Übersicht (5 Beats als Liste — die spezifischen Beats werden aber als NCP-storybeats realisiert)
- Projekt-Meta (Drive-Pfade, Material-Status)

**Beides**: Wenn ein Entscheid beide Layer berührt, beide updaten in der korrekten Reihenfolge.

## Pipeline (Skill-Canon-First)

1. **Diff erstellen**: Was hat sich geändert? Quelle (User-Entscheid / Research-Output / OQ-Resolution) → Ziele (welche NCP-Pfade, welche canon-meta-Sektionen).
2. **NCP-Update** (falls strukturell): `ncp-author` konsultieren — JSON-Pfade gezielt mutieren, schema-konform halten. Validierung (upstream `validate-file.js`).
3. **canon-meta.md aktualisieren** (falls nicht-strukturell): str_replace gezielt in der relevanten Sektion.
4. **progress.md updaten**: Was ist passiert, was ist nächster Schritt.
5. **open-questions.md updaten** (falls OQ resolved): Eintrag als „erledigt" markieren mit Datum + Entscheid.
6. **(optional) Memory-Broadcast**: NUR wenn User explizit verlangt. memory-sync mit Skill→Memory-Richtung. Niemals umgekehrt.
7. **(optional) Drive-Sync**: Wenn Reset-Doc oder Outline-Revision betroffen → `drive-markdown-converter`.
8. **Checkpoint**: package + present (siehe significance-heuristics.md).

## Pre-Checks

- Es liegt eine konkrete, formulierte Änderung vor (nicht „lass uns mal überlegen")
- User-Bestätigung für die Änderung existiert (oder wird im Verlauf eingeholt)
- Decision-Rule strukturell vs. nicht-strukturell ist getroffen
- **Hierarchie-Check**: Falls User auf etwas in Memory verweist, das nicht im Skill steht — nachfragen, ob das Canon werden soll. Nicht stillschweigend „Memory says X, also ist X Canon" annehmen.

## Output

- **Skill-Canon (verpflichtend)**: NCP-Datei aktualisiert (falls strukturell), canon-meta.md aktualisiert (falls nicht-strukturell), progress.md aktualisiert, open-questions.md aktualisiert (falls OQ resolved)
- **Memory (optional, auf User-Wunsch)**: aktualisierte Slots via memory-sync
- **Drive (optional, auf User-Wunsch)**: aktualisierte Reset-Doc / Outline
- **Skill-Package**: neu gepackt + via `present_files` zurückgegeben

## Anti-Pattern

- NCP-Datei direkt editieren ohne ncp-author → Schema-Drift
- Strukturelle Daten in canon-meta.md schmuggeln → Single-Source-of-Truth-Verletzung
- canon-meta-Daten in NCP zwingen → Schema-Inkonsistenz
- **Memory automatisch syncen** → Hierarchie-Verletzung (Skill > Memory; Memory ist Notiz, nicht Maßstab)
- **Memory als Wahrheit annehmen** → Bei Diskrepanz Memory vs. Skill: Skill gewinnt. Memory ist möglicherweise stale.
- Mehrere unzusammenhängende Änderungen in einen /synthesize-Lauf packen → Diff wird unleserlich

## TODO

- Vollen Template-Wortlaut für strukturierten Diff-Display ausarbeiten
- NCP-Mutation-Konvention (welche Pfade-Änderungen sind atomar) dokumentieren
- Drive-Sync-Detail (welche Datei wo) ergänzen, wenn Folder-IDs verfügbar
- Memory-Broadcast-Trigger-Phrasen sammeln („auch in Memory", „Memory updaten", „broadcast", …)
