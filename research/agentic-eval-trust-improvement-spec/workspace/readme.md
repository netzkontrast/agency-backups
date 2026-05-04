# workspace

**What is this folder?** Scratchpad for all temporary work artifacts generated during
execution of the `agentic-eval-trust-improvement-spec` research prompt.

**Why is it here?** Per `RESEARCH.md §Directory Structure`, all planning scripts, search
logs, downloaded pages, and temporary tracking files MUST be saved here to avoid polluting
the root or output directories.

**Current status:** Initialized scaffold. Will be populated by the executing agent.

## Contents (once populated)

- [session.log](./session.log): Chronological log of all terminal commands, searches,
  and file creations executed during the research run. MANDATORY per RESEARCH.md.
- Additional scratchpad notes (track notes, query expansion logs, contradiction drafts)
  will appear here during execution.

## Workflow Assumptions

- Execution scripts (`.py`, `.sh`) MUST be deleted before the final commit, per `RESEARCH.md §3`.
- Only raw notes, dumps, and `session.log` may remain after commit.
- The executing agent MUST initialize `session.log` at the very start of execution and
  append to it continuously throughout the session.
