---
type: note
status: active
slug: triage-note-skip-rationale-summary
summary: "Roll-up rationale for all 39 skip rows in the matrix, grouped by skip-class. Documents why no port was attempted so a future maintainer does not re-litigate decisions."
created: 2026-05-12
updated: 2026-05-12
---

# Triage note — Skip-rationale roll-up (39 rows)

Every `skip` decision in `triage-matrix.md` falls into one of six skip-classes. Listing them by class so future maintainers can audit at a glance whether a skip was substantive (capability already exists) or mechanical (duplicate file / D.7 violator / non-skill artefact).

## Class A — Duplicate of already-ported capability (16 rows)

The capability is already shipped in Agency under `skills/sc-*/` (Phase 1) or in a Phase 2 port row that supersedes this row.

| Row | File | Superseded by |
|---|---|---|
| 17 | `commands/agent.md` | `sc-pm-agent` + Agency Task layer |
| 18 | `commands/git.md` | Agency `Bash` tool + CLAUDE.md §11 |
| 19 | `commands/help.md` | Native `/sc:help` |
| 20 | `commands/index-repo.md` | Native `index-repo` in Phase 1 |
| 21 | `commands/pm.md` | Phase-1-ported `sc-pm-agent` |
| 22 | `commands/recommend.md` | Native `/sc:recommend` |
| 23 | `commands/sc.md` | Native `/sc:` dispatcher |
| 25 | `commands/spawn.md` | `sc-task` + Agency `Agent` tool |
| 34 | `agents/business-panel-experts.md` | `sc-business-panel/references/expert-profiles.md` |
| 35 | `agents/deep-research.md` | Phase-1-ported `sc-deep-research-agent` |
| 36 | `agents/repo-index.md` | `sc-index-repo` Phase 1 skill |
| 37 | `agents/technical-writer.md` | `sc-document` (Phase 2 port row 3) |
| 40 | `modes/MODE_Brainstorming.md` | `sc-brainstorm` (Phase 2 port row 5) |
| 41 | `modes/MODE_Business_Panel.md` | `sc-business-panel/references/sub-modes.md` |
| 42 | `modes/MODE_Token_Efficiency.md` | Existing Agency `sc-*` corpus equivalent |
| 24 | `commands/select-tool.md` | Agency is MCP-free; no tool-selection layer needed |

## Class B — Plugin mirror / duplicate snapshot copy (8 rows)

Byte-equivalent copy of a canonical source in the same snapshot.

| Row | File | Canonical source |
|---|---|---|
| 44 | `.claude/skills/confidence-check/SKILL.md` | row 43 |
| 45 | `plugins/superclaude/skills/confidence-check/SKILL.md` | row 43 |
| 46 | `skills/confidence-check/SKILL.md` | row 43 |
| 47 | `plugins/superclaude/skills/brainstorm/SKILL.md` | `commands/brainstorm.md` (row 5) |
| 48 | `plugins/superclaude/skills/deep-research/SKILL.md` | `commands/research.md` (Phase 1) |
| 49 | `plugins/superclaude/skills/pm/SKILL.md` | `agents/pm-agent.md` (Phase 1) |
| 50 | `plugins/superclaude/skills/token-efficiency/SKILL.md` | `modes/MODE_Token_Efficiency.md` (row 42) |
| 51 | `plugins/superclaude/skills/troubleshoot/SKILL.md` | `commands/troubleshoot.md` (row 26) |

## Class C — D.7 SessionStart-injection prohibited (3 rows)

See dedicated note [`superpowers-hooks-skip.md`](./superpowers-hooks-skip.md).

| Row | File |
|---|---|
| 71 | `superpowers/hooks/hooks.json` |
| 72 | `superpowers/hooks/session-start.sh` |
| 73 | `superpowers/hooks/run-hook.cmd` |

## Class D — Non-skill artefact (build / lib / packaging) (4 rows)

| Row | File | What it is |
|---|---|---|
| 52 | `superclaude_framework` packaging metadata (representative) | `pyproject.toml` / `setup.py` / `MANIFEST.in` |
| 74 | `superpowers/lib/skills-core.js` | Node-based skill-loader runtime |
| 80 | `superpowers/.claude-plugin/marketplace.json` | Plugin marketplace metadata |
| 81 | `superpowers/.claude-plugin/plugin.json` | Plugin descriptor metadata |

## Class E — One-line dispatcher command (3 rows)

Single-line `<command>.md` files that simply route to a sibling SKILL.md. Agency surfaces skills via the Skill tool directly; the dispatcher layer is unnecessary.

| Row | File |
|---|---|
| 68 | `superpowers/commands/brainstorm.md` (→ `brainstorming` skill) |
| 69 | `superpowers/commands/execute-plan.md` (→ `executing-plans` skill) |
| 70 | `superpowers/commands/write-plan.md` (→ `writing-plans` skill) |

## Class F — Platform-specific or upstream-internal docs (5 rows)

| Row | File | Why skip |
|---|---|---|
| 75 | `superpowers/docs/testing.md` | Covered by Agency `sc-test` + `superpowers-tdd` port |
| 76 | `superpowers/docs/README.codex.md` | Codex-platform-specific; not Agency scope |
| 77 | `superpowers/docs/README.opencode.md` | OpenCode-platform-specific; not Agency scope |
| 78 | `superpowers/docs/plans/` | Upstream's own project planning; not skill content |
| 79 | `superpowers/docs/windows/` | Windows-platform docs; Agency is cross-platform |

## Roll-up

| Class | Count |
|---|---|
| A — duplicate-of-ported | 16 |
| B — plugin mirror | 8 |
| C — D.7 violator | 3 |
| D — non-skill artefact | 4 |
| E — dispatcher command | 3 |
| F — platform docs | 5 |
| **Total skip** | **39** |

Sum reconciles with the matrix counts summary (port=18 + adapt=24 + skip=39 = 81).
