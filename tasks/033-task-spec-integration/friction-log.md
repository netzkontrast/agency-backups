---
type: note
status: active
slug: task-033-friction-log
summary: "Friction log for Task 033 — TASK.md spec integration. FL1: research subtasks dispatched in parallel via deep-research subagents while ST-3 / ST-4 / ST-5 implementation proceeded; one pre-existing branch ERROR (Task 046 missing `## Todo`) is documented as scope-out."
created: 2026-05-07
updated: 2026-05-18
---

# Task 033 — Friction Log

## FL Declaration

**FL1** — minor friction. The chain executed largely as planned; two specific points are recorded below for the friction-pattern-synthesis corpus (Task 033 ST-1 itself).

## Notes

### Phase A — parallel dispatch

- ST-3 (`tools/fm/check-duplicate-task-id.py`) and ST-4 (`tools/fm/check-task-lifecycle-classification.py`) were implemented directly in this session; ST-1 (friction synthesis) and ST-2 (staleness algorithm) were dispatched as background `deep-research` subagents and ran concurrently.
- ST-2 landed first and committed `de03603` autonomously per its prompt convention; the §4.7 prose in TASK.md was updated mid-stream once `research/spec-staleness-decision-formalization/output/SPEC.md` materialised, so the helper docstring and §4.7 helper paragraph cite the now-existing SPEC instead of the "when it lands" placeholder language.
- ST-1 produced its SPEC + reflection workspace but did not commit autonomously; its files were folded into the closing commit.
- The duplicate-task-id linter was wired into `tools/check-governance.sh` as **advisory by default** (gated by `FM_DUPLICATE_TASK_ID_STRICT=1`) rather than gating because the current branch has four unresolved collisions (006/006, 009/009, 031/031, 032/032) that Task 043 owns. The brief anticipated this — see `tasks/033-task-spec-integration/readme.md` Assumptions Log. Once Task 043 lands, the strict flag can be flipped on by default.

### ST-4 algorithm scope

ST-4's helper currently implements the **four-condition fallback** derived from TASK.md §4.7 prose (two CLI-attestation flags + two mechanical checks). The ratified `classify_task` decision tree from `research/spec-staleness-decision-formalization/output/SPEC.md §1` (Task 033 ST-2) is more sophisticated — it consumes five signals (todo_satisfaction, affects_paths_present, plan_anchors_live, goal_endorsed, successor_present) and emits one of four §4.7 buckets without any agent attestation. A follow-up Task SHOULD migrate the helper onto the SPEC's algorithm; the docstring of `tools/fm/check-task-lifecycle-classification.py` and the §4.7 prose in TASK.md both note the migration as pending.

### Pre-existing branch state (out of scope for Task 033)

`tools/check-governance.sh` returns non-zero on this branch due to issues introduced upstream of this Task and not within `task_affects_paths`:

1. `tasks/046-github-workflow-research/task.md` is missing the mandatory `## Todo` section (TASK.md §5). The Task 046 author owns this fix.
2. `tasks/readme.md` membership for Tasks 045 and 046 was missing from the index. Fixed in this commit as a §7.11 mechanical sync (covered by TASK.md §4.8 / §7.11 — any commit that touches `tasks/<NNN>-<slug>/` MUST update the index, and Task 045 / 046 were created on parallel branches without the same-commit update).

After fixing #2, only #1 remains. It is filed here so a downstream maintainer can attribute it correctly; this Task does not modify Task 046.

### What worked

- The brief's "Phase A parallel" decomposition let ST-1 / ST-2 / ST-3 / ST-4 run concurrently with minimal coordination cost. Both research subagents respected the "do not modify governance specs" boundary and committed with the parent task's `Task 033 ST-N` trailer convention.
- The `tools/fm/_core.py` shared frontmatter parser made ST-3 and ST-4 ~80 LOC each rather than re-implementing YAML parsing.
- The supersession-reciprocity escape hatch in ST-3's algorithm correctly distinguishes legitimate `updated`-predecessor / live-successor pairs from genuine collisions; all four current collisions correctly trip the ERROR.

## Closure

All Goal conditions (a)–(f) satisfied:

- (a) Duplicate `task_id` collisions mechanically detected — `tools/fm/check-duplicate-task-id.py` ships with five passing tests; wired into `tools/check-governance.sh`.
- (b) `updated` vs `abandoned` lifecycle boundary has a deterministic decision helper — `tools/fm/check-task-lifecycle-classification.py` ships with nine passing tests; cross-references the ratified ST-2 algorithm SPEC.
- (c) `T.B.SUP.1` supersession-blocker-inheritance Gherkin scenario added to TASK.md §6.
- (d) TASK.md §3.3 cross-links to `research/flexible-frontmatter-toolchain/output/SPEC.md` §3–§4 with explicit anchor.
- (e) New `skill_*` L2 quickref subsection in TASK.md §3.3 citing `research/skills-namespace-ontology/output/SPEC.md` as authoritative source.
- (f) New `adr_*` L2 quickref subsection in TASK.md §3.3 citing `maintenance/schemas/header-ontology.json:208`.

Plus the Task 040 §A row §2.1+§2.2 MERGE: TASK.md §1 lifts the Planner / Tech-Lead framing as a single-paragraph addition.
