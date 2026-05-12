---
name: sc-build
description: "Build, compile, and package projects with intelligent error handling and optimization"
skill_kind: tool
skill_target_agents: [claude-code]
skill_references_skills: [sc-test]
skill_references_research: []
skill_references_prompts: []
skill_bootstrap_required: false
skill_source: "superclaude@v4.3.0"
---

# sc-build — `/sc:build` (imported from SuperClaude v4.3.0)

## What

Imported `/sc:build` command from SuperClaude_Framework. Coordinates project compilation, packaging, and artifact generation with diagnostic-aware error handling. Body adapted per ADR-0011 D.8: **Bash is the primary execution surface** (see `## Compatibility` for upstream Playwright MCP notes).

## When to use

Use when the user invokes `/sc:build`, asks to compile/package a project, prepares deployment artifacts, or needs build-failure diagnosis. Hand off to `sc-test` after a successful build when verification is required.

## How to use

1. **Analyze**: `Read` build manifests (`package.json`, `pyproject.toml`, `Makefile`, `Cargo.toml`, etc.) and `Grep` for relevant build targets and toolchain pins.
2. **Validate**: confirm required toolchain components are present via `Bash` (`which`, `--version`, `ls`). Surface missing dependencies — do NOT install them.
3. **Execute**: invoke the project's native build system via `Bash` (`make build`, `npm run build`, `cargo build --release`, etc.). Stream output; capture exit code.
4. **Optimize**: when the user passes `--type prod` or `--optimize`, append the build system's optimization flags (minification, tree-shaking, release profile). Do not invent new build scripts.
5. **Diagnose**: on non-zero exit, `Grep` the build log for error/warning lines and produce an actionable resolution summary — pointer to file:line, root-cause hypothesis, suggested fix.
6. **Report**: summarise artifacts (paths, sizes via `ls -lh`), timing, and any quality gates. If post-build UI verification is requested, defer to `sc-test`.

## Adaptations from upstream

- **Dropped MCP binding**: `playwright` (D.8). Build validation and any UI-smoke verification step now defer to the `sc-test` skill, which can opt into Playwright if available. The upstream "Development Build with Validation" example collapses to plain `Bash` build + optional `sc-test` follow-up.
- All other behavioural clauses (Triggers, Behavioral Flow, Boundaries, Will/Will-Not) are preserved.

## References

- Upstream: [`src/superclaude/commands/build.md@22ad3f4`](https://github.com/SuperClaude-Org/SuperClaude_Framework/blob/22ad3f483a6fe6c626834e1c9a3573126644a058/src/superclaude/commands/build.md) — verbatim mirror at [`references/upstream-sc-build.md`](./references/upstream-sc-build.md) (ADR-0011 D.3).
- Import policy: [`decisions/0011-external-skill-corpora-import.md`](../../decisions/0011-external-skill-corpora-import.md) §D.8 (MCP-binding adaptation).
- Companion skill: [`skills/sc-test`](../sc-test/SKILL.md).

## Compatibility

- Target agent: `claude-code` (this repo's primary surface).
- MCP servers used: **none required**. **Playwright MCP** is OPTIONAL — when present, it MAY substitute for the build-validation / UI-smoke step in `How to use` step 6; when absent, native `Bash` plus the `sc-test` skill provide sufficient coverage (ADR-0011 D.8).
- Known limitation: imported one-shot snapshot at SuperClaude_Framework `v4.3.0` — re-syncs require a new Task per ADR-0011 D.9.
