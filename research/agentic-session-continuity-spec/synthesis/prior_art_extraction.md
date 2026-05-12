## Prior Art Extraction

| ID | Statement | Source | What to extend |
|:---|:---|:---|:---|
| B.3.4 | Context rot occurs past ~300k tokens; wide reads SHOULD be delegated to subagents | Spec-B | When exactly? What observable signals? |
| B.4.4 | Planning phase and execution phase MUST NOT be merged into a single command | Spec-B | |
| D.2.2 | Spec authors MUST chunk a specification into separate files if it exceeds standard agent context windows | Spec-D | Chunking strategy for non-spec content too |
| E.2.1 | A multi-agent orchestrator MUST separate the Planning Agent from the Execution Agent | Spec-E | |
| E.3.2 | A ReAct agent MUST externalize its Observation log to a persistent artifact before any context compaction event | Spec-E | Define the schema of that externalization |
| F.2.1 | A repository-resident agent MUST read AGENTS.md before modifying any file | Spec-F | |
| F.3.1 | Every folder touched by an agent MUST contain a readme.md with relative Markdown links | Spec-F | |
