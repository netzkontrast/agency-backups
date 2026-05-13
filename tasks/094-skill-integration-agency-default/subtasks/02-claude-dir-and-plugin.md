---
type: note
status: active
slug: task-094-st2-claude-dir-and-plugin
summary: "ST-2 (Task 094 Epic): create the .claude/ directory (settings.json + skills/ symlink + agents/ re-exports) and the .claude-plugin/plugin.json manifest declaring agency@1.0.0. Updates FOLDERS.md §8 to carve out the new top-level dirs. CLOSED 2026-05-13 — see [02-friction-log.md](./02-friction-log.md) (FL0)."
created: 2026-05-12
updated: 2026-05-13
---

# ST-2 — `.claude/` directory + plugin manifest

**Executor:** main-agent.

**Parallelism:** Sequential after ST-1 (the SKILL.md frontmatter enum changes from ST-1 are loaded by Claude Code at SessionStart — ST-2 confirms the loader's discovery of the expanded enum works in practice).

**Depends on:** ST-1 closed `done` (enum ratified, root specs hooked up).

## Scope

### `.claude/` directory creation

- **`.claude/settings.json`** — project-level config. Declares:
  - `skillListingBudgetFraction: 0.05` (lift from Anthropic default 1% to fit 52 descriptions; per `https://docs.anthropic.com/en/docs/claude-code/settings`).
  - `hooks` block — registered as empty placeholder; ST-3 populates with the 5 event scripts.
  - `permissions` — match Agency's existing `.githooks/pre-commit` posture (Bash, Edit, Read, Write all permitted; destructive ops require confirmation).
- **`.claude/skills/`** — **symbolic link** to `../skills/`. Per the research, Pattern A from `https://docs.anthropic.com/en/docs/claude-code/skills` ("Project skills: `.claude/skills/<name>/SKILL.md` — shared via git, applies only to this project"). Symlink form preserves a single source of truth.
- **`.claude/skills-fallback/install-claude-dir.sh`** — Windows-friendly copy fallback. On platforms where Git or Claude Code do not follow symlinks, this script materialises the `.claude/skills/` content from `../skills/`. Idempotent. Not required for unix; documented as escape hatch.
- **`.claude/agents/`** — re-export 17 persona-kind skills as thin `.md` wrappers (per the [Anthropic sub-agents doc](https://docs.anthropic.com/en/docs/claude-code/sub-agents) "Project agents at `.claude/agents/`"). Each `.claude/agents/<slug>.md` is a 5-line Markdown file with `name`, `description`, and a body that says "See `skills/<slug>/SKILL.md` for the canonical body." The 17 persona-kind slugs: `sc-system-architect`, `sc-backend-architect`, `sc-frontend-architect`, `sc-security-engineer`, `sc-quality-engineer`, `sc-refactoring-expert`, `sc-performance-engineer`, `sc-deep-research-agent`, `sc-pm-agent`, `sc-devops-architect`, `sc-learning-guide`, `sc-python-expert`, `sc-requirements-analyst`, `sc-root-cause-analyst`, `sc-self-review`, `sc-socratic-mentor`, `superpowers-code-reviewer`.
- **`.claude/commands/`** — empty placeholder folder with a single `readme.md` explaining that slash commands are now skills per the platform's "commands → skills" merge (https://docs.anthropic.com/en/docs/claude-code/slash-commands). Each `/sc:<name>` resolves through `.claude/skills/sc-<name>/SKILL.md`.

### Plugin manifest

- **`.claude-plugin/plugin.json`** — declares Agency as a Claude Code plugin per `https://docs.anthropic.com/en/docs/claude-code/plugins`:
  ```json
  {
    "name": "agency",
    "version": "1.0.0",
    "description": "Agency framework: 52 imported skills + 17 sub-agents + 5 D.7-compliant event hooks + the agency governance substrate (Task / Prompt / Research / ADR layers).",
    "author": { "name": "netzkontrast/agency contributors" },
    "homepage": "https://github.com/netzkontrast/agency",
    "repository": "https://github.com/netzkontrast/agency",
    "license": "see LICENSE"
  }
  ```
- Per the platform docs, the **only file inside `.claude-plugin/` is `plugin.json`** — `skills/`, `agents/`, `hooks/` stay at the plugin root (i.e. at the Agency repo root). The directory structure satisfies this naturally: `skills/` is at repo root; `.claude/agents/` is already at repo root; `tools/hooks/` (added by ST-3) is at repo root.

### Topology spec update

- **`FOLDERS.md §8`** — extend the "Non-Operational Storage Folders" section to carve out `.claude/` and `.claude-plugin/` as harness-config folders exempt from the operational `/tasks/`-`/prompts/`-`/research/` partition rule. Add Assumptions Log entries explaining the symlink, the persona-agent re-export pattern, and the plugin manifest.

### `.gitignore` hygiene

- Ensure nothing under `.claude/` is ignored. The symlink-to-skills MUST be tracked so it persists across clones. Add an explicit `!.claude/` un-ignore line if any parent rule would have swept it.

## Out of scope

- Hooks — that is ST-3's scope. The `hooks` block in `.claude/settings.json` lands empty in ST-2 and is populated in ST-3.
- Marketplace publishing — `agency@1.0.0` is declared, not published.
- ADR-0011 D.7 — re-stated as a constraint, not modified.

## Acceptance Criteria (Gherkin)

```gherkin
Feature: ST-2 lands the .claude/ + plugin infrastructure

  # anchor: T094.2.1
  Scenario: Claude Code discovers the imported skill corpus
    Given ST-2 is complete
    When a fresh Claude Code session opens in the agency repo root
    Then `.claude/skills/` MUST resolve to /skills/ (symlink or copy fallback)
    And the session's loaded-skill listing MUST contain 52 descriptions
    And every SKILL.md description MUST be ≤ 1536 characters (Anthropic SKILL.md cap)

  # anchor: T094.2.2
  Scenario: Plugin manifest validates
    Given ST-2 is complete
    When `claude plugin validate --plugin-dir .` runs
    Then exit code MUST be 0
    And the plugin name MUST be "agency"
    And the plugin version MUST be "1.0.0"

  # anchor: T094.2.3
  Scenario: 17 persona agents are @-invocable
    Given ST-2 is complete
    When a Claude Code session lists available sub-agents
    Then every slug in the 17-persona roster (sc-system-architect, sc-backend-architect, …, superpowers-code-reviewer)
        MUST appear with the prefix `@<slug>` available
    And each `.claude/agents/<slug>.md` MUST cite the canonical SKILL.md at skills/<slug>/SKILL.md

  # anchor: T094.2.4
  Scenario: FOLDERS.md §8 carves out the new topology
    Given ST-2 is complete
    When a reader greps FOLDERS.md §8 for ".claude/" and ".claude-plugin/"
    Then both MUST be cited as carve-outs
    And both MUST be exempted from the operational-folder partition rule
```

## Branch + PR shape

Branch: `claude/task-094-st2-claude-dir-and-plugin`. PR title: `Task 094 ST-2: .claude/ directory + .claude-plugin/plugin.json + 17 agent re-exports`. PR body MUST include:

- Tree-listing of new `.claude/` + `.claude-plugin/` files.
- Confirmation that `.claude/skills/` resolves to `../skills/` (e.g. `readlink .claude/skills` output).
- Output of `claude plugin validate --plugin-dir .` (exit 0).
- Friction-log declaration.
