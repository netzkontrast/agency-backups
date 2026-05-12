---
type: prompt
status: active
slug: skills-navigation-bootstrap
summary: "Research internal skill navigation, skills skill bootstrap mechanics, tool indexing for md files, and propose a skill.md root spec."
created: 2026-05-04
updated: 2026-05-04
prompt_kind: research-proposal
prompt_framework: RISEN+ReAct
prompt_target_agent: "any"
prompt_relates_to_task: skills-navigation-bootstrap
prompt_spawned_from_research: ""
---

# Skills Navigation and Bootstrap Research

## Framework: RISEN+ReAct

This prompt uses the RISEN (Role, Instructions, Steps, End Goal, Narrowing) and ReAct (Reasoning and Acting) frameworks.

## Role
You are an expert AI systems architect and prompt engineer specializing in multi-agent environments, token-efficient tool design, and repository governance protocols.

## Instructions

You MUST research the current state of the `/skills/` directory, evaluate the mechanics for a "skills skill bootstrap" process, and design an internal skill navigation tool suite. You MUST synthesise these findings into a root `skill.md` specification and propose schemas for structured extraction.

## Steps

1. **Analyze Current State (ReAct)**
   - **Thought:** I need to understand how skills are currently structured and how agents are governed.
   - **Action:** Read `AGENTS.md`, `TASK.md`, and scan the contents of the `/skills/` directory and its `readme.md`.
   - **Observation:** Note the current sync mechanism (`skills-skill-bootstrap`), the `SKILL.md` format, and how agents (Claude, Jules, Gemini) are expected to interact with them.

2. **Research Skill Inter-Referencing**
   - Identify how skills can token-efficiently reference each other.
   - Determine the necessary tools required within the `/skills/` directory to support this navigation for various agents (Google Jules, Claude Code, Gemini).

3. **Design the Bootstrap Process**
   - Define the "skills skill bootstrap" mechanism. How does an agent check out the latest version of all skills into their current workspace?
   - Formulate token-efficient usage instructions for these downloaded tools.

4. **Investigate Markdown Indexing Tools**
   - Research existing tools or propose a design for indexing all `.md` files in the repository.
   - The index MUST utilize frontmatter data to facilitate precise navigation by agents.
   - Design schema files defining what specific markdown headers mean, enabling tools to extract exactly what an agent needs.

5. **Draft Root Specification (`skill.md`)**
   - Draft a new normative specification intended for the repository root (`skill.md`).
   - Detail how skills MUST be used, the required tools, and the implications for `AGENTS.md` and other workflows.

6. **Create Output Deliverables**
   - Produce a comprehensive `output/SPEC.md` documenting the findings, the proposed architecture, and the root `skill.md` draft.
   - If the scope is too large, you MAY propose additional follow-up tasks or prompts, prioritizing adherence to the repository's Highway Standards.

## End Goal
A complete research workspace detailing the architecture for internal skill navigation, the skills bootstrap process, markdown indexing schemas, and a draft of the root `skill.md` specification.

## Narrowing / Constraints
- You MUST adhere strictly to RFC 2119 keywords for all normative statements.
- You MUST NOT execute the implementation of the tools or the `skill.md` file in the root; you are only researching and proposing them in this task.
- You MUST ensure the proposed indexing tools are token-efficient.
- If you skip any optional components due to size, you MUST log them as Open Questions Surfaced to be routed to new prompts.
