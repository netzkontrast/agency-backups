# Skill-Improvement TODO

Beobachtungen über die Skill-Pipeline hinweg, die hier nicht akut gefixt werden, aber dokumentiert gehören. Liste wächst über Zeit.

Stand: 2026-05-03 (novel-architect v0.3.0 — NCP als State-Layer)

---

## novel-architect (this skill)

### Done in v0.2.0 → v0.3.0 (2026-05-03)
- [x] Bootstrap-Protocol eingebaut
- [x] Routing-Matrix für 10 Workflows
- [x] Significance-Heuristik kodifiziert
- [x] Reference-Files gebaut
- [x] commands/-Stubs angelegt
- [x] Veraltete BERICHT.md + todo.md entfernt
- [x] OQ-01/02/03 als „durch Reset 2026-04-30 erledigt" markiert
- [x] **NCP als State-Management-Layer eingeführt** (v0.3.0)
- [x] **canon-state.md aufgelöst** in canon/kohaerenz-protokoll.ncp.json (strukturell) + canon-meta.md (nicht-strukturell)
- [x] **Skeleton-NCP-Datei erstellt** mit Storyform A + B + alle 16 Dynamics gefüllt
- [x] Workflows auf NCP-Mutation via ncp-author umgestellt
- [x] Constraint hinzugefügt: NCP-Mutation NUR via ncp-author

### Open
- [ ] **commands/-Templates ausbauen**: Aktuell Stubs. Voller `analyze.md`, `interview.md`, `synthesize.md` (jetzt mit NCP-Sub-Step), `draft.md` (jetzt mit NCP-Pre-Checks)
- [ ] **Drive-Folder-IDs einfügen**: canon-meta.md verweist auf `netzkontrast/Dual-Kernel`, aber konkrete Folder-IDs für Reset-Doc, Outline-Revision, Session-History fehlen
- [ ] **Slot 16 (Dual-POV) operationalisieren**: Sobald entschieden, in workflows.md → storyweaving + chapter-drafting einarbeiten. NCP-Hypothese (cross-narrative Storybeat-Refs in Moments) gegen Schema-Validator prüfen
- [ ] **NCP-Skeleton füllen**: Im Phasenwerk werden players, storypoints, storybeats, moments gefüllt. Initial leer.
- [ ] **Versionierungs-Konvention**: v0.3.0 jetzt — Vorschlag v1.0 = Phase 1-4 (alle Throughlines encoded in NCP), v2.0 = Storyweaving (alle 39 Moments), v3.0 = Vortex operationalisiert, v4.0 = ein Kapitel-Draft fertig

---

## ncp-author (KRITISCH — jetzt State-Layer-Owner)

Der Skill ist seit v0.3.0 von „optional persistence" zu **load-bearing infrastructure** für novel-architect geworden. Risiken müssen aktiv gemanagt werden.

- [ ] **Reife-Watch**: WIP 0.1.0-draft. In jeder Roman-Session prüfen ob Skill-Version voranschreitet.
- [ ] **Validator-Script**: TODO T-2 in ncp-author. Bis dahin: upstream `validate-file.js` als Workaround. Validator IST der primäre Bedarf — ohne Validierung ist NCP-Schema-Drift unentdeckbar.
- [ ] **Multi-Narrative-Use-Case-Beispiele**: ncp-author dokumentiert nicht das Dual-Storyform-Pattern. Eigene Reference-Sektion „Multiple narratives in one story" mit Empire/Barbie-Pattern wäre wertvoll, da Kohärenz-Protokoll genau dieser Use-Case ist.
- [ ] **Cross-Narrative Storybeat-References**: Ist das Schema-konform? `moment.storybeats[].storybeat_id` ist nur ein String — aber prüft der Validator narrative-internal-Konsistenz? Slot-16-Hypothese hängt daran.
- [ ] **KTAD-Validierung-Lücke**: NCP encodet keine Knowledge/Thought/Ability/Desire-Kohärenz. Bei Element-Auswahl in Phase 1-4 muss `dramatica-vocabulary` parallel validieren — Workflow-Hook fehlt aktuell.
- [ ] **Heavy-required-fields-Mitigation**: `players[]` braucht visual, audio, bio, motivations[] — auch im Skeleton. Aktuell als leeres Array. Bei nächster ncp-author-Iteration: Konvention für „TBD"-Werte oder Status-Feld dokumentieren.

---

## memory-sync

- [ ] **Outward-Only-Semantik kodifizieren**: memory-sync ist Skill→Memory Broadcaster, niemals Memory→Skill. Skill-Files (NCP + canon-meta) sind Source-of-Truth, Memory ist abgeleiteter Snapshot. Aktuell suggeriert die memory-sync-Beschreibung zweiseitige Synchronisation — das ist falsch.
- [ ] **Auf-Anfrage-Trigger**: memory-sync triggert nur, wenn User explizit „Memory updaten" / „auch in Memory broadcasten" sagt. Nicht automatisch bei Canon-Updates, nicht bei Session-End, nicht bei Checkpoints.
- [ ] **Drift-Awareness**: memory-sync sollte beim Lesen prüfen, ob Memory älter ist als der Skill-Stand (via Timestamp in canon-meta.md / NCP). Falls ja: Hinweis ausgeben, aber Memory NICHT als Wahrheit behandeln.
- [ ] **Drei-State-Modell dokumentieren**: novel-architect = Workspace-State (Source-of-Truth), ncp-author = strukturelle Persistenz, memory-sync = Memory-Broadcast (subordiniert). Skill-Files dominieren.

---

## dramatica-vocabulary

- [ ] **Konkrete Handoff-Signature**: Vorschlag definiertes Schema `{project: "kohärenz-protokoll", phase: "encoding", throughline: "MC", narrative: "narrative_storyform_a", ncp_path: "narratives[0].subtext.storypoints"}` — wenn novel-architect das schickt, weiß dramatica-vocabulary genau was zu liefern ist.
- [ ] **NCP-Enum-Awareness**: Wenn dramatica-vocabulary einen Element-Begriff vorschlägt, sollte sie auch den korrespondierenden `narrative_function`-Enum-Wert liefern (NCP hat 144 canonical narrative_functions).
- [ ] **KTAD-Coherence-Check**: Bei ncp-author-Hook → dramatica-vocabulary wird KTAD geprüft. Aktuell informeller Vermerk in ncp-author SKILL.md.

---

## dramatica-theory

- [ ] **Encoding-Phase Quick-Reference**: Aktuell stark auf Storyforming, schwächer auf Encoding für Dual-Storyform-Projekte.
- [ ] **Dual-Storyform-Diagnostik**: Asymmetrische Storyforms parallel zu führen ist kein Standard-Fall. Empire/Barbie-Beispiele aus NCP-SPECIFICATION als Referenz aufnehmen.

---

## research-prompt-optimizer

- [ ] **Gemini-Archivist Template**: Eigener vorgefertigter Prompt-Template-Variant für den novel-architect /analyze-Use-Case.
- [ ] **Output-Schema-Spec**: Output-Schema mit Struktur „Befund | Beleg | NCP-Pfad-Hypothese | canon-meta-Sektion-Hypothese | Slot-Hypothese".

---

## doc-coauthoring

- [ ] **canon-meta.md Variante prüfen**: doc-coauthoring ist generisch. Für canon-meta.md-Updates wäre eine Roman-spezifische Variante mit Section-Awareness sinnvoll.

---

## Inter-Skill-Handoff-Schema (cross-cutting)

- [ ] **Standard-Handoff-Schema**: `{project, phase, narrative, throughline, ncp_path, brief, constraints}` als JSON-Format.
- [ ] **Per-Skill accepts/produces deklarieren**: Roman-relevante Skills sollten in SKILL.md eine „Akzeptiert"/„Produziert"-Sektion haben.

---

## Skill-Kandidat: ncp-validator

- [ ] **Existiert noch nicht** als eigenständiger Skill. Idee: lightweight wrapper um upstream `validate-file.js`, der nach jeder ncp-author-Mutation läuft und Schema-Konformität bestätigt. Könnte in ncp-author selbst integriert werden (TODO T-2 dort).

---

## Skill-Kandidat: canon-diff

- [ ] **Existiert noch nicht.** Idee: Standalone-Skill, der den Skill-Canon (NCP + canon-meta.md) gegen externe Snapshots (Drive-Reset-Doc, Memory-Export, alte Skill-Versionen) diffed — Drift-Report mit Konflikt-Detection.
- [ ] **Skill-Canon-First**: canon-diff darf NICHT externe Snapshots als „korrekt" behandeln. Skill-Files sind Source-of-Truth. Externe Quellen sind Vergleichsmaterial, nicht Korrektur-Maßstab.
- [ ] **On-Demand-Invokation**: Nicht auto-laufen-lassen. Nur wenn User explizit Audit verlangt („gleicht Drive zum Skill ab?", „ist die Memory aktuell?").

---

## Skill-Kandidat: writing-navigator

- [ ] **Lower priority** jetzt — novel-architect IST faktisch der Navigator für Kohärenz Protokoll.

---

## Globale Beobachtungen

### Mehrfach-Trigger-Konflikte
„Storyform" triggert dramatica-theory + dramatica-vocabulary + novel-architect + ncp-author. Hierarchie: novel-architect ist Hub, andere Skills werden VON novel-architect aufgerufen, nicht direkt.

### NCP-Lock-in-Risiko
Mit v0.3.0 ist novel-architect NCP-abhängig. Mitigations-Plan in `references/canon/README.md`: Wenn NCP-Pfad sich blockierend erweist (Validator kommt nie, Schema-Drift wird unhandhabbar), Rollback auf Markdown-Canon ist möglich (regressives Refactoring, kein Daten-Verlust).

### Versionierungs-Drift
Skills haben uneinheitliche Versionierung. Wenn mehrere Skills für einen Workflow geladen werden, ist nicht klar welche Versionen miteinander getestet sind.

### Dokumentations-Drift
BERICHT.md im novel-architect war nach 4 Wochen veraltet. → Skill-interne Status-Dokumente sollten ein „Last-Verified" haben und beim Bootstrap geprüft werden.
