---
type: note
status: draft
slug: task-032-st1-research-adr-corpus-extraction
summary: "Subtask ST-1 (research head): extract implicit ADR-style architectural decisions already embedded in the 8 root specs and propose them as the bootstrap ADR-0001..N corpus, mitigating ASM-007 (cultural assumption that humans author ADRs proactively)."
created: 2026-05-06
updated: 2026-05-06
---

# ST-1: Research — ADR Corpus Extraction from Governance Specs

**Executor:** main-agent

**Parallelism:** Phase A (parallel) — runs concurrently with ST-2, ST-3, ST-4. No inter-dependencies.

**Prompt:** [`/prompts/research-adr-corpus-extraction/prompt.md`](../../../prompts/research-adr-corpus-extraction/prompt.md) — the executable instruction set for this subtask. The Goal, Falsification, Inputs, Acceptance Criteria, Dependencies, and Estimated Effort sections that previously lived inline have moved to that prompt's [`brief.md`](../../../prompts/research-adr-corpus-extraction/brief.md) per Task 041 (PR #70 review C.3 audit-graph repair).
