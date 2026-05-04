---
type: note
status: active
slug: skills-navigation-bootstrap-friction-log
summary: "FL1 — minor friction from a duplicate task slot at index 006 and three pre-existing structural lint errors blocking the global governance check."
created: 2026-05-04
updated: 2026-05-04
---

# Friction Log — skills-navigation-bootstrap

**Highest Frustration Level: FL1**

## Summary

The run completed end-to-end. Two minor friction points are worth surfacing for future sessions, both per `FRUSTRATED.md` FL1.

## FL1.1 — Duplicate Task ID at slot 006

`/tasks/` contains two folders both carrying `task_id: "006"`:

- `tasks/006-skills-navigation-bootstrap/` (this run)
- `tasks/006-surface-skills-architecture/`

`/tasks/readme.md` lists only the second; the first is unlinked. `tools/lint-linkage.py` did not catch the collision because both `task_id` values are merely strings, not folder-derived. The branch name `claude/run-task-006-vGA6Y` is the only signal the agent has to disambiguate, and it points at this folder by default because it was the most recently created.

**Recommendation (Task 008 candidate):** extend `tools/check-governance.sh` to enforce uniqueness of `task_id` across `/tasks/`. Renumbering one of the two is per `TASK.md` §8.1 the responsibility of whichever agent commits second; in this case the prior commit (PR #30) created the duplicate, so the renumber falls on Task 005 / 008 maintenance, not on this run.

## FL1.2 — Pre-existing Structural Lint Errors

`tools/check-governance.sh --no-trust` reports six errors before any change in this run:

```
ERROR prompts/claude-ai-container-git-verification: missing required brief.md
ERROR prompts/claude-ai-container-git-verification: missing required readme.md
ERROR prompts/skills-skill-container-capabilities: missing required brief.md
ERROR prompts/skills-skill-container-capabilities: missing required readme.md
ERROR prompts/skills-skill-enterprise-offline: missing required brief.md
ERROR prompts/skills-skill-enterprise-offline: missing required readme.md
```

These prompts shipped without their L1 readme/brief stubs in earlier merges (`3c75d55` and adjacent commits). Per `MAINTENANCE.md` §1 these are T1 mechanical fixes (missing required readme/brief stubs). Because the same spec's `MAINTENANCE.md` §1 explicitly authorises T1 fixes "in-place", and because the global gate in `tools/check-governance.sh` blocks `/sc:createPR` until they are fixed, I performed the T1 fix during this run: minimal `brief.md` + `readme.md` stubs were written for each of the three prompts, citing the source question they answer. `task_affects_paths` was extended accordingly. Post-fix, `check-governance.sh --no-trust` returns `PASS: all governance checks passed.`

**Recommendation (still valid for Task 008):** the absence is a *symptom* of the structure linter not running pre-merge on the contributing branches. Task 008 (coherence baseline hardening) should add a CI gate or branch-protection rule so these don't recur silently.

## FL1.3 — Pre-existing Hooks Not Installed

`.git/hooks/pre-commit` is absent; `git config core.hooksPath` is empty. Per `tools/install-hooks.sh` the hook is opt-in. This means agents who skip `install-hooks.sh` can bypass the governance gate, with `/sc:createPR` being the only catch. Recorded for situational awareness; no action taken in this run.

## What Went Right (Process)

- The frontmatter ontology (`TASK.md` §3) and the `research/` template were sufficient to author every artifact without reinventing structure.
- The pre-existing `research/skills-skill-architecture/` provided a near-complete model for the bootstrap layer; this run did not need to reauthor it.
- Filing follow-up prompts (`skills-namespace-ontology`, `skills-manifest-emission-tool`) was a clean way to keep the SPEC.md scope tight without losing implementation detail to memory.
