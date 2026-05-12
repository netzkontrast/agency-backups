---
name: superpowers-using-git-worktrees
description: >-
  Create isolated git worktrees with safety verification. Use when running multiple Claude Code sessions in parallel on the same repo to avoid branch-switching conflicts.
skill_kind: workflow
skill_target_agents: [claude-code]
skill_references_skills: []
skill_references_research: []
skill_references_prompts: []
skill_bootstrap_required: false
skill_source: "superpowers@v4.0.3"
---

# superpowers-using-git-worktrees (imported from Superpowers v4.0.3)

## What

Imported git-worktree workflow from the Superpowers corpus. Provides the safety verification + creation + tear-down protocol for `git worktree add` so parallel agents (or parallel human sessions) can work on different branches of the same repo without state corruption.

## When to use

Fire when the user wants to run two or more Claude Code sessions on the same repository simultaneously, each on a different branch — the classic case where naive `git checkout` between sessions would clobber state.

## How to use

1. **Safety precheck** — confirm: clean working tree (`git status` empty), no unmerged paths, target worktree directory does not already exist.
2. **Create** the worktree: `git worktree add <path> <branch>` (or `-b <new-branch>` for a new branch).
3. **Open** the new worktree in the parallel Claude Code session; the agent reads it as a fresh repo root.
4. **Tear down** when done: `git worktree remove <path>` (or `--force` only after confirming no unique work is held there).

Full behavioural specification + worked examples at `references/upstream-superpowers-using-git-worktrees.md`.

## References

- Upstream verbatim mirror: [`references/upstream-superpowers-using-git-worktrees.md`](./references/upstream-superpowers-using-git-worktrees.md) (Superpowers `skills/using-git-worktrees/SKILL.md` @ SHA `b9e16498`, v4.0.3).
- Agency anchor: [CLAUDE.md §11 — Branch & commit conventions](../../CLAUDE.md#11-branch--commit-conventions).
- Import policy: [`decisions/0011-external-skill-corpora-import.md`](../../decisions/0011-external-skill-corpora-import.md).

## Compatibility

- Target agent: `claude-code`.
- No MCP bindings; Agency-native tools only.
- Known limitation: one-shot snapshot at Superpowers `v4.0.3` — re-syncs require a new Task per ADR-0011 D.9.
