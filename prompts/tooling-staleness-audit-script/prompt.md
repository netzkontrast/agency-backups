---
type: prompt
status: active
slug: tooling-staleness-audit-script
summary: "Ship `tools/maintenance/staleness-audit.py` that, given the active task corpus, assigns each open task to one of {still-accurate, drifted, completed-by-drift, no-longer-desirable} per the deterministic algorithm in ST-2's SPEC. Configura..."
created: 2026-05-06
updated: 2026-05-06
prompt_kind: task-spec
prompt_framework: RISEN+ReAct
prompt_target_agent: "Claude Code"
prompt_relates_to_task: maintenance-spec-integration
---

# ST-3: `staleness-audit` — MAINTENANCE.md §3.4 Mechanization — Task-Spec Prompt

## Framework

RISEN+ReAct. The prompt declares the framework in frontmatter (`prompt_framework: RISEN+ReAct`) and restates it here for `fm-validate` header conformance. The R/I/S/E sections below carry the canonical roles; a final **Constraints** section groups normative scope/failure rules per repo convention.

## R — Role

You are the **maintenance-agent** dispatched to execute subtask ST-3 of [Task maintenance-spec-integration](../../tasks/039-maintenance-spec-integration/task.md). Your remit is bounded by the Acceptance Criteria in [`brief.md`](./brief.md); you MUST NOT expand scope beyond those criteria without surfacing the divergence in `friction-log.md`.

**Parallelism:** Phase A (parallel-grouped, soft-blocked) — runs alongside ST-1/ST-4/ST-5 but soft-depends on ST-2 SPEC. May ship with stub algorithm + upgrade post-ST-2..

## I — Input

- ST-2 output: `research/spec-staleness-decision-formalization/output/SPEC.md` §1 algorithm + §2 signals.
- `tools/fm/_core.py`, `tools/fm/query.py`.
- `tools/adr/graph.py` (cycle detection prior art for blocker chains).
- All `tasks/*/task.md` (test corpus).
- `tasks/039-maintenance-spec-integration/task.md` — parent task chain-level context.

## S — Steps

1. The agent MUST produce the artefact required by acceptance criterion: **Surface.** `python3 tools/maintenance/staleness-audit.py [--stale-days N]`.
2. The agent MUST produce the artefact required by acceptance criterion: **Algorithm.** Implements ST-2 SPEC §1 decision tree.
3. The agent MUST produce the artefact required by acceptance criterion: **Output.** Table of (task_id, current_status, bucket, evidence) — markdown for human; JSON via `--format json` for tooling.
4. The agent MUST produce the artefact required by acceptance criterion: **Tests.** `tests/maintenance/test_staleness_audit.py` covers each bucket using ST-2 SPEC §3 walkthroughs as fixtures.
5. The agent MUST produce the artefact required by acceptance criterion: **Integration.** Invoked by the nightly run; output appended to `maintenance/run-log.md`.
6. The agent MUST verify every Acceptance Criterion enumerated in [`brief.md`](./brief.md) holds against the produced artefacts; on any failure the agent MUST iterate the relevant implementation step rather than weakening the criterion.
7. The agent MUST run `tools/check-governance.sh` and resolve every ERROR before committing; a non-zero exit MUST block the commit.
8. The agent SHOULD author or update `tasks/039-maintenance-spec-integration/friction-log.md` per FRUSTRATED.md FL[0-3] when frictions arise; absence of frictions MAY be recorded as `FL: 0`.
9. The agent MUST commit with a message that names `Task 039 ST-3` in its trailer; the agent MUST NOT push (the maintainer pushes after review).

## E — Expectations

- **Surface.** `python3 tools/maintenance/staleness-audit.py [--stale-days N]`.
- **Algorithm.** Implements ST-2 SPEC §1 decision tree.
- **Output.** Table of (task_id, current_status, bucket, evidence) — markdown for human; JSON via `--format json` for tooling.
- **Tests.** `tests/maintenance/test_staleness_audit.py` covers each bucket using ST-2 SPEC §3 walkthroughs as fixtures.
- **Integration.** Invoked by the nightly run; output appended to `maintenance/run-log.md`.
- `tools/check-governance.sh` exits 0 on the produced commit.
- Commit message follows the parent task's convention; the commit cites `Task 039 ST-3` in its trailer.

## Constraints

- Dependency: ST-2 (research) MUST land first.
- MUST NOT trigger the subtask's Falsification clause: Wrong cut **iff** the algorithm's signal-extractor recipes (from ST-2 SPEC §2) cannot be implemented in stdlib + git. Mitigation: ST-2's "≤5 signals; mechanically extractable" constraint is verified during ST-2 authoring.
- MUST NOT inline this prompt's Goal/Inputs/Acceptance back into the subtask file — the subtask body is now a thin pointer per Task 041.
- MUST run `tools/check-governance.sh` before pushing; a non-zero exit MUST block the push.
- SHOULD cite the parent task's `task_id` in any commit-message trailer for traceability.
