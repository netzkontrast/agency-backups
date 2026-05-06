---
type: prompt
status: active
slug: research-session-continuity-protocol-instantiation
summary: "Produce `research/session-continuity-protocol-instantiation/output/SPEC.md` containing a concrete, file-format-spec'd instantiation of the abstract Spec-I from `agentic-session-continuity-spec/output/SPEC.md`. Output: (a) `state.md` sche..."
created: 2026-05-06
updated: 2026-05-06
prompt_kind: task-spec
prompt_framework: RISEN+ReAct
prompt_target_agent: "Claude Code"
prompt_relates_to_task: research-spec-integration
---

# ST-1: Research — Session-Continuity Protocol Instantiation — Task-Spec Prompt

## Framework

RISEN+ReAct. The prompt declares the framework in frontmatter (`prompt_framework: RISEN+ReAct`) and restates it here for `fm-validate` header conformance. The R/I/S/E sections below carry the canonical roles; a final **Constraints** section groups normative scope/failure rules per repo convention.

## R — Role

You are the **main-agent** dispatched to execute subtask ST-1 of [Task research-spec-integration](../../tasks/035-research-spec-integration/task.md). Your remit is bounded by the Acceptance Criteria in [`brief.md`](./brief.md); you MUST NOT expand scope beyond those criteria without surfacing the divergence in `friction-log.md`.

**Parallelism:** Phase A (parallel) — runs concurrently with ST-2, ST-3, ST-4. No inter-dependencies..

## I — Input

- [`research/agentic-session-continuity-spec/output/SPEC.md`](../../../research/agentic-session-continuity-spec/output/SPEC.md) (Spec-G/H/I).
- [`RESEARCH.md`](../../../RESEARCH.md) §4 (workspace structure).
- [`research/adr-spec-research-synthesis/output/SPEC.md`](../../../research/adr-spec-research-synthesis/output/SPEC.md) — example multi-session workspace.
- [`maintenance/schemas/header-ontology.json`](../../../maintenance/schemas/header-ontology.json) — frontmatter schema constraint.
- `tasks/035-research-spec-integration/task.md` — parent task chain-level context.

## S — Steps

1. The agent MUST treat the following preamble as authoritative orientation before executing any subsequent step: Run research-prompt-optimizer Phase 1–3. Skip Phase 1 askuser; intent canonical. Render to /research/session-continuity-protocol-instantiation/research-prompt.md. Execute and produce /research/session-continuity-protocol-instantiation/output/SPEC.md. Author reflection/friction-log.md. Run tools/check-governance.sh. Commit "research(session-continuity): file-format instantiation of Spec-I (Task 035 ST-1)". Do NOT push.
2. The agent MUST verify every Acceptance Criterion enumerated in [`brief.md`](./brief.md) holds against the produced artefacts; on any failure the agent MUST iterate the relevant implementation step rather than weakening the criterion.
3. The agent MUST run `tools/check-governance.sh` and resolve every ERROR before committing; a non-zero exit MUST block the commit.
4. The agent SHOULD author or update `tasks/035-research-spec-integration/friction-log.md` per FRUSTRATED.md FL[0-3] when frictions arise; absence of frictions MAY be recorded as `FL: 0`.
5. The agent MUST commit with a message that names `Task 035 ST-1` in its trailer; the agent MUST NOT push (the maintainer pushes after review).

## E — Expectations

- SPEC.md at `/research/session-continuity-protocol-instantiation/output/SPEC.md`.
- §1 includes a complete `state.md` example for a real research workspace (Task 027 as worked example).
- §2 cadence rule cites empirical token cost on the worked example.
- §3 delta-encoding format is JSON-Schema-validated.
- §4 restore-procedure pseudocode runs against the worked example without error.
- §5 contains a verbatim RESEARCH.md §4 amendment ready for Task 035 ST-5 to lift.
- `research_phase: complete`; reflection friction-log.
- `tools/check-governance.sh` exits 0 on the produced commit.
- Commit message follows the parent task's convention; the commit cites `Task 035 ST-1` in its trailer.

## Constraints

- Dependency: None. Phase A.
- MUST NOT trigger the subtask's Falsification clause: Wrong cut **iff** the checkpoint cadence cannot fit in <10% additional token cost vs. uninstrumented runs. Mitigation: synthesis-step boundaries are natural checkpoint points; the cost is one file write per boundary.
- MUST NOT inline this prompt's Goal/Inputs/Acceptance back into the subtask file — the subtask body is now a thin pointer per Task 041.
- MUST run `tools/check-governance.sh` before pushing; a non-zero exit MUST block the push.
- SHOULD cite the parent task's `task_id` in any commit-message trailer for traceability.
