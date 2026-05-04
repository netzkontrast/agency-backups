---
type: spec
status: active
slug: folders-spec
summary: "Repository folder topology, separation of concerns between /tasks/, /prompts/, /research/, and the mandatory readme.md rule."
created: 2026-05-02
updated: 2026-05-04
---

# Folder Interaction Specification

To ensure navigation and traceability across the repository, agents MUST abide by the rules below.

## 1. Top-Level Topology (Separation of Concerns)

| Directory | Owner Spec | Purpose | Holds |
|---|---|---|---|
| `/tasks/` | `TASK.md` | Orchestration: *what should be done*. | Task folders `<NNN>-<slug>/` with `task.md`. |
| `/prompts/` | `PROMPT.md` | Instruction: *what the agent is told to do*. | Prompt folders `<slug>/` with `brief.md` and `prompt.md`. |
| `/research/` | `RESEARCH.md` | Evidence: *what running a prompt produced*. | Research workspaces `<slug>/` with workspace, synthesis, reflection, output. |

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

## 5. Frontmatter on Folder Indexes

`readme.md` files in operational folders SHOULD carry L1 Vault Core frontmatter (per `TASK.md` §3) so the file system itself is queryable. Minimal example:

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

## 6. Cross-Directory Linking (Audit Graph)

Linkage between Tasks, Prompts, and Research MUST flow exclusively through frontmatter keys defined in `TASK.md` §3:

- Task → Prompt: `task_uses_prompts: [<slug>, ...]`
- Task → Research: `task_spawns_research: [<slug>, ...]`
- Prompt → Task: `prompt_relates_to_task: <slug>`
- Prompt → Research (origin): `prompt_spawned_from_research: <slug>`
- Research → Prompt: `research_executes_prompt: <slug>`

Body-level Markdown links between folders are encouraged for human navigation, but the **frontmatter is the source of truth** for any future CLI/graph tooling.

## 7. Anti-Patterns

- **MUST NOT** create operational folders outside `/tasks/`, `/prompts/`, `/research/`. Top-level governance specs (`TASK.md`, `PROMPT.md`, `RESEARCH.md`, `FOLDERS.md`, `FRUSTRATED.md`, `PRE_COMMIT.md`, `AGENTS.md`) live at the repo root. *Exemption:* the non-operational storage folders enumerated in §8 (`/skills/`, `/templates/`, `/tools/`, `/maintenance/`) are explicitly out of scope of this rule.
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

`tools/validate-frontmatter.py` enforces this partition mechanically: it walks `/tasks/`, `/prompts/`, `/research/`, `/templates/`, `/tools/` only. Adding a new top-level folder that is *not* on this list is itself an anti-pattern unless it is explicitly listed in the table above.
