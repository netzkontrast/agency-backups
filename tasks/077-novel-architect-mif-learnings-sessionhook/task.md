---
type: task
status: active
slug: novel-architect-mif-learnings-sessionhook
summary: "Adopt MIF Level 3 schema for novel-architect's references/learnings.md (semantic/episodic/procedural classification, bitemporal tracking, decay_rate, derivation_chain) AND ship a lean SessionStart-Hook (scripts/session-start.sh) that loads project-config and last phase context. Replaces v1.0.0's free-form append-only learnings.md with structured memory traces."
created: 2026-05-11
updated: 2026-05-11
task_id: "077"
task_status: open
task_owner: "unassigned"
task_priority: P3
task_uses_prompts: []
task_spawns_research: []
task_spawns_prompts: []
task_blocked_by:
  - "071"
task_supersedes: []
task_superseded_by: []
task_affects_paths:
  - skills/novel-architect/references/learnings.md
  - skills/novel-architect/schemas/mif-level3.yaml
  - skills/novel-architect/scripts/session-start.sh
  - skills/novel-architect/phases/phase0-bootstrap.md
  - skills/novel-architect/phases/phase7-iteration.md
---

# Task 077 — MIF Level 3 learnings + SessionStart-Hook (lean)

## Goal

Two coupled Dual-Kernel patterns:

**A. MIF Level 3 learnings schema** — `references/learnings.md` evolves from free-form append-list to structured memory traces with cognitive triad (semantic/episodic/procedural), bitemporal tracking (transaction_time vs valid_time), decay_rate, derivation_chain. Schema adopted from `/home/user/Dual-Kernel/schemas/mif_level3_agent_trace.yaml`.

**B. Lean SessionStart-Hook** — `scripts/session-start.sh` (adapted from `/home/user/Dual-Kernel/.claude/hooks/session-start.sh`) runs per project on session start: verifies `project-config.yaml`, checks `ncp-author` skill availability, parses last phase's `learnings.md` entries for context-injection. Lean = no Python venv setup, no spacy model — minimal, optional, per-project.

`done` when:
1. `schemas/mif-level3.yaml` exists in skill (subset of Dual-Kernel schema appropriate for narrative work)
2. `references/learnings.md` migrated to MIF Level 3 format (existing entries get retroactive minimal frontmatter; new entries follow schema)
3. `scripts/session-start.sh` exists, executable, runs in <2s, exits cleanly when project-config absent
4. Phase 0 (bootstrap) detail file references the SessionStart-Hook as optional
5. Phase 7 (iteration) detail file documents the MIF Level 3 capture pattern for session-end checkpoint
6. Backward compat: old plain-text learnings entries continue to work (graceful schema-detection)

## Context

v1.0.0's `references/learnings.md` is a chronological append-list. Sessions log lessons, but:
- No classification (everything is mixed-mode)
- No decay (entries from 2026-03 read the same as 2026-12)
- No derivation chain (cannot trace why a lesson exists)
- No conflict-tracking when two sessions learn contradictory lessons

Dual-Kernel's MIF Level 3 schema solves all four. Adopting the **full** schema would be over-engineering for narrative work — this task adopts a **narrative-appropriate subset**:

```yaml
- id: "mif:novel-architect-learning-001"
  type: "framework-choice"  # or: refinement-step, debug-session, architecture-choice
  timestamp: "2026-05-11T12:00:00Z"
  namespace: "novel-architect"
  cognitive_function: "exploitation"  # or: exploration, semantic_consolidation
  storage_tier: "LTM"  # or: STM, PM (procedural memory)
  valid_time: "2026-05-11T12:00:00Z"
  decay_rate: 0.1
  confidence_score: 0.9
  derivation_chain: ["session-2026-05-11"]
  body: |
    Lesson: Description doesn't auto-include all command-trigger names — must add manually.
    Action: All commands now in metadata.triggers.
```

The SessionStart-Hook complements this by surfacing the most-recent N traces (sorted by `valid_time × decay_rate`) at session-start.

## Plan

1. Read `/home/user/Dual-Kernel/schemas/mif_level3_agent_trace.yaml` end-to-end
2. Identify narrative-appropriate subset (remove fields like `bias`, `variance` that are ML-specific)
3. Author `skills/novel-architect/schemas/mif-level3.yaml` (subset schema)
4. Migrate `references/learnings.md` entries to MIF Level 3 format (retroactive — minimal valid frontmatter)
5. Author lean `scripts/session-start.sh` (no Python deps, just bash + grep + maybe yq)
6. Update `phases/phase0-bootstrap.md` to mention SessionStart-Hook as optional
7. Update `phases/phase7-iteration.md` to document Session-End checkpoint capture pattern using MIF Level 3
8. Decide whether to integrate with mnemonic system (`/mnemonic:capture`) or keep file-based — lean = file-based
9. Backward compat test: old plain-text entries still parseable

## Todo

- [ ] 1. Read Dual-Kernel MIF Level 3 schema
- [ ] 2. Subset schema for narrative work
- [ ] 3. Author `schemas/mif-level3.yaml`
- [ ] 4. Migrate existing learnings.md entries
- [ ] 5. Author `scripts/session-start.sh`
- [ ] 6. Update Phase 0 detail file
- [ ] 7. Update Phase 7 detail file
- [ ] 8. Backward compat smoke test
- [ ] 9. Decide mnemonic integration (defer to v1.2.0?)

## Links

- Parent epic: [Task 070](../070-novel-architect-v110-epic/task.md)
- Blocked by: [Task 071](../071-novel-architect-submodule-refactor/task.md)
- Schema source: `/home/user/Dual-Kernel/schemas/mif_level3_agent_trace.yaml`
- Hook pattern source: `/home/user/Dual-Kernel/.claude/hooks/session-start.sh`
- Related (v1.2.0+): Full mnemonic system integration (`/mnemonic:capture`, `_episodic/`, `_semantic/`, `_procedural/` from Dual-Kernel) — explicitly out-of-scope for v1.1.0 (lean integration only)
- Governing specs: [`TASK.md`](../../TASK.md), [`SKILLS.md`](../../SKILLS.md)
