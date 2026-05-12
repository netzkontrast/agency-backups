---
type: research
status: completed
slug: agentic-session-continuity-spec
summary: "Normative specs (G/H/I) for context engineering, agent memory architecture, and cross-session continuity protocols in long-horizon agentic pipelines."
created: 2026-05-04
updated: 2026-05-04
research_phase: complete
research_executes_prompt: ""
research_friction_level: FL0
---

# Agentic Long-Horizon Context Continuity

## Executive Summary
This specification defines normative best practices for preserving agent epistemic continuity across context window boundaries, multi-session gaps, and cross-agent handoffs. It introduces three new architectural layers: Spec-G (Context Engineering Layer), Spec-H (Agent Memory Architecture), and Spec-I (Cross-Session Continuity Protocol). This document extends the previous workflow and repository governance specifications (Spec-A through Spec-F) to address the 'lost-in-the-middle' phenomena and memory contamination observed in >300k token pipelines.

## Common Conventions Across Specs
These cross-cutting rules apply to G, H, and I:
- All operations must strictly document state externalization.
- Soft token thresholds supersede hard byte limits.
- Cryptographic hashes are used where stated to prevent undetected data decay.

## Spec-G: Context Engineering Layer

### §0. Status & Provenance
- **Target Subject:** Context Engineering Layer (Write/Select/Compress/Isolate)
- **Status:** Proposed
- **Last Review Date:** 2026-05-03
- **Sources:** Anthropic context compaction cookbook [T1], Anthropic engineering blog [T1], Chroma Research [T2].

### §1. Normative Conventions
The key words **MUST**, **MUST NOT**, **REQUIRED**, **SHALL**, **SHALL NOT**, **SHOULD**, **SHOULD NOT**, **RECOMMENDED**, **NOT RECOMMENDED**, **MAY**, and **OPTIONAL** in every produced Spec are to be interpreted as described in BCP 14 [RFC 2119] [RFC 8174] **when, and only when, they appear in all capitals**, as shown here.

### §2. System-Level Conventions
- **G.2.1** The context management layer MUST monitor the active token count continuously.

### §3. Aspect 1 — Explore
# anchor: G.3.1
Feature: Wide Exploration
  Scenario: Agent encounters massive directory
    Given an agent exploring a repository exceeding 300k tokens
    When the agent needs to read the entire directory
    Then the agent MUST delegate the reading to a specialized subagent

- **G.3.1** The agent MUST isolate exploration context by delegating wide reads to subagents when the target exceeds 30% of the active context budget. [extends B.3.4] [Source: Anthropic engineering blog, T1]
- **Rationale:** Subagent isolation prevents the primary reasoning thread from being overwhelmed by raw file dumps, mitigating the lost-in-the-middle phenomenon.

### §4. Aspect 2 — Plan / Develop Context Strategy
# anchor: G.4.1
Feature: Context Strategy Planning
  Scenario: Agent plans memory usage
    Given an agent initiating a long-horizon task
    When the agent constructs its execution plan
    Then the agent SHOULD declare a soft context budget limit

- **G.4.1** The agent SHOULD declare an explicit soft context budget limit before beginning execution. [Source: Chroma Research, T2]
- **Rationale:** A declared budget allows the agent to anticipate compaction rather than hitting hard system limits unexpectedly.

### §5. Aspect 3 — Implement / Execute
# anchor: G.5.1
Feature: Context Compaction Gate
  Scenario: Agent triggers compaction before context limit
    Given an agent whose active context has exceeded its declared budget threshold
    When the agent begins a new reasoning step
    Then the agent MUST pause execution and invoke the context compaction procedure
    And the agent writes the compaction summary to the external memory store
    And the agent resumes execution with the compacted context plus the raw tail

- **G.5.1** The agent MUST trigger compaction before beginning any new reasoning step when the active context exceeds the declared context budget threshold. [extends B.3.4] [Source: Anthropic context compaction cookbook, T1]
- **Rationale:** Proactive compaction prevents sudden execution failure and ensures semantic continuity is maintained while the agent is in a stable state.
- **G.5.2** The agent MUST write the compaction summary to the persistent external store before discarding the raw context segments. [Source: Anthropic Managed Agents, T1]
- **Rationale:** The summary acts as the bridge for future context reconstitution.

### §6. Aspect 4 — Review
# anchor: G.6.1
Feature: Context Quality Review
  Scenario: Agent evaluates compressed context
    Given an agent that has just compacted its context
    When the agent performs its next reasoning step
    Then the agent MAY optionally query the raw logs if the summary is insufficient

- **G.6.1** The agent MAY query the raw externalized logs if the compacted context lacks the specificity required for the current task. [Source: Anthropic Managed Agents, T1]
- **Rationale:** Compaction inherently loses detail; a fallback retrieval mechanism ensures critical edge cases are not permanently lost.

### §7. Aspect 5 — Validate / Verify
# anchor: G.7.1
Feature: Context Verification
  Scenario: Agent verifies context integrity
    Given an agent resuming from a compacted state
    When the agent executes a state-modifying action
    Then the agent MUST verify its current context accurately reflects the physical state

- **G.7.1** The agent MUST verify its internal state model against the external environment after a compaction event. [Source: Anthropic context compaction cookbook, T1]
- **Rationale:** This ensures that no critical constraints were lost during the compression process.

### §8. Known Limitations & Open Questions
- Compaction algorithms often struggle to decide which variables are "safe" to drop.
- The exact ratio of raw tail vs compacted head is still task-dependent.

### §9. Source Index
- [T1] Anthropic context compaction cookbook
- [T1] Anthropic engineering blog: Effective context engineering for AI agents
- [T1] Anthropic Managed Agents documentation
- [T2] Chroma Research: Context Rot study

### §10. Optional Extended Aspect: Emergency Recovery
# anchor: G.10.1
Feature: Context Emergency Recovery
  Scenario: Agent loses compacted summary
    Given an agent whose compacted summary is corrupted
    When the agent detects the corruption
    Then the agent MUST halt execution and request human intervention

- **G.10.1** The agent SHOULD halt execution and escalate if its compacted summary is detected as corrupted or missing. [Confidence: low]
- **Rationale:** Operating without a valid summary in a long-horizon task leads to unpredictable and often destructive behavior.

## Spec-H: Agent Memory Architecture

### §0. Status & Provenance
- **Target Subject:** Agent Memory Architecture (STM / MTM / LTM / Graph)
- **Status:** Proposed
- **Last Review Date:** 2026-05-03
- **Sources:** arxiv:2601.01885 [T2], mem0.ai [T2], arxiv:2601.03236 (MAGMA) [T2].

### §1. Normative Conventions
The key words **MUST**, **MUST NOT**, **REQUIRED**, **SHALL**, **SHALL NOT**, **SHOULD**, **SHOULD NOT**, **RECOMMENDED**, **NOT RECOMMENDED**, **MAY**, and **OPTIONAL** in every produced Spec are to be interpreted as described in BCP 14 [RFC 2119] [RFC 8174] **when, and only when, they appear in all capitals**, as shown here.

### §2. System-Level Conventions
- **H.2.1** The memory architecture MUST isolate short-term working memory from long-term semantic memory.

### §3. Aspect 1 — Explore
# anchor: H.3.1
Feature: Memory Namespace Isolation
  Scenario: Agent stores new observation
    Given an agent executing a tool call
    When the agent receives the observation
    Then the agent MUST store the observation in a dedicated short-term namespace
    And the agent MUST NOT append it directly to the global long-term memory

- **H.3.1** The agent MUST use isolated namespaces for short-term memory writes to prevent semantic drift in the global store. [Source: arxiv:2601.01885, T2]
- **Rationale:** Naive appending of raw observations to a global vector store causes memory contamination and degrades retrieval quality over time.

### §4. Aspect 2 — Plan / Develop Context Strategy
# anchor: H.4.1
Feature: Memory Structure Planning
  Scenario: Agent selects memory backend
    Given an agent planning a task requiring multi-hop reasoning
    When the agent initializes its memory connections
    Then the agent SHOULD utilize a graph-enhanced index

- **H.4.1** The orchestrator SHOULD supplement vector retrieval with a graph index when the agent's tasks require multi-hop relationship traversal. [Source: arxiv:2601.03236, T2]
- **Rationale:** Vector stores alone struggle with relational logic. Graph indexes provide explicit edge mapping between entities.

### §5. Aspect 3 — Implement / Execute
# anchor: H.5.1
Feature: Explicit Memory Consolidation
  Scenario: Agent transfers memory to LTM
    Given an agent that has completed a sub-task
    When the agent is ready to clear its short-term memory
    Then the agent SHOULD execute a memory consolidation tool call
    And the agent MUST structure the LTM entry as an externalized observation

- **H.5.1** The agent SHOULD execute memory consolidation explicitly via tool calls rather than relying on automatic background policies. [Source: arxiv:2601.01885, T2]
- **Rationale:** Explicit tool usage forces the agent to summarize and justify the semantic value of the memory, reducing noise.
- **H.5.2** The memory architecture MUST structure consolidated LTM entries in accordance with the externalized Observation log schema. [extends E.3.2] [Source: mem0.ai, T2]
- **Rationale:** Standardizing the LTM schema ensures interoperability with orchestration logs.

### §6. Aspect 4 — Review
# anchor: H.6.1
Feature: Memory Contamination Check
  Scenario: Agent reviews retrieved memories
    Given an agent that has retrieved context from LTM
    When the agent detects contradictory facts
    Then the agent MAY flag the specific memory block for review

- **H.6.1** The agent MAY flag specific LTM blocks for review if they contradict freshly observed ground truth. [Confidence: low]
- **Rationale:** A self-healing memory architecture requires mechanisms to identify and deprecate stale facts.

### §7. Aspect 5 — Validate / Verify
# anchor: H.7.1
Feature: Memory Retrieval Verification
  Scenario: Agent validates memory relevance
    Given an agent that has performed a memory query
    When the agent receives the retrieval results
    Then the agent MUST verify the results match the current task context

- **H.7.1** The agent MUST verify the relevance of retrieved LTM context before integrating it into its execution plan. [Source: mem0.ai, T2]
- **Rationale:** Blindly trusting vector retrieval can lead to hallucinations if the semantic match is conceptually adjacent but practically irrelevant.

### §8. Known Limitations & Open Questions
- The boundary between Medium-Term Memory (MTM) and LTM is often blurry and implementation-specific.
- Graph databases introduce significant latency overhead compared to pure vector retrieval.

### §9. Source Index
- [T2] arxiv:2601.01885 — Agentic Memory: Unified LTM/STM Management
- [T2] mem0.ai: State of AI Agent Memory 2026
- [T2] arxiv:2601.03236 — MAGMA: Multi-Graph Agentic Memory Architecture

### §10. Optional Extended Aspect: Memory Governance
# anchor: H.10.1
Feature: Intentional Forgetting
  Scenario: Agent deprecates stale memory
    Given an agent that has verified a memory is no longer accurate
    When the agent executes a memory management tool
    Then the agent MUST mark the memory as deprecated rather than hard-deleting it

- **H.10.1** The agent SHOULD mark inaccurate memories as deprecated rather than executing a hard deletion. [Confidence: low]
- **Rationale:** Soft deletion preserves the episodic history of *why* the agent previously believed a false fact, aiding in debugging and audit trails.

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

## Cross-Spec Dependency Map
| New Statement | Extends / Supersedes | Relationship |
|:---|:---|:---|
| G.3.1 | B.3.4 | Extends: Specifies 30% active context limit for delegation |
| G.5.1 | B.3.4 | Extends: B.3.4 identifies context rot threshold; G.5.1 specifies the triggering mechanic |
| H.5.2 | E.3.2 | Extends: E.3.2 mandates externalizing Observation log; H.5.2 specifies the schema of that externalization |
| I.4.1 | E.2.1 | Refines: E.2.1 mandates Planning/Execution separation; I.4.1 adds the handoff contract requirement |

## Contradiction Log

### Contradiction C1: Proactive vs Reactive Compaction
- **Claim A:** Compaction MUST trigger proactively at budget thresholds (Anthropic docs, T1).
- **Claim B:** Compaction MUST trigger reactively upon performance failure (Research Papers, T2).
- **Hypothesized Cause:** Task dependencies. Long-reading favors reactive (retain max data until failure), code-generation favors proactive (maintain clean context window).
- **Evidence for Resolution:** Found that waiting for failure leads to unpredictable tool calls. Proactive is safer for agentic autonomy.
- **Interim Statement:** The agent MUST trigger compaction before beginning any new reasoning step when the active context exceeds the declared context budget threshold.

### Contradiction C2: Save Everything vs Filtered Event Stream
- **Claim A:** Session checkpoints save full state including all messages and tool outputs (LangGraph, T1).
- **Claim B:** Externalized logs save only a curated, distilled event stream (Anthropic Managed Agents, T1).
- **Hypothesized Cause:** Audience differences. State persistence (debugging/replay) needs everything. Handoff persistence (epistemic continuity) needs only relevant events.
- **Evidence for Resolution:** Spec-E states observation logs must be externalized, but reading raw tool outputs of 100k tokens breaks context.
- **Interim Statement:** A cross-session handoff artifact MUST distill raw tool outputs into an event stream schema, but MAY retain pointers to the raw data block.

### Contradiction C3: Automatic vs Explicit Memory Transfer
- **Claim A:** STM to LTM transfer MUST happen automatically via a background policy (Various Papers, T2).
- **Claim B:** STM to LTM transfer MUST be executed explicitly by the agent using a tool (Agentic Memory paper, T2).
- **Hypothesized Cause:** Supervision vs Autonomy. If humans govern memory, agents use tools. If the system is fully autonomous, background policies are used.
- **Evidence for Resolution:** Explicit tool usage prevents semantic drift by forcing the agent to justify what it is saving.
- **Interim Statement:** The agent SHOULD execute memory consolidation explicitly via tool calls rather than relying on automatic background policies.


## World-Change Log

- **Pre-Spec-H/I Scan:**
  - **LangGraph Checkpoint API Updates (April 2026):** Introduced native time-travel states directly exposed to agent APIs, meaning agents can query past states without full serialization. This impacts Spec-I, as the handoff contract MUST account for native history graphs if available.
  - **Mem0 Core Updates (March 2026):** Graph integration became the default fallback for vector retrieval misses. This reinforces the T2 sources that suggest hybrid graph/vector memory for Spec-H.
  - **Google A2A v1.2 (Feb 2026):** Solidified JSON schema requirements for inter-agent context passing. Spec-I MUST use JSON schemas for state serialization, not raw markdown strings, to remain compliant with industry trends.


## Query Expansion Log

| Spec | Axis | Query | Novel Finding | Conclusion Modified |
|:---|:---|:---|:---|:---|
| Spec-G | Adjacent | "token budget allocation agent" | Yes | Agents MUST dynamically reallocate budget based on tool verbosity |
| Spec-G | Opposing | "against context compaction — what fails" | Yes | Compaction loses edge-case variables; MUST keep raw tail of last N messages |
| Spec-G | Abstraction | "operating system memory paging analogy agent" | No | Only reaffirmed existing Write Context paradigms |
| Spec-G | Orthogonal | "database transaction isolation levels as analogy" | Yes | Isolate Context subagents MUST use read-only parent context views |
| Spec-H | Adjacent | "episodic memory LLM vector graph hybrid" | Yes | Hybrid retrieval SHOULD use episodic logs as edges |
| Spec-H | Opposing | "single flat memory vs tiered memory agent tradeoffs" | Yes | Flat memory is fine for short tasks, tiered MUST be used >24h |
| Spec-H | Abstraction | "cognitive architecture working memory model AI" | No | Parallels existing STM/MTM/LTM |
| Spec-H | Orthogonal | "library science document taxonomy as memory schema" | Yes | LTM namespaces SHOULD adopt explicit semantic tagging |
| Spec-I | Adjacent | "distributed system checkpoint protocol" | Yes | Session checkpoints MUST implement two-phase commit equivalent for external APIs |
| Spec-I | Opposing | "stateless agent better than stateful" | Yes | Emphasized externalizing state explicitly over relying on LLM context |
| Spec-I | Abstraction | "version control as state management analogy" | Yes | Handoff artifacts SHOULD contain a semantic diff (what changed) |
| Spec-I | Orthogonal | "theatrical production prompt book as session continuity" | No | Provided a good analogy but no novel normative requirements |


### Kickoff Reflection
1. **What do I actually believe right now, and how confident am I?** I believe the Anthropic Write/Select/Compress/Isolate framework is fundamentally complete, but missing normative triggers. (High confidence based on prompt hypothesis G-H0). I also believe memory contamination is a huge, under-addressed issue (H-H0). Cross-session handoffs lack a universal standard (I-H0).
2. **What is the strongest piece of evidence against my current belief?** LangGraph might already have robust internal state serialization that obsoletes custom handoff specs.
3. **Where am I most likely wrong, and why?** I might be wrong about memory contamination being purely semantic drift; it could also be attention dilution from bad vector retrieval.
4. **What would I do differently if I restarted from scratch knowing what I know now?** I'd explicitly map out the differences between Google A2A and Anthropic Managed Agents before starting anything else.
5. **What is the single highest-value next action?** Extract the prior art seeds from Spec A/B/C and Spec D/E/F.


### Post-Spec-G Reflection
1. **What do I actually believe right now, and how confident am I?** I believe proactive compaction is superior to reactive compaction for maintaining agent stability. (High confidence).
2. **What is the strongest piece of evidence against my current belief?** Wait-and-see approaches allow for more complete context if the task finishes before the window fills.
3. **Where am I most likely wrong, and why?** The soft budget limit might be too abstract for an agent to enforce reliably without external orchestration.
4. **What would I do differently if I restarted from scratch knowing what I know now?** I'd focus more on the exact structure of the compaction summary.
5. **What is the single highest-value next action?** Draft Spec-H.

### Post-Spec-H Reflection
1. **What do I actually believe right now, and how confident am I?** I believe write isolation is the single most important fix for current memory architectures. (High confidence).
2. **What is the strongest piece of evidence against my current belief?** Some systems use automated clustering to fix semantic drift post-hoc rather than strictly isolating writes.
3. **Where am I most likely wrong, and why?** The distinction between STM and MTM might be purely academic; most production systems just use one DB with different metadata tags.
4. **What would I do differently if I restarted from scratch knowing what I know now?** I would emphasize explicit tagging schemas in the LTM section.
5. **What is the single highest-value next action?** Draft Spec-I.

### Post-Spec-I Reflection
1. **What do I actually believe right now, and how confident am I?** I believe JSON schemas are strictly required for handoffs; pure markdown is too brittle for complex state passing. (High confidence based on Google A2A).
2. **What is the strongest piece of evidence against my current belief?** LLMs are natively better at parsing markdown than deeply nested JSON.
3. **Where am I most likely wrong, and why?** The requirement to distill tool outputs might lose critical stack trace information needed for debugging.
4. **What would I do differently if I restarted from scratch knowing what I know now?** I'd include an explicit mapping of the Anthropic `getEvents()` schema to the Google A2A schema.
5. **What is the single highest-value next action?** Run the pre-synthesis integrity check.

### Pre-Synthesis Reflection
1. **What do I actually believe right now, and how confident am I?** I believe the three drafted specs comprehensively outline the required normative standards for Context Engineering, Agent Memory, and Continuity Protocols. All constraints (RFC 2119, Gherkin anchors) have been met. (High confidence).
2. **What is the strongest piece of evidence against my current belief?** The specs are dense and heavily interrelated; downstream developers might struggle to implement all three simultaneously.
3. **Where am I most likely wrong, and why?** The dependency map might miss subtle contradictions between the new Spec-I serialization schemas and the old Spec-E ReAct loop logs.
4. **What would I do differently if I restarted from scratch knowing what I know now?** I'd establish the cross-spec dependency map *first*, before drafting the individual specs, to ensure tighter cohesion.
5. **What is the single highest-value next action?** Assemble the final document `SPEC.md`.


## Source Index

| Source | Tier | Target Spec | Focus |
|:---|:---|:---|:---|
| Anthropic context compaction cookbook | T1 | Spec-G | Compaction triggers |
| Chroma Research: Context Rot study | T2 | Spec-G | Performance degradation limits |
| Anthropic engineering blog: Effective context | T1 | Spec-G | Framework (Write/Select/Compress/Isolate) |
| arxiv:2601.01885 — Agentic Memory | T2 | Spec-H | Memory contamination & Write isolation |
| mem0.ai: State of AI Agent Memory 2026 | T2 | Spec-H | Production multi-tiered architecture |
| arxiv:2601.03236 — MAGMA | T2 | Spec-H | Graph-enhanced memory |
| LangGraph checkpointing documentation | T1 | Spec-I | State persistence & Staleness |
| Anthropic Managed Agents documentation | T1 | Spec-I | Session log externalization |
| Google A2A protocol specification | T1 | Spec-I | Cross-framework handoff contracts |
