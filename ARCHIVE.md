---
type: spec
status: active
slug: archive-spec
summary: "Governance-Spezifikation für Archivierungsregeln über Tasks, Prompts und Research-Artefakte inklusive Trigger, Operationsmodell, Invarianten und Ablaufcheckliste."
created: 2026-05-12
updated: 2026-05-12
---

# Archive Governance Spec

## Scope

Diese Spezifikation gilt für alle Artefakte unter:

- `/tasks/`
- `/prompts/`
- `/research/`

## Trigger für Archivierung

Archivierung wird ausgelöst, wenn mindestens einer der folgenden Trigger erfüllt ist:

1. **Task-Trigger (STRICT)**
   - **Nur** `task_status: done` ist archivierungsfähig.
   - `open`, `in_progress`, `blocked`, `updated`, `abandoned` und `archived` dürfen **nicht** aus `/tasks/` in `/archive/tasks/` verschoben werden.
   - Zusätzlich ist ein Cooldown abgelaufen (Standard: 7 Tage seit `updated`, sofern kein aktiver Folge-Task verlinkt ist).
2. **Prompt-Trigger**
   - Der referenzierte Task ist abgeschlossen (`done` oder `abandoned`) und der Prompt hat keine offenen Folgeausführungen.
3. **Research-Trigger**
   - `research_phase` ist `complete`.
   - Alle dokumentierten Folgefragen sind entweder als neue Prompts ausgelagert oder als erledigt markiert.
4. **Manueller Governance-Trigger**
   - Eine explizite Archivierungsentscheidung wurde in einem Task/Decision-Dokument dokumentiert.

## Operationsmodell

Archivierung nutzt genau eines der folgenden Modi je Artefakt:

1. **Move**
   - Datei/Ordner wird in einen definierten Archivpfad verschoben.
   - Einsatz: abgeschlossene, selten benötigte Artefakte mit stabilen Referenzen.
2. **Snapshot**
   - Ein unveränderlicher Snapshot wird erzeugt, während das Original aktiv bleibt oder weiterlebt.
   - Einsatz: revisionskritische Zwischenstände oder Governance-Meilensteine.
3. **Index-only-Archivmarkierung**
   - Keine Dateiverschiebung; nur Index-/Readme-/Frontmatter-Markierung als archiviert.
   - Einsatz: wenn Relativlinks und Tooling stark auf aktuelle Pfade angewiesen sind.

Die gewählte Operation MUST pro Archivierungsaktion begründet und im jeweiligen Index dokumentiert werden.

## Canonical Archive Paths

Die kanonischen Ziele für `Move` sind:

- `/archive/tasks/<task-folder>/`
- `/archive/prompts/<prompt-folder>/`
- `/archive/research/<research-folder>/`

Für diesen Repo-Workflow ist `Move` der **Default-Modus** für abgeschlossene Artefakte. `Index-only` ist nur zulässig, wenn ein dokumentierter Tooling-Blocker vorliegt.

## Invarianten

Jede Archivierungsaktion muss folgende Invarianten erhalten:

1. **Keine kaputten Relativlinks**
   - Interne Links müssen nach der Aktion auflösbar bleiben.
2. **Audit-Graph bleibt nachvollziehbar**
   - Beziehungen zwischen Task ↔ Prompt ↔ Research dürfen nicht unkenntlich werden.
3. **Frontmatter bleibt valide**
   - L1/L2-Felder bleiben schema-konform; Datums- und Statusfelder bleiben parsebar.
4. **Provenienz bleibt rekonstruierbar**
   - Archivierungszeitpunkt, Grund und gewählter Modus müssen dokumentiert sein.

## Archivierungs-Checkliste (Reihenfolge bindend)

1. **Pre-Check**
   - Trigger verifizieren.
   - Link-/Graph-Auswirkungen prüfen.
   - Betroffene Indexdateien identifizieren.
2. **Archive Action**
   - Gewählten Modus (Move/Snapshot/Index-only) ausführen.
   - Archivierungsgrund und Zeitpunkt dokumentieren.
3. **Index Sync**
   - Alle betroffenen `readme.md`/Indexdateien und Statuslisten synchronisieren.
4. **Post-Check**
   - Governance-Checks ausführen.
   - Link-Integrität und Frontmatter-Validität bestätigen.

Ein Lauf gilt nur als abgeschlossen, wenn alle vier Schritte in dieser Reihenfolge erfüllt sind.


## Hard Guardrail — Tasks

- ONLY Done Tasks can be archived.
- Every archive run MUST verify `task_status == done` immediately before `git mv`.
- If a Task is not `done`, the run MUST skip it and log the skip reason.
