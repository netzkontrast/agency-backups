---
type: research
status: completed
slug: superclaude-agency-orchestration-spec
summary: "Gemini-generated SuperClaude orchestration / meta-governance specification — proposes a workspace↔command↔MCP-server mapping for the netzkontrast/agency repo (30 /sc: commands, 8 MCP servers, normative Gherkin SC.CMD.* anchors). Self-asserts 'binding / IN-FORCE' but is RAW external ingestion per RESEARCH.md §6; downstream evaluation Task 040 owns the binding decision."
created: 2026-05-06
updated: 2026-05-06
research_phase: complete
research_executes_prompt: superclaude-agency-orchestration-spec
research_friction_level: FL0
---

# Result — SuperClaude Orchestration & Meta-Governance Specification (Gemini)

Raw external output from a Gemini Deep Research run. Full content in [`superclaude-agency-orchestration-spec.md`](./superclaude-agency-orchestration-spec.md).

**Status caveat — important.** The document self-asserts "binding, IN-FORCE governance model". Per `RESEARCH.md §6`, external research results are *raw material*, not normative governance, until evaluated by a downstream Task. The binding-status assertion in §0 is therefore **not in force** at ingestion time; it is a *proposal* awaiting evaluation by [Task 040](../../../tasks/040-superclaude-spec-evaluation/task.md).

Originating prompt: not filed (external Gemini run; no `/prompts/superclaude-agency-orchestration-spec/` exists at ingestion time — see Task 040 plan for whether a stub prompt should be retro-filed).

Downstream analysis task: [`tasks/040-superclaude-spec-evaluation/`](../../../tasks/040-superclaude-spec-evaluation/).

## Pre-evaluation observations (informational, not findings)

The maintainer flagged the following at ingestion to anchor Task 040's scope; these are *not* the evaluation — Task 040 owns that:

- The doc proposes a workspace↔command mapping (`AGENTS.md → /sc:pm`, `TASK.md → /sc:spawn+/sc:task`, etc.) that is asserted, not derived from the existing repo state.
- It cites MCP servers (Tavily, Playwright, Morphllm, Chrome DevTools) that are **not currently integrated** in this repo's tooling.
- Its FRUSTRATED.md FL0–FL3 references match existing governance, but its `ReflexionPattern` and `confidence-check skill` references do **not** exist as repo skills.
- Gherkin anchor scheme `SC.CMD.<aspect>.<statement>` is well-formed and parallel to the `ADR.A.<aspect>.<statement>` scheme shipped by Task 031, suggesting potential alignment.
- The 30-command claim aligns roughly with the user-invocable `sc:*` skill list visible in this repo, though several mentioned skills (`sc-document` with hyphen, `confidence-check`) don't match repo names.