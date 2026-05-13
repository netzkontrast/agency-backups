---
type: spec
status: active
slug: folders-spec
summary: "Repository folder topology, separation of concerns between /tasks/, /prompts/, /research/, and the mandatory readme.md rule."
created: 2026-05-02
updated: 2026-05-13
---

# Folder Interaction Specification

> **Mechanical Enforcement Notice:** This spec is mechanically enforced by `tools/check-governance.sh`. Before editing any folder under `/tasks/`, `/prompts/`, or `/research/`, install the pre-commit hook once with `tools/install-hooks.sh`. The readme.md presence rule (§3) is enforced by [`tools/lint-structure.py`](./tools/lint-structure.py); the readme.md frontmatter rule (§5) is enforced by [`tools/check-readme-frontmatter.py`](./tools/check-readme-frontmatter.py) (ERROR-tier); the cross-directory frontmatter linkage rule (§6) is enforced by [`tools/lint-linkage.py`](./tools/lint-linkage.py); the body-link / frontmatter dual-surface drift rule (§6) is detected (WARN-tier) by [`tools/check-audit-graph-consistency.py`](./tools/check-audit-graph-consistency.py).

To ensure navigation and traceability across the repository, agents MUST abide by the rules below.

## 1. Top-Level Topology (Separation of Concerns)

| Directory | Owner Spec | Purpose | Holds |
|---|---|---|---|
| `/tasks/` | `TASK.md` | Orchestration: *what should be done*. | Task folders `<NNN>-<slug>/` with `task.md`. |
| `/prompts/` | `PROMPT.md` | Instruction: *what the agent is told to do*. | Prompt folders `<slug>/` with `brief.md` and `prompt.md`. |
| `/research/` | `RESEARCH.md` | Evidence: *what running a prompt produced*. | Research workspaces `<slug>/` with workspace, synthesis, reflection, output. |
| `/skills/` | `SKILLS.md` | Capability: *what the agent knows how to do* | Skill folders `<slug>/` with `SKILL.md`. |

**Hard rule on flow:** A Task references one or more Prompts (`task_uses_prompts`). A Prompt, when executed by an agent, produces a Research run whose slug equals the Prompt's slug. Research surfaces follow-up questions back into `/prompts/` (never inline). This forms the audit graph.

```text
/tasks/<NNN>-<slug>/task.md
        │ task_uses_prompts ──► /prompts/<slug>/prompt.md
                                        │ executed by agent ──► /research/<slug>/output/SPEC.md
                                                                          │ open questions ──► /prompts/<new-slug>/ (prompt_kind: follow-up)
```

## 2. Slug & Folder Naming

- All operational folders use the form `/<top-level>/<slug>/`. Slugs are kebab-case, max 5 tokens.
- Tasks additionally prefix with a zero-padded sequence: `/tasks/<NNN>-<slug>/`.
- The slug of a Research workspace MUST equal the slug of the Prompt it executes.

## 3. The `readme.md` Rule (Decentralized Documentation)

- **Rule:** EVERY folder MUST contain a `readme.md`.
- **Enforcement:** [`tools/lint-structure.py`](./tools/lint-structure.py) emits an `ERROR` for every operational folder (`/tasks/<NNN>-<slug>/`, `/prompts/<slug>/`, non-provider `/research/<slug>/`) missing a `readme.md`. The pre-commit hook blocks the commit on any such error.
- **Exemption (F.1.1):** Provider sub-trees `/research/<provider>/<slug>/` (where `<provider>` ∈ `gemini`, `gpt`, `human`, `other`) and the ADR ledger `/decisions/` are out of scope. They are external mirrors / governed-by-their-own-spec storage folders, not operational orchestration folders. The linters [`tools/lint-structure.py`](./tools/lint-structure.py), [`tools/check-readme-frontmatter.py`](./tools/check-readme-frontmatter.py), and [`tools/check-audit-graph-consistency.py`](./tools/check-audit-graph-consistency.py) MUST honour the exemption.
- **Why:** Adjacent docs prevent doc-drift; the user can trust repository state without consulting a separate `/docs/` tree.
- **Update Trigger:** Pre-commit batching. Agents update touched folders' `readme.md` as a single pre-commit step, not on every file change. This protects context window from administrative bloat.
- **Required Content:**
  1. **What and Why** — What the folder is, why it exists in this location.
  2. **Linked Navigation** — Every file/subfolder listed via relative Markdown links (e.g., `[output/](./output)`).
  3. **Assumptions Log** — Any implicit assumption the agent made about how the folder is used.

## 4. Subfolder Heuristics

1. **Prefer Flat Structures** — Do not create a subfolder unless 4+ files of the exact same category accumulate.
2. **Consolidation First** — Consolidate inside the parent before reaching for sub-directories.
3. **No Empty Scaffolding** — Do not pre-create subfolders "in case". Create them when populated.

### 4.1 Mandatory Scaffold for `/prompts/<slug>/`

Every `/prompts/<slug>/` folder MUST contain three files at creation time, regardless of which template the agent copies from:

| File | Purpose | Enforcement |
|---|---|---|
| `prompt.md` | The executable instruction set, with L1 + Prompt-namespace frontmatter (per `PROMPT.md §3`). | `tools/lint-structure.py` emits an ERROR if absent. |
| `brief.md` | One-screen orientation: what this prompt asks an agent to do and why, written for a human reader skimming the directory. | `tools/lint-structure.py` emits an ERROR if absent. |
| `readme.md` | Directory index per §3, linking the two files above. | `tools/lint-structure.py` emits an ERROR if absent. |

This rule is **mandatory at folder creation**, not deferred to a later cleanup step. The Task 001 friction log recorded multiple cases where `brief.md` or `readme.md` were omitted because the agent assumed the template was authoritative; relying on template fidelity alone is not sufficient. Treat the three-file scaffold as the contract, with the templates as a convenience.

When a follow-up prompt is generated mid-run (e.g. a research run produces an open question that becomes a new prompt), the spawning agent MUST create all three files in the same commit that introduces the prompt folder. A prompt folder containing only `prompt.md` is a structural lint failure even if the body content is otherwise complete.

## 5. Frontmatter on Folder Indexes

`readme.md` files in operational folders MUST carry L1 Vault Core frontmatter (per `TASK.md` §3) so the file system itself is queryable. Minimal example:

```yaml
---
type: index
status: active
slug: <folder-slug>
summary: "What this folder holds and why it exists."
created: YYYY-MM-DD
updated: YYYY-MM-DD
---
```

**Slug convention.** Vault-level slug uniqueness forces the readme to qualify itself so it does not collide with the sibling `task.md` / `prompt.md`. Convention: `task-<NNN>-<bare-slug>` for tasks, `<bare-slug>-readme` for prompts, `<bare-slug>-research-readme` for research workspaces. The linter ([`tools/check-readme-frontmatter.py`](./tools/check-readme-frontmatter.py)) requires the bare folder slug (with the `<NNN>-` prefix stripped for tasks) to appear as a substring of the readme `slug:`.

**Enforcement:** [`tools/check-readme-frontmatter.py`](./tools/check-readme-frontmatter.py) emits an `ERROR` for any operational-folder `readme.md` missing an L1 Vault Core key or whose `slug:` fails the substring rule above. Step `[2/N]` of [`tools/check-governance.sh`](./tools/check-governance.sh) invokes the linter; the pre-commit hook blocks on any diagnostic. Provider research sub-trees (§F.1.1) and `/skills/<slug>/` (§8) are exempt; `/decisions/<NNNN>-<slug>.md` files use the `adr` type validated by [`tools/adr/cli.py validate`](./tools/adr/cli.py).

## 6. Cross-Directory Linking (Audit Graph)

Linkage between Tasks, Prompts, and Research MUST flow exclusively through frontmatter keys defined in `TASK.md` §3:

- Task → Prompt: `task_uses_prompts: [<slug>, ...]`
- Task → Research: `task_spawns_research: [<slug>, ...]`
- Prompt → Task: `prompt_relates_to_task: <slug>`
- Prompt → Research (origin): `prompt_spawned_from_research: <slug>`
- Research → Prompt: `research_executes_prompt: <slug>`
- Skill → Skill: `skill_references_skills: [<slug>, ...]`
- Skill → Research: `skill_references_research: [<slug>, ...]`
- Skill → Prompt: `skill_references_prompts: [<slug>, ...]`

Body-level Markdown links between folders are encouraged for human navigation, but the **frontmatter is the source of truth** for any future CLI/graph tooling.

**Enforcement:** [`tools/lint-linkage.py`](./tools/lint-linkage.py) walks every operational folder and emits an `ERROR` when any of the five frontmatter linkage keys above fails to resolve to its target file or folder. The pre-commit hook blocks the commit on any such error. Reciprocity (Prompt ↔ Task) is also checked.

**Dual-surface drift (F.6 advisory).** The frontmatter and the prose are two surfaces of the same audit graph. When a body link cites a sibling operational folder (e.g. `task.md` body links `[the prompt](../../prompts/foo/prompt.md)`) but the corresponding frontmatter linkage key (`task_uses_prompts: [foo]`) is silent, the prose has drifted ahead of the source-of-truth. [`tools/check-audit-graph-consistency.py`](./tools/check-audit-graph-consistency.py) walks every `task.md` / `prompt.md` / `readme.md` in the operational roots and emits a `WARN` diagnostic for each drift. The reverse asymmetry (frontmatter present, body silent) is **not** flagged — body links remain encouraged, not required. The linter runs WARN-tier `[opt]` in `tools/check-governance.sh` and never gates the commit; agents resolve drift either by adding the missing frontmatter linkage or by rephrasing the body to remove the implied edge. Set `FM_AUDIT_GRAPH_STRICT=1` to promote the WARN-tier diagnostics to gating (useful once the historical drift backlog is resolved by a triage Task).

## Acceptance Criteria

The following Gherkin scenarios are the executable acceptance contract for §1, §2, §4.1.1, §6, and §8. Each scenario is anchored with a stable identifier (`F.B.<n>`); the linters above are MAY-implement hooks for scenarios where mechanical enforcement is feasible. The section number `§6.1` is the stable downstream-tooling identifier (e.g. for Gherkin parsers); the heading text mirrors the wording of `prompts/spec-amendment-folders-md/brief.md` AC4.

```gherkin
# anchor: F.B.1
Feature: readme.md presence rule (F.1, F.3)
Scenario: Operational folder missing readme.md — ERROR
  Given a new folder `tasks/099-example/` containing only `task.md`
  When `tools/lint-structure.py` runs at pre-commit
  Then the linter MUST emit an ERROR identifying the missing readme.md
  And `tools/check-governance.sh` MUST exit non-zero
  And the commit MUST be blocked until the readme.md is added
```

```gherkin
# anchor: F.B.2
Feature: slug naming rule (F.2)
Scenario: Task folder name does not match `<NNN>-<slug>` pattern — ERROR
  Given a folder `tasks/example-without-prefix/` (no numeric prefix)
  When `tools/lint-structure.py` runs at pre-commit
  Then the linter MUST emit an ERROR citing the F.2 naming rule
  And `tools/check-governance.sh` MUST exit non-zero
```

```gherkin
# anchor: F.B.3
Feature: prompt three-file scaffold (F.4.1.1)
Scenario: New prompt folder missing brief.md — ERROR
  Given a new folder `prompts/new-prompt/` containing only `prompt.md` and `readme.md`
  When `tools/lint-structure.py` runs at pre-commit
  Then the linter MUST emit an ERROR identifying the missing brief.md
  And the diagnostic MUST cite F.4.1.1
  And `tools/check-governance.sh` MUST exit non-zero
```

```gherkin
# anchor: F.B.4
Feature: audit-graph dual-surface consistency (F.6)
Scenario: Body link cites a sibling prompt but `task_uses_prompts` is silent — WARN
  Given a `tasks/<NNN>-<slug>/task.md` whose `task_uses_prompts` does NOT include `foo`
  And the body of the same `task.md` contains the link `[the prompt](../../prompts/foo/prompt.md)`
  When `tools/check-audit-graph-consistency.py` runs at pre-commit (`[opt]` tier)
  Then the linter MUST emit a WARN diagnostic
        `<relpath>::WARN:F.6:body-link-without-frontmatter:foo`
  And `tools/check-governance.sh` MUST NOT block the commit (advisory only)
  And the agent MAY resolve the drift either by adding `foo` to
        `task_uses_prompts` or by rephrasing the body to remove the
        implied edge
```

```gherkin
# anchor: F.B.5
Feature: §8 exemption coverage for `/decisions/`
Scenario: ADR file under `/decisions/` exempt from prompt-scaffold rule
  Given a new file `decisions/0042-storage-path.md` with frontmatter `type: adr`
  And the file matches the pattern `decisions/[0-9][0-9][0-9][0-9]-*.md`
        registered in `maintenance/schemas/header-ontology.json`
  When `tools/lint-structure.py` runs at pre-commit
  Then the linter MUST NOT flag the file for missing brief.md / prompt.md
        (those are F.4.1.1 prompt-scaffold requirements, not ADR requirements)
  And `tools/adr/cli.py validate` MUST validate the `adr_*` L2 keys
        per the ADR JSON-Schema in `header-ontology.json`
```

## 7. Anti-Patterns

- **MUST NOT** create operational folders outside `/tasks/`, `/prompts/`, `/research/`. Top-level governance specs (`TASK.md`, `PROMPT.md`, `RESEARCH.md`, `FOLDERS.md`, `FRUSTRATED.md`, `PRE_COMMIT.md`, `AGENTS.md`) live at the repo root. *Exemption:* the non-operational storage folders enumerated in §8 (`/skills/`, `/templates/`, `/tools/`, `/maintenance/`, `/decisions/`, `/Agency-System/`, `/.claude/`, `/.claude-plugin/`) are explicitly out of scope of this rule.
- **MUST NOT** mix kinds inside one folder (e.g., a prompt draft inside a research workspace).
- **MUST NOT** rely on body-level Markdown links instead of frontmatter for cross-directory linkage that tooling will consume.

## 8. Non-Operational Storage Folders (Explicit Exemptions)

Some top-level folders hold content that is mirrored from, or destined for, an external runtime — they are not operational orchestration folders and are therefore exempt from §1 and §7:

| Folder | Purpose | Exemption scope |
|---|---|---|
| `/skills/` | Version-controlled mirror of Claude skills (`SKILL.md` + assets). Runtime location is `~/.claude/skills/` and `/mnt/skills/user/`. | Exempt from the `/tasks/`-`/prompts/`-`/research/` partition. Per-skill `readme.md` files are auto-generated from each `SKILL.md` frontmatter and SHOULD NOT be hand-edited. They are NOT required to carry L1 Vault Core frontmatter. |
| `/templates/` | Frontmatter and folder skeletons consumed by agents when creating new operational artifacts. | Files MAY contain `REPLACE` tokens; the validator skips template files for that check. The folder's own `readme.md` MUST carry L1 frontmatter. |
| `/tools/` | Repository tooling (validator, lints, helpers). | The folder's own `readme.md` MUST carry L1 frontmatter; individual scripts do not. |
| `/maintenance/` | Canonical language spec and maintenance run logs. | Treated as a governance annex; not in the audit graph. |
| `/decisions/` | Architectural Decision Records (ADRs) — repo-native MADR 4.0.0 ledger governed by `research/adr-spec-research-synthesis/output/SPEC.md` and validated by `tools/adr/cli.py`. | Files use the `adr` type and `adr_*` L2 namespace; each `decisions/<NNNN>-<slug>.md` MUST carry L1 frontmatter. Once `adr_status: Accepted`, the file is T4-immutable per `MAINTENANCE.md` §1; the corpus synthesises into the guarded section of `AGENTS.md` via `tools/adr/cli.py synthesize`. |
| `/Agency-System/` | Frontend prototype for the Agency System triptychon (HTML/JSX/SVG) — design-system source consumed by `skills/the-agency-system-architect/`. Not an operational orchestration folder. | Exempt from §1 / §7 and from the audit graph. The folder is opaque to `tools/validate-frontmatter.py` and `tools/lint-linkage.py`; assets are referenced from skills via plain Markdown links. The folder MUST contain a `readme.md` documenting the prototype's purpose and lifecycle (authoring ADR pending). |
| `/.claude/` | Claude Code project-level integration surface authored by Task 094 ST-2. Holds `settings.json` (project config + ST-3 hook registry), a `skills/` symlink to the repo-root `/skills/` corpus, 16 persona sub-agent re-exports under `agents/` (`sc-pm-agent` deliberately excluded per CLAUDE.md §13.1 `/sc:pm`-only routing), a `commands/` placeholder, and a `skills-fallback/install-claude-dir.sh` copy-tree materialiser for platforms without symlink support. | Exempt from §1 / §7 and from the audit graph. The folder is opaque to `tools/validate-frontmatter.py`, `tools/lint-linkage.py`, and the operational-readme linters. The `agents/<slug>.md` wrappers re-export by reference (canonical bodies stay at `skills/<slug>/SKILL.md`). ADR-0011 D.7 forbids SessionStart-hook injection — `settings.json` MUST NOT register a SessionStart hook. |
| `/.claude-plugin/` | Plugin manifest folder declaring `agency@1.0.0` per `https://docs.anthropic.com/en/docs/claude-code/plugins`. Holds exactly one file: `plugin.json`. | Exempt from §1 / §7 and from the audit graph. The folder is opaque to `tools/validate-frontmatter.py` and `tools/lint-linkage.py`. Per platform docs, every other plugin asset (skills/, agents/, hooks/) stays at the plugin root (= this repo root); `.claude-plugin/` itself MUST NOT contain those folders. |

`tools/validate-frontmatter.py` enforces this partition mechanically: it walks `/tasks/`, `/prompts/`, `/research/`, `/templates/`, `/tools/` only. Adding a new top-level folder that is *not* on this list is itself an anti-pattern unless it is explicitly listed in the table above.
