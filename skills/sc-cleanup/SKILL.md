---
name: sc-cleanup
description: "Systematically clean up code, remove dead code, and optimize project structure"
skill_kind: tool
skill_target_agents: [claude-code]
skill_references_skills: [sc-refactoring-expert]
skill_references_research: []
skill_references_prompts: []
skill_bootstrap_required: false
skill_source: "superclaude@v4.3.0"
---

# sc-cleanup — `/sc:cleanup` (imported from SuperClaude v4.3.0)

## What

Imported `/sc:cleanup` command from SuperClaude_Framework. Coordinates systematic dead-code removal, import optimization, and project-structure tidying, with a safety-first auto-fix vs approval-required split. Body adapted per ADR-0011 D.8: **`Read` + `Grep` + `Edit` + `Bash(rm)` are the primary surface** (see `## Compatibility` for upstream MCP notes).

## When to use

Use when the user invokes `/sc:cleanup`, asks to remove dead code, prune unused imports, or tidy project structure. Hand off to `sc-refactoring-expert` for non-trivial structural rewrites that go beyond mechanical removal.

## When NOT to use

Do NOT run on a `research_phase: complete` workspace — research bodies are T4-immutable (CLAUDE.md §8). Do NOT use `git add .` style sweeps; stage by name.

## How to use

1. **Analyze**: `Read` the cleanup target (file, folder, or repo subtree). `Grep` for usage patterns and dead-code signals (unreachable branches, zero-reference identifiers, commented-out blocks, unused imports).
2. **Plan**: classify each candidate by the upstream "Auto-fix vs Approval-Required" matrix — unused imports / zero-ref dead code / empty blocks / redundant type annotations are auto-fix; indirect references, public exports, test fixtures, and config values require user approval.
3. **Apply**: use `Edit` for code modifications and `Bash` (`rm`, `git rm`) only for whole-file removal. Stage by name; never `git add .`.
4. **Validate**: re-run the project's tests/lints via `Bash` to confirm no functionality regression. If a regression appears, revert that specific edit and downgrade the candidate to approval-required.
5. **Report**: produce a cleanup summary — files touched, lines removed, imports pruned, items deferred to approval — plus recommendations for ongoing maintenance.

## Adaptations from upstream

- **Dropped MCP bindings**: `sequential` and `context7` (D.8). The "systematic multi-step cleanup analysis" loop collapses to native Claude reasoning over `Read`/`Grep` output; "framework-specific cleanup patterns" become inline knowledge plus optional `WebFetch` for framework docs if the user requests deep authority.
- The upstream Sequential/Context7 "Persona Coordination" (architect / quality / security) is preserved as inline guidance: structural tidying = architect lens; debt reduction = quality lens; credential / secret scrub = security lens.
- The `AUTO-FIX VS APPROVAL-REQUIRED` decision matrix is preserved verbatim in spirit.

## References

- Upstream: [`src/superclaude/commands/cleanup.md@22ad3f4`](https://github.com/SuperClaude-Org/SuperClaude_Framework/blob/22ad3f483a6fe6c626834e1c9a3573126644a058/src/superclaude/commands/cleanup.md) — verbatim mirror at [`references/upstream-sc-cleanup.md`](./references/upstream-sc-cleanup.md) (ADR-0011 D.3).
- Import policy: [`decisions/0011-external-skill-corpora-import.md`](../../decisions/0011-external-skill-corpora-import.md) §D.8.
- Companion skill: [`skills/sc-refactoring-expert`](../sc-refactoring-expert/SKILL.md).

## Compatibility

- Target agent: `claude-code` (this repo's primary surface).
- MCP servers used: **none required**.
- **Sequential MCP** is OPTIONAL — when present, MAY substitute for the native chain-of-thought used in `How to use` steps 1–2 (multi-step cleanup analysis); when absent, native reasoning is sufficient (ADR-0011 D.8).
- **Context7 MCP** is OPTIONAL — when present, MAY substitute for the framework-pattern lookup that otherwise relies on inline knowledge or `WebFetch`; when absent, the inline guidance is sufficient (ADR-0011 D.8).
- Known limitation: imported one-shot snapshot at SuperClaude_Framework `v4.3.0` — re-syncs require a new Task per ADR-0011 D.9.
