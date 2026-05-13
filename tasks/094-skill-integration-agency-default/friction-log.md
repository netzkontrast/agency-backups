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

## ST-2 — `.claude/` directory + plugin manifest (FL1)

Highest Frustration Level: FL1 (Codex PR #124 review surfaced one routing violation + two architectural deferrals; resolved in two follow-up commits)

Detailed account lives in [`subtasks/02-friction-log.md`](./subtasks/02-friction-log.md) (kept as a per-subtask side log to avoid bloating this Epic log). Summary:

- `.claude/settings.json` + `.claude/skills` → `../skills/` symlink + `.claude-plugin/plugin.json` (`agency@1.0.0`) shipped in a single pass; live SessionStart auto-loaded the corpus from 14 → 54 skills the moment the symlink landed.
- 17 → 16 persona re-exports under `.claude/agents/`: `sc-pm-agent` dropped per the Codex P2 #1 review (root-spec routing constraint — `/sc:pm`-only). The drift was a planning-artifact-vs-root-spec inconsistency, resolved by deleting the wrapper and recording it as a T1 mechanical correction.
- Wrappers migrated from "thin stubs" → **hybrid pattern** per the PR thread resolution (P1 #2): frontmatter exposes slug/description; body directs the activated subagent to `Skill`-load (or `Read`-fallback) `skills/<slug>/SKILL.md` before producing output. Preserves ADR-0011 D.3 single-source-of-truth.
- Plugin asset layout (P2 #3) deferred to a future ADR after a sandbox `claude plugin validate` + `install` run.
- FOLDERS.md §8 + `tools/check-clean-working-directory.py` PC.1.1 carve-outs landed in the same commit as the new folders (dual-surface drift rule).
- FL1 reflects the discovery cost of two review round-trips; the rework was mechanical.

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

## ST-4 — Cleanup + Epic close (FL0)

Highest Frustration Level: FL0

- Sequential close after ST-1/ST-2/ST-3 all merged to `main`. No new repo changes beyond the orchestration close per the subtask spec's "No other repo changes" clause.
- `tools/check-governance.sh` exits 0 against the pre-ST-4 working tree (verified before any ST-4 edit) — confirming ST-1/ST-2/ST-3 left no untreated diagnostics. Re-verified after each ST-4 edit; pre-commit gate passes on the final commit.
- `task_status: open → done` + `task_owner: unassigned → claude` flipped via `tools/fm/edit.py --set`; `updated:` bumped on `tasks/094-…/task.md`, `tasks/readme.md`, `skills/readme.md` per the subtask spec's step 3.
- `tasks/readme.md` Task 094 row updated: `Status: open → done`; the bullet now cites all four subtask PRs (#123 ST-1 / #124 ST-2 / #125 ST-3 / this PR ST-4) with merge timestamps. The skill-count typo in the index entry (52 → 54; 13 → 15 `superpowers-*`) was corrected as a T1 mechanical fix in the same edit, mirroring the ST-1 friction-log correction.
- Todo list in `task.md` flipped from `[ ]` → `[x]` for all seven items (items 1/4/5/6/7 were `[ ]` before this commit; items 2/3 were already `[x]` after ST-2/ST-3 merged).
- No new ADR filed; if Phase 3 surfaces architecture decisions (e.g. ratifying the `.claude/skills/` symlink as the canonical loader path, or formalising the `.claude/agents/` hybrid pattern), file a successor ADR per the subtask spec's out-of-scope clause.

## Epic-level summary

**Highest Frustration Level (Epic): FL1** — driven by the ST-2 + ST-3 PR review round-trips (one routing violation in ST-2; three confident Codex corrections in ST-3). Spec authoring (PR #122) + ST-1 (PR #123) + ST-4 (this PR) all closed FL0.

**Cumulative output:**

| Subtask | PR | Merged | FL | Shipped |
|---|---|---|---|---|
| Epic spec | #122 | 2026-05-12T20:05:30Z | FL0 | `task.md` + 4 subtask specs + `references/source-plan.md` + Epic-level friction-log stub |
| ST-1 — Root-spec hookup + T3 enum + T1 typo sweep | #123 | 2026-05-12T20:52:33Z | FL0 | CLAUDE.md §13 expanded (`SK.13.*` anchors); AGENTS.md "Skill Index by Category" H2; TASK.md §4.9 + RESEARCH.md §7 citations; SKILLS.md §3.3 9-value enum ratified; `F.B.11` ERROR-tier diagnostic in `tools/fm/validate.py` + `maintenance/schemas/diagnostic-explanations.json` + `test_validate_skill_kind.py` (4 tests + 12 subtests); 11 triage-note typo sweep |
| ST-2 — `.claude/` + plugin manifest | #124 | 2026-05-13T05:26:24Z | FL1 | `.claude/settings.json` + `.claude/skills` → `../skills/` symlink + 16 `.claude/agents/<slug>.md` hybrid wrappers + `.claude-plugin/plugin.json` (`agency@1.0.0`) + `.claude/skills-fallback/install-claude-dir.sh` + FOLDERS.md §8 carve-out + `tools/check-clean-working-directory.py` PC.1.1 update |
| ST-3 — Event-driven hooks | #125 | 2026-05-13T06:25:29Z | FL1 | 5 D.7-compliant hook scripts (`tools/hooks/{user-prompt-submit,pre-tool-use,post-tool-use,stop,subagent-stop}.sh` + sister `_*.py` modules + `_common.py`); `tools/check-hooks.py` (`H.1.1` / `H.1.2` / `H.1.3` diagnostics) wired as step `[5d]` of `tools/check-governance.sh`; `tools/tests/test_hooks.py` 35 tests; CLAUDE.md §14 + §14.A + PRE_COMMIT.md §7.A docs |
| ST-4 — Cleanup + Epic close | this PR | this PR | FL0 | `task_status: done`; `task_owner: claude`; Todo flips + bumps; `tasks/readme.md` row to `done` with PR trail; this Epic-level summary |

**Acceptance Criteria verification (BR.94.1 – BR.94.5):**

- **BR.94.1** — Every imported skill cited in ≥ 1 root spec; ST-1 grep verified zero orphans across 54 skills (39 `sc-*` + 15 `superpowers-*`).
- **BR.94.2** — `.claude/skills` symlink resolves to `../skills/`; `find .claude/skills -maxdepth 2 -name SKILL.md | wc -l` → 54; SKILL.md description lengths all ≤ 1536 chars (verified by `tools/fm/validate.py` ADR-0011 schema check).
- **BR.94.3** — `claude plugin validate --plugin-dir .` deferred to a future sandbox run (CLI not installed in agent harness; manifest syntactic validity confirmed by `json.load`). Documented as an open follow-up in ST-2 friction-log.
- **BR.94.4** — All 5 hooks exit 0/2 correctly on fixtures; `grep -c SessionStart .claude/settings.json` → 0; `tools/check-hooks.py` exits 0 (D.7 enforced).
- **BR.94.5** — SKILLS.md §3.3 enum lists all 9 values; `F.B.11` ERROR-tier diagnostic active; `grep -r "superclaude_framework@v4.3.0" tasks/092-port-skill-corpora-phase-2/references/triage-notes/` returns zero matches.

**Carried-forward follow-ups out of Task 094:**

- **Runtime verification of `.claude/agents/*.md` hybrid pattern** — ST-2 friction-log §"Open follow-ups" recommends dispatching `@sc-backend-architect` and confirming the `Skill`-bootstrap directive fires before producing output. If the runtime differs from Codex's PR #124 P1 #2 claim, the body's `Read`-fallback still produces correct behaviour; a future Task may file an ADR if the pattern needs formalising.
- **Plugin asset layout ADR** — ST-2 P2 #3 resolution deferred to a future Task that pairs `claude plugin validate` + `claude plugin install` in a sandbox to confirm the runtime's component-path expectations.
- **`claude plugin validate` sandbox run** — Epic AC BR.94.3 deferred (CLI not installed in the agent harness during the Epic). Trivial to retire once the CLI is available; not a structural blocker.

At PR merge, Task 094 Epic closes. ADR-0011 D.7 SessionStart prohibition remains enforced (`tools/check-hooks.py` H.1.3); Agency's bootstrap contract in AGENTS.md SS.1–SS.3 remains canonical.
