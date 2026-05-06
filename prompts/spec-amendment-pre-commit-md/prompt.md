---
type: prompt
status: active
slug: spec-amendment-pre-commit-md
summary: "Land the PRE_COMMIT.md edits per Task 037 (a)-(e). Reconciled §2 wording matches Task 038 ST-3's §28 wording byte-for-byte (modulo spec-name prefix). §7.A becomes a three-column tool-mapping table (Legacy / Flexible / ADR §7.C). New lint..."
created: 2026-05-06
updated: 2026-05-06
prompt_kind: task-spec
prompt_framework: RISEN+ReAct
prompt_target_agent: "Claude Code"
prompt_relates_to_task: pre-commit-spec-integration
---

# ST-4: Spec Amendment — PRE_COMMIT.md (Joint with Task 038 ST-3) — Task-Spec Prompt

## Framework

RISEN+ReAct. The prompt declares the framework in frontmatter (`prompt_framework: RISEN+ReAct`) and restates it here for `fm-validate` header conformance. The R/I/S/E sections below carry the canonical roles; a final **Constraints** section groups normative scope/failure rules per repo convention.

## R — Role

You are the **main-agent** dispatched to execute subtask ST-4 of [Task pre-commit-spec-integration](../../tasks/037-pre-commit-spec-integration/task.md). Your remit is bounded by the Acceptance Criteria in [`brief.md`](./brief.md); you MUST NOT expand scope beyond those criteria without surfacing the divergence in `friction-log.md`.

**Parallelism:** Phase B (sequential) — depends on ST-1, ST-2, ST-3. **Joint commit with Task 038 ST-3** — §2 wording in this subtask MUST be byte-identical to §28 wording in Task 038 ST-3..

## I — Input

- ST-1 output: `research/pre-commit-readme-update-cadence/output/SPEC.md` (canonical wording).
- ST-2 implementation: `tools/check-clean-working-directory.py`.
- ST-3 implementation: per-rule waiver refactor.
- Task 038 ST-3 draft: must reach byte-identical §28 wording.
- `tools/adr/cli.py` (PRE_COMMIT.md §7.C anchor).
- `tasks/037-pre-commit-spec-integration/task.md` — parent task chain-level context.

## S — Steps

1. The agent MUST produce the artefact required by acceptance criterion: PRE_COMMIT.md §2 wording = FRUSTRATED.md §28 wording (modulo spec-name prefix); verified by `diff`.
2. The agent MUST produce the artefact required by acceptance criterion: PRE_COMMIT.md §7.A is a three-column Legacy/Flexible/ADR table covering ≥10 tools/checks.
3. The agent MUST produce the artefact required by acceptance criterion: ST-2 + ST-3 linters documented in §6.
4. The agent MUST produce the artefact required by acceptance criterion: ≥4 Gherkin scenarios anchored PC.B.1-PC.B.4 land in a new acceptance section.
5. The agent MUST produce the artefact required by acceptance criterion: `tools/check-governance.sh` exits 0.
6. The agent MUST verify every Acceptance Criterion enumerated in [`brief.md`](./brief.md) holds against the produced artefacts; on any failure the agent MUST iterate the relevant implementation step rather than weakening the criterion.
7. The agent MUST run `tools/check-governance.sh` and resolve every ERROR before committing; a non-zero exit MUST block the commit.
8. The agent SHOULD author or update `tasks/037-pre-commit-spec-integration/friction-log.md` per FRUSTRATED.md FL[0-3] when frictions arise; absence of frictions MAY be recorded as `FL: 0`.
9. The agent MUST commit with a message that names `Task 037 ST-4` in its trailer; the agent MUST NOT push (the maintainer pushes after review).

## E — Expectations

- PRE_COMMIT.md §2 wording = FRUSTRATED.md §28 wording (modulo spec-name prefix); verified by `diff`.
- PRE_COMMIT.md §7.A is a three-column Legacy/Flexible/ADR table covering ≥10 tools/checks.
- ST-2 + ST-3 linters documented in §6.
- ≥4 Gherkin scenarios anchored PC.B.1-PC.B.4 land in a new acceptance section.
- `tools/check-governance.sh` exits 0.
- `tools/check-governance.sh` exits 0 on the produced commit.
- Commit message follows the parent task's convention; the commit cites `Task 037 ST-4` in its trailer.

## Constraints

- Dependency: ST-1, ST-2, ST-3 MUST land first. Task 038 ST-3 MUST be authored before this subtask is committed.
- MUST NOT trigger the subtask's Falsification clause: Wrong cut **iff** the §2 / §28 reconciled wording diverges between the two specs at commit time. Mitigation: a pre-commit hook (or manual `diff` step in this subtask's verification) compares the two paragraphs byte-for-byte before staging.
- MUST NOT inline this prompt's Goal/Inputs/Acceptance back into the subtask file — the subtask body is now a thin pointer per Task 041.
- MUST run `tools/check-governance.sh` before pushing; a non-zero exit MUST block the push.
- SHOULD cite the parent task's `task_id` in any commit-message trailer for traceability.
