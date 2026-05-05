---
type: index
status: active
slug: adr-spec-research-synthesis-prompt-readme
summary: "Index for prompt adr-spec-research-synthesis — drives Task 026 via /sc:analyze, /sc:brainstorm, and a full RISEN+ReAct research run producing the repo-native ADR governance spec."
created: 2026-05-05
updated: 2026-05-05
---

# Prompt — adr-spec-research-synthesis

- [`brief.md`](./brief.md) — Raw user request and context.
- [`prompt.md`](./prompt.md) — The executable research-proposal prompt.

## Usage

Execute via Task 026: `tasks/026-adr-spec-research-synthesis/task.md`. The prompt spawns a Research workspace at `research/adr-spec-research-synthesis/`.

## Key Constraints

- Input priority: repo root files first, Gemini draft second (reference only).
- Output: `research/adr-spec-research-synthesis/output/SPEC.md` following §0–§9 schema.
- SuperClaude skills invoked: `/sc:analyze`, `/sc:brainstorm`.
- Critical-thinking methods active: M06, M07, M08, M13.
