---
type: note
status: active
slug: skills-navigation-bootstrap-methodology
summary: "Methods applied during the skills-navigation-bootstrap synthesis."
created: 2026-05-04
updated: 2026-05-04
---

# Methodology

The run combined the RISEN+ReAct framework declared by the executing prompt with three named methods from the repository's research toolbox.

## M02 — Environment Inspection

Read-only enumeration of the live state of `/skills/`, `/tasks/`, `/prompts/`, root governance specs, and `tools/`. No fabrication: every claim about repo state is rooted in a file read recorded in `workspace/session.log`. M02 produced the State track input (`tracks.md` § T-NAV-1) and the inventory of existing primitives in `output/SPEC.md` §2.

## M06 — Separation of Concerns

The prompt bundles four concerns into one deliverable: (a) governance for `/skills/`, (b) skill-to-skill navigation, (c) markdown indexing tools, (d) per-agent bootstrap. M06 splits them along their stable axes — *spec layer*, *graph layer*, *tooling layer*, *runtime layer* — and routes each to the downstream Task whose scope already covers it (009, 011, 010, future). The split is documented in `output/SPEC.md` §1.

## M13 — Adversarial Query Expansion

Four query axes were exercised against the architectural draft (per `research/agent-prompt-specs-3-systems-sdd/output/SPEC.md` §M13):

1. **Specificity axis** — Does each normative statement bind exactly one actor and one observable behaviour? (Yes after edit; see SPEC §3-§7.)
2. **Generality axis** — Does the design hold for agents not yet enumerated (Jules, gemini-cli)? (Partially. Bootstrap contract is agent-neutral; runtime adapters are deferred to existing follow-up prompts.)
3. **Inversion axis** — What if the manifest file is corrupt or absent? (See SPEC §6.4 failure modes; falls back to body scan with a warning.)
4. **Abstraction axis** — Could the same indexing approach apply to `/prompts/` or `/research/`? (Yes; the manifest schema is intentionally namespace-aware. Generalisation deferred.)

## Pre-Commitments

Declared before drafting `output/SPEC.md`:

- **PC.1** No tool implementation — only contracts, schemas, and Gherkin acceptance scenarios.
- **PC.2** RFC 2119 keywords used per `AGENTS.md` discipline (one normative keyword per sentence; uppercase only for binding clauses).
- **PC.3** No edits to root governance files (`AGENTS.md`, `MAINTENANCE.md`, `TASK.md`) — those are explicit Task 009 scope, not this research run's scope per the prompt's Narrowing constraint.
- **PC.4** No mutation of any `research_phase: complete` workspace, including `research/skills-skill-architecture/`.
