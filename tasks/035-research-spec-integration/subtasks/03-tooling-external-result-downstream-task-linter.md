---
type: note
status: draft
slug: task-035-st3-tooling-external-result-downstream-task-linter
summary: "Subtask ST-3: ship tools/check-external-result-downstream-task.py — closes R.6.5 by enforcing every /research/<provider>/<slug>/result.md has a corresponding open Task in /tasks/."
created: 2026-05-06
updated: 2026-05-06
---

# ST-3: `check-external-result-downstream-task` — Closes RESEARCH.md R.6.5 Gap

**Executor:** main-agent

**Insertion point:** `[1/5]` frontmatter linter extension — runs as part of `tools/fm/validate.py --type-check` when external-research files are staged.

## Goal

Ship `tools/check-external-result-downstream-task.py` that, for every staged `/research/<provider>/<slug>/result.md`, verifies a corresponding `/tasks/<NNN>-<slug-or-related>/task.md` exists and references the result. Closes R.6.5 (currently human-review only).

## Falsification

Wrong cut **iff** the slug-matching heuristic produces false negatives because downstream Tasks legitimately use a different slug (precedent: Task 027 = `adr-spec-research-synthesis` for `/research/gemini/agency-adr-governance-spec/`). Mitigation: the linter accepts a back-link via `task_affects_paths` containing the result.md path, OR `task_uses_prompts` containing the provider slug.

## Inputs

- `RESEARCH.md` §6.5 (rule statement).
- `tools/fm/query.py` (frontmatter query for `task_affects_paths` cross-reference).
- Existing precedent pairs:
  - `research/gemini/agency-adr-governance-spec/` ↔ `tasks/027-adr-spec-research-synthesis/`
  - `research/gemini/superclaude-agency-orchestration-spec/` ↔ `tasks/040-superclaude-spec-evaluation/`

## Acceptance Criteria

1. **Surface.** `python3 tools/check-external-result-downstream-task.py [<paths>]`.
2. **Algorithm.** Detect any `/research/<provider>/<slug>/result.md` lacking a back-linked open Task; emit ERROR-tier diagnostic.
3. **Diagnostic format.** `<result.md path>::ERROR:R.6.5:no-downstream-task`.
4. **Tests.** `tests/test_external_result_downstream_task.py` covers: linked Task (pass), missing Task (fail), differently-slugged but back-linked Task (pass via `task_affects_paths`).
5. **Integration.** `tools/check-governance.sh` step `[1/5]` extension; ERROR-tier (gating).

## Dependencies

None. Phase A.

## Estimated Effort

Small (~100 LOC + 80 LOC tests).
