---
type: index
status: active
slug: superpowers-using-superpowers
summary: "Directory index for the imported using-superpowers skill (Superpowers v4.0.3, adapted per ADR-0011 D.1+D.6+D.7). Verbatim upstream archived in `references/`; Agency adaptations live in `SKILL.md`."
created: 2026-05-12
updated: 2026-05-12
---

# `skills/superpowers-using-superpowers/`

**What:** Meta-skill — discipline-gate selector. Adapted per D.7 (no SessionStart injection).

**Why here:** Imported under [Task 092](../../tasks/092-port-skill-corpora-phase-2/task.md) ST-3 batch B per the policy ratified in [ADR-0011](../../decisions/0011-external-skill-corpora-import.md). Vendor-prefixed (`superpowers-`) folder path per D.1; `skill_source: "superpowers@v4.0.3"` pin per D.2; SHA-pinned upstream citation per D.3 (mirror at `references/upstream-superpowers-using-superpowers.md`, snapshot SHA `b9e16498`).

## Contents

- [`SKILL.md`](./SKILL.md) — Agency-facing skill body (Anthropic `name`+`description` frontmatter + Agency L2 keys).
- [`references/upstream-superpowers-using-superpowers.md`](./references/upstream-superpowers-using-superpowers.md) — Verbatim mirror of `skills/using-superpowers/SKILL.md` from upstream at SHA `b9e16498`. **Do not edit** — re-syncs require a new Task per ADR-0011 D.9.

## Assumptions Log

- This skill was triaged as an **adapt** decision in Task 092 ST-1 ([triage matrix](../../tasks/092-port-skill-corpora-phase-2/references/triage-matrix.md)). The Agency SKILL.md body rewrites upstream patterns to use Agency-native primitives (Skill tool, Agent tool, Task layer) instead of the Superpowers SessionStart-hook + lib/skills-core.js mechanisms.
- Upstream YAML frontmatter is replaced with Agency L2 frontmatter; the verbatim body is preserved in `references/` for audit.
- Skill body ≤ 5 KB per ADR-0011 D.6; upstream content of any size lives in `references/` only.
