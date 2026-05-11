# Research Brief — `<DOMAIN>`

> **Phase:** 4 (World & Research)
> **Handoff zu:** `research-prompt-optimizer` (Skill, der Deep-Research-Prompts baut)
> **Written by:** Phase 4
> **Outcome of research:** `research/findings/<domain>.md`

## Brief Metadata

- **Projekt:** <SLUG>
- **Domain:** <z.B. Quantenphysik, Kognitive Neurowissenschaft, KI-Ethik>
- **Integration-Level:** <decoration | frame | engine>
- **Priorität:** <core | supporting | nice-to-have>

## Research-Frage

> Eine Frage (1-2 Sätze, präzise). Dieses Brief geht an `research-prompt-optimizer`,
> dieser baut daraus einen Deep-Research-Prompt für Gemini/Perplexity/etc.

**Frage:** <PLACEHOLDER>

**Was ist NICHT gemeint:** <PLACEHOLDER Abgrenzung>

## Roman-Kontext (für den Researcher zur Orientierung)

- **Genre:** <aus intent.yaml>
- **Core Conflict:** <aus intent.yaml>
- **Welche Charaktere/Plotpunkte berühren diese Domain?** <PLACEHOLDER>
- **Wie soll die Information in den Roman einfließen?** <PLACEHOLDER>
  - z.B. „als technische Backstory für AEGIS-System-Beschreibung"
  - z.B. „als Konflikt-Engine für MC-IC-Diskussion"

## Bisheriger Wissensstand

- Was weißt du bereits? <PLACEHOLDER>
- Welche Quellen hast du schon gelesen? <PLACEHOLDER>
- Welche Hypothesen hast du? <PLACEHOLDER>

## Erwarteter Output-Typ

- <markdown_report | comparison_table | annotated_bibliography | concept_map>
- **Tiefe:** <surface | standard | exhaustive>
- **Sprache:** <de | en>

## Handoff-Anweisung

```
Übergib dies an research-prompt-optimizer:
- Trigger: "/sc:research" oder direkt skill-aufruf
- Phase 1 Intent dort wird aus diesem Brief abgeleitet
- Bestätige roman-spezifische Eingrenzung (audience = Roman-Autor, output_format = Roman-tauglich)
```

## Findings-Integration

Nach Recherche-Abschluss:
1. `research/findings/<domain>.md` schreiben
2. `world-bible.md` aktualisieren (Roman-relevante Erkenntnisse)
3. Bei Canon-Auswirkung: `canon-meta.md` updaten
4. Bei Storypoint-Auswirkung: NCP updaten via `ncp-author`
