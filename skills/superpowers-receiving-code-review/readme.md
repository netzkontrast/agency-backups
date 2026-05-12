---
type: index
status: active
slug: superpowers-receiving-code-review
summary: "Directory index for the imported receiving-code-review skill (Superpowers v4.0.3). Verbatim upstream archived in `references/`; Agency adaptations live in `SKILL.md`."
created: 2026-05-12
updated: 2026-05-12
---

# `skills/superpowers-receiving-code-review/`

**What:** Technical verification before implementing review feedback; not performative.

**Why here:** Imported under [Task 092](../../tasks/092-port-skill-corpora-phase-2/task.md) ST-3 per the policy ratified in [ADR-0011](../../decisions/0011-external-skill-corpora-import.md). Vendor-prefixed (`superpowers-`) folder path per D.1; `skill_source: "superpowers@v4.0.3"` pin per D.2; SHA-pinned upstream citation per D.3 (mirror at `references/upstream-superpowers-receiving-code-review.md`, snapshot SHA `b9e16498`).

## Contents

- [`SKILL.md`](./SKILL.md) — Agency-facing skill body (Anthropic `name`+`description` frontmatter + Agency L2 keys).
- [`references/upstream-superpowers-receiving-code-review.md`](./references/upstream-superpowers-receiving-code-review.md) — Verbatim mirror of `skills/receiving-code-review/SKILL.md` from upstream at SHA `b9e16498`. **Do not edit** — re-syncs require a new Task per ADR-0011 D.9.

## Assumptions Log

- This skill was triaged as a **port** (no `adapt`) in Task 092 ST-1 ([triage matrix](../../tasks/092-port-skill-corpora-phase-2/references/triage-matrix.md)): no MCP bindings; no SessionStart-injection clauses to strip. Upstream body may exceed 5 KB (lives only in `references/`); the Agency SKILL.md body is independent and ≤ 5 KB per ADR-0011 D.6.
- Upstream YAML frontmatter is replaced with Agency L2 frontmatter; the verbatim body is preserved in `references/` for audit.
