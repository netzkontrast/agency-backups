---
type: note
status: active
slug: superclaude-integration-spec
summary: "Methods applied during the SC-Agency integration spec research run."
created: 2026-05-04
updated: 2026-05-04
---

# Methodology

## M01 — Catalog-First Approach

Full inventory of all installed SuperClaude components before mapping. Sources: `ls ~/.claude/commands/sc/`, `ls ~/.claude/agents/`, `ls ~/.claude/skills/`, read of individual command `.md` files, SuperClaude CLAUDE.md, KNOWLEDGE.md. This prevents gaps from assumptions.

## M06 — Phase-Workflow Mapping

Each catalog item was evaluated against each Agency workflow phase (TASK.md §4, RESEARCH.md §4, PROMPT.md §4, MAINTENANCE.md §1–4). Mapping criteria: does the tool's behavioral flow directly serve the phase's stated goals?

## M13 — Pattern Extraction (Four Axes)

For each integration pattern, four axes were evaluated:
1. **Structural**: What file/folder does the tool operate on?
2. **Temporal**: When in the phase lifecycle does the tool add most value?
3. **Cognitive**: What mental load does the tool offload from the agent?
4. **Abstraction**: Is the tool a direct action or a meta-orchestration layer?

## M15 — Gap Analysis via KNOWLEDGE.md

Cross-referenced SuperClaude KNOWLEDGE.md §"Claude Code Integration Gap Analysis" (March 2026). Four highest-impact gaps identified: Skills System, Hooks System, Plan Mode Integration, Settings Profiles. Integration patterns focus on the currently usable gaps (Skills, Commands, Agents).

## M20 — Template Derivation

The SuperClaude Integration Block template (SPEC.md §4) was derived from TASK.md §3.2 (namespaced, flat, machine-readable metadata). Same structural principle: predictable keys, one normative statement per rule, back-link to source spec.
