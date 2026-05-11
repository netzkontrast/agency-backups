# /novel-draft — Phase 6 Trigger

> **Phase:** 6 (Drafting)
> **/sc:-Analog:** `sc:implement` + `sc:test`

## Zweck

Per-Kapitel Prosa-Entwurf mit harten Pre-Checks gegen Architektur,
Charaktere, Scene Matrix, canon-meta.

## Trigger

- „/novel-draft Kapitel X"
- „/draft"
- „Kapitel X schreiben"
- „Prosa für ch-XX"

## Pre-Conditions (MANDATORY Pre-Checks)

```
1. NCP geladen, Kapitel-X-storybeats vorhanden ✓
2. canon-meta.md geladen ✓
3. open-questions.md → keine blockierenden OQs für Kapitel X? ✓
4. character-architecture.yaml für beteiligte Charaktere geladen ✓
5. Storypoint des Kapitels klar (aus scene-matrix.md) ✓
6. POV / Erzählperspektive festgelegt ✓
7. Konflikt-Vektor klar ✓
```

Bei Fail: stop, surface askuser, optional Phase 5 oder Phase 7 first.

## Workflow

```
1. Lade chapter-draft-template.md (assets/)
2. Fülle Metadata aus scene-matrix.md + architecture.yaml
3. Erstelle drafts/ch-XX.<format>
4. Drafte Szene für Szene:
   - Konsultiere dramatica-vocabulary für Term-Präzision
   - POV-Schutz: strukturelle/stilistische Signale BESTÄTIGEN, nicht glätten
   - Bei Konflikt Theorie vs. Draft: Story-First-Rule
5. Post-Draft Konsistenz-Check (aus Template)
6. NCP moments[].prose_status = "drafted" (via ncp-author)
7. progress.md aktualisieren
```

## Output

- `drafts/ch-XX.docx` oder `drafts/ch-XX.md`
- ggf. NCP `moments[].prose_status` Update

## Hand-off

→ Phase 7 (`/novel-reflect`) für Konsistenz-Audit, oder zurück zu Phase 5 wenn Drafting Probleme aufdeckte

## Detail

- `phases/phase6-drafting.md`
- `assets/chapter-draft-template.md`
