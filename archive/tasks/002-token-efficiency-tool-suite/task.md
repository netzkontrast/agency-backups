---
type: task
status: archived
slug: token-efficiency-tool-suite
summary: "Research public GitHub repos that address token efficiency via mandatory tool calling; synthesise findings into a spec for a Token Efficiency Tool Suite for this repository."
created: 2026-05-04
updated: 2026-05-12
task_id: "002"
task_status: archived
task_owner: "jules"
task_priority: P1
task_uses_prompts:
  - token-efficiency-tool-suite
task_spawns_research:
  - token-efficiency-tool-suite
task_spawns_prompts: []
task_affects_paths:
  - research/token-efficiency-tool-suite/
  - prompts/token-efficiency-tool-suite/
  - tasks/002-token-efficiency-tool-suite/
---

# Task 002 — Token Efficiency Tool Suite Research

## Goal

Survey public GitHub repositories that address **token efficiency via mandatory tool calling** — meaning architectures, libraries, or frameworks where agents are forced (not merely encouraged) to invoke tools rather than generating answers from context alone. Synthesise the findings into a formal **Token Efficiency Tool Suite Specification** for this repository: a set of tools, hooks, and conventions that enforce token-efficient navigation and action patterns in all agents operating here. The task is done when `research/token-efficiency-tool-suite/output/SPEC.md` exists, passes the pre-commit checks defined in `RESEARCH.md`, and constitutes an actionable spec from which a future Task can implement the described tool suite.

## Plan

1. **Ensure prompt exists.** Confirm `/prompts/token-efficiency-tool-suite/prompt.md` is present, well-formed, and carries valid L1+L2 frontmatter. If it does not exist, author it per `PROMPT.md` before proceeding.
2. **Initialize research workspace.** Create `/research/token-efficiency-tool-suite/` with the four canonical subdirectories (`workspace/`, `synthesis/`, `reflection/`, `output/`) per `RESEARCH.md §2`.
3. **Snapshot the prompt.** Copy the prompt body into `/research/token-efficiency-tool-suite/prompt.md` as the immutable run-start snapshot.
4. **Execute the research.** Follow the RISEN+ReAct steps in the prompt: search GitHub for repos using query axes defined there (mandatory tool calling, token budget enforcement, context-window compression, structured output coercion), collect evidence, and log findings in `workspace/session.log`.
5. **Synthesis pass.** Populate `/synthesis/` with `methodology.md`, `tracks.md`, `state.md`, and `post-synthesis-log.md`. Apply M01 (Falsification), M06 (First Principles), M07 (Contradiction Log), M13 (Adversarial Query Expansion) at minimum.
6. **Reflection pass.** Write reflection files in `/reflection/` (kickoff, midrun, post-query, pre-synthesis, post-synthesis). Log friction in `friction-log.md`.
7. **Draft the spec.** Write `output/SPEC.md` structured as:
   - Executive Summary
   - Landscape Map (surveyed repos, classification, relevance score)
   - Design Hypotheses (H1…Hn) for the tool suite
   - Surviving Architecture (justified by evidence)
   - Normative Spec (RFC 2119 clauses, Gherkin acceptance criteria)
   - Open Questions Surfaced (routed to `/prompts/` per `RESEARCH.md §4.9`)
8. **Pre-commit verification.** Run all checks from `RESEARCH.md §5`. Ensure every open question is filed as a follow-up prompt.
9. **Update this task.** Set `task_status: done`, update `updated`, confirm `task_spawns_research` lists the research slug, write `friction-log.md`.

## Todo

- [x] 1. Verify `/prompts/token-efficiency-tool-suite/prompt.md` exists and is valid.
- [x] 2. Initialize `/research/token-efficiency-tool-suite/` workspace.
- [x] 3. Snapshot prompt into `/research/token-efficiency-tool-suite/prompt.md`.
- [x] 4. Execute research — search GitHub, collect repos, log findings in `workspace/session.log`.
- [x] 5. Complete synthesis pass (methodology, tracks, state, post-synthesis-log).
- [x] 6. Complete reflection pass (all milestone reflections + friction-log).
- [x] 7. Draft `output/SPEC.md` with all required sections.
- [x] 8. Run RESEARCH.md §5 pre-commit checks; fix all failures.
- [x] 9. File any open questions as follow-up prompts under `/prompts/`.
- [x] 10. Set `task_status: done`, update `updated`, write `friction-log.md`.

## Links

- Executing prompt: [`/prompts/token-efficiency-tool-suite/prompt.md`](../../prompts/token-efficiency-tool-suite/prompt.md)
- Spawned research workspace: [`/research/token-efficiency-tool-suite/`](../../research/token-efficiency-tool-suite/) *(to be created during execution)*
- Language spec: [`/maintenance/language-spec.md`](../../maintenance/language-spec.md)
- Governing specs: [`TASK.md`](../../TASK.md), [`PROMPT.md`](../../PROMPT.md), [`RESEARCH.md`](../../RESEARCH.md), [`FOLDERS.md`](../../FOLDERS.md)

## Frustration Log
- Highest Friction Level: FL1
- Summary: The initial strict exact-match searches on GitHub returned 0 results. Had to loosen the query operators to find relevant examples. Ensure tasks are flexible about the specific terminology used by the community.
