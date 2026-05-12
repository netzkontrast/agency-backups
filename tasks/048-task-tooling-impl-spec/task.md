---
type: task
status: archived
slug: task-tooling-impl-spec
summary: "Research the /skills/ corpus (especially research-prompt-optimizer) for inspiration, inventory existing /tasks/ tooling and gaps, and produce an implementation-ready SPEC for Task-orchestration tooling — state-transition helpers, template scaffolding, lifecycle automation, audit-graph maintenance, friction-log automation."
created: 2026-05-07
updated: 2026-05-12
task_id: "048"
task_status: open
task_owner: "unassigned"
task_priority: P2
task_uses_prompts: []
task_spawns_research:
  - task-tooling-impl-spec
task_spawns_prompts: []
task_affects_paths:
  - research/task-tooling-impl-spec/
  - prompts/research-skills-corpus-inspiration-survey/
  - prompts/research-existing-task-tooling-inventory/
  - prompts/spec-task-tooling-impl/
---

# Task 048 — Task Tooling Implementation SPEC

## Goal

Produce `research/task-tooling-impl-spec/output/SPEC.md` — an implementation-ready specification for the next generation of `/tasks/` tooling. The SPEC answers a single question: *what tools should the repo ship to mechanise Task creation, state-transition, template scaffolding, audit-graph maintenance, and friction-log capture, and what should each tool's surface look like?*

The Task is `done` when:

1. The SPEC enumerates **≥6** concrete tools with one-paragraph rationale, CLI surface, integration point (pre-commit / manual / both), and falsification clause each.
2. Every proposed tool cites at least one inspiration source from `/skills/<slug>/` (preferably `research-prompt-optimizer/`'s phase + module decomposition or `prompt-optimizer/`'s scenario-keyed decision tables).
3. The SPEC maps each proposed tool to the existing `tools/fm/`, `tools/adr/`, and root-spec contracts (TASK.md §4 lifecycle, §3.3 ontology, §7 pre-commit linters, §8.1 duplicate-id, §4.7 lifecycle-classifier) so reviewers can locate the integration seam without re-reading the SPEC.
4. The §1–§7 build contract pattern (proven by [Task 028 `adr-tooling-impl-plan`](../028-adr-tooling-impl-plan/)) is followed: §1 inputs / §2 architecture / §3 per-tool spec / §4 tests / §5 integration / §6 rollout / §7 falsification.
5. `tools/check-governance.sh` exits 0 on the closing commit (or remaining ERRORs are documented as out-of-scope per the Task 033 / Task 032 friction-log precedent).
6. A follow-up Task (NOT scoped here) implements the SPEC; this Task ends at SPEC ratification.

## Context

The repo has accumulated significant `/tasks/`-side governance debt that recent tasks chip at piecemeal:

- **Task 031** shipped `tools/fm/index_diff.py` to mechanise §7.11 tasks-index freshness.
- **Task 033 ST-3** shipped `tools/fm/check-duplicate-task-id.py` to mechanise §8.1.
- **Task 033 ST-4** shipped `tools/fm/check-task-lifecycle-classification.py` as a §4.7 helper.
- **Task 041** repaired the `task_uses_prompts ↔ prompt_relates_to_task` audit-graph edge after PR #70.
- **Task 042 / Task 043 / Task 044** are open follow-ups for narrative-nav / renumber / maintenance findings.

Each lands one tool in isolation; **no integrating spec** says what the full toolchain should look like, what's missing, or how the existing tools relate. The `/skills/` corpus — specifically `research-prompt-optimizer/` (phases, modules, render, examples, AGENTS.md) and `prompt-optimizer/` (scenario-keyed decision tables, intent-framework-map) — solves an analogous problem at the prompt layer with a structured decomposition that the Task layer has never adopted.

This Task surveys that prior art, inventories the existing `/tasks/` tooling and gaps, and produces the missing integrating SPEC.

## Preconditions (satisfied at branch-time)

- **Task 016 / 017** — flexible-frontmatter toolchain shipped + repo migrated.
- **Task 023** — `header-ontology.json` is the source of truth; Task tooling MUST consume it rather than duplicate the schema.
- **Task 028** — the §1–§7 build-contract template the SPEC will follow.
- **Task 031** — `tools/fm/index_diff.py` baseline.
- **Task 033** — duplicate-id linter + lifecycle-classifier baseline; ST-2 SPEC ratified the staleness algorithm.
- **Task 041** — extracted-prompt corpus the SPEC will reference for `task_uses_prompts ↔ prompt_relates_to_task` automation candidates.

## Build-On

- **`skills/research-prompt-optimizer/`** — phase decomposition (`phases/`), module catalog (`modules/`, `catalog.yaml`), render pipeline (`render/`), AGENTS.md interaction contract. The ST-1 inspiration survey extracts patterns that map onto Task tooling.
- **`skills/prompt-optimizer/`** — scenario-keyed decision tables (`selection.md`, `intent-framework-map.md`, `framework-components.md`, `templates.md`). Pattern source for the SPEC's tool-selection table.
- **`tools/fm/_core.py`** — frontmatter parser + `iter_operational_files()` foundation for any new linter.
- **`tools/adr/cli.py`** — composite-CLI pattern (`validate`, `synthesize`, `extract`, `compress`, `runlog`, `ids`) the SPEC may emulate for a `task-tooling` CLI.
- **`maintenance/schemas/header-ontology.json`** — the schema every new tool MUST consume.

## Plan

1. **Phase A — Inspiration survey.** Dispatch [`subtasks/01-research-skills-corpus-inspiration.md`](./subtasks/01-research-skills-corpus-inspiration.md). Author the executing prompt at `/prompts/research-skills-corpus-inspiration-survey/` at dispatch time (per Task 041 audit-graph repair pattern); add the slug to `task_uses_prompts` once the prompt exists.
2. **Phase A — Existing-tooling inventory.** Dispatch [`subtasks/02-research-existing-task-tooling-inventory.md`](./subtasks/02-research-existing-task-tooling-inventory.md). Author the executing prompt at `/prompts/research-existing-task-tooling-inventory/`; add the slug to `task_uses_prompts`.
3. **Phase B — SPEC synthesis.** Dispatch [`subtasks/03-spec-task-tooling-impl.md`](./subtasks/03-spec-task-tooling-impl.md). Author the executing prompt at `/prompts/spec-task-tooling-impl/`; add the slug to `task_uses_prompts`. Output: `research/task-tooling-impl-spec/output/SPEC.md` per the §1–§7 build-contract pattern, integrating ST-1 patterns and ST-2 inventory into ≥6 concrete tool proposals.
4. **Closing run.** Author `friction-log.md` (FL[0-3]); update `tasks/readme.md` to reflect `task_status: archived`; flip status; commit; push. Per AGENTS.md CR.1.

**Planned prompt slugs** (frontmatter pre-declaration deferred until each prompt is authored, per the F.T.1 linter contract): `research-skills-corpus-inspiration-survey`, `research-existing-task-tooling-inventory`, `spec-task-tooling-impl`.

## Falsification

The Task is the **wrong cut** iff any of the following hold at SPEC ratification:

1. Fewer than 6 concrete tools surface from the synthesis (the goal threshold; below this, the existing piecemeal pattern is sufficient and a SPEC adds no value).
2. The SPEC duplicates schema content already in `maintenance/schemas/header-ontology.json` rather than cross-referencing it (mitigation: ST-3 validates the SPEC against the schema's required-key matrix before commit).
3. ST-1's pattern extraction yields fewer than 4 transfers from `skills/research-prompt-optimizer/` (mitigation: the skill has 7+ surface artefacts — phases/, modules/, render/, examples/, AGENTS.md, catalog.yaml, meta-prompt-spec.md — so a four-pattern minimum is well-cleared at floor).
4. The proposed tool surface forces a TASK.md amendment chain greater than 3 sections (mitigation: the SPEC is *implementation-ready* — its §5 integration column cites existing TASK.md anchors rather than proposing new ones; ≥3 amendments signals scope creep).

## Sample SPEC §3 Entry Shape (the synthesiser should produce ≥6 of these)

```text
### §3.N — `tools/fm/<name>.py` — <one-line purpose>

**Inspiration source:** skills/<slug>/<artefact> (citation + anchor).
**Surface:** `python3 tools/fm/<name>.py [args]` — exit codes 0 (clean), 1 (diagnostic), 2 (usage).
**Integration:** pre-commit / manual / both; cited TASK.md anchor.
**Schema dependency:** `maintenance/schemas/header-ontology.json` keys consumed.
**Test surface:** `tools/tests/fm/test_<name>.py` — N test cases covering …
**Falsification:** the tool is the wrong cut iff …
```

The `T.T.<topic>.<n>` anchor namespace MAY be reserved for SPEC-internal Gherkin scenarios per the Task 033 §6 precedent.

## Todo

- [ ] 1. Dispatch subtask `01-research-skills-corpus-inspiration` (Phase A).
- [ ] 2. Dispatch subtask `02-research-existing-task-tooling-inventory` (Phase A).
- [ ] 3. Dispatch subtask `03-spec-task-tooling-impl` (Phase B; consumes 01, 02).
- [ ] 4. Run `tools/check-governance.sh`; resolve every newly-introduced ERROR (pre-existing baseline ERRORs documented out-of-scope per the Task 033 / Task 032 precedent).
- [ ] 5. Update `tasks/readme.md` with the closure bullet (cite the produced SPEC).
- [ ] 6. Author `friction-log.md` with FL[0-3] declaration.
- [ ] 7. Set `task_status: done` and commit.

## Links

- Subtask index: [`subtasks/readme.md`](./subtasks/readme.md)
- Inspiration sources:
  - [`skills/research-prompt-optimizer/`](../../skills/research-prompt-optimizer/) — phases / modules / render / AGENTS.md.
  - [`skills/prompt-optimizer/`](../../skills/prompt-optimizer/) — scenario-keyed decision tables.
  - [`skills/spec-skill/`](../../skills/spec-skill/) — apply-mode pattern (potential transfer to Task templates).
  - [`skills/the-agency-system-architect/`](../../skills/the-agency-system-architect/) — meta-system orchestration framing.
- Build-contract template: [Task 028 `adr-tooling-impl-plan`](../028-adr-tooling-impl-plan/implementation-plan.md) §1–§7.
- Existing Task tooling baseline:
  - [`tools/fm/`](../../tools/fm/) — validate, edit, query, extract, section, rename, fix, graph, index_diff.
  - [`tools/fm/check-duplicate-task-id.py`](../../tools/fm/check-duplicate-task-id.py) — Task 033 ST-3.
  - [`tools/fm/check-task-lifecycle-classification.py`](../../tools/fm/check-task-lifecycle-classification.py) — Task 033 ST-4.
  - [`tools/adr/cli.py`](../../tools/adr/cli.py) — composite-CLI pattern (Task 031).
- Governing specs: [`TASK.md`](../../TASK.md), [`MAINTENANCE.md`](../../MAINTENANCE.md), [`PROMPT.md`](../../PROMPT.md), [`RESEARCH.md`](../../RESEARCH.md), [`SKILLS.md`](../../SKILLS.md).
