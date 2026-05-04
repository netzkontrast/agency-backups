---
type: prompt
status: active
slug: superclaude-integration-spec
summary: "Immutable run-start snapshot of /prompts/superclaude-integration-spec/prompt.md."
created: 2026-05-04
updated: 2026-05-04
prompt_kind: research-proposal
prompt_framework: RISEN+ReAct
prompt_target_agent: "Claude Code"
prompt_relates_to_task: ""
prompt_spawned_from_research: ""
---

# SuperClaude Integration Research Prompt (Snapshot)

*Immutable run-start snapshot of `/prompts/superclaude-integration-spec/prompt.md`.*

**Framework: RISEN + ReAct**

## Role

You are a senior agentic-workflow architect with deep knowledge of the Agency governance system (`AGENTS.md`, `TASK.md`, `RESEARCH.md`, `PROMPT.md`, `FOLDERS.md`) and the SuperClaude Framework v4.3.0 (30 commands, 20 agents, 7 behavioral modes, skills).

## Instructions

Produce a comprehensive integration specification (`SPEC.md`) that:

1. **Catalogs** every SuperClaude command (`/sc:*`), agent, and skill installed in `~/.claude/` with a one-line purpose summary.
2. **Maps** each catalog item to one or more Agency workflow phases (Prompt authoring, Research execution, Synthesis, Reflection, Task orchestration, Maintenance).
3. **Defines** concrete integration patterns — executable invocation examples.
4. **Specifies** how future Agency specs MUST include a SuperClaude Integration Block.
5. **Identifies** which existing root specs benefit from cross-links.
6. **Extends** MAINTENANCE.md with a new §5 (SuperClaude Integration Scan).

## Situation

SuperClaude Framework v4.3.0 installed at `~/.claude/`: 30 commands, 20 agents, skills, 7 modes, MCP integrations. Agency repo has strict governance model and has not yet formally integrated with SuperClaude.

## Expected Deliverable

`/research/superclaude-integration-spec/output/SPEC.md` with 6 sections: Catalog, Phase Mapping, Integration Patterns, New Spec Template, Root Spec Link Recommendations, Anti-Patterns.

## Exclusions

- MUST NOT duplicate entire SC command files verbatim.
- MUST NOT propose changes outside the Agency repo scope.
- MUST NOT recommend SC tools where plain tool calls are more appropriate.
