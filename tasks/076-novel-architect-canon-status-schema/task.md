---
type: task
status: active
slug: novel-architect-canon-status-schema
summary: "Adopt Dual-Kernel's Canon-Status Conflict-Schema for canon-meta.md entities in novel-architect. Each entity (character, world-element, theme-claim) carries a canon_status (confirmed > provisional > disputed > uncertain > decanonized) hierarchy plus multi-variant conflicts with explicit provenance. Affects Phase 4 (research integration) and Phase 7 (canon-updates / OQ-resolution)."
created: 2026-05-11
updated: 2026-05-11
task_id: "076"
task_status: done
task_owner: "claude-code"
task_priority: P3
task_uses_prompts: []
task_spawns_research: []
task_spawns_prompts: []
task_blocked_by:
  - 071
task_supersedes: []
task_superseded_by: []
task_affects_paths:
  - skills/novel-architect/assets/canon-meta-schema.md
  - skills/novel-architect-world/phases/phase4-world-research.md
  - skills/novel-architect/phases/phase7-iteration.md
---

# Task 076 — Canon-Status Conflict-Schema

## Goal

Adopt the Dual-Kernel entity schema (`/home/user/Dual-Kernel/knowledge-graph/world/dual.md`) as the structured format for `canon-meta.md` entries in `novel-architect`. Each canon entry (character-fact, world-fact, theme-claim) carries:

```yaml
- title: "Kael's Primary Persona"
  id: "kael-primary-persona"
  domain: "character"
  canon_status: "confirmed"  # confirmed > provisional > disputed > uncertain > decanonized
  aliases: []
  tags: ["protagonist", "alter-system"]
  related:
    - "[[Kael]]"
    - "[[Juna]]"
  sources:
    - file: "intent.yaml"
      lines: "12-14"
      relevance: "primary"
  conflicts:
    - id: "trigger-mechanism"
      description: "What triggers persona-switch?"
      variants:
        - claim: "Trauma re-exposure"
          source: "session-3 OQ-resolution"
        - claim: "Voluntary, by Kael's will"
          source: "draft ch-7 §2"
  first_appearance_chapter: 3
  last_referenced_chapter: null
```

`done` when:
1. New `assets/canon-meta-schema.md` documents the schema with full example
2. Phase 4 detail file updated: when research findings integrate into canon-meta.md, they MUST use this schema with `canon_status: provisional` initially
3. Phase 7 (audit-mode) detail file updated: a canon-status pass checks for `disputed` entries that block Phase 5/6, and `decanonized` entries still being referenced in active drafts
4. Migration path documented: how to convert existing free-text `canon-meta.md` (Kohärenz-Protokoll legacy migration) to schema entries (manual + assisted)

## Context

v1.0.0's `canon-meta.md` is unstructured prose. When two sessions produce conflicting claims (e.g. Session A: "Kael's trigger is trauma"; Session B: "Kael's trigger is voluntary"), v1.0.0 has no mechanism to surface the conflict — it gets resolved silently by whichever session writes last. The Dual-Kernel schema's `conflicts.variants` field makes the conflict explicit + traceable to source.

The `canon_status` hierarchy (confirmed > provisional > disputed > uncertain > decanonized) maps natively to the agency's `task_status` pattern — it's a familiar mental model.

## Plan

1. Read `/home/user/Dual-Kernel/knowledge-graph/world/dual.md` + 2-3 other domain entries for schema patterns
2. Read `/home/user/Dual-Kernel/tools/common.py` for Pydantic models (informs which fields are mandatory vs optional)
3. Author `assets/canon-meta-schema.md` with full example + field-by-field documentation
4. Document Phase 4 integration: `provisional` is the default canon_status when findings first land
5. Document Phase 7 integration: audit-mode runs a canon-status sweep (any `disputed`? any `decanonized` still referenced?)
6. Migration guide: how to convert prose canon-meta.md to schema entries
7. Decide validation tool: do we need a Python validator, or is prose-with-yaml-blocks enough?

## Todo

- [x] 1. Read Dual-Kernel entity examples
- [x] 2. Read Dual-Kernel common.py for Pydantic patterns
- [x] 3. Author `assets/canon-meta-schema.md`
- [x] 4. Update Phase 4 detail file
- [x] 5. Update Phase 7 detail file (audit-mode addition)
- [x] 6. Author migration guide
- [x] 7. Decide validation tooling
- [x] 8. Smoke test on Kohärenz-Protokoll legacy canon-meta.md migration

## Links

- Parent epic: [Task 070](../070-novel-architect-v110-epic/task.md)
- Blocked by: [Task 071](../071-novel-architect-submodule-refactor/task.md)
- Pattern source: `/home/user/Dual-Kernel/knowledge-graph/world/dual.md`, `/home/user/Dual-Kernel/tools/common.py`
- Affects: legacy migration path (`skills/novel-architect/scripts/bootstrap_project.sh kohaerenz-protokoll`)
- Governing specs: [`TASK.md`](../../TASK.md), [`SKILLS.md`](../../SKILLS.md)
