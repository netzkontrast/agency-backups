---
type: index
status: active
slug: sc-troubleshoot
summary: "Directory index for the imported `/sc:troubleshoot` skill (SuperClaude_Framework v4.3.0). Verbatim upstream archived in `references/`; Agency-facing body in `SKILL.md`."
created: 2026-05-12
updated: 2026-05-12
---

# `skills/sc-troubleshoot/`

**What:** Diagnose and resolve issues in code, builds, deployments, and system behavior. Diagnose-first; fixes require explicit `--fix`.

**Why here:** Imported under [Task 092](../../tasks/092-port-skill-corpora-phase-2/task.md) ST-2 per the policy ratified in [ADR-0011](../../decisions/0011-external-skill-corpora-import.md). Vendor-prefixed (`sc-`) folder path per D.1; `skill_source: "superclaude@v4.3.0"` pin per D.2; SHA-pinned upstream citation per D.3 (mirror at `references/upstream-sc-troubleshoot.md`, snapshot SHA `22ad3f48`).

## Contents

- [`SKILL.md`](./SKILL.md) — Agency-facing skill body (Anthropic `name`+`description` frontmatter + Agency L2 keys).
- [`references/upstream-sc-troubleshoot.md`](./references/upstream-sc-troubleshoot.md) — Verbatim mirror of `src/superclaude/commands/troubleshoot.md` from upstream at SHA `22ad3f48`. **Do not edit** — re-syncs require a new Task per ADR-0011 D.9.

## Assumptions Log

- (none)
