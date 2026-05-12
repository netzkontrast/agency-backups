---
type: index
status: active
slug: sc-self-review
summary: "Directory index for the imported `@self-review` persona skill (SuperClaude_Framework v4.3.0). Verbatim upstream archived in `references/`; Agency-facing body in `SKILL.md`."
created: 2026-05-12
updated: 2026-05-12
---

# `skills/sc-self-review/`

**What:** Self Review Agent persona — post-implementation validation and reflexion partner running four mandatory self-check questions.

**Why here:** Imported under [Task 092](../../tasks/092-port-skill-corpora-phase-2/task.md) ST-2 per the policy ratified in [ADR-0011](../../decisions/0011-external-skill-corpora-import.md). Vendor-prefixed (`sc-`) folder path per D.1; `skill_source: "superclaude@v4.3.0"` pin per D.2; SHA-pinned upstream citation per D.3 (mirror at `references/upstream-sc-self-review.md`, snapshot SHA `22ad3f48`).

## Contents

- [`SKILL.md`](./SKILL.md) — Agency-facing skill body (Anthropic `name`+`description` frontmatter + Agency L2 keys).
- [`references/upstream-sc-self-review.md`](./references/upstream-sc-self-review.md) — Verbatim mirror of `src/superclaude/agents/self-review.md` from upstream at SHA `22ad3f48`. **Do not edit** — re-syncs require a new Task per ADR-0011 D.9.

## Assumptions Log

- (none)
