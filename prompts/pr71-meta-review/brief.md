---
type: note
status: active
slug: pr71-meta-review-brief
summary: "Raw brief for the meta-review of PR #71 (which itself reviewed PR #70)."
created: 2026-05-06
updated: 2026-05-06
---

# Brief — PR #71 Meta-Review

## Origin

This prompt was authored to address the absence of a formal `/prompts/` entry for the
review work committed in PR #71 (branch `claude/stoic-mendel-CjI39`, SHA `ec9109a`).

PR #71 deposited `tasks/040-superclaude-spec-evaluation/pr-review.md` — a 7-finding
governance critique of PR #70 (Tasks 032–040 spec-integration chain). No prompt was created
in `/prompts/` for that review session; the artifact was placed directly in a task subfolder
instead of in a `/research/<slug>/output/` workspace.

## Request

Perform a meta-review of PR #71:
1. Assess compliance of the review artifact (`pr-review.md`) with repo conventions
   (AGENTS.md, TASK.md, PROMPT.md, RESEARCH.md, FOLDERS.md).
2. Evaluate the content quality of the 7 findings (correctness, completeness, spec-citation
   accuracy, severity calibration).
3. Produce a structured `REVIEW.md` at the canonical location
   (`research/pr71-meta-review/output/REVIEW.md`).

## Target Agent

claude-code (claude-sonnet-4-6)

## Intended Use-Case

Governance self-audit: demonstrate that the reviewing session itself must follow the same
conventions it enforces.
