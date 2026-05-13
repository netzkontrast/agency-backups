# .claude/ — Claude Code project configuration

Authored by Task 094 ST-2 ([subtask spec](../tasks/094-skill-integration-agency-default/subtasks/02-claude-dir-and-plugin.md)).
This folder is the Claude Code project-level integration surface for
Agency. It is exempt from the operational-folder partition rule per
[FOLDERS.md §8](../FOLDERS.md#8-non-operational-storage-folders-explicit-exemptions).

## Contents

- **[settings.json](./settings.json)** — project-level config. Declares
  the skill-listing budget (lifted to 5% to fit 54 imported skills) and
  a placeholder `hooks: {}` block that Task 094 ST-3 will populate with
  five D.7-compliant event hooks (`UserPromptSubmit`, `PreToolUse`,
  `PostToolUse`, `Stop`, `SubagentStop`). ADR-0011 D.7 forbids
  SessionStart-hook injection; the placeholder is intentionally empty.
- **[skills/](./skills)** — symlink to `../skills/` so Claude Code
  auto-discovers all 54 imported skill descriptions (39 `sc-*` + 15
  `superpowers-*`) plus the in-repo non-imported skills at SessionStart.
  Per https://docs.anthropic.com/en/docs/claude-code/skills the loader
  walks `.claude/skills/<name>/SKILL.md` for project-scoped skills.
- **[agents/](./agents)** — 17 thin Markdown wrappers re-exporting
  `skill_kind: persona` (and the single `agent-template`
  `superpowers-code-reviewer`) so each appears as `@<slug>`-invocable
  per https://docs.anthropic.com/en/docs/claude-code/sub-agents.
- **[commands/](./commands)** — placeholder folder; all slash commands
  resolve through the symlinked `skills/sc-<name>/SKILL.md` corpus per
  the platform's commands → skills merge.
- **[skills-fallback/](./skills-fallback)** — `install-claude-dir.sh`,
  a copy-tree materialiser for platforms that do not follow Git
  symlinks. Idempotent. Documented escape hatch only; on unix the
  symlink at `.claude/skills` is the canonical path.

The plugin manifest lives one folder up at
[`.claude-plugin/plugin.json`](../.claude-plugin/plugin.json); per
https://docs.anthropic.com/en/docs/claude-code/plugins the *only* file
inside `.claude-plugin/` is `plugin.json` — every other plugin asset
(skills/, agents/, hooks/) stays at the plugin root (= this repo root).

## Assumptions Log

- The repository is cloned with `core.symlinks=true` (the unix default).
  On Windows / configurations with `core.symlinks=false`, the symlink
  at `.claude/skills` will appear as a plain text file containing the
  string `../skills`. Operators on those platforms MUST run
  `bash .claude/skills-fallback/install-claude-dir.sh` once to
  materialise a copy-tree mirror.
- Claude Code's project-level skill discovery walks `.claude/skills/`
  (per https://docs.anthropic.com/en/docs/claude-code/skills). The
  symlink target is `../skills/` (relative), so the discovery works
  regardless of the absolute path the repo is cloned into.
- The `hooks` block in `settings.json` is intentionally empty. Task 094
  ST-3 will populate it with five D.7-compliant event hooks. ADR-0011
  D.7 forbids SessionStart injection; no SessionStart hook will ever
  appear here.
- The persona-agent re-exports under `agents/` deliberately do **not**
  duplicate the canonical `SKILL.md` body — they re-export by reference
  so re-syncing the upstream corpus does not require re-touching the
  wrappers.
