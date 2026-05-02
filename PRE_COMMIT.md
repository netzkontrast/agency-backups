# General Pre-Commit Checklist for Agents

Before committing any code or documentation changes to this repository, the agent MUST perform the following checks. Failure to satisfy these checks means the commit MUST NOT be executed.

## 1. Clean Working Directory
- Verify there are no unintended temporary files, `.py` or `.sh` script scratchpads, or loose log dumps scattered in the root directory or working directories.
- Ensure that you have explicitly deleted any temporary execution scripts used to generate data.
- Use `git status` to ensure only explicitly intended files are staged.

## 2. File Integrity
- No required documentation file (like `readme.md`, `state.md`, `session.log`) may be left empty (0 bytes). If a file exists in the planned structure, it MUST contain meaningful content.

## 3. Testing & Verification
- If modifying code, run all relevant unit tests and ensure they pass.
- If editing UI/frontend elements, generate and verify screenshots/media.
- If requested by the project scope, invoke the code review tooling and address feedback before committing.

## 4. Formatting & Linting
- All Markdown files must have consistent header formatting, valid relative links, and readable tables.
- All code files must adhere to the native formatting standard of the respective language.

## 5. Context-Specific Mandates
- If the task is a **Research Task**, the agent MUST additionally satisfy the `Mandatory Pre-Commit Checks` defined in [RESEARCH.md](./RESEARCH.md), which includes strict folder structuring, synthesis tracking, and zero-empty-file policies.

Only when all applicable boxes above are conceptually "checked" may the agent invoke the `submit` or `git commit` commands.
