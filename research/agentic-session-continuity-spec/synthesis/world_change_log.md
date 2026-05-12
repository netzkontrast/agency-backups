## World-Change Log

- **Pre-Spec-H/I Scan:**
  - **LangGraph Checkpoint API Updates (April 2026):** Introduced native time-travel states directly exposed to agent APIs, meaning agents can query past states without full serialization. This impacts Spec-I, as the handoff contract MUST account for native history graphs if available.
  - **Mem0 Core Updates (March 2026):** Graph integration became the default fallback for vector retrieval misses. This reinforces the T2 sources that suggest hybrid graph/vector memory for Spec-H.
  - **Google A2A v1.2 (Feb 2026):** Solidified JSON schema requirements for inter-agent context passing. Spec-I MUST use JSON schemas for state serialization, not raw markdown strings, to remain compliant with industry trends.
