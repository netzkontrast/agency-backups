# agency

**Decoupling Machine, Actor, and Space for Long-Horizon AI Agency.**

`agency` is a governance and orchestration repository for long-horizon work performed by AI agents (Claude Code, Gemini, Jules, and humans). It is **not** an application. It is the *substrate* on which agentic work is planned, instructed, executed, audited, and continuously improved — engineered so that work done across many sessions, by many agents, in many contexts, stays coherent.

---

## 1. Why this repository exists

LLM agents lose coherence over long horizons. They forget intent, drift from prior decisions, blur the line between *what should be done*, *what the agent was told to do*, and *what running it produced*. They re-author prompts mid-research, inline instructions inside tasks, append follow-up questions to closed deliverables, and silently re-interpret governance.

This repository is an opinionated answer to that drift. It treats agentic work as a system with three intentionally **decoupled** concerns:

| Concept | Question it answers | Lives in |
|---|---|---|
| **Machine** — the *Task* | *What should be done?* (orchestration, plan, todo, ownership) | [`/tasks/`](./tasks) |
| **Actor** — the *Prompt* | *What is the agent told to do?* (executable instruction set) | [`/prompts/`](./prompts) |
| **Space** — the *Research* | *What did running it produce?* (evidence, synthesis, output) | [`/research/`](./research) |

> **Pending reframe.** [FOLDERS.md §1](./FOLDERS.md) and [AGENTS.md Task Type Routing](./AGENTS.md) now also list `/skills/` (Capability — *what the agent knows how to do*, governed by [SKILLS.md](./SKILLS.md)) as a peer concern. Reframing §1 and §3 of this README to a four-concern model is gated on R.13 / R.14 and is being done in [Task 045](./tasks/045-readme-coherence-refresh/). Until that Task lands, the operational guidance in `/skills/` is consulted via [SKILLS.md](./SKILLS.md) directly.

The decoupling is enforced both socially (via specs) and mechanically (via linters and a pre-commit hook). A Task MUST NOT inline a prompt. Research MUST NOT author its own instructions. Follow-up questions MUST NOT be appended to a closed research workspace — they MUST be filed as new prompts. The audit graph that links the three is the source of truth.

```text
/tasks/<NNN>-<slug>/task.md
        │ task_uses_prompts ──► /prompts/<slug>/prompt.md
                                        │ executed by agent ──► /research/<slug>/output/SPEC.md
                                                                          │ open questions ──► /prompts/<new-slug>/  (prompt_kind: follow-up)
```

---

## 2. Who this repository is for

- **Human operators** who want a repeatable way to run multi-session research and engineering campaigns with AI agents and end up with an *auditable artifact graph*, not a pile of prose.
- **AI agents** (Claude Code, Gemini, Jules) who need a deterministic place to land when asked "do something useful here". The repo's root specs route every request to the correct directory before the agent writes a single byte.
- **Researchers and prompt engineers** experimenting with long-horizon agency, frontmatter ontologies, friction logging, and spec-driven research workflows.

You do not need to install or run anything to read this repository — most of the value is in the specs and the artifacts they govern. To *commit* changes you need Python 3 (with `PyYAML`, `jsonschema`, `pytest`) and the pre-commit hook installed; the canonical session bootstrap is `./install.sh` followed by `tools/check-governance.sh` (see [§9 Quick start](#9-quick-start-for-humans) and [AGENTS.md "Session Setup"](./AGENTS.md)).

---

## 3. The mental model: Machine / Actor / Space

The slogan **"Decoupling Machine, Actor, and Space"** is a design constraint, not branding. Each layer has its own filesystem home, its own governance spec, its own frontmatter namespace, and its own pre-commit checks. Crossing the boundaries is an anti-pattern that the linters catch.

### 3.1 Machine — `/tasks/` (orchestration)

A **Task** is a bounded, named unit of coordination work. It carries a Goal, a Plan, a Todo checklist, and explicit links to the prompts it executes and the research it spawns. Tasks live in `/tasks/<NNN>-<slug>/task.md` and are governed by [TASK.md](./TASK.md).

A Task is *not* an instruction set. It says *what should happen*; it links to a Prompt that says *how*.

### 3.2 Actor — `/prompts/` (instruction)

A **Prompt** is a self-contained, executable instruction set written for a specific agent. Prompts live in `/prompts/<slug>/prompt.md` alongside an immutable `brief.md` capturing the original user request. Prompts are governed by [PROMPT.md](./PROMPT.md) and MUST satisfy seven engineering principles (self-containedness, framework declaration, RFC 2119 normativity, deliverable lock, anti-ambiguity, constraint isolation, failure handling).

A Prompt is *not* a Task. It does not coordinate; it instructs.

### 3.3 Space — `/research/` (execution)

A **Research workspace** is what running a Prompt produced. It contains a workspace folder for scratch work, a synthesis folder for structured outputs, a reflection folder for critical-thinking artifacts and the friction log, and an output folder for the final deliverable. Research is governed by [RESEARCH.md](./RESEARCH.md).

A Research workspace is read-mostly once `research_phase: complete`. Open questions discovered during a run are routed *outward* into new prompts under `/prompts/`, never back into the closed workspace.

---

## 4. Repository topology

```text
agency/
├── README.md            # You are here.
├── AGENTS.md            # Entry-point spec every agent reads first.
├── TASK.md              # Governs /tasks/ — orchestration.
├── PROMPT.md            # Governs /prompts/ — instruction sets.
├── RESEARCH.md          # Governs /research/ — execution workspaces.
├── FOLDERS.md           # Folder topology, naming, readme.md rule, audit graph.
├── PRE_COMMIT.md        # Mandatory pre-commit checklist for every agent.
├── FRUSTRATED.md        # FL0–FL3 friction logging spec (mandatory every session).
├── MAINTENANCE.md       # Nightly maintenance + Repo Coherence Check protocol.
├── SKILLS.md            # Governs /skills/ — skill_* namespace, lifecycle, bootstrap protocol.
├── LICENSE
├── install.sh           # Session bootstrap. Installs tools/requirements.txt; idempotent.
│
├── tasks/               # Operational: Task orchestration folders <NNN>-<slug>/
├── prompts/             # Operational: Prompt instruction folders <slug>/
├── research/            # Operational: Research execution workspaces <slug>/
│
├── tools/               # Linters, ADR CLI, frontmatter toolchain, pre-commit shim.
├── templates/           # Frontmatter and folder skeletons agents copy when bootstrapping.
├── maintenance/         # Canonical language spec + structured run-log of every coherence check.
├── skills/              # Version-controlled mirror of Claude skills (SKILL.md + assets).
├── decisions/           # Append-only ADR ledger (MADR 4.0.0) — the only mechanism for repo-architecture changes.
├── Agency-System/       # Frontend prototype for the Agency System triptychon (HTML/JSX/SVG). See FOLDERS.md §8.
└── .githooks/           # Pre-commit hook that invokes tools/check-governance.sh.
```

The three **operational** directories (`/tasks/`, `/prompts/`, `/research/`) are the only places where coordination, instruction, and evidence may live. The **non-operational** directories enumerated in [FOLDERS.md §8](./FOLDERS.md) (`/tools/`, `/templates/`, `/maintenance/`, `/skills/`, `/decisions/`, `/Agency-System/`) are explicit exemptions. Adding a new top-level folder that is neither operational nor exempt is itself an anti-pattern. The pytest suites for `/tools/adr/` and `/tools/fm/` live under [`/tools/tests/`](./tools/tests/) and are exempt-by-inheritance via the `/tools/` row in [FOLDERS.md §8](./FOLDERS.md).

---

## 5. The shared spec language

Every governance file in this repository speaks the same formal dialect so humans and agents can read each other unambiguously. The canonical definitions live in [`maintenance/language-spec.md`](./maintenance/language-spec.md). The summary:

- **RFC 2119 keywords** (MUST, MUST NOT, SHOULD, SHOULD NOT, MAY, REQUIRED, RECOMMENDED, OPTIONAL) carry their normative meaning *only* when written in ALL CAPS. Lowercase prose is non-normative.
- **Gherkin** (`Feature:`, `Scenario:`, `Given/When/Then`, `And/But`) is used for every behavioural example and acceptance criterion. Bullet-list assertions are not acceptance criteria.
- **Frontmatter Ontology** is a Layered Schema with Namespacing — L0 (Obsidian reserved) + L1 (Vault Core: `type`, `status`, `slug`, `summary`, `created`, `updated`) + L2 domain namespaces (`task_*`, `prompt_*`, `research_*`, `skill_*`, `adr_*`) + L3 (sidecar agent metadata, never in YAML). YAML MUST NOT nest beyond one level. The `skill_*` namespace is defined in [SKILLS.md §3.3](./SKILLS.md); the `adr_*` namespace is defined in `research/adr-spec-research-synthesis/output/SPEC.md` and consumed by [`tools/adr/cli.py`](./tools/adr/cli.py).

The `summary` field is the most important token-saving lever in the repo — agents are expected to read it before opening a file's body.

---

## 6. The pre-commit gate (mechanical enforcement)

The repository self-defends against drift via a pre-commit hook that runs the linters below before any commit touching `/tasks/`, `/prompts/`, `/research/`, or `/skills/`. The unified entry point is `tools/check-governance.sh`; the hook calls it directly.

| Linter | Checks |
|---|---|
| [`tools/validate-frontmatter.py`](./tools/validate-frontmatter.py) | L1 + L2 keys present, YAML depth ≤ 1, slug is kebab-case, slug matches folder name. |
| [`tools/lint-structure.py`](./tools/lint-structure.py) | Required files exist (`task.md`, `prompt.md`, `brief.md`, `readme.md` per folder). |
| [`tools/lint-linkage.py`](./tools/lint-linkage.py) | Audit-graph edges resolve: `task_uses_prompts`, `task_spawns_research`, `prompt_relates_to_task`, `prompt_spawned_from_research`, `research_executes_prompt`, `skill_references_*`. Reciprocity is enforced. |
| [`tools/check-trust.py`](./tools/check-trust.py) | A friction log with a traceable FL declaration exists when a Task closes. |
| [`tools/check-maintenance-bypass.py`](./tools/check-maintenance-bypass.py) | Nightly-maintenance commits cannot bypass the standard governance gates. |
| [`tools/lint-runlog.py`](./tools/lint-runlog.py) | The maintenance run-log under `/maintenance/` carries valid structured entries. |
| [`tools/adr/cli.py`](./tools/adr/cli.py) | ADR validation (`validate`) and AGENTS.md guarded-section synthesis (`synthesize`) for `/decisions/` per [§6.2 ADR change-control](#62-adr-change-control). |
| [`tools/check-prompt-self-containedness.py`](./tools/check-prompt-self-containedness.py) | WARN-tier (Task 034 ST-2). Detects external-context phrases in `/prompts/<slug>/prompt.md` per [PROMPT.md §6.4](./PROMPT.md). |
| [`tools/check-prompt-framework-declaration.py`](./tools/check-prompt-framework-declaration.py) | WARN-tier (Task 034 ST-3). Verifies `prompt_framework` ∈ canonical set + `## Framework` section consistency + ≥10-word rationale per [PROMPT.md §6.4.b](./PROMPT.md). |

A failing linter MUST be fixed (or waived in `tools/.frontmatter-waivers` with a documented rationale) before the commit can proceed.

### 6.1 Flexible toolchain (Task 016)

A successor toolchain ships in [`tools/fm/`](./tools/fm/) per [`research/flexible-frontmatter-toolchain/output/SPEC.md`](./research/flexible-frontmatter-toolchain/output/SPEC.md). Four single-file CLIs, Python 3.11 stdlib only, no runtime dependencies:

| Tool | Surface |
|---|---|
| [`tools/fm/validate.py`](./tools/fm/validate.py) | Required-only frontmatter + heading checks (§3, §4); opt-in body-schema check (`--check-body`, §12) for per-section shape, item-count, link-pattern, RFC-2119-keyword constraints. |
| [`tools/fm/extract.py`](./tools/fm/extract.py) | Read one section, the frontmatter, a single FM key, the whole body, the H2 table-of-contents, batch-read multiple sections, or any nth-occurrence/all-occurrences of a duplicate-named section. |
| [`tools/fm/edit.py`](./tools/fm/edit.py) | Frontmatter-only mutations: `--set`/`--unset`/`--append-list`/`--remove-from-list`/`--bump-updated`. OS file lock; preserves body bytes; preserves scalar quoting style; refuses T3/T4 operations. |
| [`tools/fm/query.py`](./tools/fm/query.py) | Stateless filesystem query: `type=`/`status=`/`slug=`/`has-key=`/`missing-key=`/`refers-to=`/`referenced-by=`/`stale-since=`. No persisted index. |

Activated via `FM_TOOLCHAIN=1 tools/check-governance.sh`; the legacy linters remain the default gate until [Task 019](./tasks/019-fm-toolchain-suite-integration/) flips it.

Install once per clone:

```bash
tools/install-hooks.sh
# or, equivalently:
git config core.hooksPath .githooks
```

### 6.2 ADR change-control (`/decisions/`)

Repo-level architectural conventions (storage paths, frontmatter schemas, hook integration, branching) are changed *only* through Architectural Decision Records authored under [`/decisions/`](./decisions). Each ADR is a [MADR 4.0.0](https://adr.github.io/madr/) record (`<NNNN>-<slug>.md`) carrying `type: adr` plus the `adr_*` L2 namespace (`adr_id`, `adr_status`, `adr_supersedes`, …).

| Stage | What happens |
|---|---|
| **Author** | `decisions/<NNNN>-<slug>.md` written from the canonical MADR sections. `python3 tools/adr/cli.py validate` MUST pass before commit. |
| **Lifecycle** | `Proposed → Accepted → Superseded`/`Deprecated`. An `Accepted` ADR is **T4-immutable** per [MAINTENANCE.md §1](./MAINTENANCE.md#1-repair-permission-tiers); changes land via a successor ADR that names the predecessor in `adr_supersedes`. |
| **Synthesis** | When status flips to `Accepted`, `python3 tools/adr/cli.py synthesize` rewrites the byte-exact guarded block in [AGENTS.md](./AGENTS.md) (`<!-- BEGIN AGENCY-ADR SYNTHESIS -->` … `<!-- END AGENCY-ADR SYNTHESIS -->`). Manual edits inside that block MUST NOT be made — they are overwritten on the next synthesis run. |

Authoring guidance lives in [`decisions/readme.md`](./decisions/readme.md). The governance contract lives in [`research/adr-spec-research-synthesis/output/SPEC.md`](./research/adr-spec-research-synthesis/output/SPEC.md).

---

## 7. The friction log (mandatory every session)

Every agent session MUST end with a Frustration Level declaration in the range **FL0** (zero friction) to **FL3** (task blocker), per [FRUSTRATED.md](./FRUSTRATED.md). The log is mandatory even when nothing went wrong — the absence of a log is itself a defect. For research runs the log lives in `/research/<slug>/reflection/friction-log.md`; for standard tasks it lives in the PR body or commit message under a `## Frustration Log` heading.

The friction log is what feeds the **Nightly Maintenance Run** ([MAINTENANCE.md](./MAINTENANCE.md)): aggregated FL1+ entries become Tasks for future agents, so the repository improves itself over time rather than rotting.

---

## 8. The Closing Run procedure (Claude Code only)

Claude Code sessions MUST close with `/sc:createPR` after a successful `git push`. The PR body cites the closed Task slug(s) and the FL declaration. The rule is binding (see [AGENTS.md § Closing Run Procedure](./AGENTS.md#closing-run-procedure-claude-code)). Other agents (Jules, Gemini) follow their own platform conventions.

`/sc:createPR` is provided by the SuperClaude Framework — its source lives at [`src/superclaude/commands/createPR.md`](https://github.com/netzkontrast/SuperClaude_Framework/blob/main/src/superclaude/commands/createPR.md) and is installed alongside the rest of the `/sc:*` command set. The skill re-runs `tools/check-governance.sh` before opening a PR; pre-commit failures gate PR creation.

---

## 9. Quick start for humans

1. **Bootstrap the session.** From the repo root, run `./install.sh` (installs [`tools/requirements.txt`](./tools/requirements.txt) — `PyYAML`, `jsonschema`, `pytest`; idempotent), then `tools/check-governance.sh`. Both MUST exit 0 before any other action — see [AGENTS.md "Session Setup"](./AGENTS.md) (SS.1, SS.2).
2. **Read first, write second.** Open [AGENTS.md](./AGENTS.md). It is the entry-point spec for every agent (and a fine briefing for humans). It routes every request to the correct directory.
3. **Decide the layer.** Coordination → Task ([TASK.md](./TASK.md)). Instruction authoring → Prompt ([PROMPT.md](./PROMPT.md)). Evidence gathering → Research ([RESEARCH.md](./RESEARCH.md)). Reusable capability → Skill ([SKILLS.md](./SKILLS.md)). Architectural change → ADR ([`decisions/readme.md`](./decisions/readme.md)).
4. **Bootstrap from a template.** Copy the matching skeleton from [`/templates/`](./templates) (`task.md`, `prompt.md`, `research-readme.md`, `notes.md`, `readme.md`, `skill.md`).
5. **Install the hook once.** `tools/install-hooks.sh`.
6. **Work in the right folder.** Operational artifacts live in `/tasks/`, `/prompts/`, `/research/`. Adjacent docs (`readme.md`) update at pre-commit time, not on every file change.
7. **Run the gate before committing.** `tools/check-governance.sh`.
8. **Log friction.** Always. FL0 inclusive.

---

## 10. Reference index of root specs

| Spec | Governs | Read it before… |
|---|---|---|
| [AGENTS.md](./AGENTS.md) | Entry-point routing, spec language, frontmatter, closing run procedure. | …doing anything in this repo. |
| [TASK.md](./TASK.md) | `/tasks/` — orchestration, lifecycle, Task frontmatter. | …creating a `task.md`. |
| [PROMPT.md](./PROMPT.md) | `/prompts/` — instruction-set authoring, prompt engineering principles. | …writing a `prompt.md`. |
| [RESEARCH.md](./RESEARCH.md) | `/research/` — execution workspaces, synthesis, reflection, output. | …executing a research run. |
| [FOLDERS.md](./FOLDERS.md) | Folder topology, slug rules, the `readme.md` rule, the audit graph. | …creating any new folder. |
| [PRE_COMMIT.md](./PRE_COMMIT.md) | Mandatory pre-commit checklist. | …every commit. |
| [FRUSTRATED.md](./FRUSTRATED.md) | FL0–FL3 friction logging. | …closing every session. |
| [MAINTENANCE.md](./MAINTENANCE.md) | Nightly maintenance + Repo Coherence Check. | …running self-improvement passes. |
| [SKILLS.md](./SKILLS.md) | `/skills/` — skill capability spec, `skill_*` namespace, lifecycle, bootstrap protocol. | …authoring or modifying any skill. |
| [`decisions/readme.md`](./decisions/readme.md) | `/decisions/` — ADR ledger (MADR 4.0.0), `adr_*` namespace, T4-immutability, synthesis pipeline. | …changing any repo-architecture convention. |
| [`maintenance/language-spec.md`](./maintenance/language-spec.md) | Canonical RFC 2119 + Gherkin + frontmatter ontology. | …writing any normative clause. |

---

## 11. Spec — How this README MUST be updated

This section is the *binding governance for this very file*. It is intentionally written in the same dialect as every other root spec so it can be enforced and audited like the rest.

```yaml
---
type: spec
status: active
slug: readme-update-spec
scope: README.md (repository root, this file only)
created: 2026-05-04
updated: 2026-05-07
---
```

### 11.1 RFC 2119 declaration

The keywords **MUST**, **MUST NOT**, **SHOULD**, **SHOULD NOT**, and **MAY** in this section are to be interpreted per RFC 2119 / RFC 8174 when, and only when, written in ALL CAPS.

### 11.2 Authority and scope

- **R.1** This README is the **human-facing entry point** to the repository. It MUST remain readable by a non-agent reader who has never seen this repository before.
- **R.2** This README MUST NOT duplicate the normative content of root specs (`AGENTS.md`, `TASK.md`, `PROMPT.md`, `RESEARCH.md`, `FOLDERS.md`, `PRE_COMMIT.md`, `FRUSTRATED.md`, `MAINTENANCE.md`, `SKILLS.md`). It MUST link to them. When a normative clause changes in a root spec, this README MUST be updated to remain *consistent with* that spec, not to *re-state* it.
- **R.3** The classification "Machine / Actor / Space" in §1 and §3 is the canonical human-readable framing of the three operational directories. If the framing is renamed, every reference to it in this README MUST be updated in the same commit.

### 11.3 Update triggers (when this README MUST change)

This README MUST be updated in the same commit that introduces any of the following changes:

- **R.4** A root governance spec at the repository root is added, removed, renamed, or its `summary` frontmatter materially changes. The Reference Index in §10 MUST reflect the new state.
- **R.5** A new top-level directory is added or an existing one is removed. The topology tree in §4 MUST be updated, and the new directory's exemption status MUST be reconciled with [FOLDERS.md §8](./FOLDERS.md).
- **R.6** A new operational namespace (a new L2 frontmatter family beyond `task_*`, `prompt_*`, `research_*`) is introduced. §5 MUST mention it and link to its definition.
- **R.7** A new linter or pre-commit check is added to `/tools/`, or an existing one is removed or renamed. The table in §6 MUST be updated.
- **R.8** The Frustration Level scale in [FRUSTRATED.md](./FRUSTRATED.md) gains, loses, or renames a level. §7 MUST reflect the new scale.
- **R.9** The Closing Run procedure in [AGENTS.md](./AGENTS.md) changes which slash-command closes a session, or which agents the rule binds. §8 MUST reflect the change.
- **R.10** A normative rule in this `## 11. Spec` section is added, removed, or modified. The rule's identifier (R.x) MUST remain stable across edits — renumbering existing rules is forbidden because cross-references would silently rot. New rules append at the next free identifier.

### 11.4 Update procedure (how to change this README)

- **R.11** Edits to this README that fall under R.4–R.10 above MUST be made in the **same commit** as the change that triggered them. A commit that introduces a new linter without updating §6, or a new root spec without updating §10, MUST be rejected at review.
- **R.12** Edits that are purely cosmetic (typo fixes, prose clarity, link formatting) MAY be made in a standalone commit.
- **R.13** A non-trivial restructure of this README (adding or removing a top-level numbered section) MUST be performed via a Task in `/tasks/<NNN>-<slug>/` per [TASK.md](./TASK.md). It MUST NOT be performed inline as a "drive-by" edit during another Task. The Task's `task_affects_paths` MUST list `README.md`.
- **R.14** Edits that change the meaning of the Machine/Actor/Space framing (R.3) are **T3 Structural** changes per [MAINTENANCE.md §1](./MAINTENANCE.md#1-repair-permission-tiers). A maintenance agent MUST NOT make such edits directly; it MUST file a Task instead.
- **R.15** Every commit that modifies this README MUST update the `updated:` field of any frontmatter blocks contained in this section to today's ISO-8601 date. (At time of writing this section carries the inline frontmatter in §11 above.)
- **R.16** This README does not require a `friction-log.md` of its own, but every session that edits it MUST still produce a session-level FL declaration per [FRUSTRATED.md](./FRUSTRATED.md).

### 11.5 Acceptance criteria

```gherkin
Feature: README stays consistent with root specs

  # anchor: RM.1.1
  Scenario: A new root spec is added
    Given a new file <NEWSPEC>.md is created at the repository root
    And it is governance-bearing (carries "type: spec" frontmatter)
    When the commit that adds <NEWSPEC>.md is prepared
    Then README.md §10 MUST list <NEWSPEC>.md in the same commit
    And README.md §4 MUST reference <NEWSPEC>.md in the topology tree

  # anchor: RM.1.2
  Scenario: A linter is renamed
    Given an existing linter under /tools/ is renamed
    When the rename commit is prepared
    Then the §6 pre-commit table in README.md MUST reference the new name
    And no occurrence of the old name MUST remain in this README

  # anchor: RM.1.3
  Scenario: The Machine/Actor/Space framing is renamed
    Given an authorised Task proposes a renaming of the framing in §1 or §3
    When the rename is applied
    Then every occurrence of the old framing in README.md MUST be replaced
    And the rename MUST occur via a Task per R.13
    And the rename MUST NOT be a maintenance-tier T1 or T2 repair

  # anchor: RM.1.4
  Scenario: A normative rule R.x is added or removed
    Given the §11.3 or §11.4 list is being modified
    When the modification is committed
    Then existing R.x identifiers MUST retain their numeric values
    And new rules MUST be appended at the next free R.x identifier
    And cross-references elsewhere in this README MUST still resolve
```

### 11.6 Anti-patterns (what this README MUST NOT become)

- **R.17** This README MUST NOT become a tutorial. Hands-on guidance lives in [`/templates/`](./templates) and the relevant root spec.
- **R.18** This README MUST NOT contain prompt drafts, research notes, or task plans. Those live in `/prompts/`, `/research/`, and `/tasks/`.
- **R.19** This README MUST NOT carry runtime state ("last updated", "current sprint", "recent work"). Dynamic state lives in folder-level `readme.md` files per [MAINTENANCE.md §3.2](./MAINTENANCE.md#32-dynamic-readme-updates).
- **R.20** This README MUST NOT contradict any root spec. If a contradiction is detected during the Repo Coherence Check, the root spec wins and this README MUST be reconciled in the same coherence-check commit per [MAINTENANCE.md](./MAINTENANCE.md).

---

*For the full set of rules every agent operating in this repository follows, start at [AGENTS.md](./AGENTS.md).*
