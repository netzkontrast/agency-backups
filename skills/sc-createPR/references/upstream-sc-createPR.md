<!-- Mirror of SuperClaude-Org/SuperClaude_Framework/src/superclaude/commands/createPR.md @ 22ad3f483a6fe6c626834e1c9a3573126644a058 (v4.3.0). Verbatim per ADR-0011 D.3/D.8. DO NOT EDIT — re-sync via a new Task. -->

---
name: createPR
description: "Open a pull request for the current branch as the closing step of a Claude Code session"
category: utility
complexity: basic
mcp-servers: [github]
personas: []
---

# /sc:createPR - Create Pull Request

> **Closing-Run Mandate:** Per `AGENTS.md` rule **CR.1** in repositories that adopt this convention (e.g. `netzkontrast/agency`), a Claude Code session MUST end with `/sc:createPR` after a successful `git push`. This command is the canonical implementation of that rule.

## Triggers
- End of a Claude Code session that committed and pushed work
- An open feature branch with no existing PR (or with new commits beyond the existing PR)
- Explicit user request to open a pull request

## Usage
```
/sc:createPR [--draft] [--base <branch>] [--title "<title>"]
```

## Behavioral Flow
1. **Verify push state**: Confirm the current branch is pushed to its remote tracking branch and is not behind origin.
2. **Verify pre-commit health**: Re-run any repository-defined governance checks (e.g. `tools/check-governance.sh`); ABORT and surface diagnostics if exit ≠ 0.
3. **Detect existing PR**: Query the GitHub API for an open PR whose `head` matches the current branch; if found, report it as a no-op success and exit.
4. **Synthesize PR metadata**:
   - Title: derive from the most recent commit subject (or use `--title` override)
   - Body: assemble from commit log since base branch, plus any `friction-log.md` FL declaration discovered in `tasks/<NNN>-<slug>/`
   - Base: default to repository default branch (`main` / `master`); honor `--base` override
   - Head: current branch
5. **Open PR**: Invoke `mcp__github__create_pull_request` with the assembled fields.
6. **Report**: Print the PR URL to the user; the session is now formally complete.

## Tool Coordination
- **Bash**: `git status`, `git log`, `git rev-parse`, `git push` (only if branch unpushed)
- **Read**: scan `tasks/<NNN>-<slug>/friction-log.md` for FL declaration to cite in PR body
- **mcp__github__list_pull_requests**: detect existing open PR for `head=<branch>`
- **mcp__github__create_pull_request**: open the PR
- **mcp__github__get_me**: resolve current GitHub user when needed

## Key Patterns
- **Idempotent**: re-running on a branch that already has an open PR is a no-op success.
- **Pre-commit gated**: refuses to open a PR when governance checks fail or were skipped.
- **Evidence-citing**: PR body cites the closed Task slug(s) and FL level when those artifacts exist.

## Examples

### End-of-session PR
```
/sc:createPR
# Detects current branch, runs governance checks, opens PR against main
# with auto-generated title and body citing the closed task and FL level.
```

### Draft PR for work-in-progress
```
/sc:createPR --draft --title "WIP: refactor governance enforcement"
# Opens a draft PR so reviewers can comment without merge pressure.
```

### Override base branch
```
/sc:createPR --base integration
# Targets the integration branch instead of main.
```

## Boundaries

**Will:**
- Open a pull request via the GitHub MCP server using verified branch state
- Refuse to open a PR when pre-commit governance checks have failed
- Detect and surface an existing open PR rather than creating duplicates
- Cite closed task slugs and friction-log FL declarations in the PR body when present

**Will Not:**
- Push commits on the user's behalf (only the user's own `git push` precedes this command)
- Merge the PR or modify branch protection settings
- Open PRs against repositories outside the agent's authorized repository scope
- Bypass or silence failing governance linters
