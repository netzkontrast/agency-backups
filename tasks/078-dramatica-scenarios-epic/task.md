---
type: task
status: active
slug: dramatica-scenarios-epic
summary: "Epic umbrella for the dramatica-scenarios corpus. Replaces nav.py's term_file pointer (filename indirection) with theory-grounded, operationally-actionable scenario instructions for every novel-architect scenario. Spawns a foundational research run, taxonomy expansion, line-indexing tooling, new `nav.py instruct` subcommand, content-template authoring, per-scenario authoring child Tasks (one per scenario), and novel-architect integration. Modeled on the Task 070 Epic pattern."
created: 2026-05-11
updated: 2026-05-11
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

`done` when:

1. A foundational research run has produced
   `research/dramatica-scenarios-foundation/output/SPEC.md` (executed via
   the prompt at `prompts/dramatica-scenarios-foundation/prompt.md`) with
   the 6 sections §0–§6 populated per the prompt's "E — Expectations"
   skeleton.
2. The SPEC.md §3.4 final scenario taxonomy has been formalized in
   `maintenance/schemas/narrative-ontology/ontology.json` (added
   `scenarios[]` tags as recommended; redundant existing IDs removed if
   §3.3 SKIP-verdicted any).
3. Build-time line-indexing for `ontology.json` (new `term_file_line:` +
   `term_file_anchor:` fields per SPEC.md §2.6) is implemented in
   `tools/dramatica-nav/precompile.py` and tested for idempotency.
4. A new `nav.py instruct <entry_id> <scenario_id>` subcommand returns the
   embedded scenario instructions + entry-specific guidance + (file, line)
   citations for every (entry, scenario) pair the ontology knows about.
5. The content-template system from SPEC.md §1 is materialized as
   `skills/dramatica-theory/scenarios/_template/` (the meta-template
   wrapper + one skeleton per archetype identified in §1.2).
6. Every `novel.*` scenario in §3.4 has a corresponding
   `skills/dramatica-theory/scenarios/<scenario_id>.md` populated to the
   done-bar (pipeline + heuristics + anti-patterns + Gherkin acceptance
   scenarios + ontology cross-refs + nav.py test + per-scenario end-to-end
   worked example).
7. `novel-architect` Phase 2 / Phase 3 / Phase 5 / Phase 7 prose has been
   updated to reference `nav.py instruct` at the operational moments where
   scenario-grounded guidance is needed (no longer "consult dramatica-
   theory" prose hand-waving).
8. Integration tests in `tools/dramatica-nav/tests/test_scenarios_integration.py`
   confirm: every `scenarios[]` tag in `ontology.json` has a corresponding
   `scenarios/<scenario_id>.md`; `nav.py instruct` returns non-empty
   structured content for every (entry, scenario) pair; the line-index
   precompile is idempotent across reruns.
9. All child Tasks (079–08N) closed with `task_status: done`; this Epic's
   `task_status` flipped to `done` only when the last child Task closes.

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
3. Open the SPEC.md and decompose §4 (Epic decomposition recommendation)
   into the actual child-Task `task.md` files. Each Cohort-1/2/4 child
   Task gets a discrete `tasks/<NNN>-<slug>/task.md`. Cohort-3 authoring
   Tasks may be batched as `tasks/<NNN>-dramatica-scenario-<scenario_id>/`
   per scenario.

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
- [ ] 3. Decompose SPEC.md §4 into discrete child-Task `task.md` files
      under `tasks/079-…/` through `tasks/08N-…/`. Set each child's
      `task_blocked_by:` per the §4.5 dependency graph.
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
