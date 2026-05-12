# Methodology Note

Applied the following methods during research and synthesis:
- **M06 (Source Triangulation):** All factual claims were verified against at least three independent sources or explicitly flagged as `[single-source]`.
- **M07 (Contradiction Log):** Tracked conflicting statements, particularly regarding state-machine handling within NCP vs Workflow phases.
- **M08 (Pre-Commitment):** Established verifiable conditions under which the recommended architectures would be considered invalid before proceeding to write the specification.
- **M10 (First-Principles Decomposition):** Broke down overloaded terms like 'scene' and 'context' into base components to formulate the glossary.
- **M13 (Adversarial Query Expansion):** Forced the search space into adjacent, opposing, and abstraction axes to prevent local-minimum lock-in.

## Contradictions Encountered
1. NCP uses `status` (`candidate`, `draft`, `complete`), but complex workflows require phase-level state tracking.
2. `narrator-position` and `research` phase are valid novel-craft concepts but excluded by the locked input lists.

## Query Expansion Log (Method M13)
- Adjacent: "behavior-driven specification authoring agent context" (Novel: Yes, Mod Conclusion: No)
- Opposing: "why agentic skill ecosystems fragment" (Novel: Yes, Mod Conclusion: No)
- Abstraction: "narrative engineering formal semantics" (Novel: Yes, Mod Conclusion: No)
- Orthogonal: "tabletop RPG narrative engines vs Dramatica" (Novel: No, Mod Conclusion: No)

## Cross-Pollination Log (Phase 2b — Steps (i.a) and (i.c))
- Hidden entities (narrator-position) and schema gaps (model params) checked.
- World-change checks on NCP repo executed using git logs showing recent commits tightening schemas up through early May 2026.
