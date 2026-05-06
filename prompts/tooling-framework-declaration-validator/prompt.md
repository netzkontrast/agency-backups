---
type: prompt
status: active
slug: tooling-framework-declaration-validator
summary: "Ship `tools/check-prompt-framework-declaration.py` that scans `/prompts/<slug>/prompt.md` and verifies (a) frontmatter `prompt_framework` is set to a canonical value (`RISEN`, `RISE-DX`, `ReAct`, `RISEN+ReAct`, `CoT`, or the post-ST-1-de..."
created: 2026-05-06
updated: 2026-05-06
prompt_kind: task-spec
prompt_framework: RISEN+ReAct
prompt_target_agent: "Claude Code"
prompt_relates_to_task: prompt-spec-integration
prompt_spawned_from_research: ""
---

# ST-3: `check-prompt-framework-declaration` — Mechanizes P.5.2 — Task-Spec Prompt

## Framework

RISEN+ReAct. The prompt declares the framework in frontmatter (`prompt_framework: RISEN+ReAct`) and restates it here for `fm-validate` header conformance. The R/I/S/E sections below carry the canonical roles; a final **Constraints** section groups normative scope/failure rules per repo convention.

## R — Role

You are the **main-agent** dispatched to execute subtask ST-3 of [Task prompt-spec-integration](../../tasks/034-prompt-spec-integration/task.md). Your remit is bounded by the Acceptance Criteria in [`brief.md`](./brief.md); you MUST NOT expand scope beyond those criteria without surfacing the divergence in `friction-log.md`.

**Parallelism:** Phase A (parallel-grouped, soft-blocked) — runs alongside ST-2; soft-depends on ST-1 SPEC §3 framework-list extension..

## I — Input

- ST-1 output: `research/prompt-engineering-principle-mechanizability/output/SPEC.md` §3 framework-declaration recipe.
- `PROMPT.md` §4.3 (canonical framework list).
- All `/prompts/<slug>/prompt.md` (test corpus).
- `tools/fm/_core.py` (frontmatter parser).
- `tools/fm/extract.py --section Framework` (body section extraction).
- `tasks/034-prompt-spec-integration/task.md` — parent task chain-level context.

## S — Steps

1. Satisfy acceptance criterion: **Surface.** `python3 tools/check-prompt-framework-declaration.py <prompt.md>` exits 0 (pass) or 2 (WARN).
2. Satisfy acceptance criterion: **Checks.** Frontmatter+body framework declaration consistency per ST-1 SPEC §3.
3. Satisfy acceptance criterion: **Tests.** `tests/test_prompt_framework_declaration.py` covers: missing frontmatter, missing section, mismatch between frontmatter and section, valid declaration.
4. Satisfy acceptance criterion: **Integration.** `tools/check-governance.sh` runs WARN-tier on changed `/prompts/<slug>/prompt.md`.
5. Run `tools/check-governance.sh` and resolve every ERROR before committing.
6. Author or update `tasks/034-prompt-spec-integration/friction-log.md` (or note that none is required for this subtask) and commit per the parent task's commit-message convention.

## E — Expectations

- **Surface.** `python3 tools/check-prompt-framework-declaration.py <prompt.md>` exits 0 (pass) or 2 (WARN).
- **Checks.** Frontmatter+body framework declaration consistency per ST-1 SPEC §3.
- **Tests.** `tests/test_prompt_framework_declaration.py` covers: missing frontmatter, missing section, mismatch between frontmatter and section, valid declaration.
- **Integration.** `tools/check-governance.sh` runs WARN-tier on changed `/prompts/<slug>/prompt.md`.
- `tools/check-governance.sh` exits 0 on the produced commit.
- Commit message follows the parent task's convention; the commit cites `Task 034 ST-3` in its trailer.

## Constraints

- Dependency: ST-1 MUST land first.
- MUST NOT trigger the subtask's Falsification clause: Wrong cut **iff** ST-1's empirical FPR study shows P.5.2 framework-declaration enforcement causes >20% false-positive rate on the existing prompt corpus. Mitigation: the linter is WARN-tier only.
- MUST NOT inline this prompt's Goal/Inputs/Acceptance back into the subtask file — the subtask body is now a thin pointer per Task 041.
- MUST run `tools/check-governance.sh` before pushing; a non-zero exit MUST block the push.
- SHOULD cite the parent task's `task_id` in any commit-message trailer for traceability.
