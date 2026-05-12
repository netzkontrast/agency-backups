---
type: spec
status: active
slug: claude-md
summary: "Instructions for AI coding assistants (Claude Code, Sonnet, Opus, Haiku) operating in this repository. Routes to canonical governance specs and enumerates non-negotiable session rules."
created: 2026-05-07
updated: 2026-05-12
---

# CLAUDE.md — AI Assistant Instructions

This file is the AI-assistant entry point to the **`agency`** repository. It does **not** replace any governance spec — it routes you into them. The full normative authority lives in [AGENTS.md](./AGENTS.md) (every agent's first read), then the layer-specific specs ([TASK.md](./TASK.md), [PROMPT.md](./PROMPT.md), [RESEARCH.md](./RESEARCH.md), [SKILLS.md](./SKILLS.md), [FOLDERS.md](./FOLDERS.md), [PRE_COMMIT.md](./PRE_COMMIT.md), [FRUSTRATED.md](./FRUSTRATED.md), [MAINTENANCE.md](./MAINTENANCE.md), [`decisions/readme.md`](./decisions/readme.md)).

When CLAUDE.md and a root spec disagree, the root spec wins. Reconcile this file in the same commit that introduces the divergence.

---

## 1. What this repository is

`agency` is **not an application**. It is a governance and orchestration substrate for long-horizon work performed by AI agents. The repo enforces a four-way **separation of concerns** mechanically (linters, pre-commit hook) and socially (specs):

| Concept | Question | Directory | Spec |
|---|---|---|---|
| **Machine** — Task | *What should be done?* | [`/tasks/<NNN>-<slug>/`](./tasks) | [TASK.md](./TASK.md) |
| **Actor** — Prompt | *What is the agent told to do?* | [`/prompts/<slug>/`](./prompts) | [PROMPT.md](./PROMPT.md) |
| **Space** — Research | *What did running it produce?* | [`/research/<slug>/`](./research) | [RESEARCH.md](./RESEARCH.md) |
| **Capability** — Skill | *What does the agent know how to do?* | [`/skills/<slug>/`](./skills) | [SKILLS.md](./SKILLS.md) |

Crossing these boundaries is an anti-pattern the pre-commit hook catches: a Task MUST NOT inline a prompt; a Research workspace MUST NOT contain prompt drafts; follow-up questions discovered during research MUST be filed as new prompts under `/prompts/`, never appended to a closed research workspace.

The audit graph that links them flows through frontmatter only:

```
/tasks/<NNN>-<slug>/task.md
        │ task_uses_prompts ──► /prompts/<slug>/prompt.md
                                        │ executed by agent ──► /research/<slug>/output/SPEC.md
                                                                          │ open questions ──► /prompts/<new-slug>/
```

---

## 2. Mandatory session bootstrap

Every session, **before reading or writing any file**:

```bash
./install.sh                    # idempotent; installs PyYAML, jsonschema, pytest from tools/requirements.txt
tools/check-governance.sh       # MUST exit 0 before any other action
```

If `check-governance.sh` exits non-zero, stop and report errors to the user. Do not "work through" a failing governance gate. The script runs the full linter suite (`tools/fm/validate.py`, `tools/lint-structure.py`, `tools/lint-runlog.py`, `tools/adr/cli.py validate`, plus advisory polarity / assumption-log / narrative-ontology checks).

Install the pre-commit hook once per clone:

```bash
tools/install-hooks.sh          # equivalent to: git config core.hooksPath .githooks
```

The hook (`.githooks/pre-commit`) re-runs `tools/check-governance.sh` on every commit and blocks unless all errors are addressed or covered by an open Task (maintenance bypass via `tools/check-maintenance-bypass.py`).

Bootstrap rules ([AGENTS.md SS.1–SS.3](./AGENTS.md#session-setup)) are binding.

---

## 3. Layer routing — pick the right spec before writing

| Request shape | Read | Then write under |
|---|---|---|
| Coordinate work with a goal, plan, todo, ownership | [TASK.md](./TASK.md) | `/tasks/<NNN>-<slug>/task.md` |
| Author an executable instruction set for an agent | [PROMPT.md](./PROMPT.md) | `/prompts/<slug>/prompt.md` (+ `brief.md` + `readme.md` — three-file scaffold mandatory at creation, [FOLDERS.md §4.1](./FOLDERS.md)) |
| Execute a prompt and produce evidence/synthesis | [RESEARCH.md](./RESEARCH.md) | `/research/<slug>/{workspace,synthesis,reflection,output}/` |
| Author or modify a reusable agent capability | [SKILLS.md](./SKILLS.md) | `/skills/<slug>/SKILL.md` |
| Change a repo-architecture convention (paths, schemas, hooks, branching) | [`decisions/readme.md`](./decisions/readme.md) | `/decisions/<NNNN>-<slug>.md` (MADR 4.0.0) |

Bootstrap from a skeleton in [`/templates/`](./templates) (`task.md`, `prompt.md`, `research-readme.md`, `notes.md`, `readme.md`, `skill.md`).

---

## 4. Frontmatter is non-negotiable

Every Markdown file in operational directories MUST carry frontmatter. Schema is **Layered with Namespacing**, depth ≤ 1, kebab-case slugs:

- **L1 Vault Core (mandatory):** `type`, `status`, `slug`, `summary`, `created`, `updated`.
  - `type` ∈ `{task, prompt, research, spec, readme, note, index}`. Drives parser routing — read first.
  - `summary` is the **primary token-saving lever**. Read it before opening the body.
  - `updated` is ISO-8601; bump on every substantive change.
- **L2 Domain Namespace (mandatory inside its directory):** `task_*`, `prompt_*`, `research_*`, `skill_*`, `adr_*`. Full key matrix in [TASK.md §3](./TASK.md) and [SKILLS.md §3](./SKILLS.md).
- **L3 Agent-Only:** vector embeddings, graph scores — MUST NOT appear in YAML; lives in `/.agent_cache/<file>.meta.json`.

Cross-directory linkage flows through frontmatter only (`task_uses_prompts`, `task_spawns_research`, `prompt_relates_to_task`, `research_executes_prompt`, `skill_references_*`). Body Markdown links are for humans; the linker reads frontmatter.

Mutate frontmatter via `tools/fm/edit.py` (file-locked, body-byte-preserving, refuses T3/T4 ops) — not `sed`/`awk`.

---

## 5. Spec language — RFC 2119 + Gherkin

Every normative clause uses **uppercase RFC 2119 keywords** (`MUST`, `MUST NOT`, `SHOULD`, `MAY`, …). Lowercase prose is non-normative. One keyword per sentence.

Every acceptance criterion is a **Gherkin scenario** (`Feature: / Scenario: / Given / When / Then`), not a bullet list. Scenarios MUST be self-contained and executable. Anchor with `# anchor: <stable-id>` on the line above `Scenario:`.

Canonical definitions: [`maintenance/language-spec.md`](./maintenance/language-spec.md). Quick reference in [AGENTS.md "Spec Language Reference"](./AGENTS.md#spec-language-reference).

---

## 6. Pre-commit gate — what runs and when

`tools/check-governance.sh` is the unified entry point invoked by the hook. The flexible toolchain (`tools/fm/`) is the **canonical, gating** path; `tools/legacy/` runs advisory and is being retired.

| Step | Tool | Checks |
|---|---|---|
| 1 | `tools/fm/validate.py --type-check` | L1+L2 keys, type/path agreement, required headings, audit-graph linkage |
| 2 | `tools/lint-structure.py` | Required files present (`task.md`, `prompt.md`, `brief.md`, `readme.md` per folder) |
| 3 | (linkage folded into step 1) | — |
| 4 | `tools/lint-runlog.py` | `maintenance/run-log.md` records well-formed |
| 5 | `tools/adr/cli.py validate` | MADR fields + `adr_*` namespace + supersession DAG sanity |
| adv | `tools/check-rfc2119-polarity.py` | WARN-tier: `MUST`/`MUST NOT` polarity inversions |
| 6 | `tools/fm/index_diff.py` | `tasks/readme.md` index reflects current `task_status` |
| opt | `tools/dramatica-nav/{validate,cleanup}.py` | Narrative-ontology integrity (gated on `ontology.json` existing) |
| opt | `tools/check-assumption-log.py` | WARN-tier: every operational `readme.md` carries `## Assumptions Log` |
| opt | `tools/check-narrative-ontology-load.py` | WARN-tier: NO.5 — non-narrative tasks MUST NOT load narrative ontology |
| trust | `tools/check-trust.py` | Every `task_status: done` Task has a traceable FL declaration |

**Body-schema** (per-section shape, item counts, link patterns) check: `python3 tools/fm/validate.py --check-body`. **Strict mode** (promote WARN → fail): `--strict`. **Legacy fallback** (one-release deprecation): `FM_TOOLCHAIN=0 tools/check-governance.sh`. Detailed matrix: [PRE_COMMIT.md §7](./PRE_COMMIT.md#7-mechanical-governance-checks).

ADR governance: any change to repo-architecture conventions (storage paths, frontmatter schemas, hook integration) MUST go through [`/decisions/<NNNN>-<slug>.md`](./decisions/) per MADR 4.0.0. `Accepted` ADRs are **T4-immutable** — supersede via a successor ADR, never edit. The `<!-- BEGIN/END AGENCY-ADR SYNTHESIS -->` block in `AGENTS.md` is **agent-written** by `tools/adr/cli.py synthesize`; manual edits are overwritten.

---

## 7. The `readme.md` rule

EVERY operational folder MUST contain a `readme.md`. Update touched folders' readmes as a **single pre-commit step**, not on every file change (batching protects the context window).

Required content:
1. **What and Why** — what the folder is, why it exists in this location.
2. **Linked Navigation** — every file/subfolder via relative Markdown links.
3. **Assumptions Log** — `## Assumptions Log` heading; either substantive entries or the literal `(none)` line. Stale assumption-logs (older `updated:` than sibling `task.md`) WARN at pre-commit (`tools/check-assumption-log.py`).

`readme.md` files in operational folders SHOULD carry L1 Vault Core frontmatter (`type: index` is appropriate). [FOLDERS.md §3](./FOLDERS.md#3-the-readmemd-rule-decentralized-documentation).

---

## 8. Repair tiers — what you may fix in-place vs. file as a Task

[MAINTENANCE.md §1](./MAINTENANCE.md#1-repair-permission-tiers):

| Tier | Examples | Action |
|---|---|---|
| **T1 — Mechanical** | Missing/stale `updated:`, derivable `slug:`, broken relative link to existing target, missing `readme.md` stub | Fix in place via `tools/fm/edit.py` |
| **T2 — Additive** | Adding an unambiguous L1/L2 key (e.g. `type: task` to a `task.md`) | Fix in place via `tools/fm/edit.py --set` / `--append-list` |
| **T3 — Structural** | Section heading rewrites, schema changes, root-spec edits beyond T1/T2, slug renames | MUST file a Task; do not edit directly |
| **T4 — Research-touching (content)** | Any *content* change to a `research_phase: complete` workspace — body prose, synthesis findings, scenario outcomes | MUST NOT touch — research content is immutable after closure |

T1 / T2 metadata-and-link repairs on closed research are permitted
under the narrow allowance in [`MAINTENANCE.md §1.0.1`](./MAINTENANCE.md#101-closed-research-t1t2-repair-allowance-task-059):
`updated:` bumps and broken-relative-link fixes when an upstream
rename moved the target. Body content remains T4-immutable.

The `Accepted` state of an ADR is also T4-immutable; supersede via a new ADR.

---

## 9. Mandatory friction log every session

Every session ends with a Frustration Level declaration **FL0–FL3** ([FRUSTRATED.md](./FRUSTRATED.md)). The log is mandatory **even when nothing went wrong** — absence of a log is itself a defect.

- **Research runs:** `/research/<slug>/reflection/friction-log.md`, `Highest Frustration Level: FLn` at the top.
- **Standard tasks / general sessions:** `## Frustration Log` section in the PR body or commit message.

FL1+ entries feed the Nightly Maintenance Run, which converts recurring friction into Tasks — the repo improves itself only if you log honestly.

---

## 10. Closing run procedure (all platforms)

Every session — Claude Code, Jules, Gemini — MUST close with the four-step platform-agnostic checklist defined in [AGENTS.md "Closing Run Procedure"](./AGENTS.md#closing-run-procedure). The checklist is the contract; each platform implements step 4 (PR creation) via its own primitive.

1. **Friction log written + committed** (`friction-log.md` with `Highest Frustration Level: FL[0-3]`).
2. **`tasks/readme.md` index synced** with new `task_status` frontmatter.
3. **`tools/check-governance.sh` exits 0** on the final commit.
4. **Open a draft PR** via the platform's primitive (Claude Code: `/sc:createPR`; Jules: native GitHub primitive; Gemini: deferred to integration-Task agent). The PR body MUST cite (a) closed Task slug(s) and (b) the FL declaration.

Notes that apply to all platforms:
- Step 4 is idempotent — re-invocation on a branch with an open PR is a no-op; pushing additional commits updates the open PR. **Do not** create duplicate PRs.
- If pre-commit failed or was skipped, do NOT advance past step 3. Report diagnostics to the user and leave the session `in_progress`.
- If the platform's PR primitive errors, do not silently exit — surface the exact output.

Rules CR.1–CR.7 in [AGENTS.md § Closing Run Procedure](./AGENTS.md#closing-run-procedure) are the binding statement; this section is a one-paragraph routing pointer.

---

## 11. Branch & commit conventions

- Develop on the assigned feature branch (e.g. `claude/<slug>-<id>`); never push directly to `main`.
- `git push -u origin <branch>`; on network errors retry up to 4× with exponential backoff (2s, 4s, 8s, 16s). Do not retry on non-network failures.
- Prefer **new commits** over `--amend`; if a hook fails, the commit did not happen, so amending would mutate the previous commit. Fix, re-stage, new commit.
- NEVER use `--no-verify`, `--no-gpg-sign`, force-push to `main`/`master`, or update `git config` without explicit user instruction.
- Stage by name (`git add path/to/file`); avoid `git add .` / `-A` (risks committing `.env`, large binaries).
- Do NOT create a pull request unless explicitly asked. Use the GitHub MCP server tools (`mcp__github__*`) — `gh` CLI is not available. Repository scope is restricted to `netzkontrast/agency`.

---

## 12. Top-level topology (what each folder is)

```
agency/
├── README.md, AGENTS.md, TASK.md, PROMPT.md, RESEARCH.md,
│   FOLDERS.md, PRE_COMMIT.md, FRUSTRATED.md, MAINTENANCE.md,
│   SKILLS.md            # Root governance specs (T1/T2 repairs only).
├── CLAUDE.md             # This file — AI-assistant entry point.
├── install.sh            # Session bootstrap (idempotent).
│
├── tasks/                # Operational: <NNN>-<slug>/task.md (orchestration).
├── prompts/              # Operational: <slug>/{prompt.md,brief.md,readme.md} (instruction).
├── research/             # Operational: <slug>/{workspace,synthesis,reflection,output} (evidence).
│
├── tools/                # Linters, fm-toolchain, ADR CLI, dramatica-nav.
│   ├── fm/               #   Canonical frontmatter toolchain (Python 3.11 stdlib only).
│   ├── adr/              #   ADR validate / synthesize / compress / graph.
│   ├── legacy/           #   One-release deprecation shims (advisory).
│   └── tests/            #   pytest suites for fm/, adr/, lints.
├── templates/            # Skeletons agents copy when bootstrapping new artifacts.
├── maintenance/          # language-spec.md + run-log.md + narrative-ontology schemas.
├── skills/               # Version-controlled mirror of Claude skills (SKILL.md + assets).
├── decisions/            # Append-only ADR ledger (MADR 4.0.0). Accepted ADRs are T4.
├── Agency-System/        # Frontend prototype for the Agency System triptychon (HTML/JSX/SVG).
└── .githooks/            # pre-commit → tools/check-governance.sh.
```

Adding a new top-level folder that is neither operational ([FOLDERS.md §1](./FOLDERS.md)) nor explicitly exempted ([FOLDERS.md §8](./FOLDERS.md)) is itself an anti-pattern.

---

## 13. Skills, Skills SDK, and the SuperClaude `/sc:*` commands

Invoke skills via the **Skill** tool only when the user types `/<skill>` or the system reminder lists the skill as available — never guess names. `/sc:createPR` is the canonical Claude Code session-closer (§10). The full skill corpus is mirrored under [`skills/`](./skills/) (SHA-pinned per [ADR-0011](./decisions/0011-external-skill-corpora-import.md)); 54 imported skills are auto-discovered when `.claude/skills/` is materialised (Task 094 ST-2 surface).

The imported corpus is grouped by `skill_kind` (the 9-value enum ratified in [SKILLS.md §3](./SKILLS.md#3-frontmatter-namespace)). Use the per-spec audit anchors below to navigate from a category to its skills.

This section partitions by **source** (SuperClaude vs. Superpowers) and counts categories within each source. AGENTS.md's "Skill Index by Category" partitions by **`skill_kind` across both sources**, so its counts differ — e.g. orchestrator is **9** here (sc-* only) but **12** in AGENTS.md (9 sc-* + 3 superpowers-*). Both partitions cite the same 54 skills; pick whichever axis matches the lookup.

<!-- anchor: SK.13.SUPERCLAUDE -->
### 13.1 SuperClaude (`sc-*`) — 39 skills (`skill_source: superclaude@v4.3.0`)

- **orchestrator (9):** [`sc-brainstorm`](./skills/sc-brainstorm/SKILL.md), [`sc-design`](./skills/sc-design/SKILL.md), [`sc-implement`](./skills/sc-implement/SKILL.md), [`sc-improve`](./skills/sc-improve/SKILL.md), [`sc-load`](./skills/sc-load/SKILL.md), [`sc-research`](./skills/sc-research/SKILL.md), [`sc-save`](./skills/sc-save/SKILL.md), [`sc-task`](./skills/sc-task/SKILL.md), [`sc-workflow`](./skills/sc-workflow/SKILL.md).
- **domain (8):** [`sc-backend-architect`](./skills/sc-backend-architect/SKILL.md), [`sc-deep-research-agent`](./skills/sc-deep-research-agent/SKILL.md), [`sc-frontend-architect`](./skills/sc-frontend-architect/SKILL.md), [`sc-performance-engineer`](./skills/sc-performance-engineer/SKILL.md), [`sc-quality-engineer`](./skills/sc-quality-engineer/SKILL.md), [`sc-refactoring-expert`](./skills/sc-refactoring-expert/SKILL.md), [`sc-security-engineer`](./skills/sc-security-engineer/SKILL.md), [`sc-system-architect`](./skills/sc-system-architect/SKILL.md).
- **analysis (7):** [`sc-analyze`](./skills/sc-analyze/SKILL.md), [`sc-business-panel`](./skills/sc-business-panel/SKILL.md), [`sc-estimate`](./skills/sc-estimate/SKILL.md), [`sc-explain`](./skills/sc-explain/SKILL.md), [`sc-reflect`](./skills/sc-reflect/SKILL.md), [`sc-spec-panel`](./skills/sc-spec-panel/SKILL.md), [`sc-troubleshoot`](./skills/sc-troubleshoot/SKILL.md).
- **persona (7):** [`sc-devops-architect`](./skills/sc-devops-architect/SKILL.md), [`sc-learning-guide`](./skills/sc-learning-guide/SKILL.md), [`sc-python-expert`](./skills/sc-python-expert/SKILL.md), [`sc-requirements-analyst`](./skills/sc-requirements-analyst/SKILL.md), [`sc-root-cause-analyst`](./skills/sc-root-cause-analyst/SKILL.md), [`sc-self-review`](./skills/sc-self-review/SKILL.md), [`sc-socratic-mentor`](./skills/sc-socratic-mentor/SKILL.md).
- **tool (7):** [`sc-build`](./skills/sc-build/SKILL.md), [`sc-cleanup`](./skills/sc-cleanup/SKILL.md), [`sc-confidence-check`](./skills/sc-confidence-check/SKILL.md), [`sc-createPR`](./skills/sc-createPR/SKILL.md), [`sc-document`](./skills/sc-document/SKILL.md), [`sc-index`](./skills/sc-index/SKILL.md), [`sc-test`](./skills/sc-test/SKILL.md).
- **meta (1):** [`sc-pm-agent`](./skills/sc-pm-agent/SKILL.md) — orchestrates the rest of the `sc-*` surface via `/sc:pm` only (inert at SessionStart per [ADR-0011 D.7](./decisions/0011-external-skill-corpora-import.md)).

<!-- anchor: SK.13.SUPERPOWERS -->
### 13.2 Superpowers (`superpowers-*`) — 15 skills (`skill_source: superpowers@v4.0.3`)

- **discipline (8):** [`superpowers-brainstorming`](./skills/superpowers-brainstorming/SKILL.md), [`superpowers-executing-plans`](./skills/superpowers-executing-plans/SKILL.md), [`superpowers-finishing-a-branch`](./skills/superpowers-finishing-a-branch/SKILL.md), [`superpowers-receiving-code-review`](./skills/superpowers-receiving-code-review/SKILL.md), [`superpowers-systematic-debugging`](./skills/superpowers-systematic-debugging/SKILL.md), [`superpowers-tdd`](./skills/superpowers-tdd/SKILL.md), [`superpowers-verification-before-completion`](./skills/superpowers-verification-before-completion/SKILL.md), [`superpowers-writing-plans`](./skills/superpowers-writing-plans/SKILL.md).
- **orchestrator (3):** [`superpowers-dispatching-parallel-agents`](./skills/superpowers-dispatching-parallel-agents/SKILL.md), [`superpowers-requesting-code-review`](./skills/superpowers-requesting-code-review/SKILL.md), [`superpowers-subagent-driven-development`](./skills/superpowers-subagent-driven-development/SKILL.md).
- **meta (2):** [`superpowers-using-superpowers`](./skills/superpowers-using-superpowers/SKILL.md) (D.7-stripped — discipline-gate selector only; SessionStart injection prohibited), [`superpowers-writing-skills`](./skills/superpowers-writing-skills/SKILL.md).
- **agent-template (1):** [`superpowers-code-reviewer`](./skills/superpowers-code-reviewer/SKILL.md) — subagent prompt for Agency's built-in `code-reviewer` agent type.
- **workflow (1):** [`superpowers-using-git-worktrees`](./skills/superpowers-using-git-worktrees/SKILL.md).

For narrative-ontology work (Dramatica / NCP / novel-architect), prefer `tools/dramatica-nav/nav.py` over loading `maintenance/schemas/narrative-ontology/ontology.json` directly. Non-narrative tasks MUST NOT load the ontology files (NO.5 in [AGENTS.md](./AGENTS.md#narrative-ontology--dramatica--ncp--novel-architect-bridge); WARN-enforced by `tools/check-narrative-ontology-load.py`).

---

## 14. Quick non-negotiables

1. Run `./install.sh` and `tools/check-governance.sh` **before** reading or writing any file.
2. Read AGENTS.md before doing anything else.
3. Pick the right layer (Task / Prompt / Research / Skill / ADR) **before** creating files.
4. Add L1 + L2 frontmatter to every operational file. YAML depth ≤ 1.
5. Update touched folders' `readme.md` at pre-commit time, not per-file.
6. Mutate frontmatter via `tools/fm/edit.py`, not `sed`/`awk`.
7. Write acceptance criteria as Gherkin, not bullet lists. Use uppercase RFC 2119 keywords.
8. Do not edit `<!-- BEGIN/END AGENCY-ADR SYNTHESIS -->` blocks by hand.
9. Do not push to `main`, force-push, skip hooks, or use `--no-verify`.
10. End every session with an FL declaration. FL0 inclusive.
11. Close every session with the four-step checklist in [AGENTS.md § Closing Run Procedure](./AGENTS.md#closing-run-procedure). Claude Code implements step 4 via `/sc:createPR`. Cite Task slug(s) + FL.
12. When in doubt, the root spec wins over this file.

---

*Authority for everything above lives in [AGENTS.md](./AGENTS.md) and the layer-specific specs. This file MUST stay consistent with them; reconcile in the same commit when they change.*
