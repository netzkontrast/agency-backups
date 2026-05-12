> **Editorial note (added when embedding this plan as the Epic task's `references/full-plan.md`):**
>
> This document is the *complete planning record* produced during the `/sc:brainstorm` → `/sc:design` → `/sc:implement` cycle that authored this Epic. **Three** renumberings were applied post-hoc to keep the embedded plan consistent with the realized repository state:
>
> 1. **`ADR-0010` → `ADR-0011`** throughout. The 0010 slot was already taken by [`decisions/0010-novel-architect-error-tier-linter-policy.md`](../../../decisions/0010-novel-architect-error-tier-linter-policy.md) (created the same day, discovered after the initial commit on this branch). The renumber preserved all content verbatim. The active ADR for this Epic is [`decisions/0011-external-skill-corpora-import.md`](../../../decisions/0011-external-skill-corpora-import.md). Gherkin anchors `ADR.10.{1,2,3}` correspondingly became `ADR.11.{1,2,3}`.
> 2. **`<NNN>` / `<NNN+1>`** in §10.5 "Task A" / "Task B" scaffolds → realized as **Task 091** (this Epic) with two subtasks: **ST-1** (`subtasks/01-phase-1-corpus.md` — Task A's corpus work) and **ST-2** (`subtasks/02-phase-1-hookup.md` — Task B's hookup work). The two-Task design from §10.5 is preserved as a two-subtask design under one Epic.
> 3. **Task 090 → Task 091.** The Epic was initially filed as Task 090, but when this branch synced with `main` two existing `tasks/090-*` folders were discovered (`090-codex-pr-review` and `090-review-pr109-archive-spec`, both claiming `task_id: "090"` — a duplicate which itself awaits a `TASK.md §8.1` renumber on main). To avoid a triple-collision, this Epic was renumbered to the next free slot **091**. All folder paths and `task_id` frontmatter values were updated; section anchors (§1–§10) and Gherkin AC anchors (`BR.9.*`, `TA.1.*`, `TB.1.*`) are unchanged.
>
> Section anchors (§1–§10) and Gherkin AC anchors (`BR.9.*`, `TA.1.*`, `TB.1.*`) are unchanged. References to "Phase 2 / Phase 3" in §5 / §9.8 describe future expansion beyond what this Epic delivers; those are explicitly out of scope for Task 091.

---

# Port SuperClaude_Framework & Superpowers skill/agent corpora into `netzkontrast/agency`

## Context

`netzkontrast/agency` is a governance & orchestration substrate (not an app) built around four decoupled concerns — **Machine (Task) / Actor (Prompt) / Space (Research) / Capability (Skill)** — with strict pre-commit governance (`tools/check-governance.sh`), an L1+L2 frontmatter ontology (YAML depth ≤ 1), RFC 2119 + Gherkin spec language, MADR 4.0.0 ADRs at `/decisions/`, and a skills sync mechanism (`skills/skills-skill-bootstrap/sync.sh`) that pushes `origin/main:skills/` → `~/.claude/skills/`.

`AGENTS.md → Closing Run Procedure` and `CLAUDE.md §13` already reference `/sc:createPR` and other `/sc:*` commands as if they exist in the skills tree — but only **22** skills exist today (mostly narrative + meta), so the `/sc:*` references are aspirational. Meanwhile, the upstream **SuperClaude_Framework** (31 commands, 20 agents, 7 modes, 9 MCP integrations) and **Superpowers** plugin (14 skills, 3 commands, 1 agent, SessionStart hook) hold a large library of proven engineering skills Agency would benefit from.

This plan:

1. Catalogs **every** SuperClaude command/agent/mode/MCP and **every** Superpowers skill/command/hook.
2. Classifies each into **must-have / nice-to-have / skip** tiers (per user direction).
3. Specifies the porting policy via a new **ADR-0011** (architectural decision: external skill corpora import, namespace prefixing, attribution, sync cadence).
4. Drafts three **Task scaffolds** under `/tasks/` that execute the port in order.
5. Keeps the prefix convention (`skills/sc-*/`, `skills/superpowers-*/`) so provenance is preserved and CLAUDE.md §13 finally resolves.

The deliverable is execution-ready: an operator can take this plan, file the ADR and three Tasks, and run them through Agency's standard `task_status: open → in_progress → done` workflow with the pre-commit gate enforcing frontmatter, structure, and audit-graph linkage at every commit.

---

## 1. Recap of what already lives in Agency

| Layer | Already present | Implication for porting |
|---|---|---|
| Root specs | `AGENTS.md`, `TASK.md`, `PROMPT.md`, `RESEARCH.md`, `SKILLS.md`, `FOLDERS.md`, `PRE_COMMIT.md`, `FRUSTRATED.md`, `MAINTENANCE.md`, `CLAUDE.md`, `README.md` | New SKILL.md files MUST satisfy `SKILLS.md §3` (L1+L2 frontmatter), `SKILLS.md §5` (5 required H2 sections), `SKILLS.md §7` (bootstrap protocol). |
| Existing skills (22) | `dramatica-theory`, `dramatica-vocabulary`, `ncp-author`, `novel-architect{,-character,-legacy,-scene,-structure,-world}`, `suno-lyric-writer`, `the-agency-system-architect`, `drive-markdown-converter`, `gdrive-notion-curator`, `notebooklm-prompt-architect`, `pdf-to-markdown`, `prompt-optimizer`, `research-prompt-optimizer`, `ralph-skill`, `skill-creator` (Anthropic mirror), `skills-skill-bootstrap`, `spec-skill`, `suno-lyric-writer` | Narrative skills + research/prompt skills are out of scope for this port. **Do not duplicate** `skill-creator` or `spec-skill`. **Do not duplicate** the `prompt-optimizer` / `research-prompt-optimizer` workflow with `sc:brainstorm` — they coexist (see §4 nice-to-have rationale). |
| Governance | `tools/check-governance.sh` runs `tools/fm/validate.py`, `tools/lint-structure.py`, `tools/lint-linkage.py`, `tools/adr/cli.py validate`, `tools/check-rfc2119-polarity.py`, plus 15+ advisory linters. ADRs 0001–0009 already live in `/decisions/`. | Every new SKILL.md commit triggers full governance. Files >5 KB MUST push prose into `references/` (T2 ladder, SKILLS.md §7.3). New top-level concept (e.g. importing external corpora) MUST land via ADR before the porting Tasks file. |
| Sync mechanism | `skills/skills-skill-bootstrap/sync.sh` + `verify.sh` (live, tested) | Ported skills inherit the sync — once they land on `main`, `sync.sh` materialises them under `~/.claude/skills/sc-*` and `~/.claude/skills/superpowers-*` on the next agent session. No additional installer needed. |
| Already-referenced upstream | `AGENTS.md` Closing Run Procedure cites `https://github.com/netzkontrast/SuperClaude_Framework/blob/main/src/superclaude/commands/createPR.md`; `CLAUDE.md §13` enumerates `sc:implement, sc:test, sc:createPR, sc:improve, sc:research` | These references are currently dangling. The port will resolve them. |

Critical files to read before executing the port (the porting agent's required reading list):

- `AGENTS.md` (entry-point + closing-run procedure)
- `SKILLS.md` §3, §5, §7.2–§7.4 (frontmatter, required sections, bootstrap invariants, three-tier ladder)
- `templates/skill.md` (canonical skeleton — copy this, do not freelance frontmatter)
- `decisions/0007-skill-bundles-tools-frontmatter.md` (precedent for adding L2 keys via ADR)
- `decisions/0008-narrative-skills-status-quo.md` (precedent for documenting "skills as-is" without normative cleanup)
- `skills/ralph-skill/SKILL.md` (example of a complex skill with `references/` directory — same shape the imported skills will take)

---

## 2. SuperClaude_Framework inventory (canonical reference)

Upstream layout: `src/superclaude/{commands,agents,modes,mcp,skills,hooks}/`. Distribution: `pipx install superclaude` → installs to `~/.claude/commands/sc/{slug}.md`. Frontmatter shape: `name`, `description`, `category`, plus optional `complexity`, `mcp-servers`, `personas`.

### 2.1 Commands (31)

| # | Slug | Purpose (one-line) | Activated agents/MCP | Port tier | Target Agency path |
|---|---|---|---|---|---|
| 1 | `sc:agent` | AI agent selection and direct invocation | any specialized agent · Context7, Sequential | **nice** | `skills/sc-agent/` |
| 2 | `sc:analyze` | Comprehensive code analysis (quality, security, perf) | quality-engineer, security-engineer, performance-engineer · Sequential, Context7 | **must** | `skills/sc-analyze/` |
| 3 | `sc:brainstorm` | Socratic dialogue for requirements discovery | socratic-mentor, requirements-analyst · Sequential, Context7, Magic, Playwright, Morphllm, Serena | **must** | `skills/sc-brainstorm/` |
| 4 | `sc:build` | Build/compile/package projects | devops-architect, backend-architect · Sequential, Playwright | **nice** | `skills/sc-build/` |
| 5 | `sc:business-panel` | 8-expert business analysis | business-panel-experts · Sequential, Serena | **must** | `skills/sc-business-panel/` |
| 6 | `sc:cleanup` | Remove dead code, optimize structure | refactoring-expert, backend-architect · Sequential | **nice** | `skills/sc-cleanup/` |
| 7 | `sc:createPR` | Open PR as session-closing step | (GitHub MCP) | **must (already cited)** | `skills/sc-createPR/` |
| 8 | `sc:design` | System architecture & API design | system-architect, backend-architect, frontend-architect · Context7, Sequential, Magic | **must** | `skills/sc-design/` |
| 9 | `sc:document` | Documentation generation | technical-writer · Context7, Magic | **nice** | `skills/sc-document/` |
| 10 | `sc:estimate` | Time/effort estimation | pm-agent · Sequential | **nice** | `skills/sc-estimate/` |
| 11 | `sc:explain` | Educational explanations of code/concepts | learning-guide, technical-writer · Context7 | **nice** | `skills/sc-explain/` |
| 12 | `sc:git` | Git operations with intelligent commit messages | (builtin git) · Serena | **skip** (overlaps with Agency's strict git rules in `CLAUDE.md §11`) | — |
| 13 | `sc:help` | List/explain all commands | (builtin) | **skip** (Claude Code surfaces this natively via the skill listing) | — |
| 14 | `sc:implement` | Feature implementation with persona activation | architect, frontend-architect, backend-architect, security-engineer, quality-engineer · Context7, Sequential, Magic, Playwright | **must (cited in CLAUDE.md §13)** | `skills/sc-implement/` |
| 15 | `sc:improve` | Systematic quality/performance improvements | quality-engineer, refactoring-expert, performance-engineer · Sequential | **must (cited in CLAUDE.md §13)** | `skills/sc-improve/` |
| 16 | `sc:index` | Project documentation & knowledge base | repo-index · Sequential, Context7 | **skip** (overlaps with `tools/fm/query.py` + `tasks/readme.md` index) | — |
| 17 | `sc:index-repo` | Repo indexing with 94% token reduction | repo-index | **nice** (the 94% claim is interesting for `tools/fm/`) | `skills/sc-index-repo/` |
| 18 | `sc:load` | Session loading with Serena MCP | pm-agent · Serena | **skip** (requires Serena, out-of-scope external dep) | — |
| 19 | `sc:pm` | Project Management Agent | pm-agent · Serena, Sequential | **nice** (depends on pm-agent agent port) | `skills/sc-pm/` |
| 20 | `sc:recommend` | Command recommendation engine | (builtin) | **skip** (meta-tool, no value once Agency surfaces skills via `Skill` tool) | — |
| 21 | `sc:reflect` | Task reflection & validation | root-cause-analyst, learning-guide · Serena, Sequential | **must** (aligns with Agency's `FRUSTRATED.md` retrospective) | `skills/sc-reflect/` |
| 22 | `sc:research` | Deep web research with adaptive planning | deep-research-agent · Tavily, Sequential, Playwright, Context7, Serena | **must (cited in CLAUDE.md §13)** | `skills/sc-research/` |
| 23 | `sc:save` | Session save with Serena | pm-agent · Serena | **skip** (Serena dep) | — |
| 24 | `sc:sc` | Show commands & framework status | (builtin) | **skip** (meta) | — |
| 25 | `sc:select-tool` | MCP tool selection by complexity score | (builtin) | **skip** (Claude Code has its own `ToolSearch`) | — |
| 26 | `sc:spawn` | Meta-system task orchestration | pm-agent · Sequential | **nice** | `skills/sc-spawn/` |
| 27 | `sc:spec-panel` | Multi-expert spec review | spec-panel (5 personas) · Sequential | **must** (Agency is spec-heavy — this is a natural fit) | `skills/sc-spec-panel/` |
| 28 | `sc:task` | Complex task execution | pm-agent, task-decomposition agents · Sequential, Serena | **skip** (Agency `/tasks/` system is canonical; this would duplicate) | — |
| 29 | `sc:test` | Test execution with coverage | quality-engineer, pytest runner · Playwright, Sequential | **must** (Agency runs pytest under `tools/tests/`) | `skills/sc-test/` |
| 30 | `sc:troubleshoot` | Diagnose code/build/deploy issues | root-cause-analyst, security-engineer · Sequential, Playwright | **must** | `skills/sc-troubleshoot/` |
| 31 | `sc:workflow` | Generate workflows from PRDs | pm-agent, architect · Sequential | **nice** | `skills/sc-workflow/` |

**Must-have count**: 12 commands. **Nice-to-have**: 11. **Skip**: 8.

### 2.2 Agents (20)

| # | Slug | Purpose (one-line) | Port tier | Target Agency path |
|---|---|---|---|---|
| 1 | `backend-architect` | Reliable backend, data integrity, fault tolerance | **nice** | `skills/sc-backend-architect/` |
| 2 | `business-panel-experts` | 8-expert business panel (Founder, Product, Ops, Marketing, Finance, Legal, CS, Tech) | **must** (paired with `sc:business-panel`) | `skills/sc-business-panel-experts/` |
| 3 | `deep-research-agent` | Autonomous web research, multi-hop, quality scoring | **must** (paired with `sc:research`) | `skills/sc-deep-research-agent/` |
| 4 | `deep-research` | Simpler research trigger | **skip** (subsumed by `deep-research-agent`) | — |
| 5 | `devops-architect` | Infrastructure, deployment, monitoring | **nice** | `skills/sc-devops-architect/` |
| 6 | `frontend-architect` | UI, UX, accessibility, framework patterns | **nice** | `skills/sc-frontend-architect/` |
| 7 | `learning-guide` | Educational mentoring, Socratic explanation | **nice** | `skills/sc-learning-guide/` |
| 8 | `performance-engineer` | Performance, memory, throughput | **must** (paired with `sc:analyze`) | `skills/sc-performance-engineer/` |
| 9 | `pm-agent` | Self-improvement; documents, analyzes, persists memory | **must** (referenced by 7+ commands; MANDATORY session-start) | `skills/sc-pm-agent/` |
| 10 | `python-expert` | Python-specific (type hints, async) | **nice** (Agency tools/ are Python 3.11 stdlib only) | `skills/sc-python-expert/` |
| 11 | `quality-engineer` | Test strategy, coverage, gates | **must** (paired with `sc:test`/`sc:analyze`) | `skills/sc-quality-engineer/` |
| 12 | `refactoring-expert` | Refactoring, dead code, tech debt | **nice** | `skills/sc-refactoring-expert/` |
| 13 | `repo-index` | Repo indexing, knowledge base | **nice** (paired with `sc:index-repo`) | `skills/sc-repo-index/` |
| 14 | `requirements-analyst` | Requirements gathering, AC definition | **must** (paired with `sc:brainstorm`) | `skills/sc-requirements-analyst/` |
| 15 | `root-cause-analyst` | RCA, error investigation | **must** (paired with `sc:troubleshoot`/`sc:reflect`) | `skills/sc-root-cause-analyst/` |
| 16 | `security-engineer` | Security arch, vuln assessment, threat modeling | **must** | `skills/sc-security-engineer/` |
| 17 | `self-review` | Post-implementation validation | **must** (aligns with Agency's pre-commit gate philosophy) | `skills/sc-self-review/` |
| 18 | `socratic-mentor` | Socratic dialogue for discovery | **must** (paired with `sc:brainstorm`) | `skills/sc-socratic-mentor/` |
| 19 | `system-architect` | System-level architecture | **must** (paired with `sc:design`) | `skills/sc-system-architect/` |
| 20 | `technical-writer` | Docs, technical guides, API docs | **nice** (paired with `sc:document`) | `skills/sc-technical-writer/` |

**Must-have agents**: 11. **Nice-to-have**: 8. **Skip**: 1.

Note: SuperClaude calls these "agents" but they're shipped as `.md` files with frontmatter — exactly the SKILL.md shape. Port them as skills with `skill_kind: domain` or `skill_kind: orchestrator`.

### 2.3 Modes (7)

| Slug | Purpose | Port tier | Target |
|---|---|---|---|
| `MODE_Brainstorming` | Socratic dialogue, non-presumptive | **must** (bundled with `sc:brainstorm` skill as `references/MODE_Brainstorming.md`) | inside `skills/sc-brainstorm/references/` |
| `MODE_Business_Panel` | 8-expert parallel analysis | **must** (bundled inside `skills/sc-business-panel/references/`) | — |
| `MODE_DeepResearch` | Adaptive planning, multi-hop, quality scoring | **must** (bundled inside `skills/sc-research/references/`) | — |
| `MODE_Introspection` | Meta-cognitive analysis, retrospective | **must** (bundled inside `skills/sc-reflect/references/`) | — |
| `MODE_Orchestration` | Multi-agent coordination, tool routing | **nice** (bundled inside `skills/sc-spawn/references/` if `sc:spawn` is ported) | — |
| `MODE_Task_Management` | TodoWrite tracking, checkpoint, multi-phase | **skip** (Agency `/tasks/` system is canonical; would conflict) | — |
| `MODE_Token_Efficiency` | Aggressive summarization, 30-50% token reduction | **nice** (could live as a standalone `skills/sc-token-efficiency/`) | `skills/sc-token-efficiency/` |

**Rationale for bundling modes inside skills**: SuperClaude's modes are behavioral framing, not standalone capabilities. In Agency's SKILLS.md model, behavioral framing belongs in a skill's body (T2) or a `references/MODE_*.md` (T3). Standalone mode files would violate the T1/T2/T3 ladder.

### 2.4 MCP servers (9)

Agency does not ship MCP server configs (it's a governance repo, not a Claude Code installer). However, documentation of which MCP each skill expects MUST appear in the ported SKILL.md's `## Compatibility` section.

| Server | Used by | Port action |
|---|---|---|
| Tavily | `sc:research` | Document in `skills/sc-research/SKILL.md` § Compatibility |
| Context7 | `sc:implement`, `sc:design`, `sc:document` | Document per skill |
| Sequential | (everywhere) | Document as universal dependency |
| Serena | `sc:pm`, `sc:save`, `sc:load`, `sc:research` | Skip (those commands skipped or document as optional) |
| Magic | `sc:implement`, `sc:brainstorm`, `sc:design` | Document per skill |
| Playwright | `sc:test`, `sc:implement`, `sc:research` | Document per skill |
| Morphllm | `sc:implement`, `sc:improve` | Document per skill |
| Chrome DevTools | perf | Document in `sc:analyze` |
| Airis-Agent | meta | **skip** |

No new MCP installer ships with Agency. The MCP integration is documentation-only.

### 2.5 SessionStart hook

SuperClaude ships a `SessionStart` hook (`hooks/hooks.json`) that auto-invokes `pm-agent` to restore Serena memory. **Skip the hook itself** — Agency's session bootstrap is `./install.sh` + `tools/check-governance.sh`, governed by AGENTS.md SS.1–SS.3. The pm-agent skill is ported, but it activates manually via `/sc:pm`, not via a hook injection that would conflict with Agency's bootstrap contract.

---

## 3. Superpowers inventory (canonical reference)

Upstream layout: `skills/`, `commands/`, `agents/`, `hooks/`, `.claude-plugin/`. Distribution: Claude Code plugin (`/plugin install superpowers@superpowers-marketplace`). Frontmatter shape: `name`, `description` only (very minimal). Skills auto-discover via SessionStart hook injection of `using-superpowers` content.

### 3.1 Skills (14)

| # | Slug | Purpose (one-line) | Port tier | Target |
|---|---|---|---|---|
| 1 | `brainstorming` | Socratic design refinement before implementation | **skip** (overlaps with `sc:brainstorm` — pick one, keep `sc:brainstorm`) | — |
| 2 | `writing-plans` | Detailed bite-sized implementation plans (2-5 min tasks) | **must** (aligns with Agency Task plan discipline) | `skills/superpowers-writing-plans/` |
| 3 | `executing-plans` | Batched execution with checkpoints | **must** | `skills/superpowers-executing-plans/` |
| 4 | `test-driven-development` | RED-GREEN-REFACTOR with anti-patterns ref | **must** (Agency uses Gherkin AC + pytest — TDD discipline is a perfect fit) | `skills/superpowers-test-driven-development/` |
| 5 | `systematic-debugging` | 4-phase RCA (condition-based-waiting, defense-in-depth, root-cause-tracing) | **must** (Agency has `root-cause-analyst` placeholder; this is the working version) | `skills/superpowers-systematic-debugging/` |
| 6 | `subagent-driven-development` | Fresh subagent per task, two-stage review | **must** (Agency encourages parallel Explore agents — this codifies it) | `skills/superpowers-subagent-driven-development/` |
| 7 | `using-git-worktrees` | Isolated dev branches via git worktrees | **nice** (Agency uses single-branch flow per `CLAUDE.md §11`; worktrees would be an addition) | `skills/superpowers-using-git-worktrees/` |
| 8 | `finishing-a-development-branch` | Verify/merge/PR/cleanup checklist | **nice** (overlaps with `sc:createPR` + Agency's Closing Run Procedure CR.1–CR.7) | `skills/superpowers-finishing-a-development-branch/` |
| 9 | `requesting-code-review` | Pre-review checklist + reviewer-agent prompt | **must** (Agency needs a structured review skill — currently nothing) | `skills/superpowers-requesting-code-review/` |
| 10 | `receiving-code-review` | Respond to review feedback systematically | **must** | `skills/superpowers-receiving-code-review/` |
| 11 | `verification-before-completion` | Ensure changes actually fix the problem | **must** (aligns with Agency's pre-commit gate philosophy) | `skills/superpowers-verification-before-completion/` |
| 12 | `dispatching-parallel-agents` | Coordinate concurrent subagents | **nice** | `skills/superpowers-dispatching-parallel-agents/` |
| 13 | `using-superpowers` | Skill system intro, priority ordering, red flags | **skip** (Agency has its own skill system per SKILLS.md; injecting this would conflict) | — |
| 14 | `writing-skills` | TDD for skill authoring (meta-skill, 22 KB body + 7 ref files) | **must** (Agency's `skill-creator` is Anthropic's stock mirror; this is Jesse Vincent's battle-tested version with `anthropic-best-practices.md` 45.8 KB ref + rationalisation tables + persuasion principles — strict upgrade) | `skills/superpowers-writing-skills/` |

**Must-have skills**: 9. **Nice-to-have**: 3. **Skip**: 2.

### 3.2 Commands (3)

| Command | Invoked skill | Port action |
|---|---|---|
| `/superpowers:brainstorm` | `superpowers:brainstorming` | **skip** (skill skipped) |
| `/superpowers:write-plan` | `superpowers:writing-plans` | **must** — port as the `Skill`-invocation shortcut alongside `skills/superpowers-writing-plans/SKILL.md` |
| `/superpowers:execute-plan` | `superpowers:executing-plans` | **must** — port as the `Skill`-invocation shortcut alongside `skills/superpowers-executing-plans/SKILL.md` |

Commands in Superpowers are thin wrappers around skills (`disable-model-invocation: true`). In Agency's model, the SKILL.md alone is sufficient — users invoke via the `Skill` tool. So **don't port the command files separately**; the skill body is the canonical artifact.

### 3.3 Agent

| Agent | Purpose | Port tier | Target |
|---|---|---|---|
| `code-reviewer` | Senior code reviewer; plan alignment + code quality | **must** (bundle inside `skills/superpowers-requesting-code-review/references/code-reviewer.md`) | inside skill `references/` |

### 3.4 SessionStart hook

Skip. Same reasoning as §2.5 — Agency's bootstrap is `./install.sh` + `tools/check-governance.sh`. The SessionStart context injection of `using-superpowers` content would conflict with the AGENTS.md mandatory first-read contract.

### 3.5 Notable patterns to absorb (already aligned with Agency)

- **Three-tier disclosure** (SessionStart intro → quick-ref → full body): Agency already has this in `SKILLS.md §7.3` (T1/T2/T3 ladder). The two systems align.
- **TDD-for-documentation**: `writing-skills` includes pressure-testing skills with subagents. Agency has `spec-skill` for normative spec authoring; combining the two gives Agency the only repo with *both* RFC 2119 spec authoring AND TDD-tested skill authoring. Worth a future ADR.
- **Rationalization-plugging discipline**: `test-driven-development` includes explicit loophole closure ("Write code before test? Delete it. Start over."). This pattern is *strictly* aligned with Agency's RFC 2119 polarity-inversion linter (`tools/check-rfc2119-polarity.py`). Port intact.

---

