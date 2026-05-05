---
type: index
status: active
slug: spec-subagent-subtask-prompt-format
summary: "Index for Task 027 — execute the agency-adr-governance-spec research prompt to produce a normative ADR-governance spec that retroactively ratifies (or amends) the conventions Task 026 used provisionally for subtasks, sub-prompts, /sc:agent dispatch, and /sc:* command lifecycle."
created: 2026-05-05
updated: 2026-05-05
---

# Task 027 — Author the Agency ADR-Governance Spec

## What and Why

Task 027 is a single-agent research execution. It runs [`/prompts/agency-adr-governance-spec/prompt.md`](../../prompts/agency-adr-governance-spec/prompt.md) (a Category-B extraction rendered upstream by `research-prompt-optimizer v3.2.0`) to produce a normative ADR-governance spec for the agency repo.

The spec retroactively addresses ten conventions Task 026 used provisionally (per [`tasks/026-cleanup-dramatica-skills-corpus/notes.md §3`](../026-cleanup-dramatica-skills-corpus/notes.md) — the verbose planning-session frustration log). Each "Suggested rule for Task 027 to ratify" item there is an FE-anchored input to this task's spec.

## Linked Navigation

- [`task.md`](./task.md) — the goal, the plan, the inputs (10 FE items), the anti-patterns.
- [`friction-log.md`](./friction-log.md) — written at task close per [`FRUSTRATED.md`](../../FRUSTRATED.md). Until then this file does not exist.
- Executing prompt: [`/prompts/agency-adr-governance-spec/`](../../prompts/agency-adr-governance-spec/).
- Source-of-input task: [`/tasks/026-cleanup-dramatica-skills-corpus/`](../026-cleanup-dramatica-skills-corpus/) — provides the ten frustration items and the provisional conventions to ratify.
- Spawned research workspace: [`/research/agency-adr-governance-spec/`](../../research/agency-adr-governance-spec/) — initialised in plan step 3 of `task.md`.

## Workflow Assumptions

- The executing prompt at `/prompts/agency-adr-governance-spec/prompt.md` is verbatim per user instruction. Task 027 does not amend it.
- The spec produced by Task 027 lives at `research/agency-adr-governance-spec/output/SPEC.md` per [RESEARCH.md](../../RESEARCH.md). A copy of normative statements MAY be projected into a new `maintenance/adrs/` directory or onto a new `maintenance/adr-spec.md` — that decision is itself one of the spec's outputs.
- Cross-spec amendments (TASK.md / PROMPT.md / AGENTS.md) are FOLLOW-UP work, optionally filed as a sibling task at the close of Task 027. Task 027 does not amend the existing top-level specs in-flight.
- Task 026 stays `task_status: open` independently; Task 027 does not block it. Task 026 may dispatch its Phase A subtasks regardless of Task 027's status. The provisional conventions in Task 026 work; Task 027 just decides whether they ARE the conventions long-term.
