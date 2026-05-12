---
type: task
status: active
slug: retire-novel-architect-legacy-duplicate
summary: "Placeholder Task that retires skills/novel-architect-legacy@0.3.3-archived once the three preconditions defined in Task 070 §Legacy Retirement Criterion are met. Blocked on Task 090 (v1.1.1-hardening) + productive Kohärenz-Protokoll sessions on v1.1.1+. Criterion (c) is already mechanically satisfied; (a)+(b) require runtime evidence. Filed now (rather than at-need) so the retirement contract is discoverable to future agents who might be tempted to clean up the legacy directory prematurely."
created: 2026-05-12
updated: 2026-05-12
task_id: "091"
task_status: blocked
task_owner: "unassigned"
task_priority: P3
task_uses_prompts: []
task_spawns_research: []
task_spawns_prompts: []
task_blocked_by:
  - 090
task_superseded_by: []
task_affects_paths:
  - skills/novel-architect-legacy/
---

# Task 091 — Retire novel-architect-legacy

## Goal

Remove `skills/novel-architect-legacy/` (currently `version: "0.3.3-legacy"`, `status: archived`, `date_deprecated: 2026-05-11`) from the repository once the three retirement preconditions defined in [Task 070 §"Legacy Retirement Criterion"](../070-novel-architect-v110-epic/task.md#legacy-retirement-criterion-pr-101-review-43) all hold. The Task is `done` when:

1. The legacy directory `skills/novel-architect-legacy/` no longer exists on `main`.
2. The retirement is recorded with a v1.2.0+ changelog entry in `skills/novel-architect/references/learnings.md`.
3. `tools/check-governance.sh` exits 0 on the removal commit.

## Retirement Preconditions (verification commands)

This Task remains `task_status: blocked` until ALL THREE hold:

- **(a)** ≥3 productive Kohärenz-Protokoll sessions completed on novel-architect v1.1.1+ without falling back to the legacy skill.
  ```bash
  # Verify on the host with the migrated workspace:
  ls /home/claude/novel-projects/kohaerenz-protokoll/sessions/ 2>/dev/null | wc -l
  # MUST report ≥ 3
  ```
- **(b)** NCP-validation of the migrated `kohaerenz-protokoll.ncp.json` passes against the latest `ncp-author` schema.
  ```bash
  # Run from the host where the migrated workspace lives:
  python3 -m skills.ncp_author.validate \
    /home/claude/novel-projects/kohaerenz-protokoll/canon/kohaerenz-protokoll.ncp.json
  # MUST exit 0
  ```
- **(c)** No `task_blocked_by` or `task_supersedes` frontmatter entries on legacy paths remain in `tasks/`.
  ```bash
  cd /home/user/agency
  grep -rn "task_blocked_by:.*legacy\|task_supersedes:.*novel-architect-legacy" tasks/ \
    | grep -v "tasks/091-retire-novel-architect-legacy-duplicate"
  # MUST report 0 hits (this Task itself is allowed to mention legacy in its own supersession metadata)
  ```
  **Status at filing time: criterion (c) is already satisfied.**

## Plan

When all three criteria hold:

1. Transition `task_status: blocked` → `open` (Task is unblocked).
2. Remove `skills/novel-architect-legacy/` via `git rm -r`.
3. Append v1.2.x retirement-note entry to `skills/novel-architect/references/learnings.md`.
4. Update [`skills/novel-architect/SKILL.md`](../../skills/novel-architect/SKILL.md) `metadata.predecessor` field — either remove or change to a historical note.
5. Run `tools/check-governance.sh`; commit; PR.

## Todo

- [ ] 1. Wait for blocker [Task 090](../090-novel-architect-v111-hardening/task.md) to close (`task_status: done`)
- [ ] 2. Verify criterion (a) — ≥3 productive sessions on v1.1.1+ — via the command above
- [ ] 3. Verify criterion (b) — NCP-validation passes — via the command above
- [ ] 4. Re-verify criterion (c) — no `task_blocked_by` legacy refs — via the command above
- [ ] 5. Transition `task_status` to `open`, fill `task_owner`
- [ ] 6. `git rm -r skills/novel-architect-legacy/`
- [ ] 7. Append retirement-note entry to `references/learnings.md`
- [ ] 8. Update orchestrator `SKILL.md` `metadata.predecessor` field
- [ ] 9. Run governance gate → exit 0
- [ ] 10. Open PR

## Links

- Blocker: [Task 090 — novel-architect-v111-hardening](../090-novel-architect-v111-hardening/task.md)
- Originating criterion: [Task 070 §Legacy Retirement Criterion](../070-novel-architect-v110-epic/task.md#legacy-retirement-criterion-pr-101-review-43)
- Target for removal: [`skills/novel-architect-legacy/`](../../skills/novel-architect-legacy/)
- Governing specs: [`TASK.md`](../../TASK.md), [`SKILLS.md`](../../SKILLS.md)
