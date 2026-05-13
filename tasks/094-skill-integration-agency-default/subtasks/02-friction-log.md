---
type: note
status: active
slug: task-094-st2-friction-log
summary: "Friction log for Task 094 ST-2 (.claude/ directory + .claude-plugin/plugin.json). Single-pass implementation; PR #124 Codex review surfaced three confident small fixes (sc-pm-agent routing, fallback prune-delete, dirty-tree note) + two deferred architectural questions (embed-body vs thin-wrapper, plugin component path resolution). Highest Frustration Level: FL1."
created: 2026-05-13
updated: 2026-05-13
---

# Task 094 ST-2 — Friction Log

Highest Frustration Level: FL1 (Codex PR review surfaced one routing violation; resolved in a follow-up commit)

## What landed

- `.claude/settings.json` — project config with `skillListingBudgetFraction: 0.05`, an intentionally empty `hooks: {}` block (ST-3 surface), and a permissions allowlist matching the existing `.githooks/pre-commit` posture.
- `.claude/skills` → `../skills/` — relative symlink so Claude Code's project-level skill discovery walks the repo-root `skills/` corpus. Verified by `readlink .claude/skills` (`../skills`) and by the live session's auto-loaded skill listing (54 imported entries surfaced after the symlink landed).
- `.claude/agents/<slug>.md` × 16 — thin Markdown re-exports for the persona roster + `superpowers-code-reviewer`. `sc-pm-agent` was initially included per the subtask spec but removed in the PR #124 review-fix commit because CLAUDE.md §13.1 marks it `skill_kind: meta` with `/sc:pm`-only routing; re-exporting it as `@sc-pm-agent` bypasses the orchestrator-routing constraint. Bodies cite `skills/<slug>/SKILL.md` rather than duplicating to avoid drift against SHA-pinned upstreams (ADR-0011 D.3) — Codex P1 review questioning that pattern is deferred to a user decision (see PR thread).
- `.claude/commands/readme.md` — placeholder folder explaining the platform's commands → skills merge; deliberately empty.
- `.claude/skills-fallback/install-claude-dir.sh` — idempotent copy-tree materialiser for symlink-less platforms (Windows / `core.symlinks=false`). Refuses to clobber an existing valid symlink.
- `.claude/readme.md` + `.claude/agents/readme.md` + `.claude-plugin/readme.md` — folder indexes with Assumptions Log entries.
- `.claude-plugin/plugin.json` — declares `agency@1.0.0` (name, version, description, author, homepage, repository, license). The folder contains only `plugin.json` + the readme, per Anthropic's plugin docs.
- `FOLDERS.md §8` — extended the Non-Operational Storage Folders table with `.claude/` and `.claude-plugin/`; `Anti-Patterns §7` exemption list mirrors the addition. `updated:` bumped to 2026-05-13.
- `.gitignore` — added a comment explaining why `.claude/` is tracked; only `.claude/worktrees/` remains ignored.
- `tools/check-clean-working-directory.py` + `PRE_COMMIT.md §1 PC.1.1` — extended the exempt prefix list with `.claude/` and `.claude-plugin/` so the `skills-fallback/install-claude-dir.sh` materialiser is a legitimate asset, not a script-scratchpad violation. T1 mechanical change paired with the FOLDERS.md §8 carve-out (single commit per the dual-surface drift rule).

## What went smoothly

- The `.claude/skills` symlink resolved at SessionStart on the first try; the live session's loaded-skill listing grew from a stable 14 (in-repo non-imported) to ≥ 54 (in-repo + imported) the moment the symlink landed, confirming T094.2.1 in practice rather than via a fixture.
- The 16 persona re-exports were generated from each canonical `SKILL.md`'s frontmatter via a single Python loop; no manual transcription required. (Initial run produced 17 wrappers including `sc-pm-agent`; the Codex P2 review caught the routing-constraint violation and the wrapper was deleted in the review-fix commit.)
- The plugin manifest schema is small enough that the Anthropic plugin docs were sufficient; no spec-mode questions surfaced.

## What needed mid-flight adjustment

- **PC.1.1 false positive** — The first governance pass flagged `.claude/skills-fallback/install-claude-dir.sh` as a script-scratchpad. The fix was mechanical: extend `tools/check-clean-working-directory.py`'s `_EXEMPT_DIR_PREFIXES` (and the matching `PRE_COMMIT.md §1` enumeration) with `.claude/` and `.claude-plugin/`. The carve-out is consistent with the new FOLDERS.md §8 entries that this subtask itself adds, so the spec → linter → spec cascade landed in one commit rather than spread across files.

## Open follow-ups for downstream subtasks

- **ST-3** will populate the empty `hooks: {}` block in `.claude/settings.json` with the five D.7-compliant event hooks (`UserPromptSubmit`, `PreToolUse`, `PostToolUse`, `Stop`, `SubagentStop`). The placeholder shape (`"hooks": {}`) is the contract ST-3 expects.
- **ST-3** will also author `tools/check-hooks.py` and the test fixtures.
- **`claude plugin validate --plugin-dir .`** (Epic AC BR.94.3) was not executed in this subtask because the `claude` CLI is not installed in the agent's sandbox. The manifest's syntactic shape was validated by `python3 -c "import json; json.load(open('.claude-plugin/plugin.json'))"`; the full validate-CLI run is deferred to ST-4's final governance pass.

## Highest Frustration Level: FL1

The initial implementation pass was clean (FL0 baseline). The Codex PR review on #124 surfaced five comments; three were confident small fixes (sc-pm-agent routing violation, fallback `cp -R` prune-delete, dirty-working-tree note on symlink-less platforms) and were landed in a single follow-up commit. Two architectural comments (embed-persona-body vs. thin-wrapper; plugin component path resolution) were deferred to a user decision because they affect the subtask spec itself.

The sc-pm-agent slip is the only true friction event: the subtask spec at line 28 explicitly listed `sc-pm-agent` as one of the 17 persona-kind slugs, but CLAUDE.md §13.1 classifies it as `skill_kind: meta` with `/sc:pm`-only routing. The discrepancy means the source plan (`tasks/094-…/references/source-plan.md`) and the subtask spec were drifted against the root spec. Per CLAUDE.md §14 #12 ("the root spec wins"), the wrapper was deleted; the source-plan and subtask-spec drift is captured as a T1 mechanical correction in this friction log rather than chasing the planning artifacts.

FL1 designation reflects the discovery cost (one review round-trip) rather than rework volume.
