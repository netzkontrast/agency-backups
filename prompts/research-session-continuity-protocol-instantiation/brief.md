---
type: brief
status: active
slug: research-session-continuity-protocol-instantiation-brief
summary: "Brief for prompt research-session-continuity-protocol-instantiation — extracted from tasks/035-research-spec-integration/subtasks/01-research-session-continuity-protocol-instantiation.md per Task 041 (PR #70 review C.3 audit-graph repair)."
created: 2026-05-06
updated: 2026-05-06
---

# Brief — ST-1: Research — Session-Continuity Protocol Instantiation

## Raw User Request

> Extract the inlined Execution Brief from `tasks/035-research-spec-integration/subtasks/01-research-session-continuity-protocol-instantiation.md` (ST-1) into a registered `/prompts/<slug>/` artefact, restoring the `task_uses_prompts ↔ prompt_relates_to_task` audit-graph edge severed in PR #70 (review finding C.3).

## Target Audience

The dispatched executor for [Task 035 `research-spec-integration`](../../tasks/035-research-spec-integration/task.md), specifically subtask ST-1 (01-research-session-continuity-protocol-instantiation.md). Default executor: **main-agent**.

## Intended Model / Agent

Claude Code (or any agent that satisfies the executor declaration in the parent subtask file).

## Use-Case Context

This prompt drives subtask ST-1 of [Task research-spec-integration](../../tasks/035-research-spec-integration/task.md). The parent task's chain-level rationale lives in its `task.md`; this brief records only the subtask's local goal + inputs + acceptance + dependencies + effort, lifted verbatim from the subtask file at extraction time.

**Parallelism:** Phase A (parallel) — runs concurrently with ST-2, ST-3, ST-4. No inter-dependencies.

## Goal (from subtask)

Produce `research/session-continuity-protocol-instantiation/output/SPEC.md` containing a concrete, file-format-spec'd instantiation of the abstract Spec-I from `agentic-session-continuity-spec/output/SPEC.md`. Output: (a) `state.md` schema (frontmatter + sections), (b) checkpoint emission cadence (every N synthesis steps), (c) epistemic-delta encoding format, (d) restore procedure for a fresh-context successor agent, (e) integration points with RESEARCH.md §4.

## Falsification (from subtask)

Wrong cut **iff** the checkpoint cadence cannot fit in <10% additional token cost vs. uninstrumented runs. Mitigation: synthesis-step boundaries are natural checkpoint points; the cost is one file write per boundary.

## Inputs (from subtask)

- [`research/agentic-session-continuity-spec/output/SPEC.md`](../../../research/agentic-session-continuity-spec/output/SPEC.md) (Spec-G/H/I).
- [`RESEARCH.md`](../../../RESEARCH.md) §4 (workspace structure).
- [`research/adr-spec-research-synthesis/output/SPEC.md`](../../../research/adr-spec-research-synthesis/output/SPEC.md) — example multi-session workspace.
- [`maintenance/schemas/header-ontology.json`](../../../maintenance/schemas/header-ontology.json) — frontmatter schema constraint.

## Acceptance Criteria (from subtask)

1. SPEC.md at `/research/session-continuity-protocol-instantiation/output/SPEC.md`.
2. §1 includes a complete `state.md` example for a real research workspace (Task 027 as worked example).
3. §2 cadence rule cites empirical token cost on the worked example.
4. §3 delta-encoding format is JSON-Schema-validated.
5. §4 restore-procedure pseudocode runs against the worked example without error.
6. §5 contains a verbatim RESEARCH.md §4 amendment ready for Task 035 ST-5 to lift.
7. `research_phase: complete`; reflection friction-log.

## Dependencies (from subtask)

None. Phase A.

## Estimated Effort (from subtask)

Large (~5 hours; protocol design + worked example + token measurement).
