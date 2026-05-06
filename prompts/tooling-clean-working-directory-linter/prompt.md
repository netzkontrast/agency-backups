---
type: prompt
status: active
slug: tooling-clean-working-directory-linter
summary: "Ship `tools/check-clean-working-directory.py` that scans staged paths for `.py`/`.sh` scratchpads outside designated tool/test directories. Closes PC.1.1 (currently relies on agent discipline). Exempts `/decisions/`, `/tools/`, `/tests/`..."
created: 2026-05-06
updated: 2026-05-06
prompt_kind: task-spec
prompt_framework: RISEN+ReAct
prompt_target_agent: "Claude Code"
prompt_relates_to_task: pre-commit-spec-integration
---

# ST-2: `check-clean-working-directory` — Closes PRE_COMMIT.md PC.1.1 Gap — Task-Spec Prompt

## Framework

RISEN+ReAct. The prompt declares the framework in frontmatter (`prompt_framework: RISEN+ReAct`) and restates it here for `fm-validate` header conformance. The R/I/S/E sections below carry the canonical roles; a final **Constraints** section groups normative scope/failure rules per repo convention.

## R — Role

You are the **main-agent** dispatched to execute subtask ST-2 of [Task pre-commit-spec-integration](../../tasks/037-pre-commit-spec-integration/task.md). Your remit is bounded by the Acceptance Criteria in [`brief.md`](./brief.md); you MUST NOT expand scope beyond those criteria without surfacing the divergence in `friction-log.md`.

**Parallelism:** Phase A (parallel) — runs concurrently with ST-1, ST-3. No inter-dependencies..

## I — Input

- `PRE_COMMIT.md` PC.1.1.
- `FOLDERS.md` §8 exemption table.
- `tools/fm/_core.py`.
- `tasks/037-pre-commit-spec-integration/task.md` — parent task chain-level context.

## S — Steps

1. The agent MUST produce the artefact required by acceptance criterion: **Surface.** `python3 tools/check-clean-working-directory.py [<paths>]`.
2. The agent MUST produce the artefact required by acceptance criterion: **Heuristic.** Flag `.py`/`.sh`/`.log` outside the §8-exempt set; honour `.script-allowlist`.
3. The agent MUST produce the artefact required by acceptance criterion: **Diagnostic format.** `<relpath>::WARN:PC.1.1:script-scratchpad`.
4. The agent MUST produce the artefact required by acceptance criterion: **Tests.** `tests/test_clean_working_directory.py` covers: clean tree, scratchpad-in-research/workspace (warn), scratchpad-in-/tools (pass), allowlisted (pass).
5. The agent MUST produce the artefact required by acceptance criterion: **Integration.** ERROR-tier in step `[2/5]` of `tools/check-governance.sh`.
6. The agent MUST verify every Acceptance Criterion enumerated in [`brief.md`](./brief.md) holds against the produced artefacts; on any failure the agent MUST iterate the relevant implementation step rather than weakening the criterion.
7. The agent MUST run `tools/check-governance.sh` and resolve every ERROR before committing; a non-zero exit MUST block the commit.
8. The agent SHOULD author or update `tasks/037-pre-commit-spec-integration/friction-log.md` per FRUSTRATED.md FL[0-3] when frictions arise; absence of frictions MAY be recorded as `FL: 0`.
9. The agent MUST commit with a message that names `Task 037 ST-2` in its trailer; the agent MUST NOT push (the maintainer pushes after review).

## E — Expectations

- **Surface.** `python3 tools/check-clean-working-directory.py [<paths>]`.
- **Heuristic.** Flag `.py`/`.sh`/`.log` outside the §8-exempt set; honour `.script-allowlist`.
- **Diagnostic format.** `<relpath>::WARN:PC.1.1:script-scratchpad`.
- **Tests.** `tests/test_clean_working_directory.py` covers: clean tree, scratchpad-in-research/workspace (warn), scratchpad-in-/tools (pass), allowlisted (pass).
- **Integration.** ERROR-tier in step `[2/5]` of `tools/check-governance.sh`.
- `tools/check-governance.sh` exits 0 on the produced commit.
- Commit message follows the parent task's convention; the commit cites `Task 037 ST-2` in its trailer.

## Constraints

- Dependency: None. Phase A.
- MUST NOT trigger the subtask's Falsification clause: Wrong cut **iff** legitimate `.py` files (e.g., a one-off migration script kept in a task's notes for audit) trigger ERROR. Mitigation: the linter accepts a per-task `.script-allowlist` file with rationale, and emits a suggestion to relocate `.py` to `/tools/<slug>/` rather than block.
- MUST NOT inline this prompt's Goal/Inputs/Acceptance back into the subtask file — the subtask body is now a thin pointer per Task 041.
- MUST run `tools/check-governance.sh` before pushing; a non-zero exit MUST block the push.
- SHOULD cite the parent task's `task_id` in any commit-message trailer for traceability.
