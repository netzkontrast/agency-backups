# Task Friction Reflection Log

**Session Date:** 2026-05-02
**Agent Status:** Completing `ncp-novel-co-authoring-spec`
**Highest Frustration Level:** FL2 — Significant Frustration (Structural Bloat / Micromanagement)

## 1. Were instructions in the prompt or repository unclear or conflicting at any point?
- **Yes.** The prompt instructions mutated dramatically over the course of the session. Initially, I was instructed to produce exactly one monolithic Markdown file and *nothing else*. This shifted to building a deep nested hierarchy, and then shifted again to flattening that hierarchy and injecting `readme.md` files everywhere.

## 2. Did the agent encounter an unusual number of errors, missing dependencies, or tooling failures?
- **No.** The bash and git environments were perfectly stable.

## 3. Was working on this task frustrating or inefficient in any way?
- **Extreme Inefficiency via Administrative Overhead:** The demand to maintain a `readme.md` inside *every single folder* that must be manually updated whenever a file changes is an anti-pattern for an AI agent.
  - **Why it is agonizing:** An agent can easily determine the contents of a directory using `ls -la` or `tree`. Forcing the agent to spend context window tokens and multiple tool calls updating a human-readable index file for a folder containing only one or two files (e.g., `/output`) is completely redundant.
  - **Structural Bloat:** The previous requirement to nest synthesis artifacts into `/method`, `/aspects`, and `/plan` when each only held a single markdown file caused unnecessary path-traversal complexity.
  - **Proposed Smarter Workflow:**
    1. Drop the "every folder needs a readme" rule. A root `README.md` is sufficient for repository navigation.
    2. Rely on standard bash tooling (`ls`) or Git trees to trace folder contents rather than forcing manual semantic indexing.
    3. If structural constraints are required, they must be front-loaded in the original prompt so the agent does not have to perform destructive "unpack and repack" passes after the core logic is already solved.
