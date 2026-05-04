---
type: prompt
status: active
slug: mega-context-limit-management
summary: "Follow-up question on empirical testing of sliding window truncation vs infinite context for 100k-word manuscripts."
created: 2026-05-04
updated: 2026-05-04
prompt_kind: follow-up
prompt_framework: RISEN+ReAct
prompt_target_agent: "external"
prompt_relates_to_task: analyze-skillmd-novel-authoring
prompt_spawned_from_research: github-skillmd-novel-authoring-de-en
---

# Follow-up: Mega-Context Limit Management
# Framework: RISEN+ReAct

## 1. Context
The progressive disclosure model (often orchestrated using SKILL.md, an open standard markdown format for agentic instructions) manages metadata efficiently, but the handling of a completed, continuous 100,000-word manuscript is unresolved. Some tools utilize a truncation marker to pass only the last 1,000 words. It is unknown whether this damages long-term narrative foreshadowing and character arcs.

## 2. Objective
You MUST design and execute a benchmark to evaluate whether localized "sliding window" context truncation causes significant narrative degradation compared to theoretically infinite context windows.

## 3. Method
1. Define a set of character arcs and foreshadowing events in a massive manuscript.
2. Execute drafting scenarios using both a 1000-word truncation and full-document injection.
3. Compare continuity and narrative consistency.
