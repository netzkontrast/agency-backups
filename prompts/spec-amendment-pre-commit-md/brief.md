---
type: brief
status: active
slug: spec-amendment-pre-commit-md-brief
summary: "Brief for prompt spec-amendment-pre-commit-md — extracted from tasks/037-pre-commit-spec-integration/subtasks/04-spec-amendment-pre-commit-md.md per Task 041 (PR #70 review C.3 audit-graph repair)."
created: 2026-05-06
updated: 2026-05-06
---

# Brief — ST-4: Spec Amendment — PRE_COMMIT.md (Joint with Task 038 ST-3)

## Raw User Request

> Extract the inlined Execution Brief from `tasks/037-pre-commit-spec-integration/subtasks/04-spec-amendment-pre-commit-md.md` (ST-4) into a registered `/prompts/<slug>/` artefact, restoring the `task_uses_prompts ↔ prompt_relates_to_task` audit-graph edge severed in PR #70 (review finding C.3).

## Target Audience

The dispatched executor for [Task 037 `pre-commit-spec-integration`](../../tasks/037-pre-commit-spec-integration/task.md), specifically subtask ST-4 (04-spec-amendment-pre-commit-md.md). Default executor: **main-agent**.

## Intended Model / Agent

Claude Code (or any agent that satisfies the executor declaration in the parent subtask file).

## Use-Case Context

This prompt drives subtask ST-4 of [Task pre-commit-spec-integration](../../tasks/037-pre-commit-spec-integration/task.md). The parent task's chain-level rationale lives in its `task.md`; this brief records only the subtask's local goal + inputs + acceptance + dependencies + effort, lifted verbatim from the subtask file at extraction time.

**Parallelism:** Phase B (sequential) — depends on ST-1, ST-2, ST-3. **Joint commit with Task 038 ST-3** — §2 wording in this subtask MUST be byte-identical to §28 wording in Task 038 ST-3.

## Goal (from subtask)

Land the PRE_COMMIT.md edits per Task 037 (a)-(e). Reconciled §2 wording matches Task 038 ST-3's §28 wording byte-for-byte (modulo spec-name prefix). §7.A becomes a three-column tool-mapping table (Legacy / Flexible / ADR §7.C). New linters from ST-2 + ST-3 documented. ≥4 Gherkin scenarios per PC.B.1-PC.B.4 anchors.

## Falsification (from subtask)

Wrong cut **iff** the §2 / §28 reconciled wording diverges between the two specs at commit time. Mitigation: a pre-commit hook (or manual `diff` step in this subtask's verification) compares the two paragraphs byte-for-byte before staging.

## Inputs (from subtask)

- ST-1 output: `research/pre-commit-readme-update-cadence/output/SPEC.md` (canonical wording).
- ST-2 implementation: `tools/check-clean-working-directory.py`.
- ST-3 implementation: per-rule waiver refactor.
- Task 038 ST-3 draft: must reach byte-identical §28 wording.
- `tools/adr/cli.py` (PRE_COMMIT.md §7.C anchor).

## Acceptance Criteria (from subtask)

1. PRE_COMMIT.md §2 wording = FRUSTRATED.md §28 wording (modulo spec-name prefix); verified by `diff`.
2. PRE_COMMIT.md §7.A is a three-column Legacy/Flexible/ADR table covering ≥10 tools/checks.
3. ST-2 + ST-3 linters documented in §6.
4. ≥4 Gherkin scenarios anchored PC.B.1-PC.B.4 land in a new acceptance section.
5. `tools/check-governance.sh` exits 0.

## Dependencies (from subtask)

ST-1, ST-2, ST-3 MUST land first. Task 038 ST-3 MUST be authored before this subtask is committed.

## Estimated Effort (from subtask)

Medium (~2 hours; coordination with Task 038 is the bottleneck).
