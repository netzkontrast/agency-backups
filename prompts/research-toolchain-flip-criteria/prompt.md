---
type: prompt
status: active
slug: research-toolchain-flip-criteria
summary: "Produce `research/toolchain-flip-criteria/output/SPEC.md` containing the deterministic flip criteria + post-flip cleanup checklist for the MAINTENANCE.md §1.1.2 dual-toolchain transition. Includes: (a) quantifiable criteria (zero outstan..."
created: 2026-05-06
updated: 2026-05-06
prompt_kind: task-spec
prompt_framework: RISEN+ReAct
prompt_target_agent: "Claude Code"
prompt_relates_to_task: maintenance-spec-integration
prompt_spawned_from_research: ""
---

# ST-1: Research — Toolchain Flip Criteria — Task-Spec Prompt

## Framework

RISEN+ReAct. The prompt declares the framework in frontmatter (`prompt_framework: RISEN+ReAct`) and restates it here for `fm-validate` header conformance. The R/I/S/E sections below carry the canonical roles; a final **Constraints** section groups normative scope/failure rules per repo convention.

## R — Role

You are the **maintenance-agent** dispatched to execute subtask ST-1 of [Task maintenance-spec-integration](../../tasks/039-maintenance-spec-integration/task.md). Your remit is bounded by the Acceptance Criteria in [`brief.md`](./brief.md); you MUST NOT expand scope beyond those criteria without surfacing the divergence in `friction-log.md`.

**Parallelism:** Phase A (parallel) — runs concurrently with ST-2, ST-3, ST-4, ST-5. No inter-dependencies..

## I — Input

- [`MAINTENANCE.md`](../../../MAINTENANCE.md) §1.1.2.
- [`PRE_COMMIT.md`](../../../PRE_COMMIT.md) §7.A and §7.B.
- [`research/governance-specs-update-research/output/SPEC.md`](../../../research/governance-specs-update-research/output/SPEC.md) §2.
- [`research/flexible-frontmatter-toolchain/output/SPEC.md`](../../../research/flexible-frontmatter-toolchain/output/SPEC.md).
- `tools/check-governance.sh`, `tools/.frontmatter-waivers`.
- Closed Tasks 016, 017, 018, 019.
- `tasks/039-maintenance-spec-integration/task.md` — parent task chain-level context.

## S — Steps

1. Execute the following instruction block faithfully — it is the verbatim Execution Brief from the parent subtask file:

```text
Run research-prompt-optimizer Phase 1–3. 


Skip Phase 1 askuser; intent canonical.
Render to /research/toolchain-flip-criteria/research-prompt.md.
Execute and produce /research/toolchain-flip-criteria/output/SPEC.md.
Author reflection/friction-log.md.
Run tools/check-governance.sh.
Commit "research(toolchain-flip-criteria): mechanical flip checklist (Task 039 ST-1)".
Do NOT push.
```
2. Verify every Acceptance Criterion in [`brief.md`](./brief.md) is satisfied by the produced artefacts.
3. Run `tools/check-governance.sh` and resolve every ERROR before committing.

## E — Expectations

- SPEC.md at `/research/toolchain-flip-criteria/output/SPEC.md`.
- §1 checklist has ≤7 mechanically-verifiable items.
- §2 flip procedure is a single git commit shape (file changes enumerated).
- §3 post-flip cleanup names every linter to retire and every WARN-to-ERROR promotion.
- §4 rollback procedure tested mentally against §2.
- `research_phase: complete`; reflection friction-log.
- `tools/check-governance.sh` exits 0 on the produced commit.
- Commit message follows the parent task's convention; the commit cites `Task 039 ST-1` in its trailer.

## Constraints

- Dependency: None. Phase A. Sibling subtask ST-2 (staleness formalization) runs in parallel.
- MUST NOT trigger the subtask's Falsification clause: Wrong cut **iff** the criteria cannot be evaluated mechanically (e.g., requires LLM judgment). Mitigation: the criteria are git/grep-extractable (waiver count, task_status, lint exit codes).
- MUST NOT inline this prompt's Goal/Inputs/Acceptance back into the subtask file — the subtask body is now a thin pointer per Task 041.
- MUST run `tools/check-governance.sh` before pushing; a non-zero exit MUST block the push.
- SHOULD cite the parent task's `task_id` in any commit-message trailer for traceability.
