# Assets

Template-Files für Phasen-Outputs. Werden beim Projekt-Bootstrap und in
einzelnen Phasen kopiert oder als Schema-Reference geladen.

| File | Phase | Funktion |
|------|-------|----------|
| `project-config-template.yaml` | 0 | Skopus-Konfiguration pro Projekt (Slug, Genre, Methoden, NCP-Pfad) |
| `intent-template.yaml` | 1 | Schema 1 — Genre, Audience, Konflikt, Methoden, Erfolgskriterium |
| `architecture-template.yaml` | 2 | Schema 2 — Storyform, Throughlines, Dynamics, NCP-Skeleton-Reference |
| `character-template.yaml` | 3 | Schema 3 — Players, Psycho-Modelle, Beziehungen |
| `scene-matrix-template.md` | 5 | 4-Akt × N-Kapitel × M-Szenen Hierarchie-Schablone |
| `chapter-draft-template.md` | 6 | Pre-Check-Liste + Prosa-Skeleton + Post-Check-Liste |
| `research-brief-template.md` | 4 | Brief für Übergabe an `research-prompt-optimizer` |
| `project-progress-template.md` | 0 | Progress-Datei für Projekt-Workspace |

## Verwendung

`scripts/bootstrap_project.sh` kopiert `project-config-template.yaml` und
`project-progress-template.md` in den Projekt-Workspace.

Andere Templates werden in den entsprechenden Phasen geladen, befüllt, und
ins Workspace geschrieben:

- Phase 1 schreibt `intent.yaml` (basiert auf `intent-template.yaml`)
- Phase 2 schreibt `architecture.yaml`
- Phase 3 schreibt `character-architecture.yaml`
- Phase 4 schreibt `research/briefs/<domain>.md` (pro Brief)
- Phase 5 schreibt `scene-matrix.md`
- Phase 6 schreibt `drafts/ch-XX.docx` oder `.md`

## Erweitern

Neue Templates: File in `assets/` anlegen + Phase-File referenzieren + diese
readme aktualisieren.
