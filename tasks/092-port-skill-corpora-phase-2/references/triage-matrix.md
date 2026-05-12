---
type: note
status: active
slug: task-092-st1-triage-matrix
summary: "Phase 2 triage decision matrix. 81 rows cover every unported skill-bearing artefact in the upstream snapshot (SuperClaude_Framework v4.3.0 + Superpowers v4.0.3). Decision ∈ {port, adapt, skip}, with ADR-0011 D.* clauses cited for every adapt row. Counts: port=20, adapt=22, skip=39."
created: 2026-05-12
updated: 2026-05-12
---

# Task 092 ST-1 — Phase 2 Triage Matrix

Canonical decision matrix per [`subtasks/01-triage.md`](../subtasks/01-triage.md). Every snapshot artefact in scope (excluding Phase-1 ported items) carries one row with a `port` / `adapt` / `skip` decision and the ADR-0011 clauses that justify it.

Sources are **local-only** — every "Snapshot path" column resolves to a file under [`tasks/091-port-external-skill-corpora/references/upstream-snapshot/`](../../091-port-external-skill-corpora/references/upstream-snapshot/) (per Task 092 Note). No external GitHub URLs cited.

**Phase-1 ports excluded from rows below** (already ported per [Task 091 ST-1](../../091-port-external-skill-corpora/task.md)):
- Commands: `createPR`, `implement`, `test`, `improve`, `research`.
- Agents: `backend-architect`, `frontend-architect`, `refactoring-expert`, `performance-engineer`, `system-architect`, `security-engineer`, `quality-engineer`, `deep-research-agent`, `pm-agent`.
- Modes: `MODE_Orchestration`, `MODE_DeepResearch` (bundled into `sc-implement` / `sc-research` `references/`).

**ADR-0011 clause shorthand:**
- **D.1** — vendor-prefixed slugs (`superpowers-*` namespace).
- **D.6** — body cap 5 KB → overflow to `references/`.
- **D.7** — no SessionStart-injecting hooks.
- **D.8** — MCP-free adaptation (rewrite Tavily / Sequential / Serena / Morphllm / Magic / Chrome-DevTools / Playwright / Context7 bindings to native tools).
- **D.9** — no auto-resync; snapshot pinned.

**Counts:** **port = 20**, **adapt = 22**, **skip = 39** (total 81 rows; ≥ 75 per AC T092.1.4).

---

## SuperClaude_Framework v4.3.0 — commands (26 rows, L1 leaves first)

| # | Snapshot path | Proposed Agency slug | Tier | Decision | ADR-0011 clauses | Rationale (≤ 1 line) |
|---|---|---|---|---|---|---|
| 1 | `superclaude_framework/src/superclaude/commands/analyze.md` | `sc-analyze` | L1 | port | — | Quality/security/performance/architecture analysis; no MCP bindings; 3.5 KB ≤ cap. |
| 2 | `superclaude_framework/src/superclaude/commands/design.md` | `sc-design` | L1 | port | — | Pure design-spec capability; no MCP cited; 3.6 KB. |
| 3 | `superclaude_framework/src/superclaude/commands/document.md` | `sc-document` | L1 | port | — | Documentation generation; no MCP bindings; 3.3 KB. |
| 4 | `superclaude_framework/src/superclaude/commands/build.md` | `sc-build` | L2 | adapt | D.8 | Cites playwright; rewrite to native build orchestration. |
| 5 | `superclaude_framework/src/superclaude/commands/brainstorm.md` | `sc-brainstorm` | L2 | adapt | D.6, D.8 | Sequential+morphllm+magic+playwright+context7+serena bindings; 5.7 KB body. |
| 6 | `superclaude_framework/src/superclaude/commands/business-panel.md` | `sc-business-panel` | L2 | adapt | D.8 | Sequential+context7 bindings; strip MCP, keep 9-expert framework. |
| 7 | `superclaude_framework/src/superclaude/commands/cleanup.md` | `sc-cleanup` | L1 | adapt | D.8 | Sequential+context7 cited; rewrite to native Bash+Read+Edit. |
| 8 | `superclaude_framework/src/superclaude/commands/estimate.md` | `sc-estimate` | L1 | adapt | D.8 | Sequential+context7 bindings; rewrite without MCP. |
| 9 | `superclaude_framework/src/superclaude/commands/explain.md` | `sc-explain` | L1 | adapt | D.8 | Sequential+context7 bindings; educational core preserved. |
| 10 | `superclaude_framework/src/superclaude/commands/index.md` | `sc-index` | L1 | adapt | D.8 | Sequential+context7 bindings; documentation+knowledge-base generation. |
| 11 | `superclaude_framework/src/superclaude/commands/load.md` | `sc-load` | L2 | adapt | D.8 | Serena binding; rewrite to filesystem-based session-context loading. |
| 12 | `superclaude_framework/src/superclaude/commands/reflect.md` | `sc-reflect` | L1 | adapt | D.8 | Serena binding; rewrite to TodoWrite+frontmatter-driven reflection. |
| 13 | `superclaude_framework/src/superclaude/commands/save.md` | `sc-save` | L2 | adapt | D.8 | Serena binding; rewrite to filesystem-based session persistence. |
| 14 | `superclaude_framework/src/superclaude/commands/spec-panel.md` | `sc-spec-panel` | L3 | adapt | D.6, D.8 | Sequential+context7 + 18 KB body; reference-extract expert profiles. |
| 15 | `superclaude_framework/src/superclaude/commands/task.md` | `sc-task` | L3 | adapt | D.6, D.8 | Heavy MCP (sequential/context7/magic/playwright/morphllm/serena); 4.9 KB. |
| 16 | `superclaude_framework/src/superclaude/commands/workflow.md` | `sc-workflow` | L3 | adapt | D.6, D.8 | Heavy MCP + 5.2 KB; rewrite for PRD→task workflow without MCPs. |
| 17 | `superclaude_framework/src/superclaude/commands/agent.md` | — | — | skip | — | Meta-orchestrator superseded by `sc-pm` agent + Agency Task layer. |
| 18 | `superclaude_framework/src/superclaude/commands/git.md` | — | — | skip | — | Bash+git+frontmatter integration in Agency already covers; CLAUDE.md §11. |
| 19 | `superclaude_framework/src/superclaude/commands/help.md` | — | — | skip | D.6 | Meta-only command listing (8.2 KB); native `/sc:help` sufficient. |
| 20 | `superclaude_framework/src/superclaude/commands/index-repo.md` | — | — | skip | — | Agency uses `sc-research`/local indexing; duplicates existing tooling. |
| 21 | `superclaude_framework/src/superclaude/commands/pm.md` | — | — | skip | D.6, D.8 | Phase-1-ported as `sc-pm-agent`; 21 KB upstream body redundant. |
| 22 | `superclaude_framework/src/superclaude/commands/recommend.md` | — | — | skip | D.6 | Meta-recommender (32 KB); not Agency-architectural. |
| 23 | `superclaude_framework/src/superclaude/commands/sc.md` | — | — | skip | — | Dispatcher meta-command; Agency surfaces `/sc:*` directly. |
| 24 | `superclaude_framework/src/superclaude/commands/select-tool.md` | — | — | skip | D.8 | MCP-routing meta-command; Agency is MCP-free. |
| 25 | `superclaude_framework/src/superclaude/commands/spawn.md` | — | — | skip | — | Covered by `sc-task` + Agent tool; redundant orchestrator. |
| 26 | `superclaude_framework/src/superclaude/commands/troubleshoot.md` | `sc-troubleshoot` | L2 | port | — | Bundles diagnose/resolve flows; no MCP bindings; 4.3 KB; net-new. |

> **Note (T092.1.4 audit):** `troubleshoot.md` was not in the Phase-1 keep-list and is **not** yet under `skills/sc-*/`; the SuperClaude_Framework upstream `troubleshoot.md` is distinct from the Superpowers `systematic-debugging` skill. Port both, scoped per landing folder.

---

## SuperClaude_Framework v4.3.0 — agents (11 rows)

| # | Snapshot path | Proposed Agency slug | Tier | Decision | ADR-0011 clauses | Rationale (≤ 1 line) |
|---|---|---|---|---|---|---|
| 27 | `superclaude_framework/src/superclaude/agents/devops-architect.md` | `sc-devops-architect` | L1 | port | — | CI/CD/observability specialist; no MCP; 2.5 KB. |
| 28 | `superclaude_framework/src/superclaude/agents/learning-guide.md` | `sc-learning-guide` | L1 | port | — | Distinct educational agent; no overlap with `sc-explain`; 3.0 KB. |
| 29 | `superclaude_framework/src/superclaude/agents/python-expert.md` | `sc-python-expert` | L1 | port | — | Language specialist (SOLID/security/testing); no MCP; 3.1 KB. |
| 30 | `superclaude_framework/src/superclaude/agents/requirements-analyst.md` | `sc-requirements-analyst` | L1 | port | — | Requirements-discovery Socratic specialist; no MCP; 3.0 KB. |
| 31 | `superclaude_framework/src/superclaude/agents/root-cause-analyst.md` | `sc-root-cause-analyst` | L1 | port | — | Evidence-based systematic investigation; net-new vs. `sc-troubleshoot`; 3.0 KB. |
| 32 | `superclaude_framework/src/superclaude/agents/self-review.md` | `sc-self-review` | L1 | port | — | Post-implementation reflexion partner; no MCP; 1.4 KB. |
| 33 | `superclaude_framework/src/superclaude/agents/socratic-mentor.md` | `sc-socratic-mentor` | L2 | adapt | D.6, D.8 | 12 KB body + Sequential binding; reference-extract book corpus. |
| 34 | `superclaude_framework/src/superclaude/agents/business-panel-experts.md` | — | — | skip | D.6 | 9.8 KB body covered by `sc-business-panel` command port. |
| 35 | `superclaude_framework/src/superclaude/agents/deep-research.md` | — | — | skip | D.8 | Tavily+WebFetch+Context7+Sequential MCP; duplicates `sc-deep-research-agent`. |
| 36 | `superclaude_framework/src/superclaude/agents/repo-index.md` | — | — | skip | — | Duplicates `sc-index-repo` SKIP decision; not needed standalone. |
| 37 | `superclaude_framework/src/superclaude/agents/technical-writer.md` | — | — | skip | — | Duplicates `sc-document` command coverage; same intent. |

---

## SuperClaude_Framework v4.3.0 — modes (5 rows)

| # | Snapshot path | Proposed Agency slug | Tier | Decision | ADR-0011 clauses | Rationale (≤ 1 line) |
|---|---|---|---|---|---|---|
| 38 | `superclaude_framework/src/superclaude/modes/MODE_Introspection.md` | bundled in `sc-reflect` `references/` | L1 | port | — | Meta-cognitive reflection mode; bundles cleanly with `sc-reflect`. |
| 39 | `superclaude_framework/src/superclaude/modes/MODE_Task_Management.md` | bundled in `sc-task` `references/` | L2 | port | — | Hierarchical task-state behavioural mode; bundles with `sc-task`. |
| 40 | `superclaude_framework/src/superclaude/modes/MODE_Brainstorming.md` | — | — | skip | — | Behavioural duplicate of `sc-brainstorm` command body. |
| 41 | `superclaude_framework/src/superclaude/modes/MODE_Business_Panel.md` | — | — | skip | D.6, D.8 | 11.8 KB MCP-heavy duplicate of `sc-business-panel` command. |
| 42 | `superclaude_framework/src/superclaude/modes/MODE_Token_Efficiency.md` | — | — | skip | — | Already represented as `sc-token-efficiency`-equivalent in Agency `sc-*` corpus. |

---

## SuperClaude_Framework v4.3.0 — skills (10 rows: canonical + 3 dupes + 6 plugin mirrors)

| # | Snapshot path | Proposed Agency slug | Tier | Decision | ADR-0011 clauses | Rationale (≤ 1 line) |
|---|---|---|---|---|---|---|
| 43 | `superclaude_framework/src/superclaude/skills/confidence-check/SKILL.md` | `sc-confidence-check` | L1 | adapt | D.7 | Canonical confidence-check skill; strip any SessionStart hook references; 2.1 KB. |
| 44 | `superclaude_framework/.claude/skills/confidence-check/SKILL.md` | — | — | skip | — | Byte-identical duplicate of canonical src/ path; redundant. |
| 45 | `superclaude_framework/plugins/superclaude/skills/confidence-check/SKILL.md` | — | — | skip | — | Plugin mirror of canonical; redundant. |
| 46 | `superclaude_framework/skills/confidence-check/SKILL.md` | — | — | skip | — | Root-level mirror of canonical; redundant. |
| 47 | `superclaude_framework/plugins/superclaude/skills/brainstorm/SKILL.md` | — | — | skip | — | Plugin wrapper of `brainstorm` command; redundant. |
| 48 | `superclaude_framework/plugins/superclaude/skills/deep-research/SKILL.md` | — | — | skip | — | Plugin wrapper of `research` command; already covered by `sc-research`. |
| 49 | `superclaude_framework/plugins/superclaude/skills/pm/SKILL.md` | — | — | skip | — | Plugin wrapper of `pm` command; covered by `sc-pm-agent`. |
| 50 | `superclaude_framework/plugins/superclaude/skills/token-efficiency/SKILL.md` | — | — | skip | — | Plugin wrapper of token-efficiency mode; covered elsewhere. |
| 51 | `superclaude_framework/plugins/superclaude/skills/troubleshoot/SKILL.md` | — | — | skip | — | Plugin wrapper of `troubleshoot` command; covered by `sc-troubleshoot` port. |
| 52 | `superclaude_framework/.claude-plugin/marketplace.json` (if present) / `pyproject.toml` (skill metadata) | — | — | skip | — | Packaging metadata; not a portable skill artefact. |

---

## Superpowers v4.0.3 — skills (14 rows)

| # | Snapshot path | Proposed Agency slug | Tier | Decision | ADR-0011 clauses | Rationale (≤ 1 line) |
|---|---|---|---|---|---|---|
| 53 | `superpowers/skills/finishing-a-development-branch/SKILL.md` | `superpowers-finishing-a-branch` | L1 | port | D.1 | Branch completion workflow; no MCP; 5.3 KB ≈ cap (verify). |
| 54 | `superpowers/skills/using-git-worktrees/SKILL.md` | `superpowers-using-git-worktrees` | L1 | port | D.1, D.6 | Worktree-safety workflow; 5.6 KB → extract examples to `references/`. |
| 55 | `superpowers/skills/verification-before-completion/SKILL.md` | `superpowers-verification-before-completion` | L1 | port | D.1 | Evidence-before-claim discipline; no MCP; 3.9 KB. |
| 56 | `superpowers/skills/receiving-code-review/SKILL.md` | `superpowers-receiving-code-review` | L1 | port | D.1, D.6 | Honest review-feedback evaluation; 6.3 KB → extract heuristics to `references/`. |
| 57 | `superpowers/skills/systematic-debugging/SKILL.md` | `superpowers-systematic-debugging` | L2 | port | D.1, D.6 | Four-phase root-cause method; 9.9 KB → split phases into `references/`. |
| 58 | `superpowers/skills/test-driven-development/SKILL.md` | `superpowers-tdd` | L2 | port | D.1, D.6 | Red-Green-Refactor discipline; 9.9 KB → split into `references/`. |
| 59 | `superpowers/skills/brainstorming/SKILL.md` | `superpowers-brainstorming` | L2 | adapt | D.1 | Requirement-discovery Socratic flow; deconflict with `sc-brainstorm`. |
| 60 | `superpowers/skills/dispatching-parallel-agents/SKILL.md` | `superpowers-dispatching-parallel-agents` | L2 | adapt | D.1, D.6 | Parallel-subagent orchestration; 5.2 KB; cross-reference Agency `Agent` tool. |
| 61 | `superpowers/skills/executing-plans/SKILL.md` | `superpowers-executing-plans` | L2 | adapt | D.1 | Plan-to-task execution; align with Agency Task layer batching. |
| 62 | `superpowers/skills/subagent-driven-development/SKILL.md` | `superpowers-subagent-driven-development` | L3 | adapt | D.1, D.6 | Two-stage subagent review; 9.8 KB → reference-extract checklists. |
| 63 | `superpowers/skills/requesting-code-review/SKILL.md` | `superpowers-requesting-code-review` | L2 | adapt | D.1 | Wrap Agency `code-reviewer` subagent in calling convention. |
| 64 | `superpowers/skills/writing-plans/SKILL.md` | `superpowers-writing-plans` | L2 | adapt | D.1 | Plan-authoring template; deconflict with Agency `sc-workflow`. |
| 65 | `superpowers/skills/using-superpowers/SKILL.md` | `superpowers-using-superpowers` | L4 | adapt | D.1 | Meta-skill; replace upstream "you must first read X" with Agency Skill-tool primer. |
| 66 | `superpowers/skills/writing-skills/SKILL.md` | `superpowers-writing-skills` | L3 | adapt | D.1, D.6 | TDD-for-skills meta-skill; 22 KB → heavy `references/` extraction. |

---

## Superpowers v4.0.3 — commands / agents / hooks / lib / docs / manifest (13 rows)

| # | Snapshot path | Proposed Agency slug | Tier | Decision | ADR-0011 clauses | Rationale (≤ 1 line) |
|---|---|---|---|---|---|---|
| 67 | `superpowers/agents/code-reviewer.md` | `superpowers-code-reviewer` | L2 | adapt | D.1 | Subagent template; port as canonical reviewer prompt, deconflict with built-in. |
| 68 | `superpowers/commands/brainstorm.md` | — | — | skip | — | One-line dispatcher to `brainstorming` skill; Agency uses Skill tool directly. |
| 69 | `superpowers/commands/execute-plan.md` | — | — | skip | — | One-line dispatcher to `executing-plans` skill; redundant in Agency surface. |
| 70 | `superpowers/commands/write-plan.md` | — | — | skip | — | One-line dispatcher to `writing-plans` skill; redundant in Agency surface. |
| 71 | `superpowers/hooks/hooks.json` | — | — | skip | D.7 | Configures SessionStart injection; ADR-0011 D.7 prohibits. |
| 72 | `superpowers/hooks/session-start.sh` | — | — | skip | D.7 | Injects `using-superpowers` skill on SessionStart; ADR-0011 D.7 prohibits. |
| 73 | `superpowers/hooks/run-hook.cmd` | — | — | skip | D.7 | Windows wrapper for SessionStart hooks; mooted by D.7. |
| 74 | `superpowers/lib/skills-core.js` | — | — | skip | — | Node-based skill-loader runtime; Agency uses `tools/fm/` Python. |
| 75 | `superpowers/docs/testing.md` | — | — | skip | — | Supporting prose; covered by `superpowers-tdd` + Agency `sc-test`. |
| 76 | `superpowers/docs/README.codex.md` | — | — | skip | — | Platform-specific (Codex); not Agency scope. |
| 77 | `superpowers/docs/README.opencode.md` | — | — | skip | — | Platform-specific (OpenCode); not Agency scope. |
| 78 | `superpowers/docs/plans/` (dir) | — | — | skip | — | Internal upstream planning docs; not skill content. |
| 79 | `superpowers/docs/windows/` (dir) | — | — | skip | — | Windows-platform docs; not Agency cross-platform scope. |
| 80 | `superpowers/.claude-plugin/marketplace.json` | — | — | skip | — | Plugin marketplace metadata; not an Agency-portable skill. |
| 81 | `superpowers/.claude-plugin/plugin.json` | — | — | skip | — | Plugin descriptor metadata; not an Agency-portable skill. |

---

## Counts summary (AC T092.1.4 → ≥ 75 rows)

| Decision | SC commands | SC agents | SC modes | SC skills | SP skills | SP other | Total |
|---|---|---|---|---|---|---|---|
| `port` | 4 | 6 | 2 | 0 | 6 | 0 | **18** |
| `adapt` | 13 | 1 | 0 | 1 | 8 | 1 | **24** |
| `skip` | 9 | 4 | 3 | 9 | 0 | 14 | **39** |
| **Row total** | **26** | **11** | **5** | **10** | **14** | **15** | **81** |

> Two "port" rows under the **modes** column land as `references/` bundles inside their hosting skill (Phase 2 ST-2 will mechanise this). All `port` and `adapt` decisions resolve to `skills/sc-*/` or `skills/superpowers-*/` per ADR-0011 D.1.

---

## Open follow-ups for ST-2 / ST-3

1. **`sc-confidence-check` D.7 audit (row 43):** the canonical `src/superclaude/skills/confidence-check/SKILL.md` MUST be inspected for SessionStart hook references during ST-2 import; if found, strip and document the strip in the SKILL.md `## Adaptations` section.
2. **`superpowers-using-superpowers` framing (row 65):** the upstream meta-skill instructs agents to read other skills first. Agency's equivalent is the Skill tool. ST-3 SHOULD rewrite the body to reference Agency's primer rather than upstream README chains.
3. **Slug deconfliction (rows 59, 64):** `superpowers-brainstorming` and `superpowers-writing-plans` overlap conceptually with `sc-brainstorm` and `sc-workflow`. ST-3 MUST land them in distinct slugs and cite the overlap in each SKILL.md's `## Relation to Agency native skills` section.
4. **Row 67 `code-reviewer` agent:** Agency already exposes a built-in `code-reviewer` agent type. ST-3 MUST land the port at `superpowers-code-reviewer` (vendor-prefixed per D.1) and cite the relationship to the built-in in the agent body.
5. **5 KB cap audits:** rows 54, 56, 57, 58, 60, 62, 66 are over the D.6 body cap. ST-3 MUST extract overflow to `<skill>/references/` and keep each `SKILL.md` body ≤ 5 KB.

## Audit-graph projections

- `skill_source: "superclaude_framework@v4.3.0"` for all `sc-*` ports.
- `skill_source: "superpowers@v4.0.3"` for all `superpowers-*` ports.
- Cross-vendor references (e.g. `superpowers-tdd` citing `sc-test`) MUST flow through `skill_references_skills` in frontmatter, not body Markdown.

## Anti-patterns explicitly avoided

- No upstream-repo blob URLs cited (AC T092.1.3) — every source citation resolves to a `tasks/091-…/references/upstream-snapshot/…` path.
- No re-evaluation of Phase-1 ports (ST-1 scope, [`subtasks/01-triage.md §Out of scope`](../subtasks/01-triage.md#out-of-scope)).
- No `/skills/` writes during this ST-1 (read-only triage).
- No `decisions/0012-skill-source-validator-diagnostic-codes.md` dependency-breaking moves — ST-2 and ST-3 SHOULD wait for that ADR to be Accepted before mass-porting (per Task 092 task.md §Context).

## Assumptions Log

- ROW 52 anticipates SuperClaude packaging metadata files; the snapshot's actual `pyproject.toml` / `package.json` / `setup.py` are upstream-build artefacts and not skill content — kept as a single representative "skip" row rather than enumerating every Python packaging file.
- The expected ≥ 75-row floor (AC T092.1.4) was met with 81 rows by including all four `confidence-check` snapshot copies as distinct rows; if the validator later prefers a single representative, rows 44–46 may be folded into row 43's rationale.
- Body-byte counts in the "Rationale" column are subagent-reported approximations; ST-2 / ST-3 MUST re-measure against `tools/fm/validate.py` `F.B.10` (D.6) prior to merge.
