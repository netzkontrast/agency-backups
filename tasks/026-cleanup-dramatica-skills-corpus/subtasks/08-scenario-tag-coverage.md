---
type: note
status: draft
slug: task-026-st8-scenario-tag-coverage
summary: "Subtask ST-8: bring scenario coverage from 85 → ~250 entries via three /sc:improve --loop iterations. Maintain Task 015's M01 invariant (median ≤5, max ≤8 per term)."
created: 2026-05-05
updated: 2026-05-05
subtask_id: "ST-8"
subtask_phase: "C"
subtask_recommended_agent: "quality-engineer"
subtask_depends_on:
  - "ST-1"
  - "ST-2"
  - "ST-3"
  - "ST-4"
  - "ST-5"
  - "ST-7"
subtask_falsification: "Wrong cut iff scenario tagging at scale dilutes the median below the 5-tag M01 invariant. Mitigated by capping per-term tags at 4 (subtask-enforced) and 8 (schema-enforced) plus per-iteration M01 gate."
---

# ST-8: Scenario Tag Coverage Pass

## Goal

Bring scenario coverage on the ontology up from 85 (27.9%) to ~250 entries (≥82%). Use Task 015's exact `/sc:improve --loop --iterations 3` pattern — same dispatch, same per-iteration gate, same M01 median-tag-count invariant.

Per-iteration shape (each iteration is a `/sc:improve` invocation):

1. **Iteration 1: archetypes + throughlines + classes + character-dynamics + plot-dynamics.**
   - These are the high-frequency ontology-trunk entries. Most are ALREADY tagged; this iteration backfills the few gaps. Target after iter 1: ≥90% of these kinds tagged.
2. **Iteration 2: types + variations.**
   - 16 types + 64 variations = 80 entries. Each is in a Class; the Class's scenarios cascade. Target after iter 2: ≥150 entries with ≥1 scenario.
3. **Iteration 3: elements + concepts.**
   - 64 elements + 39 concepts = 103 entries. Element-tagging is the highest-value because element-level lookups are the densest in `novel-architect`'s queries. Target after iter 3: ≥250 entries with ≥1 scenario.

After EACH iteration, run a measurement pass:

- median scenarios-per-tagged-term (target ≤4 per ST-8 cap; ≤5 per Task 015's M01)
- mean scenarios-per-tagged-term
- max scenarios-per-tagged-term (target ≤4; schema cap is 8)
- count of orphan scenarios (scenarios with <3 entries tagged)
- count of over-tagged scenarios (scenarios with >25 entries tagged)

The measurement pass is the gate. If iteration K's median > 4, ST-8 halts (the subtask FAILS) and emits a friction event. The agent does NOT advance to iteration K+1.

## Falsification

Wrong cut **iff** scenario tagging at scale dilutes the median below the 5-tag M01 invariant from Task 015. Mitigation:
- Per-term cap of 4 tags (subtask-enforced; tighter than the schema's 8-cap).
- Per-iteration M01 gate (halts the subtask, does not silently degrade).
- Cap of 3 iterations (Task 015's empirical sweet spot).

If the cut is wrong, the friction event surfaces TWO ratifiable patterns for Task 027: (1) the per-term cap should be variable (some terms genuinely apply across many scenarios), or (2) the scenario taxonomy itself is too fine-grained and Task 027 should consolidate.

## Inputs

- `maintenance/schemas/narrative-ontology/ontology.json` — write surface for scenario tags.
- `maintenance/schemas/narrative-ontology/scenarios.json` — read-only; the 11 canonical persona scenarios.
- `tools/dramatica-nav/term.py edit --set-scenario` (delivered by ST-5) — the projection tool. ST-8 USES this; doesn't re-implement.
- `tasks/015-integrate-dramatica-ncp-skills/notes.md §Plan Step 6` — the precedent for `/sc:improve --loop --iterations 3` against scenario tagging.

## Acceptance Criteria

1. **Coverage hits target.** After three iterations, `python3 tools/dramatica-nav/nav.py by-scenario novel.crucial-element-audit` (or any other scenario) returns ≥10 entries; total entries with `scenarios` non-empty is ≥250.
2. **M01 invariant holds.** Median scenarios-per-tagged-term ≤4 (stricter than Task 015's ≤5). Max ≤4. Schema cap (≤8) untouched.
3. **No orphan scenarios.** Every scenario in `scenarios.json` has ≥3 entries tagged with it.
4. **No over-tagged scenarios.** No scenario has >75 entries tagged with it (ratio sanity — at 304 total entries, no single scenario should claim >25%).
5. **Measurement table emitted.** `tasks/026-cleanup-dramatica-skills-corpus/notes.md §9` (a new section) carries a per-iteration measurement table.
6. **Validator clean.** `validate.py` reports 0 schema or scenario-tag-resolvability errors.
7. **Single commit per iteration.** Three commits total. Titles: `feat(dramatica-nav): scenario coverage iter <N>/3 (Task 026 ST-8)`.

## Dependencies

ST-1 / ST-2 / ST-3 / ST-4 (clean corpus) and ST-5 / ST-7 (term.py and aliases.py for the dispatch).

## Estimated Effort

Medium (~3 hours wall-clock; iteration-bound).

## Agent Prompt

```text
You are implementing ST-8 of Task 026 (cleanup-dramatica-skills-corpus) for
the netzkontrast/agency repo on branch claude/cleanup-dramatica-skills-1cEOO.

Repo root: /home/user/agency
Working directory: /home/user/agency

Context files (read first):
  - tasks/026-cleanup-dramatica-skills-corpus/task.md
  - tasks/026-cleanup-dramatica-skills-corpus/subtasks/08-scenario-tag-coverage.md (this file)
  - tasks/015-integrate-dramatica-ncp-skills/notes.md §Plan Step 6 (the
    precedent for the 3-iteration /sc:improve loop against scenario tagging)
  - maintenance/schemas/narrative-ontology/scenarios.json (the 11 canonical
    persona scenarios)
  - maintenance/schemas/narrative-ontology/ontology.json (current state —
    85 entries tagged out of 304)
  - tools/dramatica-nav/term.py (delivered by ST-5; the projection tool)

Goal:
  Bring scenario coverage from 85 → ~250 entries via three /sc:improve
  iterations. Per-iteration distribution per §Goal of this subtask file.
  Maintain the M01 median ≤4 invariant.

Acceptance criteria (reproduce verbatim from this file's Acceptance Criteria
section). All seven must be true.

Implementation approach:
  1. Iteration 1: walk archetypes / throughlines / classes / character-dynamics
     / plot-dynamics. For each entry not yet tagged, decide which scenario
     IDs apply by looking at the scenario's "Typical query" column from
     [Task 015 §Personas]. Use term.py edit --set-scenario per entry.
     Run measurement; halt if median > 4.
  2. Iteration 2: walk types + variations. Same approach.
     Run measurement; halt if median > 4.
  3. Iteration 3: walk elements + concepts. Same approach.
     Run measurement; halt if median > 4.
  4. After each iteration: validate.py; commit; emit measurement
     table to notes.md §9.
  5. Three commits total, one per iteration.

Constraints:
  - Use term.py edit --set-scenario (delivered by ST-5). DO NOT
    hand-edit ontology.json or per-term frontmatter.
  - Per-term cap of 4 tags (stricter than schema's 8). If a term genuinely
    needs more, file as a friction event AND drop the term back to the
    most-likely 4 tags.
  - DO NOT mint new scenario IDs. The 11 in scenarios.json are frozen
    at v0.1.
  - The M01 measurement gate halts the subtask if median > 4 in any
    iteration. Halting is correct behaviour, not a failure to escalate.

When done (after all three iterations):
  - python3 tools/dramatica-nav/validate.py                                  (must exit 0)
  - python3 -c "import json; e=json.load(open('maintenance/schemas/narrative-ontology/ontology.json'))['entries']; \
      tagged=[x for x in e if x.get('scenarios')]; print(f'tagged: {len(tagged)} / {len(e)}')"
                                                                              (must show ≥250 / 304)
  - cat tasks/026-cleanup-dramatica-skills-corpus/notes.md | grep -A3 "§9"   (must show measurement table)
  - Three commits, titled "feat(dramatica-nav): scenario coverage iter <N>/3 (Task 026 ST-8)"
  - Do NOT push.
```
