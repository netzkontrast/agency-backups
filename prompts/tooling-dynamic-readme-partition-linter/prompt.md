---
type: prompt
status: active
slug: tooling-dynamic-readme-partition-linter
summary: "Ship `tools/maintenance/dynamic-readme-partition.py` that scans operational-folder `readme.md` files and verifies the static/dynamic section partition: static sections (Purpose, Navigation, Assumptions Log) live above the `<!-- BEGIN DYN..."
created: 2026-05-06
updated: 2026-05-06
prompt_kind: task-spec
prompt_framework: RISEN+ReAct
prompt_target_agent: "Claude Code"
prompt_relates_to_task: maintenance-spec-integration
---

# ST-4: `dynamic-readme-partition` — Operationalizes repo-maintenance-protocol-spec §3.1 — Task-Spec Prompt

## Framework

RISEN+ReAct. The prompt declares the framework in frontmatter (`prompt_framework: RISEN+ReAct`) and restates it here for `fm-validate` header conformance. The R/I/S/E sections below carry the canonical roles; a final **Constraints** section groups normative scope/failure rules per repo convention.

## R — Role

You are the **maintenance-agent** dispatched to execute subtask ST-4 of [Task maintenance-spec-integration](../../tasks/039-maintenance-spec-integration/task.md). Your remit is bounded by the Acceptance Criteria in [`brief.md`](./brief.md); you MUST NOT expand scope beyond those criteria without surfacing the divergence in `friction-log.md`.

**Parallelism:** Phase A (parallel) — runs concurrently with ST-1, ST-2, ST-3, ST-5. No inter-dependencies..

## I — Input

- `research/repo-maintenance-protocol-spec/output/SPEC.md` §3.1 (partition rule).
- All operational-folder `readme.md` (test corpus).
- `tools/fm/extract.py --section`.
- `tasks/039-maintenance-spec-integration/task.md` — parent task chain-level context.

## S — Steps

1. The agent MUST produce the artefact required by acceptance criterion: **Surface.** `python3 tools/maintenance/dynamic-readme-partition.py [<paths>]`.
2. The agent MUST produce the artefact required by acceptance criterion: **Heuristic.** Detect `<!-- BEGIN DYNAMIC -->` / `<!-- END DYNAMIC -->` marker pair; verify section-name allocation per the static/dynamic taxonomy.
3. The agent MUST produce the artefact required by acceptance criterion: **Diagnostic format.** `<relpath>::WARN:M.B.6:<missing-marker|misplaced-section>:<details>`.
4. The agent MUST produce the artefact required by acceptance criterion: **Tests.** `tests/maintenance/test_dynamic_readme_partition.py` covers: partitioned readme (pass), no-markers (advisory warn), section-in-wrong-half (warn).
5. The agent MUST produce the artefact required by acceptance criterion: **Integration.** WARN-tier `[opt]` in `tools/check-governance.sh`.
6. The agent MUST verify every Acceptance Criterion enumerated in [`brief.md`](./brief.md) holds against the produced artefacts; on any failure the agent MUST iterate the relevant implementation step rather than weakening the criterion.
7. The agent MUST run `tools/check-governance.sh` and resolve every ERROR before committing; a non-zero exit MUST block the commit.
8. The agent SHOULD author or update `tasks/039-maintenance-spec-integration/friction-log.md` per FRUSTRATED.md FL[0-3] when frictions arise; absence of frictions MAY be recorded as `FL: 0`.
9. The agent MUST commit with a message that names `Task 039 ST-4` in its trailer; the agent MUST NOT push (the maintainer pushes after review).

## E — Expectations

- **Surface.** `python3 tools/maintenance/dynamic-readme-partition.py [<paths>]`.
- **Heuristic.** Detect `<!-- BEGIN DYNAMIC -->` / `<!-- END DYNAMIC -->` marker pair; verify section-name allocation per the static/dynamic taxonomy.
- **Diagnostic format.** `<relpath>::WARN:M.B.6:<missing-marker|misplaced-section>:<details>`.
- **Tests.** `tests/maintenance/test_dynamic_readme_partition.py` covers: partitioned readme (pass), no-markers (advisory warn), section-in-wrong-half (warn).
- **Integration.** WARN-tier `[opt]` in `tools/check-governance.sh`.
- `tools/check-governance.sh` exits 0 on the produced commit.
- Commit message follows the parent task's convention; the commit cites `Task 039 ST-4` in its trailer.

## Constraints

- Dependency: None. Phase A.
- MUST NOT trigger the subtask's Falsification clause: Wrong cut **iff** existing readmes have no markers and the linter retroactively breaks them. Mitigation: WARN-tier only; readmes lacking markers emit a one-time "consider partitioning" diagnostic, never an ERROR.
- MUST NOT inline this prompt's Goal/Inputs/Acceptance back into the subtask file — the subtask body is now a thin pointer per Task 041.
- MUST run `tools/check-governance.sh` before pushing; a non-zero exit MUST block the push.
- SHOULD cite the parent task's `task_id` in any commit-message trailer for traceability.
