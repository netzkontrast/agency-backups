---
type: brief
status: active
slug: tooling-framework-declaration-validator-brief
summary: "Brief for prompt tooling-framework-declaration-validator — extracted from tasks/034-prompt-spec-integration/subtasks/03-tooling-framework-declaration-validator.md per Task 041 (PR #70 review C.3 audit-graph repair)."
created: 2026-05-06
updated: 2026-05-06
---

# Brief — ST-3: `check-prompt-framework-declaration` — Mechanizes P.5.2

## Raw User Request

> Extract the inlined Execution Brief from `tasks/034-prompt-spec-integration/subtasks/03-tooling-framework-declaration-validator.md` (ST-3) into a registered `/prompts/<slug>/` artefact, restoring the `task_uses_prompts ↔ prompt_relates_to_task` audit-graph edge severed in PR #70 (review finding C.3).

## Target Audience

The dispatched executor for [Task 034 `prompt-spec-integration`](../../tasks/034-prompt-spec-integration/task.md), specifically subtask ST-3 (03-tooling-framework-declaration-validator.md). Default executor: **main-agent**.

## Intended Model / Agent

Claude Code (or any agent that satisfies the executor declaration in the parent subtask file).

## Use-Case Context

This prompt drives subtask ST-3 of [Task prompt-spec-integration](../../tasks/034-prompt-spec-integration/task.md). The parent task's chain-level rationale lives in its `task.md`; this brief records only the subtask's local goal + inputs + acceptance + dependencies + effort, lifted verbatim from the subtask file at extraction time.

**Parallelism:** Phase A (parallel-grouped, soft-blocked) — runs alongside ST-2; soft-depends on ST-1 SPEC §3 framework-list extension.

**Insertion point:** `[opt]` WARN-tier — runs only on changed `/prompts/<slug>/prompt.md` files.

## Goal (from subtask)

Ship `tools/check-prompt-framework-declaration.py` that scans `/prompts/<slug>/prompt.md` and verifies (a) frontmatter `prompt_framework` is set to a canonical value (`RISEN`, `RISE-DX`, `ReAct`, `RISEN+ReAct`, `CoT`, or the post-ST-1-decision-tree-extended set), (b) a `## Framework` section in the body exists and matches the frontmatter value, (c) the body declares why this framework fits.

## Falsification (from subtask)

Wrong cut **iff** ST-1's empirical FPR study shows P.5.2 framework-declaration enforcement causes >20% false-positive rate on the existing prompt corpus. Mitigation: the linter is WARN-tier only.

## Inputs (from subtask)

- ST-1 output: `research/prompt-engineering-principle-mechanizability/output/SPEC.md` §3 framework-declaration recipe.
- `PROMPT.md` §4.3 (canonical framework list).
- All `/prompts/<slug>/prompt.md` (test corpus).
- `tools/fm/_core.py` (frontmatter parser).
- `tools/fm/extract.py --section Framework` (body section extraction).

## Acceptance Criteria (from subtask)

1. **Surface.** `python3 tools/check-prompt-framework-declaration.py <prompt.md>` exits 0 (pass) or 2 (WARN).
2. **Checks.** Frontmatter+body framework declaration consistency per ST-1 SPEC §3.
3. **Tests.** `tests/test_prompt_framework_declaration.py` covers: missing frontmatter, missing section, mismatch between frontmatter and section, valid declaration.
4. **Integration.** `tools/check-governance.sh` runs WARN-tier on changed `/prompts/<slug>/prompt.md`.

## Dependencies (from subtask)

ST-1 MUST land first.

## Estimated Effort (from subtask)

Small (~80 LOC + 60 LOC tests).
