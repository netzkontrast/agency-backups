---
type: index
status: active
slug: task-035-folder
summary: "Folder index for Task 035 — RESEARCH.md spec integration. Lifts three orphaned research outputs (agentic-eval-trust-improvement-spec, spec-driven-research-agentic-workflows, agentic-session-continuity-spec) into normative scope; mechanizes R.4.4 and R.6.5; resolves R.4.3 prompt-snapshot ambiguity."
created: 2026-05-06
updated: 2026-05-06
---

# Task 035 Folder

## What

Operational folder for Task 035. The biggest payload across the 031–038 chain: three orphaned research outputs become normative.

## Files

- [`task.md`](./task.md)
- [`subtasks/`](./subtasks/) — 1 research, 3 tooling, 1 spec amendment.

## Assumptions Log

- The session-continuity protocol (subtask 01 output) is implemented as a `state.md` file under `/research/<slug>/workspace/`; it is *not* a new top-level operational directory.
- The trust-audit gate (subtask 04 + spec amendment) is invoked at `research_phase: complete` transition only — not on every commit.
