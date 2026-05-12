# M07 Contradiction Review

## Contradiction 1: State Machine Granularity
- **Conflict:** The 8-phase workflow requires distinct state tracking (e.g., Phase 2 to Phase 3 handoff). However, NCP's native `status` field only allows `candidate`, `draft`, `complete`.
- **Resolution in SPEC.md:** I bridged this by having the Agent query both `status` AND the structural content (e.g., checking if `subtext.storybeats` contains exactly 16 progressions) to determine the phase transition.
- **Verdict:** Transparently handled. I did not silently ignore the limitation of the `status` enum.

## Contradiction 2: Out of Scope Entities
- **Conflict:** `narrator-position` and `research` phases are valid in novel writing but excluded by the locked input constraint.
- **Resolution in SPEC.md:** Excluded from the main workflows, but `narrator-position` conceptually maps to the `audience_experiential_pov` natively found in the NCP schema. I documented the exclusions in the synthesis logs.
- **Verdict:** Handled per instructions (do not hybridize or silently change the input list).
