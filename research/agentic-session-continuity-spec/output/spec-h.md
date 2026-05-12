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
