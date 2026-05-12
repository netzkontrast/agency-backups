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
