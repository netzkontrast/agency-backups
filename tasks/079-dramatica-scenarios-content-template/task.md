---
type: task
status: active
slug: dramatica-scenarios-content-template
summary: "Cohort-1 Foundation Task in the dramatica-scenarios Epic (078). Materialize the SPEC.md §1 content-template SYSTEM as skills/dramatica-theory/scenarios/_template/ — the meta-template wrapper + one skeleton per archetype identified in §1.2 — so the Cohort-3 authoring Tasks have stable scaffolds to fill."
created: 2026-05-11
updated: 2026-05-11
task_id: "079"
task_status: open
task_owner: "unassigned"
task_priority: P1
task_uses_prompts: []
task_spawns_research: []
task_spawns_prompts: []
task_blocked_by:
  - "078"
task_supersedes: []
task_superseded_by: []
task_affects_paths:
  - skills/dramatica-theory/scenarios/_template/
  - maintenance/schemas/header-ontology.json
---

# Task 079 — Content-template system for scenarios

## Goal

Materialize SPEC.md §1 (Content-template system) from the
`dramatica-scenarios-foundation` research run as the file scaffold under
`skills/dramatica-theory/scenarios/_template/`. The scaffold gives every
Cohort-3 authoring Task a stable starting point so per-scenario authors
do not invent their own structures.

`done` when:

1. `skills/dramatica-theory/scenarios/_template/wrapper.md` — the meta-
   template wrapper from SPEC.md §1.1 (frontmatter schema + mandatory
   body sections + cross-reference rules + EN-throughout discipline).
2. `skills/dramatica-theory/scenarios/_template/_archetypes/<archetype>.md`
   — one file per archetype identified in SPEC.md §1.2 (likely:
   `slot-fill.md`, `audit.md`, `arc-design.md`, plus any new archetypes
   §1.2 surfaces).
3. `skills/dramatica-theory/scenarios/_template/readme.md` — index
   explaining the wrapper-plus-archetype pattern and how a per-scenario
   author chooses an archetype.
4. `maintenance/schemas/header-ontology.json` updated with a `scenario`
   type registration (per SPEC.md §1.1 frontmatter spec) so
   `tools/fm/validate.py --check-body` enforces the contract on
   `skills/dramatica-theory/scenarios/*.md`.
5. A minimal hand-authored proof-of-concept `<archetype>-example.md` for
   one archetype demonstrates the scaffold is fillable end-to-end without
   inventing new sections.

## Context

Parent Epic: [Task 078](../078-dramatica-scenarios-epic/task.md). Drives
the SPEC.md §1 deliverable; precondition for Cohort 3 (per-scenario
authoring). This Task is parallel-safe with [Task 080](../080-dramatica-
scenarios-line-index/task.md) and [Task 081](../081-dramatica-scenarios-
nav-instruct/task.md) but precedes [Task 082](../082-dramatica-scenarios-
taxonomy/task.md) and all Cohort-3 Tasks.

## Plan

1. Read `research/dramatica-scenarios-foundation/output/SPEC.md §1` end-to-end.
2. Extract the meta-template wrapper spec → `_template/wrapper.md`.
3. For each archetype in §1.2 → `_template/_archetypes/<id>.md`.
4. Register `type: scenario` in `header-ontology.json` with the §1.1 body-
   schema (mandatory sections, RFC-2119 normative rules).
5. Pick one archetype + author a proof-of-concept example. Walk it through
   `tools/fm/validate.py --check-body` to confirm the body-schema fits.
6. Update `skills/dramatica-theory/SKILL.md` Pipeline / Reference-Files
   section to point at the new `scenarios/_template/`.

## Todo

- [ ] 1. Read SPEC.md §1 + §1.1-§1.6
- [ ] 2. Author `_template/wrapper.md`
- [ ] 3. Author one `_template/_archetypes/<id>.md` per §1.2 archetype
- [ ] 4. Author `_template/readme.md`
- [ ] 5. Register `type: scenario` in `header-ontology.json`
- [ ] 6. Proof-of-concept fill on one archetype
- [ ] 7. Validate via `tools/fm/validate.py --check-body`
- [ ] 8. Update `skills/dramatica-theory/SKILL.md` reference index

## Links

- Parent epic: [Task 078](../078-dramatica-scenarios-epic/task.md)
- Source spec: `research/dramatica-scenarios-foundation/output/SPEC.md §1`
- Sister Foundation tasks: [Task 080](../080-dramatica-scenarios-line-index/task.md),
  [Task 081](../081-dramatica-scenarios-nav-instruct/task.md)
- Blocks: [Task 082](../082-dramatica-scenarios-taxonomy/task.md) + all
  Cohort-3 authoring Tasks (not yet spawned)
