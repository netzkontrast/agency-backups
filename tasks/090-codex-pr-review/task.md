---
type: task
status: active
slug: codex-pr-review
summary: "Governance review of PR #110 — CODEX.md onboarding spec and Codex platform note in AGENTS.md."
created: 2026-05-12
updated: 2026-05-12
task_id: "090"
task_status: in_progress
task_owner: "claude"
task_priority: P1
task_uses_prompts: []
task_spawns_research: []
task_spawns_prompts: []
task_affects_paths:
  - CODEX.md
  - AGENTS.md
---

# Task 090 — Governance Review: PR #110 Codex Platform Spec

## Goal

Review PR #110 (`codex/init-repo-for-codex-with-root-specs`) against the repository's governance specs. The task is `done` when a documented critique exists in `notes.md` and a PR comment has been posted citing this file.

## Plan

1. Read AGENTS.md, PROMPT.md, FOLDERS.md, FRUSTRATED.md, and the Closing Run Procedure.
2. Inspect the diff (`CODEX.md` + `AGENTS.md` amendment).
3. Evaluate against CR.1–CR.7, FOLDERS.md §4, and the ADR governance rules.
4. Write findings in `notes.md` (this folder).
5. Commit `notes.md` to the PR branch (`codex/init-repo-for-codex-with-root-specs`).
6. Post a PR comment linking to `notes.md` and tagging @jules.

## Todo

- [x] 1. Bootstrap: `install.sh` + `check-governance.sh`
- [x] 2. Read relevant specs (AGENTS.md, PROMPT.md, FOLDERS.md, FRUSTRATED.md)
- [x] 3. Inspect PR diff
- [x] 4. Write findings in `notes.md`
- [ ] 5. Commit and push
- [ ] 6. Post PR comment

## Links

- PR under review: [#110](https://github.com/netzkontrast/agency/pull/110) — `codex/init-repo-for-codex-with-root-specs`
- Review findings: [`notes.md`](./notes.md)
- Governing specs: [`AGENTS.md`](../../AGENTS.md), [`FOLDERS.md`](../../FOLDERS.md), [`FRUSTRATED.md`](../../FRUSTRATED.md), [`PRE_COMMIT.md`](../../PRE_COMMIT.md)
