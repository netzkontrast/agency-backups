# Research Tracks

**Status:** Initialized — awaiting research execution

This file will contain per-track notes for each of the three target Specs.

## Track 1: Spec-G — Context Engineering Layer

**Seed hypothesis:** The Write/Select/Compress/Isolate framework from Anthropic's
engineering blog provides the T1 foundation; the gap is normative triggering conditions.

**Key open questions:**
- What observable signals MUST trigger compaction (budget threshold, failure signal, or both)?
- What MUST the compaction procedure preserve vs. what MAY it discard?
- How does the Isolate strategy (delegate to subagents) interact with the Compress strategy?
- What is the minimum viable "compaction summary" schema?

## Track 2: Spec-H — Agent Memory Architecture

**Seed hypothesis:** Memory contamination (semantic drift from naive append) is the
primary undocumented failure mode requiring write isolation as the architectural fix.

**Key open questions:**
- What is the normative STM/MTM/LTM boundary definition? (based on decay time? token budget? access frequency?)
- When MUST an agent promote content from STM to LTM vs. let it decay?
- How does graph-enhanced memory (Mem0g, MAGMA) normatively differ from vector-only memory in requirements?
- What constitutes a "memory contamination" event, and what MUST the agent do when one is detected?

## Track 3: Spec-I — Cross-Session Continuity Protocol

**Seed hypothesis:** No cross-framework standard exists; Spec-I must derive minimum viable
requirements from first principles and annotate framework-specific implementations.

**Key open questions:**
- What is the minimum viable session serialization artifact (the handoff contract)?
- What triggers MUST cause a re-entering agent to verify world-model staleness?
- How does Google A2A protocol relate to the internal session handoff problem?
- What is the normative trust anchor for a reconstituted session (how does the agent
  know the artifact it's reading hasn't been corrupted or tampered with)?
