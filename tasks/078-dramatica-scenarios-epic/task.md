---
type: task
status: archived
slug: dramatica-scenarios-epic
summary: "Epic umbrella for the dramatica-scenarios corpus. Replaces nav.py's term_file pointer (filename indirection) with theory-grounded, operationally-actionable scenario instructions for every novel-architect scenario. Spawns a foundational research run, taxonomy expansion, line-indexing tooling, new `nav.py instruct` subcommand, content-template authoring, per-scenario authoring child Tasks (one per scenario), and novel-architect integration. Modeled on the Task 070 Epic pattern."
created: 2026-05-11
updated: 2026-05-12
task_id: "078"
task_status: open
task_owner: "unassigned"
task_priority: P1
task_uses_prompts:
  - dramatica-scenarios-foundation
task_spawns_research:
  - dramatica-scenarios-foundation
task_spawns_prompts: []
task_blocked_by: []
task_supersedes: []
task_superseded_by: []
task_affects_paths:
  - prompts/dramatica-scenarios-foundation/
  - research/dramatica-scenarios-foundation/
  - skills/dramatica-theory/scenarios/
  - skills/dramatica-vocabulary/references/
  - tools/dramatica-nav/lib_line_index.py
  - tools/dramatica-nav/nav.py
  - tools/dramatica-nav/precompile.py
  - maintenance/schemas/narrative-ontology/ontology.json
  - tools/dramatica-nav/tests/
---

# Task 078 — `dramatica-scenarios` Epic

## Goal

Replace `tools/dramatica-nav/nav.py`'s **filename-pointer indirection** with a
theory-grounded **scenario-content corpus**, so every `novel.*` scenario that
appears in the narrative ontology can be queried for **real operational
instructions**, not for a pointer to a markdown file the calling agent must
open, scan, and interpret on its own.

Trigger: the Task 072 self-audit (§9 worked-example accuracy) found that
`Crucial Element: SELF-INTEREST` with partner `MORALITY` would have failed
the H5/H6 hard rules — both are Variations in Physics, not Elements in Mind.
Root cause: the calling agent reasoned from `nav.py by-id` metadata alone
without dereferencing the `term_file` pointer. The scenario tags
(`scenarios: [novel.crucial-element-audit, …]`) on the entry exist as signals
without operational content behind them.

## Acceptance

```gherkin
Feature: dramatica-scenarios Epic — operational corpus + nav.py instruct

# anchor: 078.AC.1
Scenario: Foundational research SPEC.md exists and passes the prompt's acceptance signal
  Given the prompt at "prompts/dramatica-scenarios-foundation/prompt.md" has been dispatched
  When the deep-research executor completes
  Then "research/dramatica-scenarios-foundation/output/SPEC.md" MUST exist
   And SPEC.md MUST pass all 7 criteria listed in the prompt's "## Acceptance signal" section (treated as the SSoT for research-output acceptance)

# anchor: 078.AC.2
Scenario: Final taxonomy formalized in ontology.json
  Given SPEC.md §3.4 has been produced
  When child Task 082 (taxonomy formalization) closes
  Then every scenario_id in SPEC.md §3.4 MUST appear on at least one entry in "maintenance/schemas/narrative-ontology/ontology.json"
   And every entry whose `scenarios:` list was modified MUST have its modification recorded in the Task 082 friction-log delta-table

# anchor: 078.AC.3
Scenario: Build-time line-indexing landed and idempotent
  Given SPEC.md §2 has specified the precompile design
  When child Task 080 (line-index) closes
  Then every entry in "ontology.json" MUST carry `term_file_line:<int>` and `term_file_anchor:<str>`
   And re-running "tools/dramatica-nav/precompile.py" on unchanged inputs MUST produce byte-identical "ontology.json"

# anchor: 078.AC.4
Scenario: nav.py instruct subcommand resolves real (entry, scenario) pairs
  Given Tasks 079 + 080 + 081 are closed
  And at least one Cohort-3 authoring Task has landed `<scenario_id>.md`
  When an agent runs `nav.py instruct <entry_id> <scenario_id>` for an (entry, scenario) pair the ontology knows about
  Then the subcommand MUST return non-empty structured content with `definition`, `scenario_pipeline`, `worked_example`, and `citations` fields
   And every citation tuple MUST resolve to a real file:line in the indexed corpus

# anchor: 078.AC.5
Scenario: Content-template system materialized for Cohort-3 authoring
  Given SPEC.md §1 has specified the meta-template wrapper and §1.2 has enumerated the archetype skeletons
  When child Task 079 (content-template) closes
  Then "skills/dramatica-theory/scenarios/_template/" MUST contain `wrapper.md` plus one archetype file per §1.2 archetype
   And "maintenance/schemas/header-ontology.json" MUST register `type: scenario` with the §1.1 body-schema

# anchor: 078.AC.6
Scenario: Every §3.4 scenario_id has a populated content doc
  Given SPEC.md §3.4 enumerates the final scenario taxonomy
  When all Cohort-3 authoring Tasks close
  Then "skills/dramatica-theory/scenarios/<scenario_id>.md" MUST exist for every scenario_id in §3.4
   And each MUST hit the done-bar (pipeline + heuristics + anti-patterns + Gherkin acceptance + ontology cross-refs + nav.py test + per-scenario end-to-end worked example)

# anchor: 078.AC.7
Scenario: novel-architect phases call nav.py instruct at the operational moments
  Given Cohort-3 authoring is complete
  When child Task 08(N+1) (novel-architect wire-up) closes
  Then "skills/novel-architect/phases/phase2-narrative-architecture.md" MUST reference `nav.py instruct` at Phase 2 Step 6 (Crucial Element)
   And similarly for Phase 3, Phase 5, and Phase 7 operational moments per §3.5

# anchor: 078.AC.8
Scenario: Integration tests validate the full chain
  Given Cohort-4 integration Tasks have closed
  When `python3 -m pytest tools/dramatica-nav/tests/test_scenarios_integration.py` runs
  Then every `scenarios:` tag in "ontology.json" MUST have a corresponding "scenarios/<scenario_id>.md"
   And `nav.py instruct` MUST return non-empty content for every (entry, scenario) pair
   And the line-index precompile MUST be idempotent across re-runs

# anchor: 078.AC.9
Scenario: Epic closes only after all children close
  Given child Tasks 079..08N are all in `task_status: archived`
  When this Epic's `task_status` is flipped
  Then this Epic MUST transition open → done (never closed directly without all children done)
   And `tasks/078-dramatica-scenarios-epic/friction-log.md` MUST be written with a parseable `Highest Frustration Level: FL[0-3]` line
```

## Context

### Why this is an Epic, not a single Task

The user's directive: *"there needs to be a lot of subtasks"*, *"use the
decomposition steps of the research optimizer"*. The work decomposes
cleanly into 4 cohorts (per the research prompt §S Step 4):

- **Cohort 1 — Foundation** (≥ 3 child Tasks): meta-template + per-archetype
  authoring scaffold; line-index implementation; `nav.py instruct` command.
- **Cohort 2 — Discovery confirmation** (1 child Task): formalize the §3.4
  taxonomy in `ontology.json`.
- **Cohort 3 — Authoring** (`N` child Tasks; one per scenario in §3.4;
  `N ≥ 9` per the prompt's acceptance signal). Fully parallel after
  Cohorts 1 + 2 land.
- **Cohort 4 — Integration** (≥ 2 child Tasks): novel-architect phase
  wire-up + integration tests.

The Task 070 Epic landed 7 child Tasks (071–077) and used the same umbrella
pattern. This Epic likely lands 12–18 child Tasks (3 + 1 + 9-N + 2 + buffer).
Exact `N` is unknown until Cohort 1 / 2 produce SPEC.md §3.4.

### Source rules grounding the work

- **AGENTS.md NO.2** — Dramatica-flavored slots MUST resolve through the
  ontology before being written into NCP / used in operational instructions.
  The current `term_file` pointer doesn't satisfy this — agents skip the
  dereference and confabulate. The scenario corpus closes the gap.
- **AGENTS.md NO.5** — non-narrative tasks MUST NOT load the narrative
  ontology. The scenario corpus is narrative — gated under the same NO.5
  discipline. New `scenarios/*.md` files live in `skills/dramatica-theory/`
  which the NO.5 linter already covers.
- **PRE_COMMIT.md** §7.0 — body-schema validation. The new
  `scenarios/<id>.md` file type needs a body-schema entry in
  `maintenance/schemas/header-ontology.json` so `tools/fm/validate.py
  --check-body` enforces the §1.1 frontmatter wrapper. Foundation child Task
  responsibility.

### What this Epic is NOT

- **NOT** a replacement for `dramatica-theory` or `dramatica-vocabulary`.
  Both remain the SSoT for theory and term definitions. The scenario corpus
  is a **third operational layer** on top of them — distillation, not
  duplication.
- **NOT** scope-creep into `lyric.*` scenarios (suno-lyric-writer's domain).
  Out-of-scope per the captured intent.
- **NOT** a rewrite of `nav.py by-id`. The new `instruct` subcommand is
  **additive**; `by-id` keeps its current contract.
- **NOT** the actual scenario content authoring. That happens in the
  Cohort 3 child Tasks; this Epic just orchestrates.

## Plan

### Phase A — Research (the only phase this Epic body owns directly)

1. Execute the prompt at `prompts/dramatica-scenarios-foundation/prompt.md`.
   Dispatch to an external deep-research agent (Gemini Deep Research /
   Claude Research) per the prompt's `prompt_target_agent`. Produce
   `research/dramatica-scenarios-foundation/output/SPEC.md` with §0–§6
   populated.
2. Validate the research output against the prompt's "Acceptance signal"
   checklist (7 criteria). If any fail, spawn a `prompt_kind: follow-up`
   prompt to close the gap rather than accepting a partial output as
   complete.
3. **Reconcile** the pre-committed PROVISIONAL stubs (Tasks 079, 080, 081,
   082) against SPEC.md §4. SPEC.md §4 has authority over cohort sizing
   (e.g. if §1.2 surfaces a 4th archetype warranting its own Foundation
   Task, the §4.1 recommendation may call for 4 Foundation Tasks not 3).
   For each pre-committed stub:
   (a) if §4 confirms its scope: lift the PROVISIONAL banner, fill the
       acceptance Gherkin against SPEC.md's per-Task specification.
   (b) if §4 revises scope/blocked_by/Goal: edit the stub in place; record
       the delta in this Epic's friction-log.
   (c) if §4 splits a stub into multiple Tasks or merges multiple: file
       supersession via `task_supersedes`/`task_superseded_by` per
       TASK.md §4.7 (don't delete the stub history).
4. **Spawn** the additional Cohort-3 authoring Tasks per SPEC.md §3.4 row
   count (`N ≥ 9`) and Cohort-4 integration Tasks per SPEC.md §4.4
   (`≥ 2`). Naming: `tasks/<NNN>-dramatica-scenario-<scenario_id>/` for
   Cohort-3; `tasks/<NNN>-<slug>/` for Cohort-4.

### Phase B — Foundation (delegated to Cohort 1 child Tasks)

Spawned from SPEC.md §4.1. Likely shape (final shape comes from SPEC.md):

- **Task 079 — `dramatica-scenarios-content-template`** — materialize
  SPEC.md §1 as `skills/dramatica-theory/scenarios/_template/` with one
  archetype skeleton per §1.2.
- **Task 080 — `dramatica-scenarios-line-index`** — implement SPEC.md §2
  (build-time line-index precompile step, new ontology fields, idempotency
  invariants).
- **Task 081 — `dramatica-scenarios-nav-instruct`** — implement the
  `nav.py instruct <entry> <scenario>` subcommand against the line-indexed
  ontology + the (still empty) scenarios corpus. Returns structured content
  with `definition + scenario_pipeline + worked_example + citations`.

### Phase C — Discovery confirmation (Cohort 2; 1 child Task)

- **Task 082 — `dramatica-scenarios-taxonomy-formalize`** — based on SPEC.md
  §3.3 (ADD / EXTEND / SKIP verdicts) and §3.4 (FINAL taxonomy), update
  `ontology.json` entry tags. Pre-condition for Cohort 3.

### Phase D — Authoring (Cohort 3; `N` child Tasks)

Spawned from SPEC.md §3.4. One child Task per `novel.*` scenario in the
final taxonomy. Each child Task:

1. Reads all theory chunks + vocabulary refs cited by SPEC.md §3.5 for that
   scenario's archetype.
2. Authors `skills/dramatica-theory/scenarios/<scenario_id>.md` against
   the archetype skeleton.
3. Hits the done-bar: pipeline + heuristics + anti-patterns + Gherkin +
   ontology cross-refs (every cited entry resolves via `nav.py by-id`) +
   nav.py test + per-scenario end-to-end worked example.
4. Spot-test integration: `nav.py instruct <some_entry> <this_scenario_id>`
   returns the new content.

Likely scenarios (final list from SPEC.md §3.4):
- 6 existing `novel.*` keepers (act-pivot, character-arc, crucial-element-
  audit, diagnose-flat-draft, dual-storyform, storyform-slot-fill).
- 3+ new ADD-verdicted scenarios (e.g. signpost-encoding, gate-3-validation-
  failure, crucial-element-encoding — exact list pending SPEC.md §3.4).

### Phase E — Integration (Cohort 4; ≥ 2 child Tasks)

- **Task 08(N+1) — `dramatica-scenarios-novel-architect-wireup`** — update
  `novel-architect` Phase 2 / 3 / 5 / 7 prose to call `nav.py instruct` at
  the operational moments. Specifically: Phase 2 Step 6 (Crucial Element
  audit) becomes `nav.py instruct <ce> novel.crucial-element-audit` instead
  of "consult dramatica-theory". Phase 7 audit-mode becomes a sweep over
  `novel.diagnose-flat-draft`.
- **Task 08(N+2) — `dramatica-scenarios-integration-tests`** — implement
  `tools/dramatica-nav/tests/test_scenarios_integration.py` per the done-
  when checklist item 8 above.

### Phase F — Closure

When all child Tasks (079..08(N+2)) flip to `task_status: done`:

1. Flip this Epic's `task_status: done`.
2. Friction-log at `tasks/078-dramatica-scenarios-epic/friction-log.md`.
3. PR for the integration milestone (or per-child-Task PRs depending on
   how the work batches).

## Todo

- [ ] 1. Dispatch the foundational research prompt
      ([`prompts/dramatica-scenarios-foundation/prompt.md`](../../prompts/dramatica-scenarios-foundation/prompt.md))
      to an external deep-research agent (Gemini Deep Research / Claude
      Research). Track in `research/dramatica-scenarios-foundation/workspace/`.
- [ ] 2. Receive `research/dramatica-scenarios-foundation/output/SPEC.md`;
      verify against the prompt's "Acceptance signal" checklist (7 criteria).
- [ ] 3. Reconcile pre-committed PROVISIONAL stubs (Tasks 079-082) against
      SPEC.md §4 per Phase A step 3 — lift the PROVISIONAL banner where §4
      confirms scope, edit stub in place where §4 revises, supersede where
      §4 splits/merges.
- [ ] 3b. Spawn additional Cohort-3 (authoring; `N ≥ 9`) and Cohort-4
      (integration; ≥ 2) child Tasks per SPEC.md §3.4 + §4.3 + §4.4. Set
      each child's `task_blocked_by:` per the §4.5 dependency graph.
- [ ] 4. **Cohort 1** (Foundation): spawn ≥ 3 child Tasks per SPEC.md §4.1
      (content-template, line-index, nav.py instruct). Track to completion.
- [ ] 5. **Cohort 2** (Discovery confirmation): spawn 1 child Task per
      SPEC.md §4.2 (formalize §3.4 taxonomy in `ontology.json`).
- [ ] 6. **Cohort 3** (Authoring): spawn `N` child Tasks per SPEC.md §4.3
      (one per scenario). Parallel-execute once Cohort 1 + 2 land.
- [ ] 7. **Cohort 4** (Integration): spawn ≥ 2 child Tasks per SPEC.md §4.4
      (novel-architect wire-up + integration tests).
- [ ] 8. **Closure check**: every `scenarios[]` tag in `ontology.json` has
      a corresponding `skills/dramatica-theory/scenarios/<scenario_id>.md`;
      every `<scenario_id>.md` has ≥ 1 `nav.py instruct` test case.
- [ ] 9. **Phase 4 (reader-test) follow-through**: review the executing
      agent's adherence to the `[reader-test:<id>]` tags in the prompt
      output; document any unaddressed findings in this Task's friction-log.
- [ ] 10. Flip `task_status: done` only after every child Task in
       Cohorts 1–4 has reached `task_status: done`.

## Links

- **Foundational prompt:**
  [`prompts/dramatica-scenarios-foundation/prompt.md`](../../prompts/dramatica-scenarios-foundation/prompt.md)
  — the deep-research prompt that produces the SPEC.md feeding all child Tasks.
- **Brief (intent capture):**
  [`prompts/dramatica-scenarios-foundation/brief.md`](../../prompts/dramatica-scenarios-foundation/brief.md)
  — captures the 14 askuser answers from 4 rounds.
- **Source-of-truth trigger:**
  [`tasks/072-novel-architect-phase2-worksheet-loop/task.md` §Closure](../072-novel-architect-phase2-worksheet-loop/task.md)
  — Task 072's self-audit §9 surfaced the SELF-INTEREST/MORALITY worked-
  example bug that proves the `term_file` pointer-indirection model is
  operationally insufficient.
- **Related Tasks (Task 070 Epic):**
  [Task 071](../071-novel-architect-submodule-refactor/task.md) (sub-module split),
  [Task 072](../072-novel-architect-phase2-worksheet-loop/task.md) (Worksheet-Loop spec),
  [Task 073](../073-novel-architect-hard-rules-validation/task.md) (H1-H12 auto-check),
  [Task 075](../075-novel-architect-scene-level-bridge/task.md) (Q1-Q5 audit).
- **Governing specs:**
  [`AGENTS.md`](../../AGENTS.md) (NO.2 + NO.5),
  [`TASK.md`](../../TASK.md),
  [`PROMPT.md`](../../PROMPT.md),
  [`RESEARCH.md`](../../RESEARCH.md),
  [`SKILLS.md`](../../SKILLS.md).
- **Ontology SSoT:**
  [`maintenance/schemas/narrative-ontology/ontology.json`](../../maintenance/schemas/narrative-ontology/ontology.json)
  — 11 scenario_ids today (6 `novel.*` in-scope + 5 `lyric.*` out-of-scope).
