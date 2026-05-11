# Chapter Draft Template

> **Schema:** Prosa-Skeleton mit Pre-Checks (Phase 6)
> **Written to:** `drafts/ch-XX.docx` oder `drafts/ch-XX.md`

## Pre-Draft Checklist

- [ ] `<slug>.ncp.json` geladen, Kapitel-X-storybeats vorhanden
- [ ] `canon-meta.md` geladen (Prosa-Regeln, Mandate)
- [ ] `open-questions.md` → keine blockierenden OQs für dieses Kapitel?
- [ ] `character-architecture.yaml` für beteiligte Charaktere gelesen
- [ ] Storypoint des Kapitels klar (aus `scene-matrix.md`)
- [ ] POV / Erzählperspektive festgelegt
- [ ] Konflikt-Vektor klar

## Metadata

- **Projekt:** <SLUG>
- **Kapitel:** XX — "<TITEL>"
- **Akt:** <I/II/III/IV>
- **Wortzahl-Ziel:** <z.B. 2000-4000>
- **POV:** <z.B. 1. Person, Kael>
- **Storyform-Fokus:** <Single | Storyform A | Storyform B | Beide>
- **Storypoint:** <aus architecture.yaml>
- **Moment-IDs (NCP):** moment_ch{XX}_a_s01, moment_ch{XX}_a_s02, ...

## Szenen-Outline (aus Scene Matrix)

1. **Szene 1 — moment_ch{XX}_s01:** <Beschreibung>
2. **Szene 2 — moment_ch{XX}_s02:** <Beschreibung>
3. **Szene 3 — moment_ch{XX}_s03:** <Beschreibung>

## Prosa-Skeleton

<!-- Hier kommt die eigentliche Prosa. Niemals den Skeleton-Header löschen — er ist
     Referenz für Re-Drafts und Konsistenz-Checks. -->

### Szene 1 — `<Schauplatz, Zeit>`

<PROSA>

### Szene 2 — `<Schauplatz, Zeit>`

<PROSA>

### Szene 3 — `<Schauplatz, Zeit>`

<PROSA>

## Post-Draft Konsistenz-Check

- [ ] Storypoint erkennbar im Draft
- [ ] Charaktere konsistent mit `character-architecture.yaml`
- [ ] POV-Schutz: strukturelle/stilistische Signale (Risse, Mosaikstruktur, Fußnoten) sind *intentional*, nicht versehentlich
- [ ] Bei dual storyform: beide Throughlines erkennbar
- [ ] NCP `moment.prose_status` → `drafted` setzen (via ncp-author)
- [ ] `progress.md` aktualisieren

## Open Questions aus diesem Draft

<!-- Fragen, die durch das Drafting aufgetaucht sind, hier listen — werden in open-questions.md migriert -->

- [ ] OQ-XX: <Frage>
