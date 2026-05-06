---
type: note
status: draft
slug: task-035-st5-spec-amendment-research-md
summary: "Subtask ST-5 (Phase B): apply RESEARCH.md edits — §2.2 chunking rule, §4 continuity ref, §5.7 trust-audit clause, R.4.3 prompt-snapshot disambiguation, ≥6 Gherkin scenarios per R.B.1-R.B.6."
created: 2026-05-06
updated: 2026-05-06
---

# ST-5: Spec Amendment — RESEARCH.md

**Executor:** main-agent

## Goal

Land the RESEARCH.md edits per Task 035 (a)-(g): §2.2 spec-chunking rule, §4 session-continuity reference, §5.7 trust-audit clause, R.4.3 prompt-snapshot mid-run disambiguation, ≥6 Gherkin scenarios per R.B.1-R.B.6 anchors, references to ST-2/ST-3/ST-4 linters.

## Falsification

Wrong cut **iff** the §5.7 trust-audit clause references a cross-workspace AGGREGATOR (that belongs to Task 039). Mitigation: ST-5 cites ST-4's per-workspace GATE only.

## Inputs

- ST-1 output: `research/session-continuity-protocol-instantiation/output/SPEC.md`.
- ST-2/ST-3/ST-4 implementations.
- `research/agentic-eval-trust-improvement-spec/output/SPEC.md`.
- `research/spec-driven-research-agentic-workflows/output/SPEC.md` §spec-chunking.
- `research/agentic-session-continuity-spec/output/SPEC.md`.

## Acceptance Criteria

1. RESEARCH.md §2.2 mandates spec-chunking for synthesis runs >50k tokens.
2. RESEARCH.md §4 references session-continuity protocol per ST-1 output.
3. RESEARCH.md §5.7 mandates trust-audit GATE invocation at `research_phase: complete`.
4. RESEARCH.md R.4.3 disambiguates mid-run prompt-snapshot policy (lock-at-start preferred).
5. RESEARCH.md §5 has ≥6 Gherkin scenarios per R.B.1-R.B.6 anchors.
6. `tools/check-governance.sh` exits 0.

## Dependencies

ST-1, ST-2, ST-3, ST-4 MUST land first.

## Estimated Effort

Medium (~2 hours).
