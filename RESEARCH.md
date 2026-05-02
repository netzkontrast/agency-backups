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

## Mandatory Pre-Commit Checks for Research Tasks
Before committing the final deliverables of any Research Task, the agent MUST run through the following specific checks. If any check fails, the pre-commit phase fails, and the agent must resolve the issue before proceeding.

1. **Prompt Integrity:** `prompt.md` exists and contains the exact, unedited user request.
2. **Workspace Cleanliness:** Temporary scripts, JSON dumps, and raw notes are contained entirely within `/workspace`. The root of the repository is not polluted.
3. **Session Logging:** `/workspace/session.log` exists and accurately traces the CLI operations or tool calls executed during the task.
4. **Synthesis Verification:**
   - The `/synthesis` folder exists and is structured properly.
   - `/synthesis/readme.md` is complete and contains hard results.
   - `/synthesis/post-synthesis-log.md` traces the exact reasoning used to arrive at the final specification.
   - `/synthesis/plan/state.md` shows all steps checked off as complete.
   - All applied methods and aspect tracks are thoroughly documented in their respective subfolders.
5. **Output Verification:** `/output` contains the final target specification or report (e.g., `SPEC.md`), and it adheres strictly to the formatting constraints defined in the original prompt.

All steps in the synthesis process MUST be verifiably checked off in `/synthesis/plan/state.md` before this pre-commit check can pass.
