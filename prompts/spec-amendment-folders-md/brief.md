---
type: brief
status: active
slug: spec-amendment-folders-md-brief
summary: "Brief for prompt spec-amendment-folders-md — extracted from tasks/036-folders-spec-integration/subtasks/03-spec-amendment-folders-md.md per Task 041 (PR #70 review C.3 audit-graph repair)."
created: 2026-05-06
updated: 2026-05-06
---

# Brief — ST-3: Spec Amendment — FOLDERS.md

## Raw User Request

> Extract the inlined Execution Brief from `tasks/036-folders-spec-integration/subtasks/03-spec-amendment-folders-md.md` (ST-3) into a registered `/prompts/<slug>/` artefact, restoring the `task_uses_prompts ↔ prompt_relates_to_task` audit-graph edge severed in PR #70 (review finding C.3).

## Target Audience

The dispatched executor for [Task 036 `folders-spec-integration`](../../tasks/036-folders-spec-integration/task.md), specifically subtask ST-3 (03-spec-amendment-folders-md.md). Default executor: **main-agent**.

## Intended Model / Agent

Claude Code (or any agent that satisfies the executor declaration in the parent subtask file).

## Use-Case Context

This prompt drives subtask ST-3 of [Task folders-spec-integration](../../tasks/036-folders-spec-integration/task.md). The parent task's chain-level rationale lives in its `task.md`; this brief records only the subtask's local goal + inputs + acceptance + dependencies + effort, lifted verbatim from the subtask file at extraction time.

**Parallelism:** Phase B (sequential) — depends on ST-1, ST-2. MUST wait for Phase A converge.

## Goal (from subtask)

Land the FOLDERS.md edits per Task 036 (a)-(d): F.1.1 explicit provider-research + `/decisions/` exemption clause, F.5 promotion to MUST (cross-references ST-1), F.6 dual-surface guidance (cross-references ST-2), ≥5 Gherkin scenarios per F.B.1-F.B.5 anchors.

## Falsification (from subtask)

Wrong cut **iff** F.5 promotion to MUST creates retroactive ERRORs against existing readmes (would break the working tree). Mitigation: ST-1 linter is authored before ST-3 amendment lands; the linter is run pre-amendment to surface fixable readmes; readmes are fixed in the same commit as the amendment.

## Inputs (from subtask)

- ST-1 implementation: `tools/check-readme-frontmatter.py`.
- ST-2 implementation: `tools/check-audit-graph-consistency.py`.
- `research/governance-specs-update-research/output/SPEC.md` §3 (FOLDERS.md amendments).
- `maintenance/schemas/header-ontology.json:208` (decisions/ pattern).

## Acceptance Criteria (from subtask)

1. FOLDERS.md F.1.1 explicitly enumerates `/research/<provider>/<slug>/` + `/decisions/` as exempt.
2. FOLDERS.md F.5 is MUST (not SHOULD) and cites the ST-1 linter.
3. FOLDERS.md F.6 documents dual-surface; cites ST-2 as the consistency check.
4. ≥5 Gherkin scenarios anchored F.B.1-F.B.5 land in a new "## Acceptance Criteria" section.
5. `tools/check-governance.sh` exits 0 (including ST-1 / ST-2).

## Dependencies (from subtask)

ST-1, ST-2 MUST land first.

## Estimated Effort (from subtask)

Small (~1 hour).
