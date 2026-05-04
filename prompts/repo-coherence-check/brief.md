---
type: note
status: active
slug: repo-coherence-check-brief
summary: "Root cause analysis and original request that motivated the repo-coherence-check prompt."
created: 2026-05-04
updated: 2026-05-04
---

# Brief — Repo Coherence Check

## Root Cause Analysis

The Repo Coherence Check prompt was motivated by a pattern of **accumulated drift** observed in this repository:

1. **Research outputs never propagated back to governance.** Specs in `/research/*/output/SPEC.md` produced authoritative rules (Gherkin language binding, RFC 2119 conventions, the Frontmatter Ontology). None of this fed back automatically into `AGENTS.md`, `TASK.md`, or `MAINTENANCE.md`. An operator had to notice the gap and manually trigger a large clean-up task.

2. **Governance files broke their own rules.** `AGENTS.md` — the file that instructs agents to add frontmatter — had no frontmatter itself. `MAINTENANCE.md` referenced a `/todo/` directory that was never created. The coherence failure was invisible because there was no routine checking it.

3. **New files were written without language-spec awareness.** Agents writing new specs had to excavate `/research/` to find the RFC 2119 and Gherkin rules. No canonical single-source existed until `maintenance/language-spec.md` was created — also manually, after the fact.

4. **The maintenance process had no feedback loop.** `MAINTENANCE.md` described a "Nightly Maintenance Run" but provided no execution trigger, no log of past runs, and no way for the next agent to know what had already been checked.

**The pattern:** every time the repository evolved (new specs, new Tasks, merges), there was a window where the repo was subtly inconsistent. The inconsistency accumulated silently until a human operator noticed and triggered a large manual repair.

## Original Request (verbatim)

> Please think about the reasons why this current Task was needed in the First Place, and Write a new prompt that Addresses this… i want to Create a new Claude Code Routine, that Executes that specific prompt regularly — its Not a maintenance prompt per se, but should also be Referenced there… its more of a self improvement prompt — with the goal of keeping repo coherence Strictly — for that, the prompt MUST instruct the Agent to First get a Complete Overview of the last git commits… and changes since the last run… so it can then, do small things right then, and bigger things could be Addressed by writing Tasks… The prompt should also Directly link to the maintenance folder… in a way, that Tracks and Logs what it could — maybe You Need to extend and Improve MAINTENANCE.md and the folder structure for that.

## Target Agent

Claude Code (primary). Also compatible with Google Jules if the repo is connected via GitHub.

## Intended Behaviour

This prompt is NOT a one-shot research task. It is a **recurring routine** — designed to be run at the start of every Claude Code session or on a configurable interval. It is stateful: it reads `maintenance/run-log.md` to know where it left off, and writes a new record there when it finishes.
