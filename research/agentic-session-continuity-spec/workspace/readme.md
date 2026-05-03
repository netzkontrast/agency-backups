# Workspace

**Status:** Initialized — awaiting research execution

This directory will contain all temporary work artifacts generated during the execution
of the research prompt at `../prompt.md`:

- `session.log` — chronological trace of CLI operations, searches, and file creations
- `integrity_check.md` — pre-synthesis integrity check results
- Query expansion notes, raw search dumps, and other scratchpad files

**Do not create files here manually.** This folder is populated by the executing agent.
Per `RESEARCH.md §Workspace Cleanliness`, all execution scripts (`.py`, `.sh`) MUST be
deleted before the pre-commit phase. Only raw notes, dumps, and `session.log` may remain.
