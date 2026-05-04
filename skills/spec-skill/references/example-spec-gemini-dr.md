# Worked Example — Spec-C: Gemini Deep Research

This is the third reference spec from the May 2026 research report. Unlike Spec-A (cloud coding agent) and Spec-B (terminal coding agent), Spec-C describes a **research agent** — a system whose output is a synthesis report, not a code change.

This example exists in the skill primarily to show that the five-aspect schema generalizes beyond coding. The Aspects are the same; what changes is what each aspect *means*. Explore is now multi-modal source gathering. Implement is now report drafting. Validate is now citation and conflict resolution.

The example demonstrates:

- The schema applied to a **non-coding agent** with the same prefix discipline
- **Different failure modes surfaced by the rationale** — citation hallucination, conflicting evidence, premature aggregation
- A `MUST NOT` that protects user epistemics rather than system integrity (`C.6.4` — never trust confident numerical claims without source verification)
- An §8 that admits the agent's flagship failure mode (URL hallucination) is not eliminated, only reduced

---

## Spec-C: Gemini Deep Research

### §0. Status & Provenance

**Status:** Mature (High Confidence)
**Last Review Date:** May 2, 2026
**Primary Sources:** Google AI Studio documentation, Gemini API documentation, Google DeepMind Engineering Blog.

### §1. Normative Conventions

The key words MUST, MUST NOT, REQUIRED, SHALL, SHALL NOT, SHOULD, SHOULD NOT, RECOMMENDED, NOT RECOMMENDED, MAY, and OPTIONAL in every produced Spec are to be interpreted as described in BCP 14 when, and only when, they appear in all capitals, as shown here.

### §2. System-Level Prompt Conventions

- C.2.1 — A research invocation MUST utilize the specialized stateful interactions endpoint rather than legacy content generation endpoints.
- C.2.2 — A long-horizon research prompt MUST be executed with the appropriate background parameters to prevent connection timeouts.
- C.2.3 — A developer MUST select the maximum comprehensiveness agent tier when deep synthesis and exhaustive retrieval are required.
- C.2.4 — A research prompt SHOULD utilize a structured four-part query framework consisting of the task, grounding instruction, format, and constraints.
- C.2.5 — A prompt MUST NOT assume the agent will natively generate visual charts unless explicitly requested in the text.

### §3. Aspect 1 — Explore

#### §3.1 Normative Statements

- C.3.1 — An exploration prompt MUST explicitly declare the external server connections it intends to search across.
- C.3.2 — A research task MUST combine open web browsing with proprietary document uploads to ensure deep multi-modal grounding.
- C.3.3 — The agent MUST NOT be restricted to a single search query; prompts MUST allow the agent to iterate over dozens of sources.
- C.3.4 — A developer SHOULD instruct the agent to prioritize peer-reviewed journals and unbiased data sources during open-web exploration.
- C.3.5 — A prompt MAY explicitly restrict the agent's tooling strictly to custom proprietary data by turning off open web access.

#### §3.2 Acceptance Criteria (Gherkin)

```gherkin
# anchor: C.3.2
Feature: Multi-Modal Exploration Grounding

  Scenario: The research agent explores using provided context
    Given the user uploads a proprietary dataset document
    And the user connects a server pointing to an internal corporate wiki
    When the user prompts the agent to explore the historical impact of a specific feature
    Then the agent searches both the open web and the connected internal server
    And the agent successfully synthesizes findings from both public and private data environments
```

#### §3.3 Rationale

Deep autonomous research fundamentally differs from standard search aggregation by iteratively exploring vast, branching data trees over extended periods. Providing multi-modal context alongside web access securely grounds the exploration process. If the tools are not explicitly defined and constrained, the agent might hallucinate facts rather than fetching the precise proprietary data needed for an enterprise-grade workflow.

### §4. Aspect 2 — Plan / Develop Spec

#### §4.1 Normative Statements

- C.4.1 — A planning prompt MUST set the collaborative planning flag to force the agent to propose a strategy before execution begins.
- C.4.2 — A user MUST utilize the previous interaction identifier to iterate on and steer the proposed research plan.
- C.4.3 — A developer MUST explicitly alter the collaborative planning flag to formally approve the plan and trigger report generation.
- C.4.4 — A plan review prompt SHOULD specify strict constraints on which sources to avoid if the initial plan relies on low-quality content aggregators.
- C.4.5 — The agent MUST expose its intermediate reasoning steps via live thought summaries during the planning phase.

#### §4.2 Acceptance Criteria (Gherkin)

```gherkin
# anchor: C.4.1
Feature: Collaborative Planning Execution

  Scenario: The user steers the research direction prior to execution
    Given a user submits a prompt with the collaborative planning parameter enabled
    When the agent returns a proposed list of sub-topics to explore
    And the user replies with instructions to focus less on history and more on modern competitor hardware
    Then the agent updates its research plan
    And the agent does not begin extended web searching until the collaborative planning parameter is disabled
```

#### §4.3 Rationale

Autonomous research can easily burn immense compute cycles analyzing the wrong tangential topic. Collaborative planning directly solves the "black box" problem inherent to agentic artificial intelligence. By forcing the agent to reveal its planned search queries and target sources before executing a long-running research loop, the human operator guarantees that the final exhaustive report precisely aligns with organizational objectives.

### §5. Aspect 3 — Implement / Execute

#### §5.1 Normative Statements

- C.5.1 — An implementation prompt MUST explicitly define the output structure, such as bulleted lists, specific schemas, or executive summaries.
- C.5.2 — A prompt requesting data visualizations MUST configure the visualization parameter and explicitly request the chart in the text body.
- C.5.3 — The agent MUST process implementation workflows asynchronously, requiring the developer to poll the system for the completed status.
- C.5.4 — An execution prompt SHOULD specify the exact timeframe of relevance for the data to be gathered and synthesized.
- C.5.5 — The user MUST NOT split a combined research and write workflow into two separate prompts; they must be merged into a single instruction.

#### §5.2 Acceptance Criteria (Gherkin)

```gherkin
# anchor: C.5.1
Feature: Structured Execution Output

  Scenario: The agent generates a tightly formatted report
    Given the user submits an execution prompt via the specialized API
    When the prompt mandates formatting the output strictly as a comparison table
    And the task runs to completion in the background
    Then the final retrieved interaction output is formatted strictly as the requested table
```

#### §5.3 Rationale

The advanced research agent is highly capable of combining the complex tasks of exhaustive data retrieval and intricate formatting into a single pass. Splitting the workflow artificially limits the model's ability to logically structure data as it ingests it. Setting strict formatting and timeframe constraints upfront prevents the agent from returning unmanageable walls of generalized, unstructured text.

### §6. Aspect 4 — Review

#### §6.1 Normative Statements

- C.6.1 — A review prompt MUST instruct the agent to track and provide inline citations for every factual claim generated.
- C.6.2 — The agent MUST cross-check discovered statistics against live current sources to prevent data staleness and inaccuracy.
- C.6.3 — A developer SHOULD submit follow-up prompts to drill into specific sections of the generated report for deeper review.
- C.6.4 — The user MUST NOT assume that highly confident numerical claims are immune to hallucinations without manually verifying the cited source.
- C.6.5 — A review loop MAY prompt the agent to generate a risks and counterarguments section to enforce objective, balanced analysis.

#### §6.2 Acceptance Criteria (Gherkin)

```gherkin
# anchor: C.6.1
Feature: Inline Citation Verification

  Scenario: The agent provides traceable citations
    Given the agent has completed an exhaustive background research run
    When the agent compiles the final synthesis report
    Then every statistical claim in the report is immediately followed by an inline citation marker
    And the inline citation corresponds to an accessible, valid reference in the source index
```

#### §6.3 Rationale

Even advanced intelligence systems can suffer from citation hallucinations, such as fabricating author names or linking to defunct domains. Enforcing strict inline citation rules within the prompt allows human reviewers to rapidly verify the evidence presented. Requesting explicit counterarguments forces the model to review its own gathered data critically, effectively breaking internal echo-chamber retrieval loops.

### §7. Aspect 5 — Validate / Verify

#### §7.1 Normative Statements

- C.7.1 — A validation prompt MUST instruct the agent to explicitly weigh conflicting evidence against each other rather than silently picking one single source.
- C.7.2 — The developer MUST independently verify generated hyperlinks to ensure they do not lead to hallucinated or malicious domains.
- C.7.3 — A validation prompt SHOULD request the agent to flag claims that are outdated or no longer reflect current industry best practices.
- C.7.4 — The agent MUST accurately map its retrieved sources to the corresponding claims in the final export document.
- C.7.5 — A user MAY utilize audio overview features to validate the narrative coherence and flow of the generated report.

#### §7.2 Acceptance Criteria (Gherkin)

```gherkin
# anchor: C.7.1
Feature: Conflicting Evidence Resolution

  Scenario: The agent encounters differing statistics during research
    Given the agent is researching market size projections
    When one source claims the market is large and another source claims it is small
    Then the agent explicitly documents the discrepancy in the final report
    And the agent provides the context and citations for both conflicting figures without omission
```

#### §7.3 Rationale

In deep autonomous research, conflicting data represents a critical feature of the landscape, not a bug. If an agent silently aggregates conflicting numbers by mathematically averaging them or arbitrarily picking the most recent date, it destroys the necessary nuance of the research. Validation instructions must explicitly command the agent to embrace and thoroughly document contradictions to maintain expert-grade analytical integrity.

### §8. Known Limitations & Open Questions

- While the latest model iterations reduce hallucination rates significantly, URL citation hallucination remains a non-zero risk, particularly in highly niche academic or unindexed fields.
- Polling-based asynchronous workflows can be difficult to integrate seamlessly into real-time user interface applications without building extensive backend middleware.

### §9. Source Index

1. Google AI Studio Gemini API Interactions documentation
2. Google DeepMind Blog: "Deep Research Max: A step change for autonomous research agents"
3. BuildFastWithAI: "Gemini Deep Research API Tutorial"
4. DigitalApplied: "Google Gemini Deep Research Guide"
5. PromptingGuide.ai: Deep Research best practices

---

## What this example adds beyond Spec-A and Spec-B

- **The schema generalizes beyond coding.** The five aspects (Explore/Plan/Implement/Review/Validate) map onto research naturally — but with different content. Explore is multi-modal source gathering; Implement is report drafting; Review is citation tracking. When using the schema for a non-coding agent, keep the aspect names but rewrite what they *mean* for the system at hand. Don't force coding metaphors onto research workflows.
- **`MUST NOT` that protects the user, not the system.** `C.6.4` ("the user MUST NOT assume that highly confident numerical claims are immune to hallucinations without manually verifying the cited source") is unusual: it constrains the user's epistemic posture, not the agent's behavior. This is appropriate for systems where the failure mode is *user over-trust*, not *agent malfunction*. Use sparingly — but when over-trust is the documented risk, name it.
- **Prohibition against silent aggregation.** `C.7.1` and its rationale ("conflicting data represents a critical feature of the landscape, not a bug") capture a subtle quality property: the agent must *preserve* contradiction rather than resolve it. This is research-specific; coding agents have the opposite need (resolve ambiguity to ship). When writing a spec, ask which way the system should fail.
- **Honest §8 on the flagship failure.** Spec-C admits URL citation hallucination is reduced but not eliminated. A weaker spec would either not mention it or claim it's solved. Naming the residual risk maintains credibility.
- **Reduced statement count where appropriate.** Spec-C's §8 has 2 bullets where Spec-A has 3 and Spec-B has 3. Don't pad §8 to match other specs — write what's actually open, and stop.

When using the spec format for a system that produces *information* rather than *code*, this is the model. The bones stay; the meat changes.
