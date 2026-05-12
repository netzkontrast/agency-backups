---
type: index
status: active
slug: sc-confidence-check
summary: "Directory index for the imported confidence-check skill (SuperClaude_Framework v4.3.0). Verbatim upstream archived in `references/`; Agency adaptations live in `SKILL.md`. ADR-0011 D.7 SessionStart audit recorded: no hook references found."
created: 2026-05-12
updated: 2026-05-12
---

# `skills/sc-confidence-check/`

**What:** Pre-implementation confidence assessment. Five weighted checks (duplicate, architecture, docs, OSS, root cause) produce a score; target ≥ 0.90 to proceed. Advisory; not enforced by a hook.

**Why here:** Imported under [Task 092](../../tasks/092-port-skill-corpora-phase-2/task.md) ST-2 (heavy-adapt cluster B — confidence-check is the D.7 audit case) per the policy ratified in [ADR-0011](../../decisions/0011-external-skill-corpora-import.md). Vendor-prefixed (`sc-`) folder per D.1; `skill_source: "superclaude@v4.3.0"` pin per D.2; SHA-pinned upstream citation per D.3 (mirror at `references/upstream-sc-confidence-check.md`, snapshot SHA `22ad3f48`); SessionStart-injection audit per D.7 (none found in upstream body or in the three byte-equivalent mirror copies); body-MCP audit per D.8 (Context7 + Tavily noted as OPTIONAL).

## Contents

- [`SKILL.md`](./SKILL.md) — Agency-facing skill body (Anthropic `name`+`description` frontmatter + Agency L2 keys).
- [`references/upstream-sc-confidence-check.md`](./references/upstream-sc-confidence-check.md) — Verbatim mirror of `src/superclaude/skills/confidence-check/SKILL.md` from upstream at SHA `22ad3f48`. **Do not edit** — re-syncs require a new Task per ADR-0011 D.9.

## Assumptions Log

- ADR-0011 D.7 audit (recorded for traceability): `grep -ni -E 'sessionstart|session-start|session_start|hook'` against the four upstream copies (`src/superclaude/skills/confidence-check/`, `.claude/skills/confidence-check/`, `plugins/superclaude/skills/confidence-check/`, root-level `skills/confidence-check/`) returned **no matches**. The Agency body therefore did not strip any clause; the audit is documented in `SKILL.md` `## Adaptations from upstream`.
- Context7 + Tavily MCPs in the upstream Check 3 / Check 4 prose are noted as OPTIONAL under `## Compatibility` per ADR-0011 D.8; native `WebFetch` / `WebSearch` are the Agency primary surface.
- The TypeScript reference (`confidence.ts`) shipped alongside the upstream skill is not ported — the Agency port treats the check as a conversational discipline.
