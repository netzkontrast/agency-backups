
# Research Process Artifacts (not part of SPEC.md)

## Executive Summary
This research concludes that deploying the Narrative Context Protocol (NCP) for AI novel co-authoring should rely on an "Dramatica-In-NCP" architecture, directly embedding Dramatica elements into the native `subtext` arrays. The workflow operates best under an "Autonomous hand-off via NCP-state" pattern where agents poll the `status` string to route execution. The skill catalog uses a Hybrid Hexagonal structure, ensuring small router skills handle context delegation to specific sub-skills.

## Key Findings
1. NCP inherently uses Dramatica vocabulary (`perspectives`, `storybeats`, `storypoints`) making external mapping redundant.
2. Anthropic's Agentic Skill framework utilizes a `SKILL.md` format that scales via a hexagonal router pattern.
3. Gemini Jules lacks a native `.claude/skills` loader, mandating a compensation pattern (e.g., `AGENT_NOTES.md`).

## Output Matrix (Category B)
- **Track 1:** Extracted JSON data model and state machine from `ncp-schema.json`.
- **Track 2:** SDD patterns highlight property-based validation over prose.
- **Track 3:** RFC 2119 + Gherkin identified as mandatory for spec-writing.
- **Track 4:** Core Dramatica theory mapped to 8 authoring phases.
- **Track 5:** `SKILL.md` hexagonal pattern validated for Claude Code.

## Contradictions Encountered
1. NCP uses `status` (`candidate`, `draft`, `complete`), but complex workflows require phase-level state tracking.
2. `narrator-position` and `research` phase are valid novel-craft concepts but excluded by the locked input lists.

## World-Change Log (from Step (i.c))
- NCP repo showed recent commits tightening schemas and adding validation fixtures up through early May 2026.

## Query Expansion Log (Method M13)
- Adjacent: "behavior-driven specification authoring agent context" (Novel: Yes, Mod Conclusion: No)
- Opposing: "why agentic skill ecosystems fragment" (Novel: Yes, Mod Conclusion: No)
- Abstraction: "narrative engineering formal semantics" (Novel: Yes, Mod Conclusion: No)
- Orthogonal: "tabletop RPG narrative engines vs Dramatica" (Novel: No, Mod Conclusion: No)

## Reflection History (CONSTRAINT BLOCK 0)
(Stored internally in run state. Included Kickoff, Mid-run, Post-Query, Pre-Synthesis, and Post-Synthesis).

## Cross-Pollination Log (Phase 2b — Steps (i.a) and (i.c))
- Hidden entities (narrator-position) and schema gaps (model params) checked.
- World-change checks on NCP repo executed using git logs.

## Open Questions / Unresolved
- Multi-agent concurrent conflict resolution in a single JSON state file.
- Computation of complex Dramatica dynamics without proprietary software.

## Sources
- NCP Repo: `0b9ab1223d3822a49eddc139bcdf2669aa067734`
- IETF RFC 2119 / BCP 14 (https://www.rfc-editor.org/info/bcp14)
- Dramatica Theory (https://dramatica.com/theory)
- Anthropic Engineering Blogs (https://www.anthropic.com/engineering)

## Methodology Note
Applied M06 (Source Triangulation), M07 (Contradiction Log), M08 (Pre-Commitment), M10 (First-Principles Decomposition), M13 (Adversarial Query Expansion). All claims anchored or flagged as single-source.
