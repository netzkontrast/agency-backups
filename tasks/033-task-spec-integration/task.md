---
type: task
status: active
slug: task-spec-integration
summary: "Close TASK.md governance-debt (T.8.1 unenforced duplicate task_id, T.4.7 updated/abandoned boundary, missing supersession-blocker-inheritance Gherkin), back-port skills-namespace-ontology skill_* L2 vocabulary, and cross-link §3.3 to flexible-frontmatter-toolchain SPEC."
created: 2026-05-06
updated: 2026-05-06
task_id: "033"
task_status: open
task_owner: "unassigned"
task_priority: P1
task_uses_prompts: []
task_spawns_research: []
task_spawns_prompts: []
task_affects_paths:
  - TASK.md
  - tools/fm/check-duplicate-task-id.py
  - tools/check-task-lifecycle-classification.py
---

# Task 033 — TASK.md Spec Integration

## Goal

Resolve the four highest-blast-radius gaps in TASK.md surfaced by the spec-corpus audit. The Task is `done` when (a) duplicate `task_id` collisions are mechanically detected at pre-commit time (closing the gap acknowledged in TASK.md §8.1 prose), (b) the `updated` vs `abandoned` lifecycle boundary has a deterministic decision helper, (c) a supersession-blocker-inheritance Gherkin scenario is added to §6, (d) §3.3 cross-links to `research/flexible-frontmatter-toolchain/output/SPEC.md` as the authoritative L2-namespace source, (e) a new §3.3 subsection enumerates the `skill_*` L2 namespace ratified by `research/skills-namespace-ontology/`, **and (f) §3.3 cross-references the `types.adr` registration shipped by Task 031 in `maintenance/schemas/header-ontology.json:208` (pattern `decisions/[0-9][0-9][0-9][0-9]-*.md`) so the L2 ontology table acknowledges the now-fourth operational namespace (`adr_*`) alongside `task_*` / `prompt_*` / `research_*` / `skill_*`**.

## Context

Spec-audit findings (rank by blast-radius):

- **T.8.1 (TASK.md:332)** is acknowledged-but-unenforced; duplicate-id collisions on tasks 006/006 and 009/009 already exist and are pending Task 024 manual cleanup. Until a linter exists, the loop will repeat.
- **T.4.7 (TASK.md:148–164)** classifies the `updated` lifecycle but does not mechanically distinguish it from `abandoned`. Agents make subjective calls; successor tasks inherit muddled intent.
- **§6 Gherkin** has 10 scenarios but none cover *blocker inheritance through supersession* — when a Task is `task_blocked_by: ["Task X"]` and Task X transitions to `updated` (with a successor Task Y), does the blocker auto-redirect to Y? The spec is silent.
- **§3.3** describes L2 namespacing in prose without citing `research/flexible-frontmatter-toolchain/output/SPEC.md §3–§4` as the authoritative source.
- **`skill_*` namespace** is ratified in `research/skills-namespace-ontology/output/SPEC.md` but is absent from TASK.md §3.3 — agents authoring skill files cannot find the canonical L2 contract from the root spec.
- **Friction-pattern synthesis** is a known coverage gap (no spec aggregates FL0–FL3 patterns across tasks); the head-of-chain research subtask produces the input for §4.6 closure-rule clarifications.

## Preconditions (satisfied at branch-time)

- **Task 016/017/019** — flexible-frontmatter toolchain shipped + repo migrated.
- **Task 028/031** — ADR L2 namespace ratified and `types.adr` registered in `maintenance/schemas/header-ontology.json:208`. The §3.3 amendment (subtask 05) lifts the registration into the spec body.
- **Task 014/025** — friction-log aggregation pattern; subtask 01 builds on this corpus.

## Build-On

- **`tools/fm/_core.py`** — frontmatter parser + `iter_operational_files()` for the duplicate-task_id scan in subtask 03.
- **`tools/adr/ids.py`** — id allocation pattern (zero-padded sequence with collision detection); subtask 03 mirrors this approach for `task_id`.
- **`maintenance/schemas/header-ontology.json`** — single source of truth for required L1+L2 keys; the §3.3 amendment cross-references this rather than duplicating the schema in TASK.md.

## Plan

1. **Phase 1 — Research head.** Dispatch subtask `01-research-friction-pattern-synthesis` to produce a structured analysis of friction-log patterns across all closed tasks, feeding §4.6 closure-rule design.
2. **Phase 1 — Research.** Dispatch subtask `02-research-spec-staleness-decision-formalization` (shared input with Task 039 MAINTENANCE) to formalize the §4.7 updated/abandoned boundary.
3. **Phase 2 — Tooling.** Subtask `03-tooling-duplicate-task-id-linter` (closes T.8.1). Subtask `04-tooling-lifecycle-classifier` (helper for §4.7).
4. **Phase 3 — Spec amendment.** Subtask `05-spec-amendment-task-md`: add §3.3 cross-reference, §3.3 skill_* subsection, §3.3 adr_* subsection (post-Task-031), §6 supersession-blocker Gherkin, §4.7 algorithm refinement, §8.1 enforcement note.
5. **Phase 4 — README sync.** If §6 (linter table) gains the duplicate-task-id linter, update README.md §6 per R.7.

## Sample Gherkin (shape the maintainer authoring subtask 05 should produce)

```gherkin
# anchor: T.B.SUP.1 — supersession-blocker inheritance
Scenario: Blocker auto-redirect through `updated` lifecycle
  Given Task X carries `task_blocked_by: ["Y"]`
  And Task Y transitions to `task_status: updated` with `task_superseded_by: ["Z"]`
  And Task Z carries `task_supersedes: ["Y"]`
  And Task Z is `task_status: open` (not yet done)
  When `tools/fm/check-blocker-satisfaction.py` validates Task X at pre-commit
  Then the validator MUST treat Task X as still blocked
  And the diagnostic MUST cite both Y (superseded) and Z (live successor)
  And Task X MUST NOT transition open → in_progress until Z reaches `done`
```

Anchor namespace `T.B.<topic>.<n>` enables direct citation from TASK.md §6's existing scenario list.

## Todo

- [ ] 1. Dispatch subtask `01-research-friction-pattern-synthesis`.
- [ ] 2. Dispatch subtask `02-research-spec-staleness-decision-formalization` (cross-Task input; shared with Task 039).
- [ ] 3. Dispatch subtask `03-tooling-duplicate-task-id-linter` (Phase A).
- [ ] 4. Dispatch subtask `04-tooling-lifecycle-classifier` (Phase A).
- [ ] 5. Dispatch subtask `05-spec-amendment-task-md` (Phase B; consumes 01, 02, 03).
- [ ] 6. Run `tools/check-governance.sh`; fix every ERROR.
- [ ] 7. Update `README.md §6` if a new linter joins the pipeline.
- [ ] 8. Update `tasks/readme.md`.
- [ ] 9. Author `friction-log.md` with FL[0-3] declaration.
- [ ] 10. Set `task_status: done`.

## Links

- Subtask index: [`subtasks/readme.md`](./subtasks/readme.md)
- Source research:
  - [`research/flexible-frontmatter-toolchain/output/SPEC.md`](../../research/flexible-frontmatter-toolchain/output/SPEC.md) §3–§4 (authoritative L2-namespace source)
  - [`research/skills-namespace-ontology/output/SPEC.md`](../../research/skills-namespace-ontology/output/SPEC.md) (skill_* vocabulary)
  - [`research/governance-specs-update-research/output/SPEC.md`](../../research/governance-specs-update-research/output/SPEC.md) §5 (TASK.md amendment recommendations)
- Sibling: [Task 024 — renumber-duplicate-task-ids-v2](../024-renumber-duplicate-task-ids-v2/task.md) — manual cleanup superseded once subtask 03 lands.
- Governing specs: [`TASK.md`](../../TASK.md), [`MAINTENANCE.md`](../../MAINTENANCE.md) §1, [`README.md`](../../README.md) §11.3
