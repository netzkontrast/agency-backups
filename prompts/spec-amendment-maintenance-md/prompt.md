---
type: prompt
status: active
slug: spec-amendment-maintenance-md
summary: "Land the MAINTENANCE.md edits per Task 039 (a)-(f). §1.1.2 becomes a three-way Legacy/Flexible/ADR toolchain table with explicit flip criteria from ST-1. §2.3 mandates the trust-audit gate. §3.2 mandates dynamic-readme partition (cites S..."
created: 2026-05-06
updated: 2026-05-06
prompt_kind: task-spec
prompt_framework: RISEN+ReAct
prompt_target_agent: "Claude Code"
prompt_relates_to_task: maintenance-spec-integration
---

# ST-6: Spec Amendment — MAINTENANCE.md — Task-Spec Prompt

## Framework

RISEN+ReAct. The prompt declares the framework in frontmatter (`prompt_framework: RISEN+ReAct`) and restates it here for `fm-validate` header conformance. The R/I/S/E sections below carry the canonical roles; a final **Constraints** section groups normative scope/failure rules per repo convention.

## R — Role

You are the **main-agent** dispatched to execute subtask ST-6 of [Task maintenance-spec-integration](../../tasks/039-maintenance-spec-integration/task.md). Your remit is bounded by the Acceptance Criteria in [`brief.md`](./brief.md); you MUST NOT expand scope beyond those criteria without surfacing the divergence in `friction-log.md`.

**Parallelism:** Phase B (sequential) — depends on ST-1, ST-2, ST-3, ST-4, ST-5. MUST wait for all five Phase A subtasks to land..

## I — Input

- ST-1 output: `research/toolchain-flip-criteria/output/SPEC.md`.
- ST-2 output: `research/spec-staleness-decision-formalization/output/SPEC.md`.
- ST-3 / ST-4 / ST-5 implementations.
- `research/agentic-eval-trust-improvement-spec/output/SPEC.md`.
- `research/repo-maintenance-protocol-spec/output/SPEC.md`.
- `research/governance-specs-update-research/output/SPEC.md` §2.
- `FOLDERS.md:115` (ADR T4-immutability assertion).
- `PRE_COMMIT.md:107-129` (§7.C ADR validator).
- `tasks/039-maintenance-spec-integration/task.md` — parent task chain-level context.

## S — Steps

1. The agent MUST produce the artefact required by acceptance criterion: MAINTENANCE.md §1.1.2 has a three-way table with flip criteria from ST-1. **The table is exactly three columns (Legacy / Flexible / ADR) per Task 040 §C — no fourth column for MCP servers.** A footnote MAY mention MorphLLM-Fast-Apply as a future option, but no SHOULD/MUST mandate (per Task 040 §C: not configured today).
2. The agent MUST produce the artefact required by acceptance criterion: MAINTENANCE.md §2.3 mandates trust-audit gate (cites Task 035 ST-4 GATE + this Task's ST-5 AGGREGATOR).
3. The agent MUST produce the artefact required by acceptance criterion: MAINTENANCE.md §3.2 cites ST-4 partition linter.
4. The agent MUST produce the artefact required by acceptance criterion: MAINTENANCE.md §3.4 has deterministic algorithm cross-referencing ST-2 + ST-3.
5. The agent MUST produce the artefact required by acceptance criterion: MAINTENANCE.md §3.5 references Task 033 ST-3 dup-id linter as the resolution to the circular dependency.
6. The agent MUST produce the artefact required by acceptance criterion: MAINTENANCE.md §1 documents ADR T4-immutability.
7. The agent MUST produce the artefact required by acceptance criterion: ≥7 Gherkin scenarios anchored M.B.1-M.B.7.
8. The agent MUST produce the artefact required by acceptance criterion: **NEW (per Task 040 §A row §8 MERGE):** §1.1.2 prose lifts the *nightly maintenance* framing from the Gemini spec — vocabulary aligns; the citation MUST be to the Gemini source (informational only) and MUST NOT cite Tavily / Playwright / Morphllm / Chrome DevTools (per Task 040 §C). Cite Task 040 §A row §8 in the commit message.
9. The agent MUST produce the artefact required by acceptance criterion: `tools/check-governance.sh` exits 0.
10. The agent MUST verify every Acceptance Criterion enumerated in [`brief.md`](./brief.md) holds against the produced artefacts; on any failure the agent MUST iterate the relevant implementation step rather than weakening the criterion.
11. The agent MUST run `tools/check-governance.sh` and resolve every ERROR before committing; a non-zero exit MUST block the commit.
12. The agent SHOULD author or update `tasks/039-maintenance-spec-integration/friction-log.md` per FRUSTRATED.md FL[0-3] when frictions arise; absence of frictions MAY be recorded as `FL: 0`.
13. The agent MUST commit with a message that names `Task 039 ST-6` in its trailer; the agent MUST NOT push (the maintainer pushes after review).

## E — Expectations

- MAINTENANCE.md §1.1.2 has a three-way table with flip criteria from ST-1. **The table is exactly three columns (Legacy / Flexible / ADR) per Task 040 §C — no fourth column for MCP servers.** A footnote MAY mention MorphLLM-Fast-Apply as a future option, but no SHOULD/MUST mandate (per Task 040 §C: not configured today).
- MAINTENANCE.md §2.3 mandates trust-audit gate (cites Task 035 ST-4 GATE + this Task's ST-5 AGGREGATOR).
- MAINTENANCE.md §3.2 cites ST-4 partition linter.
- MAINTENANCE.md §3.4 has deterministic algorithm cross-referencing ST-2 + ST-3.
- MAINTENANCE.md §3.5 references Task 033 ST-3 dup-id linter as the resolution to the circular dependency.
- MAINTENANCE.md §1 documents ADR T4-immutability.
- ≥7 Gherkin scenarios anchored M.B.1-M.B.7.
- **NEW (per Task 040 §A row §8 MERGE):** §1.1.2 prose lifts the *nightly maintenance* framing from the Gemini spec — vocabulary aligns; the citation MUST be to the Gemini source (informational only) and MUST NOT cite Tavily / Playwright / Morphllm / Chrome DevTools (per Task 040 §C). Cite Task 040 §A row §8 in the commit message.
- `tools/check-governance.sh` exits 0.
- `tools/check-governance.sh` exits 0 on the produced commit.
- Commit message follows the parent task's convention; the commit cites `Task 039 ST-6` in its trailer.

## Constraints

- Dependency: ST-1, ST-2, ST-3, ST-4, ST-5 MUST land first. Task 033 ST-3 (dup-id linter) is a soft-dependency for §3.5.
- MUST NOT trigger the subtask's Falsification clause: Wrong cut **iff** §3.5 amendment proposes the coherence run mutates `decisions/<NNNN>-<slug>.md` files at any tier. Mitigation: M.B.7 Gherkin scenario explicitly forbids it; ST-3 staleness-audit excludes `decisions/` from its scan.
- MUST NOT inline this prompt's Goal/Inputs/Acceptance back into the subtask file — the subtask body is now a thin pointer per Task 041.
- MUST run `tools/check-governance.sh` before pushing; a non-zero exit MUST block the push.
- SHOULD cite the parent task's `task_id` in any commit-message trailer for traceability.
