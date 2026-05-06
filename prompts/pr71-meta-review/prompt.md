---
type: prompt
status: active
slug: pr71-meta-review
summary: "Meta-review prompt: assess PR #71's governance critique of PR #70 for spec compliance and content quality."
created: 2026-05-06
updated: 2026-05-06
prompt_kind: general
prompt_framework: CoT
prompt_target_agent: "Claude Code"
---

# PR #71 Meta-Review

## Framework

**Chain-of-Thought.** One-shot analytical review. The agent reads the PR #71 review
artifact, cross-references every finding against the governing specs, then produces a
structured meta-critique covering: (A) spec-compliance of the artifact itself, and
(B) content quality of the 7 findings.

---

## § RFC 2119

The key words MUST, MUST NOT, REQUIRED, SHALL, SHALL NOT, SHOULD, SHOULD NOT, RECOMMENDED,
NOT RECOMMENDED, MAY, and OPTIONAL in this document are to be interpreted as described in
BCP 14 [RFC 2119] [RFC 8174] when, and only when, they appear in all capitals as shown here.

---

## I — Input

- Review artifact: `tasks/040-superclaude-spec-evaluation/pr-review.md` (PR #71, SHA `ec9109a`)
- Canonical reference: `research/pr27-governance-review/output/REVIEW.md`
- Governing specs: AGENTS.md, TASK.md, PROMPT.md, RESEARCH.md, FOLDERS.md, FRUSTRATED.md

## S — Steps

1. Read the review artifact in full.
2. Classify the artifact's placement against RESEARCH.md §2 and FOLDERS.md §1.
3. Check for a corresponding prompt in `/prompts/` and a research workspace.
4. For each of the 7 findings (C.1, C.2, C.3, M.1, M.2, m.1, m.2), verify spec-citation
   accuracy, severity calibration, and completeness.
5. Identify any findings the review missed.
6. Produce `output/REVIEW.md` with sections: Summary, Meta-Compliance Issues, Content Quality,
   Missed Findings, Strengths, Verdict.

## E — Expectations

- `research/pr71-meta-review/output/REVIEW.md` — structured meta-critique with RFC 2119
  normative language where applicable.

## Constraints

1. MUST assess both structural (artifact placement, prompt linkage) and content (finding
   accuracy) dimensions.
2. MUST distinguish between genuine defects and stylistic preferences.
3. MUST cite the specific spec clause for each structural finding.
4. MUST NOT rewrite or fix any file outside the research workspace.
5. MUST evaluate whether C.3's "Acceptable minimal fix" is actually acceptable per TASK.md §1.

## R — Role

Meta-reviewer: auditing a PR review for adherence to the same conventions the review
enforces in the reviewed PR. Surfaces drift with RFC 2119 precision.
