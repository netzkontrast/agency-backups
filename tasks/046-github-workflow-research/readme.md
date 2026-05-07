---
type: index
status: active
slug: github-workflow-research
summary: "Folder index for Task 046 — research and decide a GitHub Actions strategy and implement the replacement workflow."
created: 2026-05-07
updated: 2026-05-07
---

# Task 046 — GitHub Workflow Research

**What is this folder?** The Task that owns the redesign of the repository's
GitHub Actions surface. The previous `.github/workflows/adr-validate.yml` was
removed on branch `claude/update-root-readme-Qufdr`; this Task replaces it
with a *designed* workflow set backed by an ADR.

**Why is it here?** The deleted workflow was authored ad-hoc and coupled the
ADR diff gate, the pytest run, and the governance check into a single job
with broad path filters. Piecemeal MCP commits during the
`/tests/` → `/tools/tests/` relocation each fired the workflow against
half-moved trees, surfacing seven CI failures on PR #76. Rather than patch
the symptoms, this Task pauses and re-derives the CI strategy from the gates
the repo actually needs to enforce — then writes an ADR, then a workflow.

## Contents

- [`task.md`](./task.md) — Goal, plan, open questions, halt condition, links.

## Assumptions Log

- The local pre-commit hook (`tools/check-governance.sh`) remains the
  authoritative gate. CI's role is to mirror it on shared infrastructure
  for PR review, not to add behaviour the hook lacks. The ADR may revisit
  this assumption.
- A research workspace (`/research/github-actions-strategy/`) will be
  spawned by this Task once it transitions to `in_progress`. The empty
  `task_spawns_research: []` in frontmatter will be updated then.
- The replacement workflow(s) will not land on this branch
  (`claude/update-root-readme-Qufdr`) — that branch is reserved for the
  README coherence work plus the relocation. Task 046 belongs on its own
  branch (suggested: `claude/task-046-github-workflow-research`).
