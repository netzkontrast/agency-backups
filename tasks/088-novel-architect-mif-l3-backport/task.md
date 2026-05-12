---
type: task
status: active
slug: novel-architect-mif-l3-backport
summary: "Retroactively apply the subset MIF Level 3 frontmatter (cognitive_type, decay_rate, derivation_chain) declared in skills/novel-architect/schemas/mif-level3.yaml to historical entries in skills/novel-architect/references/learnings.md per Task 077 prose spec. T4 entries (status: archived) receive metadata-frontmatter additions only per MAINTENANCE.md §1.0.1; no body edits. Independent of the linter cluster — touches a different file domain."
created: 2026-05-12
updated: 2026-05-12
task_id: "088"
task_status: open
task_owner: ""
task_priority: P3
task_uses_prompts: []
task_spawns_research: []
task_spawns_prompts: []
task_blocked_by:
  - "083"
task_supersedes: []
task_superseded_by: []
task_affects_paths:
  - skills/novel-architect/references/learnings.md
  - skills/novel-architect/schemas/mif-level3.yaml
---

# Task 088 — MIF Level 3 Backport (references/learnings.md)

## Goal

Apply the subset MIF Level 3 schema declared in [`skills/novel-architect/schemas/mif-level3.yaml`](../../skills/novel-architect/schemas/mif-level3.yaml) (cognitive_type ∈ {semantic, episodic, procedural}; bitemporal `valid_from` / `valid_to`; `decay_rate` ∈ [0.0, 1.0]; `derivation_chain` list) retroactively to historical Level 1/2 entries in [`skills/novel-architect/references/learnings.md`](../../skills/novel-architect/references/learnings.md). Per [Task 070's friction log §"Sub-task summary"](../070-novel-architect-v110-epic/friction-log.md#sub-task-summary): "MIF Level 1/2 → 3 backporting deferred (legacy entries stay as-is)" — this Task closes that deferred work.

`done` when:

1. Every entry in `references/learnings.md` carries the subset MIF L3 frontmatter required by `mif-level3.yaml`. Specifically: `cognitive_type`, `decay_rate`, `derivation_chain`. `valid_from` / `valid_to` MAY be inferred from `created:` / `updated:` if absent in the original entry.
2. **T4 entries (entries with `status: archived` or older than the v1.1.0 Epic close date 2026-05-11) receive metadata-frontmatter additions only** per [MAINTENANCE.md §1.0.1](../../MAINTENANCE.md#101-closed-research-t1t2-repair-allowance-task-059). No body edits. The migration MUST be auditable as additive-only via `git diff` showing only frontmatter line changes for these entries.
3. `decay_rate` defaults conservatively per the heuristic table below (operationalized in the Plan):
   | Entry age | Suggested `decay_rate` | Rationale |
   |---|---:|---|
   | < 30 days | 0.85 | High retention; recent + plausibly active |
   | 30–90 days | 0.65 | Mid retention; verify before reuse |
   | 90–180 days | 0.40 | Low retention; archive-candidate |
   | > 180 days | 0.20 | Archive-tier; survives lookup but soft-flagged |
4. `derivation_chain` populated where reconstructable from git history (`git log --follow` on the entry's first-appearance commit). Where not reconstructable, the field is set to `[]` rather than omitted.
5. The migration commit MUST pass `python3 tools/fm/validate.py --check-body skills/novel-architect/references/learnings.md` cleanly under the body-schema declared in `mif-level3.yaml`.
6. A migration audit document at `tasks/088-novel-architect-mif-l3-backport/migration-audit.md` (created during this Task's working session, not at scaffold) enumerates every migrated entry, its assigned `cognitive_type` + `decay_rate`, and the derivation-chain reconstruction source. Independent reviewer reads this audit to verify the migration without re-deriving classifications from scratch.

## Context

[Task 077 closure](../077-novel-architect-mif-learnings-sessionhook/task.md) shipped the subset MIF Level 3 schema at `skills/novel-architect/schemas/mif-level3.yaml` and a lean `scripts/session-start.sh` that surfaces recent learnings at session-start. The schema was applied forward-only — new entries written after the v1.1.0 Epic close carry L3 frontmatter, but pre-Epic entries remain at L1/L2.

The forward-only adoption was a deliberate scope decision in v1.1.0 (per Task 070's friction log: "MIF Level 1/2 → 3 backporting deferred"). It was a defensible trade given v1.1.0's session budget; carrying the backport forward to v1.2.0 is the corresponding scope-cleanup.

T4-immutability handling matches the [MAINTENANCE.md §1.0.1 closed-research T1/T2 repair allowance](../../MAINTENANCE.md#101-closed-research-t1t2-repair-allowance-task-059) precedent: archived entries can receive frontmatter additions (T1/T2 metadata repair) but never body edits (T3+ is forbidden post-archival). This boundary MUST be respected mechanically — `tools/fm/edit.py --set` and `--append-list` are the only mutation tools used; `tools/fm/section-editor` and direct body edits are forbidden on archived entries.

Per [Epic 083 sub-task DAG](../083-novel-architect-v120-enforcement-epic/task.md#dependency-graph), this Task is independent — no linter dependency. It can land before, during, or after 084-087 without blocking or being blocked.

## Plan

1. **Inventory the existing learnings.md entries** — produce a working table classifying each entry's current frontmatter level (L1, L2, or partial L3), its `status:` value (active, archived), and its age relative to 2026-05-11 (v1.1.0 close date). Build the inventory into the working-session's audit document.
2. **Assign cognitive_type per entry** — using the [Task 077 prose spec](../077-novel-architect-mif-learnings-sessionhook/task.md)'s classification heuristic: lessons-learned and prose specs → semantic; specific session events → episodic; reusable workflows → procedural. Audit each assignment in the migration-audit document.
3. **Compute decay_rate + derivation_chain** — apply the decay heuristic table in §Goal; reconstruct `derivation_chain` via `git log --follow` on the entry's first-appearance commit. Where ambiguous, set `derivation_chain: []` and note the limitation in the audit document.
4. **Apply via `tools/fm/edit.py`** — `--set` for scalar fields, `--append-list` for `derivation_chain`. Verify each archived entry receives frontmatter changes only via `git diff` review. Run `python3 tools/fm/validate.py --check-body skills/novel-architect/references/learnings.md` until clean.

## Todo

- [ ] 1. Inventory current entries in `references/learnings.md`; classify L1/L2/partial-L3 + active/archived + age-bucket.
- [ ] 2. Assign `cognitive_type` per entry; document each in `migration-audit.md`.
- [ ] 3. Compute `decay_rate` per entry per the heuristic table.
- [ ] 4. Reconstruct `derivation_chain` via `git log --follow`; populate `[]` where not reconstructable; note in audit.
- [ ] 5. Apply changes via `tools/fm/edit.py --set` / `--append-list`; verify archived entries get frontmatter-only diff via `git diff` review.
- [ ] 6. Run `python3 tools/fm/validate.py --check-body skills/novel-architect/references/learnings.md` → exits 0.
- [ ] 7. Write `tasks/088-novel-architect-mif-l3-backport/migration-audit.md` as the reviewer-facing artefact.

## Acceptance

```gherkin
Feature: skills/novel-architect/references/learnings.md historical entries carry MIF L3 frontmatter; T4 entries receive metadata-only edits

  # anchor: 088.AC.1
  Scenario: Every entry has L3 frontmatter
    Given skills/novel-architect/references/learnings.md after Task 088 closure
    When the agent queries tools/fm/validate.py --check-body on the file using the mif-level3.yaml body-schema
    Then the validator MUST exit 0
    And every entry MUST carry cognitive_type, decay_rate, and derivation_chain frontmatter keys

  # anchor: 088.AC.2
  Scenario: Archived entries receive frontmatter-only changes
    Given an entry in learnings.md with status: archived predating 2026-05-11
    When the agent inspects git diff for the Task 088 migration commit
    Then the diff for this entry MUST show only YAML frontmatter line changes
    And no body lines for this entry MUST appear in the diff

  # anchor: 088.AC.3
  Scenario: Migration audit document enumerates every migrated entry
    Given Task 088 has been closed
    When the agent reads tasks/088-novel-architect-mif-l3-backport/migration-audit.md
    Then the audit MUST list every migrated entry with its assigned cognitive_type, decay_rate, and derivation_chain source
    And entries with derivation_chain: [] MUST carry an explicit "not reconstructable" note in the audit
```

## Links

- Parent Epic: [Task 083](../083-novel-architect-v120-enforcement-epic/task.md)
- Upstream context: [Task 077 — MIF Level 3 + SessionStart-Hook](../077-novel-architect-mif-learnings-sessionhook/task.md), [Task 070 friction log §"Sub-task summary"](../070-novel-architect-v110-epic/friction-log.md#sub-task-summary)
- Governing specs: [`TASK.md`](../../TASK.md), [`MAINTENANCE.md §1.0.1`](../../MAINTENANCE.md#101-closed-research-t1t2-repair-allowance-task-059)
- Schema: [`skills/novel-architect/schemas/mif-level3.yaml`](../../skills/novel-architect/schemas/mif-level3.yaml)
- Implementation target: [`skills/novel-architect/references/learnings.md`](../../skills/novel-architect/references/learnings.md)
- Migration tooling: [`tools/fm/edit.py`](../../tools/fm/edit.py), [`tools/fm/validate.py`](../../tools/fm/validate.py) (`--check-body`)
