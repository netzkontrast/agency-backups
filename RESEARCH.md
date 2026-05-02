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
    ├── /synthesis           # Structured synthesis artifacts
    │   ├── readme.md        # The hard results of the synthesis, linking to subfolders
    │   ├── post-synthesis-log.md # Log containing and linking to every step of your synthesis process
    │   ├── /method          # Documentation of methods applied during research/synthesis
    │   ├── /aspects         # Subfolders or files detailing every specific aspect worked on
    │   └── /plan            # Tracking for the synthesis process
    │       └── state.md     # State file keeping track of every step of the synthesis
    └── /output              # The final deliverables (e.g., SPEC.md)
```

## Workflow Requirements
1. **Initialize Directory:** Immediately create the `<slugname>` folder and its three main subfolders (`workspace`, `synthesis`, `output`).
2. **Store Prompt:** Save the raw text of the user's initial prompt into `prompt.md`.
3. **Work in Workspace:** Save all planning scripts, search logs, downloaded pages, and temporary tracking files into the `/workspace` folder. Do not pollute the root directory.
4. **Log the Session:** Reconstruct or save the terminal/bash commands and reflection logs into `/workspace/session.log`.
5. **Synthesize Structurally:** The `/synthesis` folder must be populated structurally:
   - Create `readme.md` containing hard results and links to the sub-sections.
   - Maintain `/synthesis/plan/state.md` to keep track of the synthesis process step-by-step.
   - Detail the applied methods in `/synthesis/method/`.
   - Store content for different tracks/aspects in `/synthesis/aspects/`.
   - Maintain a `post-synthesis-log.md` that details and links to every synthesis step.
6. **Deliver:** Move the final completed deliverable (e.g., `SPEC.md`, `REPORT.md`) into the `/output` folder.

Follow these rules for every research-oriented task without deviation.
