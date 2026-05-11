# Phase 0 — Bootstrap (Workspace Setup)

> **Load when:** Skill triggert + Workspace existiert nicht / `project-config.yaml` fehlt / askuser für Projekt-Auswahl

## §0 Goal

Funktionierender Projekt-Workspace unter `/home/claude/novel-projects/<slug>/`
mit gültiger `project-config.yaml`. Skill weiß, welches Projekt geladen ist.

## §1 Entscheidungsbaum

```
Skill triggert
   ↓
Existiert /home/claude/novel-projects/ ?
   ├── nein → mkdir -p /home/claude/novel-projects/
   │          askuser: "Was möchtest du?"
   │            ├── "Neues Projekt anlegen"
   │            ├── "Demo-Projekt anlegen (für Erkundung)"
   │            └── "Kohärenz-Protokoll vom Legacy migrieren"
   │
   └── ja → ls /home/claude/novel-projects/*/
              ├── leer → askuser wie oben
              ├── ein Projekt → askuser: "Lade <slug>? Oder neues anlegen?"
              └── mehrere Projekte → askuser: project_slug auswählen
```

## §2 Bootstrap-Slots (askuser ≤3)

| Slot | Required | One-line meaning |
|------|----------|------------------|
| `project_action` | **yes** | `new` / `load_existing` / `demo` / `migrate_legacy` |
| `project_slug` | **yes** (außer migrate_legacy) | kebab-case slug (z.B. `my-sf-novel`) |
| `project_language` | **yes** (nur bei new/demo) | `de` / `en` / `...` |

## §3 Action-Branches

### §3.1 `project_action: new`

1. `mkdir -p /home/claude/novel-projects/<slug>/`
2. `cp skills/novel-architect/assets/project-config-template.yaml /home/claude/novel-projects/<slug>/project-config.yaml`
3. Edit: `project.slug`, `project.name`, `project.language`, `project.workspace_root` setzen
4. `cp skills/novel-architect/assets/project-progress-template.md /home/claude/novel-projects/<slug>/progress.md`
5. Erstelle leere Stubs: `intent.yaml`, `open-questions.md`, `learnings.md`, `canon-meta.md`, `canon/<slug>.ncp.json` (von `ncp-author/assets/template-empty.json`)
6. Bereit für Phase 1.

### §3.2 `project_action: load_existing`

> **Wichtig:** Auf einer NEUEN Projekt-Session existieren `intent.yaml`,
> `architecture.yaml`, `character-architecture.yaml`, `scene-matrix.md` ggf.
> noch nicht. Sie werden in den jeweiligen Phasen 1/2/3/5 erst geschrieben.
> Lies nur, was vorhanden ist, und respektiere das Phase-Routing.

1. Lade `project-config.yaml` aus `/home/claude/novel-projects/<slug>/`
2. Lies `progress.md` — wo wurde aufgehört, was kommt als nächstes?
3. Lies `<slug>.ncp.json` — strukturelle Canon-Daten (falls vorhanden)
4. Lies `canon-meta.md` — nicht-strukturelle Canon-Daten (falls vorhanden)
5. Lies `open-questions.md` — welche OQs blockieren was? (falls vorhanden)
6. Lies `learnings.md` — was lief in früheren Sessions suboptimal? (falls vorhanden)
7. Lies bisherige Phase-Outputs (`intent.yaml`, `architecture.yaml`, etc.) — nur wenn vorhanden
8. **Konsistenz prüfen:** progress.md vs. NCP vs. canon-meta — drift?
9. **Pre-Action-Sanity-Check:** gegen resolved-OQs abgleichen
10. Empfiehl nächsten Schritt aus progress.md

### §3.3 `project_action: demo`

1. `mkdir -p /home/claude/novel-projects/demo-novel/`
2. Kopiere `examples/example-intent.yaml`, `examples/example-architecture.yaml` etc.
3. Markiere als Demo (`project-config.yaml` → `project.is_demo: true`)
4. User kann damit Phase 2-7 explorieren ohne echtes Projekt anzulegen

### §3.4 `project_action: migrate_legacy`

1. Prüfe Existenz `skills/novel-architect-legacy/references/canon/kohaerenz-protokoll.ncp.json`
2. Führe aus: `bash skills/novel-architect/scripts/bootstrap_project.sh kohaerenz-protokoll`
3. Skript erstellt `/home/claude/novel-projects/kohaerenz-protokoll/` und kopiert:
   - `references/canon/kohaerenz-protokoll.ncp.json` → `canon/kohaerenz-protokoll.ncp.json`
   - `references/canon-meta.md` → `canon-meta.md`
   - `references/progress.md` → `progress.md`
   - `references/open-questions.md` → `open-questions.md`
   - `references/learnings.md` → `learnings.md`
4. Generiert `project-config.yaml` aus Legacy-Metadaten (dual storyform, 39 chapters, etc.)
5. Bestätige Migration; bereit für Phase 7 (Iteration auf Migration prüfen)

## §4 Konsistenz-Check (Pre-Action-Sanity-Check)

Nach Bootstrap und vor erster Tool-Aktion explizit gegen die Liste der
resolved-OQs (`~~Strikethrough~~`-Einträge in `open-questions.md`) abgleichen.
*„Hat das Issue, das ich gleich angehe, vielleicht schon eine resolved-OQ-
Antwort?"* Wenn ja: dem User aktiv anzeigen, statt das Issue komplett neu zu
rollen.

## §5 Exit Gate

Phase 0 ist done, wenn:
- `project-config.yaml` existiert und validiert
- `progress.md` gelesen, nächster Schritt bekannt
- `learnings.md` gelesen
- Konsistenz-Check passed (kein drift)
- User-Input kann beantwortet werden

## §6 Bootstrap-Heuristik

Der Bootstrap muss nicht bei jeder User-Nachricht laufen — nur einmal pro
Session. Wenn `project-config.yaml` bereits in Session gelesen wurde, skippen.

## §7 /sc:-Mapping

| Schritt | /sc: Command |
|---|---|
| Projekt laden | `sc:load` |
| Projekt-Übersicht | `sc:index` |
| Migration prüfen | `sc:analyze` |
