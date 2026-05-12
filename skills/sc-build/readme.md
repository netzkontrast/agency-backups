---
type: index
status: active
slug: sc-build
summary: "Directory index for the imported `/sc:build` skill (SuperClaude_Framework v4.3.0, light-MCP-adapt cluster). Playwright binding dropped per ADR-0011 D.8 and reattached OPTIONAL in `SKILL.md` Compatibility."
created: 2026-05-12
updated: 2026-05-12
---

# `skills/sc-build/`

**What:** Build, compile, and package projects with intelligent error handling and optimization. Drives the project's native build system via `Bash` and surfaces diagnostic-aware error reports.

**Why here:** Imported under [Task 092](../../tasks/092-port-skill-corpora-phase-2/task.md) ST-2 (light-MCP-adapt cluster) per the policy ratified in [ADR-0011](../../decisions/0011-external-skill-corpora-import.md). Vendor-prefixed (`sc-`) folder path per D.1; `skill_source: "superclaude@v4.3.0"` pin per D.2; SHA-pinned upstream citation per D.3 (mirror at `references/upstream-sc-build.md`, snapshot SHA `22ad3f48`). Playwright MCP binding stripped from the `How to use` flow and reattached as OPTIONAL in `## Compatibility` per D.8.

## Contents

- [`SKILL.md`](./SKILL.md) — Agency-facing skill body with MCP-free `How to use` and OPTIONAL Playwright note in `## Compatibility`.
- [`references/upstream-sc-build.md`](./references/upstream-sc-build.md) — Verbatim mirror of `src/superclaude/commands/build.md` from upstream at SHA `22ad3f48`. **Do not edit** — re-syncs require a new Task per ADR-0011 D.9.

## Assumptions Log

- (none)
