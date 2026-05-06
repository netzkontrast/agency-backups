---
type: prompt
status: active
slug: tooling-workspace-cleanliness-linter
summary: "Ship `tools/check-workspace-cleanliness.py` that scans staged `/research/<slug>/workspace/` paths for execution-script stragglers (`.py`, `.sh`, `.log`) and emits a WARN diagnostic. Closes the R.4.4 enforcement gap (currently human-revie..."
created: 2026-05-06
updated: 2026-05-06
prompt_kind: task-spec
prompt_framework: RISEN+ReAct
prompt_target_agent: "Claude Code"
prompt_relates_to_task: research-spec-integration
---

# ST-2: `check-workspace-cleanliness` — Closes RESEARCH.md R.4.4 Gap — Task-Spec Prompt

## Framework

RISEN+ReAct. The prompt declares the framework in frontmatter (`prompt_framework: RISEN+ReAct`) and restates it here for `fm-validate` header conformance. The R/I/S/E sections below carry the canonical roles; a final **Constraints** section groups normative scope/failure rules per repo convention.

## R — Role

You are the **main-agent** dispatched to execute subtask ST-2 of [Task research-spec-integration](../../tasks/035-research-spec-integration/task.md). Your remit is bounded by the Acceptance Criteria in [`brief.md`](./brief.md); you MUST NOT expand scope beyond those criteria without surfacing the divergence in `friction-log.md`.

**Parallelism:** Phase A (parallel) — runs concurrently with ST-1, ST-3, ST-4. No inter-dependencies..

## I — Input

- `RESEARCH.md` R.4.4 (rule statement).
- `tools/fm/_core.py` (path iteration helpers).
- `tools/adr/runlog.py` (diagnostic format prior art).
- `tasks/035-research-spec-integration/task.md` — parent task chain-level context.

## S — Steps

1. The agent MUST produce the artefact required by acceptance criterion: **Surface.** `python3 tools/check-workspace-cleanliness.py [<paths>]` (defaults to scanning `research/`).
2. The agent MUST produce the artefact required by acceptance criterion: **Heuristic.** Flag any `.py`/`.sh`/`.log` under `/research/<slug>/workspace/`; honour `.cleanignore`.
3. The agent MUST produce the artefact required by acceptance criterion: **Diagnostic format.** `<relpath>::WARN:R.4.4:execution-script-not-cleaned`.
4. The agent MUST produce the artefact required by acceptance criterion: **Tests.** `tests/test_workspace_cleanliness.py` covers: clean workspace, straggler `.py`, ignored path, missing-workspace edge case.
5. The agent MUST produce the artefact required by acceptance criterion: **Integration.** `tools/check-governance.sh` runs WARN-tier.
6. The agent MUST verify every Acceptance Criterion enumerated in [`brief.md`](./brief.md) holds against the produced artefacts; on any failure the agent MUST iterate the relevant implementation step rather than weakening the criterion.
7. The agent MUST run `tools/check-governance.sh` and resolve every ERROR before committing; a non-zero exit MUST block the commit.
8. The agent SHOULD author or update `tasks/035-research-spec-integration/friction-log.md` per FRUSTRATED.md FL[0-3] when frictions arise; absence of frictions MAY be recorded as `FL: 0`.
9. The agent MUST commit with a message that names `Task 035 ST-2` in its trailer; the agent MUST NOT push (the maintainer pushes after review).

## E — Expectations

- **Surface.** `python3 tools/check-workspace-cleanliness.py [<paths>]` (defaults to scanning `research/`).
- **Heuristic.** Flag any `.py`/`.sh`/`.log` under `/research/<slug>/workspace/`; honour `.cleanignore`.
- **Diagnostic format.** `<relpath>::WARN:R.4.4:execution-script-not-cleaned`.
- **Tests.** `tests/test_workspace_cleanliness.py` covers: clean workspace, straggler `.py`, ignored path, missing-workspace edge case.
- **Integration.** `tools/check-governance.sh` runs WARN-tier.
- `tools/check-governance.sh` exits 0 on the produced commit.
- Commit message follows the parent task's convention; the commit cites `Task 035 ST-2` in its trailer.

## Constraints

- Dependency: None. Phase A.
- MUST NOT trigger the subtask's Falsification clause: Wrong cut **iff** legitimate `.py` files for the worked-example need to live under `/workspace/` long-term. Mitigation: the linter accepts a `.cleanignore` file at the workspace root listing exempt paths with rationale.
- MUST NOT inline this prompt's Goal/Inputs/Acceptance back into the subtask file — the subtask body is now a thin pointer per Task 041.
- MUST run `tools/check-governance.sh` before pushing; a non-zero exit MUST block the push.
- SHOULD cite the parent task's `task_id` in any commit-message trailer for traceability.
