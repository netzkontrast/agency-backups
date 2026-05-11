---
type: task
status: active
slug: dramatica-scenarios-taxonomy
summary: "Cohort-2 Discovery-confirmation Task in the dramatica-scenarios Epic (078). Formalize SPEC.md §3.4's FINAL scenario taxonomy in maintenance/schemas/narrative-ontology/ontology.json — add the new ADD-verdicted scenario_ids to entry `scenarios:` lists; remove any §3.3 SKIP-verdicted IDs; surface and resolve any §3.3 EXTEND-EXISTING decisions. Pre-condition for Cohort-3 authoring (one Task per scenario in the final taxonomy)."
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
  - "078"
  - "080"
task_supersedes: []
task_superseded_by: []
task_affects_paths:
  - maintenance/schemas/narrative-ontology/ontology.json
  - tools/dramatica-nav/tests/test_scenario_tags.py
---

# Task 082 — Formalize SPEC.md §3.4 scenario taxonomy in ontology.json

## Goal

Take SPEC.md §3.4's FINAL scenario taxonomy + §3.3 ADD/EXTEND/SKIP verdicts
and apply them to `maintenance/schemas/narrative-ontology/ontology.json`:

1. For each ADD-verdicted scenario_id: walk the candidate-entries list from
   §3.2 ("entries it would tag" column) and append the scenario_id to each
   matching entry's `scenarios:` list.
2. For each EXTEND-EXISTING verdict: rename or merge per §3.3's instruction.
3. For each SKIP verdict: leave unchanged (no removal — SKIP means "don't
   add"; only the ADD scenarios are net-new tagging work).
4. Run `tools/dramatica-nav/precompile.py` to re-line-index (Task 080's
   pipeline) and `tools/dramatica-nav/validate.py` to confirm the modified
   ontology is internally consistent.

`done` when:

1. `ontology.json` carries every §3.4 FINAL scenario_id at least once (i.e.
   no scenario_id is "defined" in §3.4 but "tagged on zero entries").
2. Every entry that was previously tagged with a SKIP-verdicted ID retains
   that tag (no destructive removal — preserves backward compat for the
   transition).
3. `tools/dramatica-nav/tests/test_scenario_tags.py` — covers: every §3.4
   scenario_id appears on ≥ 1 entry; cross-cohort sanity (Cohort-3 will
   author one `<scenario_id>.md` per §3.4 ID, so the IDs MUST align);
   alphabetical-stability of `scenarios:` lists per entry (no nondeterministic
   ordering).
4. `tools/dramatica-nav/validate.py` exits 0 against the modified ontology.
5. The tagging delta (which entries gained which IDs) is summarized in the
   Task's friction-log so Cohort-3 authors know which entries each scenario
   touches.

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
