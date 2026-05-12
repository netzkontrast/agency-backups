---
type: index
status: active
slug: sc-workflow
summary: "Directory index for the imported `/sc:workflow` skill (SuperClaude_Framework v4.3.0). Verbatim upstream archived in `references/`; Agency adaptations live in `SKILL.md`."
created: 2026-05-12
updated: 2026-05-12
---

# `skills/sc-workflow/`

**What:** Generates structured implementation workflows from PRDs / feature briefs — phases, dependency map, validation checkpoints. Plan-only; execution is delegated to `sc-implement` / `sc-task`.

**Why here:** Imported under [Task 092](../../tasks/092-port-skill-corpora-phase-2/task.md) ST-2 (heavy-adapt cluster A) per the policy ratified in [ADR-0011](../../decisions/0011-external-skill-corpora-import.md). Vendor-prefixed (`sc-`) folder per D.1; `skill_source: "superclaude@v4.3.0"` pin per D.2; SHA-pinned upstream citation per D.3 (mirror at `references/upstream-sc-workflow.md`, snapshot SHA `22ad3f48`). Body adaptation per D.6 — the six upstream MCP bindings were stripped and the plan flow re-anchored to Agency's Prompt → Task layers.

## Contents

- [`SKILL.md`](./SKILL.md) — Agency-facing skill body (Anthropic `name`+`description` frontmatter + Agency L2 keys).
- [`references/upstream-sc-workflow.md`](./references/upstream-sc-workflow.md) — Verbatim mirror of `src/superclaude/commands/workflow.md` from upstream at SHA `22ad3f48`. **Do not edit** — re-syncs require a new Task per ADR-0011 D.9.

## Assumptions Log

- The workflow plan lands in `prompts/<slug>/prompt.md` (when execution-ready) or as a free-standing Markdown synthesis; it MUST NOT land in `research/` (research is for evidence per [RESEARCH.md](../../RESEARCH.md)).
- The skill is **plan-only**. Any code, build, or test execution is out of scope and MUST be deferred to `/sc:implement`.
- Cross-session continuity is satisfied by frontmatter on the host Prompt + Task — no external memory store.
