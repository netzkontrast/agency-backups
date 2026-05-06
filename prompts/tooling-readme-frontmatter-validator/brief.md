---
type: brief
status: active
slug: tooling-readme-frontmatter-validator-brief
summary: "Brief for prompt tooling-readme-frontmatter-validator — extracted from tasks/036-folders-spec-integration/subtasks/01-tooling-readme-frontmatter-validator.md per Task 041 (PR #70 review C.3 audit-graph repair)."
created: 2026-05-06
updated: 2026-05-06
---

# Brief — ST-1: `check-readme-frontmatter` — F.5 SHOULD → MUST

## Raw User Request

> Extract the inlined Execution Brief from `tasks/036-folders-spec-integration/subtasks/01-tooling-readme-frontmatter-validator.md` (ST-1) into a registered `/prompts/<slug>/` artefact, restoring the `task_uses_prompts ↔ prompt_relates_to_task` audit-graph edge severed in PR #70 (review finding C.3).

## Target Audience

The dispatched executor for [Task 036 `folders-spec-integration`](../../tasks/036-folders-spec-integration/task.md), specifically subtask ST-1 (01-tooling-readme-frontmatter-validator.md). Default executor: **main-agent**.

## Intended Model / Agent

Claude Code (or any agent that satisfies the executor declaration in the parent subtask file).

## Use-Case Context

This prompt drives subtask ST-1 of [Task folders-spec-integration](../../tasks/036-folders-spec-integration/task.md). The parent task's chain-level rationale lives in its `task.md`; this brief records only the subtask's local goal + inputs + acceptance + dependencies + effort, lifted verbatim from the subtask file at extraction time.

**Parallelism:** Phase A (parallel) — runs concurrently with ST-2. No inter-dependencies.

**Insertion point:** `[2/5]` directory-structure linter — extends `tools/lint-structure.py`.

## Goal (from subtask)

Ship `tools/check-readme-frontmatter.py` that scans every operational-folder `readme.md` and verifies L1 Vault Core frontmatter is present (type, status, slug, summary, created, updated). Promotes F.5 from SHOULD to mechanically-enforced MUST in the post-Task-035 amendment.

## Falsification (from subtask)

Wrong cut **iff** legitimate readmes (e.g. provider-folder `readme.md` under `/research/<provider>/`) need different frontmatter shape. Mitigation: the linter honours the `types.index` and `types.readme` patterns from `header-ontology.json` and falls back to L1 only.

## Inputs (from subtask)

- `FOLDERS.md` F.5 (rule statement).
- `maintenance/schemas/header-ontology.json` (type-aware required-key matrix).
- `tools/fm/_core.py`, `tools/fm/validate.py`.

## Acceptance Criteria (from subtask)

1. **Surface.** `python3 tools/check-readme-frontmatter.py [<paths>]`.
2. **Checks.** L1 Vault Core key presence + slug-vs-folder agreement.
3. **Tests.** `tests/test_readme_frontmatter.py` covers: clean, missing-key, slug-mismatch, exempt provider folder.
4. **Integration.** ERROR-tier in step `[2/5]` of `tools/check-governance.sh`.

## Dependencies (from subtask)

None. Phase A.

## Estimated Effort (from subtask)

Small (~80 LOC + 60 LOC tests).
