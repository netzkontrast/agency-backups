---
type: research
status: active
slug: token-efficiency-tool-suite
summary: "Synthesized specification for a Token Efficiency Tool Suite, derived from public GitHub repos enforcing token budgets and context pruning."
created: 2026-05-04
updated: 2026-05-04
research_phase: complete
research_executes_prompt: token-efficiency-tool-suite
research_friction_level: FL1
---

# Token Efficiency Tool Suite Specification

## §1. Normative Conventions

The key words MUST, MUST NOT, REQUIRED, SHALL, SHALL NOT, SHOULD, SHOULD NOT, RECOMMENDED, NOT RECOMMENDED, MAY, and OPTIONAL in this document are to be interpreted as described in BCP 14 [RFC 2119] [RFC 8174] when, and only when, they appear in all capitals as shown here.

## 1. Executive Summary

This specification defines a Token Efficiency Tool Suite for the repository, derived from a survey of 14 public GitHub repositories. The research identified that relying on system prompts for conciseness is ineffective. Instead, efficiency MUST be enforced structurally. The proposed suite consists of four components: a Token-Estimator (planner), a Context-Pruner (middleware), a Budget-Enforcer (hard limits), and a Strict-Schema-Validator (coercion layer). This suite extends the existing RTK proxy to guarantee bounded LLM execution.

## 2. Landscape Map

| Repository | Axis | Stars | Enforcement Mechanism | Relevance |
|---|---|---|---|---|
| `narendrakumarnutalapati/licitra-sentry` | Mandatory tools | 4 | Mandatory tool mediation layer | High |
| `chkao831/agentic_mp_dualrag` | Mandatory tools | 2 | Allowlisted tool execution | High |
| `ArkadeepGanguli/Token-Budgeted-Multi...` | Token budget | 0 | Pre-invocation budget routing | High |
| `revenium/openclaw-revenium` | Token budget | 11 | Invocation layer guardrails | High |
| `pykul/tokencap` | Token budget | 3 | Hard limits & configurable policy | High |
| `OzmaKa/structured-output` | Structured output | 1 | Pydantic validation + JSON mode | High |
| `Context-Engine-AI/Context-Engine` | Context window | 391 | Context compression middleware | High |
| `jabbatrixx/ContextGate` | Context window | 3 | Pre-invocation pruning | High |
| `zubair-trabzada/ai-trading-claude` | Mandatory tools | 99 | Application specific limits | Low |
| `cosmicstack-labs/mercury-agent` | Token budget | 1952 | Permission-hardened tools | Medium |
| `AravChandra/PydanticAI_weather...` | Structured output | 0 | Pydantic AI integration | Medium |
| `paarths-collab/killport` | Structured output | 4 | JSON-mode agent | Low |
| `LearnPrompt/cc-harness-skills` | Context window | 210 | CC-inspired skills | Medium |
| `Sompote/tiger_cowork` | Context window | 56 | MCP context compression | Medium |

## 3. Design Hypotheses

- **H1 (The Mediation Hypothesis):** Agents MUST interact with the system exclusively through a mediation layer that drops non-schema compliant output, ensuring zero tokens are wasted on free-form hallucination. Supported by `licitra-sentry` and `agentic_mp_dualrag`.
- **H2 (The Pre-flight Hypothesis):** Token budgets MUST be checked prior to tool execution, not post-hoc, to prevent overruns during heavy operations. Supported by `openclaw-revenium` and `tokencap`.
- **H3 (The Pruning Hypothesis):** The context window MUST be pruned by a dedicated middleware before reaching the LLM to maximize the budget. Supported by `Context-Engine` and `ContextGate`.

## 4. Surviving Architecture

All three hypotheses survived synthesis. The resulting architecture is a four-stage pipeline:

```text
[ Agent ]
   |
   v
+-----------------------+
| 1. Token-Estimator    | <-- Decides if query is cheap enough for standard mode or needs tools.
+-----------------------+
   |
   v
+-----------------------+
| 2. Context-Pruner     | <-- Strips noise/history before execution.
+-----------------------+
   |
   v
+-----------------------+
| 3. Budget-Enforcer    | <-- Hard-aborts if estimated cost > remaining budget.
+-----------------------+
   |
   v
+-----------------------+
| 4. Schema-Validator   | <-- Drops any output not conforming to strict JSON tools.
+-----------------------+
   |
   v
[ Environment / RTK ]
```

## 5. Normative Specification

### § Tool Suite Roles
1. The **Token-Estimator** MUST calculate an approximate token cost for the proposed action.
2. The **Context-Pruner** MUST strip redundant whitespace, duplicate logs, and archived file contents from the payload.
3. The **Budget-Enforcer** MUST maintain a running token tally for the active task.
4. The **Strict-Schema-Validator** MUST reject any agent output that fails to match the predefined JSON schema.

### § Mandatory Invocation Points
1. The Token-Estimator MUST be invoked immediately after the agent generates a thought but before the action is executed.
2. The Context-Pruner MUST be invoked whenever the agent reads a file larger than 10KB.

### § Token Budget Rules
1. The Budget-Enforcer MUST abort the task if the threshold reaches 90% without a completion plan.
2. Tools MUST report their consumed token sizes back to the Budget-Enforcer upon completion.

### § Integration with existing repo hooks
1. The Context-Pruner MUST operate upstream of the RTK proxy to avoid duplicating compression logic.
2. Pre-commit hooks MUST NOT execute if the Budget-Enforcer flags a negative balance.

## 6. Gherkin Acceptance Criteria

Feature: Token Efficiency Enforcement

  Background:
    Given the agent is running in the repository environment
    And the Token Efficiency Tool Suite is active

  # anchor: TE.1.1
  Scenario: Agent attempts to execute an action exceeding the budget
    Given the task has a remaining budget of 500 tokens
    When the agent proposes an action estimated at 600 tokens
    Then the Budget-Enforcer MUST abort the action
    And the system MUST prompt the agent to use a cheaper tool

  # anchor: TE.1.2
  Scenario: Agent reads a large file
    Given a file exists that is 15KB in size
    When the agent invokes the read_file tool on this file
    Then the Context-Pruner MUST compress the file content before returning it
    And the returned content MUST NOT exceed 10KB

  # anchor: TE.1.3
  Scenario: Agent generates non-compliant output
    Given the Strict-Schema-Validator requires JSON output
    When the agent outputs a mix of Markdown and JSON
    Then the Schema-Validator MUST reject the output
    And the system MUST log a parsing error

  # anchor: TE.1.4
  Scenario: Integration with RTK proxy
    Given the RTK proxy is filtering command line output
    When a shell command is executed
    Then the RTK proxy MUST filter the output first
    And the Context-Pruner MUST further compress the RTK output if it exceeds the token limit

## 7. Contradiction Log

```text
Contradiction: Overhead of Mandatory Tools vs. Token Savings
Claim A: Mandatory tool calling enforces concise communication and prevents verbose hallucination, thus saving tokens.
Claim B: Forcing tool calls for simple requests introduces JSON schema parsing overhead that uses more tokens than a direct response.
Hypothesised cause: Static token budgets vs. dynamic task complexity. Small tasks suffer from tool-call JSON wrapper overhead; large tasks benefit from blocked hallucination.
Evidence to resolve: Implemented the "Token-Estimator" (Query Planner) to dynamically assess if the overhead is justified.
```

## 8. Open Questions / Unresolved

- How exactly does the Context-Pruner differentiate between "noise" and "critical context" without using another LLM (which would cost more tokens)?
- What is the exact fallback mechanism when the Budget-Enforcer aborts a task? Does the agent wait for human approval, or does it permanently fail?

## 9. Sources

1. `narendrakumarnutalapati/licitra-sentry` (Primary)
2. `chkao831/agentic_mp_dualrag` (Primary)
3. `revenium/openclaw-revenium` (Primary)
4. `Context-Engine-AI/Context-Engine` (Primary)

## 10. Methodology Note

This research applied M01 (Falsification) to filter out non-structural tools, M06 (First Principles) to deconstruct efficiency mechanisms, M07 (Contradiction Log) to balance schema overhead, and M13 (Adversarial Query Expansion) to identify missing query planning abstractions.
