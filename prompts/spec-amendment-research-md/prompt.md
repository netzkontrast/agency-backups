---
type: prompt
status: active
slug: spec-amendment-research-md
summary: "Land the RESEARCH.md edits per Task 035 (a)-(g): §2.2 spec-chunking rule, §4 session-continuity reference, §5.7 trust-audit clause, R.4.3 prompt-snapshot mid-run disambiguation, ≥6 Gherkin scenarios per R.B.1-R.B.6 anchors, references to..."
created: 2026-05-06
updated: 2026-05-06
prompt_kind: task-spec
prompt_framework: RISEN+ReAct
prompt_target_agent: "Claude Code"
prompt_relates_to_task: research-spec-integration
---

# ST-5: Spec Amendment — RESEARCH.md — Task-Spec Prompt

## Framework

RISEN+ReAct. The prompt declares the framework in frontmatter (`prompt_framework: RISEN+ReAct`) and restates it here for `fm-validate` header conformance. The R/I/S/E sections below carry the canonical roles; a final **Constraints** section groups normative scope/failure rules per repo convention.

## R — Role

You are the **main-agent** dispatched to execute subtask ST-5 of [Task research-spec-integration](../../tasks/035-research-spec-integration/task.md). Your remit is bounded by the Acceptance Criteria in [`brief.md`](./brief.md); you MUST NOT expand scope beyond those criteria without surfacing the divergence in `friction-log.md`.

**Parallelism:** Phase B (sequential) — depends on ST-1, ST-2, ST-3, ST-4. MUST wait for all four to land..

## I — Input

- ST-1 output: `research/session-continuity-protocol-instantiation/output/SPEC.md`.
- ST-2/ST-3/ST-4 implementations.
- `research/agentic-eval-trust-improvement-spec/output/SPEC.md`.
- `research/spec-driven-research-agentic-workflows/output/SPEC.md` §spec-chunking.
- `research/agentic-session-continuity-spec/output/SPEC.md`.
- `tasks/035-research-spec-integration/task.md` — parent task chain-level context.

## S — Steps

1. The agent MUST produce the artefact required by acceptance criterion: RESEARCH.md §2.2 mandates spec-chunking for synthesis runs >50k tokens.
2. The agent MUST produce the artefact required by acceptance criterion: RESEARCH.md §4 references session-continuity protocol per ST-1 output.
3. The agent MUST produce the artefact required by acceptance criterion: RESEARCH.md §5.7 mandates trust-audit GATE invocation at `research_phase: complete`.
4. The agent MUST produce the artefact required by acceptance criterion: RESEARCH.md R.4.3 disambiguates mid-run prompt-snapshot policy (lock-at-start preferred).
5. The agent MUST produce the artefact required by acceptance criterion: RESEARCH.md §5 has ≥6 Gherkin scenarios per R.B.1-R.B.6 anchors.
6. The agent MUST produce the artefact required by acceptance criterion: `tools/check-governance.sh` exits 0.
7. The agent MUST verify every Acceptance Criterion enumerated in [`brief.md`](./brief.md) holds against the produced artefacts; on any failure the agent MUST iterate the relevant implementation step rather than weakening the criterion.
8. The agent MUST run `tools/check-governance.sh` and resolve every ERROR before committing; a non-zero exit MUST block the commit.
9. The agent SHOULD author or update `tasks/035-research-spec-integration/friction-log.md` per FRUSTRATED.md FL[0-3] when frictions arise; absence of frictions MAY be recorded as `FL: 0`.
10. The agent MUST commit with a message that names `Task 035 ST-5` in its trailer; the agent MUST NOT push (the maintainer pushes after review).

## E — Expectations

- RESEARCH.md §2.2 mandates spec-chunking for synthesis runs >50k tokens.
- RESEARCH.md §4 references session-continuity protocol per ST-1 output.
- RESEARCH.md §5.7 mandates trust-audit GATE invocation at `research_phase: complete`.
- RESEARCH.md R.4.3 disambiguates mid-run prompt-snapshot policy (lock-at-start preferred).
- RESEARCH.md §5 has ≥6 Gherkin scenarios per R.B.1-R.B.6 anchors.
- `tools/check-governance.sh` exits 0.
- `tools/check-governance.sh` exits 0 on the produced commit.
- Commit message follows the parent task's convention; the commit cites `Task 035 ST-5` in its trailer.

## Constraints

- Dependency: ST-1, ST-2, ST-3, ST-4 MUST land first.
- MUST NOT trigger the subtask's Falsification clause: Wrong cut **iff** the §5.7 trust-audit clause references a cross-workspace AGGREGATOR (that belongs to Task 039). Mitigation: ST-5 cites ST-4's per-workspace GATE only.
- MUST NOT inline this prompt's Goal/Inputs/Acceptance back into the subtask file — the subtask body is now a thin pointer per Task 041.
- MUST run `tools/check-governance.sh` before pushing; a non-zero exit MUST block the push.
- SHOULD cite the parent task's `task_id` in any commit-message trailer for traceability.
