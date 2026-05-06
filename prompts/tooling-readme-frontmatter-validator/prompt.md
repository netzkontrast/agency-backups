---
type: prompt
status: active
slug: tooling-readme-frontmatter-validator
summary: "Ship `tools/check-readme-frontmatter.py` that scans every operational-folder `readme.md` and verifies L1 Vault Core frontmatter is present (type, status, slug, summary, created, updated). Promotes F.5 from SHOULD to mechanically-enforced..."
created: 2026-05-06
updated: 2026-05-06
prompt_kind: task-spec
prompt_framework: RISEN+ReAct
prompt_target_agent: "Claude Code"
prompt_relates_to_task: folders-spec-integration
prompt_spawned_from_research: ""
---

# ST-1: `check-readme-frontmatter` — F.5 SHOULD → MUST — Task-Spec Prompt

## Framework

RISEN+ReAct. The prompt declares the framework in frontmatter (`prompt_framework: RISEN+ReAct`) and restates it here for `fm-validate` header conformance. The R/I/S/E sections below carry the canonical roles; a final **Constraints** section groups normative scope/failure rules per repo convention.

## R — Role

You are the **main-agent** dispatched to execute subtask ST-1 of [Task folders-spec-integration](../../tasks/036-folders-spec-integration/task.md). Your remit is bounded by the Acceptance Criteria in [`brief.md`](./brief.md); you MUST NOT expand scope beyond those criteria without surfacing the divergence in `friction-log.md`.

**Parallelism:** Phase A (parallel) — runs concurrently with ST-2. No inter-dependencies..

## I — Input

- `FOLDERS.md` F.5 (rule statement).
- `maintenance/schemas/header-ontology.json` (type-aware required-key matrix).
- `tools/fm/_core.py`, `tools/fm/validate.py`.
- `tasks/036-folders-spec-integration/task.md` — parent task chain-level context.

## S — Steps

1. Satisfy acceptance criterion: **Surface.** `python3 tools/check-readme-frontmatter.py [<paths>]`.
2. Satisfy acceptance criterion: **Checks.** L1 Vault Core key presence + slug-vs-folder agreement.
3. Satisfy acceptance criterion: **Tests.** `tests/test_readme_frontmatter.py` covers: clean, missing-key, slug-mismatch, exempt provider folder.
4. Satisfy acceptance criterion: **Integration.** ERROR-tier in step `[2/5]` of `tools/check-governance.sh`.
5. Run `tools/check-governance.sh` and resolve every ERROR before committing.
6. Author or update `tasks/036-folders-spec-integration/friction-log.md` (or note that none is required for this subtask) and commit per the parent task's commit-message convention.

## E — Expectations

- **Surface.** `python3 tools/check-readme-frontmatter.py [<paths>]`.
- **Checks.** L1 Vault Core key presence + slug-vs-folder agreement.
- **Tests.** `tests/test_readme_frontmatter.py` covers: clean, missing-key, slug-mismatch, exempt provider folder.
- **Integration.** ERROR-tier in step `[2/5]` of `tools/check-governance.sh`.
- `tools/check-governance.sh` exits 0 on the produced commit.
- Commit message follows the parent task's convention; the commit cites `Task 036 ST-1` in its trailer.

## Constraints

- Dependency: None. Phase A.
- MUST NOT trigger the subtask's Falsification clause: Wrong cut **iff** legitimate readmes (e.g. provider-folder `readme.md` under `/research/<provider>/`) need different frontmatter shape. Mitigation: the linter honours the `types.index` and `types.readme` patterns from `header-ontology.json` and falls back to L1 only.
- MUST NOT inline this prompt's Goal/Inputs/Acceptance back into the subtask file — the subtask body is now a thin pointer per Task 041.
- MUST run `tools/check-governance.sh` before pushing; a non-zero exit MUST block the push.
- SHOULD cite the parent task's `task_id` in any commit-message trailer for traceability.
