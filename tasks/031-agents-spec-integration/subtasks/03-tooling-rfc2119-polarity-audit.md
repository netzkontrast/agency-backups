---
type: note
status: draft
slug: task-031-st3-tooling-rfc2119-polarity-audit
summary: "Subtask ST-3: ship tools/check-rfc2119-polarity.py — a static analysis that flags potential MUST/MUST NOT polarity inversions in spec text and ADR extraction, mitigating ASM-001 from research/adr-assumption-audit/output/REPORT.md §1."
created: 2026-05-06
updated: 2026-05-06
---

# ST-3: `check-rfc2119-polarity` — ASM-001 Mitigation

## Goal

Ship `tools/check-rfc2119-polarity.py` that scans every root spec and every `research/<slug>/output/SPEC.md` for adjacent `MUST` / `MUST NOT` clauses on the same subject, reporting candidates for human review. Mitigates the polarity-inversion blind spot identified in `research/adr-assumption-audit/output/REPORT.md §1 ASM-001`.

## Falsification

Wrong cut **iff** the false-positive rate exceeds 30% on the existing root-spec corpus. Mitigation: the check is advisory (WARN), not gating; agents review; the value is catching the rare-but-high-blast inversions, not eliminating false positives.

## Inputs

- [`research/adr-assumption-audit/output/REPORT.md`](../../../research/adr-assumption-audit/output/REPORT.md) §1 (ASM-001 description + worked example of a polarity inversion).
- All 8 root specs (test corpus).
- [`maintenance/language-spec.md`](../../../maintenance/language-spec.md) (RFC 2119 keyword definition).

## Acceptance Criteria

1. **Surface.** `python3 tools/check-rfc2119-polarity.py <file-or-dir>` reports each suspected polarity pair.
2. **Heuristic.** For each MUST/MUST NOT keyword, extract the noun phrase being constrained (subject + complement). Pair across the file when subjects match within edit-distance threshold.
3. **Output.** WARN-level diagnostics with file:line of both poles + the matched subject.
4. **Tests.** `tests/test_rfc2119_polarity.py` covers: synthetic inversion (catches it), legitimate negation (does not flag), keyword in code-block (skips).
5. **Integration.** `tools/check-governance.sh` runs it WARN-tier on root specs + SPEC.md files.

## Dependencies

None. Phase A.

## Estimated Effort

Medium (~150 LOC + 100 LOC tests; subject-extraction heuristic is the bulk).

## Agent Prompt

```text
Implement tools/check-rfc2119-polarity.py.

Repo root: /home/user/agency
Branch: claude/integrate-repo-specs-cIWtI

Read first:
  - research/adr-assumption-audit/output/REPORT.md §1 ASM-001
  - maintenance/language-spec.md
  - tools/check-governance.sh

Acceptance: see file. Use Python 3.11 stdlib only. No NLP dependency
beyond regex + simple noun-phrase heuristic. False-positive rate ≤ 30%
on the 8 root specs.

When done:
  python3 -m unittest discover -s tests
  python3 tools/check-rfc2119-polarity.py AGENTS.md TASK.md PROMPT.md \
    RESEARCH.md FOLDERS.md PRE_COMMIT.md FRUSTRATED.md MAINTENANCE.md
  Commit "feat(tools): RFC-2119 polarity audit (Task 031 ST-3, ASM-001 mitigation)".
  Do NOT push.
```
