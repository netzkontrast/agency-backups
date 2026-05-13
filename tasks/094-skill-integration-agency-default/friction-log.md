---
type: note
status: active
slug: task-094-friction-log
summary: "Task 094 Epic friction log. ST-1, ST-2, ST-3 entries filled as each subtask lands; ST-4 appends the Epic-level summary at close. Stub created at Epic spec authoring time."
created: 2026-05-12
updated: 2026-05-13
---

# Task 094 — Friction Log

Highest Frustration Level: FL0

## Epic spec authoring (FL0)

- Planning workflow executed cleanly in Claude Code Plan mode at session `01WBrHNUZUEoew9PE9A7SguS`. Three parallel `Explore` subagents returned consistent intel (imported-skill inventory, Claude Code `.claude/` + plugin + hook docs, root-spec landscape gap analysis).
- User-locked three design decisions via `AskUserQuestion` before plan finalisation: hook granularity (event-driven, 5 hooks), Epic scope (4 subtasks, full implementation), carry-forward closure (absorb both T3 + T1).
- Plan-mode auto-exit transitioned cleanly to execution; no rework needed between plan and Epic spec.
- Epic spec mirrors Task 091 + Task 092 idioms (frontmatter, Goal/Context/Plan/AC structure, subtask-file format, friction-log layout).

No FL1+ items from spec authoring.

### PR #122 peer review — 5 advisory items (FL0)

Peer review on PR #122 returned **APPROVED · 0 blocking · 5 advisory**. Three small T1 fixes (A1 / A3 / A4) applied in this PR; two scope items (A2 / A5) carried forward to subtasks:

- **A1 (resolved this PR):** `task.md ## Note` lead sentence rewritten to point at `references/source-plan.md` first; ephemeral `/root/.claude/plans/` path is now secondary.
- **A2 (carried forward — ST-4 prerequisite):** `task_uses_prompts: []` with no prompt-layer rationale creates an audit-graph gap; first Plan-mode Epic without a `/prompts/` entry. Needs a TASK.md policy note (or a new ADR) ratifying Plan-mode artifacts as a valid prompt-layer substitute. MUST resolve before ST-4 flips the Epic to `done`.
- **A3 (resolved this PR):** Gherkin BR.94.2 rewritten with executable proxy `find .claude/skills -maxdepth 2 -name SKILL.md | wc -l` MUST return 52; replaces the unverifiable "session log MUST show 52 descriptions" assertion.
- **A4 (resolved this PR):** Unicode `…` ellipsis in Gherkin grep paths replaced with full slug `tasks/092-port-skill-corpora-phase-2/...` in `task.md ## Goal` "done when" list and `subtasks/01-root-spec-hookup.md` AC T094.1.3. Narrative ellipsis elsewhere (prose-only shorthand) left as-is.
- **A5 (carried forward — ST-2 scope):** No ADR for the new `.claude/` + `.claude-plugin/` topology yet. Per CLAUDE.md §5 "repo-architecture convention changes" route through `decisions/<NNNN>-<slug>.md`. ST-2 MUST file ADR-0013 declaring the symlink idiom + plugin manifest + 17-agent re-export pattern before `.claude/` lands.

## ST-1 — Root-spec hookup + T3 enum + T1 typo sweep (FL0)

Highest Frustration Level: FL0

- Root-spec hookup executed without blocker. All 54 imported skills (39 sc-* + 15 superpowers-*; spec said 52 but actual count is 54) are now cited in ≥ 1 root spec — zero orphans per AC T094.1.1.
- CLAUDE.md §13 expanded with `SK.13.SUPERCLAUDE` + `SK.13.SUPERPOWERS` anchors and 9-`skill_kind`-grouped enumeration; AGENTS.md gained a new H2 "Skill Index by Category" section with `SK.AGENTS.<kind>.<n>` anchors covering every category (orchestrator / discipline / domain / analysis / persona / tool / meta / workflow / agent-template).
- TASK.md §4.9 now inline-cites the four planning-ladder SKILL.md paths (sc-analyze / sc-brainstorm / sc-design / sc-workflow). RESEARCH.md §7 expanded to compose sc-research with sc-analyze + sc-deep-research-agent and four Superpowers discipline gates (brainstorming / writing-plans / systematic-debugging / verification-before-completion).
- T3 carried-forward enum ratified in SKILLS.md §3.3 to the 9-value closed set; F.B.11 ERROR-tier diagnostic added to `tools/fm/validate.py` (mirrors F.B.8/F.B.9 idiom from ADR-0011/ADR-0012 precedent); diagnostic registered in `maintenance/schemas/diagnostic-explanations.json`. Pytest fixture `tools/tests/fm/test_validate_skill_kind.py` covers all 9 valid + 3 invalid values + absent-key + repo-regression — 4 tests + 12 subtests pass.
- T1 carried-forward typo sweep applied to all 11 triage-notes that contained `superclaude_framework@v4.3.0`; verified `grep -r "superclaude_framework@v4.3.0" tasks/092-port-skill-corpora-phase-2/references/triage-notes/` returns zero matches per AC T094.1.3. `updated:` bumped via `tools/fm/edit.py --bump-updated` per MAINTENANCE.md §1.0.1 allowance idiom.
- `tools/check-governance.sh` exits 0 on the final commit. Validate-related pytest battery (test_validate.py + test_validate_extensions.py + test_validate_skill_bundles.py + test_validate_skill_source.py + test_validate_skill_kind.py) passes 40/40. Pre-existing failures in `test_fm_wrapper.py` + `test_duplicate_task_id.py` are unrelated to ST-1's surface (confirmed via baseline `git stash` check).
- Branch deviation: developed on the assigned `claude/execute-skill-integration-task-RAuYR` per the session-setup instruction rather than the spec-suggested `claude/task-094-st1-root-spec-hookup`. This is a session-policy override (CLAUDE.md §11 "develop on assigned feature branch"), not a friction event.

No FL1+ items from ST-1.

## ST-2 — `.claude/` directory + plugin manifest (FL declared per subtask)

(Populated as ST-2 work proceeds.)

## ST-3 — Event-driven hooks (FL1)

Highest Frustration Level: FL1 (Codex PR #125 review surfaced two P1 + one P2 confident corrections; resolved in a follow-up commit)

- Single-pass implementation. Five D.7-compliant hook scripts authored under `tools/hooks/` (`user-prompt-submit.sh`, `pre-tool-use.sh`, `post-tool-use.sh`, `stop.sh`, `subagent-stop.sh`); each is a thin bash shim that `exec`s a sister `_<event>.py` Python module so pytest can import the logic directly. Shared helpers (event parsing, repo-root, active-Task heuristic, skill-frontmatter read, telemetry append) live in `tools/hooks/_common.py` — Python 3.11 stdlib only.
- Hook registrations replaced the placeholder `"hooks": {}` block in `.claude/settings.json` from ST-2. Matchers per spec: `Skill|Agent` for `PreToolUse`/`PostToolUse`, `code-reviewer|deep-research` for `SubagentStop`, empty for the rest. `SessionStart` intentionally absent (ADR-0011 D.7).
- Governance check `tools/check-hooks.py` enforces three diagnostic codes — `H.1.1` orphan script, `H.1.2` orphan registration / non-executable, `H.1.3` SessionStart violation. Wired into `tools/check-governance.sh` as step `[5d]`. ERROR-tier; gates the suite unconditionally.
- Pytest fixture `tools/tests/test_hooks.py` covers all five hooks + the check-hooks linter — **26 tests pass**, every code path exercised. Sample event payloads under `tools/tests/fixtures/hooks/<event>.json`.
- Documentation: CLAUDE.md gained §14 "Hooks" with `HK.14.1`–`HK.14.5` anchors (one paragraph per hook) plus a `§14.A` "Governance + authoring" subsection; the pre-commit step matrix in §6 gained the `5d` row; the previous §14 "Quick non-negotiables" renumbered to §15. PRE_COMMIT.md §7.A toolchain-precedence matrix gained the `check-hooks.py` row.
- Side effect: the PreToolUse/PostToolUse telemetry writes to `tasks/<active>/skill-invocation-log.md`. The file's own banner declares it non-normative; added `tasks/*/skill-invocation-log.md` to `.gitignore` so smoke-test runs don't pollute the commit.
- `tools/check-governance.sh` exits 0 on the final commit (includes the new `[5d]` step). D.7 verification: `grep -c "SessionStart" .claude/settings.json` returns 0; the linter's H.1.3 unit test fires correctly when a `SessionStart` entry is injected into a temp settings file.

### PR #125 Codex review — 3 confident corrections (FL1)

Initial ST-3 commit landed FL0; the Codex automated review on PR #125 surfaced **3 actionable comments**, all of which were correct and applied in a follow-up commit:

- **P1 #1 (`tools/hooks/_common.py:211`) — `active_task()` ambiguity:** the original implementation fell back to the most-recently-modified active task when multiple were `in_progress`/`open`/`updated` and the branch did not disambiguate. Because the Stop hook is exit-2-blocking on FL-missing, this could block a session by checking the wrong task's friction-log. Rewrote `active_task()` to return None on ambiguity; tightened the branch-match heuristic to require exactly one matching slug-tail. Added 5 new pytest cases under `ActiveTaskAmbiguity`.
- **P1 #2 (`.claude/settings.json:10`) — anchor commands to `${CLAUDE_PROJECT_DIR}`:** the Anthropic hooks doc (`https://code.claude.com/docs/en/hooks`) recommends `${CLAUDE_PROJECT_DIR}` + exec-form (`args: []`) so hooks fire regardless of which subdirectory Claude Code is started under. Migrated all 5 registrations; extended `tools/check-hooks.py` with `_resolve_command_path()` to resolve both `${CLAUDE_PROJECT_DIR}` and bare `$CLAUDE_PROJECT_DIR` prefixes against the repo root. Added 3 new pytest cases under `CheckHooksProjectDirResolution`.
- **P2 #3 (`.claude/settings.json:40`) — restrict SubagentStop routing:** Codex was *partially* incorrect (the docs confirm SubagentStop accepts `matcher`), but the defense-in-depth point holds: an unrelated subagent that slipped past the matcher would have received an unearned routing message via the fallback. Removed the fallback from `_subagent_stop.py` — unknown agent names now exit silently. Replaced `test_unknown_agent_default_message` with `test_unknown_agent_silent` + `test_missing_name_silent`.

Documentation reflows: CLAUDE.md §14.A authoring instructions now mention `${CLAUDE_PROJECT_DIR}` + exec-form; `tools/hooks/readme.md` step 4 mirrors the change. Test count: 26 → 35; all green.

FL1 designation reflects the discovery cost (one Codex round-trip) rather than rework volume. The three corrections were single-pass, mechanically driven by the Codex comments' specific file:line citations and the Anthropic-doc verification.

## ST-4 — Cleanup + Epic close (FL declared per subtask)

(Populated as ST-4 work proceeds. Final entry: Epic-level summary consolidating all four subtask FL values and declaring the Highest Frustration Level for the Epic, mirroring the Task 092 Epic-level summary at `tasks/092-port-skill-corpora-phase-2/friction-log.md ## Epic-level summary`.)
