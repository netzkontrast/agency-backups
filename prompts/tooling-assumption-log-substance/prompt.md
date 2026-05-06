---
type: prompt
status: active
slug: tooling-assumption-log-substance
summary: "Ship `tools/check-assumption-log.py` that scans every operational-folder `readme.md` for an `## Assumptions Log` section and validates: (a) section exists when the parent task involved a non-trivial decision, (b) entries are not stale (c..."
created: 2026-05-06
updated: 2026-05-06
prompt_kind: task-spec
prompt_framework: RISEN+ReAct
prompt_target_agent: "Claude Code"
prompt_relates_to_task: agents-spec-integration
---

# ST-4: `check-assumption-log` — FOLDERS.md F.3 / AGENTS.md §60-65 Enforcement — Task-Spec Prompt

## Framework

RISEN+ReAct. The prompt declares the framework in frontmatter (`prompt_framework: RISEN+ReAct`) and restates it here for `fm-validate` header conformance. The R/I/S/E sections below carry the canonical roles; a final **Constraints** section groups normative scope/failure rules per repo convention.

## R — Role

You are the **main-agent** dispatched to execute subtask ST-4 of [Task agents-spec-integration](../../tasks/032-agents-spec-integration/task.md). Your remit is bounded by the Acceptance Criteria in [`brief.md`](./brief.md); you MUST NOT expand scope beyond those criteria without surfacing the divergence in `friction-log.md`.

**Parallelism:** Phase A (parallel) — runs concurrently with ST-1, ST-2, ST-3. No inter-dependencies..

## I — Input

- [`FOLDERS.md`](../../../FOLDERS.md) §3 (Required Content for readme.md including Assumptions Log).
- [`AGENTS.md`](../../../AGENTS.md) §60–65 (assumption-logging rule).
- All `tasks/<NNN>-<slug>/readme.md` (test corpus).
- All `research/<slug>/readme.md` (test corpus).
- `tools/fm/extract.py` (section extraction).
- `tasks/032-agents-spec-integration/task.md` — parent task chain-level context.

## S — Steps

1. The agent MUST treat the following preamble as authoritative orientation before executing any subsequent step: Implement tools/check-assumption-log.py. Read first: FOLDERS.md §3, AGENTS.md §60-65, tools/fm/extract.py. Acceptance: as documented. Python 3.11 stdlib only. WARN-tier exits. Tests cover present/absent/stale. When done: python3 -m unittest discover -s tests python3 tools/check-governance.sh Commit "feat(tools): assumption-log substance linter (Task 032 ST-4)". Do NOT push.
2. The agent MUST verify every Acceptance Criterion enumerated in [`brief.md`](./brief.md) holds against the produced artefacts; on any failure the agent MUST iterate the relevant implementation step rather than weakening the criterion.
3. The agent MUST run `tools/check-governance.sh` and resolve every ERROR before committing; a non-zero exit MUST block the commit.
4. The agent SHOULD author or update `tasks/032-agents-spec-integration/friction-log.md` per FRUSTRATED.md FL[0-3] when frictions arise; absence of frictions MAY be recorded as `FL: 0`.
5. The agent MUST commit with a message that names `Task 032 ST-4` in its trailer; the agent MUST NOT push (the maintainer pushes after review).

## E — Expectations

- **Surface.** `python3 tools/check-assumption-log.py <folder>` exits 0 (pass) or 2 (WARN).
- **Checks.** - Section heading `## Assumptions Log` present. - Section body non-empty OR contains exact line `(none)`. - If parent folder's frontmatter `updated` is more recent than the readme's, surface `STALE` warning.
- **Tests.** `tests/test_assumption_log.py` covers all three checks.
- **Integration.** `tools/check-governance.sh` runs WARN-tier on `tasks/<NNN>-<slug>/readme.md` and `research/<slug>/readme.md`.
- `tools/check-governance.sh` exits 0 on the produced commit.
- Commit message follows the parent task's convention; the commit cites `Task 032 ST-4` in its trailer.

## Constraints

- Dependency: Reuses `tools/fm/extract.py` — gracefully degrade to grep if not available.
- MUST NOT trigger the subtask's Falsification clause: Wrong cut **iff** the substance check produces too many false positives on legitimate "no assumptions" cases. Mitigation: empty section with explicit "(none)" line is permitted; the linter only flags absent-or-truly-empty.
- MUST NOT inline this prompt's Goal/Inputs/Acceptance back into the subtask file — the subtask body is now a thin pointer per Task 041.
- MUST run `tools/check-governance.sh` before pushing; a non-zero exit MUST block the push.
- SHOULD cite the parent task's `task_id` in any commit-message trailer for traceability.
