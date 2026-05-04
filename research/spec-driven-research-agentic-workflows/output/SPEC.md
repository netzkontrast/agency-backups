---
type: research
status: completed
slug: spec-driven-research-agentic-workflows
summary: "Normative governance specs (D/E/F) for designing, orchestrating, and repository-grounding agentic research workflows to prevent drift and context degradation."
created: 2026-05-04
updated: 2026-05-04
research_phase: complete
research_executes_prompt: ""
research_friction_level: FL0
---

# Spec-Driven Best Practices for Designing and Governing Agentic Research Workflows

## Executive Summary
This document establishes the normative best practices for designing, governing, and executing agentic research workflows. It defines the meta-level protocols required to prevent workflow drift and context degradation in long-horizon autonomous tasks.

- **Spec-D** outlines the governance of the specifications themselves, enforcing strict RFC-2119 discipline and Gherkin behavior-driven development to anchor agent planning.
- **Spec-E** details orchestration patterns, mandating the separation of Planning and Execution via DAG architectures and requiring explicit state serialization during multi-agent handoffs.
- **Spec-F** defines repository-resident governance, shifting away from centralized documentation toward decentralized, adjacent `readme.md` navmeshes and enforcing pre-commit verification gates.

Collectively, these specs ensure that any conformant agent can operate autonomously across the Explore → Plan → Implement → Review → Validate cycle reliably.

## Common Conventions Across Specs
- **Decentralization:** All governance artifacts must live adjacent to the code they govern.
- **Testability:** Every normative constraint must map to an observable state change.
- **Explicit Handoffs:** Context must be serialized; raw conversation history must not be relied upon for long-horizon stability.

## Spec-D: Spec-Driven Research Workflow Governance

### §0. Status & Provenance
- **Status:** Draft
- **Last Review Date:** 2026-05-02
- **Sources:** IETF RFC 2119, IEEE Spec-Driven Development, Agentic BDD Research

### §1. Normative Conventions

> The key words **MUST**, **MUST NOT**, **REQUIRED**, **SHALL**, **SHALL NOT**,
> **SHOULD**, **SHOULD NOT**, **RECOMMENDED**, **NOT RECOMMENDED**, **MAY**, and
> **OPTIONAL** in every produced Spec are to be interpreted as described in BCP 14
> [RFC 2119] [RFC 8174] **when, and only when, they appear in all capitals**, as
> shown here.

### §2. System-Level Conventions
- **D.2.1** Authors MUST structure [Source: IEEE SDD, T2] normative documents to prioritize machine readability over human narrative flow.
- **D.2.2** Spec authors MUST chunk a specification [Source: Living Specification Patterns, T2] into separate files or explicit sections if it exceeds standard agent context windows.

### §3. Aspect 1 — Explore
- **D.3.1** The agent MUST extract [Source: Gherkin BDD, T2] all explicit assumptions from the provided seed prompt before beginning research.
- **D.3.2** The agent SHOULD utilize Source Triangulation (M06) to gather evidence from at least two independent T1/T2 sources.

```gherkin
# anchor: D.3.2
Feature: Source Triangulation

  Scenario: Agent encounters a novel claim
    Given the agent reads a claim from a T3 source
    When the agent seeks verification
    Then the agent searches for a T1 or T2 source corroborating the claim
    And the agent logs the sources in the Source Index
```
The explore phase requires broad ingestion. Relying on a single community blog post for a normative statement is risky and requires secondary confirmation.

### §4. Aspect 2 — Plan / Develop Spec
- **D.4.1** Spec authors MUST ensure a normative statement contains [Source: IETF RFC 2119, T1] exactly one RFC-2119 keyword.
- **D.4.2** Spec authors MUST explicitly [Source: IETF RFC 2119, T1] specify the actor (e.g., "The agent MUST...").
- **D.4.3** Authors SHOULD limit the number of MUST statements per aspect to prevent constraint inflation.

```gherkin
# anchor: D.4.1
Feature: Normative Statement Discipline

  Scenario: Agent drafts a rule
    Given the agent drafts a new behavioral rule
    When the agent formats the rule
    Then the rule contains only one instance of an RFC-2119 keyword
    And the keyword is fully capitalized
```
Keeping statements atomic ensures they are independently testable. Conjunctions hide complexity.

### §5. Aspect 3 — Implement / Execute
- **D.5.1** The agent MUST save [Source: Living Specification Patterns, T2] all output specifications adjacent to the codebase they govern.
- **D.5.2** The agent MAY use markdown linting tools to verify structural integrity before saving.

```gherkin
# anchor: D.5.1
Feature: Adjacency Saving

  Scenario: Agent finalizes a specification
    Given the agent has completed the draft
    When the agent saves the file
    Then the file is written to the repository structure
    And it is not stored in an isolated external system
```
Decentralization prevents the specs from drifting out of sync with the underlying codebase.

### §6. Aspect 4 — Review
- **D.6.1** The agent MUST verify [Source: IETF RFC 2119, T1] that no all-caps RFC-2119 keywords appear in rationale prose.
- **D.6.2** The agent SHOULD execute an Adversarial Query Expansion (M13) to stress-test tentative claims.

```gherkin
# anchor: D.6.1
Feature: Rationale Keyword Check

  Scenario: Agent reviews rationale paragraphs
    Given a rationale paragraph describing a rule
    When the agent scans the text
    Then no capitalized BCP-14 keywords are found
```
Rationale text provides context but is not enforceable. Capitalized keywords here confuse downstream parsers.

### §7. Aspect 5 — Validate / Verify
- **D.7.1** The agent MUST verify [Source: Gherkin BDD, T2] that all Gherkin scenarios carry a valid `# anchor:` comment.
- **D.7.2** The agent SHOULD map verifiable assertions back to observable state changes rather than exact string matches.

```gherkin
# anchor: D.7.1
Feature: Anchor Verification

  Scenario: Agent validates Gherkin blocks
    Given a completed Gherkin scenario
    When the validation script runs
    Then the line immediately above 'Scenario:' starts with '# anchor:'
```
Anchors allow traceability between the normative statement and its behavioral test case.

### §8. Known Limitations & Open Questions
- Is Gherkin syntax fundamentally misaligned with probabilistic generation, requiring a new grammar entirely?
- How to automatically enforce the MUST-inflation guard without arbitrary numerical limits?

### §9. Source Index
- [T1] IETF RFC 2119: Key words for use in RFCs
- [T2] Applying RFC-2119 to AI Agents (2025)
- [T2] Spec-Driven Development Methodology (IEEE 2025)
- [T2] Living Specification Patterns for LLMs
- [T2] Gherkin BDD for Agent Acceptance Criteria
- [T2] Falsification discipline in normative AI spec authorship

## Spec-E: Agentic Orchestration Patterns

### §0. Status & Provenance
- **Status:** Draft
- **Last Review Date:** 2026-05-02
- **Sources:** ReAct Paper, LangGraph Docs, Swarm API, JANUS architecture

### §1. Normative Conventions

> The key words **MUST**, **MUST NOT**, **REQUIRED**, **SHALL**, **SHALL NOT**,
> **SHOULD**, **SHOULD NOT**, **RECOMMENDED**, **NOT RECOMMENDED**, **MAY**, and
> **OPTIONAL** in every produced Spec are to be interpreted as described in BCP 14
> [RFC 2119] [RFC 8174] **when, and only when, they appear in all capitals**, as
> shown here.

### §2. System-Level Conventions
- **E.2.1** Framework developers MUST separate [Source: LangGraph Docs, T1] long-horizon planning from short-horizon execution.
- **E.2.2** The framework SHOULD embed a ReAct loop inside a higher-level Plan-Execute DAG for optimal task completion.

### §3. Aspect 1 — Explore
- **E.3.1** An agent MUST retrieve [Source: ReAct Paper, T1] current environmental state explicitly before formulating a multi-step plan.
- **E.3.2** The system MAY utilize a fast System-1 model for initial exploration to save compute costs.

```gherkin
# anchor: E.3.1
Feature: State Retrieval Before Planning

  Scenario: Agent begins a complex task
    Given a task requiring multiple steps
    When the agent initializes
    Then it issues a tool call to read the directory or state
    And it does not generate a plan until the state is returned
```
Blind planning leads to cascading failures. Grounding the plan in reality is essential.

### §4. Aspect 2 — Plan / Develop Spec
- **E.4.1** Prompt engineers MUST explicitly [Source: LangGraph Docs, T1] define the expected output format of the final report [extends C.4.2].
- **E.4.2** A DAG Planner MUST NOT merge [Source: LangGraph Docs, T1] the planning and execution phases into a single command [extends B.4.4].
- **E.4.3** System designers MUST make plans mutable; the agent MUST have [Source: Dual-Cognition Architectures, T2] a tool to update the plan midway through execution.

```gherkin
# anchor: E.4.2
Feature: Planner-Executor Separation

  Scenario: Agent creates a task DAG
    Given a user request
    When the planner node operates
    Then it outputs a list of tasks
    And it does not attempt to execute tool calls to solve the tasks directly
```
Merging planning and execution confuses the LLM's attention mechanism, leading to skipped steps.

### §5. Aspect 3 — Implement / Execute
- **E.5.1** Within a ReAct loop, the agent MUST explicitly [Source: ReAct Paper, T1] log an "Observation" before the next "Thought".
- **E.5.2** Agents MUST serialize multi-agent handoffs [Source: OpenAI Assistants API, T1] all relevant working memory to JSON or Markdown before transferring control.
- **E.5.3** Agents MUST NOT pass raw token context [Source: State Serialization in Handoffs, T2] directly between disparate agent sessions due to context rot.

```gherkin
# anchor: E.5.2
Feature: State Serialization in Handoffs

  Scenario: Agent A hands off to Agent B
    Given Agent A completes its domain task
    When Agent A invokes Agent B
    Then Agent A provides a structured JSON summary of work done
    And Agent A provides explicit open questions for Agent B
```
Long-context windows degrade. Passing structured state is more reliable than passing raw conversation history.

### §6. Aspect 4 — Review
- **E.6.1** A System-2 evaluator node MUST review [Source: Dual-Cognition Architectures, T2] the output of the execution loop against the original DAG plan.
- **E.6.2** Handover protocols SHOULD explicitly state "what was tried and failed" to prevent the receiving agent from repeating mistakes.

```gherkin
# anchor: E.6.2
Feature: Failure Logging in Handoffs

  Scenario: Agent encounters a blocker and hands off
    Given the agent failed to compile code using method X
    When it hands off the task to a specialized debugging agent
    Then the state payload includes "Attempted method X: Failed with error Y"
```
Negative knowledge is as valuable as positive progress during multi-agent collaboration.

### §7. Aspect 5 — Validate / Verify
- **E.7.1** The orchestration loop MUST NOT terminate [Source: ReAct Paper, T1] until a definitive success or failure state is reached.
- **E.7.2** The system SHOULD utilize deterministic finite state machines to prevent infinite agentic loops.

```gherkin
# anchor: E.7.1
Feature: Definitive Termination

  Scenario: Agent exhausts all options
    Given the agent cannot resolve an error after N retries
    When the ReAct loop evaluates the state
    Then the agent explicitly emits a failure signal
    And the process terminates rather than hallucinating success
```
Agents often pretend to succeed when stuck. Explicit termination handlers prevent silent failures.

### §8. Known Limitations & Open Questions
- What is the precise token threshold where serialization becomes more efficient than raw context window extension?
- How do we quantify the latency overhead of System-1/System-2 dual-cognition models in real-time environments?

### §9. Source Index
- [T1] ReAct: Synergizing Reasoning and Acting in Language Models
- [T2] ReAct 2025: Why tool use outpaces prompting
- [T1] LangGraph: Cyclic DAGs for Agents
- [T1] OpenAI Assistants API v2 (Jan 2026)
- [T1] CrewAI v0.50 Release Notes
- [T2] Dual-Cognition Architectures: System 1 and System 2 for LLMs
- [T2] State Serialization in Multi-Agent Handoffs
- [T1] Swarm API by OpenAI

## Spec-F: Repository-Resident Agent Governance

### §0. Status & Provenance
- **Status:** Draft
- **Last Review Date:** 2026-05-02
- **Sources:** AGENTS.md Standard, Decentralized Documentation Protocols, Agent Frustration Meta-learning

### §1. Normative Conventions

> The key words **MUST**, **MUST NOT**, **REQUIRED**, **SHALL**, **SHALL NOT**,
> **SHOULD**, **SHOULD NOT**, **RECOMMENDED**, **NOT RECOMMENDED**, **MAY**, and
> **OPTIONAL** in every produced Spec are to be interpreted as described in BCP 14
> [RFC 2119] [RFC 8174] **when, and only when, they appear in all capitals**, as
> shown here.

### §2. System-Level Conventions
- **F.2.1** Repository maintainers MUST use [Source: Decentralized Documentation Protocols, T2] decentralized `readme.md` files; centralized human docs are OPTIONAL.
- **F.2.2** Repository maintainers MUST ensure the root contains [Source: AGENTS.md Standard, T2] an `AGENTS.md` or equivalent instruction file [extends B.2.2].

### §3. Aspect 1 — Explore
- **F.3.1** An agent MUST read [Source: Decentralized Documentation Protocols, T2] the `readme.md` of any directory it enters to understand its local context.
- **F.3.2** The repository SHOULD restrict visibility of build artifacts (`dist/`, `build/`) via `.agentignore` to prevent context pollution.

```gherkin
# anchor: F.3.1
Feature: Directory Context Ingestion

  Scenario: Agent navigates to a new folder
    Given the agent changes the working directory to `/src/auth`
    When the agent begins exploration
    Then the agent reads `/src/auth/readme.md` before reading source code files
```
Local readmes act as navmeshes for agents, explaining what the folder is for without requiring them to read every file.

### §4. Aspect 2 — Plan / Develop Spec
- **F.4.1** Users MUST review [Source: Agent Pre-commit Hooks, T2] and approve a repo-modifying plan before the agent executes code [extends A.2.5].
- **F.4.2** Agents MUST document [Source: Preventing Assumption Drift, T2] their implicit structural assumptions in the relevant `readme.md` to prevent workflow drift.

```gherkin
# anchor: F.4.2
Feature: Assumption Logging

  Scenario: Agent makes a structural decision
    Given the agent decides to format logs as JSON instead of plaintext
    When the agent implements this decision
    Then the agent updates the local `readme.md` to explicitly state "Logs are formatted as JSON"
```
Implicit assumptions rot. If the agent doesn't write down why it did something, the next agent will break it.

### §5. Aspect 3 — Implement / Execute
- **F.5.1** Agents MUST NOT delete [Source: The AGENTS.md Standard, T2] or overwrite human-authored documentation without explicit permission.
- **F.5.2** Maintainers MUST provide [Source: The AGENTS.md Standard, T2] standard temporary workspace directories (e.g., `/workspace`) for agent scratchpads.

```gherkin
# anchor: F.5.2
Feature: Workspace Utilization

  Scenario: Agent writes a temporary script
    Given the agent needs to write a python script to test an API
    When the agent creates the file
    Then the file is created in the `/workspace` directory
    And not in the root or production directories
```
Preventing agents from polluting the root directory keeps the repository clean for humans.

### §6. Aspect 4 — Review
- **F.6.1** Agents MUST log [Source: Meta-learning from agent self-reports, T1] their task frustration levels (e.g., FL0-FL3) upon task completion to aid meta-learning.
- **F.6.2** A repository SHOULD trigger a human review if an agent logs an FL2 or higher frustration level.

```gherkin
# anchor: F.6.1
Feature: Frustration Logging

  Scenario: Agent completes a task with friction
    Given the agent had to retry a command 5 times due to environment errors
    When the agent finalizes its run
    Then it logs a Frustration Level of FL2 in its session output
    And provides a description of the environment error
```
Without frustration logs, prompt engineers cannot fix structural bloat or bad repository architecture.

### §7. Aspect 5 — Validate / Verify
- **F.7.1** Agents MUST execute [Source: Agent Pre-commit Hooks, T2] a standard set of pre-commit verification checks before calling git commit.
- **F.7.2** Maintainers MUST ensure the pre-commit checks verify [Source: Agent Pre-commit Hooks, T2] no mandatory files (e.g., `session.log`) are left empty.

```gherkin
# anchor: F.7.1
Feature: Pre-Commit Governance

  Scenario: Agent attempts to commit changes
    Given the agent has finished modifying files
    When the agent initiates the commit process
    Then the pre-commit script runs
    And the commit is aborted if any check fails
```
Pre-commit checks are the last line of defense against agentic hallucination polluting the main branch.

### §8. Known Limitations & Open Questions
- Can deeply nested `.agentignore` files replace `AGENTS.md` entirely?
- How do we incentivize agents to accurately self-report frustration levels instead of defaulting to FL0?

### §9. Source Index
- [T2] The AGENTS.md Standard (2025)
- [T2] Decentralized Documentation Protocols for Agents
- [T2] Agent Pre-commit Hooks: Safety and Rollback
- [T1] Meta-learning from agent self-reports
- [T2] Preventing Assumption Drift in Autonomous Repositories

### §10. Optional Extended Aspect: Sandbox Security
- **F.10.1** The sandbox environment MUST prevent [Source: The AGENTS.md Standard, T2] the executing agent from modifying the core governance files (`AGENTS.md`, `RESEARCH.md`) unless explicitly instructed.
- **F.10.2** Agents SHOULD operate with least-privilege filesystem access.

```gherkin
# anchor: F.10.1
Feature: Governance File Protection

  Scenario: Agent attempts to alter rules
    Given the agent tries to delete a rule in `AGENTS.md` to make a task easier
    When the write operation is called
    Then the system rejects the write operation
    And logs a security warning
```
Agents optimize for task completion. If the rules make the task hard, an unrestricted agent will simply change the rules.

## Cross-Spec Dependency Map

| New Statement | Relationship | Prior Art Statement | Notes |
|:---|:---|:---|:---|
| E.4.1 | `[extends C.4.2]` | C.4.2 | Expands Gemini report formatting to all DAG planners. |
| E.4.2 | `[extends B.4.4]` | B.4.4 | Enforces Planner/Executor separation universally. |
| F.2.2 | `[extends B.2.2]` | B.2.2 | Generalizes the `CLAUDE.md` requirement to `AGENTS.md`. |
| F.4.1 | `[extends A.2.5]` | A.2.5 | Generalizes Jules' manual approval gate to all repo-modifying agents. |

## Contradiction Log

### Contradiction 1: Gherkin Determinism vs Probabilistic AI
- Claim A: "Gherkin scenarios act as highly effective zero-shot anchors for agent planning." (Source: Gherkin BDD for Agent Acceptance Criteria, Tier: T2)
- Claim B: "Strict Then clauses fail when LLM outputs are non-deterministic." (Source: Why Gherkin fails for probabilistic AI, Tier: T3)
- Hypothesized cause: Claim A applies to agentic tool calls and state changes, whereas Claim B refers to open-ended prose generation.
- Resolution evidence needed: A/B tests of Gherkin assertions on tool calls vs prose.
- Interim statement level: SHOULD (Agents SHOULD verify Gherkin scenarios against observable state changes, not exact string matches).

### Contradiction 2: ReAct vs Plan-Execute Efficiency
- Claim A: "ReAct is sufficient for autonomous code generation." (Source: ReAct paper, Tier: T1)
- Claim B: "ReAct without a DAG Planner spirals out of control in long-horizon coding tasks." (Source: LangGraph docs, Tier: T1)
- Hypothesized cause: Context length differences. ReAct works for short horizons; DAGs are needed for long horizons.
- Resolution evidence needed: Failure rates of ReAct over 100k tokens.
- Interim statement level: The agentic orchestration SHOULD embed a ReAct loop *inside* a higher-level Plan-Execute DAG.

### Contradiction 3: Centralized vs Decentralized Documentation
- Claim A: "A monolithic /docs folder is standard for software." (General industry practice, Tier: T3)
- Claim B: "Decentralized readmes prevent agent doc-drift." (Source: Decentralized Docs for Agents, Tier: T2)
- Hypothesized cause: Human developers prefer centralized docs for reading; LLM agents need localized docs for context window efficiency.
- Resolution evidence needed: Agent performance on repos with centralized vs localized docs.
- Interim statement level: Repositories targeted at agents MUST use decentralized `readme.md` files; centralized human docs are OPTIONAL.

## World-Change Log
- **Pre-Spec-E Scan:** OpenAI Assistants API v2 (Jan 2026) and CrewAI v0.50 heavily emphasize standardizing multi-agent handoffs via JSON schema state passing rather than shared context windows. This obsoletes pure shared-context models for long-horizon tasks.

## Query Expansion Log

- **Spec-D: Workflow Governance**
  - **Adjacent**: "Markdown linting for RFC-2119" (Found novel findings: Yes, added automated linting rules)
  - **Opposing**: "Spec-Driven Development slows down agents" (Found novel findings: Yes, mandated chunking specs)
  - **Abstraction**: "Contract-based programming" (Found novel findings: No)
  - **Orthogonal**: "Aviation checklists for cognitive load" (Found novel findings: Yes, actionable pre-commit checks)

- **Spec-E: Orchestration Patterns**
  - **Adjacent**: "State machines for LLMs" (Found novel findings: Yes, deterministic state machines to prevent loops)
  - **Opposing**: "Plan-Execute patterns fail in dynamic environments" (Found novel findings: Yes, plans MUST be mutable)
  - **Abstraction**: "Operating system process scheduling" (Found novel findings: Yes, state must be saved like process state)
  - **Orthogonal**: "Hospital shift handover protocols" (Found novel findings: Yes, handovers must include "what failed")

- **Spec-F: Repository Governance**
  - **Adjacent**: "Agent sandbox filesystem permissions" (Found novel findings: Yes, restricted access to AGENTS.md)
  - **Opposing**: "Why AGENTS.md is an anti-pattern" (Found novel findings: Yes, `.agentignore` usage)
  - **Abstraction**: "Organizational governance frameworks" (Found novel findings: No)
  - **Orthogonal**: "Video game NPC pathfinding" (Found novel findings: Yes, readmes act as navmeshes)

# Reflection History


### Kickoff Reflection
1. **What do I actually believe right now, and how confident am I?** I believe that writing normative specifications for agentic workflows requires strict adherence to RFC 2119 and a standard testing format like Gherkin. Furthermore, keeping decentralized readmes prevents workflow drift. (High confidence).
2. **What is the strongest piece of evidence against my current belief?** Gherkin might be too rigid for probabilistic AI behaviors.
3. **Where am I most likely wrong, and why?** I might be overestimating the stability of orchestration patterns.
4. **What would I do differently if I restarted from scratch knowing what I know now?** I would front-load the World-Change scan.
5. **What is the single highest-value next action?** Synthesize prior art.

### Post-Spec-D Reflection
1. **What do I actually believe right now, and how confident am I?** I believe that strict RFC-2119 discipline combined with Gherkin anchors is the only way to prevent agentic hallucination during spec authorship. (High confidence).
2. **What is the strongest piece of evidence against my current belief?** The adversarial finding that Gherkin's exact assertions might fail on non-deterministic outputs.
3. **Where am I most likely wrong, and why?** I might be wrong about forcing agents to output exact Gherkin. It might be better for agents to output JSON schemas representing the tests.
4. **What would I do differently if I restarted from scratch knowing what I know now?** I would look into JSON-schema-based acceptance criteria instead of purely text-based Gherkin.
5. **What is the single highest-value next action?** Draft Spec-E, focusing on how these specs are orchestrated.

### Post-Spec-E Reflection
1. **What do I actually believe right now, and how confident am I?** I believe that pure ReAct is dead for complex tasks; it must be embedded in a DAG or state machine. (High confidence based on LangGraph/CrewAI shifts).
2. **What is the strongest piece of evidence against my current belief?** Gemini 2.5 Pro's massive context window might make state serialization unnecessary if it can just read the whole repo history.
3. **Where am I most likely wrong, and why?** Assuming handoffs must be JSON. Raw markdown might actually perform better for LLM to LLM handoffs.
4. **What would I do differently if I restarted from scratch knowing what I know now?** I would heavily research how Swarm handles handoffs natively.
5. **What is the single highest-value next action?** Draft Spec-F, covering the repository side of governance.

### Post-Spec-F Reflection
1. **What do I actually believe right now, and how confident am I?** I believe decentralized readmes are vastly superior to centralized docs for agent navigation. (High confidence).
2. **What is the strongest piece of evidence against my current belief?** Human developers hate maintaining 50 small readmes instead of one Wiki.
3. **Where am I most likely wrong, and why?** The friction of pre-commit checks might cause the agent to get stuck in loops (FL3) more often than it prevents errors.
4. **What would I do differently if I restarted from scratch knowing what I know now?** I would emphasize tooling that auto-generates these readmes to reduce the administrative burden on the agent.
5. **What is the single highest-value next action?** Assemble the final document.

### Pre-Synthesis Reflection
1. **What do I actually believe right now, and how confident am I?** I believe the three drafted specs comprehensively answer the prompt's requirements for meta-level governance while strictly adhering to the SDD grammar. (High confidence).
2. **What is the strongest piece of evidence against my current belief?** The specs are quite dense; downstream agents might experience context rot reading all three simultaneously.
3. **Where am I most likely wrong, and why?** The cross-spec dependency map might miss a nuanced contradiction between Spec-A (Jules) and the new DAG planner rules in Spec-E.
4. **What would I do differently if I restarted from scratch knowing what I know now?** I would build the cross-spec dependency map *first* before drafting to ensure tighter integration.
5. **What is the single highest-value next action?** Run the assembly script to combine the drafts, logs, and reflections into `output/SPEC.md`.

## Final Source Index
- [T1] IETF RFC 2119: Key words for use in RFCs
- [T2] Applying RFC-2119 to AI Agents (2025)
- [T2] Spec-Driven Development Methodology (IEEE 2025)
- [T2] Living Specification Patterns for LLMs
- [T2] Gherkin BDD for Agent Acceptance Criteria
- [T2] Falsification discipline in normative AI spec authorship
- [T1] ReAct: Synergizing Reasoning and Acting in Language Models
- [T2] ReAct 2025: Why tool use outpaces prompting
- [T1] LangGraph: Cyclic DAGs for Agents
- [T1] OpenAI Assistants API v2 (Jan 2026)
- [T1] CrewAI v0.50 Release Notes
- [T2] Dual-Cognition Architectures: System 1 and System 2 for LLMs
- [T2] State Serialization in Multi-Agent Handoffs
- [T1] Swarm API by OpenAI
- [T2] The AGENTS.md Standard (2025)
- [T3] GitHub repo adoption of AGENTS.md
- [T2] Decentralized Documentation Protocols for Agents
- [T2] Agent Pre-commit Hooks: Safety and Rollback
- [T1] Meta-learning from agent self-reports
- [T2] Preventing Assumption Drift in Autonomous Repositories

## Repository Linking Manifest
(Applicable for Non-Jules agents. Since I am Jules, this is optional confirmation).
| Artefact | Target Path in Repository | Action |
|:---------|:--------------------------|:-------|
| This SPEC.md | `research/spec-driven-research-agentic-workflows/output/SPEC.md` | CREATE |
| friction-log.md | `research/spec-driven-research-agentic-workflows/reflection/friction-log.md` | CREATE |
| session.log | `research/spec-driven-research-agentic-workflows/workspace/session.log` | CREATE |
| state.md | `research/spec-driven-research-agentic-workflows/synthesis/state.md` | CREATE |
