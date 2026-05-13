---
type: note
status: active
slug: task-094-st2-friction-log
summary: "Friction log for Task 094 ST-2 (.claude/ directory + .claude-plugin/plugin.json). Single-pass implementation; no rework; T1 governance carve-out for the PC.1.1 exempt prefix list was the only mid-flight adjustment. Highest Frustration Level: FL0."
created: 2026-05-13
updated: 2026-05-13
---

# Task 094 ST-2 — Friction Log

Highest Frustration Level: FL0

## What landed

- `.claude/settings.json` — project config with `skillListingBudgetFraction: 0.05`, an intentionally empty `hooks: {}` block (ST-3 surface), and a permissions allowlist matching the existing `.githooks/pre-commit` posture.
- `.claude/skills` → `../skills/` — relative symlink so Claude Code's project-level skill discovery walks the repo-root `skills/` corpus. Verified by `readlink .claude/skills` (`../skills`) and by the live session's auto-loaded skill listing (54 imported entries surfaced after the symlink landed).
- `.claude/agents/<slug>.md` × 17 — thin Markdown re-exports for the persona roster + `superpowers-code-reviewer`. Bodies cite `skills/<slug>/SKILL.md` rather than duplicating to avoid drift against SHA-pinned upstreams (ADR-0011 D.3).
- `.claude/commands/readme.md` — placeholder folder explaining the platform's commands → skills merge; deliberately empty.
- `.claude/skills-fallback/install-claude-dir.sh` — idempotent copy-tree materialiser for symlink-less platforms (Windows / `core.symlinks=false`). Refuses to clobber an existing valid symlink.
- `.claude/readme.md` + `.claude/agents/readme.md` + `.claude-plugin/readme.md` — folder indexes with Assumptions Log entries.
- `.claude-plugin/plugin.json` — declares `agency@1.0.0` (name, version, description, author, homepage, repository, license). The folder contains only `plugin.json` + the readme, per Anthropic's plugin docs.
- `FOLDERS.md §8` — extended the Non-Operational Storage Folders table with `.claude/` and `.claude-plugin/`; `Anti-Patterns §7` exemption list mirrors the addition. `updated:` bumped to 2026-05-13.
- `.gitignore` — added a comment explaining why `.claude/` is tracked; only `.claude/worktrees/` remains ignored.
- `tools/check-clean-working-directory.py` + `PRE_COMMIT.md §1 PC.1.1` — extended the exempt prefix list with `.claude/` and `.claude-plugin/` so the `skills-fallback/install-claude-dir.sh` materialiser is a legitimate asset, not a script-scratchpad violation. T1 mechanical change paired with the FOLDERS.md §8 carve-out (single commit per the dual-surface drift rule).

## What went smoothly

- The `.claude/skills` symlink resolved at SessionStart on the first try; the live session's loaded-skill listing grew from a stable 14 (in-repo non-imported) to ≥ 54 (in-repo + imported) the moment the symlink landed, confirming T094.2.1 in practice rather than via a fixture.
- The 17 persona re-exports were generated from each canonical `SKILL.md`'s frontmatter via a single Python loop; no manual transcription required.
- The plugin manifest schema is small enough that the Anthropic plugin docs were sufficient; no spec-mode questions surfaced.

## What needed mid-flight adjustment

- **PC.1.1 false positive** — The first governance pass flagged `.claude/skills-fallback/install-claude-dir.sh` as a script-scratchpad. The fix was mechanical: extend `tools/check-clean-working-directory.py`'s `_EXEMPT_DIR_PREFIXES` (and the matching `PRE_COMMIT.md §1` enumeration) with `.claude/` and `.claude-plugin/`. The carve-out is consistent with the new FOLDERS.md §8 entries that this subtask itself adds, so the spec → linter → spec cascade landed in one commit rather than spread across files.

## Open follow-ups for downstream subtasks

- **ST-3** will populate the empty `hooks: {}` block in `.claude/settings.json` with the five D.7-compliant event hooks (`UserPromptSubmit`, `PreToolUse`, `PostToolUse`, `Stop`, `SubagentStop`). The placeholder shape (`"hooks": {}`) is the contract ST-3 expects.
- **ST-3** will also author `tools/check-hooks.py` and the test fixtures.
- **`claude plugin validate --plugin-dir .`** (Epic AC BR.94.3) was not executed in this subtask because the `claude` CLI is not installed in the agent's sandbox. The manifest's syntactic shape was validated by `python3 -c "import json; json.load(open('.claude-plugin/plugin.json'))"`; the full validate-CLI run is deferred to ST-4's final governance pass.

## Highest Frustration Level: FL0

Single-pass implementation, no rework other than the mechanical PC.1.1 carve-out (which was a foreseeable consequence of adding a new exempt top-level folder; it landed in the same commit as the FOLDERS.md §8 entry). No spec ambiguities, no platform-doc surprises, no failed tool calls.
