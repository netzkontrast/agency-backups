---
type: note
status: active
slug: spec-amendment-task-md-brief
summary: "Brief for prompt spec-amendment-task-md — extracted from tasks/033-task-spec-integration/subtasks/05-spec-amendment-task-md.md per Task 041 (PR #70 review C.3 audit-graph repair)."
created: 2026-05-06
updated: 2026-05-06
---

# Brief — ST-5: Spec Amendment — TASK.md

## Raw User Request

> Extract the inlined Execution Brief from `tasks/033-task-spec-integration/subtasks/05-spec-amendment-task-md.md` (ST-5) into a registered `/prompts/<slug>/` artefact, restoring the `task_uses_prompts ↔ prompt_relates_to_task` audit-graph edge severed in PR #70 (review finding C.3).

## Target Audience

The dispatched executor for [Task 033 `task-spec-integration`](../../tasks/033-task-spec-integration/task.md), specifically subtask ST-5 (05-spec-amendment-task-md.md). Default executor: **main-agent**.

## Intended Model / Agent

Claude Code (or any agent that satisfies the executor declaration in the parent subtask file).

## Use-Case Context

This prompt drives subtask ST-5 of [Task task-spec-integration](../../tasks/033-task-spec-integration/task.md). The parent task's chain-level rationale lives in its `task.md`; this brief records only the subtask's local goal + inputs + acceptance + dependencies + effort, lifted verbatim from the subtask file at extraction time.

**Parallelism:** Phase B (sequential) — depends on ST-1, ST-2, ST-3 (and soft-depends on ST-4). MUST wait for Phase A converge.

## Goal (from subtask)

Land the TASK.md edits per Task 033 (a)-(f): close T.8.1 enforcement gap (cross-link to ST-3 linter), refine §4.7 boundary using ST-2 algorithm, add §6 supersession-blocker scenario, cross-link §3.3 to flexible-frontmatter-toolchain SPEC, add `skill_*` + `adr_*` L2 subsections.

## Falsification (from subtask)

Wrong cut **iff** §3.3 amendment duplicates schema content already in `maintenance/schemas/header-ontology.json` rather than cross-referencing it. Mitigation: the amendment cites the schema as authoritative and lists ≤3 keys per namespace inline as a quickref.

## Inputs (from subtask)

- ST-1 output: `research/friction-pattern-synthesis/output/SPEC.md`.
- ST-2 output: `research/spec-staleness-decision-formalization/output/SPEC.md`.
- ST-3 implementation: `tools/fm/check-duplicate-task-id.py`.
- `research/skills-namespace-ontology/output/SPEC.md` (skill_* vocabulary).
- `research/flexible-frontmatter-toolchain/output/SPEC.md` §3-§4 (authoritative L2-namespace source).
- `maintenance/schemas/header-ontology.json:208` (types.adr registration).

## Acceptance Criteria (from subtask)

1. TASK.md §3.3 cross-references the flexible-frontmatter-toolchain SPEC + header-ontology.json with explicit version anchor.
2. TASK.md §3.3 has new subsections enumerating `skill_*` (per skills-namespace-ontology) and `adr_*` (per types.adr registration).
3. TASK.md §6 has the supersession-blocker scenario from task.md "Sample Gherkin" anchored `T.B.SUP.1`.
4. TASK.md §4.7 algorithm is refined per ST-2's deterministic decision tree.
5. TASK.md §8.1 enforcement note now states the rule is gated by ST-3's linter.
6. **NEW (per Task 040 §A row §2.1+§2.2 MERGE):** TASK.md §1 prose lifts the *Planner / Tech-Lead* framing — a Task is the Planner-layer artefact (it decomposes work and coordinates dependencies); a Prompt is the Tech-Lead-layer artefact (it instructs the executor). One paragraph; no RFC-2119 mandates; no `/sc:spawn` / `/sc:task` skill citations (those are operator surface, not normative). Anchor any new Gherkin `T.B.SPAWN.1` or `T.B.DELEG.1` per Task 040 §B remap table.
7. `tools/check-governance.sh` exits 0.

## Dependencies (from subtask)

ST-1, ST-2, ST-3 MUST land first.

## Estimated Effort (from subtask)

Medium (~2 hours; multiple section edits + cross-reference verification).
