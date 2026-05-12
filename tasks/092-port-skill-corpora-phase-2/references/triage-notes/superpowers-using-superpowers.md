---
type: note
status: active
slug: triage-note-using-superpowers
summary: "Triage note for superpowers/skills/using-superpowers/SKILL.md. Decision adapt: meta-skill instructs agent to load Superpowers framework before any other skill; conflicts with Agency's Skill-tool-only invocation model."
created: 2026-05-12
updated: 2026-05-12
---

# Triage note — `superpowers/skills/using-superpowers/SKILL.md`

## What it is

A **meta-skill** that instructs the agent to read other Superpowers skills *before* taking any action. The upstream framework relies on this meta-skill to be injected at SessionStart (via `hooks/session-start.sh` → row 72 in the matrix, decision `skip` per ADR-0011 D.7).

## Why `adapt` (not `port`, not `skip`)

- **Cannot `port` verbatim:** the body's "you must first read X" instruction depends on the SessionStart hook stripping (D.7). Without the hook, the instruction reads as orphan prose.
- **Cannot `skip`:** the meta-skill carries real value — it documents skill-invocation discipline (when to fire which skill, avoiding mid-task rationalisation) that maps directly onto Agency's `Skill` tool semantics.
- **Therefore `adapt`:** ST-3 MUST rewrite the body to:
  1. Replace "read SUPERPOWERS.md first" with "the Agency Skill tool surfaces Superpowers skills via `/sc:superpowers-*`."
  2. Preserve the discipline rules (when-to-fire, ordering, rationalisation traps).
  3. Drop the "framework auto-load" framing entirely.

## Landing folder

`skills/superpowers-using-superpowers/SKILL.md` with the rewritten body. Tier L4 (meta-orchestrator).

## Body cap

Upstream body ≈ 2.3 KB → adaptation fits under 5 KB cap (D.6). No `references/` extraction expected unless ST-3 wants to preserve the upstream "discipline checklist" verbatim as a reference.

## Audit-graph linkage

- `skill_source: "superpowers@v4.0.3"`
- `skill_references_skills: [superpowers-tdd, superpowers-systematic-debugging, superpowers-verification-before-completion]` — the meta-skill points at the discipline gates it enforces.
