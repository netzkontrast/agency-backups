---
type: task
status: active
slug: novel-architect-v110-epic
summary: "Epic umbrella for novel-architect@1.1.0 — orchestrates 7 sub-tasks (071-077) that implement Sub-Module Refactor + Dramatica-Native Integration (Worksheet-Loop, Hard Rules, Anti-Patterns, Scene-Level-Bridge) + selective Dual-Kernel Patterns (Canon-Status Schema, MIF Level 3, SessionStart-Hook). Goal: skill becomes dramatica-native instead of dramatica-delegating, structured into 4-5 sub-skills following Dual-Kernel Architect pattern."
created: 2026-05-11
updated: 2026-05-11
task_id: "070"
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
---

# Task 070 — novel-architect@1.1.0 Epic

## Goal

Coordinate the v1.1.0 release of `skills/novel-architect/` across 7 linked sub-tasks (071-077). The Epic is `done` when:

1. All 7 sub-tasks have `task_status: done` OR `task_status: updated` with documented disposition
2. `skills/novel-architect/SKILL.md` references the new sub-module architecture
3. `tools/check-governance.sh` exits 0 (gating checks pass) after all sub-tasks land
4. A v1.1.0 changelog entry is appended to `skills/novel-architect/references/learnings.md`

This Task itself contains **no diffs** — diffs land via sub-tasks. This Task is the orchestration / dependency-tracking artifact.

## Context

v1.0.0 (PR #101, commit `ee1daac`) refactored `novel-architect` to be project-agnostic with 8 phases, NCP integration, methods library. Deep analysis revealed two improvement axes:

**Axis A — Dramatica-Native:** v1.0.0 delegates to `dramatica-theory` and `dramatica-vocabulary` but does not systematically *use* their 13 reference files. Worksheet (00-storyform-worksheet.md), Hard Rules (00-storyform-validation.md), Decision Heuristics (10-decision-heuristics.md), Anti-Patterns (11-anti-patterns.md), Scene-Level-Bridge (12-scene-level-bridge.md), Worked Examples (13-worked-storyforms.md) are unused.

**Axis B — Dual-Kernel Patterns:** The `/home/user/Dual-Kernel/` project has methodological patterns (MIF Level 3 memory, autopoietic loops, SessionStart hooks, canon-status conflict schema, ETL pipeline) that selectively apply to long-running novel projects.

The user's scope decision: **Sub-Module Refactor + all 4 Dramatica integrations + 3 Dual-Kernel patterns** (Canon-Status Schema, MIF Level 3 for learnings, SessionStart-Hook lean). Full plan in `/root/.claude/plans/bitte-baue-aus-den-velvety-bentley.md` (local).

## Sub-Tasks (children)

| Task ID | Title | Blocks/Blocked-by | Affects |
|---------|-------|-------------------|---------|
| **071** | Sub-Module Architecture Refactor | foundation (none) | skills/novel-architect/ (structural) |
| **072** | Phase 2 Worksheet-Loop (00-storyform-worksheet.md) | blocked by 071 | phases/phase2-narrative-architecture.md, methods/storyform/ |
| **073** | Hard Rules Validation (H1-H12) | blocked by 072 | phases/phase2-, methods/validation/, assets/hard-rules-check.md |
| **074** | Anti-Patterns durchgängig (AP-1 bis AP-14) | blocked by 071 | phases/phase2-, phase3-, phase6- |
| **075** | Scene-Level-Bridge Q1-Q5 | blocked by 071 | phases/phase5-, phase6-, references/ncp-integration-contract.md |
| **076** | Canon-Status Conflict-Schema | blocked by 071 | phases/phase4-, phase7-, assets/canon-meta-schema.md |
| **077** | MIF Level 3 learnings + SessionStart-Hook (lean) | blocked by 071 | references/learnings.md, scripts/session-start.sh, schemas/mif-level3.yaml |

**Dependency graph:**

```
        ┌──── 072 ──── 073
        │
071 ────┼──── 074
        │
        ├──── 075
        │
        ├──── 076
        │
        └──── 077
```

## Plan

1. **Land 071** (Sub-Module Architecture Refactor) first — establishes the directory structure and orchestrator pattern that 072-077 depend on. Output: skills/novel-architect/SKILL.md updated, sub-module skill stubs in skills/novel-architect-{character,structure,world,scene}/.
2. **Land 072, 074, 075, 076, 077 in parallel** — each independent after 071. Order does not matter; commits can be sequential or interleaved.
3. **Land 073 after 072** — Hard Rules validation depends on the worksheet structure from 072.
4. **Verify Epic acceptance** — all 7 sub-tasks `done`; `tools/check-governance.sh` exit 0; update SKILL.md to reflect v1.1.0; append changelog to learnings.md.

## Todo

- [ ] 1. Land Task 071 (foundation)
- [ ] 2. Land Tasks 072, 074, 075, 076, 077 (parallel after 071)
- [ ] 3. Land Task 073 (after 072)
- [ ] 4. Update SKILL.md frontmatter: `version: "1.1.0"`, `date_updated`
- [ ] 5. Append v1.1.0 changelog entry to `references/learnings.md`
- [ ] 6. Run `tools/check-governance.sh` → exit 0
- [ ] 7. Update PR #101 (or new PR) — close Epic

## Links

- Governing specs: [`TASK.md`](../../TASK.md), [`SKILLS.md`](../../SKILLS.md), [`AGENTS.md`](../../AGENTS.md)
- Predecessor work: PR #101 (commit `ee1daac` — v1.0.0 refactor + /sc:improve iterations)
- Local plan: `/root/.claude/plans/bitte-baue-aus-den-velvety-bentley.md`
- Skill: [`skills/novel-architect/`](../../skills/novel-architect/)
- Related skill: [`skills/dramatica-theory/`](../../skills/dramatica-theory/), [`skills/ncp-author/`](../../skills/ncp-author/)
