---
type: index
status: active
slug: agency-adr-governance-spec
summary: "Index for the agency-adr-governance-spec prompt — drives Task 027's Category-B extraction that produces a normative ADR-governance spec for the agency repo (lifecycle + token-efficient rule synthesis + tooling acceptance criteria)."
created: 2026-05-05
updated: 2026-05-05
---

# Prompt — Agency ADR-Governance Spec

## What and Why

This folder holds the executable prompt that operationalizes [Task 027 — spec-subagent-subtask-prompt-format](../../tasks/027-spec-subagent-subtask-prompt-format/). The Task is the plan; this prompt is the binding instruction set the executing agent reads end-to-end before touching any file. The prompt body was rendered upstream by `research-prompt-optimizer v3.2.0` and saved verbatim per the user's instruction.

## Linked Navigation

- [`brief.md`](./brief.md) — the unedited user instruction and target context.
- [`prompt.md`](./prompt.md) — the executable instruction set (Category B / RISEN+ReAct / `status: active`). The renderer's two upstream YAML metadata blocks are preserved verbatim inside a fenced ```yaml block at the top of the body for traceability.
- Task that consumes this prompt: [`/tasks/027-spec-subagent-subtask-prompt-format/`](../../tasks/027-spec-subagent-subtask-prompt-format/).
- Sibling task this prompt unblocks: [`/tasks/026-cleanup-dramatica-skills-corpus/`](../../tasks/026-cleanup-dramatica-skills-corpus/) — its subtask / sub-prompt / subagent-dispatch / `/sc:*`-usage conventions are PROVISIONAL pending the spec this prompt produces.

## Workflow Assumptions

- The renderer's two upstream YAML blocks (one with `schema_version: 3.1`, one with `topic: …`) are intentionally NOT promoted to the file's primary frontmatter. They contain depth-2 keys that would violate the repo's YAML-depth-1 constraint ([`AGENTS.md § YAML Depth Rule`](../../AGENTS.md)). They are preserved inside a fenced ```yaml code block in the body so re-rendering upstream stays a clean replace operation.
- The primary frontmatter at the top of `prompt.md` carries the repo-required L1 + `prompt_*` namespace per [`PROMPT.md §3`](../../PROMPT.md). Both representations coexist; only the top frontmatter is read by `tools/validate-frontmatter.py`.
