---
type: prompt
status: active
slug: tooling-narrative-ontology-load-discipline
summary: "Ship `tools/check-narrative-ontology-load.py` that scans a recent session's tool-call log and emits a WARN when the 215-entry `maintenance/schemas/narrative-ontology/ontology.json` was loaded by an agent whose Task did not declare `task_..."
created: 2026-05-06
updated: 2026-05-06
prompt_kind: task-spec
prompt_framework: RISEN+ReAct
prompt_target_agent: "Claude Code"
prompt_relates_to_task: agents-spec-integration
prompt_spawned_from_research: ""
---

# ST-2: `check-narrative-ontology-load` — NO.5 Enforcement — Task-Spec Prompt

## Framework

RISEN+ReAct. The prompt declares the framework in frontmatter (`prompt_framework: RISEN+ReAct`) and restates it here for `fm-validate` header conformance. The R/I/S/E sections below carry the canonical roles; a final **Constraints** section groups normative scope/failure rules per repo convention.

## R — Role

You are the **main-agent** dispatched to execute subtask ST-2 of [Task agents-spec-integration](../../tasks/032-agents-spec-integration/task.md). Your remit is bounded by the Acceptance Criteria in [`brief.md`](./brief.md); you MUST NOT expand scope beyond those criteria without surfacing the divergence in `friction-log.md`.

**Parallelism:** Phase A (parallel) — runs concurrently with ST-1, ST-3, ST-4. No inter-dependencies..

## I — Input

- [`AGENTS.md`](../../../AGENTS.md) §NO.1–NO.6 (rules to enforce).
- `tools/dramatica-nav/` (existing narrative-ontology tooling).
- `maintenance/schemas/narrative-ontology/ontology.json`.
- `tools/fm/_core.py` (frontmatter parser).
- `tasks/032-agents-spec-integration/task.md` — parent task chain-level context.

## S — Steps

1. Execute the following instruction block faithfully — it is the verbatim Execution Brief from the parent subtask file:

```text
Implement tools/check-narrative-ontology-load.py for the netzkontrast/agency
repo (current branch).

Read first: AGENTS.md §NO.1–NO.6, tools/fm/_core.py, tools/check-governance.sh.

Acceptance:
  1. CLI as documented.
  2. Heuristic uses task_affects_paths + git diff --cached.
  3. Tests in tests/test_narrative_ontology_load.py.
  4. Integration into tools/check-governance.sh.
  5. Cookbook note in tools/readme.md.

Constraints:
  - Python 3.11 stdlib only.
  - No git binary dependency beyond `git diff --cached --name-only`.
  - Do not gate (exit 1) — WARN-tier (exit 2) only.

When done:
  python3 -m unittest discover -s tests
  python3 tools/check-governance.sh
  Commit "feat(tools): NO.5 narrative-ontology load discipline linter (Task 032 ST-2)".
  Do NOT push.
```
2. Verify every Acceptance Criterion in [`brief.md`](./brief.md) is satisfied by the produced artefacts.
3. Run `tools/check-governance.sh` and resolve every ERROR before committing.

## E — Expectations

- **Surface.** `python3 tools/check-narrative-ontology-load.py <task-folder>` exits 0 (no violation) or 2 (WARN — narrative ontology loaded in non-narrative task).
- **Heuristic.** WARN when (a) the active task's `task_affects_paths` does NOT include `skills/dramatica-*` / `skills/ncp-*` / `skills/novel-*` AND (b) the staged diff shows reads against `maintenance/schemas/narrative-ontology/`.
- **Tests.** `tests/test_narrative_ontology_load.py` covers: positive case (narrative task loads — pass), negative case (non-narrative task loads — WARN), edge case (no task context — exit 0).
- **Integration.** Listed in `tools/check-governance.sh` as a WARN-tier check (not gating).
- **Cookbook entry.** Add a one-line note to `tools/readme.md` describing the new linter.
- `tools/check-governance.sh` exits 0 on the produced commit.
- Commit message follows the parent task's convention; the commit cites `Task 032 ST-2` in its trailer.

## Constraints

- Dependency: None. Phase A.
- MUST NOT trigger the subtask's Falsification clause: Wrong cut **iff** session-trace data is unavailable to the linter at commit time. Mitigation: tools can read the active task's frontmatter `task_affects_paths` field and the staged-files diff to infer narrative-vs-non-narrative scope without needing live tool-call traces.
- MUST NOT inline this prompt's Goal/Inputs/Acceptance back into the subtask file — the subtask body is now a thin pointer per Task 041.
- MUST run `tools/check-governance.sh` before pushing; a non-zero exit MUST block the push.
- SHOULD cite the parent task's `task_id` in any commit-message trailer for traceability.
