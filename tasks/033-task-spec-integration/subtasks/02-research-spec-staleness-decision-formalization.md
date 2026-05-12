---
type: note
status: draft
slug: task-033-st2-research-spec-staleness-decision-formalization
summary: "Subtask ST-2 (research, shared with Task 039): formalize MAINTENANCE.md §3.4 staleness decision algorithm — produce a deterministic decision tree mapping observable signals to {still accurate / drifted / completed-by-drift / no-longer-desirable}."
created: 2026-05-06
updated: 2026-05-06
---

# ST-2: Research — Staleness Decision Formalization

**Executor:** main-agent

**Parallelism:** Phase A (parallel) — runs concurrently with ST-1, ST-3, ST-4. **Cross-Task shared with Task 039 ST-2** — whichever Task dispatches first authors the SPEC; the other consumes via filesystem detection (test -f).

**Prompt:** [`/prompts/research-spec-staleness-decision-formalization/prompt.md`](../../../prompts/research-spec-staleness-decision-formalization/prompt.md) — the executable instruction set for this subtask. The Goal, Falsification, Inputs, Acceptance Criteria, Dependencies, and Estimated Effort sections that previously lived inline have moved to that prompt's [`brief.md`](../../../prompts/research-spec-staleness-decision-formalization/brief.md) per Task 041 (PR #70 review C.3 audit-graph repair).
