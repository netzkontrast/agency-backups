# Research Task Specification

When handling a Research Task, the agent MUST enforce the following directory structure and workflow. This ensures consistency, traceability, and separation of concerns across multiple research engagements.

## Directory Structure
For every new research task, create a dedicated subfolder within the root `/research` directory. The folder name should be the `slugname` of the research prompt.

```text
/research
└── /<slugname>
    ├── prompt.md            # The exact, complete initial research prompt/request
    ├── /workspace           # All temporary work artifacts, bash scripts, tracking notes, etc.
    │   ├── session.log      # Reconstruction of the session commands/execution log
    │   └── ...              # Other scratchpad notes
    ├── /synthesis           # Any synthesis artifacts (e.g., intermediate comparisons, trade-off matrices)
    │   ├── artifacts.md
    │   └── ...
    └── /output              # The final deliverables (e.g., SPEC.md)
```

## Workflow Requirements
1. **Initialize Directory:** Immediately create the `<slugname>` folder and its three subfolders (`workspace`, `synthesis`, `output`).
2. **Store Prompt:** Save the raw text of the user's initial prompt into `prompt.md`.
3. **Work in Workspace:** Save all planning scripts, search logs, downloaded pages, and temporary tracking files into the `/workspace` folder. Do not pollute the root directory.
4. **Log the Session:** Reconstruct or save the terminal/bash commands and reflection logs into `/workspace/session.log`.
5. **Synthesize:** If the prompt requires synthesis documents, contradiction logs, or research summaries that are NOT the final deliverable, save them in the `/synthesis` folder.
6. **Deliver:** Move the final completed deliverable (e.g., `SPEC.md`, `REPORT.md`) into the `/output` folder.

Follow these rules for every research-oriented task without deviation.
