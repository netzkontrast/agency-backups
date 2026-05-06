---
type: note
status: active
slug: tooling-audit-graph-consistency-checker-brief
summary: "Brief for prompt tooling-audit-graph-consistency-checker — extracted from tasks/036-folders-spec-integration/subtasks/02-tooling-audit-graph-consistency-checker.md per Task 041 (PR #70 review C.3 audit-graph repair)."
created: 2026-05-06
updated: 2026-05-06
---

# Brief — ST-2: `check-audit-graph-consistency` — F.6 Dual-Surface Drift

## Raw User Request

> Extract the inlined Execution Brief from `tasks/036-folders-spec-integration/subtasks/02-tooling-audit-graph-consistency-checker.md` (ST-2) into a registered `/prompts/<slug>/` artefact, restoring the `task_uses_prompts ↔ prompt_relates_to_task` audit-graph edge severed in PR #70 (review finding C.3).

## Target Audience

The dispatched executor for [Task 036 `folders-spec-integration`](../../tasks/036-folders-spec-integration/task.md), specifically subtask ST-2 (02-tooling-audit-graph-consistency-checker.md). Default executor: **main-agent**.

## Intended Model / Agent

Claude Code (or any agent that satisfies the executor declaration in the parent subtask file).

## Use-Case Context

This prompt drives subtask ST-2 of [Task folders-spec-integration](../../tasks/036-folders-spec-integration/task.md). The parent task's chain-level rationale lives in its `task.md`; this brief records only the subtask's local goal + inputs + acceptance + dependencies + effort, lifted verbatim from the subtask file at extraction time.

**Parallelism:** Phase A (parallel) — runs concurrently with ST-1. No inter-dependencies.

**Insertion point:** `[opt]` WARN-tier — advisory only, since FOLDERS.md §6 explicitly encourages body links for human navigation.

## Goal (from subtask)

Ship `tools/check-audit-graph-consistency.py` that, for every body-level Markdown link in operational-folder `task.md` / `prompt.md` / `readme.md` referencing a sibling folder (`tasks/<NNN>-<slug>/`, `prompts/<slug>/`, `research/<slug>/`), verifies a corresponding frontmatter linkage exists (`task_uses_prompts`, `task_spawns_research`, `prompt_relates_to_task`, `prompt_spawned_from_research`, `research_executes_prompt`).

## Falsification (from subtask)

Wrong cut **iff** legitimate human-navigation body links (e.g., references to a sibling task in prose) trigger >25% false positives. Mitigation: the linter only flags links to *operational* folders matching the audit-graph pattern, ignoring all other Markdown anchors.

## Inputs (from subtask)

- `FOLDERS.md` §6 (audit-graph dual-surface rule).
- `tools/fm/query.py` (frontmatter linkage query).
- All operational folders (test corpus).

## Acceptance Criteria (from subtask)

1. **Surface.** `python3 tools/check-audit-graph-consistency.py [<paths>]`.
2. **Heuristic.** Parse body Markdown links; for each operational-folder target, verify reciprocal frontmatter key.
3. **Diagnostic format.** `<relpath>::WARN:F.6:body-link-without-frontmatter:<target>`.
4. **Tests.** `tests/test_audit_graph_consistency.py` covers: link+frontmatter both present (pass), link only (warn), frontmatter only (no warn — body links are encouraged but not required).
5. **Integration.** WARN-tier `[opt]` in `tools/check-governance.sh`.

## Dependencies (from subtask)

None. Phase A.

## Estimated Effort (from subtask)

Medium (~120 LOC + 100 LOC tests; Markdown link parsing is the bulk).
