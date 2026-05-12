---
type: task
status: active
slug: platform-agnostic-closing-procedure
summary: "Define a platform-agnostic closing-run procedure in AGENTS.md (open a PR via the platform's mechanism + attach friction-log + ensure index sync). Demote /sc:createPR to one implementation among others; give Jules and Gemini concrete, parity guidance."
created: 2026-05-07
updated: 2026-05-11
task_id: "060"
task_status: done
task_owner: "claude-code"
task_priority: P2
task_uses_prompts: []
task_spawns_research: []
task_spawns_prompts: []
task_blocked_by: []
task_supersedes: []
task_superseded_by: []
task_affects_paths:
  - AGENTS.md
  - skills/
---

# Task 060 — Platform-Agnostic Closing-Run Procedure

## Goal

`AGENTS.md` "Skill Provenance" section (lines 74–77) makes the SuperClaude `/sc:createPR` slash-command authoritative for the closing-run procedure; Jules, Gemini, and other agents are referred vaguely to "their own platform conventions." This is an asymmetry that makes the protocol incomplete for non-Claude agents. The single falsifiable outcome of this Task: `AGENTS.md` defines a platform-agnostic closing-run procedure as a numbered checklist (e.g., "1. friction-log committed; 2. tasks/readme.md synced; 3. PR opened via your platform's mechanism with the closing checklist as the PR body"), and `/sc:createPR` is reframed as one implementation that satisfies the checklist — with at least one parallel implementation note for Jules and Gemini.

## Plan

1. **Extract** the implicit checklist from the current `/sc:createPR` skill content (whatever steps it performs); write it as a platform-agnostic list of N steps in `notes.md`.
2. **Verify** that each step is achievable on Jules and Gemini without `/sc:` skills (e.g., is there a Jules-native PR-creation primitive? a Gemini-native one?). Note any genuinely Claude-only step as a *gap* the platform-agnostic procedure cannot fully replace.
3. **Author** a new `AGENTS.md §Closing Run` section with the platform-agnostic checklist + one-paragraph "implementation notes" for each platform (Claude/Jules/Gemini).
4. **Demote** the existing "Skill Provenance" / `/sc:createPR` reference to a sub-bullet under the Claude implementation note; preserve the link.
5. **Cross-link** from `MAINTENANCE.md` and `FRUSTRATED.md` if they currently cite `/sc:createPR` exclusively.

## Todo

- [ ] Extract implicit `/sc:createPR` checklist into a platform-agnostic list.
- [ ] Audit Jules + Gemini PR-creation primitives; flag any gaps.
- [ ] Author `AGENTS.md §Closing Run` (platform-agnostic).
- [ ] Demote `/sc:createPR` to one implementation note.
- [ ] Sweep `MAINTENANCE.md` + `FRUSTRATED.md` for exclusive `/sc:` references.
- [ ] Write `friction-log.md` with FL[0–3] declaration on closure.

## Links

- Parent dispatch: [Task 053](../053-core-architecture-review-followups/) finding B.9.
- Affected lines at branch-time: [`AGENTS.md` lines 74–77](../../AGENTS.md).
- SuperClaude reference: `src/superclaude/commands/createPR.md` (external).
