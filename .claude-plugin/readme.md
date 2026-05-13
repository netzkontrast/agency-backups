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

### Layout note — PR #124 Codex P2 #3

Codex flagged on PR #124 that Claude plugins, when installed via a
marketplace, may expect components in plugin-root `agents/` / `hooks/`
directories rather than the `.claude/agents/` + `tools/hooks/` layout
Agency uses. The current layout is intentional for the in-repo
operating model: `.claude/agents/` is the path Claude Code's
project-level sub-agent discovery walks (per
[sub-agents docs](https://docs.anthropic.com/en/docs/claude-code/sub-agents)),
and `tools/hooks/` is consistent with Agency's `tools/` convention
for executable scripts (see [FOLDERS.md §8](../FOLDERS.md#8-non-operational-storage-folders-explicit-exemptions)).

**Marketplace publishing is explicitly out of scope for Task 094**
(per the Epic `## Out of scope` clause). When/if Agency is published
as a downloadable plugin under a future Task, the asset-path question
will be resolved via a new ADR after running
`claude plugin validate --plugin-dir .` and `claude plugin install`
against a sandbox; if the runtime requires root-level `agents/` /
`hooks/`, the resolution will either be (a) move the assets, or
(b) add symlink wrappers from the plugin root into the canonical
in-repo paths. The current in-repo paths remain canonical until
that ADR lands.

## Assumptions Log

- The plugin version `1.0.0` is the first cut after the Task 091 +
  092 + 094 sequence; subsequent SHA-pinned re-imports of the upstream
  corpora bump the version per the standard SemVer contract.
- Marketplace publishing is **out of scope** for Task 094 — declaring
  the manifest is in scope, publishing is a separate Task.
- The plugin folder is exempt from the operational-folder partition
  per [FOLDERS.md §8](../FOLDERS.md#8-non-operational-storage-folders-explicit-exemptions).
