---
type: note
status: active
slug: triage-note-sc-troubleshoot
summary: "Triage note for SuperClaude commands/troubleshoot.md. Decision port (D.0): no MCP, 4.3 KB body. Distinct from superpowers-systematic-debugging — sc-troubleshoot is user-facing entry point, superpowers-systematic-debugging is the underlying 4-phase methodology."
created: 2026-05-12
updated: 2026-05-12
---

# Triage note — `superclaude_framework/src/superclaude/commands/troubleshoot.md`

## Why `port` (not duplicate of `superpowers-systematic-debugging`)

Both `sc-troubleshoot` (row 26 in the matrix) and `superpowers-systematic-debugging` (row 57) address the broad "diagnose a problem" domain, but they operate at different abstraction layers:

| Aspect | `sc-troubleshoot` (4.3 KB) | `superpowers-systematic-debugging` (9.9 KB) |
|---|---|---|
| Audience | User invocation (`/sc:troubleshoot <symptom>`) | Discipline gate the agent loads internally before any debug session |
| Scope | Build / deploy / system behaviour / code | Bug investigation specifically |
| Methodology | Lightweight: triage → diagnose → fix | 4-phase: gather evidence → hypothesise → test → fix |
| Body length | Fits D.6 | Requires phase split per `references/` |

ST-2 ports `sc-troubleshoot` verbatim; ST-3 ports `superpowers-systematic-debugging` with phase extraction. Each SKILL.md MUST cite the other via `skill_references_skills` so agents can escalate from the lightweight to the systematic flow.

## Port recipe (ST-2)

1. Copy `commands/troubleshoot.md` body to `skills/sc-troubleshoot/SKILL.md`.
2. Frontmatter as in the pure-ports cluster note; `skill_references_skills: [superpowers-systematic-debugging, sc-root-cause-analyst]`.
3. Add a `## Escalation` section pointing at `superpowers-systematic-debugging` when triage cannot identify the failure mode in one pass.
4. Body cap: ≤ 4 KB after frontmatter.

## Landing folder

`skills/sc-troubleshoot/SKILL.md` + `readme.md`. Tier L2.

## Audit-graph linkage

- `skill_source: "superclaude_framework@v4.3.0"`
- `skill_references_skills: [superpowers-systematic-debugging, sc-root-cause-analyst]`

## Phase 1 cross-check

`troubleshoot` was **not** in the Phase 1 keep-list — Agency `skills/sc-*/` does not yet contain `sc-troubleshoot`. ST-2 MUST land this as a net-new skill folder, not edit an existing one.
