# .claude-plugin/ — Agency plugin manifest

Authored by Task 094 ST-2. This folder declares Agency as a Claude Code
plugin per https://docs.anthropic.com/en/docs/claude-code/plugins.

## Contents

- **[plugin.json](./plugin.json)** — declares `agency@1.0.0` with the
  framework's name, version, description, author, homepage, repository,
  and license pointer.

Per the platform docs, **the only file inside `.claude-plugin/` is
`plugin.json`**. Every other plugin asset (`skills/`, `agents/`,
`hooks/`) stays at the plugin root, which is the Agency repo root.
Those assets are materialised by Task 094 as follows:

- `skills/` — at the repo root, mirrored into `.claude/skills/` via a
  symlink so Claude Code discovers them at SessionStart.
- `agents/` — at `.claude/agents/` (16 persona re-exports written by
  ST-2; `sc-pm-agent` deliberately excluded per CLAUDE.md §13.1
  `/sc:pm`-only routing).
- `hooks/` — at `tools/hooks/`, registered into `.claude/settings.json`
  by Task 094 ST-3.

## Assumptions Log

- The plugin version `1.0.0` is the first cut after the Task 091 +
  092 + 094 sequence; subsequent SHA-pinned re-imports of the upstream
  corpora bump the version per the standard SemVer contract.
- Marketplace publishing is **out of scope** for Task 094 — declaring
  the manifest is in scope, publishing is a separate Task.
- The plugin folder is exempt from the operational-folder partition
  per [FOLDERS.md §8](../FOLDERS.md#8-non-operational-storage-folders-explicit-exemptions).
