# agentic-eval-trust-improvement-spec

**Status:** PROPOSED — awaiting execution
**Created:** 2026-05-04
**Version:** 1.0

## What is this folder?

This is the task directory for research proposal `agentic-eval-trust-improvement-spec`.
It contains a fully-formed, self-contained research prompt ready to be executed by any
ReAct-capable agent (Google Jules, Claude Code, Gemini Deep Research, or equivalent).

**This research has NOT been executed yet.** The workspace, synthesis, reflection, and
output folders are initialized scaffolds. They will be populated when an agent executes
the research prompt.

## Why this research?

The existing Spec-A through Spec-F trilogy covers what agents can do and how to govern
their workflows. The proposed Spec-G/H/I covers how agents maintain context across
sessions. What is missing is the *closing layer* of the governance pyramid:

- **How do you know if an agent's output is actually good?** No normative rubric exists
  for evaluating the quality of agentic spec documents, plans, or governance artifacts
  beyond task-completion metrics.
- **How much should you trust an agent, and when?** Trust calibration is empirically
  observed in production (Anthropic Jan 2026 data) but algorithmically undefined.
- **How do failures feed back into better governance?** Feedback loops exist for
  task-performance improvement (Reflexion, DSPy) but no system formalizes the
  governance-protocol improvement loop that this repo's FRUSTRATED.md + improvement
  loop already does informally.

This research fills all three gaps with normative specifications.

## Contents

- [prompt.md](./prompt.md): The complete, self-contained research prompt. Primary
  deliverable of this proposal. Hand it verbatim to any ReAct-capable agent.
- [workspace/](./workspace/): Scratchpad directory — will be populated during execution.
- [synthesis/](./synthesis/): Structured synthesis artifacts — will be populated during execution.
- [reflection/](./reflection/): Critical thinking artifacts — will be populated during execution.
- [output/](./output/): Final deliverable (`SPEC.md`) — will be created during execution.

## Target Output

The research will produce `output/SPEC.md` containing three new normative specs:

| Spec | Subject |
|:-----|:--------|
| **Spec-J** | Agentic Output Quality Evaluation — multi-dimensional quality rubrics, Agent-as-a-Judge patterns, normative correctness evaluation for spec documents |
| **Spec-K** | Human-Agent Trust Calibration — five-level autonomy taxonomy, promotion/demotion criteria, runtime governance gates, regulatory floor (EU AI Act) |
| **Spec-L** | Governance Improvement Loop Formalization — friction taxonomy extension, failure trajectory analysis, self-rewarding vs. separate-evaluator loops, artifact-level conflict resolution |

## Prior Art Dependencies

| Artefact | Status |
|:---------|:-------|
| Spec-A/B/C (`research/agent-prompt-specs-3-systems-sdd/output/SPEC.md`) | Executed — confirmed priors |
| Spec-D/E/F (`research/spec-driven-research-agentic-workflows/output/SPEC.md`) | Executed — confirmed priors |
| Spec-G/H/I (`research/agentic-session-continuity-spec/`) | PROPOSED — executing agent must verify |

## Governing Specifications

- [RESEARCH.md](../../RESEARCH.md) — directory structure and workflow requirements
- [AGENTS.md](../../AGENTS.md) — agent instructions
- [PRE_COMMIT.md](../../PRE_COMMIT.md) — mandatory pre-commit checks
- [FRUSTRATED.md](../../FRUSTRATED.md) — frustration level logging specification

## Workflow Assumptions

- The prompt in `prompt.md` was generated using the `research-prompt-optimizer v3.1` skill
  pattern, following the RISE-DX + ReAct template from `spec-driven-research-agentic-workflows`.
- External research was conducted (May 2026) to identify and pre-seed: confirmed prior art
  sources for each Spec, three contradictions (C1/C2/C3) for the executing agent to resolve,
  and four confirmed open research problems to investigate.
- The CLEAR Framework (arxiv 2511.14136), Agent-as-a-Judge (arxiv 2508.02994), Levels of
  Autonomy taxonomy (arxiv 2506.12469), and Multi-AI Iterative Refinement (arxiv 2412.17149)
  are the key T2 sources identified during prompt authoring — the executing agent MUST verify
  these and extend them, not replace them.
- Spec-G/H/I execution status is unknown at prompt-authoring time. The executing agent MUST
  check filesystem (Jules) or document the gap (non-Jules) before proceeding.
