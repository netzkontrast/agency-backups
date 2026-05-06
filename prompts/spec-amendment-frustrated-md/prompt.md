---
type: prompt
status: active
slug: spec-amendment-frustrated-md
summary: "Land the FRUSTRATED.md edits per Task 038 (a)-(d). §28 wording = PRE_COMMIT.md §2 wording (byte-identical modulo prefix). §FL.0 carries the ST-1-research-backed rationale. §FL.Log references the ST-2 linter as the enforcement mechanism. ..."
created: 2026-05-06
updated: 2026-05-06
prompt_kind: task-spec
prompt_framework: RISEN+ReAct
prompt_target_agent: "Claude Code"
prompt_relates_to_task: frustrated-spec-integration
---

# ST-3: Spec Amendment — FRUSTRATED.md (Joint with Task 037 ST-4) — Task-Spec Prompt

## Framework

RISEN+ReAct. The prompt declares the framework in frontmatter (`prompt_framework: RISEN+ReAct`) and restates it here for `fm-validate` header conformance. The R/I/S/E sections below carry the canonical roles; a final **Constraints** section groups normative scope/failure rules per repo convention.

## R — Role

You are the **main-agent** dispatched to execute subtask ST-3 of [Task frustrated-spec-integration](../../tasks/038-frustrated-spec-integration/task.md). Your remit is bounded by the Acceptance Criteria in [`brief.md`](./brief.md); you MUST NOT expand scope beyond those criteria without surfacing the divergence in `friction-log.md`.

**Parallelism:** Phase B (sequential) — depends on ST-1, ST-2. **Joint commit with Task 037 ST-4** — §28 wording in this subtask MUST be byte-identical to §2 wording in Task 037 ST-4..

## I — Input

- ST-1 output: `research/fl0-value-justification/output/SPEC.md` §5 (canonical §FL.0 paragraph).
- ST-2 implementation: `tools/check-fl-declaration.py`.
- Task 037 ST-4 draft: must reach byte-identical §28 wording.
- `research/pre-commit-readme-update-cadence/output/SPEC.md` (canonical readme-cadence wording).
- `tasks/038-frustrated-spec-integration/task.md` — parent task chain-level context.

## S — Steps

1. The agent MUST produce the artefact required by acceptance criterion: FRUSTRATED.md §28 wording = PRE_COMMIT.md §2 wording (verified by `diff`).
2. The agent MUST produce the artefact required by acceptance criterion: §FL.0 carries the research-backed rationale paragraph (≤10 lines per ST-1 SPEC §5 budget).
3. The agent MUST produce the artefact required by acceptance criterion: §FL.Log.1 / §FL.Log.2 reference the ST-2 linter as enforcement.
4. The agent MUST produce the artefact required by acceptance criterion: ≥4 Gherkin scenarios anchored FR.B.1-FR.B.4 land.
5. The agent MUST produce the artefact required by acceptance criterion: **NEW (per Task 040 §A row §7 MERGE):** §FL.Log.1 prose lifts the *Reflexion pattern* concept from `research/gemini/superclaude-agency-orchestration-spec/superclaude-agency-orchestration-spec.md §7.1` — when an external integration fails (e.g., HTTP 429), the agent MUST log the failure mode in `friction-log.md` and synthesise the corrected approach into persistent memory to prevent re-occurrence. One paragraph; no `sc-document` skill citation (per Task 040 §A: skill conflation rejected); no `confidence-check` citation (skill does not exist locally). Anchor a new Gherkin `FR.B.REFLEX.1` per Task 040 §B remap table.
6. The agent MUST produce the artefact required by acceptance criterion: `tools/check-governance.sh` exits 0.
7. The agent MUST verify every Acceptance Criterion enumerated in [`brief.md`](./brief.md) holds against the produced artefacts; on any failure the agent MUST iterate the relevant implementation step rather than weakening the criterion.
8. The agent MUST run `tools/check-governance.sh` and resolve every ERROR before committing; a non-zero exit MUST block the commit.
9. The agent SHOULD author or update `tasks/038-frustrated-spec-integration/friction-log.md` per FRUSTRATED.md FL[0-3] when frictions arise; absence of frictions MAY be recorded as `FL: 0`.
10. The agent MUST commit with a message that names `Task 038 ST-3` in its trailer; the agent MUST NOT push (the maintainer pushes after review).

## E — Expectations

- FRUSTRATED.md §28 wording = PRE_COMMIT.md §2 wording (verified by `diff`).
- §FL.0 carries the research-backed rationale paragraph (≤10 lines per ST-1 SPEC §5 budget).
- §FL.Log.1 / §FL.Log.2 reference the ST-2 linter as enforcement.
- ≥4 Gherkin scenarios anchored FR.B.1-FR.B.4 land.
- **NEW (per Task 040 §A row §7 MERGE):** §FL.Log.1 prose lifts the *Reflexion pattern* concept from `research/gemini/superclaude-agency-orchestration-spec/superclaude-agency-orchestration-spec.md §7.1` — when an external integration fails (e.g., HTTP 429), the agent MUST log the failure mode in `friction-log.md` and synthesise the corrected approach into persistent memory to prevent re-occurrence. One paragraph; no `sc-document` skill citation (per Task 040 §A: skill conflation rejected); no `confidence-check` citation (skill does not exist locally). Anchor a new Gherkin `FR.B.REFLEX.1` per Task 040 §B remap table.
- `tools/check-governance.sh` exits 0.
- `tools/check-governance.sh` exits 0 on the produced commit.
- Commit message follows the parent task's convention; the commit cites `Task 038 ST-3` in its trailer.

## Constraints

- Dependency: ST-1, ST-2 MUST land first. Task 037 ST-4 MUST be authored before this subtask is committed.
- MUST NOT trigger the subtask's Falsification clause: Wrong cut **iff** §28 / §2 wording diverges from Task 037 ST-4's amendment. Mitigation: same `diff`-based verification as Task 037 ST-4.
- MUST NOT inline this prompt's Goal/Inputs/Acceptance back into the subtask file — the subtask body is now a thin pointer per Task 041.
- MUST run `tools/check-governance.sh` before pushing; a non-zero exit MUST block the push.
- SHOULD cite the parent task's `task_id` in any commit-message trailer for traceability.
