---
type: task
status: active
slug: novel-architect-v111-hardening
summary: "Convert novel-architect@1.1.0 from metadata-only delegation into a runtime two-layer contract. Rewrites 5 phase files + 7 command files in the orchestrator to delegate method-application to existing 4 sub-modules. Graduates scene from stub. Ships 3 of 4 deferred CLI linters (worksheet-order WARN, hard-rules WARN→ERROR-promotion-deferred, canon-status WARN). Closes /sc:analyze findings H1, H2, M1, M2, M3, M4 from the v1.1.0 release."
created: 2026-05-12
updated: 2026-05-12
task_id: "083"
task_status: open
task_owner: "claude-code"
task_priority: P1
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
  - tools/check-worksheet-order.py
  - tools/check-hard-rules.py
  - tools/check-canon-status.py
  - tools/check-governance.sh
  - TASK.md
---

# Task 083 — novel-architect@1.1.1-hardening

## Goal

Land v1.1.1 of the novel-architect skill family by converting the v1.1.0 metadata-only sub-module declaration into a runtime two-layer delegation contract. The Task is `done` when:

1. All 12 orchestrator files (5 phase + 7 command) reference no obsolete `methods/{character,structure,research}/` paths (`grep -rn ... → 0 hits`).
2. The 4 sub-modules gain the 14 new method files enumerated in [`workflow.md`](./workflow.md) §2 Cluster A.
3. `skills/novel-architect-scene/SKILL.md` no longer carries the "stub in v1.1.0" qualifier; both orchestrator and scene SKILL.md report `version: "1.1.1"`.
4. `io_helpers.SKILL_VERSION` equals `SKILL.md.metadata.version` (verified by a new pytest assertion).
5. Three new CLI linters (`check-worksheet-order.py`, `check-hard-rules.py`, `check-canon-status.py`) ship at WARN tier with passing fixture tests; wired into `tools/check-governance.sh`.
6. `tools/check-governance.sh` exits 0 on the final commit.
7. v1.1.1 changelog entry appended to `skills/novel-architect/references/learnings.md`.
8. All 5 V111.US acceptance scenarios from [`workflow.md`](./workflow.md) §4 pass their verify commands.

## Context

The v1.1.0 Epic ([Task 070](../070-novel-architect-v110-epic/task.md)) closed in a single bundled session (2026-05-11, FL2) with the friction log explicitly flagging "lean but real" depth and 4 deferred CLI linters. A subsequent `/sc:analyze` run surfaced 11 H/M/L findings, the most critical being:

- **H1** — 16+ inline references to migrated `methods/character/`, `methods/structure/`, `methods/research/` paths still in phase + command prose.
- **H2** — phase3/4/5/6 + commands have **zero** delegation prose to sub-modules (only frontmatter `metadata.delegates_to` declares it).
- **M1** — `io_helpers.SKILL_VERSION = "1.0.0"` stale vs. SKILL.md `version: "1.1.0"`.
- **M2** — `project_workspace()` docstring promises per-project YAML override never implemented.
- **M3** — 8 unused public helpers in `io_helpers.py`.
- **M4** — scene sub-module self-declared `stub in v1.1.0`.

The full planning pipeline ran in-session: `/sc:analyze` → `/sc:brainstorm` (6 locked decisions D1–D6) → `/sc:design` (5 artifacts via 4 Explore subagents) → `/sc:workflow` (19-commit plan, 4 clusters, 5 ACs). The detailed plan is in [`workflow.md`](./workflow.md).

## Plan

Per [`workflow.md`](./workflow.md):

1. **Cluster A** (9 commits) — prose rewrite under the two-layer contract. Phase files keep workflow/askuser/gates; sub-modules absorb method-detail. Path refs rewritten from `methods/character/` → `../../novel-architect-character/methods/`.
2. **Cluster B** (3 commits) — scene graduation (drop "stub" qualifier, bump versions), `SKILL_VERSION` SSoT fix, v1.1.1 changelog.
3. **Cluster C** (4 commits) — 3 new CLI linters at WARN tier with fixture corpus and `check-governance.sh` integration.
4. **Cluster D** (3 commits) — `project_workspace()` docstring alignment, dead-code cleanup of 8 unused helpers, retirement-placeholder verification.

Sub-Tasks filed alongside (see §"Spawned Tasks" below): 084 (retirement placeholder), 085 (linter ERROR-promotion follow-up), 086 (scene-audit linter).

## Todo

- [ ] 1. File companion Tasks 084, 085, 086; sync `tasks/readme.md`
- [ ] 2. Save [`workflow.md`](./workflow.md) (this Task's executable plan)
- [ ] 3. Add planning-pipeline rule §T.9 to `TASK.md` (codifies the /sc:analyze→brainstorm→design→workflow ladder)
- [ ] 4. Cluster A — 9 commits: refactor phase 2, 3, 4, 5, 6 + 7 commands under the two-layer contract
- [ ] 5. Cluster B — 3 commits: scene graduation + SKILL_VERSION SSoT + v1.1.1 changelog
- [ ] 6. Cluster C — 4 commits: 3 new linters + fixture corpus + governance.sh wiring
- [ ] 7. Cluster D — 3 commits: project_workspace docstring + io_helpers dead-code prune + retirement-placeholder verify
- [ ] 8. Run `tools/check-governance.sh` → exit 0 on final commit
- [ ] 9. Write friction-log.md with FL declaration
- [ ] 10. Open draft PR via mcp__github__create_pull_request

## Acceptance Criteria (Gherkin)

```gherkin
Feature: novel-architect@1.1.1 honours the two-layer delegation contract at runtime

  # anchor: V111.US1
  Scenario: /novel-characters delegates to novel-architect-character at runtime
    Given a Roman session at Phase 3 with approved architecture.yaml
    When the user invokes /novel-characters
    Then the orchestrator command MUST hand off to skills/novel-architect-character/SKILL.md
    And the psycho-model schema MUST resolve from skills/novel-architect-character/methods/<model>.md
    And no path under skills/novel-architect/methods/character/ MUST be referenced

  # anchor: V111.US2
  Scenario: Scene sub-module is no longer a stub
    Given a Roman session at Phase 5 needing per-moment scene detail
    When the orchestrator delegates to novel-architect-scene
    Then novel-architect-scene MUST own scene-matrix execution, drafting-precheck, and the Q1-Q5 audit
    And metadata.delegates_to in the orchestrator SKILL.md MUST NOT contain "stub"

  # anchor: V111.US3
  Scenario: Hard-rules linter catches H1-H12 violations at pre-commit
    Given a storyform file with an H7 Resolve violation
    When the contributor runs git commit
    Then tools/check-hard-rules.py MUST exit non-zero at WARN tier minimum
    And the diagnostic MUST cite H7 with file:line and the violated invariant

  # anchor: V111.US4
  Scenario: Legacy retirement contract is discoverable
    Given a future agent considering deletion of skills/novel-architect-legacy/
    When the agent searches tasks/ for retirement intent
    Then a Task 084-retire-novel-architect-legacy MUST exist
    And its task_status MUST be blocked
    And its task.md MUST list verification commands for criteria (a) and (b)

  # anchor: V111.US5
  Scenario: SKILL_VERSION matches SKILL.md
    Given the orchestrator skill loaded by an agent
    When the agent reads io_helpers.SKILL_VERSION
    Then the value MUST equal the version declared in SKILL.md metadata.version
```

## Spawned Tasks

- [Task 084 — retire-novel-architect-legacy](../084-retire-novel-architect-legacy/task.md) — placeholder, `task_status: blocked` until productive-session criteria (a)+(b) met
- [Task 085 — promote-check-hard-rules-error-tier](../085-promote-check-hard-rules-error-tier/task.md) — WARN→ERROR promotion after one validation cycle
- [Task 086 — novel-architect-scene-audit-linter](../086-novel-architect-scene-audit-linter/task.md) — 4th deferred linter, follows scene graduation

## Links

- Predecessor: [Task 070](../070-novel-architect-v110-epic/task.md) (v1.1.0 Epic; closed FL2)
- Foundation: [Task 071](../071-novel-architect-submodule-refactor/task.md) (sub-module structure)
- Executable plan: [`workflow.md`](./workflow.md)
- Friction log (at close): [`friction-log.md`](./friction-log.md)
- Governing specs: [`TASK.md`](../../TASK.md), [`SKILLS.md`](../../SKILLS.md), [`AGENTS.md`](../../AGENTS.md), [`CLAUDE.md`](../../CLAUDE.md)
- Skill: [`skills/novel-architect/`](../../skills/novel-architect/)
- Pattern source (cited but never read in v1.1.0): [`/home/user/Dual-Kernel/skill-audit/ecosystem-analysis.md`](file:///home/user/Dual-Kernel/skill-audit/ecosystem-analysis.md)
