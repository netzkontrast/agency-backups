---
name: sc-confidence-check
description: >-
  Pre-implementation confidence assessment (target ≥ 0.90 confidence). Use BEFORE starting any implementation to verify readiness via duplicate check, architecture compliance, official-docs verification, OSS references, and root-cause identification.
skill_kind: tool
skill_target_agents: [claude-code]
skill_references_skills: [sc-self-review]
skill_references_research: []
skill_references_prompts: []
skill_bootstrap_required: false
skill_source: "superclaude@v4.3.0"
---

# sc-confidence-check — Confidence Check skill (imported from SuperClaude v4.3.0)

## What

Imported `confidence-check` skill. A five-check pre-implementation gate that produces a confidence score in `[0.0, 1.0]`. Aim is to **prevent wrong-direction execution**: spend 100–200 tokens on the check to save 5,000–50,000 tokens on misaimed work. The score is advisory; the gate is conversational, not enforced by a hook.

## When to use

User-invocable only. Run **before** starting any implementation task — typically right after the user states the goal and before the first edit. Pair with [`sc-self-review`](../sc-self-review/SKILL.md) **after** implementation to close the loop.

## How to use

Compute a weighted score across five checks. If `Total ≥ 0.90` proceed; `0.70 ≤ Total < 0.90` surface alternatives and ask clarifying questions; `Total < 0.70` STOP and request more context from the user.

| # | Check | Weight | Pass criterion |
|---|---|---|---|
| 1 | **No duplicate implementations?** | 25% | `Grep` / `Glob` finds no existing functionality that already solves this |
| 2 | **Architecture compliance?** | 25% | Reuses the existing tech stack (CLAUDE.md, PLANNING.md, repo conventions); no new dependency without justification |
| 3 | **Official documentation verified?** | 20% | Authoritative docs reviewed (`WebFetch` / `WebSearch`); API compatibility confirmed |
| 4 | **Working OSS implementations referenced?** | 15% | At least one working public reference (`WebSearch` against GitHub or canonical sources) |
| 5 | **Root cause identified?** | 15% | Error messages / logs / traces analysed; the underlying issue (not just the symptom) is named |

Render the result in the conversation:

```
Confidence Checks:
   [pass] No duplicate implementations found
   [pass] Uses existing tech stack
   [pass] Official documentation verified
   [pass] Working OSS implementation found
   [pass] Root cause identified

Confidence: 1.00 (100%)
High confidence — proceeding to implementation.
```

A TypeScript reference implementation (`confidence.ts`) ships with the upstream skill; the Agency port treats the check as a conversational discipline and does not depend on that runtime.

## Adaptations from upstream

- **YAML stripped** — upstream `name`, `description` keys replaced by Agency L1+L2 frontmatter (the Anthropic-compatible `name` + `description` are kept as required by the Skills API).
- **D.7 SessionStart-strip audit** — scanned the upstream `src/superclaude/skills/confidence-check/SKILL.md` body **and** the three byte-equivalent mirrors (`.claude/skills/confidence-check/`, `plugins/superclaude/skills/confidence-check/`, root `skills/confidence-check/`) for `SessionStart` / `session-start` / `session_start` / `hook` references. **None found.** ADR-0011 D.7 strip therefore did not modify the body; this audit is recorded for traceability.
- **D.8** — upstream cites **Context7 MCP** (official docs, check 3) and **Tavily MCP** (OSS references, check 4); both are noted as OPTIONAL under `## Compatibility`. The Agency body lists `WebFetch` + `WebSearch` as the native equivalents.
- **MCP mention in Check 1** — upstream uses `Grep` / `Glob` which are native Agency tools; no strip needed.
- **Phrasing** — emoji-laden check icons in the upstream output are kept conceptually but rendered as plain `[pass]` markers per repo style.

## References

- Upstream: [`src/superclaude/skills/confidence-check/SKILL.md@22ad3f4`](https://github.com/SuperClaude-Org/SuperClaude_Framework/blob/22ad3f483a6fe6c626834e1c9a3573126644a058/src/superclaude/skills/confidence-check/SKILL.md) — verbatim mirror at [`references/upstream-sc-confidence-check.md`](./references/upstream-sc-confidence-check.md) (ADR-0011 D.3).
- Agency anchor: CLAUDE.md §13 — `/sc:*` invocation policy.
- Import policy: [`decisions/0011-external-skill-corpora-import.md`](../../decisions/0011-external-skill-corpora-import.md) (D.6, D.7, D.8).

## Compatibility

- Target agent: `claude-code`.
- **Context7 MCP** is OPTIONAL — when present, MAY substitute for `WebFetch` in Check 3 (official-docs verification); absent, native `WebFetch` is sufficient (ADR-0011 D.8).
- **Tavily MCP** is OPTIONAL — when present, MAY substitute for `WebSearch` in Check 4 (OSS references); absent, native `WebSearch` is sufficient (ADR-0011 D.8).
- Known limitation: imported one-shot snapshot at SuperClaude_Framework `v4.3.0` — re-syncs require a new Task per ADR-0011 D.9.
