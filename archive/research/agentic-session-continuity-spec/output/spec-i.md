## Spec-I: Cross-Session Continuity Protocol

### §0. Status & Provenance
- **Target Subject:** Cross-Session Continuity Protocol (Handoffs & Re-entry)
- **Status:** Proposed
- **Last Review Date:** 2026-05-03
- **Sources:** LangGraph checkpointing docs [T1], Anthropic Managed Agents docs [T1], Google A2A protocol spec [T1].

### §1. Normative Conventions
The key words **MUST**, **MUST NOT**, **REQUIRED**, **SHALL**, **SHALL NOT**, **SHOULD**, **SHOULD NOT**, **RECOMMENDED**, **NOT RECOMMENDED**, **MAY**, and **OPTIONAL** in every produced Spec are to be interpreted as described in BCP 14 [RFC 2119] [RFC 8174] **when, and only when, they appear in all capitals**, as shown here.

### §2. System-Level Conventions
- **I.2.1** Cross-session handoffs MUST utilize a standardized serialization format to ensure epistemic continuity across agent boundaries.

### §3. Aspect 1 — Explore
# anchor: I.3.1
Feature: Staleness Detection
  Scenario: Agent resumes paused session
    Given an agent re-entering a previously paused long-horizon task
    When the agent initializes its context
    Then the agent MUST verify the staleness of its world-model against current ground truth

- **I.3.1** The agent MUST verify world-model staleness before proceeding with execution after a cross-session gap. [Source: LangGraph checkpointing documentation, T1]
- **Rationale:** The environment (files, APIs, databases) may have been modified by humans or other agents while the primary agent was asleep.

### §4. Aspect 2 — Plan / Develop Context Strategy
# anchor: I.4.1
Feature: Handoff Contract
  Scenario: Orchestrator hands task to execution agent
    Given a multi-agent orchestrator managing a complex workflow
    When the orchestrator delegates a sub-task to an execution agent
    Then the orchestrator MUST provide a serialized handoff artifact

- **I.4.1** The orchestrator MUST provide a serialized handoff artifact when delegating tasks across agent boundaries. [extends E.2.1] [Source: Google A2A protocol specification, T1]
- **Rationale:** Relying on implicit shared memory between agents leads to hallucinated context and task drift.

### §5. Aspect 3 — Implement / Execute
# anchor: I.5.1
Feature: Session Serialization Schema
  Scenario: Agent serializes state for handoff
    Given an agent preparing to externalize its session log
    When the agent generates the serialization artifact
    Then the agent MUST distill raw tool outputs into an event stream
    And the artifact MUST use a JSON schema

- **I.5.1** A cross-session handoff artifact MUST distill raw tool outputs into an event stream schema.
- **I.5.3** A cross-session handoff artifact MAY retain pointers to the raw data block. [Source: Anthropic Managed Agents documentation, T1]
- **Rationale:** Sending 100k tokens of raw `stdout` to a new agent immediately exhausts its context window. Distilled events ("Command X failed with error Y") preserve continuity efficiently.
- **I.5.2** The serialization artifact MUST be formatted using a JSON schema rather than unstructured text. [Source: Google A2A protocol specification, T1]
- **Rationale:** JSON schemas ensure deterministic parsing by the receiving agent.

### §6. Aspect 4 — Review
# anchor: I.6.1
Feature: Handoff Artifact Review
  Scenario: Receiving agent evaluates handoff
    Given an agent receiving a handoff artifact
    When the agent parses the artifact
    Then the agent SHOULD log any missing or ambiguous fields

- **I.6.1** The receiving agent SHOULD log missing or ambiguous fields in the handoff artifact before beginning execution. [Confidence: low]
- **Rationale:** Proactive logging of bad handoffs helps debug orchestration failures before they cause destructive actions.

### §7. Aspect 5 — Validate / Verify
# anchor: I.7.1
Feature: Two-Phase Commit Validation
  Scenario: Agent checkpoints external API states
    Given an agent interacting with external stateful APIs
    When the agent serializes its session
    Then the agent MUST ensure external transactions are fully committed or rolled back

- **I.7.1** The session checkpointing mechanism SHOULD ensure external API states are consistent before finalizing the serialization. [Confidence: low]
- **Rationale:** Pausing an agent midway through a non-idempotent API sequence causes irrecoverable state corruption upon resume.

### §8. Known Limitations & Open Questions
- Standardizing JSON schemas across different vendors (Google A2A vs OpenAI Swarm) remains an ongoing industry challenge.
- Distilling tool outputs requires LLM calls, adding cost and latency to the handoff process.

### §9. Source Index
- [T1] LangGraph checkpointing documentation
- [T1] Anthropic Managed Agents documentation
- [T1] Google A2A protocol specification

### §10. Optional Extended Aspect: Trust Anchoring
# anchor: I.10.1
Feature: Artifact Tamper Verification
  Scenario: Agent validates artifact origin
    Given an agent reconstituting context from a handoff artifact
    When the agent loads the artifact
    Then the agent SHOULD verify the cryptographic signature of the artifact

- **I.10.1** The agent SHOULD verify the origin and integrity of the handoff artifact to ensure it has not been tampered with. [Confidence: low]
- **Rationale:** In distributed, multi-agent systems, unverified context injection is a severe security vulnerability.
