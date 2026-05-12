---
name: sc-reflect
description: >-
  Task reflection and validation using Serena MCP analysis capabilities. Use when the user invokes /sc:reflect or asks to validate task adherence, completion quality, or session learnings.
skill_kind: analysis
skill_target_agents: [claude-code]
skill_references_skills: [sc-pm-agent, sc-self-review]
skill_references_research: []
skill_references_prompts: []
skill_bootstrap_required: false
skill_source: "superclaude@v4.3.0"
---

# sc-reflect — `/sc:reflect` (imported from SuperClaude v4.3.0)

## What

Imported `/sc:reflect` command from SuperClaude_Framework. Validates task adherence, assesses completion quality, and captures session learnings. Body adapted per ADR-0011 D.8: **TodoWrite + frontmatter-driven `task_status` review + `friction-log.md` reading** replace Serena MCP's `think_about_*` reflection tools.

## When to use

Use when the user invokes `/sc:reflect`, asks "did I finish?" / "am I on track?", before declaring a task `done`, or after a high-friction stretch (FL≥2) where pattern detection is valuable.

## How to use

1. **Snapshot the goal**: Read the active `tasks/<NNN>-<slug>/task.md` — extract `task_acceptance_criteria` (Gherkin scenarios), `task_status`, and the initial plan.
2. **Snapshot current state** via TodoWrite: enumerate completed vs. pending todos against the task's acceptance criteria.
3. **Adherence check**: for each Gherkin `Scenario:` in the task, assess whether observed work satisfies the `Then` clause. Flag deviations.
4. **Friction review**: Read `friction-log.md` entries from this session and prior sessions on the same slug; surface recurring patterns per Introspection-mode triggers (see `## Active modes`).
5. **Completion gate**: decide one of {continue / course-correct / mark `done`}. If `done`, ensure the closing-run checklist (CLAUDE.md §10) is achievable; if not, propose the next concrete step.
6. **Document** the reflection outcome inline in the session response — DO NOT mutate task frontmatter during reflect (mutation belongs to `/sc:save`).

The verbatim upstream body (which assumes Serena MCP `think_about_*` APIs) is archived at `references/upstream-sc-reflect.md` per ADR-0011 D.8.

## Active modes

- **Introspection mode** (bundled at [`references/mode-introspection.md`](./references/mode-introspection.md)) — activates silently on every `/sc:reflect` invocation. Adds meta-cognitive transparency (reasoning markers, pattern detection, framework-compliance check). Also activates on user requests like "analyze my reasoning" or after error recovery when outcomes diverge from expectations. Bundled per ADR-0011 D.5 — modes are behavioural overlays, not standalone skills.

## Adaptations from upstream

Upstream `/sc:reflect` mandates Serena MCP for `think_about_task_adherence`, `think_about_collected_information`, and `think_about_whether_you_are_done`. Agency's substitution per ADR-0011 D.8: **Serena-MCP calls are replaced with Agency filesystem patterns** — TodoWrite provides task-state introspection; the task's Gherkin acceptance criteria provide the adherence rubric; `friction-log.md` provides the cross-session pattern surface. No Serena calls appear in the Agency body.

## References

- Upstream: [`src/superclaude/commands/reflect.md@22ad3f4`](https://github.com/SuperClaude-Org/SuperClaude_Framework/blob/22ad3f483a6fe6c626834e1c9a3573126644a058/src/superclaude/commands/reflect.md) — verbatim mirror at [`references/upstream-sc-reflect.md`](./references/upstream-sc-reflect.md) (ADR-0011 D.3).
- Agency anchor: TASK.md §3 — `task_acceptance_criteria` Gherkin contract; FRUSTRATED.md — friction-log format; CLAUDE.md §5 — RFC 2119 + Gherkin spec language.
- Import policy: [`decisions/0011-external-skill-corpora-import.md`](../../decisions/0011-external-skill-corpora-import.md) (D.5 mode-bundling + D.8 adaptation clauses).
- Introspection mode bundle: [`references/mode-introspection.md`](./references/mode-introspection.md).

## Compatibility

- Target agent: `claude-code` (this repo's primary surface).
- MCP servers used: none required. **Serena MCP** is OPTIONAL — when present, MAY substitute for filesystem-based session persistence; absent, Agency's `task/<NNN>/task.md` + `friction-log.md` provide equivalent capability (ADR-0011 D.8).
- Known limitation: imported one-shot snapshot at SuperClaude_Framework `v4.3.0` — re-syncs require a new Task per ADR-0011 D.9.
