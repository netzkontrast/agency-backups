# /sc:-Command Mapping (v1.0)

> **Load when:** /sc:-Aufruf-Frage, oder User fragt „welcher Command für X"

## §0 Konzept

`/sc:`-Commands sind SuperClaude-Workflows (Skills im Agency-Repo). Der
`novel-architect` *empfiehlt* sie pro Phase aktiv, *erzwingt* sie aber nicht.
User kann jederzeit ohne `/sc:` arbeiten.

## §1 Phase-zu-Command Mapping

| Phase | Primär /sc: | Sekundär /sc: | Wann |
|-------|------------|---------------|------|
| 0 — Bootstrap | `sc:load` | `sc:index` | Projekt laden, Übersicht |
| 1 — Intent Capture | `sc:brainstorm` | `sc:business-panel` | Konflikt-Frage, Audience |
| 2 — Architecture | `sc:design` | `sc:analyze` | Storyform, Throughline-Design |
| 3 — Character Architecture | `sc:brainstorm` | `sc:design` | Charakter-Tiefe, Beziehungs-Design |
| 4 — World & Research | `sc:research` | `sc:document` | Deep Research, World-Bible |
| 5 — Scene Matrix | `sc:workflow` | `sc:design` | Akt-Struktur, Scene-Detail |
| 6 — Drafting | `sc:implement` | `sc:test` | Drafting, Konsistenz-Tests |
| 7 — Iteration | `sc:reflect` | `sc:improve`, `sc:save`, `sc:analyze` | OQ, Audit, Save |

## §2 Aufruf-Pattern

Der `novel-architect` empfiehlt `/sc:`-Commands in zwei Kontexten:

### §2.1 Im askuser

```
ask_user_input_v0:
  question: "Phase 1: Konflikt-Frage finden. /sc:brainstorm für tiefere Exploration?"
  options:
    - "Ja, /sc:brainstorm starten"
    - "Nein, direkt antworten"
```

### §2.2 Im Status-View

```markdown
## Status — Phase 2 (Architecture)

Aktueller Schritt: Throughline-Assignment

**Empfehlung:** /sc:design für strukturierte Storyform-Skizze
```

## §3 Spezifische Use-Cases

### §3.1 `sc:brainstorm` (Phasen 1, 3)

Für offene Exploration. Gut bei:
- „Was könnte mein Konflikt sein?"
- „Welche Charakter-Beziehungen sind interessant?"
- „Welche Motivationen passen zu Big-Five OCEAN-Profil X?"

### §3.2 `sc:design` (Phasen 2, 3, 5)

Für strukturierte Architektur. Gut bei:
- „Wie wähle ich Throughlines?"
- „Wie sieht meine Akt-Struktur aus?"
- „Charakter-Beziehungs-Diagramm"

### §3.3 `sc:research` (Phase 4)

Delegiert intern an `research-prompt-optimizer` Skill. Gut bei:
- „Recherche zu Domain X starten"
- „Brief an Deep Research geben"

### §3.4 `sc:workflow` (Phase 5)

Für Workflow-Strukturierung. Gut bei:
- „Plot-Outline für Akt I"
- „Kapitel-Sequenz mit Wendepunkten"

### §3.5 `sc:implement` (Phase 6)

Für Drafting. Gut bei:
- „Kapitel X drafts"
- „Szene Y schreiben mit POV Kael"

### §3.6 `sc:test` (Phase 6)

Für Konsistenz-Checks. Gut bei:
- „Konsistenz dieses Drafts mit canon-meta.md"
- „Character-Architecture vs. Verhalten in Kapitel X"

### §3.7 `sc:reflect` (Phase 7)

Für Self-Improvement. Gut bei:
- „Was lief in dieser Session suboptimal?"
- „Welche Methoden waren effektiv?"

### §3.8 `sc:improve` (Phase 7)

Für Skill-Iteration. Gut bei:
- „Refactor SKILL.md basierend auf Session-Insights"
- „learnings.md → SKILL.md anpassen"

### §3.9 `sc:save` / `sc:load` (Phase 0, 7)

Session-Persistenz.

### §3.10 `sc:analyze` (Phase 7 audit mode)

Für Konsistenz-Audits. Gut bei:
- „Audit: Stimmt scene-matrix mit NCP storybeats?"
- „Konsistenz aller Workspace-Files"

## §4 Hard Rules

- **`/sc:`-Commands sind nie obligatorisch** — Skill funktioniert ohne sie
- **Empfehlung erfolgt im Kontext** — nicht generisch im Bootstrap
- **Bei Trigger ohne Kontext** — z.B. nur „/sc:design" — askuser welche Phase

## §5 Anti-Patterns

- `/sc:`-Commands eigenständig aufrufen ohne Phase-Kontext — User verliert Orientierung
- Mehrere `/sc:`-Commands parallel empfehlen — überwältigend
- `/sc:implement` für nicht-Drafting nutzen — semantisch falsch
