# Progress — Kohärenz Protokoll

> **Letztes Update:** 2026-05-03 (Session 2: Drive-Doc-Ingest + Storyform-Kandidaten-Sichtung, Skill v0.3.2)

## Session-2-Output (2026-05-03)

**Workflow:** research-ingestion (Drive-Doc-Ingest)

**Was passierte:**
1. 14 Drive-Files identifiziert (Suche: `Dual-Kernel`/`DKT` titel + Outline/Storyform-Files modifiedTime > 2026-04-26).
2. 10 Files priorisiert (deduped per Titel-Cluster, größte Revision behalten, research-prompt-Inputs ausgeschlossen).
3. PDF-Export-Pipeline gebaut: `Google Drive:download_file_content` (exportMimeType=application/pdf) → /tmp/*.pdf → pdfplumber-basierter Konverter → `/home/claude/novel-architect-workspace/ingest/*.md`.
   - Pivot: `pymupdf4llm` nicht installierbar (PyPI im Sandbox gesperrt). Fallback auf vorinstalliertes `pdfplumber`. Output-Qualität für Prosa adäquat, Heading-Hierarchie geht verloren.
   - PDF-bytes blieben **context-safe** (Tool-Results auf Disk gespeichert, nicht in den Chat geladen).
4. Nach Ingest: zwei Whitespace-Dupe-Paare per md5 + diff identifiziert und entfernt.
5. Storyform-Kandidaten extrahiert via grep auf `Hypothese\s*[0-9H]` und `Kandidat\s*[0-9]`. Pro Marker ~30 Zeilen Body-Kontext extrahiert.

**Output-Files:**
- `outputs/research/storyform-candidates-inventory.md` — 8 Kandidaten mit Verdikt, Konflikt-Notizen, Empfehlung.
- `outputs/research/ingest-manifest-2026-05-03.md` — Datei-Index aller 10 ingest-Files mit Storyform-Marker-Density.
- `ingest/*.md` — 10 Markdown-Files (Drive-Originale).

**Hauptbefund:** Acht Storyform-Kandidaten extrahiert. Keiner ist Canon. **Frontaler Widerspruch zwischen zwei Quellen** über AEGIS-Position:
- analyse-File bestätigt A1 = Status Quo (AEGIS = MC in Universe) — entspricht NCP-Canon.
- verortung-File zertifiziert V3 = AEGIS = IC in Mind als 'kanonisch' — kontrastiert NCP-Canon.

→ Konflikt **war bereits in einer parallelen Session heute resolved** (siehe `open-questions.md` OQ-04, OQ-05, OQ-06): A1 bleibt Canon, V3 falsifiziert (Bewusstseins-Kategorie-Fehler + ANP-Symmetrie-Bruch), AEGIS = System-Ebene-ANP, Dual-Storyform behalten. **Phase 1 ist nicht mehr blockiert.** Der Drive-Ingest hat First-Principles-Material geliefert, das nachträglich verifiziert, warum die Canon-Konfiguration korrekt ist — also nützlich als Konsistenz-Beleg, aber strukturell redundant zur parallelen Session.

**Bootstrap-Lücke entdeckt** (siehe `learnings.md` Eintrag 2026-05-03 zur Bootstrap-Read-Discipline): Bei Session-Start wurde `canon-meta.md` nicht vollständig gelesen, sondern nur strukturell überflogen — daher wurden die schon-canonisierten Sektionen (AEGIS-System-ANP, Holon-Spiegelachse, Voice-Regel, Per-Throughline-Mapping, Verworfene Alternativen) erst spät in der Session entdeckt. Skill-Update v0.3.3 zieht das nach.

---

## Wo wir stehen

**Phase**: Storyforming abgeschlossen. Storyform A („Heuristics of Integration") und Storyform B („Phoenix Collapse") sind als zwei narratives in `references/canon/kohaerenz-protokoll.ncp.json` codifiziert. Alle 16 Dynamics (8 pro narrative) sind im Skeleton gefüllt. Storypoints, Storybeats, Moments und Players sind initial leer — kommen Phase-für-Phase.

**Nächste angekündigte Phase**: Encoding (Phase 1-4 — Throughlines parallel durch beide narratives).

**Letzter inhaltlicher Stand** (codifiziert in NCP-Datei und canon-meta.md, abgleichbar mit Outline-Revision 2026-05-01 auf Drive):
- Multiplizitäts-Schleier bis Ch13
- Juna-Seed ab Ch1
- FM-Achievement Ch33
- Vortex Ch35-36
- Architektur-Frage Slot 16: Per-Chapter Dual-POV. Hypothese in NCP: Moments mit cross-narrative Storybeat-Referenzen — Resolution-Workflow ausstehend.

## Was diese Session tat

**Skill-Update v0.1.0 → v0.2.0 → v0.3.0 → v0.3.1**:

v0.2.0:
- Bootstrap-Protocol eingebaut
- Routing-Matrix für 10 Workflows
- Significance-Heuristik kodifiziert
- Reference-Files gebaut (canon-state, open-questions, workflows, significance-heuristics, skill-improvement-todo)
- commands/-Stubs angelegt
- Veraltete BERICHT.md + todo.md entfernt

v0.3.0 (Architektur-Pivot):
- **NCP als State-Management-Layer** (commitment durch User)
- `references/canon-state.md` aufgelöst → Split in:
  - `references/canon/kohaerenz-protokoll.ncp.json` (strukturell — Storyform A+B als zwei narratives, alle Dynamics gefüllt, Players/Storypoints/Storybeats/Moments initial leer)
  - `references/canon-meta.md` (nicht-strukturell — DKT, Alter-Somatik, Mandate, Prosa-Regeln, Vortex-Übersicht, Projekt-Meta)
  - `references/canon/README.md` (NCP-Status, Validierungsstatus, Risiken, Slot-16-Hypothese)
- Routing-Matrix updated: ncp-author ist jetzt **State-Layer-Owner**, nicht optional
- Workflows updated: jeder strukturelle Workflow (encoding, dynamics, weaving, vortex, oq-resolution wenn strukturell) hat ncp-author als Sub-Step
- Constraint hinzugefügt: NCP-Mutation NUR via ncp-author — keine Hand-Edits am JSON

v0.3.1 (Canon-Hierarchie-Korrektur durch User):
- **Skill-Files (NCP + canon-meta.md + open-questions.md + progress.md) sind Source-of-Truth**, nicht Memory
- Memory ist abgeleiteter Snapshot, kann älter sein, kann Anregung statt Fakt sein
- Bei Diskrepanz: Skill-Files gewinnen
- memory-sync degradiert von „State-Partner" zu „optional Outward-Broadcaster" — Skill→Memory only, niemals Memory→Skill
- Bootstrap-Schritt 6 (Memory-Diff) ersetzt durch Skill-interne Konsistenz-Prüfung
- canon-update-Workflow umstrukturiert: NCP + canon-meta zuerst, Memory nur auf User-Wunsch
- Anti-Pattern-Sektion erweitert um Memory-Hierarchie-Verletzungen
- Stale-Reference auf canon-state.md in commands/analyze.md entfernt

## Was als nächstes ansteht

**Phase 1 (MC-Encoding) ist unblocked.** Drei OQs aus Session 2 sind resolved (siehe `open-questions.md`):
- A1 vs V3 → A1 bleibt Canon
- AEGIS-Ontologie → AEGIS = System-Ebene-ANP, Holon-Spiegelachse kanonisiert
- Dual-Storyform vs Quasi/Single → Dual behalten, ANP-Symmetrie verlangt's

Verbleibende parallele Tasks:

1. **Encoding-Phase 1: MC-Throughline parallel A + B**. Storypoints (Problem/Solution/Symptom/Response, Crucial Element, Benchmark, Catalyst, Inhibitor) für beide MCs konkretisieren. Pro Storypoint: Szenen-Keime, Bilder, Räume. Konsistenz-Check gegen Block 4 (Anker abstrahiert, „Stille" statt Name). Trigger: „Phase 1 starten" oder „MC-Encoding".

2. **Slot 16 Per-Chapter-Dual-POV**. Material aus Session 2 (M1: Ontologische Transposition, Pronomen I↔I aber ontologische Ebene wechselt; M2: Prozessuale Transposition, Pronomen I→We) in canon-meta.md schon teil-integriert (Per-Throughline-Mapping). Operationalisierung als per-Chapter-Mechanik bleibt offen. Trigger: „Slot 16" oder „Dual-POV-Architektur".

3. **Open-Questions Appendix C abarbeiten**: Post-Vortex-AEGIS, Moonshine-Boundary, Juna-Erscheinungs-Modus-Anker, Genesis 4. Beat. Trigger: „Appendix C" oder „OQ Appendix".

4. **Memory-Edit nachziehen**: Die userMemory-Zeile „All 13 = 1st person. AEGIS + Guardians = 3rd person" muss revidiert werden zu „All 13 = 1st person. **AEGIS = 1st person in B's MC-Throughline (System-ANP), 3rd person in A's OS (Player). Guardians = 3rd person.**" Plus neue Zeile zur Holon-Spiegelachse. Macht der User per /memory-Sync, nicht automatisch.

## NCP-Maturity-Watch

Da NCP State-Layer ist, ist die Reife von `ncp-author` projekt-relevant:
- Aktueller Status: WIP 0.1.0-draft, kein eigener Validator
- Validierung läuft via upstream `validate-file.js` (Node)
- Bei nächster Session: prüfen ob ncp-author seit 2026-05-03 weitergebaut wurde
- Falls nicht: ggf. manuell upstream-Validierung an Skeleton-Datei laufen lassen

## Hinweise an die nächste Session

- **Hierarchie:** Diese Skill-Files sind Source-of-Truth. Memory ist Notiz/Anregung, kann älter sein. Bei Diskrepanz gewinnen Skill-Files.
- Wenn User auf etwas in Memory verweist, das hier nicht steht: nachfragen, ob das in den Canon übernommen werden soll. Nicht stillschweigend annehmen.
- Roman ist aktuell deprioritized — Skill ist bereit, drängt sich aber nicht auf. Kein „push", kein „nudge".
- NCP-Datei darf nur via ncp-author mutiert werden. Bei direkter Edit-Versuchung: STOP.
