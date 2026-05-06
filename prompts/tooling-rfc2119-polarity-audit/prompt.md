---
type: prompt
status: active
slug: tooling-rfc2119-polarity-audit
summary: "Ship `tools/check-rfc2119-polarity.py` that scans every root spec, every `research/<slug>/output/SPEC.md`, **AND every `decisions/<NNNN>-<slug>.md`** for adjacent `MUST` / `MUST NOT` clauses on the same subject, reporting candidates for ..."
created: 2026-05-06
updated: 2026-05-06
prompt_kind: task-spec
prompt_framework: RISEN+ReAct
prompt_target_agent: "Claude Code"
prompt_relates_to_task: agents-spec-integration
---

# ST-3: `check-rfc2119-polarity` — ASM-001 Mitigation — Task-Spec Prompt

## Framework

RISEN+ReAct. The prompt declares the framework in frontmatter (`prompt_framework: RISEN+ReAct`) and restates it here for `fm-validate` header conformance. The R/I/S/E sections below carry the canonical roles; a final **Constraints** section groups normative scope/failure rules per repo convention.

## R — Role

You are the **main-agent** dispatched to execute subtask ST-3 of [Task agents-spec-integration](../../tasks/032-agents-spec-integration/task.md). Your remit is bounded by the Acceptance Criteria in [`brief.md`](./brief.md); you MUST NOT expand scope beyond those criteria without surfacing the divergence in `friction-log.md`.

**Parallelism:** Phase A (parallel) — runs concurrently with ST-1, ST-2, ST-4. No inter-dependencies..

## I — Input

- [`research/adr-assumption-audit/output/REPORT.md`](../../../research/adr-assumption-audit/output/REPORT.md) §1 (ASM-001 description + worked example of a polarity inversion).
- All 8 root specs (test corpus).
- [`maintenance/language-spec.md`](../../../maintenance/language-spec.md) (RFC 2119 keyword definition).
- `tasks/032-agents-spec-integration/task.md` — parent task chain-level context.

## S — Steps

1. The agent MUST treat the following preamble as authoritative orientation before executing any subsequent step: Implement tools/check-rfc2119-polarity.py. Read first: - research/adr-assumption-audit/output/REPORT.md §1 ASM-001 - maintenance/language-spec.md - tools/check-governance.sh Acceptance: see file. Use Python 3.11 stdlib only. No NLP dependency beyond regex + simple noun-phrase heuristic. False-positive rate ≤ 30% on the 8 root specs. When done: python3 -m unittest discover -s tests python3 tools/check-rfc2119-polarity.py AGENTS.md TASK.md PROMPT.md \ RESEARCH.md FOLDERS.md PRE_COMMIT.md FRUSTRATED.md MAINTENANCE.md Commit "feat(tools): RFC-2119 polarity audit (Task 032 ST-3, ASM-001 mitigation)". Do NOT push.
2. The agent MUST verify every Acceptance Criterion enumerated in [`brief.md`](./brief.md) holds against the produced artefacts; on any failure the agent MUST iterate the relevant implementation step rather than weakening the criterion.
3. The agent MUST run `tools/check-governance.sh` and resolve every ERROR before committing; a non-zero exit MUST block the commit.
4. The agent SHOULD author or update `tasks/032-agents-spec-integration/friction-log.md` per FRUSTRATED.md FL[0-3] when frictions arise; absence of frictions MAY be recorded as `FL: 0`.
5. The agent MUST commit with a message that names `Task 032 ST-3` in its trailer; the agent MUST NOT push (the maintainer pushes after review).

## E — Expectations

- **Surface.** `python3 tools/check-rfc2119-polarity.py <file-or-dir>` reports each suspected polarity pair.
- **Heuristic.** For each MUST/MUST NOT keyword, extract the noun phrase being constrained (subject + complement). Pair across the file when subjects match within edit-distance threshold.
- **Output.** WARN-level diagnostics with file:line of both poles + the matched subject.
- **Tests.** `tests/test_rfc2119_polarity.py` covers: synthetic inversion (catches it), legitimate negation (does not flag), keyword in code-block (skips).
- **Integration.** `tools/check-governance.sh` runs it WARN-tier on root specs + SPEC.md files.
- `tools/check-governance.sh` exits 0 on the produced commit.
- Commit message follows the parent task's convention; the commit cites `Task 032 ST-3` in its trailer.

## Constraints

- Dependency: None. Phase A.
- MUST NOT trigger the subtask's Falsification clause: Wrong cut **iff** the false-positive rate exceeds 30% on the existing root-spec corpus. Mitigation: the check is advisory (WARN), not gating; agents review; the value is catching the rare-but-high-blast inversions, not eliminating false positives.
- MUST NOT inline this prompt's Goal/Inputs/Acceptance back into the subtask file — the subtask body is now a thin pointer per Task 041.
- MUST run `tools/check-governance.sh` before pushing; a non-zero exit MUST block the push.
- SHOULD cite the parent task's `task_id` in any commit-message trailer for traceability.
