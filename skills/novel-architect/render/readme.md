# Render Helpers

Python-Skripte für File-IO und Status/Plan-View-Generierung. Mirrors das Pattern
von `research-prompt-optimizer/render/`.

## Files

| File | Phase | Funktion |
|------|-------|----------|
| `io_helpers.py` | alle | File-IO, atomic writes, status/plan/audit views, project-config helpers |
| `render_intent.py` | 1 | `intent.yaml` → `phase1-intent-status-view.md` |
| `render_architecture.py` | 2 | `architecture.yaml` → `phase2-architecture-status-view.md` |
| `render_scene_matrix.py` | 5 | `architecture.yaml` + `character-architecture.yaml` → `scene-matrix.md` (Skelett) |

## Invocation

```bash
# Aus dem Skill-Pfad:
python3 render/render_intent.py <project-slug>
python3 render/render_architecture.py <project-slug>
python3 render/render_scene_matrix.py <project-slug>
```

Alle Skripte erwarten einen Projekt-Workspace unter `/home/claude/novel-projects/<slug>/`.

## Dependencies

- Python 3.11+
- `pyyaml` (für YAML-IO)
- Stdlib (`pathlib`, `json`, `datetime`, `shutil`, `tempfile`)

## Erweitern

Weitere render-Skripte (z.B. `render_character.py`, `render_audit.py`) folgen
demselben Pattern: import `io_helpers`, read project files, write via
`atomic_write` oder Helper-Funktionen.
