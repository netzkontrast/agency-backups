# Contradiction Log
1. **Source Disagreement:** NCP uses `status` (`candidate`, `draft`, `complete`) internally, but the workflow needs an explicit state machine for *phases*. We will need cross-cutting skills to map workflow phases onto NCP's `status` + specific entity population checks.
2. **Out-of-Scope Candidate (Entities):** Item `narrator-position` appears to satisfy inclusion criteria but is not in the locked input list (NCP has `audience_experiential_pov`, but Dramatica has complex POV).
3. **Out-of-Scope Candidate (Phases):** Item `research` and `sensitivity reading` occur in practice but are not in the standard eight-phase list.
4. **Out-of-Scope Candidate Field:** The schema as given may be missing the field `Conflict Resolution Mechanisms` because when multi-agent changes collide, git-like merge strategies are assumed but not explicitly specified.
