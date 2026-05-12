---
type: note
status: active
slug: triage-note-sc-modes-bundling
summary: "Triage note for the two SC modes ported as references/ bundles: MODE_Introspection (bundles into sc-reflect) and MODE_Task_Management (bundles into sc-task). Phase 1 precedent: MODE_Orchestration → sc-implement, MODE_DeepResearch → sc-research."
created: 2026-05-12
updated: 2026-05-12
---

# Triage note — Mode bundling strategy

Per Phase 1 precedent ([Task 091 ST-1](../../091-port-external-skill-corpora/task.md)), behavioural **modes** do not land as standalone `skills/sc-mode-*/` folders — they bundle as `references/` content inside the host skill that activates them. ST-2 ports two modes this way:

| Snapshot path | Host skill | Landing path |
|---|---|---|
| `modes/MODE_Introspection.md` (1.9 KB) | `sc-reflect` | `skills/sc-reflect/references/mode-introspection.md` |
| `modes/MODE_Task_Management.md` (3.6 KB) | `sc-task` | `skills/sc-task/references/mode-task-management.md` |

## Why bundle, not standalone

- A mode is a **behavioural overlay** for a host skill, not an independently invocable capability. The user does not say "/sc:mode-introspection"; they say "/sc:reflect" and the mode is silently active.
- Standalone skill folders for modes would proliferate `skills/sc-mode-*/` entries that no audit-graph forward-edge ever points at.
- Phase 1 bundled `MODE_Orchestration.md` → `skills/sc-implement/references/` and `MODE_DeepResearch.md` → `skills/sc-research/references/` — Phase 2 MUST follow the same convention.

## Bundling recipe (ST-2)

For each mode:

1. Copy upstream body to `skills/<host-skill>/references/mode-<name>.md`.
2. Add L1 frontmatter (`type: note`, `status: active`, `slug: mode-<name>-bundle`, `summary: "..."`, `created: 2026-05-12`, `updated: 2026-05-12`).
3. In the **host skill's** SKILL.md body, add an `## Active modes` section listing the bundled mode(s) and explaining when each activates.
4. **No** `skill_references_skills: [mode-*]` edges — modes are not skills, so the audit graph treats them as references not capabilities.

## Skipped modes

Three of the five unported modes are `skip`:

- `MODE_Brainstorming` (row 40) — duplicates the `sc-brainstorm` command body almost verbatim. No bundle target needed.
- `MODE_Business_Panel` (row 41) — D.6 + D.8 violator (11.8 KB + MCP bindings). Sub-mode content extracted instead into `sc-business-panel/references/sub-modes.md` per the `sc-business-panel.md` triage note.
- `MODE_Token_Efficiency` (row 42) — already covered by Agency's `sc-*` corpus equivalent; no port target needed.

## Audit-graph linkage

The host skills' `skill_source` frontmatter SHOULD note the bundle:

- `sc-reflect` SKILL.md frontmatter: `skill_source: "superclaude_framework@v4.3.0"` + optional body-level `## References` link to `references/mode-introspection.md`.
- `sc-task` SKILL.md frontmatter: same; link to `references/mode-task-management.md`.
