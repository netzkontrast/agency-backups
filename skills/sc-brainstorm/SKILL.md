---
name: sc-brainstorm
description: >-
  Interactive requirements discovery through Socratic dialogue and systematic exploration. Use when the user invokes /sc:brainstorm or asks to transform an ambiguous idea into a concrete requirements specification.
skill_kind: orchestrator
skill_target_agents: [claude-code]
skill_references_skills: [sc-requirements-analyst, sc-design]
skill_references_research: []
skill_references_prompts: []
skill_bootstrap_required: false
skill_source: "superclaude@v4.3.0"
---

# sc-brainstorm — `/sc:brainstorm` (imported from SuperClaude v4.3.0)

## What

Imported `/sc:brainstorm` command from SuperClaude_Framework. Drives Socratic requirements-discovery dialogue over an ambiguous idea: explore → analyze → validate → specify → hand off. Adapted per ADR-0011 D.6/D.8: six MCP-server bindings stripped; the five-phase Behavioral Flow preserved verbatim because it is the core value-add.

## When to use

Invoke when the user runs `/sc:brainstorm [topic]`, or asks to explore a vague concept and emerge with structured requirements. Pairs with `sc-workflow` (next step: plan) and `sc-design` (next step: architecture). **Stops at a requirements document** — does not produce architecture diagrams or code.

## How to use

Follow the upstream five-phase Behavioral Flow, using Agency-native primitives at each step:

1. **Explore**: Socratic questioning to surface user goals, constraints, success criteria. Drive the dialogue in chat; capture salient answers in a working Markdown buffer.
2. **Analyze**: enumerate domains touched (architecture, frontend, backend, security, devops). For each, use `Read` + `Bash(grep|find)` to inspect prior art in the repo; consult `WebFetch` on authorised external docs when feasibility is unclear.
3. **Validate**: stress-test each requirement against feasibility, scope, and non-functional constraints. Flag unresolvable ambiguities as open questions.
4. **Specify**: synthesise into a requirements document with: clarified user goals, functional requirements, non-functional requirements, user stories / acceptance criteria (Gherkin per [`maintenance/language-spec.md`](../../maintenance/language-spec.md)), and an **open-questions** section.
5. **Handoff**: place the requirements document at `prompts/<slug>/brief.md` (per [PROMPT.md](../../PROMPT.md)) or as inline session output. Open questions discovered during the brainstorm MUST be filed as new Prompts under `/prompts/`, never appended to a closed research workspace ([CLAUDE.md §1](../../CLAUDE.md)).

Detailed reference patterns (Socratic-dialogue heuristics, depth selectors) live in [`references/upstream-sc-brainstorm.md`](./references/upstream-sc-brainstorm.md).

## Adaptations from upstream

- Stripped six MCP bindings (sequential, context7, magic, playwright, morphllm, serena).
- Replaced `sequentialthinking` MCP with native chat + Markdown reasoning chains.
- Replaced `context7` with `WebFetch` on authorised official-docs URLs and `Read` on local docs.
- Replaced `serena` cross-session memory with frontmatter-driven state on the host `prompts/<slug>/` artefacts.
- Dropped `morphllm`, `magic`, `playwright` entirely — not relevant to requirements discovery.
- Preserved the upstream **STOP AFTER REQUIREMENTS DISCOVERY** boundary verbatim in intent: no architecture, no code, no DB schemas.
- `MODE_Brainstorming` is NOT bundled (skipped per the row-40 triage note — its content duplicates the command body almost verbatim).

## References

- Upstream: [`src/superclaude/commands/brainstorm.md@22ad3f4`](https://github.com/SuperClaude-Org/SuperClaude_Framework/blob/22ad3f483a6fe6c626834e1c9a3573126644a058/src/superclaude/commands/brainstorm.md) — verbatim mirror at [`references/upstream-sc-brainstorm.md`](./references/upstream-sc-brainstorm.md) (ADR-0011 D.3).
- Agency anchors: [PROMPT.md](../../PROMPT.md), [`maintenance/language-spec.md`](../../maintenance/language-spec.md) (Gherkin + RFC 2119), [CLAUDE.md §1](../../CLAUDE.md).
- Sibling skills: [`skills/sc-workflow/SKILL.md`](../sc-workflow/SKILL.md) (next-step plan), `sc-design` (next-step architecture).
- Import policy: [`decisions/0011-external-skill-corpora-import.md`](../../decisions/0011-external-skill-corpora-import.md).

## Compatibility

- Target agent: `claude-code`.
- MCP servers used: **none required**. Each upstream MCP is OPTIONAL:
  - **Sequential** — OPTIONAL; fallback: native chat + Markdown reasoning.
  - **Context7** — OPTIONAL; fallback: `WebFetch` + `Read` on local docs.
  - **Magic** — OPTIONAL; UI-feasibility checks defer to `sc-frontend-architect`.
  - **Playwright** — OPTIONAL; UX-validation defers to `sc-quality-engineer`.
  - **Morphllm** — OPTIONAL; not used in this skill.
  - **Serena** — OPTIONAL; persistence is `prompts/<slug>/` frontmatter.
- Known limitation: imported one-shot snapshot at SuperClaude_Framework `v4.3.0`. Re-syncs require a new Task per ADR-0011 D.9.
