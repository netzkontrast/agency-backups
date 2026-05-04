# reflection

**What is this folder?** Critical thinking artifacts produced during the
`agentic-eval-trust-improvement-spec` research run.

**Why is it here?** Per `RESEARCH.md §Directory Structure`, all self-reflection outputs
based on the five critical thinking methods MUST be stored here as flat files, separate
from synthesis artifacts and the final output.

**Current status:** Initialized scaffold. Will be populated by the executing agent.

## Contents (once populated)

- [friction-log.md](./friction-log.md): MANDATORY per `FRUSTRATED.md`. The executing agent
  MUST declare its highest Frustration Level (FL0–FL3) and document workflow friction
  experienced during the run. Initialized with placeholder text below.
- `M06-source-triangulation.md`: Source triangulation evidence log.
- `M07-contradiction-log.md`: Full contradiction log (may reference synthesis/tracks.md).
- `M08-pre-commitment.md`: Pre-commitment and falsification passes for key normative claims.
- `M09-steelmanning.md`: Steelmanning passes applied to MUST-level statements.
- `M03-pre-mortem.md`: Pre-mortem analysis for lifecycle failure modes.
- `M13-adversarial-query-expansion.md`: Full M13 query expansion log (may duplicate
  workspace notes — this version should be clean and final).

## Workflow Assumptions

- Per `FRUSTRATED.md`, `friction-log.md` is mandatory even if the task proceeds perfectly (FL0).
- Method files (M##) are generated during execution; they may not all be needed depending
  on which methods the executing agent applies and how they overlap with synthesis tracks.
- Keep this folder flat per `FOLDERS.md`.
