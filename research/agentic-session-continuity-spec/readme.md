# Agentic Session Continuity Spec

**Status:** PROPOSED — awaiting execution
**Created:** 2026-05-03
**Version:** 1.0

## What is this folder?

This is the task directory for research proposal `agentic-session-continuity-spec`.
It contains a fully-formed, self-contained research prompt ready to be executed by
any ReAct-capable agent (Google Jules, Claude Code, Gemini Deep Research, or equivalent).

**This research has NOT been executed yet.** The workspace, synthesis, reflection,
and output folders are initialized scaffolds. They will be populated when an agent
executes the research prompt.

## Why this research?

The existing Spec-D/E/F trilogy (at `research/spec-driven-research-agentic-workflows/`)
defines how to *orchestrate* agentic workflows. It does not address the *epistemic lifecycle*
of an individual agent's understanding: how context is born, grows, compresses, externalizes,
and is reconstituted across session boundaries. Production deployments now routinely encounter
context windows exceeding 100k–1M tokens, with documented >50% performance degradation
at those scales. This research fills that gap.

## Contents

- [prompt.md](./prompt.md): The complete, self-contained research prompt. This is the
  primary deliverable of this proposal. Hand it verbatim to any ReAct-capable agent.
- [workspace/](./workspace/): Scratchpad directory — will be populated during execution.
- [synthesis/](./synthesis/): Structured synthesis artifacts — will be populated during execution.
- [reflection/](./reflection/): Critical thinking artifacts — will be populated during execution.
- [output/](./output/): Final deliverable (`SPEC.md`) — will be created during execution.

## Target Output

The research will produce `output/SPEC.md` containing three new normative specs:

| Spec | Subject |
|:-----|:--------|
| **Spec-G** | Context Engineering Layer — Write/Select/Compress/Isolate strategy patterns |
| **Spec-H** | Agent Memory Architecture — STM/MTM/LTM/Graph hierarchy with contamination prevention |
| **Spec-I** | Cross-Session Continuity Protocol — session handoff contracts, staleness detection |

## Governing Specifications

- [RESEARCH.md](../../RESEARCH.md) — directory structure and workflow requirements
- [AGENTS.md](../../AGENTS.md) — agent instructions
- [PRE_COMMIT.md](../../PRE_COMMIT.md) — mandatory pre-commit checks
- [FRUSTRATED.md](../../FRUSTRATED.md) — frustration level logging specification

## Workflow Assumptions

- The prompt in `prompt.md` was generated using the `research-prompt-optimizer v3.1` skill
  pattern, following the RISE-DX + ReAct template established in `spec-driven-research-agentic-workflows`.
- Confirmed priors from Spec-A through Spec-F are encoded in the prompt's PRIOR ART BLOCK
  and MUST NOT be re-researched by the executing agent.
- The three pre-seeded contradictions (C1/C2/C3) in the prompt's S5 step are hypotheses,
  not conclusions — the executing agent must investigate and resolve them.
