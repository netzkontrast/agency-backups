---
type: note
status: active
slug: triage-note-superpowers-git-worktrees
summary: "Triage note for superpowers/skills/using-git-worktrees/SKILL.md. Decision port (with D.1, D.6 reference extraction): 5.6 KB body slightly over cap; worked examples extract cleanly to references/."
created: 2026-05-12
updated: 2026-05-12
---

# Triage note — `superpowers/skills/using-git-worktrees/SKILL.md`

## Why `port` (D.1 + D.6 reference extraction)

- 5.6 KB body — marginally over the D.6 5 KB cap.
- No MCP bindings.
- Content: discipline gate for parallel-development isolation via `git worktree add`. Closely mirrors Agency's CLAUDE.md §11 "Branch & commit conventions" but adds the worktree-creation safety checks the Agency specs don't yet codify.

## Adaptation plan (ST-3)

1. **Keep the discipline gate in the body** (≤ 4 KB):
   - "When to use a worktree" trigger conditions.
   - Safety verification checklist (clean working tree, no unmerged paths, target dir does not exist).
   - Tear-down protocol.
2. **Extract worked examples** to `skills/superpowers-using-git-worktrees/references/worked-examples.md`:
   - Parallel feature-branch development.
   - Long-running review branch + main-branch hotfix in parallel.
   - Cleanup gotchas.
3. **Cross-reference** Agency's CLAUDE.md §11 in body (via Markdown link to `../../CLAUDE.md#11-branch--commit-conventions`).

## Landing folder

`skills/superpowers-using-git-worktrees/` + `references/worked-examples.md`. Tier L1 (pure git workflow; no other skill dependencies).

## Audit-graph linkage

- `skill_source: "superpowers@v4.0.3"`
- `skill_references_skills: []` — no forward edges; this is a leaf-level workflow skill.
