# Phase 4 — World & Research

> **Load when:** Phase 4 ist aktiv, oder Research-Domain-Wahl, oder Welt-Bibel-Frage

## §0 Goal

Identifiziere Forschungs-Domänen aus `intent.yaml`, erstelle Recherche-Briefs,
delegiere Deep-Research an `research-prompt-optimizer`, integriere Findings in
`world-bible.md`.

## §1 Input / Output

**Input:** `intent.yaml` (insb. `philosophy_integration_level`, `science_integration_level`, `known_priors`)

**Output:**
- `world-bible.md` (Roman-Welt-Bibel)
- `research/briefs/<domain>.md` (Pro Domain ein Brief)
- `research/findings/<domain>.md` (Pro Domain die Ergebnisse)
- optional: NCP `signposts[]` content updates (wenn Forschung Canon ändert)

## §2 Sub-Phases

```
Phase 4.1   Identify research domains                          (auto from intent + askuser)
Phase 4.2   Prioritize domains
            ──── GATE (research scope) ────                     (1 askuser)
Phase 4.3   For each domain: render research brief             (uses assets/research-brief-template.md)
Phase 4.4   Hand off to research-prompt-optimizer              (delegates)
Phase 4.5   Ingest findings → world-bible.md                   (manual review + canon-meta updates)
Phase 4.6   Update NCP signposts/concerns if relevant          (delegate ncp-author)
```

## §3 Domain Identification

Aus `intent.yaml`:
- `genre` + `subgenre_modifiers` → Genre-typische Domänen
- `philosophy_integration_level: engine` → Philosophie-Domänen sind PRIO
- `science_integration_level: engine` → Wissenschafts-Domänen sind PRIO
- `core_conflict_question` → Konflikt-spezifische Domänen
- `known_priors` → vom User vorgegebene Themen

Beispiel-Mapping (Hard-SF):
- Quantenphysik, Informationstheorie, Kognitionswissenschaft, KI-Ethik, Topologie

Beispiel-Mapping (Literary Fiction):
- Sozialwissenschaft, Psychologie, lokale Geschichte, Kultur

Beispiel-Mapping (Fantasy):
- Mythologie, Folklore, mittelalterliche Geschichte, Worldbuilding-Logik

## §4 Recherche-Brief-Template

`assets/research-brief-template.md` ist die Schablone. Pro Domain:
- Research-Frage (1-2 Sätze, präzise)
- Roman-Kontext (Genre, Core Conflict, betroffene Charaktere)
- Bisheriger Wissensstand
- Erwarteter Output-Typ + Tiefe + Sprache

## §5 Handoff zu research-prompt-optimizer

```
1. Schreibe research/briefs/<domain>.md (file-first)
2. present_files
3. askuser: "Brief fertig. An research-prompt-optimizer übergeben?"
   options: [Ja → Trigger /sc:research mit diesem Brief, Nein → manuell speichern]
4. Wenn Ja: explicit delegation
   "Bitte verwende research-prompt-optimizer mit folgendem Intent:
    - research_question: aus brief
    - audience: Roman-Autor
    - output_format: markdown_report
    - language: <project-config.language>
    - depth: <surface|standard|exhaustive>
    - success_criterion: 'Wenn die Erkenntnisse in den Roman einfließen können'
    - known_priors: aus brief"
```

## §6 Findings Integration

Nach Recherche-Abschluss von `research-prompt-optimizer`:

1. Lade `research/findings/<domain>.md`
2. **Roman-Relevanz-Check:** Welche Findings ändern Canon?
3. Update `world-bible.md`:
   - Section pro Domain
   - Quellen-Verweise
   - Roman-relevante Highlights
4. **Bei Canon-Auswirkung:** Update `canon-meta.md`
5. **Bei Storypoint-Auswirkung:** Delegate `ncp-author` für NCP-Update
6. **Bei OQ-Resolution:** Update `open-questions.md`

## §7 Hard Rules

- **Phase 4 ist iterativ** — nicht alle Domänen in einer Session
- **research-prompt-optimizer ist NICHT optional** für tiefe Recherche — er hat das Pattern
- **Findings müssen Roman-tauglich sein** — pure Wikipedia-Zitate sind unzureichend
- **world-bible.md ist die Single-Source-of-Truth für World-Lore**, nicht der Skill

## §8 Edge Cases

### §8.1 User möchte ohne research-prompt-optimizer arbeiten

→ OK, aber: warn dass Konsistenz/Tiefe leidet
→ Manuelle Findings müssen trotzdem in `research/findings/` strukturiert sein

### §8.2 Forschung widerspricht intent.yaml

z.B. user wollte „Roman über Bewusstsein", Recherche zeigt: das Thema ist zu groß
→ Surface: *„Recherche zeigt: das Thema bräuchte 200k Wörter, nicht 80k. Scope-Reduction?"*
→ Optionen: Reduce scope (back to Phase 1) / Increase length_target / Continue with caveat

### §8.3 Findings sind blockierend für Phase 5/6

z.B. „Wir können Kapitel 5 nicht schreiben, weil Quantum-Detail fehlt"
→ Markiere als blockierende OQ in `open-questions.md`
→ Phase 4 bleibt offen, Phase 5/6 für betroffene Kapitel pausiert

## §9 Exit Gate

Phase 4 hat **keine harte Exit Gate** — sie ist kontinuierlich. Aber für Phase 5 nötig:
- Genug Welt-Material für `scene-matrix.md`
- Keine blockierenden Research-OQs für Kapitel 1-10

## §10 /sc:-Mapping

| Schritt | /sc: Command |
|---|---|
| Domain-Identifikation | `sc:brainstorm` |
| Deep Research | `sc:research` (delegiert intern an research-prompt-optimizer) |
| World-Bible Schreibung | `sc:document` |
| Findings-Analyse | `sc:analyze` |
