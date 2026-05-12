---
type: index
status: active
slug: task-094-skill-integration-agency-default
summary: "Folder index for Task 094 (Skill Integration & Agency Default Surface Epic). Closes the integration gap between the 52 imported skills and Agency's default operating surface via root-spec citations, .claude/ directory, plugin manifest, and 5 D.7-compliant event-driven hooks."
created: 2026-05-12
updated: 2026-05-12
---

# Task 094 — Skill Integration & Agency Default Surface

**What:** Epic Task that integrates the 52 imported skills (39 `sc-*` + 13 `superpowers-*` shipped by Tasks 091 + 092) into Agency's default operating surface so Claude Code "uses and knows them on default" — via four layered mechanisms:

1. **Root-spec citations** (ST-1) — every orphan skill cited in ≥ 1 root spec (CLAUDE.md / AGENTS.md / SKILLS.md / TASK.md / RESEARCH.md).
2. **`.claude/` directory** (ST-2) — `settings.json` + `skills/` symlink + `agents/` re-exports so Claude Code auto-discovers the corpus at SessionStart.
3. **Plugin manifest** (ST-2) — `.claude-plugin/plugin.json` declaring `agency@1.0.0` for marketplace-ready distribution.
4. **5 D.7-compliant event-driven hooks** (ST-3) — under `tools/hooks/`, registered in `.claude/settings.json`, with governance check + test fixtures + CLAUDE.md §14 documentation.

Plus carried-forward closure of two Task 092 follow-ups (T3 `skill_kind` enum ratification; T1 triage-note typo sweep).

**Why here:** Tasks 091 + 092 ported the skill corpus but left them as inert content. This Epic wires them into Claude Code's surface — without violating ADR-0011 D.7 (which forbids SessionStart-injection hooks specifically).

## Files

- [`task.md`](./task.md) — Epic spec (Goal, Context, Plan, Acceptance Criteria, Out of scope, Links).
- [`subtasks/`](./subtasks/) — four sequential subtask files (ST-1 through ST-4).
- [`friction-log.md`](./friction-log.md) — per-subtask FL declarations + Epic-level summary (authored in ST-4).

## Source plan

This Epic was authored from the planning artifact at [`/root/.claude/plans/now-please-look-at-greedy-cascade.md`](/root/.claude/plans/now-please-look-at-greedy-cascade.md) (Claude-Code Plan-mode output; user-locked decisions at the bottom of the plan). The plan is reproduced near-verbatim in this Task's `task.md ## Goal` + `## Context` + `## Plan` sections.

## Dependencies

- **Blocked by:** Task 092 (Phase 2 corpora port) closed `done` per `task_blocked_by: ["092"]` in `task.md` frontmatter.
- **Related ADRs:** [ADR-0011](../../decisions/0011-external-skill-corpora-import.md) (D.7 SessionStart prohibition; D.8 MCP-free adaptation) + [ADR-0012](../../decisions/0012-skill-source-validator-diagnostic-codes.md) (precedent for adding new `F.B.*` diagnostic codes).
- **Precedent:** [Task 091 ST-2 — Phase 1 hookup](../091-port-external-skill-corpora/subtasks/02-phase-1-hookup.md) (the canonical idiom for citing imported skills from root specs).

## Assumptions Log

- The 52-skill count comes from `skills/sc-*` + `skills/superpowers-*` folders as of 2026-05-12 (post Task 092 closure). Future ports under the same vendor prefixes will need to be added to ST-1's enumeration; the AC at `BR.94.1` is parameterised over the actual corpus state at PR merge time.
- The `.claude/skills/` symlink may not work on Windows; ST-2 ships a copy-fallback script as the escape hatch. On unix/macOS the symlink is preferred (single source of truth, no drift).
- ADR-0011 D.7's "no SessionStart injection" rule is interpreted as: `SessionStart` hook event is forbidden; all other hook events (`UserPromptSubmit`, `PreToolUse`, `PostToolUse`, `Stop`, `SubagentStop`, etc.) are permitted. This interpretation is documented in the source plan and re-asserted in ST-3.
- The expanded `skill_kind` enum to 9 values (T3 absorbed into ST-1) is conservative: it ratifies values already in use in shipped SKILL.md files. If a future port surfaces a novel `skill_kind` value, ST-1's validator check `F.B.11` will catch it as an ERROR until the value is ratified in `SKILLS.md §3`.
