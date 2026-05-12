---
type: note
status: active
slug: triage-note-sc-pure-ports-cluster
summary: "Combined triage note for the nine SC 'pure port' items: commands/analyze, design, document + agents/devops-architect, learning-guide, python-expert, requirements-analyst, root-cause-analyst, self-review. No MCP bindings, all ≤ 5 KB. Mechanical ports with audit-graph wiring."
created: 2026-05-12
updated: 2026-05-12
---

# Triage note — SC "pure port" cluster

Nine SC artefacts have **zero MCP bindings** and bodies ≤ 5 KB. They port mechanically — no adaptation needed beyond audit-graph wiring. Listed here so ST-2 can batch them in one PR.

## Files

| Snapshot path | KB | Landing slug | Tier | Forward refs (`skill_references_skills`) |
|---|---|---|---|---|
| `commands/analyze.md` | 3.5 | `sc-analyze` | L1 | `[sc-test, sc-improve, sc-refactoring-expert]` |
| `commands/design.md` | 3.6 | `sc-design` | L1 | `[sc-implement, sc-system-architect]` |
| `commands/document.md` | 3.3 | `sc-document` | L1 | `[sc-explain]` |
| `agents/devops-architect.md` | 2.5 | `sc-devops-architect` | L1 | `[sc-system-architect, sc-backend-architect]` |
| `agents/learning-guide.md` | 3.0 | `sc-learning-guide` | L1 | `[sc-explain, sc-document, sc-socratic-mentor]` |
| `agents/python-expert.md` | 3.1 | `sc-python-expert` | L1 | `[sc-implement, sc-test, sc-quality-engineer]` |
| `agents/requirements-analyst.md` | 3.0 | `sc-requirements-analyst` | L1 | `[sc-brainstorm, sc-design]` |
| `agents/root-cause-analyst.md` | 3.0 | `sc-root-cause-analyst` | L1 | `[sc-troubleshoot, superpowers-systematic-debugging]` |
| `agents/self-review.md` | 1.4 | `sc-self-review` | L1 | `[sc-test, superpowers-verification-before-completion]` |

## Port recipe (ST-2)

For each file:

1. `cp` the body to `skills/<slug>/SKILL.md`.
2. Add Agency frontmatter:
   ```yaml
   ---
   type: skill
   status: active
   slug: <slug>
   summary: "<one-line>"
   created: 2026-05-12
   updated: 2026-05-12
   skill_source: "superclaude@v4.3.0"
   skill_references_skills: [...]
   ---
   ```
3. Strip the upstream YAML frontmatter (`name`, `description`, `category`, `complexity`, `mcp-servers`, `personas`).
4. Write `skills/<slug>/readme.md` with L1 frontmatter (`type: index`) + one-paragraph "What and Why" + `## Assumptions Log` heading.
5. No `references/` extraction needed (all bodies ≤ 5 KB).
6. Run `tools/fm/validate.py skills/<slug>/` after each port; must exit 0 before moving to the next.

## Audit-graph note

The forward refs in the table above are **proposals**; ST-2 MAY refine them as porting reveals concrete edges. The `superpowers-*` forward refs (rows for `root-cause-analyst` and `self-review`) MAY land as `[]` if ST-3 has not yet shipped the `superpowers-*/` folders — re-add the edges in a follow-up commit after ST-3.

## Assumptions

- All 9 files were inspected as part of ST-1 triage and confirmed MCP-free.
- The 8.2 KB `commands/help.md` is **not** in this cluster (skip, matrix row 19).
- The 5.7 KB `commands/brainstorm.md` is **not** in this cluster (adapt with D.6 + D.8, see `sc-brainstorm.md` note).
