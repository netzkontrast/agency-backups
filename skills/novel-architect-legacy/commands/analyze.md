# /analyze — Gemini-Archivist Research-Ingestion

> **Status**: Stub. Voller Prompt-Template ausstehend (siehe skill-improvement-todo.md).

## Zweck

Wenn der User Recherche-Material (PDFs, Web-Quellen, eigene Notizen) gegen den Roman-Canon prüfen lassen will. Pipeline:

1. novel-architect identifiziert das Research-Anliegen
2. research-prompt-optimizer baut den Gemini-Deep-Research-Prompt (5-Phasen-Pipeline, MAPS-D oder SPECD)
3. User führt Prompt extern in Gemini Deep Research aus
4. Output wird zurück in novel-architect gegeben → /synthesize Workflow

## Pre-Checks

- NCP-Datei und canon-meta.md geladen (für Widerspruchs-Prüfung)
- Research-Anliegen ist klar definiert (nicht zu breit — sonst zerfällt Gemini-Output)

## Stub-Prompt-Skeleton (zu erweitern)

```
ROLLE: Du bist Archivist für ein Hard-SF/Philosophical-Horror-Romanprojekt.
KONTEXT: <relevanter Canon-Auszug aus NCP-Datei + canon-meta.md>
AUFGABE: <konkrete Research-Frage>
OUTPUT-SCHEMA:
- Befund (was ist die Antwort)
- Beleg (Quellen)
- Canon-Implikation (was würde sich am Canon ändern?)
- Canon-Target-Hypothese (welche NCP-Pfade oder canon-meta-Sektionen wären betroffen?)
ZWANG: Keine Spekulation ohne Beleg. Wenn unklar: explizit „nicht entscheidbar" mit Begründung.
```

## Output-Konsumption

Gemini-Output → `outputs/research/<topic>.md` strukturieren mit:
- Original-Prompt
- Gemini-Output verlinkt/eingebettet
- Widerspruchs-Report gegen NCP + canon-meta.md
- Canon-Implikationen aufgelistet (NCP-Pfade + canon-meta-Sektionen)

Dann: /synthesize aufrufen, falls Implikationen substantiell sind.

## TODO

Voller Template ausstehend. Bei nächster Research-Runde: Template hier erweitern, gegen real-world Use-Case validieren.
