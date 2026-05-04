# M07 — Contradiction Log

Every contradiction surfaced between the pre-refactor root specs and the new architecture, with the resolution applied.

## C1 — Where Do Follow-Up Questions Live?

- **Pre-refactor state:** `RESEARCH.md` §6 implied open questions get appended to the research workspace (e.g., a `## Open Questions` section in `output/SPEC.md`). This left the questions buried in a closed run.
- **New rule:** `RESEARCH.md` §4.9 mandates open questions be filed *outward* as new prompts under `/prompts/` with `prompt_kind: follow-up` and `prompt_spawned_from_research: <source-slug>`.
- **Resolution:** Authored. Closed-run amendments are explicitly forbidden in `RESEARCH.md` §6 anti-patterns.

## C2 — Where Do Research Proposals Live?

- **Pre-refactor state:** `/prompt/` (singular) was unspecified for "research proposals". `RESEARCH.md` did not explicitly forbid drafting a prompt inside `/research/<slug>/`.
- **New rule:** All instruction sets — including research proposals — live under `/prompts/`. `RESEARCH.md` is execution-only.
- **Resolution:** Authored. `PROMPT.md` §1 lists research proposals as the first prompt kind.

## C3 — `prompt/` (Singular) vs `prompts/` (Plural)

- **Contradiction:** Pre-refactor folder was `/prompt/`. New spec mandates `/prompts/`. Existing readme content already said "Prompt Root" (which is fine in either spelling).
- **Resolution:** `git mv prompt prompts`. All cross-spec references updated. The legacy prompt body inside `research-prompt-from-annotations/prompt.md` still references `/prompt/` and is queued for retrofit by Task-001.

## C4 — Pre-Commit Routing

- **Contradiction:** `PRE_COMMIT.md` §6 routed only Research Tasks to a context-specific spec. Tasks and Prompts were second-class.
- **Resolution:** `PRE_COMMIT.md` §6 rewritten with three-row routing table (Task/Prompt/Research). New §7 added invoking the frontmatter validator.

## C5 — Frontmatter Requirement vs Existing Workspaces

- **Contradiction:** New spec mandates frontmatter on operational files. Every pre-refactor research workspace lacks it. Naive enforcement would block every commit.
- **Resolution:** Two-layer mitigation. (a) The validator scopes itself narrowly to spec-mandated files (`task.md`, `prompt.md`, `output/SPEC.md`, root `readme.md`s). (b) A `tools/.frontmatter-waivers` file grandfathers pre-existing artifacts; closing Task-001 burns that list to zero.

## C6 — `task.md` vs `task_status` Frontmatter Field

- **Risk:** Two layers of "status" — L1 `status` (active/draft/archived) and L2 `task_status` (open/in_progress/done/abandoned). Could confuse readers.
- **Resolution:** L1 `status` is *publication-state* (is this file actively maintained?); L2 `task_status` is *workflow-state* (where in the lifecycle?). Documented in `TASK.md` §3.2 and §3.3. Both kept because collapsing them would lose information visible to the Obsidian Properties UI.

## C7 — Sequence Numbering Concurrency

- **Contradiction:** Slug-based naming was always collision-resistant; `<NNN>-<slug>` reintroduces a numeric collision class.
- **Resolution:** `TASK.md` §8.1 added in second pass — agents MUST renumber on commit if `<NNN>` already exists. Slug remains the stable identifier; number is presentation order only.
