---
type: readme
status: active
slug: novel-architect-readme
summary: Index for novel-architect@1.0.0 skill — methodengetriebene Roman-Architektur mit 8 Phasen, NCP-Integration, /sc:-Mapping
created: 2026-05-11
updated: 2026-05-11
---

# novel-architect (v1.0.0)

## What

Methodengetriebener Roman-Architektur-Orchestrator. Strukturiert die Entwicklung
literarischer Langform (Roman, Novelle, Triptychon) in **8 klare Phasen** mit
Hard Exit Gates, AskUserQuestion-Loops (≤3 Slots pro Call), File-First-Prinzip
und progressivem Reference-Loading. State-Management über **NCP** (Narrative
Context Protocol v1.3.0) via `ncp-author`. **Projekt-agnostisch** — alle
projekt-spezifischen Daten leben unter `/home/claude/novel-projects/<slug>/`,
niemals im Skill.

**Vorgänger:** `novel-architect-legacy@0.3.3` (Kohärenz-Protokoll-spezifisch,
deprecated). Migration via `scripts/bootstrap_project.sh kohaerenz-protokoll`.

## Why here

Skill lebt in `/home/user/agency/skills/` und wird per Agency-Governance
gepflegt (L1+L2 Frontmatter, `tools/fm/edit.py`, Pre-Commit-Hooks). Andere
Agents (Claude Code, Jules, gemini-cli) können hier audit-en und via PR
vorschlagen.

## Top-level Navigation

| File / Dir | Inhalt |
|------------|--------|
| [SKILL.md](./SKILL.md) | Pipeline-Übersicht, Frontmatter, Anti-Patterns, Reference-Index |
| [phases/](./phases/) | 8 Phase-Detail-Files (Bootstrap → Iteration) |
| [methods/](./methods/) | Selektierbare Methoden-Bibliothek (character/structure/conflict/research) |
| [assets/](./assets/) | Template-Files (YAML + Markdown) |
| [examples/](./examples/) | Worked Examples (projekt-agnostic) |
| [render/](./render/) | Python-Helpers (io_helpers, render_intent, etc.) |
| [commands/](./commands/) | /sc:-kompatible Sub-Commands (novel-start, novel-design, etc.) |
| [references/](./references/) | Routing, NCP-Contract, /sc:-Mapping, Learnings, Significance |
| [scripts/](./scripts/) | Bootstrap-Skript, Package-Skript, Utilities |

## Quick Start

1. Trigger den Skill (Phrasen wie „starte Roman", „neue Novelle", „/novel-start")
2. **Phase 0** lädt oder erstellt Projekt-Workspace unter `/home/claude/novel-projects/<slug>/`
3. **Phase 1** capturet Intent (Genre, Audience, Konflikt) via AskUserQuestion-Loop
4. **Phase 2** baut Storyform-Architektur (Dramatica) mit 3 Approval-Gates
5. **Phase 3-7** entwickeln Charaktere, Welt/Recherche, Scene Matrix, Drafts, Iteration

Detail in [SKILL.md](./SKILL.md).

## Migration vom Legacy

Wenn du das Kohärenz-Protokoll-Projekt aus `novel-architect-legacy/` migrieren willst:

```bash
bash /home/user/agency/skills/novel-architect/scripts/bootstrap_project.sh kohaerenz-protokoll
```

Erstellt `/home/claude/novel-projects/kohaerenz-protokoll/` mit allen Legacy-Files
und einer initialisierten `project-config.yaml`.

## Assumptions Log

- Skill-interne Subfolders (`phases/`, `methods/`, etc.) bekommen jetzt eigene
  `readme.md` für Progressive-Disclosure-Klarheit. Dies weicht von der älteren
  v0.3.3 ab, wo subfolders keine eigenen Readmes hatten — Rationale: in v1.0.0
  ist Skill modular genug, dass Subfolders eigene Navigation rechtfertigen.
- `name` und `description` aus SKILL.md Frontmatter sind die Quelle der Wahrheit;
  dieses readme.md drifted bei Inkonsistenz und muss reconciliert werden.
- Projekt-spezifische Daten (NCP, canon-meta, progress) leben NICHT im Skill,
  sondern unter `/home/claude/novel-projects/<slug>/`. Dies weicht von v0.3.3 ab,
  wo `references/canon/` projekt-spezifische Daten enthielt.
