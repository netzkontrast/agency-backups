# Method: Deep Research Briefs (Delegation an research-prompt-optimizer)

> **Category:** Research
> **Load when:** Phase 4.3-4.4 (Brief schreiben + Delegation)

## §0 Konzept

`novel-architect` macht selbst KEINE Deep Research. Stattdessen werden
Recherche-Briefs erstellt und an `research-prompt-optimizer` delegiert. Dieser
baut den Deep-Research-Prompt und ruft ein externes System auf (Gemini Deep
Research, Perplexity, Claude Research).

## §1 Workflow

```
1. Pro Domain: research/briefs/<domain>.md schreiben
   (Template: assets/research-brief-template.md)
2. askuser: "Brief fertig. An research-prompt-optimizer übergeben?"
3. Bei Ja: Trigger research-prompt-optimizer mit den Brief-Inhalten
4. research-prompt-optimizer durchläuft seine 5-Phasen-Pipeline:
   - Intent Capture
   - Planning (3 Gates)
   - Render
   - Reader Test (opt-in)
   - Finalize → Workspace-Zip
5. Externer Research-Agent läuft mit dem rendered prompt
6. Findings kommen zurück → research/findings/<domain>.md
7. novel-architect Phase 4.5-4.6 integriert Findings in world-bible.md + canon-meta + ggf. NCP
```

## §2 Brief-Anatomie

Aus `assets/research-brief-template.md`:

1. **Brief Metadata** — Projekt, Domain, Integration-Level, Priorität
2. **Research-Frage** — präzise, 1-2 Sätze
3. **Was ist NICHT gemeint** — Abgrenzung
4. **Roman-Kontext** — Genre, Core Conflict, betroffene Charaktere
5. **Bisheriger Wissensstand** — was weißt du schon, welche Quellen
6. **Erwarteter Output-Typ** — markdown_report, comparison_table, etc.
7. **Handoff-Anweisung** — explizite Delegation

## §3 Handoff-Pattern

```
ask_user_input_v0:
  question: "Recherche-Brief für '<domain>' bereit. Wie weiter?"
  options:
    - "An research-prompt-optimizer übergeben (Deep Research starten)"
    - "Manuell recherchieren (ich mache selbst)"
    - "Brief erst anpassen"
```

Bei „research-prompt-optimizer":
- Explicit handoff message: „Bitte verwende research-prompt-optimizer Skill"
- Brief-Datei als Input
- Resultat: rendered prompt in research-prompt-optimizer's workspace

## §4 Findings-Integration Pattern

Wenn Findings zurückkommen:

```
1. research/findings/<domain>.md lesen
2. Klassifizieren der Findings:
   - relevant für world-bible (Welt-Lore) → world-bible.md update
   - relevant für canon (Roman-Regel) → canon-meta.md update
   - relevant für Charakter (Motivation, Background) → character-architecture.yaml update
   - relevant für Storypoint → architecture.yaml + NCP update
   - relevant für offene Frage → open-questions.md update
3. Cascading: Wenn Update Phase 5/6 betrifft → entsprechende Phase anstoßen
4. Checkpoint: Skill packen
```

## §5 Hard Rules

- **Nicht selbst tief recherchieren** — das ist research-prompt-optimizer's Domain
- **Briefs müssen Roman-spezifisch sein** — nicht generische Wissens-Anfragen
- **Findings müssen kuratiert werden** — Raw-Output aus DRG ist nicht Welt-Bibel-ready
- **Citations preserve** — pro Finding Quelle, damit später nachgesucht werden kann

## §6 Anti-Patterns

- „Schick alles an research-prompt-optimizer, dann sehen wir" — zu viel Output, ohne Kuration nutzlos
- Briefs zu breit („Forschung zu Bewusstsein") — DRG produziert dann oberflächlichen Report
- Findings ungekürzt in world-bible kopieren — Welt-Bibel ist Roman-tauglich, nicht Wissenschaftsdoku
