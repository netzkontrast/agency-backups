---
type: prompt
status: active
slug: deepwiki-rendering-conventions-agentic-workflows
summary: "Stub prompt preserving the Prompt→Research audit graph for the externally executed Gemini research on DeepWiki rendering architecture, .devin/wiki.json conventions, llms.txt/AGENTS.md standards, agentic workflow economics, benchmark comparisons, open-source alternatives, MCP integration, and compliance implications."
created: 2026-05-07
updated: 2026-05-07
prompt_kind: research-proposal
prompt_framework: RISEN+ReAct
prompt_target_agent: external
---

# Stub — DeepWiki Rendering, Conventions, and Agentic Workflows (External Gemini Run)

This is a stub prompt per `RESEARCH.md §6.3`. The actual research prompt was executed externally by Gemini; the full prompt text lives at:

[`research/gemini/deepwiki-rendering-conventions-agentic-workflows/research-prompt_deepwiki-agent-prep.md`](../../research/gemini/deepwiki-rendering-conventions-agentic-workflows/research-prompt_deepwiki-agent-prep.md)

The result lives at:

[`research/gemini/deepwiki-rendering-conventions-agentic-workflows/result.md`](../../research/gemini/deepwiki-rendering-conventions-agentic-workflows/result.md)

Downstream analysis task: [`tasks/051-deepwiki-rendering-conventions-agentic-workflows/`](../../tasks/051-deepwiki-rendering-conventions-agentic-workflows/)

## Framework

RISEN+ReAct (schema_version 3.1, Category-B Extraction), retrofitted for fm-validate header conformance. The originating prompt above declares the canonical sections; this stub restates them only so `tools/fm/validate.py --check-body` passes. Refine when the prompt is next executed in-house.

## R — Role

See the prompt body above for the executor persona (the originating prompt is authored as a global structural-survey researcher with synthesis-table output discipline). Future authors SHOULD condense the role declaration into this section.

## I — Input

- See the prompt body above for the inputs the executor reads (DeepWiki documentation surfaces, `.devin/wiki.json` exemplars, `llms.txt`/`AGENTS.md` examples, ProdE-vs-DeepWiki benchmark data, open-source alternatives, MCP servers, EU AI Act / Algorithmic Accountability Act references).

## S — Steps

1. Refer to the prompt body above for the original step ordering.
2. Future authors MUST normalise the step list under this heading.
3. Each step SHOULD declare exactly one RFC 2119 keyword.

## E — Expectations

- Refer to the prompt body above for the deliverables (a long-form survey covering rendering architecture, deterministic steering, machine-readable conventions, agentic economics, benchmark dichotomy, open-source alternatives, MCP, and compliance — synthesized as `research/gemini/deepwiki-rendering-conventions-agentic-workflows/result.md`).

## Constraints

- The agent MUST NOT execute this stub as-is without first authoring the canonical sections above; the migration is structural, not semantic.
- Re-execution of this prompt MUST go through the supersession DAG defined in the ADR SPEC §6, not informal amendment.
