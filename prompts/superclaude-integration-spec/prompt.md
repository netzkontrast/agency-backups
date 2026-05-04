---
type: prompt
status: active
slug: superclaude-integration-spec
summary: "Research prompt: produce a governance spec mapping SuperClaude commands, agents, and skills to Agency workflow phases."
created: 2026-05-04
updated: 2026-05-04
prompt_kind: research-proposal
prompt_framework: RISEN+ReAct
prompt_target_agent: "Claude Code"
prompt_relates_to_task: ""
prompt_spawned_from_research: ""
---

# SuperClaude Integration Research Prompt

**Framework: RISEN + ReAct**

## Role

You are a senior agentic-workflow architect with deep knowledge of the Agency governance system (`AGENTS.md`, `TASK.md`, `RESEARCH.md`, `PROMPT.md`, `FOLDERS.md`) and the SuperClaude Framework v4.3.0 (30 commands, 20 agents, 7 behavioral modes, skills).

## Instructions

Produce a comprehensive integration specification (`SPEC.md`) that:

1. **Catalogs** every SuperClaude command (`/sc:*`), agent, and skill installed in `~/.claude/` with a one-line purpose summary.
2. **Maps** each catalog item to one or more Agency workflow phases (Prompt authoring, Research execution, Synthesis, Reflection, Task orchestration, Maintenance).
3. **Defines** concrete integration patterns — executable invocation examples showing how an agent running a future research or task session MUST invoke the corresponding SuperClaude tool.
4. **Specifies** how future Agency specs (TASK.md, RESEARCH.md, PROMPT.md, MAINTENANCE.md additions, new research prompts) MUST include a SuperClaude Integration Block.
5. **Identifies** which existing root specs benefit from cross-links to this spec and states exactly what link to add.
6. **Extends** MAINTENANCE.md with a new §5 (SuperClaude Integration Scan) that governs recurring checks for new integration opportunities.

## Situation

The SuperClaude Framework v4.3.0 is installed at `~/.claude/` and provides:
- 30 slash commands in `~/.claude/commands/sc/`
- 20 domain-specialist agents in `~/.claude/agents/`
- Skills in `~/.claude/skills/` plus system-provided skills (confidence-check)
- 7 behavioral modes
- MCP server integrations (Tavily, Context7, Sequential, Serena, Playwright, Mindbase)

The Agency repo has a strict governance model (TASK.md §3 frontmatter ontology, RESEARCH.md workflow, FOLDERS.md topology) and has not yet formally integrated with SuperClaude capabilities.

## Expected Deliverable

A file `/research/superclaude-integration-spec/output/SPEC.md` containing:

1. `# SuperClaude Integration Specification` (H1 title)
2. Mandatory YAML frontmatter (L1 + research namespace per TASK.md §3)
3. `## 1. Catalog` — Full tables of all SC commands, agents, skills with purpose
4. `## 2. Phase Mapping` — Per-phase integration table (Agency phase → SC tools → invocation pattern)
5. `## 3. Integration Patterns` — Concrete executable examples per phase
6. `## 4. New Spec Template` — The mandatory SuperClaude Integration Block for all future specs
7. `## 5. Root Spec Link Recommendations` — Table of root specs + exact link text to add
8. `## 6. Anti-Patterns` — What NOT to do when integrating SC into Agency workflows

## Exclusions

- MUST NOT duplicate entire SC command files verbatim; summarize only.
- MUST NOT propose changes outside the Agency repo scope.
- MUST NOT recommend SC tools where plain tool calls are more appropriate.

## Normative Language

All normative requirements MUST use RFC 2119 keywords (MUST, SHOULD, MAY). Exactly one normative keyword per sentence.
