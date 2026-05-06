---
type: prompt
status: active
slug: spec-amendment-task-md
summary: "Land the TASK.md edits per Task 033 (a)-(f): close T.8.1 enforcement gap (cross-link to ST-3 linter), refine §4.7 boundary using ST-2 algorithm, add §6 supersession-blocker scenario, cross-link §3.3 to flexible-frontmatter-toolchain SPEC..."
created: 2026-05-06
updated: 2026-05-06
prompt_kind: task-spec
prompt_framework: RISEN+ReAct
prompt_target_agent: "Claude Code"
prompt_relates_to_task: task-spec-integration
prompt_spawned_from_research: ""
---

# ST-5: Spec Amendment — TASK.md — Task-Spec Prompt

## Framework

RISEN+ReAct. The prompt declares the framework in frontmatter (`prompt_framework: RISEN+ReAct`) and restates it here for `fm-validate` header conformance. The R/I/S/E sections below carry the canonical roles; a final **Constraints** section groups normative scope/failure rules per repo convention.

## R — Role

You are the **main-agent** dispatched to execute subtask ST-5 of [Task task-spec-integration](../../tasks/033-task-spec-integration/task.md). Your remit is bounded by the Acceptance Criteria in [`brief.md`](./brief.md); you MUST NOT expand scope beyond those criteria without surfacing the divergence in `friction-log.md`.

**Parallelism:** Phase B (sequential) — depends on ST-1, ST-2, ST-3 (and soft-depends on ST-4). MUST wait for Phase A converge..

## I — Input

- ST-1 output: `research/friction-pattern-synthesis/output/SPEC.md`.
- ST-2 output: `research/spec-staleness-decision-formalization/output/SPEC.md`.
- ST-3 implementation: `tools/fm/check-duplicate-task-id.py`.
- `research/skills-namespace-ontology/output/SPEC.md` (skill_* vocabulary).
- `research/flexible-frontmatter-toolchain/output/SPEC.md` §3-§4 (authoritative L2-namespace source).
- `maintenance/schemas/header-ontology.json:208` (types.adr registration).
- `tasks/033-task-spec-integration/task.md` — parent task chain-level context.

## S — Steps

1. Satisfy acceptance criterion: TASK.md §3.3 cross-references the flexible-frontmatter-toolchain SPEC + header-ontology.json with explicit version anchor.
2. Satisfy acceptance criterion: TASK.md §3.3 has new subsections enumerating `skill_*` (per skills-namespace-ontology) and `adr_*` (per types.adr registration).
3. Satisfy acceptance criterion: TASK.md §6 has the supersession-blocker scenario from task.md "Sample Gherkin" anchored `T.B.SUP.1`.
4. Satisfy acceptance criterion: TASK.md §4.7 algorithm is refined per ST-2's deterministic decision tree.
5. Satisfy acceptance criterion: TASK.md §8.1 enforcement note now states the rule is gated by ST-3's linter.
6. Satisfy acceptance criterion: **NEW (per Task 040 §A row §2.1+§2.2 MERGE):** TASK.md §1 prose lifts the *Planner / Tech-Lead* framing — a Task is the Planner-layer artefact (it decomposes work and coordinates dependencies); a Prompt is the Tech-Lead-layer artefact (it instructs the executor). One paragraph; no RFC-2119 mandates; no `/sc:spawn` / `/sc:task` skill citations (those are operator surface, not normative). Anchor any new Gherkin `T.B.SPAWN.1` or `T.B.DELEG.1` per Task 040 §B remap table.
7. Satisfy acceptance criterion: `tools/check-governance.sh` exits 0.
8. Run `tools/check-governance.sh` and resolve every ERROR before committing.
9. Author or update `tasks/033-task-spec-integration/friction-log.md` (or note that none is required for this subtask) and commit per the parent task's commit-message convention.

## E — Expectations

- TASK.md §3.3 cross-references the flexible-frontmatter-toolchain SPEC + header-ontology.json with explicit version anchor.
- TASK.md §3.3 has new subsections enumerating `skill_*` (per skills-namespace-ontology) and `adr_*` (per types.adr registration).
- TASK.md §6 has the supersession-blocker scenario from task.md "Sample Gherkin" anchored `T.B.SUP.1`.
- TASK.md §4.7 algorithm is refined per ST-2's deterministic decision tree.
- TASK.md §8.1 enforcement note now states the rule is gated by ST-3's linter.
- **NEW (per Task 040 §A row §2.1+§2.2 MERGE):** TASK.md §1 prose lifts the *Planner / Tech-Lead* framing — a Task is the Planner-layer artefact (it decomposes work and coordinates dependencies); a Prompt is the Tech-Lead-layer artefact (it instructs the executor). One paragraph; no RFC-2119 mandates; no `/sc:spawn` / `/sc:task` skill citations (those are operator surface, not normative). Anchor any new Gherkin `T.B.SPAWN.1` or `T.B.DELEG.1` per Task 040 §B remap table.
- `tools/check-governance.sh` exits 0.
- `tools/check-governance.sh` exits 0 on the produced commit.
- Commit message follows the parent task's convention; the commit cites `Task 033 ST-5` in its trailer.

## Constraints

- Dependency: ST-1, ST-2, ST-3 MUST land first.
- MUST NOT trigger the subtask's Falsification clause: Wrong cut **iff** §3.3 amendment duplicates schema content already in `maintenance/schemas/header-ontology.json` rather than cross-referencing it. Mitigation: the amendment cites the schema as authoritative and lists ≤3 keys per namespace inline as a quickref.
- MUST NOT inline this prompt's Goal/Inputs/Acceptance back into the subtask file — the subtask body is now a thin pointer per Task 041.
- MUST run `tools/check-governance.sh` before pushing; a non-zero exit MUST block the push.
- SHOULD cite the parent task's `task_id` in any commit-message trailer for traceability.
