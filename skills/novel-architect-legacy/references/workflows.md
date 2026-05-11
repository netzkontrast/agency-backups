# Workflows — Detail-Specs

10 Workflows, je mit Pre-Checks, Skill-Stack, NCP-Hooks, Output-Format, Exit-Bedingung. Wenn ein Workflow nicht mehr passt: hier umschreiben, dann packen.

> **NCP-Mutations-Regel**: Strukturelle Canon-Daten (Storyform-Slots, Players, Storypoints, Storybeats, Moments) werden NUR via `ncp-author` mutiert. Direkte Hand-Edits an `references/canon/kohaerenz-protokoll.ncp.json` sind verboten — würden Schema-Drift erzeugen.

---

## 1. bootstrap

**Trigger**: Implicit, sobald novel-architect getriggert wird und Workspace nicht existiert oder Session frisch ist.

**Pre-Checks**: keine — das IST der Pre-Check für alle anderen.

**Skill-Stack**: self.

**Schritte**: Siehe SKILL.md → Bootstrap-Protocol.

**Output**: Funktionierender Workspace unter `/home/claude/novel-architect-workspace/`. progress.md, NCP-Datei, canon-meta.md, open-questions.md gelesen.

**Exit**: Workspace ready, Skill-Pipeline geladen, User-Input kann beantwortet werden.

---

## 2. throughline-encoding

**Trigger**: „Encoding", „Throughline X encoden", „Phase 1", „Phase 2", „Phase 3", „Phase 4", „MC Throughline", „IC Throughline", „OS Throughline", „RS Throughline", „Storypoint übersetzen".

**Pre-Checks**:
- NCP-Datei geladen — `narratives[].subtext.perspectives[]` und `narratives[].subtext.dynamics[]` für die zu encodende Throughline existieren bereits (Skeleton hat sie)
- canon-meta.md geladen für Block-4-Anker-Constraints und Riss-Mandate
- open-questions.md → keine blockierenden OQs für diese Throughline?

**Skill-Stack**:
1. **dramatica-theory** — Storyform-Sektion + Encoding-Phase-Reference für die spezifische Class/Type/Variation/Element der Throughline
2. **dramatica-vocabulary** — Term-Präzision, Dynamic-Pair-Checks, Element-Auswahl
3. **ncp-author** — Storypoints in NCP schreiben (`narratives[].subtext.storypoints[]`), ggf. Player-Detail (`narratives[].subtext.players[]`)
4. **novel-architect** — Project-Constraints (Block-4-Anker abstrahieren, Riss-Mandate, Computational-Class-Style, Polyphonie-Verteilung)

**Wichtige Regel — Dual-Storyform-Integrität**:
Throughline-für-Throughline durch BEIDE narratives simultan, nicht erst A komplett dann B. Sonst geht die 5D-Interferenz verloren bevor sie entsteht. Konkret: Bei MC-Encoding entstehen Storypoints in `narrative_storyform_a.subtext.storypoints[]` UND `narrative_storyform_b.subtext.storypoints[]`.

**NCP-Hooks**:
- Pro Throughline 4 Storypoints (Class, Type/Concern, Variation/Issue, Element/Problem) als `storypoint`-Einträge mit `appreciation`-Enum-Wert (z. B. „Main Character Concern")
- `narrative_function` aus 144-Werte-Enum für jeden Storypoint (oder `custom_narrative_function` mit namespace)
- `perspectives[]` jedes Storypoints linkt auf den Perspective-Eintrag der Throughline (z. B. `perspective_a_mc`)
- `players[]` wird befüllt — Kael/AEGIS/Juna mit role + perspectives + motivations je narrative

**Begleit-Output (Markdown)** in `outputs/encoding/<storyform>-<throughline>.md`:
```markdown
# <Storyform> — <Throughline> Encoding

## Storypoints (Quelle: NCP)
- Class: X (Storypoint-ID: storypoint_a_mc_class)
- Type/Concern: Y
- Variation/Issue: Z
- Element/Problem: W

## Träger (Player-Link in NCP)
- Player: <player_kael / player_juna / ...>
- Role in this narrative: <Main Character / Influence Character / ...>

## Szenen-Keime (3-5 pro Storypoint)
### Storypoint X
- Bild: ...
- Raum: ...
- Klang: ...
(In NCP als `storypoint.illustration` und `storypoint.storytelling` verdichtet.)

## Konsistenz-Check gegen Block 4
- Anker abstrahiert? <ja/nein/notes>

## Offene Fragen
- ...
```

**Exit**: Eine Throughline ist in BEIDEN narratives encoded (NCP storypoints + relevante player-Felder gefüllt). Phase-Unit complete → Checkpoint-Trigger.

---

## 3. dynamics-encoding

**Trigger**: „Phase 5", „Dynamics encoden", „Driver-Pivot", „Limit", „Outcome", „Judgment".

**Pre-Checks**:
- Phase 1-4 abgeschlossen (alle 4 Throughlines in beiden narratives encoded)
- NCP-Datei: `dynamics[]` ist initial bereits gefüllt (Skeleton hat alle 8 Dynamics pro narrative entschieden) — dieser Workflow ist primär VERFEINERUNG der `summary` und `storytelling`-Felder

**Skill-Stack**: dramatica-theory → dramatica-vocabulary → ncp-author → novel-architect.

**NCP-Hooks**:
- Verfeinerung von `dynamic.summary` und `dynamic.storytelling` für alle 16 Dynamics (8 pro narrative)
- Besonderes Augenmerk: `dynamic_b_driver` mit `vector: action` und Klimax-Pivot zu de-facto-decision — die Pivot-Mechanik wird in `storytelling` präzisiert und im storyweaving-Workflow als Storybeat realisiert

**Output**: NCP-Datei mit verfeinerten dynamics. Optional Begleit-Markdown `outputs/encoding/dynamics.md`.

**Exit**: Driver, Limit, Outcome, Judgment für beide narratives sind nicht nur als Vector entschieden, sondern in Storytelling-Intent ausgearbeitet inkl. der Pivot-Mechanik.

---

## 4. storyweaving

**Trigger**: „Phase 6", „Storyweaving", „Kapitel-Plan", „39-Kapitel-Map", „Polyphonie-Verteilung", „Computational-Class-Progression KW1→KW4", „Reader-Leerstellen-Architektur".

**Pre-Checks**:
- Phase 1-5 abgeschlossen
- Slot 16 (Dual-POV-Architektur) entschieden — ohne diese Entscheidung blockiert Storyweaving in Praxis. Hypothese in `canon/README.md`: Moments mit cross-narrative Storybeat-Referenzen.
- Outline-Revision 2026-05-01 als Skelett geladen (canon-meta.md → Outline-Revision)

**Skill-Stack**: dramatica-theory → ncp-author (storybeats + moments) → novel-architect.

**NCP-Hooks**:
- `narratives[].subtext.storybeats[]` — pro narrative ~30-50 Beats (signpost / progression / event scopes), throughline-getaggt, sequence-nummeriert
- `narratives[].storytelling.moments[]` — 39 Moments (Kapitel) mit `act`, `order`, `setting`, `timing`, `imperatives`, `synopsis`
- Pro Moment: `storybeats[]` mit cross-narrative Referenzen (Hypothese — in praxi prüfen ob Validator das durchlässt; wenn nicht, alternative Architektur via custom-Felder)
- `audience_experiential_pov` pro Moment (third_person_omniscient für Polyphonie-Sektionen, first_person_central für ANP-POV-Sektionen)

**Output**: NCP-Datei mit storybeats + moments. Begleit-Markdown `outputs/weaving/chapter-map.md` als menschenlesbare Übersicht (Polyphonie-Verteilung über 13 Alters, Computational-Class-Progression, Reader-Leerstellen).

**Milestones / Checkpoints**: 10-Kapitel-Blöcke (Ch1-10, Ch11-20, Ch21-30, Ch31-39).

**Exit**: 39 Moments + zugehörige Storybeats in NCP, jeder Slot besetzt, Vortex-Beats (Ch35-36) als Platzhalter prepariert.

---

## 5. vortex-architecture

**Trigger**: „Phase 7", „Vortex", „Ch35-36 ausarbeiten", „Klimax operationalisieren", „Mnemosyne-Archipel", „5 Beats detaillieren", „Witness-Function-3-Layer im Klimax".

**Pre-Checks**:
- Phase 1-6 mindestens grob durchlaufen (storybeats für Ch35-36 als Platzhalter existieren)
- Driver-Pivot-Mechanik (Phase 5) klar
- canon-meta.md Vortex-Sektion geladen

**Skill-Stack**: dramatica-theory (Klimax-Patterns) → dramatica-vocabulary (Author's-Proof, Driver-Pivot-Begriffe) → ncp-author → novel-architect.

**NCP-Hooks**:
- 5 spezifische `storybeat`-Einträge in `narrative_storyform_b.subtext.storybeats[]` (event-scope) für die 5 Beats
- 1-2 `moment`-Einträge in `storytelling.moments[]` für Ch35-36 mit detailliertem `setting` (Mnemosyne-Archipel), `imperatives`, `audience_experiential_pov` 
- Driver-Pivot-Beat: `storybeat.narrative_function` reflektiert den Übergang von action zu decision

**Die 5 Beats** (canonical, aus canon-meta.md):
1. Konvergenz Mnemosyne-Archipel → AEGIS-Erasure
2. Pivot Kael → A-Logic + ANP/EP-Drop
3. Stille = lebende Dialetheia
4. Heat-Spike Landauer → ∞
5. Rotation → Algo.Melancholy

**Output**: NCP-Update + Begleit-Markdown `outputs/vortex/beat-1.md` bis `beat-5.md` plus `outputs/vortex/mnemosyne-archipel-setting.md`.

**Exit**: Alle 5 Beats szenisch operationalisiert in NCP. Setting konkret. 3-Layer-Witness-Function (narratologisch / phänomenologisch / operational) im Klimax verortet.

---

## 6. open-questions-resolution

**Trigger**: „OQ", „Slot 16 entscheiden", „offene Frage entscheiden", „Phase 8", „Appendix C abarbeiten".

**Pre-Checks**: open-questions.md geladen, betroffene OQ identifiziert.

**Skill-Stack**: novel-architect (Kontext laden) → dramatica-theory (strukturelle Implikationen prüfen) → ncp-author (falls OQ strukturell — z. B. Slot 16) → canon-meta-Edit (falls nicht-strukturell). Memory-Broadcast nur auf User-Wunsch.

**NCP-Hooks (falls strukturell)**:
- OQ-A (Post-Vortex-AEGIS-Status): potenziell ein neuer Akt-3-Storybeat oder ein verändertes `dynamic_b_outcome.storytelling`
- OQ-B (Moonshine-Boundary): Storypoints in `narrative_storyform_a.subtext.storypoints[]` (RS-Throughline)
- OQ-C (Juna-Erscheinungs-Modus-Anker): neue Custom-Felder in `player_juna.visual` oder zusätzliche `storypoint`-Einträge mit den 2-3 weiteren Modi
- OQ-D (Genesis 4. Beat?): potenziell ein neuer Storybeat in beiden narratives' Akt-1-Bereich
- Slot 16 (Dual-POV-Architektur): kann substantielle NCP-Schema-Erweiterung erfordern (custom-Felder oder custom-Namespace)

**Output**: `outputs/oq-resolved/<oq-id>.md` mit Entscheid, Begründung, betroffenen NCP-Pfaden, betroffenen canon-meta-Sektionen, Folge-Aktionen.

**Resolution-Methode**: Phönix-Mode (Steelman vs. Inversion vs. First-Principles). Truth-Rotation = Canon. Bei Multi-Variable-Entscheidungen: `ask_user_input_v0` mit 2-4 Optionen.

**Nach Resolution**:
- open-questions.md updaten (durchstreichen + Entscheid + Datum)
- Falls Memory-Broadcast vom User gewünscht: memory-sync run (sonst überspringen)
- Falls NCP betroffen: ncp-author run
- Falls canon-meta.md betroffen: dort updaten
- Checkpoint-Trigger: package + present

**Exit**: OQ entschieden, dokumentiert, NCP + canon-meta synchronisiert. Memory ggf. via memory-sync gebroadcastet, falls vom User gewünscht.

---

## 7. chapter-drafting

**Trigger**: „/draft", „Kapitel X entwerfen", „Prosa schreiben für Ch X", „Entwurf Kapitel X".

**Pre-Checks** (HARD):
- Phase 1-6 abgeschlossen für die im Kapitel relevanten Storypoints und Moments
- NCP-Datei: `narrative_storyform_a.storytelling.moments[X]` (oder narrative_b, je nach Slot-16-Architektur) existiert mit `synopsis`, `setting`, `timing`, `imperatives`, `storybeats[]`
- Per-Kapitel-Beat-Pattern in NCP festgelegt
- Polyphonie-Verteilung für Ch X klar (welche Alters POV haben — über `audience_experiential_pov` und player-Referenzen ableitbar)
- Slot 16 (Dual-POV-Architektur) entschieden

Wenn ein Pre-Check failt: STOP, drafting blockiert. Erst Pre-Check fixen.

**Skill-Stack**:
1. **novel-architect** — NCP + canon-meta laden, Pre-Checks verifizieren, Constraints für die Szenen vorbereiten
2. **dramatica-vocabulary** — Term-Präzision während Prosa-Entscheidungen (Driver, Limit, Element-Pairs in Szenen-Spannung)
3. **docx** — Export als .docx ins `outputs/drafts/`

**Wichtig**: NCP hält nur strukturelle Intent. Prosa lebt **außerhalb** von NCP, in `outputs/drafts/ch-XX.docx`. Cross-Reference via `moment.id` für Traceability.

**Prosa-Regeln** (siehe canon-meta.md → Prosa-Regeln Sektion): Lesersteuerung, Max 1 Konzept/Szene, Polyphonie nach Akt, Style 1/2/3 nach Kontext, erste 50 Seiten KEINE DKT-Terminologie, Ted-Chiang-Maßstab, somatischer Filter.

**Output**: `outputs/drafts/ch-XX.docx` mit Header `<!-- moment.id: moment_ch_XX -->` für NCP-Traceability.

**Exit**: Kapitel-Entwurf existiert, ist konsistent zu NCP-Moment + Storybeats, hält die Prosa-Regeln.

---

## 8. research-ingestion

**Trigger**: „/analyze", „Gemini-Output verarbeiten", „Recherche zu X für Roman", „Deep Research Prompt für X".

**Skill-Stack**:
1. **research-prompt-optimizer** — Gemini-Deep-Research-Prompt bauen
2. **(extern)** — User führt Prompt in Gemini Deep Research aus, kopiert Output
3. **novel-architect** — Output gegen Canon prüfen (NCP + canon-meta), Widerspruchs-Report
4. **doc-coauthoring** — strukturierter Canon-Doc-Eintrag

**Output**: `outputs/research/<topic>.md` mit:
- Original-Prompt
- Gemini-Output (referenziert oder summarisiert)
- Widerspruchs-Report gegen NCP + canon-meta (Skill-Canon)
- Canon-Implikationen (welche Slots / NCP-Pfade / canon-meta-Sektionen müssen updaten?)

**Exit**: Research-Material strukturiert für Canon-Konsumption verfügbar. /synthesize-Workflow falls Implikationen.

---

## 9. canon-update

**Trigger**: „/synthesize", „Kanon ändern", „das ist jetzt kanonisch", „entschieden", „das gilt jetzt", „korrigiere".

**Skill-Stack**:
1. **ncp-author** (falls strukturell) UND/ODER canon-meta.md-Edit (falls nicht-strukturell)
2. **novel-architect** — Konsistenz-Check, progress.md + open-questions.md updaten
3. **(optional) memory-sync** — NUR wenn User explizit Memory-Broadcast verlangt („auch in Memory updaten" o.ä.). Skill→Memory broadcast, niemals Memory→Skill.
4. **(optional) drive-markdown-converter** — Drive-Sync (Reset-Doc)

**Decision-Rule strukturell vs. nicht-strukturell**:
- Strukturell (geht in NCP): Player-Detail, Storyform-Slot-Verfeinerung, Storypoint-Encoding, Storybeat-Position, Moment-Definition
- Nicht-strukturell (geht in canon-meta.md): DKT-Regel, Prosa-Regel, Mandate, Alter-Somatik (Tabelle bleibt Markdown), Projekt-Meta (Drive-Pfade etc.)
- Beides: Wenn ein Entscheid beide Layer berührt, beide updaten

**Hierarchie-Regel**:
Skill-Files (NCP + canon-meta) sind Source-of-Truth. Memory ist nicht Teil des Canon-Pfads. Wenn User sich auf Memory-Inhalt beruft, der hier nicht steht: nachfragen, ob das in den Canon übernommen werden soll. Nicht stillschweigend annehmen, dass Memory korrekt ist.

**Output**:
- NCP-Datei und/oder `references/canon-meta.md` aktualisiert
- progress.md + open-questions.md ggf. aktualisiert
- Optional: Memory-Slots (Slot #1-#13) auf User-Wunsch broadcastet
- Optional: Reset-Doc auf Drive aktualisiert

**Exit**: NCP + canon-meta sind konsistent (Source-of-Truth). Memory + Drive optional gespiegelt, falls vom User verlangt.

---

## 10. archive-material

**Trigger**: „alte PDFs konvertieren", „Material in Markdown bringen", „Archiv migrieren".

**Skill-Stack**: pdf-to-markdown → drive-markdown-converter (optional).

**Output**: Markdown-Dateien in `archive/` oder im Drive-Ordner.

**Status-Note**: Per User-Setzung (Reset 2026-04-30) archiviert, NICHT canonisch. Kann als Steinbruch (Quarry) für Recherche genutzt werden, ist aber nicht Source-of-Truth.

**Exit**: PDFs konvertiert, Markdown verfügbar, Status als „archiviert / nicht-bindend" klar markiert.

---

## Workflow-Pivot-Regel

Wenn der User innerhalb einer Session Workflow wechselt:
1. Aktuellen Workflow notieren (was war der letzte Stand)
2. progress.md updaten — beide Workflows benannt
3. Falls strukturelle Mutation am laufen war: NCP-State final committed via ncp-author
4. Checkpoint triggern (package + present)
5. Neuen Workflow starten

Das verhindert verlorenen Stand bei Workflow-Sprüngen.
