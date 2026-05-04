---
type: task
status: active
slug: review-pr28-readme-spec
summary: "Review PR #28 (docs/readme): analyse governance compliance, identify the R.13 self-contradiction, and post a formal critique comment on the PR referencing @jules."
created: 2026-05-04
updated: 2026-05-04
task_id: "009"
task_status: in_progress
task_owner: claude-code
task_priority: P1
task_uses_prompts: []
task_spawns_research: []
task_affects_paths:
  - tasks/009-review-pr28-readme-spec/
  - tasks/009-review-pr28-readme-spec/review.md
---

# Review PR #28 — docs(readme): write detailed root README with self-update spec

## Goal

Produce a thorough, evidence-based governance review of PR #28 that identifies
compliance gaps against the repository's own specs, documents what the agent did
well, and posts the critique as a PR comment referencing @jules.

## Plan

1. Read AGENTS.md, TASK.md, PROMPT.md, RESEARCH.md, FOLDERS.md to establish the
   normative baseline.
2. Read the PR diff and PR body in full.
3. Run `tools/check-governance.sh` to confirm the pre-existing error count.
4. Identify compliance gaps (process) and content quality (substance).
5. Write the review document to `review.md` in this task folder.
6. Commit and push to branch `claude/stoic-mendel-a7wVu`.
7. Post the review as a comment on PR #28, referencing the review file and @jules.

## Todo

- [x] Read governance specs baseline
- [x] Read PR #28 diff and body
- [x] Run governance check to confirm error count
- [x] Draft review document (`review.md`)
- [ ] Commit and push
- [ ] Post PR comment referencing `review.md` and @jules

## Links

- PR under review: [#28](https://github.com/netzkontrast/agency/pull/28)
- Review document: [review.md](./review.md)
