---
type: index
status: active
slug: 010-skills-frontmatter-index-suite
summary: "Index for Task 010 — design and implement a token-efficient frontmatter index + skills tool suite for cross-agent navigation."
created: 2026-05-04
updated: 2026-05-04
---

# Task 010 — Skills Tool Suite & Frontmatter Index

## What and Why

This folder coordinates the build of the indexer + query CLI + skill manifest tooling that operationalizes the proposed `SKILLS.md §B.5` ("agents MUST query the manifest before opening any SKILL.md body"). It is the first concrete implementation tranche of the `token-efficiency-tool-suite` SPEC produced by Task 002.

## Linked Navigation

- [`task.md`](./task.md) — Goal, Plan, Todo, Links.
- Executing prompt: [`/prompts/skills-frontmatter-index-suite/prompt.md`](../../prompts/skills-frontmatter-index-suite/prompt.md).
- Sibling tasks: [`../009-author-skills-root-spec/`](../009-author-skills-root-spec/), [`../011-skills-frontmatter-schema-files/`](../011-skills-frontmatter-schema-files/).
- Source SPEC: [`../../research/token-efficiency-tool-suite/output/SPEC.md`](../../research/token-efficiency-tool-suite/output/SPEC.md).

## Assumptions Log

- We assume the index lives at `.agent_cache/frontmatter-index.json` per `TASK.md §3.4`'s rule that L3 metadata is sidecar, not frontmatter. If a future agent decides L3 should be checked into git rather than gitignored, this assumption needs revisiting alongside `.gitignore`.
- We assume the index rebuild on pre-commit is fast enough not to dominate commit latency (target: < 500 ms on the current 600-file tree). If profiling shows otherwise, the gate becomes "rebuild on push, not on commit" and the spec is amended accordingly.
- We assume Jules/Gemini integration requires no special adapter beyond the JSON file: both can read JSON from a known path. If a Jules harness later forbids filesystem reads of dotfiles, the index path is moved to a non-dot location (open question logged here).
