# Research Task Specification

When handling a Research Task, the agent MUST enforce the following directory structure and workflow. This ensures consistency, traceability, and separation of concerns across multiple research engagements. No required file may remain completely empty; placeholder text or raw data must be inserted to prove execution.

## Directory Structure
For every new research task, create a dedicated subfolder within the root `/research` directory. The folder name should be the `slugname` of the research prompt.

```text
/research
└── /<slugname>
    ├── prompt.md            # The exact, complete initial research prompt/request. Must not be empty.
    ├── /workspace           # All temporary work artifacts, bash scripts, tracking notes, etc.
    │   ├── session.log      # A chronological list of terminal commands, searches, and file creations. Must not be empty.
    │   └── ...              # Other scratchpad notes (unneeded execution scripts must be deleted before commit).
    ├── /synthesis           # Structured synthesis artifacts
    │   ├── readme.md        # The hard results of the synthesis, linking to subfolders. Must not be empty.
    │   ├── post-synthesis-log.md # A chronological log detailing how facts were merged to create the final spec. Must not be empty.
    │   ├── /method          # Documentation of methods applied (e.g., M06, M13 logs).
    │   ├── /aspects         # Subfolders or files detailing every specific aspect/track worked on.
    │   └── /plan            # Tracking for the synthesis process.
    │       └── state.md     # A checklist state file keeping track of every step of the synthesis. Must not be empty.
    ├── /reflection          # Rigorous self-reflection based on the 5 critical thinking methods.
    │   ├── readme.md        # The overarching reflection plan.
    │   └── /step-[1-5]      # Individual workbooks and artifact evidence for each method.
    └── /output              # The final deliverables (e.g., SPEC.md)
```

## Workflow Requirements
1. **Initialize Directory:** Immediately create the `<slugname>` folder and its main subfolders (`workspace`, `synthesis`, `reflection`, `output`).
2. **Store Prompt:** Save the raw text of the user's initial prompt into `prompt.md`.
3. **Work in Workspace:** Save all planning scripts, search logs, downloaded pages, and temporary tracking files into the `/workspace` folder. Do not pollute the root directory. *Ensure execution scripts (e.g., `.py` or `.sh` test runners) are deleted prior to finalizing the branch.*
4. **Log the Session:** Reconstruct or continuously save the terminal/bash commands and tool calls into `/workspace/session.log`. This file must map a chronological timeline of the agent's actions.
5. **Synthesize Structurally:** The `/synthesis` folder must be populated structurally:
   - Create `readme.md` containing hard results and relative links to the sub-sections.
   - Maintain `/synthesis/plan/state.md` with markdown checkboxes (`[x]`) for the synthesis process.
   - Detail the applied methods in `/synthesis/method/`.
   - Store content for different tracks/aspects in `/synthesis/aspects/`.
   - Maintain a `post-synthesis-log.md` that details and links to every synthesis step. *If you simply merged text, document that sequence.*
6. **Reflect:** Conduct self-reflection according to the methods outlined in the prompt and save the evidence in `/reflection`.
7. **Deliver:** Move the final completed deliverable (e.g., `SPEC.md`, `REPORT.md`) into the `/output` folder.

Follow these rules for every research-oriented task without deviation.

## Mandatory Pre-Commit Checks for Research Tasks
Before committing the final deliverables of any Research Task, the agent MUST run through the following specific checks. If any check fails, the pre-commit phase fails, and the agent must resolve the issue before proceeding.

1. **Prompt Integrity:** `prompt.md` exists and contains the exact, unedited user request.
2. **Workspace Cleanliness:** Temporary scripts, `.py` runners, and `.sh` generators MUST be deleted from `/workspace`. Only raw notes, dumps, and `session.log` may remain. The root of the repository is not polluted.
3. **No Empty Files:** No required file (`session.log`, `post-synthesis-log.md`, `state.md`, `readme.md`) may be completely empty (0 bytes). They must contain actual trace data or explanatory text.
4. **Session Logging:** `/workspace/session.log` exists, is populated, and accurately traces the CLI operations or tool calls executed during the task.
5. **Synthesis Verification:**
   - The `/synthesis` folder exists and is structured properly.
   - `/synthesis/readme.md` is complete and contains hard results.
   - `/synthesis/post-synthesis-log.md` traces the exact sequence used to arrive at the final specification.
   - `/synthesis/plan/state.md` shows all steps checked off as complete `[x]`.
   - All applied methods and aspect tracks are thoroughly documented in their respective subfolders.
6. **Output Verification:** `/output` contains the final target specification or report (e.g., `SPEC.md`), and it adheres strictly to the formatting constraints defined in the original prompt.

All steps in the synthesis process MUST be verifiably checked off in `/synthesis/plan/state.md` before this pre-commit check can pass.
7. **Task Friction Reflection:** After all other checks are complete, and right before executing the commit, the agent MUST write a meta-reflection document located at `/reflection/friction-log.md`. This document must explicitly answer:
   - Were the instructions in the prompt or repository unclear or conflicting at any point?
   - Did the agent encounter an unusual number of errors, missing dependencies, or tooling failures?
   - **Crucially:** Was working on this task frustrating or inefficient in any way? If the agent had to perform tedious reorganizations or backtrack significantly, this friction must be logged so future protocols or prompts can be improved.
