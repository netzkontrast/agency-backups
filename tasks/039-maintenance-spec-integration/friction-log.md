---
type: note
status: completed
slug: task-039-maintenance-spec-integration-friction-log
summary: "Friction log for Task 039 — maintenance-spec-integration. FL0: every Phase A subtask (ST-1, ST-3, ST-4, ST-5) and Phase B (ST-6) declared FL0; ST-2 was already complete on disk via Task 033 cross-Task arrangement; no friction-bearing decisions arose during the run."
created: 2026-05-08
updated: 2026-05-08
---

Highest Frustration Level: FL0

# Friction Log — Task 039 (MAINTENANCE.md Spec Integration)

## What landed

- **ST-1.** [`research/toolchain-flip-criteria/`](../../research/toolchain-flip-criteria/) workspace closed (`research_phase: complete`). SPEC.md ships seven mechanically-verifiable flip criteria (TFC.1.1–TFC.1.7), a single-commit flip procedure (§2), a post-flip cleanup table covering every `[opt]` WARN block in `tools/check-governance.sh` (§3), and a `git revert <flip-sha>` rollback procedure (§4). Per-workspace trust audit: schema=1.00, behavioral=1.00, governance=1.00. Commit `5bb7431`.
- **ST-2.** Already complete on disk before dispatch — [`research/spec-staleness-decision-formalization/`](../../research/spec-staleness-decision-formalization/) was authored as the joint deliverable of [Task 033 ST-2](../033-task-spec-integration/subtasks/02-research-spec-staleness-decision-formalization.md) and this Task's ST-2 per the cross-Task arrangement. Three-level / four-leaf decision tree with five signals; `MAINT_STALE_DAYS` declared; consumed by ST-3 verbatim.
- **ST-3.** [`tools/maintenance/staleness-audit.py`](../../tools/maintenance/staleness-audit.py) (780 LOC, 29 tests passing) implements the SPEC §1 pseudocode end-to-end, with diagnostic / markdown / JSON output formatters and the four worked examples (Tasks 022/023/024/025) reproduced as regression cases. Wired as `[opt]` WARN-tier step in `tools/check-governance.sh` (`FM_STALENESS_AUDIT_STRICT=1` to gate). Commit `54d3fa2`.
- **ST-4.** [`tools/maintenance/dynamic-readme-partition.py`](../../tools/maintenance/dynamic-readme-partition.py) (359 LOC, 11 tests passing) enforces the `<!-- BEGIN/END DYNAMIC -->` partition per `repo-maintenance-protocol-spec/output/SPEC.md §3.1`. Walks `tasks/`, `research/`, `prompts/`. WARN-tier; advisory `M.B.6:missing-marker` finding so the existing 170-readme corpus is not retroactively flagged ERROR. Commit `3aa2519`.
- **ST-5.** [`tools/maintenance/trust-audit.py`](../../tools/maintenance/trust-audit.py) (559 LOC, 18 tests passing) — the AGGREGATOR per spec-panel C3 partition. Imports `DIAGNOSTIC_SCHEMA` and `audit()` from [`tools/check-trust-audit.py`](../../tools/check-trust-audit.py) (Task 035 ST-4 GATE) via `importlib.util.spec_from_file_location`; never re-implements Spec-J/K/L thresholds. Per-workspace summary line + roll-up tally consumed by MAINTENANCE.md §3.2 friction-aggregation. `PartitionGuard` test asserts the AGGREGATOR carries no `_score_*` helpers. Commit `f64e9a8`.
- **ST-6.** [`MAINTENANCE.md`](../../MAINTENANCE.md) amended:
  - §1 mirrors the FOLDERS.md:191 Accepted-ADR T4-immutability rule (was unsourced in the governance hub).
  - §1.1 split into §1.1.1 baseline + §1.1.2 three-way Legacy / Flexible / ADR transition matrix; flip criteria cite the ST-1 SPEC §1 TFC.1.x predicates; MorphLLM-Fast-Apply footnote informational only (Task 040 §C MCP-reality discipline). Cites Task 040 §A row §8 for the nightly-maintenance vocabulary lift.
  - §2.3 mandates trust-audit gating before research closure (cites GATE + AGGREGATOR + `agentic-eval-trust-improvement-spec/output/SPEC.md`); appends run-log baseline recovery procedure for corrupted run-log per `governance-specs-update-research/output/SPEC.md` §2.
  - §3.2 cites the partition linter and `repo-maintenance-protocol-spec/output/SPEC.md`; integrates AGGREGATOR roll-up into the nightly run.
  - §3.4 carries the deterministic five-signal table + 3-level decision tree + `MAINT_STALE_DAYS` contract; cross-references the staleness SPEC and `tools/maintenance/staleness-audit.py`.
  - §3.5 closes the discovery loop: coherence run files the dedup Task on first encounter; subsequent encounters surface the existing Task without re-discovery; ADR validator step (now `[5/6]`) is unaffected because the renumber excludes `decisions/`.
  - New §6 Acceptance Criteria carries 15 Gherkin scenarios across all seven anchors M.B.1–M.B.7. M.B.7 second scenario forbids any tier-level mutation of `decisions/<NNNN>-<slug>.md` — closes the §3.5 falsification clause.
  - Commit `60f764c`.

## Friction (FL0)

No frictions. Every subtask declared FL0 in its own reflection / commit narrative. The handful of micro-bookkeeping items that arose during dispatch — the ST-1/ST-3/ST-4/ST-5 race on `tools/maintenance/readme.md` (resolved by additive merging on each commit), the line-191-vs-line-115 drift in `FOLDERS.md` (cited at the actual line), and the pre-existing `test_fm_wrapper.py` failures unrelated to this Task — were neither blocking nor friction-bearing under the FL0–FL3 rubric.

## Falsification clause

Per parent task §Goal:

- **(a) §2.3 trust-audit gate** — landed at MAINTENANCE.md §2.3; cites the orphaned `agentic-eval-trust-improvement-spec` SPEC + Task 035 ST-4 GATE + this Task's ST-5 AGGREGATOR. ✓
- **(b) §3.2 dynamic-readme partition** — landed at MAINTENANCE.md §3.2; cites the orphaned `repo-maintenance-protocol-spec` SPEC + `tools/maintenance/dynamic-readme-partition.py`. ✓
- **(c) Three-way toolchain table with flip criteria** — landed at §1.1.2; columns are exactly Legacy / Flexible / ADR per Task 040 §C; flip criteria cite ST-1 SPEC §1. ✓
- **(d) Deterministic staleness algorithm with `MAINT_STALE_DAYS`** — landed at §3.4; pseudocode + signals + worked-example cross-reference. ✓
- **(e) §3.5 dup-id circular dependency resolved** — landed; "self-file on first encounter, surface on subsequent" rule + ADR-validator step `[5/6]` interaction documented. ✓
- **(f) ≥7 Gherkin scenarios anchored M.B.1–M.B.7** — 15 scenarios delivered (M.B.1×1, M.B.2×3, M.B.3×2, M.B.4×2, M.B.5×2, M.B.6×2, M.B.7×2). ✓
- **ST-1 falsification** ("criteria require LLM judgment") — did not fire. All seven TFC.1.x predicates are git/grep/exit-code based.
- **ST-3 falsification** ("decision tree exceeds 5 levels or 12 leaves") — did not fire. Tree is 3 levels / 4 leaves.
- **ST-4 falsification** ("legitimate readmes flagged ERROR") — did not fire. WARN-tier `M.B.6:missing-marker` does not gate; 170/170 advisory hits, 0 ERRORs.
- **ST-5 falsification** ("aggregator duplicates GATE schema") — did not fire. `PartitionGuard` test asserts schema-content equality and absence of `_score_*` helpers on the AGGREGATOR.
- **ST-6 falsification** ("§3.5 amendment proposes mutation of `decisions/`") — did not fire. M.B.7 second Gherkin explicitly forbids it; ST-3 staleness audit excludes `decisions/` from its scan.

## Recommendation

The four-agents-in-parallel dispatch pattern was the largest single Phase A in the chain (ST-1 + ST-3 + ST-4 + ST-5 ran concurrently). Two minor coordination considerations surfaced for future similar batches:

1. **Shared-file additive merge.** All three tooling subtasks shipped a new `tools/maintenance/readme.md`; the second/third agent to land merged additively rather than overwriting. Documenting this convention explicitly in the dispatch prompt (which we did inline) made the merge frictionless. A formal `tools/check-additive-merge.py` is not warranted at this volume.
2. **`tools/check-governance.sh` step-numbering churn.** Each tooling subtask added its own `[opt]` block, which would in principle compete for the same line range. In practice the agents inserted their blocks in non-overlapping regions (one between assumption-log and prompt-block, one between prompt-block and trust-audit GATE) and the file remained well-formed. A future Task could canonicalise the `[opt]` block ordering with a sentinel-anchor pattern, but this is below the friction threshold.

No prompt restructure recommended. The 6-subtask plan executed cleanly on first pass.
