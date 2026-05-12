---
type: task
status: archived
slug: review-pr109-archive-spec
summary: "Structured governance review of PR #109 (codex/create-/archive.md-governance-specification → main). Evaluates ARCHIVE.md for spec-language compliance, governance-graph completeness, and mechanical enforceability. Produces review.md with categorised findings."
created: 2026-05-12
updated: 2026-05-12
task_id: "090"
task_status: archived
task_owner: "claude-sonnet-4-6"
task_priority: P1
task_uses_prompts: []
task_spawns_research: []
task_spawns_prompts: []
task_affects_paths:
  - tasks/090-review-pr109-archive-spec/review.md
  - tasks/090-review-pr109-archive-spec/readme.md
  - tasks/090-review-pr109-archive-spec/task.md
---

# Task 090 — Review PR #109: ARCHIVE.md Governance Spec

## Goal

Produce a structured, evidence-based critique of PR #109
(`codex/create-/archive.md-governance-specification → main`), which introduces
`ARCHIVE.md` as a new root-level governance spec and adds a routing-table entry
to `AGENTS.md`. The review is done when `review.md` exists in this folder with
actionable findings categorised by severity, and a GitHub comment on PR #109
cites the findings and links to the file.

## Plan

1. Read `AGENTS.md`, `TASK.md`, `PROMPT.md`, `FOLDERS.md`, `CLAUDE.md` to
   internalize the governance contract the PR must satisfy.
2. Inspect all files introduced or modified by the single PR commit
   (`ARCHIVE.md`, `AGENTS.md` diff).
3. Verify audit-graph completeness: Task → Prompt linkage, ADR presence.
4. Assess spec-language compliance: RFC 2119, Gherkin, language consistency.
5. Author `review.md` with Critical / Structural / Minor findings.
6. Run `tools/check-governance.sh`; confirm zero new errors from this task.
7. Commit, push to PR branch, post GitHub comment.

## Todo

- [x] 1. Read governance specs.
- [x] 2. Read ARCHIVE.md and AGENTS.md diff.
- [x] 3. Check audit-graph completeness.
- [x] 4. Assess spec-language compliance.
- [x] 5. Author review.md.
- [x] 6. Run governance checks.
- [x] 7. Commit, push, post comment.

## Links

- PR under review: [#109](https://github.com/netzkontrast/agency/pull/109)
- Review artifact: [`review.md`](./review.md)
- Codex Task: https://chatgpt.com/codex/cloud/tasks/task_e_6a030b644b208324a7e2ad7938219657
