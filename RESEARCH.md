# Research Task Specification

When handling a Research Task, the agent MUST enforce the following directory structure and workflow. This ensures consistency, traceability, and separation of concerns across multiple research engagements. No required file may remain completely empty; placeholder text or raw data must be inserted to prove execution.

## Directory Structure
For every new research task, create a dedicated subfolder within the root `/research` directory. The folder name should be the `slugname` of the research prompt. All folders must adhere to the rules in `FOLDERS.md` (e.g. keeping structures flat and maintaining a `readme.md`).

```text
/research
└── /<slugname>
    ├── readme.md            # Directory index.
    ├── prompt.md            # The exact, complete initial research prompt/request. Must not be empty.
    ├── /workspace           # All temporary work artifacts, bash scripts, tracking notes, etc.
    │   ├── readme.md        # Directory index.
    │   ├── session.log      # A chronological list of terminal commands, searches, and file creations.
    │   └── ...              # Other scratchpad notes (unneeded execution scripts must be deleted before commit).
    ├── /synthesis           # Structured, flattened synthesis artifacts.
    │   ├── readme.md        # The hard results of the synthesis, linking to other files in this folder.
    │   ├── post-synthesis-log.md # A chronological log detailing how facts were merged.
    │   ├── methodology.md   # Documentation of methods applied (e.g., M06, M13 logs).
    │   ├── tracks.md        # Files detailing specific aspect/track worked on.
    │   └── state.md         # A checklist state file keeping track of every step of the synthesis.
    ├── /reflection          # Rigorous self-reflection based on the 5 critical thinking methods.
    │   ├── readme.md        # The overarching reflection plan and directory index.
    │   ├── friction-log.md  # Standardized tracking of agent frustration levels (FL0-FL3).
    │   └── M<XX>-*.md       # Individual flattened artifact files for each method (e.g. M06-audit.md).
    └── /output              # The final deliverables (e.g., SPEC.md)
        ├── readme.md        # Directory index.
        └── SPEC.md
```

## Workflow Requirements
1. **Initialize Directory:** Immediately create the `<slugname>` folder and its main subfolders (`workspace`, `synthesis`, `reflection`, `output`).
2. **Store Prompt:** Save the raw text of the user's initial prompt into `prompt.md`.
3. **Readmes Everywhere:** Create a `readme.md` in every folder created.
4. **Work in Workspace:** Save all planning scripts, search logs, downloaded pages, and temporary tracking files into the `/workspace` folder. Do not pollute the root directory. *Ensure execution scripts (e.g., `.py` or `.sh` test runners) are deleted prior to finalizing the branch.*
5. **Log the Session:** Reconstruct or continuously save the terminal/bash commands and tool calls into `/workspace/session.log`. This file must map a chronological timeline of the agent's actions.
6. **Synthesize Structurally:** The `/synthesis` folder must be populated structurally. Keep the structure flat per `FOLDERS.md` unless subcategorizing 4+ files of the exact same type.
7. **Reflect:** Conduct self-reflection according to the methods outlined in the prompt and save the evidence in `/reflection` as flat files.
8. **Deliver:** Move the final completed deliverable (e.g., `SPEC.md`, `REPORT.md`) into the `/output` folder.

Follow these rules for every research-oriented task without deviation.

## Mandatory Pre-Commit Checks for Research Tasks
Before committing the final deliverables of any Research Task, the agent MUST run through the following specific checks. If any check fails, the pre-commit phase fails, and the agent must resolve the issue before proceeding.

1. **Prompt Integrity:** `prompt.md` exists and contains the exact, unedited user request.
2. **Workspace Cleanliness:** Temporary scripts, `.py` runners, and `.sh` generators MUST be deleted from `/workspace`. Only raw notes, dumps, and `session.log` may remain.
3. **No Empty Files:** No required file (`session.log`, `post-synthesis-log.md`, `state.md`, `readme.md`) may be completely empty (0 bytes). They must contain actual trace data or explanatory text.
4. **Readme Audit:** EVERY folder must contain an updated `readme.md` cataloging its current contents.
5. **Session Logging:** `/workspace/session.log` exists, is populated, and accurately traces the CLI operations executed during the task.
6. **Synthesis Verification:**
   - The `/synthesis` folder exists and is structured properly (flattened).
   - `/synthesis/readme.md` is complete and contains hard results.
   - `/synthesis/post-synthesis-log.md` traces the exact sequence used to arrive at the final specification.
   - `/synthesis/state.md` shows all steps checked off as complete `[x]`.
7. **Output Verification:** `/output` contains the final target specification or report.
8. **Task Friction Reflection:** After all other checks are complete, the agent MUST write a meta-reflection document located at `/reflection/friction-log.md`. This document MUST conform to the specifications in `FRUSTRATED.md`. It must declare an explicit **Frustration Level (FL0 - FL3)** at the top of the file, explain any confusing/conflicting instructions, and document workflow inefficiencies or backtracking caused by the prompt structure.

All steps in the synthesis process MUST be verifiably checked off in `/synthesis/state.md` before this pre-commit check can pass.
