# /novel-start — Phase 0+1 Trigger

> **Phase:** 0 (Bootstrap) + 1 (Intent Capture)
> **/sc:-Analog:** `sc:brainstorm` für Konflikt-Exploration

## Zweck

Startet ein neues Roman-Projekt oder lädt ein bestehendes. Triggert
Bootstrap (Phase 0) und führt direkt in Intent Capture (Phase 1).

## Trigger

- „/novel-start"
- „Starte einen Roman"
- „Neues Roman-Projekt"
- „Lade Projekt X"

## Workflow

```
1. Phase 0 (Bootstrap):
   - Existiert /home/claude/novel-projects/?
   - askuser: project_action (new/load/demo/migrate)
   - bei new: askuser project_slug + language
   - Workspace setup
   - Reference-Files lesen

2. Phase 1 (Intent Capture):
   - Loop ≤3 askuser per turn
   - Intent Slot Set: genre, audience, core_conflict, methods, etc.
   - File-first: intent-status-view.md
   - Approval-Gate: intent.yaml approved
```

## Output

- `/home/claude/novel-projects/<slug>/project-config.yaml`
- `/home/claude/novel-projects/<slug>/intent.yaml` (approved)
- `/home/claude/novel-projects/<slug>/intent-status-view.md` (final)

## Hand-off

→ Phase 2 (`/novel-design`) für Narrative Architecture

## Detail

- `phases/phase0-bootstrap.md`
- `phases/phase1-intent-capture.md`
- `assets/project-config-template.yaml`
- `assets/intent-template.yaml`
