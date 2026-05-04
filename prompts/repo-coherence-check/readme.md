---
type: index
status: active
slug: repo-coherence-check
summary: "Directory index for the repo-coherence-check self-improvement routine prompt."
created: 2026-05-04
updated: 2026-05-04
---

# Prompt — Repo Coherence Check

**What:** This folder holds the self-improvement routine prompt. Unlike research proposals or task-specs, this prompt is designed to be **executed repeatedly** — at session start, on an interval, or before opening any new Task.

**Why here:** Per `PROMPT.md §2`, every executable instruction set lives in `/prompts/<slug>/`.

## Navigation

- [brief.md](./brief.md) — Root cause analysis and original request that motivated this prompt.
- [prompt.md](./prompt.md) — The deliverable: full RISE-DX prompt with 6-step execution spine, reflection gates, and wiring instructions for Claude Code.

## How to Execute

```
Execute prompts/repo-coherence-check/prompt.md
```

Or, for automated wiring, see `prompt.md §Wiring as a Claude Code Routine`.

## Runtime Artefacts

This prompt does not produce files in `/research/`. Instead it:
- Modifies files in-place (T1/T2 repairs).
- Creates Tasks in `/tasks/` (T3 findings).
- Appends a record to [`/maintenance/run-log.md`](../../maintenance/run-log.md).

## Assumptions Log

- The prompt is classified as `prompt_kind: tool-instruction` (not `research-proposal`) because it produces in-place repairs and log entries, not a research workspace.
- Framework is RISE-DX (reflection-driven spine) rather than RISEN+ReAct because the output is adaptive to what the agent finds in the delta, not a fixed deliverable format.
