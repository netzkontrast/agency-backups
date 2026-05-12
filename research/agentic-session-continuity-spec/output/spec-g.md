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
