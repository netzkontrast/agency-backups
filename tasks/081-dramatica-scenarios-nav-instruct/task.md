---
type: task
status: active
slug: dramatica-scenarios-nav-instruct
summary: "PROVISIONAL stub (final scope from SPEC.md §4 of research/dramatica-scenarios-foundation/). Cohort-1 Foundation Task in the dramatica-scenarios Epic (078). Implement the new `nav.py instruct <entry_id> <scenario_id>` subcommand — returns structured content (definition + scenario_pipeline + worked_example + citations) by joining ontology entry data (Task 080's line-index) with the per-scenario corpus (Task 079's template, Cohort-3's per-scenario authoring). Additive: the existing `nav.py by-id` contract is unchanged."
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
  - 079
  - 080
task_supersedes: []
task_superseded_by: []
task_affects_paths:
  - tools/dramatica-nav/nav.py
  - tools/dramatica-nav/lib_instruct.py
  - tools/dramatica-nav/tests/test_instruct.py
  - tools/dramatica-nav/readme.md
---

# Task 081 — `nav.py instruct` subcommand

> **🔶 PROVISIONAL STUB** — Cohort-1 Foundation work locked at the goal level
> (additive `nav.py instruct <entry> <scenario>` subcommand); detailed
> acceptance below reconciles against SPEC.md §4.1 + §1.2 + §1.6 once the
> foundational research run completes. Do not start implementation until
> §4.1 has landed. (Per Epic 078 Phase A step 3.)

## Goal

Implement the additive `nav.py instruct <entry_id> <scenario_id>` subcommand
per SPEC.md §4.1 (Foundation cohort). The subcommand validates the
(entry, scenario) pair, reads the scenario doc, dereferences the entry's
definition via the Task 080 line-index, and returns structured JSON with
`entry`, `definition`, `scenario_pipeline`, `decision_heuristics`,
`anti_patterns`, `worked_example`, `cross_references`, and `citations`
fields. The existing `by-id` subcommand contract is unchanged.

## Acceptance

```gherkin
Feature: nav.py instruct subcommand

# anchor: 081.AC.1
Scenario: Happy path returns structured content
  Given Tasks 079 + 080 are closed
  And a Cohort-3 authoring Task has produced "skills/dramatica-theory/scenarios/novel.crucial-element-audit.md"
  When the agent runs `python3 tools/dramatica-nav/nav.py instruct el.equity novel.crucial-element-audit`
  Then the subcommand MUST exit 0
   And MUST return a JSON object with non-empty `entry`, `definition`, `scenario_pipeline`, `worked_example`, and `citations` fields

# anchor: 081.AC.2
Scenario: Unknown entry returns structured error
  When the agent runs `instruct el.does-not-exist novel.crucial-element-audit`
  Then the subcommand MUST exit non-zero
   And MUST return a structured error naming the unknown entry-id

# anchor: 081.AC.3
Scenario: Unknown scenario returns structured error
  When the agent runs `instruct el.equity novel.does-not-exist`
  Then the subcommand MUST exit non-zero
   And MUST return a structured error naming the unknown scenario-id

# anchor: 081.AC.4
Scenario: Scenario does not apply to entry
  Given `el.equity` has `scenarios:` list NOT containing `novel.act-pivot`
  When the agent runs `instruct el.equity novel.act-pivot`
  Then the subcommand MUST exit non-zero
   And MUST return a structured error citing the applicability mismatch

# anchor: 081.AC.5
Scenario: Scenario doc not yet authored
  Given `scenarios:` list applies but "skills/dramatica-theory/scenarios/<id>.md" does NOT yet exist
  When the agent runs `instruct` for that pair
  Then the subcommand MUST exit non-zero
   And MUST return a structured error stating "scenario doc not yet authored — pending Cohort-3"

# anchor: 081.AC.6
Scenario: Line-index missing
  Given the entry's `term_file_line` is missing (Task 080 not yet run)
  When the agent runs `instruct`
  Then the subcommand MUST exit non-zero
   And MUST return a structured error stating "line-index not yet built — run tools/dramatica-nav/precompile.py"

# anchor: 081.AC.7
Scenario: Citation links resolve
  Given a happy-path call has returned content with `citations:` entries
  When each `[file:line]` tuple in `citations` is resolved
  Then every cited line MUST exist in the cited file
```

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
