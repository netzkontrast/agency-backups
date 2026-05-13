---
type: task
status: active
slug: skill-integration-agency-default
summary: "Epic: Integrate the 54 imported skills (39 sc-* + 15 superpowers-*) into Agency's default operating surface — root-spec citations (every orphan skill cited), .claude/ directory + .claude-plugin/plugin.json (agency@1.0.0), 5 D.7-compliant event-driven hooks, and carried-forward closure of the Task 092 T3 (skill_kind enum) + T1 (triage-note typos) follow-ups."
created: 2026-05-12
updated: 2026-05-13
task_id: "094"
task_status: open
task_owner: "unassigned"
task_priority: P2
task_uses_prompts: []
task_spawns_research: []
task_spawns_prompts: []
task_affects_paths:
  - CLAUDE.md
  - AGENTS.md
  - SKILLS.md
  - TASK.md
  - RESEARCH.md
  - FOLDERS.md
  - PRE_COMMIT.md
  - .claude/
  - .claude-plugin/
  - tools/hooks/
  - tools/fm/validate.py
  - tools/check-hooks.py
  - tools/tests/test_hooks.py
  - tasks/092-port-skill-corpora-phase-2/references/triage-notes/
task_blocked_by:
  - 092
---

# Task 094 — Skill Integration & Agency Default Surface (Epic)

## Note — Source plan

This Epic spec is the execution surface of the planning artifact archived verbatim at [`references/source-plan.md`](./references/source-plan.md) (canonical, repo-tracked). The plan was originally authored in Claude-Code Plan-mode at the ephemeral session-local path `/root/.claude/plans/now-please-look-at-greedy-cascade.md` (session `01WBrHNUZUEoew9PE9A7SguS`); the canonical record lives in this Task's `references/` folder. User-locked decisions captured at the bottom of the plan:

1. **Hook granularity:** Event-driven (~5 hooks total, one per Claude Code event).
2. **Epic scope:** Full implementation (4 sequential subtasks: root-spec hookup, `.claude/` + plugin, hooks, cleanup).
3. **Carried-forward closure:** Absorb both T3 (`skill_kind` enum ratification) and T1 (triage-note typos) into this Epic.

The plan content is reproduced verbatim as this Task's `## Goal` + `## Context` + `## Plan` + `## Acceptance Criteria` below; subtask files at [`subtasks/01..04-*.md`](./subtasks/) implement the per-subtask scope.

## Goal

After closing Task 092 (Phase 2 skill-corpora port), Agency hosts **52 imported skills** under `skills/sc-*` + `skills/superpowers-*` — but **47 of them have no root-spec citation**, no `.claude/` directory exists, no plugin manifest exists, and no per-skill hooks fire. The skills are inert content; Claude Code does not "know" about them on default.

This Epic closes that integration gap by layering four mechanisms:

1. **Default discoverability** — Claude Code auto-loads skill descriptions every session (`.claude/skills/` symlink → `skills/`).
2. **Reusable distribution** — Agency declares itself a plugin so the whole stack ships as `agency@1.0.0` (`.claude-plugin/plugin.json`).
3. **Spec-layer documentation** — every imported skill cited from ≥ 1 root spec so a human reader can audit the surface.
4. **Event-driven hooks** — 5 D.7-compliant hooks (one per Claude Code event) that route invocations through the relevant Superpowers discipline gates and emit audit telemetry.

Plus carried-forward closure of two Task 092 friction-log follow-ups: ratify the expanded `skill_kind` enum in `SKILLS.md §3` (T3) and fix `superclaude_framework@v4.3.0` → `superclaude@v4.3.0` typos in the triage notes (T1).

The Epic is **done** when:

1. Every imported skill is cited in ≥ 1 root spec (zero orphans).
2. `.claude/skills/` auto-loads 52 skill descriptions at SessionStart in any Claude Code session opened in this repo.
3. `claude plugin validate --plugin-dir .` exits 0 against the new `.claude-plugin/plugin.json`.
4. All 5 event-driven hooks fire correctly on their events (test fixtures pass) and the governance check `tools/check-hooks.py` exits 0.
5. SKILLS.md §3 enum lists 9 values; `tools/fm/validate.py` emits `F.B.11` ERROR on any out-of-enum `skill_kind`.
6. `grep -r "superclaude_framework@v4.3.0" tasks/092-port-skill-corpora-phase-2/references/triage-notes/` returns zero matches.

## Context

### Phase 2 closure baseline

Task 091 (Phase 1) ported 14 specific skills and hooked 2 of them (`sc-createPR` in `AGENTS.md` CR.7, `sc-research` in `RESEARCH.md §7`) into root specs. Task 092 (Phase 2) ported the remaining 38 skills (across PRs #116/#117/#118/#119/#120/#121) but **did not hook them into root specs** — that was explicitly out of scope per the Task 092 task.md "Out of scope" clause.

This Epic picks up where Task 092 stopped. The audit graph from [`tasks/092-…/references/triage-matrix.md`](../092-port-skill-corpora-phase-2/references/triage-matrix.md) (81 rows; final counts port=18, adapt=24, skip=39) is the source of truth for which skills exist; this Epic adds the citation + hook + manifest layer over the corpus.

### Critical constraint — ADR-0011 D.7

> "**D.7 No SessionStart injection.** Upstream SessionStart hooks (SuperClaude pm-agent restore, Superpowers `using-superpowers` injection) MUST NOT be ported. The Agency bootstrap contract in [`AGENTS.md SS.1–SS.3`](../AGENTS.md#session-setup) remains canonical."

D.7 forbids **SessionStart hooks only**. This Epic uses 5 D.7-compliant events: `UserPromptSubmit`, `PreToolUse`, `PostToolUse`, `Stop`, `SubagentStop`. Every subtask spec MUST cite D.7 compliance in its `## Out of scope` section.

### Three integration patterns (research distilled)

Pre-plan research enumerated three viable integration patterns; this Epic layers all three:

- **Pattern A — `.claude/` directory mirror.** Symlink `skills/` → `.claude/skills/`. Claude Code auto-discovers and loads descriptions at SessionStart. Used by ST-2.
- **Pattern B — Plugin manifest.** Declare Agency as a Claude Code plugin via `.claude-plugin/plugin.json`. Skills + agents + hooks bundle under `agency@1.0.0`. Used by ST-2.
- **Pattern C — Root-spec citation.** Document every skill in CLAUDE.md / AGENTS.md / SKILLS.md / TASK.md / RESEARCH.md so a human auditor and the LLM context-window both surface the skill names. Used by ST-1.

All three patterns are D.7-compliant (none of them use SessionStart hooks; only `UserPromptSubmit`/`PreToolUse`/`PostToolUse`/`Stop`/`SubagentStop`).

### Precedent — Task 091 ST-2 "Phase 1 hookup"

The closest precedent for the root-spec hookup work in ST-1 is Task 091 ST-2 ([`subtasks/02-phase-1-hookup.md`](../091-port-external-skill-corpora/subtasks/02-phase-1-hookup.md)), which:

1. Rewrote `AGENTS.md` CR.7 (Closing Run Procedure step 4) to cite local `skills/sc-createPR/SKILL.md` instead of the upstream GitHub URL.
2. Added `RESEARCH.md §7` (Skill-driven research runs) citing `skills/sc-research/SKILL.md` + ADR-0011 D.8 adaptation note.
3. Single-pass idempotent edits; pre-commit gate validated.

ST-1 of this Epic generalises that pattern to 52 skills.

### Carried-forward Task 092 follow-ups

The Task 092 Epic-level friction log cited two follow-ups:

- **T3 — `skill_kind` enumeration:** `SKILLS.md §3` currently defines the closed set as `{domain, tool, orchestrator, meta}`. Phase 2 introduced `discipline | workflow | persona | analysis | agent-template` ad hoc (PR #120 review A1). This Epic ratifies the 9-value enum and adds an enum check to `tools/fm/validate.py` (new diagnostic `F.B.11`).
- **T1 — triage-note typos:** Some `tasks/092-…/references/triage-notes/*.md` files cite `skill_source: "superclaude_framework@v4.3.0"`; the canonical short form is `superclaude@v4.3.0` (per ADR-0012 + the actual SKILL.md `skill_source` values shipped in PRs #117/#118). Cosmetic sweep.

## Plan (four sequential subtasks)

1. **[ST-1 — Root-spec hookup + T3 enum + T1 typo sweep](./subtasks/01-root-spec-hookup.md):** every imported skill cited in ≥ 1 root spec; `SKILLS.md §3` enum ratified to 9 values; `tools/fm/validate.py` enum check `F.B.11` added; triage-note typos fixed.
2. **[ST-2 — `.claude/` directory + plugin manifest](./subtasks/02-claude-dir-and-plugin.md):** `.claude/` directory created at repo root with `settings.json` + `skills/` symlink + `agents/` re-exports + `.claude-plugin/plugin.json` declaring `agency@1.0.0`.
3. **[ST-3 — Event-driven hooks](./subtasks/03-event-driven-hooks.md):** 5 D.7-compliant hook scripts under `tools/hooks/`, registered in `.claude/settings.json`. Governance check `tools/check-hooks.py` + test fixtures. CLAUDE.md §14 + PRE_COMMIT.md §7.A documentation.
4. **[ST-4 — Cleanup + Epic close](./subtasks/04-cleanup-and-close.md):** final `tools/check-governance.sh` exit 0; flip `task_status: open → done`; update `tasks/readme.md`; author Epic-level friction-log summary.

ST-1 → ST-2 → ST-3 → ST-4 is strictly sequential: each subtask depends on its predecessor being closed `done`. ST-1 and ST-2 MAY proceed in parallel only if their `task_affects_paths` are mechanically partitioned non-overlappingly (ST-1 touches root specs; ST-2 touches `.claude/` + `.claude-plugin/`; no path collision).

## Todo

- [ ] 1. ST-1 root-spec hookup + T3 enum ratification + T1 typo sweep PR'd and merged
- [x] 2. ST-2 `.claude/` directory + `.claude-plugin/plugin.json` PR'd and merged
- [ ] 3. ST-3 5 event-driven hooks + governance check + tests PR'd and merged
- [ ] 4. ST-4 cleanup + Epic close PR'd and merged
- [ ] 5. End-to-end governance: `tools/check-governance.sh` exits 0; `tools/check-hooks.py` exits 0
- [ ] 6. `tasks/readme.md` index entry flipped `Status: open` → `done`
- [ ] 7. Epic-level friction log authored (`friction-log.md` with `Highest Frustration Level: FL[0-3]`)

## Acceptance Criteria

Gherkin scenarios (anchored for downstream tooling). Per-subtask AC live inside each subtask file (anchors `T094.N.M`).

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
    When `readlink .claude/skills` runs (or on Windows, the copy-fallback materialiser)
    Then it MUST resolve to ../skills/
    And `find .claude/skills -maxdepth 2 -name SKILL.md | wc -l` MUST return 52
    And every SKILL.md `description` field MUST be ≤ 1536 characters (Anthropic SKILL.md cap)

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
    And `grep -r "superclaude_framework@v4.3.0" tasks/092-port-skill-corpora-phase-2/references/triage-notes/` MUST return zero matches
```

## Out of scope

- **Marketplace publishing** — declaring the plugin manifest is in scope; actually publishing `agency@1.0.0` to an external marketplace is a separate Task.
- **SessionStart hooks** — D.7 explicitly forbids; this Epic uses only `UserPromptSubmit` / `PreToolUse` / `PostToolUse` / `Stop` / `SubagentStop`.
- **Skill body re-adaptation** — ST-2 batch B's `## Adaptations from upstream` sections (Task 092 PR #118) already cover the D.8 rewrites; this Epic does NOT re-touch SKILL.md bodies.
- **PROMPT.md `prompt_relates_to_skill`** — deferred to a future Task 011 follow-up; not part of this Epic.
- **`tools/dramatica-nav/` integration** — narrative-ontology skills (NCP / novel-architect / dramatica-*) are NOT in scope; this Epic only integrates the imported `sc-*` and `superpowers-*` skills.
- **Re-syncing upstream** — ADR-0011 D.9 forbids within the snapshot's lifetime; this Epic uses the existing pins (`superclaude@v4.3.0`, `superpowers@v4.0.3`).

## Links

- **Parent Epic chain:** [Task 091 — Phase 1 corpora port](../091-port-external-skill-corpora/task.md) (`task_status: done`) → [Task 092 — Phase 2 corpora port](../092-port-skill-corpora-phase-2/task.md) (`task_status: done`) → **Task 094 — this Epic**.
- **Source ADRs:** [ADR-0011 — External Skill Corpora Import Policy](../../decisions/0011-external-skill-corpora-import.md) (esp. §D.7 SessionStart prohibition) + [ADR-0012 — Skill-source validator diagnostic codes](../../decisions/0012-skill-source-validator-diagnostic-codes.md) (precedent for new `F.B.11` enum check).
- **Phase 1 hookup precedent:** [Task 091 ST-2 spec](../091-port-external-skill-corpora/subtasks/02-phase-1-hookup.md).
- **Phase 2 closure:** [Task 092 friction-log Epic summary](../092-port-skill-corpora-phase-2/friction-log.md) — carries-forward T3 + T1 absorbed by this Epic.
- **Skill inventory:** [`skills/readme.md`](../../skills/readme.md) + [Task 092 triage matrix](../092-port-skill-corpora-phase-2/references/triage-matrix.md).
- **Source plan:** [`/root/.claude/plans/now-please-look-at-greedy-cascade.md`](/root/.claude/plans/now-please-look-at-greedy-cascade.md) (Plan-mode output; user-locked decisions at the bottom).
- **Anthropic platform docs (cited by ST-2 + ST-3):**
  - `https://docs.anthropic.com/en/docs/claude-code/skills` — SKILL.md frontmatter + activation model.
  - `https://docs.anthropic.com/en/docs/claude-code/hooks` — 8 hook events + payloads (this Epic uses 5).
  - `https://docs.anthropic.com/en/docs/claude-code/plugins` — `.claude-plugin/plugin.json` manifest schema.
  - `https://docs.anthropic.com/en/docs/claude-code/settings` — `.claude/settings.json` schema.
- **Governing root specs:** [`TASK.md`](../../TASK.md), [`SKILLS.md`](../../SKILLS.md), [`AGENTS.md`](../../AGENTS.md), [`CLAUDE.md`](../../CLAUDE.md), [`FOLDERS.md`](../../FOLDERS.md).
