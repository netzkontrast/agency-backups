---
type: index
status: active
slug: core-architecture-review-2026-05-prompt-readme
summary: "Index for prompt core-architecture-review-2026-05 — drives the periodic architectural audit of the Agency substrate. Executed via Task 053; output lives at research/core-architecture-review-2026-05/output/REPORT.md."
created: 2026-05-07
updated: 2026-05-07
---

# Prompt — core-architecture-review-2026-05

- [`brief.md`](./brief.md) — Raw user request and authoring-note (retrospective).
- [`prompt.md`](./prompt.md) — The executable RISEN+ReAct research-proposal prompt.

## Usage

Execute via [Task 053](../../tasks/053-core-architecture-review-followups/task.md). Produces [`research/core-architecture-review-2026-05/output/REPORT.md`](../../research/core-architecture-review-2026-05/output/REPORT.md).

## Key Constraints

- Single-agent execution (no subagent fan-out).
- Citations MUST pin a specific commit SHA.
- The executor MUST NOT modify any audited file; findings become Tasks via the dispatching Task's `triage.md`.
- Boundary discipline: the deliverable MUST land under `/research/<slug>/output/`, never inside the dispatching Task folder.

## Assumptions Log

(none)

## Re-execution

To re-audit on a future commit, copy this prompt to `prompts/core-architecture-review-YYYY-MM/` (new slug), update Provenance, and dispatch via a successor Task.
