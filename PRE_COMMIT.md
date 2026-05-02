# General Pre-Commit Checklist for Agents

Before committing any code or documentation changes to this repository, the agent MUST perform the following checks. Failure to satisfy these checks means the commit MUST NOT be executed.

## 1. Clean Working Directory
- Verify there are no unintended temporary files, `.py` or `.sh` script scratchpads, or loose log dumps.
- Ensure that you have explicitly deleted any temporary execution scripts used to generate data.
- Use `git status` to ensure only explicitly intended files are staged.

## 2. File Integrity & Decentralized Documentation
- No required documentation file (like `readme.md`, `state.md`, `session.log`) may be left empty (0 bytes).
- **Global Readme Audit:** EVERY folder that has been touched MUST have an updated `readme.md`.
- **Readme Format:** The `readme.md` MUST explicitly explain the "what" and "why" of the directory's contents, and MUST use clickable relative Markdown links for every file and subfolder referenced.

## 3. Testing & Verification
- If modifying code, run all relevant unit tests and ensure they pass.
- If editing UI/frontend elements, generate and verify screenshots/media.

## 4. Formatting & Linting
- All Markdown files must have consistent header formatting, valid relative links, and readable tables.

## 5. Context-Specific Mandates
- If the task is a **Research Task**, the agent MUST additionally satisfy the `Mandatory Pre-Commit Checks` defined in [RESEARCH.md](./RESEARCH.md).

Only when all applicable boxes above are conceptually "checked" may the agent invoke the `submit` or `git commit` commands.
