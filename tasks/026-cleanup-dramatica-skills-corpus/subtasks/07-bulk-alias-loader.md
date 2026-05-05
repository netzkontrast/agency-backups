---
type: note
status: draft
slug: task-026-st7-bulk-alias-loader
summary: "Subtask ST-7: ship tools/dramatica-nav/aliases.py — parse skills/dramatica-vocabulary/references/_synonym-lookup.md (~512 alias rows) into aliases_en across the ontology, plus a hand-curated DE starter set for ~50 high-frequency terms (Hauptfigur, Vertrauen, Wandel, Wendepunkt, Akt, etc.)."
created: 2026-05-05
updated: 2026-05-05
subtask_id: "ST-7"
subtask_phase: "B"
subtask_recommended_agent: "python-expert"
subtask_depends_on: []
subtask_falsification: "Wrong cut iff the synonym-lookup contains alias entries that conflict with already-distinct ontology IDs. Mitigated by a conflict-report dry-run pass; only conflict-free aliases are committed."
---

# ST-7: `aliases.py` — Bulk Alias Loader

## Goal

Two coupled deliverables:

1. **`tools/dramatica-nav/aliases.py`** — a CLI that parses `skills/dramatica-vocabulary/references/_synonym-lookup.md` (which carries ~512 EN-locale alias-to-canonical mappings per [Task 015 §Inventory](../../015-integrate-dramatica-ncp-skills/notes.md)) and projects those mappings into `aliases_en` arrays across `ontology.json` and per-term frontmatter blocks.

   CLI surface:
   ```text
   tools/dramatica-nav/aliases.py load-en --source <path>     # bulk-load from synonym-lookup.md
   tools/dramatica-nav/aliases.py add --id <oid> --locale <l> --value "<alias>"
   tools/dramatica-nav/aliases.py remove --id <oid> --locale <l> --value "<alias>"
   tools/dramatica-nav/aliases.py list --id <oid> [--locale <l>]
   tools/dramatica-nav/aliases.py conflict-report           # report aliases that map to multiple ontology IDs
   ```

   `load-en` operates in three passes:
   - **Pass 1: parse.** Walk `_synonym-lookup.md`'s 23 alphabetical-bucket sections; extract `<alias> → <canonical-term>` rows.
   - **Pass 2: resolve.** Map each canonical-term to its ontology ID. If multiple IDs match (same term name across kinds), surface as a conflict; do NOT auto-resolve.
   - **Pass 3: project.** For each conflict-free mapping, append to the entry's `aliases_en` array (in BOTH the ontology table AND the per-term frontmatter block). Idempotent: re-running the load is a no-op if frontmatter is already up-to-date.

2. **DE-locale starter set: `tools/dramatica-nav/data/aliases_de_starter.json`** — a hand-curated JSON listing ~50 high-frequency German aliases for the canonical Dramatica terms a German-speaking author (per the `dramatica-vocabulary` SKILL.md German-primary persona) is likely to query. Suggested seed list (ST-7's brief locks the IDs but the agent picks the German renderings from canonical Dramatica DE community sources):

   - `throughline.main` → `Hauptfigur`
   - `throughline.influence` → `Einflussfigur`, `Impact-Figur`
   - `el.trust` → `Vertrauen`
   - `el.test` → `Prüfung`
   - `el.control` → `Kontrolle`
   - `el.uncontrolled` → `Unkontrolliert`
   - `el.logic` → `Logik`
   - `el.feeling` → `Gefühl`
   - `character-dynamic.problem-solving-style` → `Problemlösungsstil`
   - `character-dynamic.resolve` → `Wandel-Entscheidung`
   - … (continue to ~50 entries; coverage should hit at least all 8 archetypes, all 4 throughlines, all 4 character-dynamics, and the ~30 most-cross-referenced elements/variations)

   `aliases.py load-de --source <path>` consumes this JSON and projects per the same three-pass protocol as `load-en`.

## Falsification

Wrong cut **iff** the synonym-lookup contains alias entries that conflict with already-distinct ontology IDs (e.g., the alias "Resolve" mapping ambiguously to both `character-dynamic.resolve` AND `el.solution`). Mitigation: ST-7's `conflict-report` subcommand emits the full conflict set FIRST. The agent reviews; only conflict-free aliases are auto-loaded. Conflicts are filed as Bucket-D-style entries in [`notes.md`](../notes.md) for Task 027 to ratify.

## Inputs

- `skills/dramatica-vocabulary/references/_synonym-lookup.md` — the 512-row source.
- `maintenance/schemas/narrative-ontology/ontology.json` — write surface.
- `skills/dramatica-vocabulary/references/*.md` — write surface for per-term frontmatter blocks.
- `tools/dramatica-nav/lib/ontology.py` — reuse load/index helpers.
- `maintenance/schemas/narrative-ontology/term-frontmatter.schema.json` — `aliases_<locale>` patternProperties contract.

## Acceptance Criteria

1. **CLI complete.** Five subcommands work as documented.
2. **`load-en` smoke-passes.** Running `aliases.py load-en --source skills/dramatica-vocabulary/references/_synonym-lookup.md` projects ≥250 aliases into `ontology.json` (the conflict-free subset of 512). Running it again produces no diff.
3. **`load-de` smoke-passes.** Running `aliases.py load-de --source tools/dramatica-nav/data/aliases_de_starter.json` projects ~50 DE aliases. Running it again produces no diff.
4. **Conflict report emitted.** `tasks/026-cleanup-dramatica-skills-corpus/notes.md §8` (a new section) lists every conflict the run found.
5. **Validator clean.** `validate.py` reports 0 alias-uniqueness violations after both loads.
6. **Tests.** `tools/dramatica-nav/tests/test_aliases.py` covers parse / resolve / project / idempotency / conflict-report (≥6 tests).
7. **Single commit.** Title: `feat(dramatica-nav): aliases.py — bulk EN loader + DE starter set (Task 026 ST-7)`. Body lists the project counts (EN: ≥250, DE: ~50) and the conflict count.

## Dependencies

None. Phase B (parallel with ST-5 and ST-6).

## Estimated Effort

Medium (~200 LOC tool + ~100 LOC tests + ~50 hand-curated DE entries).

## Agent Prompt

```text
You are implementing ST-7 of Task 026 (cleanup-dramatica-skills-corpus) for
the netzkontrast/agency repo on branch claude/cleanup-dramatica-skills-1cEOO.

This subtask runs in worktree isolation.

Repo root: /home/user/agency
Working directory: /home/user/agency

Context files (read first):
  - tasks/026-cleanup-dramatica-skills-corpus/task.md
  - tasks/026-cleanup-dramatica-skills-corpus/subtasks/07-bulk-alias-loader.md (this file)
  - skills/dramatica-vocabulary/references/_synonym-lookup.md (the 512-row source)
  - skills/dramatica-vocabulary/SKILL.md (the German-primary persona context)
  - tools/dramatica-nav/lib/ontology.py (reuse helpers)
  - maintenance/schemas/narrative-ontology/term-frontmatter.schema.json
    (aliases_<locale> patternProperties contract)
  - maintenance/schemas/narrative-ontology/ontology.json

Goal:
  Ship tools/dramatica-nav/aliases.py with five subcommands. Project ~250+
  conflict-free EN aliases from _synonym-lookup.md into the ontology.
  Hand-curate a ~50-entry DE starter set in
  tools/dramatica-nav/data/aliases_de_starter.json.

Acceptance criteria (reproduce verbatim from this file's Acceptance Criteria
section). All seven must be true.

Implementation approach:
  1. Implement the parser for _synonym-lookup.md. The file uses 23
     alphabetical-bucket sections; format is `<alias> → <canonical>`
     bullet lines. Be tolerant of formatting variants (em-dash vs.
     arrow, parenthetical context).
  2. Implement resolve: alias → ontology ID via canonical-label match.
     If a canonical-label appears on multiple kinds (e.g. "Resolve" as
     character-dynamic AND as a concept), the lookup is ambiguous —
     surface as a conflict, NEVER pick one.
  3. Implement project: append to aliases_en (table + frontmatter).
     Schema-validate after each entry write.
  4. For load-de, hand-curate the JSON starter set per the seed list
     suggestions. Coverage targets: all 8 archetypes, all 4 throughlines,
     all 4 character-dynamics, ≥30 elements/variations.
  5. Idempotency check: re-run load-en; expect zero diff.
  6. conflict-report subcommand emits the conflicts to stdout (and
     returns exit 0 if zero, exit 1 if non-zero — for CI consumption).
  7. Author tests/test_aliases.py per Acceptance §6.
  8. Append the conflict list to notes.md §8 (create the section).
  9. Commit one focused commit; do NOT push.

Constraints:
  - Python 3.11 stdlib + jsonschema only.
  - DO NOT auto-resolve conflicts. Surface them; let a human or Task 027
    ADR decide.
  - DO NOT add aliases beyond what _synonym-lookup.md provides (for EN)
    or your hand-curated DE starter set. Out-of-source additions are
    forbidden in this subtask.
  - DO NOT touch _synonym-lookup.md itself.
  - Schema validation MUST be on every write. A schema-violating alias is
    a hard failure (exit 1, no partial commit).

When done:
  - pytest tools/dramatica-nav/tests/                                          (must pass)
  - python3 tools/dramatica-nav/aliases.py load-en \
      --source skills/dramatica-vocabulary/references/_synonym-lookup.md      (must succeed)
  - python3 tools/dramatica-nav/aliases.py load-de \
      --source tools/dramatica-nav/data/aliases_de_starter.json                (must succeed)
  - python3 tools/dramatica-nav/aliases.py conflict-report                     (must exit 0 if all conflicts moved to notes.md)
  - python3 tools/dramatica-nav/nav.py by-alias 'Vertrauen' --lang de          (must return el.trust)
  - python3 tools/dramatica-nav/validate.py                                    (must exit 0)
  - Commit "feat(dramatica-nav): aliases.py — bulk EN loader + DE starter set (Task 026 ST-7)"
  - Do NOT push.
```
