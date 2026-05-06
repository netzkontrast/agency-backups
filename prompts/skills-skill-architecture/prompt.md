---
type: prompt
status: active
slug: skills-skill-architecture
summary: "Research and spec the skills-skill loader: architecture for a single stub skill that routes all skill loading through this repository."
created: 2026-05-04
updated: 2026-05-04
prompt_kind: research-proposal
prompt_framework: RISEN
prompt_target_agent: Claude Code
prompt_relates_to_task: ""
---

# Task: research and spec the `skills-skill`

## Context

Michael Schimmer maintains a collection of ~14 user-skills under `/mnt/skills/user/` in his [claude.ai](http://claude.ai) container. That location is read-only and ephemeral per session, with no upstream and no cross-agent visibility. A bootstrap PR mirrored those skills into `/skills/` of this repository, establishing a versioned, multi-agent-accessible source of truth.

The current arrangement is transitional: 14 skills are installed in `/mnt/skills/user/` *and* mirrored in `/skills/`. The endgame is that `/mnt/skills/user/` contains exactly **one** installed skill — `skills-skill` — which on trigger clones this repository and routes all skill loading through a management layer that lives in `/skills/skills-skill/` here. The other 13 skills become content, not installed entities.

This task: research the design space, choose an architecture, produce a spec rigorous enough that another agent can implement it from the spec alone. A subsequent task will run a Google Gemini Deep Research pass on the same questions; the Gemini PDF result will be folded back into the spec as a v2.

## Out of scope

- Implementing the `skills-skill` itself.
- Migrating any individual existing skill to consume the new loader.
- Changing how [claude.ai](http://claude.ai)'s native skill-trigger mechanism works. Treat that as a fixed external system.

## Research questions

### R1. Bootstrap mechanics
How does a minimal `SKILL.md` installed in `/mnt/skills/user/skills-skill/` reliably activate when needed and route control to the cloned repo? What are the failure modes when the repo is unreachable, and what is the minimal acceptable behaviour in each?

### R2. Sync direction and conflict model
What is the read/write topology between `/mnt/skills/user/`, this repo's `/skills/`, and the local skill capabilities of the other agents (Claude Code, Jules, gemini-cli)? Where do edits originate, where do they land, how are concurrent edits reconciled?

### R3. Runtime routing
After the repo is cloned in-session, how does `skills-skill` decide which underlying skill (if any) is the right one to load for the user's current prompt? How does this interact with the host system's own skill-trigger mechanism — complement, replace, or conflict?

### R4. Progressive disclosure
The existing skill collection follows a discipline of keeping `SKILL.md` bodies small and pushing depth into `references/`. The new loader must preserve this property. Define a mechanism for stepwise content delivery that does not assume persistent state between turns.

### R5. Trust boundary
Repo content becomes model instructions on load. The repo is public; anyone with write access (currently constrained to PR-and-merge by Michael) is therefore an instruction channel. What invariants must the bootstrap stub enforce regardless of repo content? What is the relationship between the bootstrap stub's immutability (it lives in the read-only `/mnt/skills/user/`) and the mutable repo content it loads?

### R6. Cross-agent portability
Claude Code, Jules, and gemini-cli have different skill-loading conventions. How close can a single canonical `/skills/skills-skill/SKILL.md` get to being directly loadable by all of them? Where adapters are required, where do they live and who maintains them?

### R7. Offline behaviour and version pinning
Should the bootstrap clone fresh every session, pull-if-exists, or sync only on explicit trigger? Should it pin a commit SHA or always track `main`? What is the relationship between freshness, reproducibility, and latency, and what guarantees does the spec offer?

## Required deliverables

A research workspace at `/research/skills-skill-architecture/` (follows `RESEARCH.md`):

1. `/output/SPEC.md` — RFC-2119 normative preliminary spec covering R1–R7. Uncertain sections MUST be explicitly marked. Each MUST/SHOULD MUST have a corresponding Gherkin scenario.
2. `/output/gemini-prompt.md` — Self-contained Deep Research prompt for Google Gemini. An agent reading only that file, with no access to this repo, MUST be able to execute it.
3. `/output/integration-plan.md` — Precise instructions for how the next agent folds the Gemini PDF into the spec.
4. Full workspace per `RESEARCH.md §2`: workspace/, synthesis/, reflection/.

## Success criteria

- The preliminary spec is implementable in principle (an agent reading only the output could build a working `skills-skill`).
- Uncertain sections are marked as such; "I haven't decided" is not acceptable; "deferred to Gemini with justification" is.
- The Gemini prompt is verifiably self-contained.
- The integration plan makes the next agent's job mechanical, not interpretive.
- Friction is logged per `FRUSTRATED.md`.
- Open questions are filed as follow-up prompts in `/prompts/`, not appended to this research workspace.


## Framework

RISEN+ReAct, retrofitted by Task 020. The original prompt above predates the canonical headings; this section restates the framework for fm-validate header conformance. Refine when the prompt is next executed.

## R — Role

See the prompt body above for the executor persona. Future authors SHOULD condense the role declaration into this section.

## I — Input

- See the prompt body above for the inputs the executor reads.

## S — Steps

1. Refer to the prompt body above for the original step ordering.
2. Future authors MUST normalise the step list under this heading.
3. Each step SHOULD declare exactly one RFC 2119 keyword.

## E — Expectations

- Refer to the prompt body above for the deliverables.

## Constraints

- The agent MUST NOT execute this prompt as-is without first authoring the canonical sections above; the migration is structural, not semantic.
- Future authors SHOULD treat the body migration as a T3 change per MAINTENANCE.md §1.
