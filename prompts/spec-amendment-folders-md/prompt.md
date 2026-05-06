---
type: prompt
status: active
slug: spec-amendment-folders-md
summary: "Land the FOLDERS.md edits per Task 036 (a)-(d): F.1.1 explicit provider-research + `/decisions/` exemption clause, F.5 promotion to MUST (cross-references ST-1), F.6 dual-surface guidance (cross-references ST-2), ≥5 Gherkin scenarios per..."
created: 2026-05-06
updated: 2026-05-06
prompt_kind: task-spec
prompt_framework: RISEN+ReAct
prompt_target_agent: "Claude Code"
prompt_relates_to_task: folders-spec-integration
prompt_spawned_from_research: ""
---

# ST-3: Spec Amendment — FOLDERS.md — Task-Spec Prompt

## Framework

RISEN+ReAct. The prompt declares the framework in frontmatter (`prompt_framework: RISEN+ReAct`) and restates it here for `fm-validate` header conformance. The R/I/S/E sections below carry the canonical roles; a final **Constraints** section groups normative scope/failure rules per repo convention.

## R — Role

You are the **main-agent** dispatched to execute subtask ST-3 of [Task folders-spec-integration](../../tasks/036-folders-spec-integration/task.md). Your remit is bounded by the Acceptance Criteria in [`brief.md`](./brief.md); you MUST NOT expand scope beyond those criteria without surfacing the divergence in `friction-log.md`.

**Parallelism:** Phase B (sequential) — depends on ST-1, ST-2. MUST wait for Phase A converge..

## I — Input

- ST-1 implementation: `tools/check-readme-frontmatter.py`.
- ST-2 implementation: `tools/check-audit-graph-consistency.py`.
- `research/governance-specs-update-research/output/SPEC.md` §3 (FOLDERS.md amendments).
- `maintenance/schemas/header-ontology.json:208` (decisions/ pattern).
- `tasks/036-folders-spec-integration/task.md` — parent task chain-level context.

## S — Steps

1. Satisfy acceptance criterion: FOLDERS.md F.1.1 explicitly enumerates `/research/<provider>/<slug>/` + `/decisions/` as exempt.
2. Satisfy acceptance criterion: FOLDERS.md F.5 is MUST (not SHOULD) and cites the ST-1 linter.
3. Satisfy acceptance criterion: FOLDERS.md F.6 documents dual-surface; cites ST-2 as the consistency check.
4. Satisfy acceptance criterion: ≥5 Gherkin scenarios anchored F.B.1-F.B.5 land in a new "## Acceptance Criteria" section.
5. Satisfy acceptance criterion: `tools/check-governance.sh` exits 0 (including ST-1 / ST-2).
6. Run `tools/check-governance.sh` and resolve every ERROR before committing.
7. Author or update `tasks/036-folders-spec-integration/friction-log.md` (or note that none is required for this subtask) and commit per the parent task's commit-message convention.

## E — Expectations

- FOLDERS.md F.1.1 explicitly enumerates `/research/<provider>/<slug>/` + `/decisions/` as exempt.
- FOLDERS.md F.5 is MUST (not SHOULD) and cites the ST-1 linter.
- FOLDERS.md F.6 documents dual-surface; cites ST-2 as the consistency check.
- ≥5 Gherkin scenarios anchored F.B.1-F.B.5 land in a new "## Acceptance Criteria" section.
- `tools/check-governance.sh` exits 0 (including ST-1 / ST-2).
- `tools/check-governance.sh` exits 0 on the produced commit.
- Commit message follows the parent task's convention; the commit cites `Task 036 ST-3` in its trailer.

## Constraints

- Dependency: ST-1, ST-2 MUST land first.
- MUST NOT trigger the subtask's Falsification clause: Wrong cut **iff** F.5 promotion to MUST creates retroactive ERRORs against existing readmes (would break the working tree). Mitigation: ST-1 linter is authored before ST-3 amendment lands; the linter is run pre-amendment to surface fixable readmes; readmes are fixed in the same commit as the amendment.
- MUST NOT inline this prompt's Goal/Inputs/Acceptance back into the subtask file — the subtask body is now a thin pointer per Task 041.
- MUST run `tools/check-governance.sh` before pushing; a non-zero exit MUST block the push.
- SHOULD cite the parent task's `task_id` in any commit-message trailer for traceability.
