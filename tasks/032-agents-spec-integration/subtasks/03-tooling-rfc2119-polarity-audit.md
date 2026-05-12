---
type: note
status: draft
slug: task-032-st3-tooling-rfc2119-polarity-audit
summary: "Subtask ST-3: ship tools/check-rfc2119-polarity.py — a static analysis that flags potential MUST/MUST NOT polarity inversions in spec text and ADR extraction, mitigating ASM-001 from research/adr-assumption-audit/output/REPORT.md §1."
created: 2026-05-06
updated: 2026-05-06
---

# ST-3: `check-rfc2119-polarity` — ASM-001 Mitigation

**Executor:** main-agent
**Insertion point:** `[opt]` WARN-tier — runs after step `[5/5]` ADR validator; gates only on `--strict` invocation.

**Parallelism:** Phase A (parallel) — runs concurrently with ST-1, ST-2, ST-4. No inter-dependencies.

**Prompt:** [`/prompts/tooling-rfc2119-polarity-audit/prompt.md`](../../../prompts/tooling-rfc2119-polarity-audit/prompt.md) — the executable instruction set for this subtask. The Goal, Falsification, Inputs, Acceptance Criteria, Dependencies, and Estimated Effort sections that previously lived inline have moved to that prompt's [`brief.md`](../../../prompts/tooling-rfc2119-polarity-audit/brief.md) per Task 041 (PR #70 review C.3 audit-graph repair).
