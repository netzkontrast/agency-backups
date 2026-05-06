---
type: brief
status: active
slug: spec-amendment-frustrated-md-brief
summary: "Brief for prompt spec-amendment-frustrated-md — extracted from tasks/038-frustrated-spec-integration/subtasks/03-spec-amendment-frustrated-md.md per Task 041 (PR #70 review C.3 audit-graph repair)."
created: 2026-05-06
updated: 2026-05-06
---

# Brief — ST-3: Spec Amendment — FRUSTRATED.md (Joint with Task 037 ST-4)

## Raw User Request

> Extract the inlined Execution Brief from `tasks/038-frustrated-spec-integration/subtasks/03-spec-amendment-frustrated-md.md` (ST-3) into a registered `/prompts/<slug>/` artefact, restoring the `task_uses_prompts ↔ prompt_relates_to_task` audit-graph edge severed in PR #70 (review finding C.3).

## Target Audience

The dispatched executor for [Task 038 `frustrated-spec-integration`](../../tasks/038-frustrated-spec-integration/task.md), specifically subtask ST-3 (03-spec-amendment-frustrated-md.md). Default executor: **main-agent**.

## Intended Model / Agent

Claude Code (or any agent that satisfies the executor declaration in the parent subtask file).

## Use-Case Context

This prompt drives subtask ST-3 of [Task frustrated-spec-integration](../../tasks/038-frustrated-spec-integration/task.md). The parent task's chain-level rationale lives in its `task.md`; this brief records only the subtask's local goal + inputs + acceptance + dependencies + effort, lifted verbatim from the subtask file at extraction time.

**Parallelism:** Phase B (sequential) — depends on ST-1, ST-2. **Joint commit with Task 037 ST-4** — §28 wording in this subtask MUST be byte-identical to §2 wording in Task 037 ST-4.

## Goal (from subtask)

Land the FRUSTRATED.md edits per Task 038 (a)-(d). §28 wording = PRE_COMMIT.md §2 wording (byte-identical modulo prefix). §FL.0 carries the ST-1-research-backed rationale. §FL.Log references the ST-2 linter as the enforcement mechanism. ≥4 Gherkin scenarios per FR.B.1-FR.B.4 anchors.

## Falsification (from subtask)

Wrong cut **iff** §28 / §2 wording diverges from Task 037 ST-4's amendment. Mitigation: same `diff`-based verification as Task 037 ST-4.

## Inputs (from subtask)

- ST-1 output: `research/fl0-value-justification/output/SPEC.md` §5 (canonical §FL.0 paragraph).
- ST-2 implementation: `tools/check-fl-declaration.py`.
- Task 037 ST-4 draft: must reach byte-identical §28 wording.
- `research/pre-commit-readme-update-cadence/output/SPEC.md` (canonical readme-cadence wording).

## Acceptance Criteria (from subtask)

1. FRUSTRATED.md §28 wording = PRE_COMMIT.md §2 wording (verified by `diff`).
2. §FL.0 carries the research-backed rationale paragraph (≤10 lines per ST-1 SPEC §5 budget).
3. §FL.Log.1 / §FL.Log.2 reference the ST-2 linter as enforcement.
4. ≥4 Gherkin scenarios anchored FR.B.1-FR.B.4 land.
5. **NEW (per Task 040 §A row §7 MERGE):** §FL.Log.1 prose lifts the *Reflexion pattern* concept from `research/gemini/superclaude-agency-orchestration-spec/superclaude-agency-orchestration-spec.md §7.1` — when an external integration fails (e.g., HTTP 429), the agent MUST log the failure mode in `friction-log.md` and synthesise the corrected approach into persistent memory to prevent re-occurrence. One paragraph; no `sc-document` skill citation (per Task 040 §A: skill conflation rejected); no `confidence-check` citation (skill does not exist locally). Anchor a new Gherkin `FR.B.REFLEX.1` per Task 040 §B remap table.
6. `tools/check-governance.sh` exits 0.

## Dependencies (from subtask)

ST-1, ST-2 MUST land first. Task 037 ST-4 MUST be authored before this subtask is committed.

## Estimated Effort (from subtask)

Small (~1 hour).
