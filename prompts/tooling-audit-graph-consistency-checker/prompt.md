---
type: prompt
status: active
slug: tooling-audit-graph-consistency-checker
summary: "Ship `tools/check-audit-graph-consistency.py` that, for every body-level Markdown link in operational-folder `task.md` / `prompt.md` / `readme.md` referencing a sibling folder (`tasks/<NNN>-<slug>/`, `prompts/<slug>/`, `research/<slug>/`..."
created: 2026-05-06
updated: 2026-05-06
prompt_kind: task-spec
prompt_framework: RISEN+ReAct
prompt_target_agent: "Claude Code"
prompt_relates_to_task: folders-spec-integration
---

# ST-2: `check-audit-graph-consistency` — F.6 Dual-Surface Drift — Task-Spec Prompt

## Framework

RISEN+ReAct. The prompt declares the framework in frontmatter (`prompt_framework: RISEN+ReAct`) and restates it here for `fm-validate` header conformance. The R/I/S/E sections below carry the canonical roles; a final **Constraints** section groups normative scope/failure rules per repo convention.

## R — Role

You are the **main-agent** dispatched to execute subtask ST-2 of [Task folders-spec-integration](../../tasks/036-folders-spec-integration/task.md). Your remit is bounded by the Acceptance Criteria in [`brief.md`](./brief.md); you MUST NOT expand scope beyond those criteria without surfacing the divergence in `friction-log.md`.

**Parallelism:** Phase A (parallel) — runs concurrently with ST-1. No inter-dependencies..

## I — Input

- `FOLDERS.md` §6 (audit-graph dual-surface rule).
- `tools/fm/query.py` (frontmatter linkage query).
- All operational folders (test corpus).
- `tasks/036-folders-spec-integration/task.md` — parent task chain-level context.

## S — Steps

1. The agent MUST produce the artefact required by acceptance criterion: **Surface.** `python3 tools/check-audit-graph-consistency.py [<paths>]`.
2. The agent MUST produce the artefact required by acceptance criterion: **Heuristic.** Parse body Markdown links; for each operational-folder target, verify reciprocal frontmatter key.
3. The agent MUST produce the artefact required by acceptance criterion: **Diagnostic format.** `<relpath>::WARN:F.6:body-link-without-frontmatter:<target>`.
4. The agent MUST produce the artefact required by acceptance criterion: **Tests.** `tests/test_audit_graph_consistency.py` covers: link+frontmatter both present (pass), link only (warn), frontmatter only (no warn — body links are encouraged but not required).
5. The agent MUST produce the artefact required by acceptance criterion: **Integration.** WARN-tier `[opt]` in `tools/check-governance.sh`.
6. The agent MUST verify every Acceptance Criterion enumerated in [`brief.md`](./brief.md) holds against the produced artefacts; on any failure the agent MUST iterate the relevant implementation step rather than weakening the criterion.
7. The agent MUST run `tools/check-governance.sh` and resolve every ERROR before committing; a non-zero exit MUST block the commit.
8. The agent SHOULD author or update `tasks/036-folders-spec-integration/friction-log.md` per FRUSTRATED.md FL[0-3] when frictions arise; absence of frictions MAY be recorded as `FL: 0`.
9. The agent MUST commit with a message that names `Task 036 ST-2` in its trailer; the agent MUST NOT push (the maintainer pushes after review).

## E — Expectations

- **Surface.** `python3 tools/check-audit-graph-consistency.py [<paths>]`.
- **Heuristic.** Parse body Markdown links; for each operational-folder target, verify reciprocal frontmatter key.
- **Diagnostic format.** `<relpath>::WARN:F.6:body-link-without-frontmatter:<target>`.
- **Tests.** `tests/test_audit_graph_consistency.py` covers: link+frontmatter both present (pass), link only (warn), frontmatter only (no warn — body links are encouraged but not required).
- **Integration.** WARN-tier `[opt]` in `tools/check-governance.sh`.
- `tools/check-governance.sh` exits 0 on the produced commit.
- Commit message follows the parent task's convention; the commit cites `Task 036 ST-2` in its trailer.

## Constraints

- Dependency: None. Phase A.
- MUST NOT trigger the subtask's Falsification clause: Wrong cut **iff** legitimate human-navigation body links (e.g., references to a sibling task in prose) trigger >25% false positives. Mitigation: the linter only flags links to *operational* folders matching the audit-graph pattern, ignoring all other Markdown anchors.
- MUST NOT inline this prompt's Goal/Inputs/Acceptance back into the subtask file — the subtask body is now a thin pointer per Task 041.
- MUST run `tools/check-governance.sh` before pushing; a non-zero exit MUST block the push.
- SHOULD cite the parent task's `task_id` in any commit-message trailer for traceability.
