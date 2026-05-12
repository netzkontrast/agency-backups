---
type: task
status: archived
slug: surface-skills-architecture
summary: "Found by coherence check 2026-05-04: Surface skills-skill-architecture research findings to governance."
created: 2026-05-04
updated: 2026-05-12
task_id: "006"
task_status: archived
task_owner: "claude-code"
task_priority: P2
task_uses_prompts:
  - skills-skill-architecture
task_spawns_research: []
task_spawns_prompts: []
task_affects_paths:
  - AGENTS.md
  - SKILLS.md
  - MAINTENANCE.md
  - TASK.md
---

# Task 006 — Surface Skills Architecture to Governance

## Goal
The `skills-skill-architecture` research run was marked complete, but its findings have not been integrated into the root governance documents (`AGENTS.md`, `TASK.md`, `MAINTENANCE.md`). Ensure the architecture and triggers discovered in that research run are canonically logged.

## Plan
1. Review `/research/skills-skill-architecture/output/SPEC.md`.
2. Determine which rules need to be surfaced to root specs.
3. Update `AGENTS.md` and/or `MAINTENANCE.md` with those findings.

## Todo
- [x] Review `skills-skill-architecture` findings (§§2–8 covering R1–R7).
- [x] Incorporate into root specs:
  - Three new `SKILLS.md` subsections — [§7.2 Trust-Boundary Invariants (R5)](../../SKILLS.md#72-trust-boundary-invariants-r5) (B.6–B.9), [§7.3 Three-Tier Content Ladder (R4)](../../SKILLS.md#73-three-tier-content-ladder-r4) (T1/T2/T3 size targets), [§7.4 Version-Pinning and Offline Mode (R7)](../../SKILLS.md#74-version-pinning-and-offline-mode-r7) (`SKILLS_SKILL_PIN`, `SKILLS_SKILL_OFFLINE`).
  - `AGENTS.md` "Skills Architecture" section gains a one-paragraph pointer to the new SKILLS.md subsections plus the residual `UNCERTAIN` markers list (U3–U6).
  - `MAINTENANCE.md` / `TASK.md` left untouched — the surfaced findings are skill-loader operational invariants, which belong under SKILLS.md (the layer-specific spec), not under root-task or root-maintenance prose. Cross-references from AGENTS.md fold them into the agent-entry-point reading path.

## Notes on scope

- The original `task_affects_paths` listed AGENTS.md, MAINTENANCE.md, TASK.md but not SKILLS.md. SKILLS.md was added to the list at close because it is the natural home for skill-loader invariants (per the layer routing in `CLAUDE.md §3`).
- Residual `UNCERTAIN` markers from the source SPEC (`U3` host activation, `U4` Jules portability, `U5` raw-message availability, `U6` git signing) remain deferred to Gemini Deep Research per the workspace's §9 open-questions table. They are NOT surfaced as normative root-spec content because they are not yet resolved.
- `U1` and `U2` were resolved by [`research/skills-skill-container-capabilities/output/SPEC.md`](../../research/skills-skill-container-capabilities/output/SPEC.md) and were already surfaced in [`AGENTS.md "Skills Architecture — Container Capabilities and Citation Protocol"`](../../AGENTS.md#skills-architecture--container-capabilities-and-citation-protocol). This Task does not re-surface them.

## Links
- Source spec: [`../../research/skills-skill-architecture/output/SPEC.md`](../../research/skills-skill-architecture/output/SPEC.md)
- Surfaced to: [`../../SKILLS.md §7.2 / §7.3 / §7.4`](../../SKILLS.md#72-trust-boundary-invariants-r5), [`../../AGENTS.md "Skills Architecture"`](../../AGENTS.md#skills-architecture--container-capabilities-and-citation-protocol)
- Friction log: [`./friction-log.md`](./friction-log.md)
- Found by: coherence check run `maintenance/run-log.md` entry 2026-05-04
