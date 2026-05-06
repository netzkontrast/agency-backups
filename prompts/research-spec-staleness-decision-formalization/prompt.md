---
type: prompt
status: active
slug: research-spec-staleness-decision-formalization
summary: "Produce `research/spec-staleness-decision-formalization/output/SPEC.md` containing a decision tree that converts observable git-history + repo-state signals into one of four staleness buckets without subjective judgment, plus the `MAINT_..."
created: 2026-05-06
updated: 2026-05-06
prompt_kind: task-spec
prompt_framework: RISEN+ReAct
prompt_target_agent: "Claude Code"
prompt_relates_to_task: task-spec-integration
prompt_spawned_from_research: ""
---

# ST-2: Research — Staleness Decision Formalization — Task-Spec Prompt

## Framework

RISEN+ReAct. The prompt declares the framework in frontmatter (`prompt_framework: RISEN+ReAct`) and restates it here for `fm-validate` header conformance. The R/I/S/E sections below carry the canonical roles; a final **Constraints** section groups normative scope/failure rules per repo convention.

## R — Role

You are the **main-agent** dispatched to execute subtask ST-2 of [Task task-spec-integration](../../tasks/033-task-spec-integration/task.md). Your remit is bounded by the Acceptance Criteria in [`brief.md`](./brief.md); you MUST NOT expand scope beyond those criteria without surfacing the divergence in `friction-log.md`.

**Parallelism:** Phase A (parallel) — runs concurrently with ST-1, ST-3, ST-4. **Cross-Task shared with Task 039 ST-2** — whichever Task dispatches first authors the SPEC; the other consumes via filesystem detection (test -f)..

## I — Input

- [`MAINTENANCE.md`](../../../MAINTENANCE.md) §3.4 (current prose algorithm).
- [`TASK.md`](../../../TASK.md) §4.7 (lifecycle states).
- [`tasks/014-improve-maintenance-spec-from-session/`](../../014-improve-maintenance-spec-from-session/) (F2/F3/F4/F7 findings).
- [`tasks/025-maintenance-spec-remaining-findings/`](../../025-maintenance-spec-remaining-findings/) (carry-forward findings).
- All currently-open tasks (~7) as test cases for the algorithm.
- `tasks/033-task-spec-integration/task.md` — parent task chain-level context.

## S — Steps

1. Execute the following instruction block faithfully — it is the verbatim Execution Brief from the parent subtask file:

```text
Run research-prompt-optimizer Phase 1–3 against the intent above. Repo root:


Skip Phase 1 askuser; intent is canonical.
Render the research prompt to /research/spec-staleness-decision-formalization/research-prompt.md.
Execute and produce /research/spec-staleness-decision-formalization/output/SPEC.md per acceptance.
Run tools/check-governance.sh.
Commit "research(staleness-formalization): deterministic algorithm (Task 033 ST-2 / Task 039 ST-2)".
Do NOT push.
```
2. Verify every Acceptance Criterion in [`brief.md`](./brief.md) is satisfied by the produced artefacts.
3. Run `tools/check-governance.sh` and resolve every ERROR before committing.

## E — Expectations

- SPEC.md at `/research/spec-staleness-decision-formalization/output/SPEC.md`.
- §1 contains a decision tree expressible in <30 lines of pseudocode.
- §2 lists ≤5 signals; each has a one-line extraction recipe.
- §3 walks through ≥4 currently-open tasks (e.g., 022, 023, 024, 025) and assigns each a bucket per the algorithm.
- §4 declares the configuration mechanism (env var, repo file, or TASK.md frontmatter).
- Two test runs by independent agents agree on bucket assignment for the §3 walkthroughs.
- `tools/check-governance.sh` exits 0 on the produced commit.
- Commit message follows the parent task's convention; the commit cites `Task 033 ST-2` in its trailer.

## Constraints

- Dependency: None. Phase A. NOTE: Task 039 ST-2 is the *same* research subtask (cross-Task shared input). Whichever lands first authors the SPEC; the second references it.
- MUST NOT trigger the subtask's Falsification clause: Wrong cut **iff** the decision tree requires more than 5 levels or more than 12 leaf rules. Mitigation: TASK.md §4.7 already enumerates 4 buckets; the algorithm need only deterministically map signals → buckets.
- MUST NOT inline this prompt's Goal/Inputs/Acceptance back into the subtask file — the subtask body is now a thin pointer per Task 041.
- MUST run `tools/check-governance.sh` before pushing; a non-zero exit MUST block the push.
- SHOULD cite the parent task's `task_id` in any commit-message trailer for traceability.
