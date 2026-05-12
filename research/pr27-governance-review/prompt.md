---
type: prompt
status: active
slug: pr27-governance-review
summary: "Snapshot of the executing prompt at run-start (immutable per RESEARCH.md §4.3)."
created: 2026-05-04
updated: 2026-05-04
prompt_kind: general
prompt_framework: CoT
prompt_target_agent: "Claude Code"
---

# PR #27 Governance Review

## Framework

**Chain-of-Thought.** One-shot analytical review. The agent reads the full PR diff and the
relevant governance specs (AGENTS.md, TASK.md, PROMPT.md, RESEARCH.md, MAINTENANCE.md),
then produces a structured critique covering correctness, completeness, scope, and
audit-graph integrity.

---

## § RFC 2119

The key words MUST, MUST NOT, REQUIRED, SHALL, SHALL NOT, SHOULD, SHOULD NOT, RECOMMENDED,
NOT RECOMMENDED, MAY, and OPTIONAL in this document are to be interpreted as described in
BCP 14 [RFC 2119] [RFC 8174] when, and only when, they appear in all capitals as shown here.

---

## Input

- PR diff: 19 files changed, +251 / −207 lines on branch `claude/analyze-code-PfoLl`
- Driving prompt snapshot: `prompts/repo-coherence-check/prompt.md`
- Governance specs: AGENTS.md, TASK.md, PROMPT.md, RESEARCH.md, FOLDERS.md, MAINTENANCE.md, PRE_COMMIT.md

## Steps

1. Read the PR diff in full.
2. Cross-reference each change cluster against the governance spec it touches.
3. Identify correctness issues, scope concerns, audit-graph gaps, and self-referential inconsistencies.
4. Produce `output/REVIEW.md` with sections: Summary, Strengths, Issues, Verdict.

## Deliverable

`research/pr27-governance-review/output/REVIEW.md` — structured critique with RFC 2119
normative language where applicable.

## Constraints

1. MUST assess every change cluster named in the PR body.
2. MUST distinguish between genuine defects and stylistic preferences.
3. MUST cite the specific spec clause for each finding.
4. MUST NOT rewrite or "fix" any file outside the research workspace.
