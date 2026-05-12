---
name: sc-createPR
description: >-
  Open a pull request for the current branch as the closing step of a Claude Code session. Use at the end of a session after a successful git push to satisfy AGENTS.md Closing Run Procedure step 4 (CR.1–CR.7).
skill_kind: tool
skill_target_agents: [claude-code]
skill_references_skills: [skills-skill-bootstrap]
skill_references_research: [skills-skill-architecture]
skill_references_prompts: []
skill_bootstrap_required: false
skill_source: "superclaude@v4.3.0"
---

# sc-createPR — `/sc:createPR` (imported from SuperClaude v4.3.0)

## What

Imported `/sc:createPR` command from SuperClaude_Framework. Canonical session-closer for Claude Code per AGENTS.md CR.1–CR.7.

## When to use

Use at the end of a Claude Code session after `git push` succeeds, to open (or update) a pull request that cites the closed Task slug(s) and the Frustration Log declaration.

## How to use

1. Verify push state and run `tools/check-governance.sh`; ABORT if exit ≠ 0 (defence-in-depth on CR.3).
2. Detect existing open PR via `mcp__github__list_pull_requests`; no-op if found.
3. Synthesize PR title (commit subject) and body (commit log + `tasks/<NNN>-<slug>/friction-log.md` FL declaration).
4. Open the PR via `mcp__github__create_pull_request`.

Full behavioural specification at `references/upstream-sc-createPR.md`. PR body MUST cite the closed Task slug(s) and FL level per AGENTS.md CR.5.

## References

- Upstream: [`src/superclaude/commands/createPR.md@22ad3f4`](https://github.com/SuperClaude-Org/SuperClaude_Framework/blob/22ad3f483a6fe6c626834e1c9a3573126644a058/src/superclaude/commands/createPR.md) — verbatim mirror at [`references/upstream-sc-createPR.md`](./references/upstream-sc-createPR.md) (ADR-0011 D.3).
- Agency anchor: AGENTS.md Closing Run Procedure CR.1–CR.7 — canonical session-closer for Claude Code.
- Import policy: [`decisions/0011-external-skill-corpora-import.md`](../../decisions/0011-external-skill-corpora-import.md).

## Compatibility

- Target agent: `claude-code` (this repo's primary surface)
- Known limitation: imported one-shot snapshot at SuperClaude_Framework `v4.3.0` — re-syncs require a new Task per ADR-0011 D.9.
