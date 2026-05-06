---
type: brief
status: active
slug: tooling-rfc2119-polarity-audit-brief
summary: "Brief for prompt tooling-rfc2119-polarity-audit — extracted from tasks/032-agents-spec-integration/subtasks/03-tooling-rfc2119-polarity-audit.md per Task 041 (PR #70 review C.3 audit-graph repair)."
created: 2026-05-06
updated: 2026-05-06
---

# Brief — ST-3: `check-rfc2119-polarity` — ASM-001 Mitigation

## Raw User Request

> Extract the inlined Execution Brief from `tasks/032-agents-spec-integration/subtasks/03-tooling-rfc2119-polarity-audit.md` (ST-3) into a registered `/prompts/<slug>/` artefact, restoring the `task_uses_prompts ↔ prompt_relates_to_task` audit-graph edge severed in PR #70 (review finding C.3).

## Target Audience

The dispatched executor for [Task 032 `agents-spec-integration`](../../tasks/032-agents-spec-integration/task.md), specifically subtask ST-3 (03-tooling-rfc2119-polarity-audit.md). Default executor: **main-agent**.

## Intended Model / Agent

Claude Code (or any agent that satisfies the executor declaration in the parent subtask file).

## Use-Case Context

This prompt drives subtask ST-3 of [Task agents-spec-integration](../../tasks/032-agents-spec-integration/task.md). The parent task's chain-level rationale lives in its `task.md`; this brief records only the subtask's local goal + inputs + acceptance + dependencies + effort, lifted verbatim from the subtask file at extraction time.

**Parallelism:** Phase A (parallel) — runs concurrently with ST-1, ST-2, ST-4. No inter-dependencies.

**Insertion point:** `[opt]` WARN-tier — runs after step `[5/5]` ADR validator; gates only on `--strict` invocation.

## Goal (from subtask)

Ship `tools/check-rfc2119-polarity.py` that scans every root spec, every `research/<slug>/output/SPEC.md`, **AND every `decisions/<NNNN>-<slug>.md`** for adjacent `MUST` / `MUST NOT` clauses on the same subject, reporting candidates for human review. Mitigates the polarity-inversion blind spot identified in `research/adr-assumption-audit/output/REPORT.md §1 ASM-001`.

**Urgency upgraded post-Task-031.** With `tools/adr/synthesize.py` now actively rewriting `AGENTS.md` between the `<!-- BEGIN/END AGENCY-ADR SYNTHESIS -->` markers, an ASM-001 polarity inversion in a single `decisions/*.md` would silently invert governance language in AGENTS.md on the next synthesizer run. The linter that ST-3 ships is no longer a precaution — it is the missing guard rail on the deployed pipeline. Pair this WARN-tier output with `tools/adr/cli.py validate` (which catches structural errors but not semantic polarity inversions) for full coverage.

## Falsification (from subtask)

Wrong cut **iff** the false-positive rate exceeds 30% on the existing root-spec corpus. Mitigation: the check is advisory (WARN), not gating; agents review; the value is catching the rare-but-high-blast inversions, not eliminating false positives.

## Inputs (from subtask)

- [`research/adr-assumption-audit/output/REPORT.md`](../../../research/adr-assumption-audit/output/REPORT.md) §1 (ASM-001 description + worked example of a polarity inversion).
- All 8 root specs (test corpus).
- [`maintenance/language-spec.md`](../../../maintenance/language-spec.md) (RFC 2119 keyword definition).

## Acceptance Criteria (from subtask)

1. **Surface.** `python3 tools/check-rfc2119-polarity.py <file-or-dir>` reports each suspected polarity pair.
2. **Heuristic.** For each MUST/MUST NOT keyword, extract the noun phrase being constrained (subject + complement). Pair across the file when subjects match within edit-distance threshold.
3. **Output.** WARN-level diagnostics with file:line of both poles + the matched subject.
4. **Tests.** `tests/test_rfc2119_polarity.py` covers: synthetic inversion (catches it), legitimate negation (does not flag), keyword in code-block (skips).
5. **Integration.** `tools/check-governance.sh` runs it WARN-tier on root specs + SPEC.md files.

## Dependencies (from subtask)

None. Phase A.

## Estimated Effort (from subtask)

Medium (~150 LOC + 100 LOC tests; subject-extraction heuristic is the bulk).
