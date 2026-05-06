---
type: note
status: draft
slug: task-036-st2-tooling-audit-graph-consistency-checker
summary: "Subtask ST-2: ship tools/check-audit-graph-consistency.py — warns when body Markdown links reference sibling folders without matching frontmatter linkage."
created: 2026-05-06
updated: 2026-05-06
---

# ST-2: `check-audit-graph-consistency` — F.6 Dual-Surface Drift

**Executor:** main-agent

**Insertion point:** `[opt]` WARN-tier — advisory only, since FOLDERS.md §6 explicitly encourages body links for human navigation.

## Goal

Ship `tools/check-audit-graph-consistency.py` that, for every body-level Markdown link in operational-folder `task.md` / `prompt.md` / `readme.md` referencing a sibling folder (`tasks/<NNN>-<slug>/`, `prompts/<slug>/`, `research/<slug>/`), verifies a corresponding frontmatter linkage exists (`task_uses_prompts`, `task_spawns_research`, `prompt_relates_to_task`, `prompt_spawned_from_research`, `research_executes_prompt`).

## Falsification

Wrong cut **iff** legitimate human-navigation body links (e.g., references to a sibling task in prose) trigger >25% false positives. Mitigation: the linter only flags links to *operational* folders matching the audit-graph pattern, ignoring all other Markdown anchors.

## Inputs

- `FOLDERS.md` §6 (audit-graph dual-surface rule).
- `tools/fm/query.py` (frontmatter linkage query).
- All operational folders (test corpus).

## Acceptance Criteria

1. **Surface.** `python3 tools/check-audit-graph-consistency.py [<paths>]`.
2. **Heuristic.** Parse body Markdown links; for each operational-folder target, verify reciprocal frontmatter key.
3. **Diagnostic format.** `<relpath>::WARN:F.6:body-link-without-frontmatter:<target>`.
4. **Tests.** `tests/test_audit_graph_consistency.py` covers: link+frontmatter both present (pass), link only (warn), frontmatter only (no warn — body links are encouraged but not required).
5. **Integration.** WARN-tier `[opt]` in `tools/check-governance.sh`.

## Dependencies

None. Phase A.

## Estimated Effort

Medium (~120 LOC + 100 LOC tests; Markdown link parsing is the bulk).
