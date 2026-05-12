---
type: note
status: active
slug: task-094-source-plan
summary: "Verbatim mirror of the Claude-Code Plan-mode planning artifact for Task 094 (originally authored at /root/.claude/plans/now-please-look-at-greedy-cascade.md). Captured here for audit trail per the user's request: every Epic spec MUST cite its source plan."
created: 2026-05-12
updated: 2026-05-12
---

# Plan — Write Task 094 Epic: "Skill Integration & Agency Default Surface"

## Context

After closing Task 092 (Phase 2 skill-corpora port), Agency hosts **52 imported skills** under `skills/sc-*` + `skills/superpowers-*` — but **47 of them have no root-spec citation**, no `.claude/` directory exists, no plugin manifest exists, and no per-skill hooks fire. The skills are inert content; Claude Code does not "know" about them on default.

The user wants:

1. **Default discoverability** — Claude Code auto-loads skill descriptions every session (Pattern A: `.claude/` mirror).
2. **Reusable distribution** — Agency declares itself a plugin so the whole stack ships as `agency@1.0.0` (Pattern B: `.claude-plugin/plugin.json`).
3. **Spec-layer documentation** — every imported skill cited from at least one root spec so a human reader can audit the surface (Pattern C: root-spec citations).
4. **Event-driven hooks** — 5 D.7-compliant hooks (one per Claude Code event) that route invocations through the relevant Superpowers discipline gates.
5. **Carried-forward closure** — ratify the expanded `skill_kind` enum in `SKILLS.md §3` (T3) and fix the triage-note `superclaude_framework@v4.3.0` typos (T1) from Task 092's friction log.

This is a single Epic Task (proposed slot **094**) that mirrors the four-sequential-subtask structure of Task 091 and Task 092. The plan below is the **planning artifact**; the deliverable of executing this plan is the Epic Task file itself (`tasks/094-<slug>/task.md` + 4 subtask files + `friction-log.md` + `readme.md`), *not* the integration work yet.

---

## Critical Constraint — ADR-0011 D.7

> "**D.7 No SessionStart injection.** Upstream SessionStart hooks (SuperClaude pm-agent restore, Superpowers `using-superpowers` injection) MUST NOT be ported. The Agency bootstrap contract in [`AGENTS.md SS.1–SS.3`](../AGENTS.md#session-setup) remains canonical."

D.7 forbids **SessionStart hooks only**. The Epic uses 5 D.7-compliant events: `UserPromptSubmit`, `PreToolUse`, `PostToolUse`, `Stop`, `SubagentStop`. Each carried-forward design decision in the Epic spec MUST cite D.7 compliance.

---

## Files To Create (Epic deliverable)

| Path | Purpose |
|---|---|
| `tasks/094-skill-integration-agency-default/task.md` | Epic spec — Goal / Context / Plan (4 subtasks) / AC / Out of scope / Links |
| `tasks/094-skill-integration-agency-default/readme.md` | Folder index per CLAUDE.md §7 |
| `tasks/094-skill-integration-agency-default/friction-log.md` | Stub; FL filled as subtasks land |
| `tasks/094-skill-integration-agency-default/subtasks/readme.md` | Sub-folder index |
| `tasks/094-skill-integration-agency-default/subtasks/01-root-spec-hookup.md` | ST-1 spec (root-spec citations + T3 enum + T1 typo sweep) |
| `tasks/094-skill-integration-agency-default/subtasks/02-claude-dir-and-plugin.md` | ST-2 spec (`.claude/` + `.claude-plugin/plugin.json`) |
| `tasks/094-skill-integration-agency-default/subtasks/03-event-driven-hooks.md` | ST-3 spec (5 hook scripts + settings.json wiring + governance check) |
| `tasks/094-skill-integration-agency-default/subtasks/04-cleanup-and-close.md` | ST-4 spec (final governance + flip `task_status: done`) |

Plus `tasks/readme.md` gets a new index row for 094. **No other repo files change during the planning Task** — the *execution* is what each ST-N PR ships.

---

## Templates To Reuse

- **Task structure** — copy frontmatter + section scaffold from `tasks/092-port-skill-corpora-phase-2/task.md` (Goal / Context / Plan / Todo / Acceptance Criteria (Gherkin) / Out of scope / Links).
- **Subtask file structure** — copy from `tasks/092-port-skill-corpora-phase-2/subtasks/01-triage.md` (Executor / Parallelism / Depends on / Scope / Out of scope / Acceptance Criteria / Branch + PR shape).
- **AC Gherkin pattern** — anchor IDs `T094.1.1`, `T094.1.2`, ... `T094.4.4` per Task 092's `T092.N.M` convention.
- **Friction-log per-subtask layout** — copy from `tasks/092-port-skill-corpora-phase-2/friction-log.md`.

---

## Epic Subtask Plan (encoded in `task.md ## Plan`)

### ST-1 — Root-spec hookup + T3 enum + T1 typo sweep

**Goal:** every imported skill cited in ≥ 1 root spec; SKILLS.md §3 enum ratified; T1 typos fixed.

**Files changed:**

- `CLAUDE.md §13` — expand from 7 lines to ~40, add stable anchor `SK.13.SUPERCLAUDE` + `SK.13.SUPERPOWERS`, enumerate all 52 skills grouped by `skill_kind`.
- `AGENTS.md` — new H2 section after CR.7 titled "Skill Index by Category" (~400 lines, anchors `SK.AGENTS.1.x` per category).
- `TASK.md §4.9` — inline-cite the four planning-ladder skills (`/sc:analyze`, `/sc:brainstorm`, `/sc:design`, `/sc:workflow`) with SKILL.md paths.
- `RESEARCH.md §7` — expand to enumerate research-relevant skills (`sc-research`, `sc-analyze`, `sc-deep-research-agent`).
- `SKILLS.md §3` — **T3 absorbed**: ratify expanded enum `{domain, tool, orchestrator, meta, discipline, workflow, persona, analysis, agent-template}` (9 values; Phase 2 introduced 5 new ones ad hoc).
- `tools/fm/validate.py` — add enum check `F.B.11` (ERROR) emitted when `skill_kind` is not in the ratified set.
- `tools/tests/fm/test_validate_skill_kind.py` — new test fixture validating the 9-value enum.
- `tasks/092-port-skill-corpora-phase-2/references/triage-notes/*.md` — **T1 absorbed**: sweep `superclaude_framework@v4.3.0` → `superclaude@v4.3.0` (cosmetic, ~12 files).

**AC anchors:** `T094.1.1` (zero orphan skills), `T094.1.2` (enum check fires), `T094.1.3` (T1 typos zero), `T094.1.4` (governance exits 0).

**Precedent:** Mirror Task 091 ST-2's idempotent multi-file edit pattern (cited verbatim in the Epic Context section).

### ST-2 — `.claude/` directory + plugin manifest

**Goal:** Claude Code auto-loads all imported skills at SessionStart via `.claude/skills/`; Agency is distributable as `agency@1.0.0` plugin.

**Files created:**

- `.claude/settings.json` — project-level config; declares 5 hooks (registered, scripts shipped in ST-3); declares `skillListingBudgetFraction: 0.05` (lift from default 1% to fit 52 descriptions).
- `.claude/skills/` — **symlink to `../skills/`** (Pattern A from research). On Windows, ST-2 ships a `tools/hooks/install-claude-dir.sh` that does the copy-fallback.
- `.claude/agents/` — re-export the 14 persona-kind skills (sc-system-architect, sc-backend-architect, sc-frontend-architect, sc-security-engineer, sc-quality-engineer, sc-refactoring-expert, sc-performance-engineer, sc-deep-research-agent, sc-pm-agent, sc-devops-architect, sc-learning-guide, sc-python-expert, sc-requirements-analyst, sc-root-cause-analyst, sc-self-review, sc-socratic-mentor, superpowers-code-reviewer) as `.claude/agents/<slug>.md` thin wrappers that import the canonical `skills/<slug>/SKILL.md` body. Each agent file uses Agency L2 frontmatter (`agent_source: agency`, `agent_target_agents: [claude-code]`).
- `.claude/commands/` — empty (slash commands are now skills per the platform docs; the existing `/sc:*` invocations resolve via `.claude/skills/sc-*/`).
- `.claude-plugin/plugin.json` — manifest declaring `name: "agency"`, `version: "1.0.0"`, `description: "Agency framework: 52 skills + 17 subagents + 5 hooks"`, `author`, `homepage`, `license`. Per the platform docs, this is the *only* file inside `.claude-plugin/` — `skills/`, `agents/`, `hooks/` stay at plugin root.
- `FOLDERS.md §8` — **T3 spec update**: carve `.claude/` and `.claude-plugin/` out of operational-folder topology; add Assumptions Log entries.
- `.gitignore` — ensure nothing under `.claude/` is ignored (the symlink-to-skills/ MUST be tracked so it persists).

**AC anchors:** `T094.2.1` (Claude Code discovers `.claude/skills/` and lists 52 descriptions), `T094.2.2` (`agency@1.0.0` plugin validates via `claude plugin validate --plugin-dir .`), `T094.2.3` (all 17 persona agents appear as `@<slug>`-invocable), `T094.2.4` (FOLDERS.md §8 carve-outs land).

### ST-3 — Event-driven hooks (5 hooks total)

**Goal:** 5 D.7-compliant hooks fire on Claude Code events, routing invocations through Superpowers discipline gates and emitting audit telemetry.

**Files created (under `tools/hooks/`):**

1. **`tools/hooks/user-prompt-submit.sh`** (event: `UserPromptSubmit`) — reads the prompt, runs `superpowers-using-superpowers` discipline-gate selector logic (see `skills/superpowers-using-superpowers/SKILL.md ## How to use` table), and emits a single `additionalContext` line suggesting which skill to load (e.g. "Consider `/sc:troubleshoot` or `superpowers-systematic-debugging`"). Non-blocking; `block: false`.

2. **`tools/hooks/pre-tool-use.sh`** (event: `PreToolUse`, matcher: `Skill|Agent`) — when a Skill or Agent tool is invoked: (a) verifies the skill exists in `.skills-manifest.json` (generated by `skills/skills-skill-bootstrap/sync.sh`); (b) injects `superpowers-verification-before-completion` context if the prompt contains completion-claim keywords ("done", "complete", "ready"); (c) appends to `tasks/<active-task-id>/skill-invocation-log.md` if a Task is active. Non-blocking unless skill missing.

3. **`tools/hooks/post-tool-use.sh`** (event: `PostToolUse`, matcher: `Skill|Agent`) — after a Skill/Agent invocation: (a) logs telemetry to `tasks/<active-task-id>/skill-invocation-log.md` with `tool_response` summary; (b) checks if the just-completed skill has a downstream chain (e.g. `sc-implement` → `sc-test`) per `skill_references_skills` frontmatter, and emits an `additionalContext` suggestion. Non-blocking.

4. **`tools/hooks/stop.sh`** (event: `Stop`) — enforces the AGENTS.md Closing Run Procedure (CR.1–CR.7): (a) ensures `friction-log.md` carries a `Highest Frustration Level: FL[0-3]` line; (b) reminds about `tasks/readme.md` index sync; (c) reminds about `/sc:createPR`. Returns `block: true` with stderr if FL declaration missing (escalates the session-close discipline).

5. **`tools/hooks/subagent-stop.sh`** (event: `SubagentStop`, matcher: `code-reviewer|deep-research`) — when a code-reviewer or deep-research subagent finishes: (a) routes the output through `superpowers-receiving-code-review` discipline gate (cite the technical-verification-before-action rule); (b) emits structured "Verified / Blocking / Advisory" summary header into context. Non-blocking.

**Hook config in `.claude/settings.json`** (already created in ST-2, populated in ST-3):

```json
{
  "hooks": {
    "UserPromptSubmit": [{ "matcher": "", "hooks": [{ "type": "command", "command": "tools/hooks/user-prompt-submit.sh" }] }],
    "PreToolUse": [{ "matcher": "Skill|Agent", "hooks": [{ "type": "command", "command": "tools/hooks/pre-tool-use.sh" }] }],
    "PostToolUse": [{ "matcher": "Skill|Agent", "hooks": [{ "type": "command", "command": "tools/hooks/post-tool-use.sh" }] }],
    "Stop": [{ "matcher": "", "hooks": [{ "type": "command", "command": "tools/hooks/stop.sh" }] }],
    "SubagentStop": [{ "matcher": "code-reviewer|deep-research", "hooks": [{ "type": "command", "command": "tools/hooks/subagent-stop.sh" }] }]
  }
}
```

**Governance addition:**

- `tools/check-hooks.py` — new pre-commit check verifying every script in `tools/hooks/` is registered in `.claude/settings.json` and vice versa (no orphan hooks, no orphan scripts).
- `tools/tests/test_hooks.py` — fixture-based tests using sample event payloads to verify each hook's exit code + stdout/stderr behaviour.
- `CLAUDE.md §14` — new section "Hooks" documenting the 5-event framework, the D.7 compliance, and how to author a new hook. Stable anchors `HK.14.1` through `HK.14.5` (one per hook).
- `PRE_COMMIT.md §7.A` — add `tools/check-hooks.py` row to the toolchain matrix.

**AC anchors:** `T094.3.1` (each of 5 hooks fires on its event with correct exit codes via test fixtures), `T094.3.2` (`tools/check-hooks.py` exits 0; no orphans either direction), `T094.3.3` (no hook is registered on SessionStart — D.7 enforcement), `T094.3.4` (CLAUDE.md §14 + PRE_COMMIT.md §7.A land).

### ST-4 — Cleanup + Epic close

**Goal:** final governance run; flip Epic to `done`; author Epic-level friction-log summary.

**Files changed:**

- `tasks/094-skill-integration-agency-default/task.md` — `task_status: open → done` via `tools/fm/edit.py --set`.
- `tasks/094-skill-integration-agency-default/friction-log.md` — Epic-level summary section appended.
- `tasks/readme.md` — index entry for Task 094 updated to `Status: done`.
- `skills/readme.md` — bump `updated:` and add a one-line "fully integrated into `.claude/` + plugin per Task 094" note.

**AC anchors:** `T094.4.1` (`tools/check-governance.sh` exits 0), `T094.4.2` (task_status: done flipped via fm/edit.py), `T094.4.3` (Epic friction-log present with `Highest Frustration Level: FL[0-3]`).

---

## Epic-Level Acceptance Criteria (encoded in `task.md ## Acceptance Criteria`)

```gherkin
Feature: Task 094 closes the skill-integration gap

  # anchor: BR.94.1
  Scenario: Every imported skill is cited in a root spec
    Given Task 094 is complete
    When a reader greps the root specs (AGENTS.md / CLAUDE.md / SKILLS.md / TASK.md / RESEARCH.md)
        for each skill slug under skills/sc-* and skills/superpowers-*
    Then every slug MUST produce ≥ 1 match
    And no skill MAY be cited only by example (CLAUDE.md §13 narrative aside is not a citation)

  # anchor: BR.94.2
  Scenario: Claude Code auto-discovers the skill corpus
    Given Task 094 is complete
    When a fresh Claude Code session starts in the agency repo
    Then `.claude/skills/` MUST resolve to /skills/ (symlink or copy)
    And the session log MUST show 52 skill descriptions loaded into context
    And every skill description MUST be ≤ 1536 characters (Anthropic SKILL.md cap)

  # anchor: BR.94.3
  Scenario: Agency is distributable as a plugin
    Given Task 094 is complete
    When `claude plugin validate --plugin-dir .` runs
    Then exit code MUST be 0
    And the plugin name MUST be "agency"
    And the plugin version MUST be "1.0.0"

  # anchor: BR.94.4
  Scenario: Five event-driven hooks fire correctly (D.7-compliant)
    Given Task 094 is complete
    When the test fixture in tools/tests/test_hooks.py runs each hook against its sample event payload
    Then every hook MUST exit 0 (or 2 with explicit block rationale)
    And none of the 5 hooks MAY be registered on SessionStart
    And `tools/check-hooks.py` MUST exit 0

  # anchor: BR.94.5
  Scenario: Carried-forward T3 + T1 closed
    Given Task 094 is complete
    When a reader greps SKILLS.md §3 for the skill_kind enum values
    Then the enum MUST list all 9 values: domain, tool, orchestrator, meta, discipline, workflow, persona, analysis, agent-template
    And `python3 tools/fm/validate.py skills/` MUST emit diagnostic F.B.11 ERROR on any out-of-enum value
    And `grep "superclaude_framework@v4.3.0" tasks/092-…/references/triage-notes/` MUST return zero matches
```

---

## Implementation Sequence (when executing the Epic, post-plan)

1. **Phase 1 — Plan task file authoring** (this plan):
   - Use `tools/fm/edit.py --set` to author frontmatter (`task_id: "094"`, `task_status: open`, etc.).
   - Author Goal / Context / Plan / AC sections per Task 092 template.
   - Author 4 subtask files (`subtasks/0[1-4]-*.md`) each ≤ 100 lines.
   - Add `friction-log.md` stub + `readme.md` folder index.
   - Add `tasks/readme.md` row for 094.
   - Commit: `Task 094: file Epic spec for skill-integration + .claude/ + plugin + hooks`.
   - Push + open PR per Agency's standard workflow.

2. **Phases 2–5 — Subtask PRs** (out of scope for the plan):
   - One PR per subtask (ST-1, ST-2, ST-3, ST-4), strictly sequential per the Epic Plan section.

---

## Verification

After executing this plan, the user can verify by:

1. **Plan PR ships only Task spec files** — `git diff --stat origin/main` shows ~8 new files under `tasks/094-*/` and ~5 modified lines in `tasks/readme.md`. **Zero changes** under `skills/`, `tools/`, root specs, `.claude/`, or `.claude-plugin/` — those are deferred to ST-1..ST-4 PRs.

2. **Pre-commit gate exits 0** — `tools/check-governance.sh` passes on the new Task 094 files.

3. **Frontmatter validates** — `python3 tools/fm/validate.py tasks/094-skill-integration-agency-default/` exits 0; all required L2 keys (`task_id`, `task_status`, `task_owner`, `task_priority`, `task_uses_prompts`, `task_spawns_research`, `task_spawns_prompts`, `task_affects_paths`, `task_blocked_by`) present.

4. **Index sync** — `tasks/readme.md` shows Task 094 with `Status: open`; `tools/fm/index_diff.py` exits 0.

5. **Cross-task linkage** — Task 094's `task_blocked_by` cites `["092"]` (Task 092 must be merged before this Epic starts); `task.md ## Links` cites Task 091 + Task 092 + ADR-0011 + ADR-0012.

---

## Critical Files To Reference During Execution

- **Task 092 task.md** (`tasks/092-port-skill-corpora-phase-2/task.md`) — Epic structural template.
- **Task 092 ST-1 subtask** (`tasks/092-port-skill-corpora-phase-2/subtasks/01-triage.md`) — subtask file template.
- **Task 091 ST-2 spec** (`tasks/091-port-external-skill-corpora/subtasks/02-phase-1-hookup.md`) — *the* precedent for root-spec hookup work (ST-1 of this Epic mirrors it at scale).
- **ADR-0011** (`decisions/0011-external-skill-corpora-import.md`) — D.7 constraint to cite in every subtask's Context.
- **ADR-0012** (`decisions/0012-skill-source-validator-diagnostic-codes.md`) — sets the precedent for adding new `F.B.*` diagnostic codes (this Epic adds `F.B.11`).
- **CLAUDE.md §13** — current state of the §13 "Skills" section that ST-1 expands.
- **AGENTS.md CR.7** — current state of the createPR citation that proves the hookup pattern works.
- **`skills/readme.md`** — current Phase 1 + Phase 2 skill index that ST-1 cross-references.
- **Anthropic docs**:
  - `https://docs.anthropic.com/en/docs/claude-code/skills` — Skill activation model + frontmatter.
  - `https://docs.anthropic.com/en/docs/claude-code/hooks` — Hook events + payloads (8 events listed; the 5 used by this Epic are non-SessionStart per D.7).
  - `https://docs.anthropic.com/en/docs/claude-code/plugins` — Plugin manifest schema.
  - `https://docs.anthropic.com/en/docs/claude-code/settings` — settings.json schema.

---

## Out of Scope (explicit, recorded in `task.md`)

- **Marketplace publishing** — declaring the plugin manifest is in scope; actually publishing `agency@1.0.0` to an external marketplace is a separate Task.
- **SessionStart hooks** — D.7 forbids; explicitly not added.
- **Skill body re-adaptation** — ST-2 batch B's `## Adaptations from upstream` sections already cover the D.8 rewrites; this Epic does not re-touch SKILL.md bodies.
- **PROMPT.md `prompt_relates_to_skill`** — deferred to a future Task 011 follow-up; not part of this Epic.
- **`tools/dramatica-nav/` integration** — narrative-ontology skills (NCP / novel-architect / dramatica-*) are NOT in scope; this Epic only integrates the imported `sc-*` and `superpowers-*` skills.
- **Re-syncing upstream** — ADR-0011 D.9 forbids within the snapshot's lifetime; this Epic uses the existing pins (`superclaude@v4.3.0`, `superpowers@v4.0.3`).

---

## Decisions Locked With User (Plan-mode answers)

1. **Hook granularity:** Event-driven (~5 hooks total, one per Claude Code event) — chosen for smallest surface + maximum flexibility.
2. **Epic scope:** Full implementation (4 subtasks: root-spec hookup, `.claude/` + plugin, hooks, cleanup) — mirrors Task 092 structure.
3. **Carried-forward closure:** Absorb both T3 (`skill_kind` enum) + T1 (triage-note typos) into this Epic — cleaner closure of Task 092 outstanding items.
