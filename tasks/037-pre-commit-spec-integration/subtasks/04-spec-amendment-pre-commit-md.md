---
type: note
status: draft
slug: task-037-st4-spec-amendment-pre-commit-md
summary: "Subtask ST-4 (Phase B; co-coordinated with Task 038 ST-3): apply PRE_COMMIT.md edits — §2 reconciled with FRUSTRATED.md §28, §7.A three-way Legacy/Flexible/ADR matrix, ST-2/ST-3 linter docs, ≥4 Gherkin scenarios per PC.B.1-PC.B.4."
created: 2026-05-06
updated: 2026-05-06
---

# ST-4: Spec Amendment — PRE_COMMIT.md (Joint with Task 038 ST-3)

**Executor:** main-agent

**Parallelism:** Phase B (sequential) — depends on ST-1, ST-2, ST-3. **Joint commit with Task 038 ST-3** — §2 wording in this subtask MUST be byte-identical to §28 wording in Task 038 ST-3.

## Goal

Land the PRE_COMMIT.md edits per Task 037 (a)-(e). Reconciled §2 wording matches Task 038 ST-3's §28 wording byte-for-byte (modulo spec-name prefix). §7.A becomes a three-column tool-mapping table (Legacy / Flexible / ADR §7.C). New linters from ST-2 + ST-3 documented. ≥4 Gherkin scenarios per PC.B.1-PC.B.4 anchors.

## Falsification

Wrong cut **iff** the §2 / §28 reconciled wording diverges between the two specs at commit time. Mitigation: a pre-commit hook (or manual `diff` step in this subtask's verification) compares the two paragraphs byte-for-byte before staging.

## Inputs

- ST-1 output: `research/pre-commit-readme-update-cadence/output/SPEC.md` (canonical wording).
- ST-2 implementation: `tools/check-clean-working-directory.py`.
- ST-3 implementation: per-rule waiver refactor.
- Task 038 ST-3 draft: must reach byte-identical §28 wording.
- `tools/adr/cli.py` (PRE_COMMIT.md §7.C anchor).

## Acceptance Criteria

1. PRE_COMMIT.md §2 wording = FRUSTRATED.md §28 wording (modulo spec-name prefix); verified by `diff`.
2. PRE_COMMIT.md §7.A is a three-column Legacy/Flexible/ADR table covering ≥10 tools/checks.
3. ST-2 + ST-3 linters documented in §6.
4. ≥4 Gherkin scenarios anchored PC.B.1-PC.B.4 land in a new acceptance section.
5. `tools/check-governance.sh` exits 0.

## Dependencies

ST-1, ST-2, ST-3 MUST land first. Task 038 ST-3 MUST be authored before this subtask is committed.

## Estimated Effort

Medium (~2 hours; coordination with Task 038 is the bottleneck).
