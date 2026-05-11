# Phase 1 — Intent Capture (Loop until 100% clarity)

> **Load when:** Phase 1 ist aktiv, Slot ist ambiguous, oder edge-case auftritt
> (contradiction, scope creep, mehrsprachig)

## §0 Goal

Produziere `intent.yaml` im Projekt-Workspace mit ALLEN required Slots gefüllt
und vom User approved. **Kein Slot darf ambiguous, missing oder geraten sein.**

## §1 Vollständiges Slot-Set

> **Derived view.** The canonical Phase 1 slot list lives in
> [`assets/intent-template.yaml`](../assets/intent-template.yaml) under
> `_meta._required` / `_meta._optional`. `render/render_intent.py` loads it
> at runtime; this table is a human-readable mirror. When you add or remove
> a slot, edit the template's `_meta` block first, then re-sync this table
> and bump the "Regenerated from intent-template.yaml on …" footer line below.
> Drift between the template and this table is a regression — Task 072
> (PR #101 review §2.5) consolidated three prior copies into one.

| Slot | Required | Type | Beispielwerte |
|---|---|---|---|
| `genre` | yes | single_select | hard_sf, fantasy, literary, horror, thriller, mystery, romance, historical, magical_realism |
| `subgenre_modifiers` | yes | free_text | "Philosophical Horror", "Cli-Fi", "Slipstream", "Cosmic Horror" |
| `audience` | yes | free_text | "Erwachsene mit Vorbildung in Philosophie", "Young Adult", "Literary Fiction Leser" |
| `core_conflict_question` | yes | free_text (1-2 Sätze) | "Kann ein fragmentiertes Bewusstsein authentisch sein?", "Was passiert wenn KI sich selbst korrigiert?" |
| `core_conflict_unpacked` | yes | free_text | Was ist NICHT gemeint? Abgrenzung zu Nachbar-Fragen |
| `length_target` | yes | single_select | `short_novel` (40-60k Wörter), `standard` (80-120k), `epic` (150k+) |
| `language` | yes | single_select | `de`, `en`, `fr`, `es`, ... |
| `chapter_count_target` | yes | integer | typisch: 24, 32, 39, 40, 50 |
| `methods_preference` | yes | multi_select | aus `methods/character/`, `methods/structure/`, `methods/conflict/`, `methods/research/` |
| `dramatica_storyform_count` | yes | single_select | `single` / `dual` (parallel-encoded) |
| `philosophy_integration_level` | optional | single_select | `decoration` (Zitate), `frame` (Charaktere diskutieren), `engine` (Konflikt ist philosophisch) |
| `science_integration_level` | optional | single_select | `decoration`, `frame`, `engine` |
| `known_priors` | optional | free_text | Bisherige Roman-Ideen, Charaktere, Welt |
| `success_criterion` | yes | free_text | "Der Roman ist fertig, wenn ___" |

> *Regenerated from `intent-template.yaml` on 2026-05-12 (Task 072).*

## §2 Loop-Pseudocode

```
EXTRACT:
  parse user input
  mark slot states: filled / partial / empty / contradicted
  detect signals (genre hints, audience hints)

LOOP until all required slots filled and approved:
  ASK:
    write intent-status-view.md (file-first)
    select up to 3 thematically-grouped open slots
    call ask_user_input_v0 with those slots
    
  EXTRACT_ANSWERS:
    parse user response
    update slot states
    if contradiction surface → flag in next status view

CONFIRM:
  write intent.yaml (Schema 1)
  write final intent-status-view.md
  call ask_user_input_v0:
    "intent.yaml fertig. Approve oder Edit?"
    options: ["Approve", "Edit X", "Edit Y", ...]

EXIT:
  on approve: mark approved=true in intent.yaml, present_files, → Phase 2
  on edit: loop back into ASK with edited slot
```

## §3 Slot-zu-Frage-Mapping (worked examples)

### §3.1 `genre` + `subgenre_modifiers`

> *„In welches Genre fällt dein Roman? Hast du spezifische Subgenre-Modifikatoren?"*
> Options: Hard-SF, Fantasy, Literary, Horror, Thriller, Mystery, Other (free text)

### §3.2 `core_conflict_question` + `core_conflict_unpacked`

> *„Was ist die zentrale Frage deines Romans? (1-2 Sätze, kein Genre-Cliché)"*
> Free text. Folgefrage: *„Was ist NICHT gemeint? Welche ähnliche Frage wäre dein Roman NICHT?"*

### §3.3 `methods_preference`

> *„Welche Methoden möchtest du einsetzen?"*
> Multi-select:
> - **Charakter:** TSDP-IFS, Big Five, Enneagramm, Jung-Archetypen
> - **Struktur:** 40-Kapitel-Matrix, Hero's Journey, Save-the-Cat, Dramatica-Quad
> - **Konflikt:** Philosophy-as-Engine, Science-as-Engine, Dual-Storyform
> - **Recherche:** Domain-Mapping, Deep-Research-Briefs

### §3.4 `dramatica_storyform_count`

> *„Single oder Dual Storyform? Dual heißt: zwei parallele Storyforms, die als 5D-Interferenz wirken (Kohärenz-Protokoll-Pattern)."*
> Options: Single (Standard), Dual (Advanced)

## §4 Hard Rules

- **3-question cap per askuser call.** 4+ open slots → next turn
- **Don't re-ask answered slots** unless user explicitly chose to edit
- **Don't proceed on assumption.** „100% clarity" ist der Contract
- **Surface contradictions.** Wenn Slot N Slot M widerspricht, beide in nächster status-view side-by-side; askuser resolved
- **Mobile-friendly.** `single_select` über enum slots; free-text nur wenn genuinely offen
- **Scope creep guard.** Phase 1 capturet *was wird geschrieben* + *welche Methoden zur Verfügung stehen* (Pre-Selektion). Die konkrete Storyform-Architektur, Throughline-Decisions und Scene-Strukturen gehören in Phase 2-5
- **Chat minimalism.** Keine Status-Announcements; status-view file ist der User-Window

## §5 Edge Cases

### §5.1 User gibt Plot oder Charaktere statt Konflikt

→ Surface in status-view: *„Du hast Plot/Charaktere gegeben. Phase 1 fragt nach der zentralen Frage. Wir kommen zu Plot in Phase 5, Charakteren in Phase 3."*
→ Ask: „Was ist die zentrale Frage hinter diesem Plot?"

### §5.2 Mehrere zentrale Fragen

→ Surface: *„Du nennst mehrere Fragen. Welche ist die zentrale? Die anderen werden Sub-Threads."*
→ Ask single_select.

### §5.3 Genre + Methoden inkompatibel

z.B. `genre: romance` + `methods_preference: dual_storyform`
→ Surface: *„Dual-Storyform passt selten zu Romance (eher zu Hard-SF/Philosophical Horror). Bist du sicher?"*
→ Ask: confirm or change methods

### §5.4 Sprache mehrdeutig

→ Default zu User-Konversationssprache, surface in status-view, askuser auf confirm

## §6 intent.yaml Schema 1

```yaml
schema_version: "1.0"
provenance:
  generated_by: novel-architect@1.0.0
  generated_at: <ISO-8601>
  project_slug: <slug>
intent:
  genre: <enum>
  subgenre_modifiers: <free_text>
  audience: <free_text>
  core_conflict_question: <free_text>
  core_conflict_unpacked: <free_text>
  length_target: <enum>
  language: <enum>
  chapter_count_target: <int>
  methods_preference:
    character: [<list>]
    structure: [<list>]
    conflict: [<list>]
    research: [<list>]
  dramatica_storyform_count: <enum>
  philosophy_integration_level: <enum|null>
  science_integration_level: <enum|null>
  known_priors: <free_text|null>
  success_criterion: <free_text>
approved: false  # → true bei EXIT
revisions: []    # append-only via io_helpers.append_revision()
```

## §7 Exit Gate

Phase 1 ist done, wenn:
- Alle required Slots gefüllt
- `intent.yaml` mit `approved: true` geschrieben
- `intent-status-view.md` final geschrieben
- `present_files` aufgerufen auf intent.yaml + status-view

→ Übergang zu Phase 2 (Narrative Architecture)

## §8 /sc:-Mapping

| Schritt | /sc: Command |
|---|---|
| Konflikt-Frage finden | `sc:brainstorm` |
| Audience-Analyse | `sc:business-panel` |
| Genre-Validation | `sc:analyze` |
| Methoden-Empfehlung | `sc:recommend` |
