---
type: task
status: active
slug: dramatica-scenarios-taxonomy
summary: "PROVISIONAL stub (final scope from SPEC.md §4 of research/dramatica-scenarios-foundation/). Cohort-2 Discovery-confirmation Task in the dramatica-scenarios Epic (078). Formalize SPEC.md §3.4's FINAL scenario taxonomy in maintenance/schemas/narrative-ontology/ontology.json — add the new ADD-verdicted scenario_ids to entry `scenarios:` lists; remove any §3.3 SKIP-verdicted IDs; surface and resolve any §3.3 EXTEND-EXISTING decisions. Pre-condition for Cohort-3 authoring (one Task per scenario in the final taxonomy)."
created: 2026-05-11
updated: 2026-05-11
task_id: "082"
task_status: open
task_owner: "unassigned"
task_priority: P1
task_uses_prompts: []
task_spawns_research: []
task_spawns_prompts: []
task_blocked_by:
  - 080
task_supersedes: []
task_superseded_by: []
task_affects_paths:
  - maintenance/schemas/narrative-ontology/ontology.json
  - tools/dramatica-nav/tests/test_scenario_tags.py
---

# Task 082 — Formalize SPEC.md §3.4 scenario taxonomy in ontology.json

> **🔶 PROVISIONAL STUB** — Cohort-2 Discovery-confirmation work locked at the
> goal level (apply SPEC.md §3.4 verdicts to ontology.json); detailed
> acceptance below reconciles against §3.2–§3.4 once the foundational
> research run completes. Do not start implementation until §3.4 has landed.
> (Per Epic 078 Phase A step 3.)

## Goal

Take SPEC.md §3.4's FINAL scenario taxonomy + §3.3 ADD/EXTEND/SKIP verdicts
and apply them to `maintenance/schemas/narrative-ontology/ontology.json`:
for each ADD-verdicted scenario_id, walk §3.2's candidate-entries filter
and append the scenario_id to each matching entry's `scenarios:` list; for
each EXTEND-EXISTING verdict, rename or merge per §3.3's instruction; for
each SKIP verdict, leave unchanged. Re-run precompile (Task 080) and
validate to confirm internal consistency.

## Acceptance

```gherkin
Feature: Formalize SPEC.md §3.4 scenario taxonomy

# anchor: 082.AC.1
Scenario: Every §3.4 ID tagged on ≥ 1 entry
  Given SPEC.md §3.4 has produced a FINAL taxonomy
  When this Task closes
  Then every scenario_id in §3.4 MUST appear on at least one entry's `scenarios:` list
   And no scenario_id MUST be "defined in §3.4 but tagged on zero entries"

# anchor: 082.AC.2
Scenario: SKIP verdicts preserve existing tags (no destructive removal)
  Given §3.3 has SKIP-verdicted some candidates
  When this Task closes
  Then every entry that was previously tagged with a SKIP-verdicted ID MUST still carry that tag
   And the modification script MUST be additive-only (no entry loses tags it had before)

# anchor: 082.AC.3
Scenario: Tag delta documented in friction-log
  Given the modification script has run
  When this Task closes
  Then "tasks/082-dramatica-scenarios-taxonomy/friction-log.md" MUST contain a delta table
   And the table MUST list: scenario_id × entries-tagged × entries-untouched

# anchor: 082.AC.4
Scenario: Re-precompile is idempotent on the modified ontology
  Given the modification script has run
  When "tools/dramatica-nav/precompile.py" is run twice
  Then the two resulting `ontology.json` files MUST be byte-identical

# anchor: 082.AC.5
Scenario: Validation passes
  Given the modified ontology is committed
  When "tools/dramatica-nav/validate.py" runs
  Then the validator MUST exit 0
   And report no orphan tags, no duplicate entries, and no broken cross-references

# anchor: 082.AC.6
Scenario: Tag list ordering is deterministic
  Given any entry's `scenarios:` list has been modified
  When the modified entry is inspected
  Then the `scenarios:` list MUST be alphabetically sorted
   And re-running the modification script MUST NOT change the order
```

## Context

Parent Epic: [Task 078](../078-dramatica-scenarios-epic/task.md). Single
Cohort-2 Task. Must run AFTER Task 080 (line-index) so the modified
ontology re-indexes cleanly. Precedes ALL Cohort-3 authoring Tasks
(which need final scenario_ids to enumerate).

## Plan

1. Read SPEC.md §3.2 + §3.3 + §3.4 + §3.5.
2. Build a scripted modification pass (one-shot Python script) that:
   - Loads `ontology.json`
   - For each §3.3 ADD candidate: applies the §3.2 "entries it would tag"
     filter and appends the new scenario_id to matching entries
   - Persists the modified ontology with stable key ordering
3. Run `tools/dramatica-nav/precompile.py` to re-line-index.
4. Run `tools/dramatica-nav/validate.py` — fix any errors.
5. Spot-check 5 random ADDed (entry, scenario) pairs are sensible.
6. Author `test_scenario_tags.py` — assertion gates listed above.
7. Document the delta in friction-log: ADDed-IDs × entry-counts table.

## Todo

- [ ] 1. Read SPEC.md §3.2-§3.5
- [ ] 2. Write the modification script (idempotent — re-runnable)
- [ ] 3. Apply ADD verdicts to ontology.json
- [ ] 4. Re-precompile (Task 080's pipeline)
- [ ] 5. Run `tools/dramatica-nav/validate.py` — fix any errors
- [ ] 6. Spot-check 5 random ADDed pairs (sanity)
- [ ] 7. Author `test_scenario_tags.py`
- [ ] 8. Friction-log: tag-delta summary table

## Links

- Parent epic: [Task 078](../078-dramatica-scenarios-epic/task.md)
- Source spec: `research/dramatica-scenarios-foundation/output/SPEC.md §3.2-§3.5`
- Blocked by: [Task 080](../080-dramatica-scenarios-line-index/task.md)
  (precompile must integrate first)
- Blocks: all Cohort-3 authoring Tasks (one per §3.4 scenario_id)
