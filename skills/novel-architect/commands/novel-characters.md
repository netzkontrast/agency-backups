# /novel-characters — Phase 3 Trigger

> **Phase:** 3 (Character Architecture)
> **/sc:-Analog:** `sc:brainstorm` + `sc:design`

## Zweck

Definiert Players (Charaktere) mit Psycho-Modellen, Throughline-Assignments,
Motivationen, Beziehungen. Persistiert in NCP `players[]` via `ncp-author`.

## Trigger

- „/novel-characters"
- „Charaktere definieren"
- „Players, Persönlichkeit, Beziehungen"

## Pre-Conditions

- `architecture.yaml` approved (Phase 2 done)
- NCP-Skeleton vorhanden

## Workflow

```
LOOP per character:
  askuser ≤3 slots:
    - character_name + narrative_role + throughline_assignment
    - psycho_model_primary + psycho_config (delegates to [→ novel-architect-character] for <model> schema on demand)
    - motivations + arc_direction

LOOP for relationships (nach allen Characters):
  askuser pairs: { target, kind, weight }

CONSOLIDATE:
  write character-architecture.yaml
  delegate ncp-author: add narratives[].subtext.players[]
  validate

APPROVE:
  show character-status-view.md
  askuser: Approve / Edit / Add / Remove
```

## Delegations

- `ncp-author` für `players[]` Update
- `dramatica-vocabulary` für Archetyp-Validation

## Output

- `character-architecture.yaml` (approved)
- NCP `narratives[].subtext.players[]` befüllt
- `character-status-view.md`

## Hand-off

→ Phase 4 (`/novel-research`) für World & Research,
oder direkt Phase 5 (`/novel-scenes`) wenn World schon klar

## Detail

- `phases/phase3-character-architecture.md`
- `assets/character-template.yaml`
- [`novel-architect-character/methods/`](../../novel-architect-character/methods/) (lazy-loaded per `psycho_model_primary` selection)
