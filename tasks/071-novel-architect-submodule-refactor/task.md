---
type: task
status: active
slug: novel-architect-submodule-refactor
summary: "Refactor monolithic novel-architect@1.0.0 into 4-5 sub-module skills (character-architect, structure-architect, world-architect, scene-architect) following Dual-Kernel Architect-with-Submodules pattern. The orchestrator novel-architect retains the 8-phase pipeline but delegates method-application to sub-modules. Foundation task — blocks 072, 074, 075, 076, 077."
created: 2026-05-11
updated: 2026-05-11
task_id: "071"
task_status: open
task_owner: "unassigned"
task_priority: P2
task_uses_prompts: []
task_spawns_research: []
task_spawns_prompts: []
task_blocked_by: []
task_supersedes: []
task_superseded_by: []
task_affects_paths:
  - skills/novel-architect/
  - skills/novel-architect-character/
  - skills/novel-architect-structure/
  - skills/novel-architect-world/
  - skills/novel-architect-scene/
---

# Task 071 — novel-architect Sub-Module Refactor

## Goal

Split the monolithic `novel-architect@1.0.0` skill into an **orchestrator + 4 sub-module skills** following the Dual-Kernel "Architect-with-Submodules" pattern (`refactor/ecosystem-analysis.md`). The orchestrator (`novel-architect`) keeps the 8-phase pipeline, project-config, NCP integration. The sub-modules own method application:

- `novel-architect-character/` — Phase 3 Character Architecture (TSDP/IFS/Big Five/Enneagramm/Jung application)
- `novel-architect-structure/` — Phase 2 + 5 (Storyform structure + Scene Matrix structure templates: 40-chapter-matrix, hero's-journey, save-the-cat, dramatica-quad)
- `novel-architect-world/` — Phase 4 World & Research (domain-mapping, deep-research-briefs delegation)
- `novel-architect-scene/` — Phase 5 + 6 (scene-level execution: per-moment Q1-Q5 audit, drafting workflow)

`done` when:
1. 4 new skill directories exist with valid L1+L2 frontmatter (passes `tools/fm/validate.py --type-check`)
2. `skills/novel-architect/SKILL.md` updated to reference sub-modules via `delegates_to` metadata
3. `skills/novel-architect/methods/{character,structure,conflict,research}/` migrated to corresponding sub-module skills (with old paths kept as compatibility symlinks/pointers during transition)
4. `tools/check-governance.sh` exit 0
5. Manual walk-through: `/novel-characters` command in orchestrator delegates to `novel-architect-character`

## Context

v1.0.0 is monolithic — all methods live under `skills/novel-architect/methods/`, all phases under `skills/novel-architect/phases/`. The Dual-Kernel analysis (refactor/SKILL_HOOKS_ANALYSIS.md) shows that sub-module skills with single entry-points per domain reduce skill-matching ambiguity and allow each sub-module to evolve independently.

Foundation task — blocks 072-077. Most v1.1.0 work touches sub-module skills, so the directory structure must exist first.

## Plan

1. Design sub-module directory structure (skill.md scaffold, references, methods location). Reference `/home/user/Dual-Kernel/skill-audit/ecosystem-analysis.md` for pattern.
2. Create 4 new skill directories with SKILL.md (orchestrator delegation contract documented)
3. Migrate `methods/character/*.md` → `skills/novel-architect-character/methods/`
4. Migrate `methods/structure/*.md` → `skills/novel-architect-structure/methods/`
5. Migrate `methods/research/*.md` → `skills/novel-architect-world/methods/`
6. Keep `skills/novel-architect/methods/` as compatibility pointers (references to sub-modules) for transition
7. Update `skills/novel-architect/SKILL.md` to list sub-modules in `metadata.delegates_to`
8. Update `skills/novel-architect/commands/novel-{characters,scenes,research,draft}.md` to delegate to sub-modules
9. Run `tools/fm/validate.py --type-check skills/` → 0 diagnostics
10. Verify governance pass

## Todo

- [ ] 1. Design + decision on sub-module count (4 vs 5; conflict-engine could be its own sub-module)
- [ ] 2. Create 4 sub-module skill directories with SKILL.md + readme.md
- [ ] 3. Migrate methods/character/ → novel-architect-character/methods/
- [ ] 4. Migrate methods/structure/ → novel-architect-structure/methods/
- [ ] 5. Migrate methods/research/ → novel-architect-world/methods/
- [ ] 6. methods/conflict/ — decide: stays in orchestrator OR splits across structure+character
- [ ] 7. Update orchestrator SKILL.md delegates_to
- [ ] 8. Update commands/ to delegate
- [ ] 9. Frontmatter validation + governance check
- [ ] 10. Manual walk-through test

## Links

- Parent epic: [Task 070](../070-novel-architect-v110-epic/task.md)
- Pattern source: `/home/user/Dual-Kernel/skill-audit/ecosystem-analysis.md`, `/home/user/Dual-Kernel/refactor/SKILL_HOOKS_ANALYSIS.md`
- Governing specs: [`TASK.md`](../../TASK.md), [`SKILLS.md`](../../SKILLS.md)
- Skill: [`skills/novel-architect/`](../../skills/novel-architect/)
