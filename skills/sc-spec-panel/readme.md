---
type: index
status: active
slug: sc-spec-panel
summary: "Directory index for the imported `/sc:spec-panel` skill (SuperClaude_Framework v4.3.0). Verbatim upstream archived in `references/`; per-expert profiles extracted under D.6; Agency adaptations live in `SKILL.md`."
created: 2026-05-12
updated: 2026-05-12
---

# `skills/sc-spec-panel/`

**What:** Multi-expert specification review using renowned spec / software-engineering experts (Wiegers, Adzic, Cockburn, Fowler, Nygard, Newman, Hohpe, Crispin, Gregory, Hightower). Runs in `discussion`, `critique`, or `socratic` mode.

**Why here:** Imported under [Task 092](../../tasks/092-port-skill-corpora-phase-2/task.md) ST-2 (heavy-adapt cluster B) per the policy ratified in [ADR-0011](../../decisions/0011-external-skill-corpora-import.md). Vendor-prefixed (`sc-`) folder per D.1; `skill_source: "superclaude@v4.3.0"` pin per D.2; SHA-pinned upstream citation per D.3 (mirror at `references/upstream-sc-spec-panel.md`, snapshot SHA `22ad3f48`); per-expert profile extraction per D.6 (upstream 18.3 KB body, 3.7× the 5 KB cap); MCP strip per D.8 (Sequential + Context7).

## Contents

- [`SKILL.md`](./SKILL.md) — Agency-facing skill body (Anthropic `name`+`description` frontmatter + Agency L2 keys).
- [`references/upstream-sc-spec-panel.md`](./references/upstream-sc-spec-panel.md) — Verbatim mirror of `src/superclaude/commands/spec-panel.md` from upstream at SHA `22ad3f48`. **Do not edit** — re-syncs require a new Task per ADR-0011 D.9.
- [`references/experts/wiegers.md`](./references/experts/wiegers.md) — Karl Wiegers (requirements).
- [`references/experts/adzic.md`](./references/experts/adzic.md) — Gojko Adzic (BDD / specification by example).
- [`references/experts/cockburn.md`](./references/experts/cockburn.md) — Alistair Cockburn (use cases).
- [`references/experts/fowler.md`](./references/experts/fowler.md) — Martin Fowler (architecture).
- [`references/experts/nygard.md`](./references/experts/nygard.md) — Michael Nygard (reliability).
- [`references/experts/newman.md`](./references/experts/newman.md) — Sam Newman (microservices).
- [`references/experts/hohpe.md`](./references/experts/hohpe.md) — Gregor Hohpe (integration patterns).
- [`references/experts/crispin.md`](./references/experts/crispin.md) — Lisa Crispin (agile testing).
- [`references/experts/gregory.md`](./references/experts/gregory.md) — Janet Gregory (collaborative testing).
- [`references/experts/hightower.md`](./references/experts/hightower.md) — Kelsey Hightower (cloud-native).

## Assumptions Log

- Sequential MCP + Context7 MCP citations in the upstream body are stripped from the Agency `SKILL.md` per ADR-0011 D.8; both are listed as OPTIONAL under `## Compatibility`.
- The verbatim upstream lists 10 experts (one in the "Modern Software Experts" group); the roster table in `SKILL.md` carries all 10. Operationally the panel runs ≤5 active experts per pass to keep signal high — that heuristic mirrors the upstream Focus-Area panel definitions.
