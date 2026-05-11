# Commands

Slash-Command-Kompatible Sub-Commands für die Phasen. Triggert die
entsprechende Phase im Skill.

| Command | Phase | /sc:-Analog |
|---------|-------|-------------|
| `/novel-start` | 0 + 1 (Bootstrap + Intent) | `sc:brainstorm` |
| `/novel-design` | 2 (Narrative Architecture) | `sc:design` |
| `/novel-characters` | 3 (Character Architecture) | `sc:brainstorm` + `sc:design` |
| `/novel-research` | 4 (World & Research) | `sc:research` (delegiert intern an research-prompt-optimizer) |
| `/novel-scenes` | 5 (Scene Matrix) | `sc:workflow` |
| `/novel-draft` | 6 (Drafting) | `sc:implement` |
| `/novel-reflect` | 7 (Iteration, 3-Mode) | `sc:reflect`, `sc:improve`, `sc:analyze` |

## Pre-Conditions

Jeder Command prüft Pre-Conditions (vorherige Phase done?). Bei Fehler:
askuser für Pivot oder vorherige Phase.

## Detail-Files

Volle Phase-Specs in `phases/phase{0..7}-*.md`.
