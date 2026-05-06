---
type: prompt
status: active
slug: research-fl0-value-justification
summary: "Produce `research/fl0-value-justification/output/SPEC.md` answering the question 'what does an FL0 entry contribute upstream that an absent log does not'. Inputs: every closed-task friction log. Outputs: (a) FL0-frequency stats, (b) qual..."
created: 2026-05-06
updated: 2026-05-06
prompt_kind: task-spec
prompt_framework: RISEN+ReAct
prompt_target_agent: "Claude Code"
prompt_relates_to_task: frustrated-spec-integration
prompt_spawned_from_research: ""
---

# ST-1: Research — FL0 Value Justification — Task-Spec Prompt

## Framework

RISEN+ReAct. The prompt declares the framework in frontmatter (`prompt_framework: RISEN+ReAct`) and restates it here for `fm-validate` header conformance. The R/I/S/E sections below carry the canonical roles; a final **Constraints** section groups normative scope/failure rules per repo convention.

## R — Role

You are the **main-agent** dispatched to execute subtask ST-1 of [Task frustrated-spec-integration](../../tasks/038-frustrated-spec-integration/task.md). Your remit is bounded by the Acceptance Criteria in [`brief.md`](./brief.md); you MUST NOT expand scope beyond those criteria without surfacing the divergence in `friction-log.md`.

**Parallelism:** Phase A (parallel) — runs concurrently with ST-2. No inter-dependencies..

## I — Input

- All closed-task `friction-log.md` files (~16 closed tasks).
- All `research/<slug>/reflection/friction-log.md`.
- [`MAINTENANCE.md`](../../../MAINTENANCE.md) §3.2 (upstream consumer).
- [`TASK.md`](../../../TASK.md) §306 (mandate restatement).
- `tasks/038-frustrated-spec-integration/task.md` — parent task chain-level context.

## S — Steps

1. Execute the following instruction block faithfully — it is the verbatim Execution Brief from the parent subtask file:

```text
Run research-prompt-optimizer Phase 1–3. 


Skip Phase 1 askuser; intent canonical.
Render to /research/fl0-value-justification/research-prompt.md.
Execute and produce /research/fl0-value-justification/output/SPEC.md.
Author reflection/friction-log.md.
Run tools/check-governance.sh.
Commit "research(fl0-justification): empirical value of FL0 entries (Task 038 ST-1)".
Do NOT push.
```
2. Verify every Acceptance Criterion in [`brief.md`](./brief.md) is satisfied by the produced artefacts.
3. Run `tools/check-governance.sh` and resolve every ERROR before committing.

## E — Expectations

- SPEC.md at `/research/fl0-value-justification/output/SPEC.md`.
- §1 covers ≥15 closed tasks.
- §2 quotes ≥10 distinct FL0 entries verbatim.
- §3 names ≥1 concrete upstream consumer that depends on FL0 presence.
- §4 verdict is one of {mandate / make-optional / clarify} with rationale.
- §5 contains a drop-in §FL.0 paragraph for FRUSTRATED.md.
- `research_phase: complete`; reflection friction-log.
- `tools/check-governance.sh` exits 0 on the produced commit.
- Commit message follows the parent task's convention; the commit cites `Task 038 ST-1` in its trailer.

## Constraints

- Dependency: None. Phase A. NOTE: Task 033 ST-1 (friction-pattern-synthesis) is a sibling — they share the same corpus but ask orthogonal questions (patterns vs FL0 specifically). They can run in parallel; the FL0 study cites the pattern-synthesis if it lands first.
- MUST NOT trigger the subtask's Falsification clause: Wrong cut **iff** FL0 entries provide no measurable upstream signal — in that case, the recommendation should be to make FL0 *optional* (a finding that itself justifies a spec amendment).
- MUST NOT inline this prompt's Goal/Inputs/Acceptance back into the subtask file — the subtask body is now a thin pointer per Task 041.
- MUST run `tools/check-governance.sh` before pushing; a non-zero exit MUST block the push.
- SHOULD cite the parent task's `task_id` in any commit-message trailer for traceability.
