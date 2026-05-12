---
name: novel-architect
description: >-
  Methodengetriebener Roman-Architektur-Orchestrator für literarische Langform
  (Roman, Novelle, Triptychon). Strukturiert die Roman-Entwicklung in 8 Phasen
  (Bootstrap, Intent, Narrative Architecture, Characters, World & Research,
  Scene Matrix, Drafting, Iteration) mit Hard Exit Gates, AskUserQuestion-Loops
  (≤3 Slots/Call) und NCP-State-Persistenz via ncp-author. Methoden-Bibliothek
  selektierbar pro Projekt (Charakter, Struktur, Konflikt, Research). Projekt-
  agnostisch — Workspaces leben unter /home/claude/novel-projects/<slug>/,
  niemals im Skill. Trigger: novel, roman, novella, narrative architecture,
  storyform, throughline, dramatica, scene matrix, chapter draft, /novel-start,
  /novel-design, /novel-characters, /novel-research, /novel-scenes, /novel-draft,
  /novel-reflect. Implizit bei Genre-Wahl, Plot-Struktur, Storyweaving. NICHT
  bei Agency-System-Tracks, Suno-Lyrics, generischer Prosa ohne Roman-Scope.
metadata:
  category: creative-writing
  source: user
  version: "1.1.1"
  status: active
  date_added: "2026-05-11"
  date_updated: "2026-05-12"
  predecessor: "novel-architect-legacy@0.3.3"
  state_management: "ncp"
  ncp_schema_version: "1.3.0"
  project_workspace_root: "/home/claude/novel-projects"
  project_workspace_root_env: "NOVEL_ARCHITECT_PROJECTS_ROOT"
  triggers: >-
    novel-architect, novel, roman, novella, narrative architecture, storyform,
    throughline, dramatica, scene matrix, chapter draft, character
    architecture, novel project, /novel-start, /novel-design, /novel-characters,
    /novel-research, /novel-scenes, /novel-draft, /novel-reflect, Roman planen,
    Roman strukturieren, Charakter-Architektur, Storyweaving, 40-Kapitel-Matrix
  delegates_to: >-
    novel-architect-character (Phase 3 methods), novel-architect-structure
    (Phase 2 + Phase 5 methods), novel-architect-world (Phase 4 methods),
    novel-architect-scene (Phase 5 + Phase 6 detail),
    dramatica-theory, dramatica-vocabulary, ncp-author,
    research-prompt-optimizer, skill-creator, memory-sync (optional)
  language_contract: "bilingual_de_en"
skill_bundles_tools:
  - tools/dramatica-nav
---

# novel-architect v1.1.1

Methodengetriebener Orchestrator für die Roman-Entwicklung. Strukturiert die
Arbeit an einem literarischen Langform-Projekt in **8 klare Phasen** mit Hard
Exit Gates, AskUserQuestion-Loops und NCP-State-Persistenz. Der Skill ist
**projekt-agnostisch** — alle projekt-spezifischen Daten leben im Projekt-
Workspace unter `/home/claude/novel-projects/<slug>/`, niemals im Skill selbst.

> **Vorgänger:** `novel-architect-legacy@0.3.3` (Kohärenz-Protokoll-spezifisch).
> Migration der Kohärenz-Protokoll-Daten siehe `scripts/bootstrap_project.sh`.

---

## Pipeline Overview

| Phase | Goal | Output | Implementation |
|-------|------|--------|----------------|
| **Phase 0 — Bootstrap** | Workspace setup, Projekt laden/erstellen | Workspace-Dir + `project-config.yaml` | `phases/phase0-bootstrap.md` |
| **Phase 1 — Intent Capture** | Genre, Audience, Konflikt-Frage, Methoden-Auswahl | `intent.yaml` (approved) | `phases/phase1-intent-capture.md` |
| **Phase 2 — Narrative Architecture** | 8-Step Storyform Worksheet → Throughlines, Classes, Dynamics, Story Points, Crucial Element, Signposts (3 Gates) | `architecture.yaml` + NCP Skeleton | `phases/phase2-narrative-architecture.md` + [`novel-architect-structure/methods/storyform/worksheet-loop.md`](../novel-architect-structure/methods/storyform/worksheet-loop.md) |
| **Phase 3 — Character Architecture** | Players, Psycho-Modelle, Beziehungen | `character-architecture.yaml` + NCP `players[]` | `phases/phase3-character-architecture.md` |
| **Phase 4 — World & Research** | Welt-Bibel, Recherche-Briefs | `world-bible.md`, `research/briefs/*.md` | `phases/phase4-world-research.md` |
| **Phase 5 — Scene & Chapter Matrix** | 40-Kapitel-Plan, Storybeats, Moments (3 Gates) | `scene-matrix.md` + NCP `storybeats[]`/`moments[]` | `phases/phase5-scene-matrix.md` |
| **Phase 6 — Drafting** | Per-Kapitel Prosa | `drafts/ch-XX.docx` (außerhalb NCP) | `phases/phase6-drafting.md` |
| **Phase 7 — Iteration (3-Mode)** | OQ-Resolution, Canon-Updates, Audits (generate/apply/audit) | Updates an NCP/canon-meta/learnings | `phases/phase7-iteration.md` |

**Hand-off Contract:** Strukturierte YAML zwischen Phasen (intent → architecture
→ character-architecture → scene-matrix) plus NCP-JSON als zentraler Storyform-
State. Kein Prosa-Hand-off, kein impliziter Kontext.

**File-First Principle:** Alle substantiellen Artefakte — Status-Views, Plan-
Views, Audit-Reports — werden via `render/io_helpers.py` geschrieben und über
`present_files` präsentiert. Chat trägt nur `ask_user_input_v0`-Prompts und
`present_files`-Calls.

---

## Sub-Module Architektur (v1.1.0)

Seit v1.1.0 ist die Methoden-Bibliothek in vier Sub-Skills aufgeteilt
(siehe [Task 071](../../tasks/071-novel-architect-submodule-refactor/task.md)).
Der Orchestrator (dieser Skill) hält das 8-Phasen-Pipeline + Projekt-Setup +
NCP-Integration; die Sub-Skills liefern die domänenspezifischen Methoden:

| Sub-Skill | Domäne | Phase(n) | Methods |
|-----------|--------|----------|---------|
| [`novel-architect-character`](../novel-architect-character/) | Charakter-Psychologie | Phase 3 | TSDP/IFS, Big Five, Enneagramm, Jung Archetypen |
| [`novel-architect-structure`](../novel-architect-structure/) | Plot-Struktur | Phase 2, 5 | 40-Chapter-Matrix, Hero's Journey, Save the Cat, Dramatica Quad |
| [`novel-architect-world`](../novel-architect-world/) | Welt & Recherche | Phase 4 | Domain-Mapping, Deep-Research-Briefs (delegation an `research-prompt-optimizer`) |
| [`novel-architect-scene`](../novel-architect-scene/) | Scene-Level Detail | Phase 5/6 | Q1–Q5 Scene-Level-Bridge Audit (Stub in v1.1.0; populiert via Task 075) |

**Cross-cutting Methoden** (Konflikt-Engines: Philosophy-as-Engine, Science-
as-Engine, Dual-Storyform) bleiben im Orchestrator unter
[`methods/conflict/`](./methods/conflict/), weil sie sowohl Throughline-
Architektur (Phase 2) als auch Charakter-Motivationen (Phase 3) prägen und
keinem einzelnen Sub-Skill zuzuordnen sind.

**Delegation-Pattern:** Wenn `/novel-characters`, `/novel-design`, `/novel-research`,
`/novel-scenes`, `/novel-draft` triggert, lädt der Skill-Loader **nur den Sub-Skill,
dessen Domäne gefragt ist** — der Orchestrator wird nicht eager mit allen 4
Sub-Skills geladen. Progressive Disclosure.

---

## Bilingual Contract (DE / EN)

> **PR #101 review §2.7 — codified by Task 070 Todo 6.**

Dieser Skill und seine Sub-Skills sind **bilingual** (Deutsch + Englisch).
Der Author-Workflow ist auf einen deutschsprachigen Roman optimiert
(Kohärenz-Protokoll als Erst-Projekt), während die governance-, API-, und
spec-orientierten Schichten englisch sind. **Beide Sprachen sind absichtlich
gemischt** — Contributoren und automatische "Normalizer" MÜSSEN diese
Trennung respektieren:

| Surface | Sprache | Beispiele |
|---|---|---|
| Body-Prose / Phase-Beschreibungen / askuser-Prompts | DE | "Approval gates analog research-prompt-optimizer Phase 2." |
| Frontmatter / Slot-Namen / Schema-Keys / Frontmatter-Werte | EN | `task_id`, `task_status`, `storyform_count`, `chapter_count_target` |
| Acceptance Criteria (Gherkin) | EN (RFC 2119 + Gherkin keywords) | `Given … When … Then … MUST …` |
| Anti-Pattern-Tabellen / Heuristik-Listen | DE (Body) + EN (Term-Anker) | "Skip askuser weil ‚Input feels clear'" |
| Tool/CLI Output, Error Messages | EN | `ERROR: slug must be kebab-case` |

**Regel:** Kein „Normalisieren" auf eine einzige Sprache ohne explizite
Eskalation an den Skill-Owner. Die DE/EN-Mischung ist Teil des
Kohärenz-Protokoll-Provenance und der Roman-Author-Erfahrung.

---

## Bootstrap-Protocol (FIRST ACTION jeder Session)

Wenn dieser Skill triggert, ist der erste Schritt — vor jeder inhaltlichen
Antwort — der Bootstrap. Anders als beim Legacy-Skill ist der Bootstrap
**parametrisiert über `project-config.yaml`**, nicht hardcoded.

### Bootstrap-Entscheidungsbaum

```
Skill triggert
   ↓
Existiert /home/claude/novel-projects/ ?
   ├── nein → mkdir + askuser: "Neues Projekt anlegen, bestehendes laden, Demo anlegen?"
   └── ja → ls /home/claude/novel-projects/
              ├── leer → askuser: "Neues Projekt anlegen?"
              ├── ein Projekt → askuser: "Dieses Projekt laden oder neues anlegen?"
              └── mehrere Projekte → askuser: project_slug auswählen
```

### Bootstrap-Schritte (Detail in `phases/phase0-bootstrap.md`)

1. **Workspace finden oder erstellen** unter `/home/claude/novel-projects/<slug>/`
2. **`project-config.yaml` laden oder schreiben** (siehe `assets/project-config-template.yaml`)
3. **Reference-Files lesen** (im Projekt-Workspace, nicht im Skill):
   - `progress.md` — Wo wurde aufgehört?
   - `intent.yaml` — Bisheriger Intent
   - `architecture.yaml` — Bisheriger Storyform
   - `<slug>.ncp.json` — Strukturelle Canon-Daten
   - `canon-meta.md` — Nicht-strukturelle Canon-Daten
   - `open-questions.md` — Blockierende OQs
   - `learnings.md` — Self-Improvement-Log
4. **Skill-interne Konsistenz prüfen** (drift zwischen Files)
5. **Pre-Action-Sanity-Check** — gegen resolved-OQs abgleichen, bevor Action läuft

### Migration vom Legacy-Skill

Wenn `project-config.yaml` fehlt aber Legacy-Daten in `skills/novel-architect-legacy/references/canon/` existieren, schlägt der Skill ein Migrations-Skript vor:

```bash
bash skills/novel-architect/scripts/bootstrap_project.sh kohaerenz-protokoll
```

Das erstellt `/home/claude/novel-projects/kohaerenz-protokoll/` mit den Legacy-Files (siehe `scripts/bootstrap_project.sh`).

---

## Phase 1 — Intent Capture (Loop until 100% clarity)

### Goal

Produziere ein `intent.yaml` File, das vollständig spezifiziert: Genre,
Audience, zentrales Thema, Konflikt-Frage, Skopus, Sprache, Methoden-Auswahl.
**Kein Slot darf ambiguous, missing oder geraten sein.**

### Intent Slot Set

| Slot | Required | One-line meaning |
|------|----------|------------------|
| `genre` | **yes** | Hard-SF, Fantasy, Literary, Horror, etc. |
| `subgenre_modifiers` | **yes** | „Philosophical Horror", „Cli-Fi", „Slipstream" |
| `audience` | **yes** | Leser-Typ + Vorbildung |
| `core_conflict_question` | **yes** | Die zentrale Frage des Romans (1-2 Sätze) |
| `core_conflict_unpacked` | **yes** | Was *gemeint* ist (Abgrenzung) |
| `length_target` | **yes** | `short_novel` / `standard` / `epic` |
| `language` | **yes** | `de` / `en` / `...` |
| `chapter_count_target` | **yes** | z.B. 39, 40, 24 |
| `methods_preference` | **yes** | Multi-select aus `methods/` (character/structure/conflict/research) |
| `dramatica_storyform_count` | **yes** | `single` / `dual` (parallel-encoded) |
| `philosophy_integration_level` | optional | `decoration` / `frame` / `engine` |
| `science_integration_level` | optional | `decoration` / `frame` / `engine` |
| `known_priors` | optional | Bestehende Roman-Ideen, Charaktere, Welt |
| `success_criterion` | **yes** | „Der Roman ist fertig, wenn ___" |

### Loop — Summary

**EXTRACT** (parse input, mark slot states) → **ASK** (file-first; write
status view, then `ask_user_input_v0` with ≤3 thematically-grouped slots; loop
until all required slots filled) → **CONFIRM** (write `intent.yaml` + final
status view, askuser approve/edit) → **EXIT** (only when approved=true).

### Hard Rules

- **3-question cap per askuser call.** 4+ open slots → next turn
- **Don't re-ask answered slots** unless user explicitly edits
- **Don't proceed on assumption.** 100% clarity bar
- **Surface contradictions** in status view
- **Scope creep guard:** Phase 1 = *was wird geschrieben*, nicht *wie strukturiert*

Vollständiger Algorithm + edge cases in `phases/phase1-intent-capture.md`.

---

## Phase 2 — Narrative Architecture (8-Step Worksheet-Loop, 3-Gate Approval)

### Goal

Produziere `architecture.yaml` + NCP-Skeleton in `<slug>.ncp.json` durch
das **8-Schritte-Storyform-Worksheet** aus `dramatica-theory`. Steps:
(0) Author's Intent — gelesen aus `intent.yaml`; (1) Four Throughlines
(OS/MC/IC/SS); (2) Class Assignment; (3) Character Dynamics (Resolve /
Growth / Approach / Mental Sex); (4) Plot Dynamics (Driver / Limit /
Outcome / Judgment); (5) Plot Story Points (static + driver + thematic);
(6) Crucial Element + dynamic-pair partner; (7) Signposts + Journeys
(4 + 3 per throughline); (8) optional Genre Mode; (V) Validation pass.

**3-Gate-Mapping** über die 8 Steps:
- **Gate 1** = Steps 0 + 1 (storyform shape + throughline names).
- **Gate 2** = Steps 2 + 3 + 4 + 5 (classes + 8 dynamics + story points).
- **Gate 3** = Steps 6 + 7 (+ 8) + Validation pass (crucial element +
  signposts + 5 hard checks).

### Sub-Phases

```
Phase 2.1   Load intent.yaml + select methods                                 (silent)
Phase 2.2   Step 0: read Author's Intent from intent.yaml                     (silent)
Phase 2.3   Step 1: name the 4 Throughlines (OS / MC / IC / SS)               (askuser)
            ──── GATE 1 (storyform shape + throughlines) ────                 (approve/edit)
Phase 2.4   Step 2: Class assignment (pair constraint enforced)               (askuser, quick-ref §1)
Phase 2.5   Step 3: Character Dynamics (4 binaries)                           (askuser, quick-ref §2-5)
Phase 2.6   Step 4: Plot Dynamics (4 binaries)                                (askuser, quick-ref §6-8)
Phase 2.7   Step 5: Plot Story Points (static + driver + thematic)            (1-2 askuser, quick-ref §9)
            ──── GATE 2 (classes + dynamics + storypoints) ────               (approve/edit)
Phase 2.8   Step 6: Crucial Element + dynamic-pair partner                    (askuser, quick-ref §10)
Phase 2.9   Step 7: Signposts + Journeys (4 per throughline)                  (askuser, nav.py Type-Quad)
Phase 2.10  Step 8 (optional): Genre Mode                                     (askuser ONLY on request)
Phase 2.11  Validation pass (5 hard checks: dynamic pairs, goal-level, …)     (silent — auto)
Phase 2.12  NCP Skeleton Write                                                (delegate ncp-author)
Phase 2.13  Render Architecture View                                          (file-first)
            ──── GATE 3 (final architecture) ────                             (approve/edit-step)
Phase 2.14  Write architecture.yaml (approved=true) + present_files
```

**Best:** 3 askuser turns. **Typical:** 5–8. **Cap:** 10 (HR.A4).

### Delegations (verbindlich)

- **`dramatica-theory`** für Storyform-Reasoning (Why this Class/Type?)
  und Validation (`00-storyform-validation.md`).
- **[`novel-architect-structure/assets/decision-heuristic-quick-ref.md`](../novel-architect-structure/assets/decision-heuristic-quick-ref.md)** —
  inline-quotable Heuristiken für Steps 2–7 askuser-Calls (HR.M2.3 /
  HR.P2.8: heuristic inline, not just linked).
- **[`novel-architect-structure/methods/storyform/worksheet-loop.md`](../novel-architect-structure/methods/storyform/worksheet-loop.md)** —
  operationale Walkthrough (per-step askuser shape, decision heuristic,
  recovery path, NCP slot map).
- **`dramatica-vocabulary`** für Dynamic-Pair-Validation, Type-Quad-Lookup
  (Signposts), Element-Quad-Lookup (Crucial Element).
- **`ncp-author`** für NCP-Skeleton-Erstellung (`narratives[].subtext.perspectives[]`,
  `dynamics[]`, `storypoints[]`, `storybeats[]`).
- **`tools/dramatica-nav/nav.py`** für Ontology-Lookups (AGENTS.md Rule **NO.2**).

Detail in [`phases/phase2-narrative-architecture.md`](./phases/phase2-narrative-architecture.md)
(gate-binding contract) + [`novel-architect-structure/methods/storyform/worksheet-loop.md`](../novel-architect-structure/methods/storyform/worksheet-loop.md)
(operational recipe).

---

## Phases 3-7 — Compact Overview

Für detaillierte Specs siehe `phases/phase{3..7}-*.md`. Hier nur der Überblick:

| Phase | Loop-Pattern | NCP-Slots befüllt | /sc:-Mapping |
|---|---|---|---|
| **3 — Character Architecture** | Per-Charakter-Slots (multi-select Psycho-Modelle) | `players[]`, `players[].motivations[]` | `sc:brainstorm`, `sc:design` |
| **4 — World & Research** | Domain-Selection + Delegation an research-prompt-optimizer | optional: `signposts[]` content updates | `sc:research`, `sc:document` |
| **5 — Scene Matrix** | 3-Gate-Loop (Akt → Kapitel → Szene) | `storybeats[]`, `moments[]` | `sc:workflow`, `sc:design` |
| **6 — Drafting** | Per-Kapitel mit Pre-Checks (NCP+canon-meta+OQ) | Prosa lebt **außerhalb** NCP (cross-ref via `moment.id`) | `sc:implement`, `sc:test` |
| **7 — Iteration (3-Mode)** | generate (Spec) / apply (Workflow-Empfehlung) / audit (Konsistenz-Check) | beliebige Updates basierend auf Resolution | `sc:reflect`, `sc:improve`, `sc:save` |

---

## NCP-Integration-Kontrakt

Detail in `references/ncp-integration-contract.md`. Kurzform:

- **Phase 2** schreibt `narratives[].subtext.perspectives[]`, `narratives[].subtext.dynamics[]`
- **Phase 3** schreibt `narratives[].subtext.players[]`, `players[].motivations[]`, `players[].perspectives[]`
- **Phase 4** optional: `signposts[]` content updates (nur wenn Forschung Canon ändert)
- **Phase 5** schreibt `narratives[].subtext.storypoints[]`, `narratives[].subtext.storybeats[]`, `narratives[].storytelling.moments[]`
- **Phase 6** keine NCP-Mutation (Prosa außerhalb)
- **Phase 7** beliebige Updates basierend auf Resolution

**Regel (AGENTS.md NO.2):** NCP-Mutation NUR via `ncp-author`. Dramatica-Slots
vorher über Ontology auflösen (`nav.py by-id` / `nav.py by-ncp`).

---

## /sc:-Command-Mapping

Detail in `references/sc-command-mapping.md`. Übersicht:

| Phase | Primär /sc: | Sekundär /sc: |
|---|---|---|
| 0 — Bootstrap | `sc:load` | `sc:index` |
| 1 — Intent | `sc:brainstorm` | `sc:business-panel` |
| 2 — Architecture | `sc:design` | `sc:analyze` |
| 3 — Characters | `sc:brainstorm` | `sc:design` |
| 4 — Research | `sc:research` | `sc:document` |
| 5 — Scenes | `sc:workflow` | `sc:design` |
| 6 — Drafting | `sc:implement` | `sc:test` |
| 7 — Iteration | `sc:reflect` | `sc:improve`, `sc:save` |

**Aufruf-Pattern:** Skill *empfiehlt* `/sc:`-Commands aktiv (im askuser oder
Status-View), erzwingt sie aber nicht. User kann jederzeit ohne `/sc:`-Wrapper
arbeiten.

---

## Iteration Discipline: Significance + Packaging

Detail-Heuristik in `references/significance-heuristics.md` (übernommen aus
Legacy, generalisiert).

### Was ist „signifikant" (= Checkpoint-Trigger)

Ein Checkpoint löst aus:
1. `progress.md` im Projekt-Workspace aktualisieren
2. **NCP-Update** falls strukturell: `<slug>.ncp.json` via `ncp-author`
3. **canon-meta.md aktualisieren** falls nicht-strukturell
4. **`learnings.md` Eintrag** (mandatorisch bei Session-End)
5. **memory-sync NUR** wenn User explizit Memory-Broadcast wünscht
6. **Skill packen** via `bash scripts/package_skill.sh`
7. `present_files` mit `.skill`-Datei + Output-Artefakt

### Checkpoint triggert wenn

- **Canon-Shift (strukturell)** — NCP-Mutation
- **Canon-Shift (nicht-strukturell)** — canon-meta.md Änderung
- **Phase-Unit complete** — Throughline encoded, Akt-Block gemapped, Chapter draft fertig
- **Workflow-Pivot** — User wechselt Phase
- **Volume threshold** — 3+ neue Files oder ~2000 Wörter
- **Session-End** — immer

### NICHT signifikant (kein Package)

- Term-Lookup in `dramatica-vocabulary`
- Q&A ohne Canon-Berührung
- Brainstorm ohne Festlegung
- Reference-Reading
- askuser-Antwort ohne approved-Slot-Setzung

`progress.md` darf bei jedem nicht-trivialen Schritt cheap-updated werden. Packen
passiert nur am Checkpoint.

---

## Constraints (nicht überschreibbar)

- **POV-Schutz:** Strukturelle/stilistische Signale im Draft erst bestätigen, dann ändern — Mosaikstruktur, unzuverlässige Erzähler, widersprüchliche Fußnoten sind *Risse, kein Stil-Mangel*.
- **Canon-Hierarchy:** **Projekt-Workspace-Files (NCP + canon-meta + open-questions + progress) > Memory > Training.** Bei Diskrepanz: Workspace-Files gewinnen.
- **NCP-Mutation NUR via ncp-author:** Direkte Hand-Edits an `.ncp.json` sind verboten — würden Schema-Drift erzeugen.
- **Dual-Storyform-Integrität:** Wenn `dramatica_storyform_count: dual` gewählt: Throughline-für-Throughline durch BEIDE narratives simultan, niemals A komplett vor B.
- **Story-First:** Wenn Theorie und Draft sich widersprechen, gewinnt der Draft. Theorie ist Diagnose, kein Rezept.
- **Memory ist Notiz, kein Maßstab:** Memory wird nur dann updated, wenn User es explizit verlangt.
- **AGENTS.md NO.2:** Dramatica-Slots müssen über Narrative Ontology aufgelöst werden, bevor sie in NCP geschrieben werden.

---

## Anti-Patterns

| Anti-Pattern | Why It Fails |
|---|---|
| Skip askuser weil „Input feels clear", oder 5+ Fragen in einem Batch | Loop-Design genau dagegen; `ask_user_input_v0` cap 3 |
| Edit a slot the user did not ask to edit | Bricht Approval-Contract |
| Phase überspringen oder Reihenfolge ignorieren | Hand-off-Kontrakt ist YAML-strukturiert; spätere Phasen brauchen früher entschiedene Slots |
| Direkter Hand-Edit der `.ncp.json` | Schema-Drift, NCP-Validator failed |
| Roman-Prosa in den Skill packen | Prosa lebt im Projekt-Workspace, niemals im Skill |
| Methoden-Module alle bei Bootstrap laden | Progressive Disclosure verletzt; lade on demand |
| `dramatica-theory` oder `dramatica-vocabulary` duplizieren | Delegation-Kontrakt verletzt; theorie/vocabulary leben dort, nicht hier |
| Memory automatisch updaten ohne User-Wunsch | Memory-Sync ist outward-only und explizit opt-in |
| Genre-spezifische Annahmen in den Skill hardcoden | Skill ist projekt-agnostisch; Genre kommt aus `intent.yaml` |
| Bootstrap überspringen weil „User-Input klar ist" | Workspace muss existieren; ohne `project-config.yaml` kein Phase-Routing |
| `dramatica_storyform_count: dual` ohne Begründung wählen | Dual verdoppelt Aufwand in Phase 2/3/5; nur bei explizit-gewünschter 5D-Interferenz |
| Storyform-Wahl ohne `dramatica-theory` consult | Verletzt AGENTS.md NO.2; freie Element-Namen erzeugen NCP-Schema-Drift |
| Asset-Templates als Reference statt Kopie nutzen | Templates sind Schablonen — beim Anlegen kopieren, nicht direkt referenzieren |

---

## Reference Files (Load on Demand)

| File | Load When | Purpose |
|------|-----------|---------|
| `phases/phase0-bootstrap.md` | Bootstrap edge cases | Workspace-Setup-Detail, Migration vom Legacy |
| `phases/phase1-intent-capture.md` | Phase 1 edge cases | Slot-to-question mapping, contradiction patterns |
| `phases/phase2-narrative-architecture.md` | Phase 2 | 3-Gate-Detail, Storyform-Decision-Tree |
| `phases/phase3-character-architecture.md` | Phase 3 | Per-Charakter-Slot-Set, Methoden-Auswahl |
| `phases/phase4-world-research.md` | Phase 4 | Domain-Mapping, Delegation an research-prompt-optimizer |
| `phases/phase5-scene-matrix.md` | Phase 5 | 3-Gate-Detail, Akt-Kapitel-Szenen-Hierarchie |
| `phases/phase6-drafting.md` | Phase 6 | Pre-Checks, Konsistenz-Checks |
| `phases/phase7-iteration.md` | Phase 7 | 3-Mode-Pattern (generate/apply/audit) |
| `../novel-architect-character/methods/*.md` | Phase 3, on demand | TSDP/IFS, Big Five, Enneagramm, Jung (Sub-Skill seit v1.1.0) |
| `../novel-architect-structure/methods/*.md` | Phase 2, 5, on demand | 40-Chapter-Matrix, Hero's Journey, Save-the-Cat, Dramatica-Quad (Sub-Skill seit v1.1.0) |
| `methods/conflict/*.md` | Phase 2, 3, on demand | Philosophy/Science-as-Engine, Dual-Storyform (cross-cutting; bleibt im Orchestrator) |
| `../novel-architect-world/methods/*.md` | Phase 4, on demand | Domain-Mapping, Deep-Research-Briefs (Sub-Skill seit v1.1.0) |
| `../novel-architect-scene/methods/*.md` | Phase 5/6 Detail | Q1–Q5 Scene-Level-Bridge Audit (Stub bis Task 075) |
| `assets/*-template.yaml` | Phase 1, 2, 3 | Schema-Templates |
| `assets/*-template.md` | Phase 5, 6 | MD-Templates (Scene-Matrix, Chapter-Draft) |
| `examples/*` | Reference | Worked Examples (nicht Kohärenz-spezifisch) |
| `render/io_helpers.py` | Phase 1, 2, 3, 5 file I/O | File-Writers, append-only revisions, status views |
| `render/render_intent.py` | Phase 1 | Intent YAML → Status-View MD |
| `render/render_architecture.py` | Phase 2 | Architecture YAML → NCP Skeleton + MD |
| `render/render_scene_matrix.py` | Phase 5 | Scene-Matrix → NCP storybeats + moments |
| `commands/novel-*.md` | Trigger-spezifisch | `/sc:`-kompatible Sub-Commands |
| `references/routing-matrix.md` | Bei Workflow-Verzweigung | Methodische Routing-Matrix |
| `references/ncp-integration-contract.md` | NCP-Edit-Frage | Welche NCP-Slots pro Phase befüllt werden |
| `references/sc-command-mapping.md` | /sc:-Aufruf-Frage | Phase → /sc:-Commands |
| `references/significance-heuristics.md` | Vor Checkpoint-Entscheidung | Detail-Heuristik (übernommen aus Legacy) |
| `references/learnings.md` | Bei Bootstrap + Session-End | Self-Improvement-Log (generisch) |
| `references/skill-improvement-todo.md` | Skill-Wartung | Skill-Lücken-Liste |
| `scripts/bootstrap_project.sh` | Erstmal-Migration | Erstellt Projekt-Workspace, optional Legacy-Migration |
| `scripts/package_skill.sh` | Checkpoint | Wrapper für skill-creator/package_skill.py |
| `scripts/convert_pdfplumber.py` | Archive-Material-Workflow | PDF→MD Fallback (übernommen aus Legacy) |

---

## Integration mit anderen Skills

| Skill | Relation | Wann |
|---|---|---|
| `dramatica-theory` | Input / Reference | Storyform-Arbeit, Akt-Diagnose (Phase 2, 5) |
| `dramatica-vocabulary` | Companion | Bei jeder Dramatica-Term-Berührung (Phase 2, 3, 5) |
| `ncp-author` | **State-Layer Owner** | Bei jeder strukturellen Canon-Mutation (Phase 2, 3, 5) — NICHT optional |
| `memory-sync` | Outward Broadcaster (optional) | Nur auf expliziten User-Wunsch (Phase 7) |
| `research-prompt-optimizer` | Upstream | Deep-Research-Prompts (Phase 4) |
| `skill-creator` | Self-update | Packaging dieses Skills (Checkpoint) |
| `spec-skill` | Optional | Formale Roman-Spec generieren (Phase 7 Mode: generate) |
| `suno-lyric-writer` | DELEGIERT NICHT | Album-Tracks haben eigenen Skill |
| `the-agency-system-architect` | DELEGIERT NICHT | Eigene Domäne |

---

## End-to-End Walk-Through

Ein User-Input wie *„Ich möchte einen Hard-SF Roman über Bewusstsein und KI schreiben"* läuft so:

1. **Phase 0** — Bootstrap: askuser ob neues Projekt; User wählt slug `consciousness-novel`
2. **Phase 1** — Intent: 3-Slot-askuser-Loops für Genre, Audience, Konflikt, Methoden; ergibt `intent.yaml`
3. **Phase 2** — Architecture: 3 Gates für Storyform (single/dual), Throughlines, Dynamics; ergibt `architecture.yaml` + NCP-Skeleton
4. **Phase 3** — Characters: Per-Charakter-Loop für Players (Protagonist + Antagonist + Influence); ergibt `character-architecture.yaml` + NCP `players[]`
5. **Phase 4** — Research: askuser welche Domänen (z.B. Kognitive Neurowissenschaft, KI-Ethik); delegate `research-prompt-optimizer`; ergibt `world-bible.md`
6. **Phase 5** — Scene Matrix: 3 Gates (Akt → Kapitel → Szene); ergibt `scene-matrix.md` + NCP `storybeats[]`+`moments[]`
7. **Phase 6** — Drafting: Per-Kapitel mit Pre-Checks; ergibt `drafts/ch-01.docx`
8. **Phase 7** — Iteration: kontinuierlich nach jedem Checkpoint; Audit-Reports bei Session-End

Typischerweise 15-25 askuser-Turns für komplette Phasen 0-2; Phasen 3-7 inkrementell über mehrere Sessions.

---

## Closing Note

Dieser Skill ist methoden-zentriert. Er strukturiert die Roman-Entwicklung,
schreibt aber **keine Prosa** — Drafting ist Phase 6, und auch da wird die
Prosa-Generierung an dramatica-vocabulary/Word-Processor-Tools delegiert. Der
Skill ist die **Source-of-Truth für die Methode**; der **Projekt-Workspace
ist die Source-of-Truth für die Inhalte**. Bei Diskrepanz: Workspace-Files
gewinnen, der Skill ist nur die Schablone.
