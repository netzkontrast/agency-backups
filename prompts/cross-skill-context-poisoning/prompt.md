---
type: prompt
status: active
slug: cross-skill-context-poisoning
summary: "Follow-up question on arbitrating stylistic conflicts when multiple SKILL.md files are loaded simultaneously."
created: 2026-05-04
updated: 2026-05-04
prompt_kind: follow-up
prompt_framework: RISEN+ReAct
prompt_target_agent: "external"
prompt_relates_to_task: analyze-skillmd-novel-authoring
prompt_spawned_from_research: github-skillmd-novel-authoring-de-en
---

# Follow-up: Cross-Skill Context Poisoning
# Framework: RISEN+ReAct

## 1. Context
The SKILL.md (an open standard markdown format for agentic instructions) specification allows agents to load multiple skills simultaneously. It remains undocumented how neural architectures arbitrate severe stylistic conflicts if, for example, a "Hard Sci-Fi Worldbuilder" skill and a "Comedic Romance Dialogue" skill are invoked into the same context window.

## 2. Objective
You MUST investigate the stylistic resolution mechanisms (or failure modes) when contradictory SKILL.md persona instructions are concurrently active.

## 3. Method
1. Create strongly conflicting persona skills.
2. Load both simultaneously and prompt for scene generation.
3. Document which instructions override the others and identify any systemic arbitration patterns.
