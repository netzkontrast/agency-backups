# Phases

Pipeline-Detail-Files für die 8 Roman-Entwicklungs-Phasen. Progressive
Disclosure — diese Files werden NUR geladen, wenn die entsprechende Phase
aktiv ist oder ein Edge-Case auftritt.

| File | Phase | Load When |
|------|-------|-----------|
| `phase0-bootstrap.md` | 0 — Bootstrap | Skill triggert + Workspace fehlt / askuser für Projekt |
| `phase1-intent-capture.md` | 1 — Intent Capture | Phase 1 aktiv, oder Slot-Edge-Case |
| `phase2-narrative-architecture.md` | 2 — Narrative Architecture | Phase 2 aktiv, oder Storyform-Edge-Case |
| `phase3-character-architecture.md` | 3 — Character Architecture | Phase 3 aktiv, oder Psycho-Model-Frage |
| `phase4-world-research.md` | 4 — World & Research | Phase 4 aktiv, oder Domain-Wahl |
| `phase5-scene-matrix.md` | 5 — Scene Matrix | Phase 5 aktiv, oder Akt-Struktur-Frage |
| `phase6-drafting.md` | 6 — Drafting | Phase 6 aktiv, oder per-Kapitel Drafting |
| `phase7-iteration.md` | 7 — Iteration (3-Mode) | Continuous, OQ-Resolution, Canon-Update, Session-End |

Alle Phasen folgen dem Pattern: Goal → Input/Output → Sub-Phases mit Gates →
Hard Rules → Edge Cases → Exit Gate → /sc:-Mapping.
