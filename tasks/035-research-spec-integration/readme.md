---
type: index
status: completed
slug: task-035-folder
summary: "Folder index for Task 035 — RESEARCH.md spec integration. Lifts three orphaned research outputs (agentic-eval-trust-improvement-spec, spec-driven-research-agentic-workflows, agentic-session-continuity-spec) into normative scope; mechanizes R.4.4 and R.6.5; resolves R.4.3 prompt-snapshot ambiguity."
created: 2026-05-06
updated: 2026-05-07
---

# Task 035 Folder

## What

Operational folder for Task 035. The biggest payload across the 031–038 chain: three orphaned research outputs become normative.

## Files

- [`task.md`](./task.md) — `task_status: done`.
- [`friction-log.md`](./friction-log.md) — FL1 closure log.
- [`subtasks/`](./subtasks/) — 1 research, 3 tooling, 1 spec amendment.

## Closure summary

- Linters shipped: `tools/check-workspace-cleanliness.py` (R.4.4), `tools/check-external-result-downstream-task.py` (R.6.5), `tools/check-trust-audit.py` (Spec-J/K/L GATE).
- Research workspace shipped: [`research/session-continuity-protocol-instantiation/`](../../research/session-continuity-protocol-instantiation/) — concrete `state.md` format and resume protocol.
- RESEARCH.md amendments: §2.2 spec-chunking, §4.10 pause-and-resume, §5.0 enforcement-mapping refresh, §5.7 trust-audit GATE clause, R.4.3 prompt-snapshot lock-at-start, six Gherkin scenarios under §5.11 (R.B.1–R.B.6).
- Strict gates default off during the migration window; see [`friction-log.md`](./friction-log.md) for follow-ups.

## Assumptions Log

- The session-continuity protocol (subtask 01 output) is implemented as a `state.md` file under `/research/<slug>/workspace/`; it is *not* a new top-level operational directory.
- The trust-audit gate (subtask 04 + spec amendment) is invoked at `research_phase: complete` transition only — not on every commit.
