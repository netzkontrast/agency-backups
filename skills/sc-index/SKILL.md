---
name: sc-index
description: "Generate comprehensive project documentation and knowledge base with intelligent organization"
skill_kind: tool
skill_target_agents: [claude-code]
skill_references_skills: [sc-document]
skill_references_research: []
skill_references_prompts: []
skill_bootstrap_required: false
skill_source: "superclaude@v4.3.0"
---

# sc-index — `/sc:index` (imported from SuperClaude v4.3.0)

## What

Imported `/sc:index` command from SuperClaude_Framework. Generates project documentation and knowledge-base indexes — structure docs, API surface maps, READMEs — with intelligent organization and cross-referencing. Body adapted per ADR-0011 D.8: **`Read` + `Grep` + `Glob` + Markdown synthesis are the primary surface** (see `## Compatibility` for upstream MCP notes).

## When to use

Use when the user invokes `/sc:index`, asks for a project map, requests an API or structure overview, or needs an organized README/knowledge-base entry. Hand off to `sc-document` for deep documentation of a specific component or feature.

## When NOT to use

Do NOT overwrite existing manual documentation without the user's explicit permission — the upstream `Will Not` clause is preserved. Do NOT use to author full per-component documentation; route that to `sc-document`.

## How to use

1. **Survey**: use `Glob` to enumerate the project tree (`**/*.py`, `**/*.ts`, `**/README*`, `**/*.md`, etc.) and `Read` top-level manifests (`package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`) to fix the project shape.
2. **Identify**: `Grep` for documentation anchors — module docstrings, exported symbols, route definitions, public API surfaces, top-level headings in existing `README*`/`docs/` content.
3. **Organize**: classify findings by the user's requested `--type` — `structure` (folder layout + responsibilities), `api` (entry points and signatures), `docs` (knowledge-base aggregation), or `readme` (top-level overview).
4. **Synthesise**: write the index in Markdown with intelligent cross-references — every entry links back to the source file with a relative path; group by domain; surface gaps where source code lacks docstrings.
5. **Validate**: re-read the generated index against the file tree; flag any path that no longer resolves. Preserve any pre-existing manual sections the user marked sticky.

## Adaptations from upstream

- **Dropped MCP bindings**: `sequential` and `context7` (D.8). The "Sequential MCP for systematic multi-step analysis" loop collapses to native reasoning over `Glob`/`Read`/`Grep` output; "Context7 MCP for framework-specific documentation patterns" becomes inline knowledge plus references to project-pinned style guides.
- Multi-persona coordination (architect / scribe / quality) survives as inline lenses applied during step 3 organization.
- All Triggers, Boundaries, and Will/Will-Not clauses are preserved.

## References

- Upstream: [`src/superclaude/commands/index.md@22ad3f4`](https://github.com/SuperClaude-Org/SuperClaude_Framework/blob/22ad3f483a6fe6c626834e1c9a3573126644a058/src/superclaude/commands/index.md) — verbatim mirror at [`references/upstream-sc-index.md`](./references/upstream-sc-index.md) (ADR-0011 D.3).
- Import policy: [`decisions/0011-external-skill-corpora-import.md`](../../decisions/0011-external-skill-corpora-import.md) §D.8.
- Companion skill: [`skills/sc-document`](../sc-document/SKILL.md).

## Compatibility

- Target agent: `claude-code` (this repo's primary surface).
- MCP servers used: **none required**.
- **Sequential MCP** is OPTIONAL — when present, MAY substitute for the native chain-of-thought used in `How to use` steps 2–4 (multi-step survey, classification, and synthesis); when absent, native reasoning is sufficient (ADR-0011 D.8).
- **Context7 MCP** is OPTIONAL — when present, MAY substitute for the framework-pattern / doc-style lookup that otherwise relies on inline knowledge plus project pins; when absent, the inline approach is sufficient (ADR-0011 D.8).
- Known limitation: imported one-shot snapshot at SuperClaude_Framework `v4.3.0` — re-syncs require a new Task per ADR-0011 D.9.
