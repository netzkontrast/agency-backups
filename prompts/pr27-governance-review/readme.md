---
type: index
status: active
slug: pr27-governance-review
summary: "Prompt workspace: governance review of PR #27."
created: 2026-05-04
updated: 2026-05-04
---

# Prompt: pr27-governance-review

Analytical review prompt for PR #27 ("fix(governance): restore green check-governance +
clarify spec semantics"). Spawned by Claude Code in response to a human operator request
on 2026-05-04.

## Files

- [brief.md](./brief.md) — Original user request and context.
- [prompt.md](./prompt.md) — The executable prompt (CoT, general kind).

## Execution

This prompt was executed immediately in the same session it was authored.
Research output: [`research/pr27-governance-review/output/REVIEW.md`](../../research/pr27-governance-review/output/REVIEW.md).

## Assumptions

- Classified as `prompt_kind: general` rather than `research-proposal` because the review
  is a one-shot analytical output, not a multi-pass research synthesis.
- `prompt_framework: CoT` chosen over RISE-DX because the input (PR diff) is fixed;
  no iterative adaptation is needed.
