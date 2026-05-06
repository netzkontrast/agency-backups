---
type: brief
status: active
slug: spec-amendment-maintenance-md-brief
summary: "Brief for prompt spec-amendment-maintenance-md — extracted from tasks/039-maintenance-spec-integration/subtasks/06-spec-amendment-maintenance-md.md per Task 041 (PR #70 review C.3 audit-graph repair)."
created: 2026-05-06
updated: 2026-05-06
---

# Brief — ST-6: Spec Amendment — MAINTENANCE.md

## Raw User Request

> Extract the inlined Execution Brief from `tasks/039-maintenance-spec-integration/subtasks/06-spec-amendment-maintenance-md.md` (ST-6) into a registered `/prompts/<slug>/` artefact, restoring the `task_uses_prompts ↔ prompt_relates_to_task` audit-graph edge severed in PR #70 (review finding C.3).

## Target Audience

The dispatched executor for [Task 039 `maintenance-spec-integration`](../../tasks/039-maintenance-spec-integration/task.md), specifically subtask ST-6 (06-spec-amendment-maintenance-md.md). Default executor: **main-agent**.

## Intended Model / Agent

Claude Code (or any agent that satisfies the executor declaration in the parent subtask file).

## Use-Case Context

This prompt drives subtask ST-6 of [Task maintenance-spec-integration](../../tasks/039-maintenance-spec-integration/task.md). The parent task's chain-level rationale lives in its `task.md`; this brief records only the subtask's local goal + inputs + acceptance + dependencies + effort, lifted verbatim from the subtask file at extraction time.

**Parallelism:** Phase B (sequential) — depends on ST-1, ST-2, ST-3, ST-4, ST-5. MUST wait for all five Phase A subtasks to land.

## Goal (from subtask)

Land the MAINTENANCE.md edits per Task 039 (a)-(f). §1.1.2 becomes a three-way Legacy/Flexible/ADR toolchain table with explicit flip criteria from ST-1. §2.3 mandates the trust-audit gate. §3.2 mandates dynamic-readme partition (cites ST-4). §3.4 has the deterministic algorithm (cites ST-2/ST-3). §3.5 resolves the dup-id circular dependency (cites Task 033 ST-3). §1 documents ADR T4-immutability per FOLDERS.md:115. ≥7 Gherkin scenarios per M.B.1-M.B.7 anchors.

## Falsification (from subtask)

Wrong cut **iff** §3.5 amendment proposes the coherence run mutates `decisions/<NNNN>-<slug>.md` files at any tier. Mitigation: M.B.7 Gherkin scenario explicitly forbids it; ST-3 staleness-audit excludes `decisions/` from its scan.

## Inputs (from subtask)

- ST-1 output: `research/toolchain-flip-criteria/output/SPEC.md`.
- ST-2 output: `research/spec-staleness-decision-formalization/output/SPEC.md`.
- ST-3 / ST-4 / ST-5 implementations.
- `research/agentic-eval-trust-improvement-spec/output/SPEC.md`.
- `research/repo-maintenance-protocol-spec/output/SPEC.md`.
- `research/governance-specs-update-research/output/SPEC.md` §2.
- `FOLDERS.md:115` (ADR T4-immutability assertion).
- `PRE_COMMIT.md:107-129` (§7.C ADR validator).

## Acceptance Criteria (from subtask)

1. MAINTENANCE.md §1.1.2 has a three-way table with flip criteria from ST-1. **The table is exactly three columns (Legacy / Flexible / ADR) per Task 040 §C — no fourth column for MCP servers.** A footnote MAY mention MorphLLM-Fast-Apply as a future option, but no SHOULD/MUST mandate (per Task 040 §C: not configured today).
2. MAINTENANCE.md §2.3 mandates trust-audit gate (cites Task 035 ST-4 GATE + this Task's ST-5 AGGREGATOR).
3. MAINTENANCE.md §3.2 cites ST-4 partition linter.
4. MAINTENANCE.md §3.4 has deterministic algorithm cross-referencing ST-2 + ST-3.
5. MAINTENANCE.md §3.5 references Task 033 ST-3 dup-id linter as the resolution to the circular dependency.
6. MAINTENANCE.md §1 documents ADR T4-immutability.
7. ≥7 Gherkin scenarios anchored M.B.1-M.B.7.
8. **NEW (per Task 040 §A row §8 MERGE):** §1.1.2 prose lifts the *nightly maintenance* framing from the Gemini spec — vocabulary aligns; the citation MUST be to the Gemini source (informational only) and MUST NOT cite Tavily / Playwright / Morphllm / Chrome DevTools (per Task 040 §C). Cite Task 040 §A row §8 in the commit message.
9. `tools/check-governance.sh` exits 0.

## Dependencies (from subtask)

ST-1, ST-2, ST-3, ST-4, ST-5 MUST land first. Task 033 ST-3 (dup-id linter) is a soft-dependency for §3.5.

## Estimated Effort (from subtask)

Large (~3 hours; biggest spec-amendment in the chain).
