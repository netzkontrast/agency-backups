---
type: prompt
status: active
slug: research-pre-commit-readme-update-cadence
summary: "Produce `research/pre-commit-readme-update-cadence/output/SPEC.md` that resolves the contradiction surfaced by the spec audit. Output: (a) a single normative rule on when readme.md is updated (immediate / batched-at-pre-commit / hybrid),..."
created: 2026-05-06
updated: 2026-05-06
prompt_kind: task-spec
prompt_framework: RISEN+ReAct
prompt_target_agent: "Claude Code"
prompt_relates_to_task: pre-commit-spec-integration
prompt_spawned_from_research: ""
---

# ST-1: Research — Pre-Commit Readme-Update Cadence — Task-Spec Prompt

## Framework

RISEN+ReAct. The prompt declares the framework in frontmatter (`prompt_framework: RISEN+ReAct`) and restates it here for `fm-validate` header conformance. The R/I/S/E sections below carry the canonical roles; a final **Constraints** section groups normative scope/failure rules per repo convention.

## R — Role

You are the **main-agent** dispatched to execute subtask ST-1 of [Task pre-commit-spec-integration](../../tasks/037-pre-commit-spec-integration/task.md). Your remit is bounded by the Acceptance Criteria in [`brief.md`](./brief.md); you MUST NOT expand scope beyond those criteria without surfacing the divergence in `friction-log.md`.

**Parallelism:** Phase A (parallel) — runs concurrently with ST-2, ST-3. **Cross-Task: this subtask's output also feeds Task 038 ST-3 (FRUSTRATED.md §28 reconciliation); both Task 037 ST-4 and Task 038 ST-3 consume the same SPEC.**.

## I — Input

- [`FRUSTRATED.md`](../../../FRUSTRATED.md) §28.
- [`PRE_COMMIT.md`](../../../PRE_COMMIT.md) §2.
- [`MAINTENANCE.md`](../../../MAINTENANCE.md) §3.2.
- [`research/repo-maintenance-protocol-spec/output/SPEC.md`](../../../research/repo-maintenance-protocol-spec/output/SPEC.md) §3.1 (static/dynamic partition).
- ≥3 recent merged PRs as token-cost evidence (one with many readme updates, one with few).
- `tasks/037-pre-commit-spec-integration/task.md` — parent task chain-level context.

## S — Steps

1. Execute the following instruction block faithfully — it is the verbatim Execution Brief from the parent subtask file:

```text
Run research-prompt-optimizer Phase 1–3. 


Skip Phase 1 askuser; intent canonical.
Render to /research/pre-commit-readme-update-cadence/research-prompt.md.
Execute and produce /research/pre-commit-readme-update-cadence/output/SPEC.md.
Author reflection/friction-log.md.
Run tools/check-governance.sh.
Commit "research(readme-cadence): reconcile FRUSTRATED.md §28 with PRE_COMMIT.md §2 (Task 037 ST-1)".
Do NOT push.
```
2. Verify every Acceptance Criterion in [`brief.md`](./brief.md) is satisfied by the produced artefacts.
3. Run `tools/check-governance.sh` and resolve every ERROR before committing.

## E — Expectations

- SPEC.md at `/research/pre-commit-readme-update-cadence/output/SPEC.md`.
- §1 token-cost comparison covers ≥3 cadence choices.
- §2 normative rule is unambiguous and consistent with MAINTENANCE.md §3.2.
- §3 contains drop-in wording for FRUSTRATED.md §28 AND PRE_COMMIT.md §2.
- §4 walkthrough on a recent session shows the rule yields the expected behaviour.
- `research_phase: complete`; reflection friction-log.
- `tools/check-governance.sh` exits 0 on the produced commit.
- Commit message follows the parent task's convention; the commit cites `Task 037 ST-1` in its trailer.

## Constraints

- Dependency: None. Phase A.
- MUST NOT trigger the subtask's Falsification clause: Wrong cut **iff** any choice yields >2× token cost vs. status quo. Mitigation: existing closed tasks already have an emergent practice; the research can codify the cheapest one.
- MUST NOT inline this prompt's Goal/Inputs/Acceptance back into the subtask file — the subtask body is now a thin pointer per Task 041.
- MUST run `tools/check-governance.sh` before pushing; a non-zero exit MUST block the push.
- SHOULD cite the parent task's `task_id` in any commit-message trailer for traceability.
