---
type: prompt
status: active
slug: tooling-duplicate-task-id-linter
summary: "Ship `tools/fm/check-duplicate-task-id.py` that scans `tasks/<NNN>-<slug>/task.md` files, extracts `task_id` from each frontmatter, and exits 1 if any value appears more than once across active (non-`updated`, non-`abandoned`) tasks. Clo..."
created: 2026-05-06
updated: 2026-05-06
prompt_kind: task-spec
prompt_framework: RISEN+ReAct
prompt_target_agent: "Claude Code"
prompt_relates_to_task: task-spec-integration
---

# ST-3: `check-duplicate-task-id` — Closes TASK.md §8.1 Enforcement Gap — Task-Spec Prompt

## Framework

RISEN+ReAct. The prompt declares the framework in frontmatter (`prompt_framework: RISEN+ReAct`) and restates it here for `fm-validate` header conformance. The R/I/S/E sections below carry the canonical roles; a final **Constraints** section groups normative scope/failure rules per repo convention.

## R — Role

You are the **main-agent** dispatched to execute subtask ST-3 of [Task task-spec-integration](../../tasks/033-task-spec-integration/task.md). Your remit is bounded by the Acceptance Criteria in [`brief.md`](./brief.md); you MUST NOT expand scope beyond those criteria without surfacing the divergence in `friction-log.md`.

**Parallelism:** Phase A (parallel) — runs concurrently with ST-1, ST-2, ST-4. No inter-dependencies..

## I — Input

- [`TASK.md`](../../../TASK.md) §8.1 (rule statement).
- [`tasks/024-renumber-duplicate-task-ids-v2/`](../../024-renumber-duplicate-task-ids-v2/) (the manual cleanup task this linter supersedes).
- `tools/fm/_core.py` (iter_operational_files, frontmatter parser).
- All current `tasks/*/task.md` (test corpus — should fail until Task 024 lands).
- `tasks/033-task-spec-integration/task.md` — parent task chain-level context.

## S — Steps

1. The agent MUST treat the following preamble as authoritative orientation before executing any subsequent step: Implement tools/fm/check-duplicate-task-id.py. Read first: TASK.md §8.1, tasks/024-renumber-duplicate-task-ids-v2/task.md, tools/fm/_core.py. Acceptance: as documented above. Note: When you run the linter against the current repo, you SHOULD see two ERRORs (006/006 and 009/009). Do NOT fix those; this subtask only ships the linter. Task 024 fixes the underlying collisions. When done: python3 -m unittest discover -s tests/fm python3 tools/fm/check-duplicate-task-id.py tasks/ # expect 2 ERRORs Commit "feat(tools/fm): duplicate task_id linter (Task 033 ST-3, closes TASK.md §8.1 gap)". Do NOT push.
2. The agent MUST verify every Acceptance Criterion enumerated in [`brief.md`](./brief.md) holds against the produced artefacts; on any failure the agent MUST iterate the relevant implementation step rather than weakening the criterion.
3. The agent MUST run `tools/check-governance.sh` and resolve every ERROR before committing; a non-zero exit MUST block the commit.
4. The agent SHOULD author or update `tasks/033-task-spec-integration/friction-log.md` per FRUSTRATED.md FL[0-3] when frictions arise; absence of frictions MAY be recorded as `FL: 0`.
5. The agent MUST commit with a message that names `Task 033 ST-3` in its trailer; the agent MUST NOT push (the maintainer pushes after review).

## E — Expectations

- **Surface.** `python3 tools/fm/check-duplicate-task-id.py [<paths>]` (defaults to scanning `tasks/`).
- **Algorithm.** - Build `{task_id: [paths]}` map across active tasks. - For each id with `len(paths) > 1`, check whether the supersession reciprocity (predecessor.task_superseded_by ↔ successor.task_supersedes) explains it. - Unexplained duplicates → ERROR exit 1; explained → INFO exit 0.
- **Tests.** `tests/fm/test_duplicate_task_id.py` covers: clean repo (pass), 006/006 collision (fail), 009/009 collision (fail), supersession-explained duplicate (pass).
- **Integration.** Add to `tools/check-governance.sh` as ERROR-tier when `FM_TOOLCHAIN=1`; default-off in legacy mode (until the migration window closes per Task 039 ST-1).
- **Documentation.** Cite TASK.md §8.1 in the script docstring.
- `tools/check-governance.sh` exits 0 on the produced commit.
- Commit message follows the parent task's convention; the commit cites `Task 033 ST-3` in its trailer.

## Constraints

- Dependency: None. Phase A. NOTE: this linter is *expected to fail* on the current repo (006/006 and 009/009 are unresolved); that signals Task 024 is the natural unblocking work.
- MUST NOT trigger the subtask's Falsification clause: Wrong cut **iff** the linter cannot distinguish active from `updated` predecessors. Mitigation: filter on `task_status` ∈ {open, in_progress, blocked, done} only; predecessors with `task_status: updated` are explicitly allowed to share the original id with their successor only if `task_supersedes`/`task_superseded_by` reciprocity holds.
- MUST NOT inline this prompt's Goal/Inputs/Acceptance back into the subtask file — the subtask body is now a thin pointer per Task 041.
- MUST run `tools/check-governance.sh` before pushing; a non-zero exit MUST block the push.
- SHOULD cite the parent task's `task_id` in any commit-message trailer for traceability.
