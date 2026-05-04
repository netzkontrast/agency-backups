# /interview — Strukturiertes Autor-Interview

> **Status**: Stub. Voller Prompt-Template ausstehend.

## Zweck

Wenn der Canon eine Lücke hat (offene OQ, Detail-Frage, Storypoint-Klärung), wird der User strukturiert interviewt — nicht offen befragt. Ziel: Multi-Variable-Entscheide kollabieren in 2-4 Optionen, jede mit Implikationen.

## Format

- **Max 3 Fragen pro Runde**
- Jede Frage hat **2-4 Optionen** (single_select oder multi_select)
- Jede Option hat eine **kurze Implikation** angedeutet (was bedeutet diese Wahl für andere Canon-Bereiche)
- Tool: `ask_user_input_v0`

## Wann triggert /interview

- Workflow `open-questions-resolution` läuft
- Eine OQ ist nicht durch Reasoning lösbar — User muss entscheiden
- Multi-Variable-Frage taucht in einem anderen Workflow auf (z. B. „welcher Alter trägt diese Szene?")
- User selbst sagt „interview mich"

## Pre-Checks

- OQ ist klar formuliert
- 2-4 plausible Optionen identifiziert
- Implikationen je Option vorab durchdacht (sonst nicht sinnvoll fragen)

## Anti-Pattern

- Offene Fragen ohne Optionen
- Mehr als 3 Fragen in einer Runde
- Optionen, die der User selbst formulieren muss
- Frage stellen ohne vorab durchdachte Implikationen

## Beispiel-Skeleton

> Frage: „Wie soll Junas Erscheinungs-Modus in Akt II markiert werden?"
> 
> Optionen:
> 1. Phantom-Resonanz im Host-Feld (subtil, indirekt) — *Implikation: Silas-Arc trägt mehr Last, Juna bleibt weiter unsichtbar*
> 2. Anomale Erasure-Balance (physikalisch lesbar) — *Implikation: DKT-Mechanik wird in Akt II expliziter, Risiko Bruch der „erste 50 Seiten ohne DKT"-Regel*
> 3. Phone-Silence als wiederkehrender Anker (rituell) — *Implikation: Block-4-Anker wird strukturell verknüpft, Risiko der Direktheit*

## Output

User-Antwort wird im aufrufenden Workflow konsumiert (typisch: `open-questions-resolution`).

## TODO

Voller Template + Beispielsammlung ausstehend.
