---
type: index
status: active
slug: deepwiki-rendering-conventions-agentic-workflows-prompt-readme
summary: "Index for stub prompt deepwiki-rendering-conventions-agentic-workflows — preserves audit graph for the externally executed Gemini research run on DeepWiki rendering, conventions, and agentic workflows."
created: 2026-05-07
updated: 2026-05-07
---

# Stub Prompt — deepwiki-rendering-conventions-agentic-workflows

- [`prompt.md`](./prompt.md) — Stub per RESEARCH.md §6.3 (canonical RISEN+ReAct headings retrofitted for fm-validate conformance).
- [`brief.md`](./brief.md) — Raw paraphrased request + audience + execution context.

## Note

Execution happened outside the repository (Gemini). The full originating prompt is at `research/gemini/deepwiki-rendering-conventions-agentic-workflows/research-prompt_deepwiki-agent-prep.md`. The result is at `research/gemini/deepwiki-rendering-conventions-agentic-workflows/result.md`. Downstream analysis: Task 051; integration artifact: Task 052.

## Assumptions Log

- This stub preserves the audit graph per `RESEARCH.md §6.3` even though execution was external; no in-house RISEN+ReAct refinement has been performed because the originating prompt is itself a `schema_version 3.1` Category-B Extraction prompt authored upstream.
- The `## Framework` and RISEN headings inside `prompt.md` are retrofitted boilerplate (mirrors the `prompts/agency-adr-governance-spec/` pattern) so that `tools/fm/validate.py --check-body` passes; they are NOT canonical and SHOULD be normalized when the prompt is next executed in-house.
