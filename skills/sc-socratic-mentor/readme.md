---
type: index
status: active
slug: sc-socratic-mentor
summary: "Directory index for the imported Socratic Mentor agent (SuperClaude_Framework v4.3.0). Verbatim upstream archived in `references/`; teaching corpus extracted under D.6; Agency adaptations live in `SKILL.md`."
created: 2026-05-12
updated: 2026-05-12
---

# `skills/sc-socratic-mentor/`

**What:** Educational guide using the Socratic method for programming-knowledge discovery (Clean Code, GoF patterns). Discovery-driven counterpart to the progression-driven [`sc-learning-guide`](../sc-learning-guide/).

**Why here:** Imported under [Task 092](../../tasks/092-port-skill-corpora-phase-2/task.md) ST-2 (heavy-adapt cluster B) per the policy ratified in [ADR-0011](../../decisions/0011-external-skill-corpora-import.md). Vendor-prefixed (`sc-`) folder per D.1; `skill_source: "superclaude@v4.3.0"` pin per D.2; SHA-pinned upstream citation per D.3 (mirror at `references/upstream-sc-socratic-mentor.md`, snapshot SHA `22ad3f48`); teaching-corpus extraction per D.6 (upstream 12.0 KB body, 2.4× the 5 KB cap); MCP strip per D.8 (Sequential).

## Contents

- [`SKILL.md`](./SKILL.md) — Agency-facing skill body (Anthropic `name`+`description` frontmatter + Agency L2 keys).
- [`references/upstream-sc-socratic-mentor.md`](./references/upstream-sc-socratic-mentor.md) — Verbatim mirror of `src/superclaude/agents/socratic-mentor.md` from upstream at SHA `22ad3f48`. **Do not edit** — re-syncs require a new Task per ADR-0011 D.9.
- [`references/teaching-corpus.md`](./references/teaching-corpus.md) — Book corpus (Clean Code, GoF), level-adaptive question banks, session-orchestration templates, and persona-collaboration mapping (D.6 extraction).

## Assumptions Log

- Sequential MCP citation in the upstream body is stripped from the Agency `SKILL.md` per ADR-0011 D.8; listed as OPTIONAL under `## Compatibility`.
- Persona handoffs in the upstream body (analyzer / architect / mentor / scribe) are remapped to Agency siblings (`sc-analyze`, `sc-system-architect`, `sc-explain`) in `references/teaching-corpus.md`; no new MCP coordination layer is introduced.
- The Socratic mentor is **discovery-driven**; `sc-learning-guide` is **progression-driven**. The two are cross-listed but not collapsed.
