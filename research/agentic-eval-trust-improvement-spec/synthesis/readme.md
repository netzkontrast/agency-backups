# synthesis

**What is this folder?** Structured, flattened synthesis artifacts for the
`agentic-eval-trust-improvement-spec` research run.

**Why is it here?** Per `RESEARCH.md §Directory Structure`, all structured synthesis
work — state tracking, methodology notes, post-synthesis logs, and track notes — MUST
live here, separate from the raw scratchpad workspace and the final deliverable output.

**Current status:** Initialized scaffold. Will be populated by the executing agent.

## Contents (once populated)

- [state.md](./state.md): Checklist tracking every step of the synthesis process.
  All steps MUST be checked off before the pre-commit phase begins.
- `methodology.md`: Documentation of methods applied (M06 triangulation, M13 expansion,
  M07 contradiction log, M08 pre-commitment, M09 steelmanning, M03 pre-mortem).
- `post-synthesis-log.md`: Chronological log detailing how findings were merged into
  normative statements and how contradictions were resolved.
- `tracks.md`: Notes on specific research tracks (Spec-J track, Spec-K track, Spec-L track).

## Workflow Assumptions

- Structure must remain flat per `FOLDERS.md` unless 4+ files of the same type accumulate.
- The `state.md` file is MANDATORY — it must be non-empty and show all steps checked as
  `[x]` before the pre-commit check can pass.
- `post-synthesis-log.md` MUST trace the exact sequence used to arrive at each final Spec.
