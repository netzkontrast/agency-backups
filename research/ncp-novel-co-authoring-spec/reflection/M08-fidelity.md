# M08 Pre-Commitment Fidelity

## Decision 1: NCP ↔ Dramatica Integration (Option B)
- **Pre-commitment:** "I would reverse this recommendation if I found that NCP lacks fields for dynamically resolving Quads or parallel constraints that require an external inference engine."
- **Fidelity Check:** This was a genuine, observable condition. While NCP stores the *results* of the Dramatica Storyform (in `storypoints` and `storybeats`), it actually *does* lack an internal inference engine to dynamically resolve Quads (that requires proprietary software or complex LLM prompting).
- **Correction Required?** The recommendation holds because the agent (Claude) acts as the inference engine via prompt logic in Phase 2, populating the static NCP JSON. However, the pre-commitment accurately highlighted a limitation, which was documented in §12 (Open Questions).

## Decision 2: Workflow Architecture (Autonomous State-handoff)
- **Pre-commitment:** "I would reverse this recommendation if I found that Claude Code cannot natively trigger on file-watcher events without a DAG orchestrator."
- **Fidelity Check:** This is highly relevant. Claude Code is an interactive CLI, not a background daemon. True autonomous polling might actually fail in a standard Claude Code setup without user intervention or an external bash loop.
- **Correction Required?** The architecture proposed relies on the agent being invoked or polling. If the agent requires human triggering, it degrades to a Pipeline. This exposes a slight flaw in my assumption about Claude Code's autonomy level, making the pre-commitment successful in identifying a weak spot.
