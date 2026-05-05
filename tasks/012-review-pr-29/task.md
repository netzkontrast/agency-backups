---
type: task
status: active
slug: review-pr-29
summary: "Code review of PR #29 (tasks 009–011, skills governance). Produces a structured critique covering prompt engineering quality, frontmatter correctness, inter-task dependency risks, and RFC-2119 compliance."
created: 2026-05-04
updated: 2026-05-04
task_id: "012"
task_status: in_progress
task_owner: "claude-sonnet-4-6"
task_priority: P1
task_uses_prompts: []
task_spawns_research: []
task_spawns_prompts: []
task_affects_paths:
  - tasks/012-review-pr-29/notes.md
  - tasks/012-review-pr-29/readme.md
---

# Task 012 — Review PR #29: Skills Governance (Tasks 009–011)

## Goal

Produce a structured, evidence-based code-review critique of PR #29
(`claude/analyze-skills-tools-BF0wL → main`), which introduces Tasks 009, 010,
and 011 plus their executing prompts. The review is complete when a
`notes.md` exists in this folder with actionable findings keyed to specific
files and line numbers, and a GitHub PR comment has been posted that
summarises the findings and links to `notes.md`.

## Plan

1. Read `AGENTS.md`, `PROMPT.md`, `TASK.md`, `FOLDERS.md` to internalize the
   governance contract the PR is supposed to satisfy.
2. Read every new file in PR #29 (three `task.md` files, three `prompt.md` files,
   three `brief.md` files, six `readme.md` files, and the index updates).
3. Author `notes.md` in this folder with categorised findings (Critical /
   Structural / Minor).
4. Run `tools/check-governance.sh` on the branch; confirm zero new errors
   introduced by *this* review task.
5. Commit and push to `claude/stoic-mendel-ZWbh5`.
6. Post a GitHub comment on PR #29 citing the findings and linking `notes.md`.

## Todo

- [x] 1. Read governance specs.
- [x] 2. Read all PR #29 new files.
- [x] 3. Author `notes.md` with findings.
- [ ] 4. Run governance checks.
- [ ] 5. Commit and push.
- [ ] 6. Post GitHub PR comment.

## Links

- PR under review: [#29](https://github.com/netzkontrast/agency/pull/29)
- Review artifact: [`notes.md`](./notes.md)
- Reviewed tasks: [`009`](../009-author-skills-root-spec/task.md),
  [`010`](../010-skills-frontmatter-index-suite/task.md),
  [`011`](../011-skills-frontmatter-schema-files/task.md)
