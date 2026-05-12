---
type: note
status: draft
slug: task-039-st3-tooling-staleness-audit-script
summary: "Subtask ST-3: ship tools/maintenance/staleness-audit.py implementing the deterministic staleness decision tree from ST-2 SPEC. Honours MAINT_STALE_DAYS env var (default 7)."
created: 2026-05-06
updated: 2026-05-06
---

# ST-3: `staleness-audit` — MAINTENANCE.md §3.4 Mechanization

**Executor:** maintenance-agent
**Insertion point:** Not in `tools/check-governance.sh`; invoked by the nightly maintenance run only.

**Parallelism:** Phase A (parallel-grouped, soft-blocked) — runs alongside ST-1/ST-4/ST-5 but soft-depends on ST-2 SPEC. May ship with stub algorithm + upgrade post-ST-2.

**Prompt:** [`/prompts/tooling-staleness-audit-script/prompt.md`](../../../prompts/tooling-staleness-audit-script/prompt.md) — the executable instruction set for this subtask. The Goal, Falsification, Inputs, Acceptance Criteria, Dependencies, and Estimated Effort sections that previously lived inline have moved to that prompt's [`brief.md`](../../../prompts/tooling-staleness-audit-script/brief.md) per Task 041 (PR #70 review C.3 audit-graph repair).
