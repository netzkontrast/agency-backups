# .claude/commands/ — placeholder

Authored by Task 094 ST-2. This folder is intentionally empty.

Per the Claude Code platform's "commands → skills" merge
(see https://docs.anthropic.com/en/docs/claude-code/slash-commands),
every `/sc:<name>` slash command resolves through its corresponding
skill at `.claude/skills/sc-<name>/SKILL.md` (via the symlink to
the repo-root `skills/` corpus).

If you ever need a project-only command that is *not* backed by a
versioned skill, add the `.md` file here. The cataloged Agency
surface uses skills exclusively, so this folder stays empty by design.
