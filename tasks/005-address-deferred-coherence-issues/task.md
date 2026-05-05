---
type: task
status: active
slug: address-deferred-coherence-issues
summary: "Found by coherence check 2026-05-04: 148 T1/T2 Issues deferred — too large for atomic commit."
created: 2026-05-04
updated: 2026-05-05
task_id: "005"
task_status: updated
task_owner: "claude-code"
task_priority: P3
task_uses_prompts: []
task_spawns_research: []
task_spawns_prompts: []
task_superseded_by:
  - "021"
task_affects_paths: []
---

# Task 005 — Address Deferred Coherence Issues

## Goal
The coherence check run on 2026-05-04 encountered 148 files missing L1/L2 frontmatter stubs. These files were deeply nested operational files (primarily older research and sub-files). To prevent a massive git diff, the T1/T2 stubs were skipped.

## Plan
1. Systematically batch-update these missing stubs.
2. Ensure they meet frontmatter requirements.

## Todo
- [ ] Generate frontmatter stubs for all 148 files listed in run-log 2026-05-04.

## Links
- Found by: coherence check run `maintenance/run-log.md` entry 2026-05-04
