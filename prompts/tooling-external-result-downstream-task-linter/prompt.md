---
type: prompt
status: active
slug: tooling-external-result-downstream-task-linter
summary: "Ship `tools/check-external-result-downstream-task.py` that, for every staged `/research/<provider>/<slug>/result.md`, verifies a corresponding `/tasks/<NNN>-<slug-or-related>/task.md` exists and references the result. Closes R.6.5 (curre..."
created: 2026-05-06
updated: 2026-05-06
prompt_kind: task-spec
prompt_framework: RISEN+ReAct
prompt_target_agent: "Claude Code"
prompt_relates_to_task: research-spec-integration
prompt_spawned_from_research: ""
---

# ST-3: `check-external-result-downstream-task` — Closes RESEARCH.md R.6.5 Gap — Task-Spec Prompt

## Framework

RISEN+ReAct. The prompt declares the framework in frontmatter (`prompt_framework: RISEN+ReAct`) and restates it here for `fm-validate` header conformance. The R/I/S/E sections below carry the canonical roles; a final **Constraints** section groups normative scope/failure rules per repo convention.

## R — Role

You are the **main-agent** dispatched to execute subtask ST-3 of [Task research-spec-integration](../../tasks/035-research-spec-integration/task.md). Your remit is bounded by the Acceptance Criteria in [`brief.md`](./brief.md); you MUST NOT expand scope beyond those criteria without surfacing the divergence in `friction-log.md`.

**Parallelism:** Phase A (parallel) — runs concurrently with ST-1, ST-2, ST-4. No inter-dependencies..

## I — Input

- `RESEARCH.md` §6.5 (rule statement).
- `tools/fm/query.py` (frontmatter query for `task_affects_paths` cross-reference).
- Existing precedent pairs:
- `research/gemini/agency-adr-governance-spec/` ↔ `tasks/027-adr-spec-research-synthesis/`
- `research/gemini/superclaude-agency-orchestration-spec/` ↔ `tasks/040-superclaude-spec-evaluation/`
- `tasks/035-research-spec-integration/task.md` — parent task chain-level context.

## S — Steps

1. Satisfy acceptance criterion: **Surface.** `python3 tools/check-external-result-downstream-task.py [<paths>]`.
2. Satisfy acceptance criterion: **Algorithm.** Detect any `/research/<provider>/<slug>/result.md` lacking a back-linked open Task; emit ERROR-tier diagnostic.
3. Satisfy acceptance criterion: **Diagnostic format.** `<result.md path>::ERROR:R.6.5:no-downstream-task`.
4. Satisfy acceptance criterion: **Tests.** `tests/test_external_result_downstream_task.py` covers: linked Task (pass), missing Task (fail), differently-slugged but back-linked Task (pass via `task_affects_paths`).
5. Satisfy acceptance criterion: **Integration.** `tools/check-governance.sh` step `[1/5]` extension; ERROR-tier (gating).
6. Run `tools/check-governance.sh` and resolve every ERROR before committing.
7. Author or update `tasks/035-research-spec-integration/friction-log.md` (or note that none is required for this subtask) and commit per the parent task's commit-message convention.

## E — Expectations

- **Surface.** `python3 tools/check-external-result-downstream-task.py [<paths>]`.
- **Algorithm.** Detect any `/research/<provider>/<slug>/result.md` lacking a back-linked open Task; emit ERROR-tier diagnostic.
- **Diagnostic format.** `<result.md path>::ERROR:R.6.5:no-downstream-task`.
- **Tests.** `tests/test_external_result_downstream_task.py` covers: linked Task (pass), missing Task (fail), differently-slugged but back-linked Task (pass via `task_affects_paths`).
- **Integration.** `tools/check-governance.sh` step `[1/5]` extension; ERROR-tier (gating).
- `tools/check-governance.sh` exits 0 on the produced commit.
- Commit message follows the parent task's convention; the commit cites `Task 035 ST-3` in its trailer.

## Constraints

- Dependency: None. Phase A.
- MUST NOT trigger the subtask's Falsification clause: Wrong cut **iff** the slug-matching heuristic produces false negatives because downstream Tasks legitimately use a different slug (precedent: Task 027 = `adr-spec-research-synthesis` for `/research/gemini/agency-adr-governance-spec/`). Mitigation: the linter accepts a back-link via `task_affects_paths` containing the result.md path, OR `task_uses_prompts` containing the provider slug.
- MUST NOT inline this prompt's Goal/Inputs/Acceptance back into the subtask file — the subtask body is now a thin pointer per Task 041.
- MUST run `tools/check-governance.sh` before pushing; a non-zero exit MUST block the push.
- SHOULD cite the parent task's `task_id` in any commit-message trailer for traceability.
