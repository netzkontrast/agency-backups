---
type: prompt
status: active
slug: tooling-fl-declaration-linter
summary: "Ship `tools/check-fl-declaration.py` that parses `friction-log.md` (research) and PR-description `## Frustration Log` sections (standard), validates the presence of a canonical `Highest Frustration Level: FL[0-3]` line, and rejects task ..."
created: 2026-05-06
updated: 2026-05-06
prompt_kind: task-spec
prompt_framework: RISEN+ReAct
prompt_target_agent: "Claude Code"
prompt_relates_to_task: frustrated-spec-integration
---

# ST-2: `check-fl-declaration` — Mechanical FL-Declaration Gate — Task-Spec Prompt

## Framework

RISEN+ReAct. The prompt declares the framework in frontmatter (`prompt_framework: RISEN+ReAct`) and restates it here for `fm-validate` header conformance. The R/I/S/E sections below carry the canonical roles; a final **Constraints** section groups normative scope/failure rules per repo convention.

## R — Role

You are the **main-agent** dispatched to execute subtask ST-2 of [Task frustrated-spec-integration](../../tasks/038-frustrated-spec-integration/task.md). Your remit is bounded by the Acceptance Criteria in [`brief.md`](./brief.md); you MUST NOT expand scope beyond those criteria without surfacing the divergence in `friction-log.md`.

**Parallelism:** Phase A (parallel-grouped, soft-blocked) — runs alongside ST-1 but soft-depends on ST-1 SPEC §2 (variant-form set). Phase A may ship with strict canonical form + upgrade post-ST-1..

## I — Input

- ST-1 output: `research/fl0-value-justification/output/SPEC.md` §2 (variant forms in corpus).
- `FRUSTRATED.md` (FL.Log.1, FL.Log.2 — both surfaces).
- `TASK.md` §313 (existence enforcement; ST-2 adds substance enforcement).
- `tools/check-trust.py` (the existing extension point).
- `tools/adr/runlog.py` (diagnostic format prior art).
- `tasks/038-frustrated-spec-integration/task.md` — parent task chain-level context.

## S — Steps

1. The agent MUST produce the artefact required by acceptance criterion: **Surface.** `python3 tools/check-fl-declaration.py <task-folder-or-pr-body>` exits 0/1.
2. The agent MUST produce the artefact required by acceptance criterion: **Heuristic.** Parse `friction-log.md` first; fall back to PR-description `## Frustration Log` section; reject only if neither surface has a parseable declaration.
3. The agent MUST produce the artefact required by acceptance criterion: **Diagnostic format.** `<relpath>::ERROR:FR.B.4:<missing|malformed>:<details>`.
4. The agent MUST produce the artefact required by acceptance criterion: **Tests.** `tests/test_fl_declaration.py` covers: clean FL0, clean FL2, missing log, malformed value, both surfaces present (no warn).
5. The agent MUST produce the artefact required by acceptance criterion: **Integration.** Hooked into `tools/check-trust.py` for tasks transitioning to `done`.
6. The agent MUST verify every Acceptance Criterion enumerated in [`brief.md`](./brief.md) holds against the produced artefacts; on any failure the agent MUST iterate the relevant implementation step rather than weakening the criterion.
7. The agent MUST run `tools/check-governance.sh` and resolve every ERROR before committing; a non-zero exit MUST block the commit.
8. The agent SHOULD author or update `tasks/038-frustrated-spec-integration/friction-log.md` per FRUSTRATED.md FL[0-3] when frictions arise; absence of frictions MAY be recorded as `FL: 0`.
9. The agent MUST commit with a message that names `Task 038 ST-2` in its trailer; the agent MUST NOT push (the maintainer pushes after review).

## E — Expectations

- **Surface.** `python3 tools/check-fl-declaration.py <task-folder-or-pr-body>` exits 0/1.
- **Heuristic.** Parse `friction-log.md` first; fall back to PR-description `## Frustration Log` section; reject only if neither surface has a parseable declaration.
- **Diagnostic format.** `<relpath>::ERROR:FR.B.4:<missing|malformed>:<details>`.
- **Tests.** `tests/test_fl_declaration.py` covers: clean FL0, clean FL2, missing log, malformed value, both surfaces present (no warn).
- **Integration.** Hooked into `tools/check-trust.py` for tasks transitioning to `done`.
- `tools/check-governance.sh` exits 0 on the produced commit.
- Commit message follows the parent task's convention; the commit cites `Task 038 ST-2` in its trailer.

## Constraints

- Dependency: ST-1 SHOULD land first (provides variant-form set). If absent, ST-2 ships with the strict canonical form only and is upgraded post-ST-1.
- MUST NOT trigger the subtask's Falsification clause: Wrong cut **iff** the canonical-format regex is too strict and rejects legitimate variations (`Final FL: FL2`, `FL2 declared`). Mitigation: ST-1's research output enumerates the variant forms found in the existing corpus; the linter accepts that bounded set.
- MUST NOT inline this prompt's Goal/Inputs/Acceptance back into the subtask file — the subtask body is now a thin pointer per Task 041.
- MUST run `tools/check-governance.sh` before pushing; a non-zero exit MUST block the push.
- SHOULD cite the parent task's `task_id` in any commit-message trailer for traceability.
