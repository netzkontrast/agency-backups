# Phase 3 — Character Architecture

> **Load when:** Phase 3 ist aktiv, oder Edge-Case bei Psycho-Modell-Auswahl
> oder Player-zu-Throughline Assignment

## §0 Goal

Produziere `character-architecture.yaml` + NCP `players[]` Update. Pro Charakter:
narrative role, throughline assignment, psycho-model config, motivations,
arc direction, relationships.

## §1 Input / Output

**Input:** `architecture.yaml` (approved) + `intent.yaml` (`methods_preference.character`)

**Output:**
- `character-architecture.yaml`
- NCP `narratives[].subtext.players[]` (via `ncp-author`)
- `character-status-view.md`

## §2 Per-Character Slot Set (≤3 askuser pro Charakter)

| Slot | Required | Type | Beispiele |
|---|---|---|---|
| `character_name` | yes | free_text | "Kael", "Sarah", "Detective Morrison" |
| `narrative_role` | yes | single_select | Protagonist / Antagonist / Guardian / Contagonist / Reason / Emotion / Sidekick / Skeptic |
| `throughline_assignment` | yes | single_select per storyform | MC / IC / OS_member / SS_member |
| `psycho_model_primary` | yes | single_select | tsdp-ifs / big-five / enneagramm / jung-archetypes |
| `psycho_config` | yes | structured | hängt vom Modell ab — siehe `[→ novel-architect-character]` für `<model>` Schema |
| `motivations` | yes | list[free_text] | "Wahrheit finden", "System zerstören", "Bewusstsein integrieren" |
| `arc_direction` | yes | single_select per storyform | Change / Steadfast |
| `relationships` | optional | list[struct] | { target: char_id, kind: enum, weight: enum } |

## §3 Loop-Pseudocode

```
LOOP per character:
  ASK (≤3 slots from above):
    - character_name + narrative_role + throughline_assignment
    - psycho_model_primary + psycho_config (ask [→ novel-architect-character] for <model> schema via psycho_model_primary selection)
    - motivations + arc_direction
    
LOOP for relationships (after all characters defined):
  ASK pairs: { target, kind, weight }
  
CONSOLIDATE:
  write character-architecture.yaml
  delegate ncp-author: write narratives[].subtext.players[]
  validate via ncp-author scripts/validate.js
  
APPROVE:
  show character-status-view.md
  askuser: Approve / Edit <char> / Add character / Remove character
```

## §4 Methoden-Module (Sub-Skill-owned; load on demand)

Beim Auswählen des `psycho_model_primary` delegiert der Orchestrator an
`[→ novel-architect-character]`. Die vier verfügbaren Modelle und ihre
phase-level Slot-Konturen (Details und Schema im Sub-Skill):

- **`tsdp-ifs`** — Tertiäre Strukturelle Dissoziation + Internal Family Systems
  - Slots: alters[] mit role/function/somatic
  - Beispiel: Kael (Host/ANP), Lex (analytisch/EP), Kiko (kindlich/EP)
- **`big-five`** — OCEAN
  - Slots: openness, conscientiousness, extraversion, agreeableness, neuroticism (0-100)
- **`enneagramm`** — 9 Typen
  - Slots: type (1-9), wing, integration_path, disintegration_path
- **`jung-archetypes`** — Archetypen
  - Slots: archetypes[] (Shadow, Anima/Animus, etc.), individuation_stage

Schema-Definition + askuser-Detail-Loops leben im Sub-Skill: siehe
[`novel-architect-character/methods/`](../../novel-architect-character/methods/).

## §5 NCP-Player-Workflow (delegated to ncp-author)

Phase 3 ruft `ncp-author` auf pro Charakter:

1. **Input:** Character entry aus `character-architecture.yaml`
2. **Operation:** Add player to `narratives[X].subtext.players[]`
3. **Required NCP fields:**
   - `id` (kebab-case from name)
   - `character_name`
   - `archetype` (Dramatica enum)
   - `perspectives[]` (Throughline-Assignments)
   - `motivations[]` (mapped to NCP narrative_functions)
4. **Validation:** `node skills/ncp-author/scripts/validate.js canon/<slug>.ncp.json`

## §6 Hard Rules

- **Players werden pro narrative gespiegelt** bei dual storyform — ein Charakter kann unterschiedliche Rollen in A vs. B haben
- **NCP-Mutation NUR via ncp-author**
- **Psycho-Model schemas owned by `[→ novel-architect-character]`, nicht inline** — Progressive Disclosure; load via `psycho_model_primary` selection
- **Relationships werden NACH allen Charakteren definiert** — sonst zirkuläre Refs
- **Mindestens MC + IC sind erforderlich** bei single storyform; bei dual: MC+IC per narrative
- **MC ist NICHT zwingend Protagonist** — siehe `dramatica-theory` Reference

## §7 Edge Cases

### §7.1 Charakter passt in keine Dramatica-Rolle

→ Surface: *„<Name> hat keine klare Dramatica-Rolle. Sub-Story-Character? Outside Story Mind?"*
→ Optionen: Skip / Force-fit to Skeptic/Sidekick / Re-think OS

### §7.2 TSDP wird gewählt für nicht-fragmentierten Protagonisten

→ Surface: *„TSDP modelliert Dissoziation. Sicher? Big Five passt eher für integrierte Persönlichkeiten."*
→ Confirm or change

### §7.3 Mehrere MCs (Ensemble-Cast)

→ Dramatica erlaubt strictly nur EINEN MC pro storyform
→ Bei dual storyform: 2 MCs (einer pro narrative) ist OK
→ Bei Ensemble: surface „Welcher ist Storymind-MC?"

## §8 character-architecture.yaml

Siehe `assets/character-template.yaml` für vollständige Schema.

## §9 Exit Gate

Phase 3 ist done, wenn:
- Alle erforderlichen Charaktere in `character-architecture.yaml`
- NCP `players[]` befüllt, validation passed
- `approved: true` in yaml
- `character-status-view.md` final

→ Übergang zu Phase 4 (World & Research)

## §10 /sc:-Mapping

| Schritt | /sc: Command |
|---|---|
| Charakter-Tiefe | `sc:brainstorm` |
| Beziehungs-Netzwerk | `sc:design` |
| Psycho-Modell-Auswahl | `sc:recommend` |
