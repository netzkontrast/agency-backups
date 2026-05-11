---
type: task
status: active
slug: dramatica-scenarios-nav-instruct
summary: "Cohort-1 Foundation Task in the dramatica-scenarios Epic (078). Implement the new `nav.py instruct <entry_id> <scenario_id>` subcommand — returns structured content (definition + scenario_pipeline + worked_example + citations) by joining ontology entry data (Task 080's line-index) with the per-scenario corpus (Task 079's template, Cohort-3's per-scenario authoring). Additive: the existing `nav.py by-id` contract is unchanged."
created: 2026-05-11
updated: 2026-05-11
task_id: "081"
task_status: open
task_owner: "unassigned"
task_priority: P1
task_uses_prompts: []
task_spawns_research: []
task_spawns_prompts: []
task_blocked_by:
  - "079"
  - "080"
task_supersedes: []
task_superseded_by: []
task_affects_paths:
  - tools/dramatica-nav/nav.py
  - tools/dramatica-nav/lib_instruct.py
  - tools/dramatica-nav/tests/test_instruct.py
---

# Task 081 — `nav.py instruct` subcommand

## Goal

Implement the additive `nav.py instruct <entry_id> <scenario_id>` subcommand
per SPEC.md §4.1 (Foundation cohort). The subcommand:

1. Validates that the entry exists (via existing `by-id` machinery) AND
   the scenario applies to the entry (the entry's `scenarios:` list
   contains `<scenario_id>`).
2. Reads `skills/dramatica-theory/scenarios/<scenario_id>.md` (Task 079's
   template, Cohort-3's filled content).
3. Reads the entry's definition prose at `term_file:term_file_line` (Task
   080's line-index).
4. Returns a structured JSON object with:
   - `entry` — `{id, kind, canonical_label, …}` (current `by-id` output)
   - `definition` — verbatim definition prose from `term_file`
   - `scenario_pipeline` — the §pipeline section from `<scenario_id>.md`
   - `decision_heuristics` — the §heuristics section
   - `anti_patterns` — the §anti-patterns section
   - `worked_example` — the §worked-example section
   - `cross_references` — every ontology-id cited in the above sections
     resolved to `{id, term_file, term_file_line}` tuples
   - `citations` — every `[file:line]` citation in the above sections
5. Returns non-zero exit + structured error when:
   - `<entry_id>` does not exist
   - `<scenario_id>` does not exist in ontology
   - The entry's `scenarios:` list does not contain `<scenario_id>`
   - `<scenario_id>.md` does not yet exist (Cohort-3 hasn't authored it)
   - `term_file_line:` is missing (Task 080 hasn't precompiled)

`done` when:

1. `tools/dramatica-nav/nav.py` registers the new `instruct` subparser.
2. `tools/dramatica-nav/lib_instruct.py` — the content-joining logic.
3. `tools/dramatica-nav/tests/test_instruct.py` — covers: happy-path
   resolution, all 5 error cases, JSON output schema stability,
   citations-link-resolve (every cited file:line resolves to a real line
   in a real file).
4. Documentation update in `tools/dramatica-nav/readme.md` covering the
   new subcommand syntax + output schema.

## Context

Parent Epic: [Task 078](../078-dramatica-scenarios-epic/task.md). Depends
on both Foundation sister Tasks ([Task 079](../079-dramatica-scenarios-
content-template/task.md) for the per-scenario file shape; [Task 080](../
080-dramatica-scenarios-line-index/task.md) for the line-index integration
point). Precedes Cohort-3 authoring Tasks (which write the `<scenario_id>.md`
files this subcommand reads) and Cohort-4 integration Tasks (which call
this subcommand from `novel-architect` Phase 2/3/5/7 prose).

**The user-facing payoff:** this subcommand is the deliverable that the
Task 072 self-audit's SELF-INTEREST/MORALITY bug needed. With it, the
calling agent does NOT have to dereference `term_file` and reason from
metadata — `nav.py instruct el.equity novel.crucial-element-audit` returns
the operational instructions inline.

## Plan

1. Read SPEC.md §4.1 (foundation cohort Task spec for this subcommand) +
   §1.2 (archetype skeletons) + §1.6 (nav.py test pattern).
2. Implement `lib_instruct.py`:
   - Entry resolution + scenario applicability validation.
   - Scenario doc parsing (mandatory sections from §1.1 wrapper).
   - Cross-reference resolution (every cited `el.*` / `var.*` / `type.*`
     etc. tag resolves via `by-id` to a `{id, term_file, term_file_line}`
     tuple).
   - Citation link validation (every `[file:line]` resolves to a real
     line in the indicated file).
3. Wire `nav.py` argparse: new `instruct` subparser with positional
   `entry_id` and `scenario_id` arguments, optional `--format json|text`,
   optional `--include-citations`.
4. Test scaffold: 5 error cases + happy path + JSON schema stability test
   (regression against a fixture). Mock `<scenario_id>.md` files in
   `tests/fixtures/` until Cohort-3 lands real content.
5. Document subcommand + output schema in `tools/dramatica-nav/readme.md`.

## Todo

- [ ] 1. Read SPEC.md §4.1 + §1.2 + §1.6
- [ ] 2. Implement `lib_instruct.py` (resolution + parsing + cross-refs)
- [ ] 3. Wire `nav.py instruct` subparser
- [ ] 4. Write `test_instruct.py` (≥ 7 cases: happy + 5 errors + schema)
- [ ] 5. Add fixture `scenarios/` mock for tests (until Cohort-3 lands)
- [ ] 6. Update `tools/dramatica-nav/readme.md` with usage docs
- [ ] 7. End-to-end smoke: `nav.py instruct el.equity novel.crucial-
       element-audit` returns valid JSON against the fixture
- [ ] 8. Run full `tools/dramatica-nav/tests/` — no regression

## Links

- Parent epic: [Task 078](../078-dramatica-scenarios-epic/task.md)
- Source spec: `research/dramatica-scenarios-foundation/output/SPEC.md §4.1`
- Sister Foundation tasks (this Task depends on both):
  [Task 079](../079-dramatica-scenarios-content-template/task.md),
  [Task 080](../080-dramatica-scenarios-line-index/task.md)
- Blocks: all Cohort-3 authoring Tasks (which need a working `instruct`
  to validate their scenario doc renders) and Cohort-4 integration Tasks
  (which call `instruct` from novel-architect phases)
- Task 072 trigger: [Task 072 §Closure](../072-novel-architect-phase2-
  worksheet-loop/task.md) — documents the SELF-INTEREST/MORALITY bug
  this subcommand prevents
