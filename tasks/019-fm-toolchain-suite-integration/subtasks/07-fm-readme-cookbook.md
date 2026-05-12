---
type: note
status: draft
slug: task-019-st7-fm-readme-cookbook
summary: "Subtask ST-7: author tools/fm/readme.md as the discoverable entry point for the toolchain, plus a cookbook of the eight most-used workflows. Independent — runs in parallel with all other Phase A subtasks."
created: 2026-05-05
updated: 2026-05-05
---

# ST-7: `tools/fm/readme.md` + Cookbook

## Goal

Author the missing `tools/fm/readme.md` (every other tool dir has one) and a cookbook of the eight most-used workflows. The cookbook is example-driven; the SPEC stays normative.

## Falsification

Wrong cut **iff** the cookbook duplicates SPEC content. Mitigation: cookbook entries lead with a *recipe* (shell snippet) and one-line *when to reach for it*; the *normative why* stays in SPEC.

## Inputs

- All four (now five with `fm-section`) tools' `--help` output.
- [`/research/flexible-frontmatter-toolchain/output/SPEC.md`](../../../research/flexible-frontmatter-toolchain/output/SPEC.md).
- The eight named workflows (below).

## The Eight Workflows

1. **Validate one file.** `python3 tools/fm/validate.py path/to/file.md`
2. **Validate the whole tree.** `python3 tools/fm/validate.py`
3. **Validate body schemas too.** `python3 tools/fm/validate.py --check-body`
4. **Read a section quickly.** `python3 tools/fm/extract.py path --section Goal`
5. **Bump the `updated:` date.** `python3 tools/fm/edit.py path --bump-updated`
6. **Find every task in `task_status: open`.** `python3 tools/fm/query.py "type=task,status=active"`
7. **Find broken slug references.** `python3 tools/fm/validate.py --type-check` (after ST-5)
8. **Close a task** (compound):
   ```
   python3 tools/fm/edit.py task.md --set task_status=done
   python3 tools/fm/edit.py task.md --bump-updated
   python3 tools/fm/section.py task.md --check-task Todo "<item>"   # after Task 018
   ```

## Acceptance Criteria

1. **`tools/fm/readme.md`.** Has frontmatter (`type: index`), a one-paragraph "what this folder is", a navigation section listing every `.py` in the folder with a one-line summary, and a link to the cookbook.
2. **Cookbook file.** `tools/fm/cookbook.md` (or merged into the readme — author's choice). Each workflow gets: a shell snippet, a one-line "when", and a link to the relevant SPEC section. ≤ 300 lines total.
3. **Body-schema clean.** Both files pass `python3 tools/fm/validate.py --check-body`.
4. **No duplication.** Sample audit: pick three sentences at random; each MUST point at SPEC.md for the *why*, while the cookbook owns the *how*.

## Dependencies

None. Phase A.

## Estimated Effort

Small (~250 lines of Markdown).

## Agent Prompt

```text
You are authoring tools/fm/readme.md and tools/fm/cookbook.md for the
netzkontrast/agency repo on branch claude/execute-task-16-ZrBJe.

Repo root: /home/user/agency

Context files (read first):
  - tools/fm/{validate,extract,edit,query}.py   (run --help on each)
  - research/flexible-frontmatter-toolchain/output/SPEC.md
  - tools/readme.md                             (model the style on this)
  - tools/dramatica-nav/                        (example of a tool-dir readme)

Deliverables:
  1. tools/fm/readme.md
       - frontmatter (type: index, status: active, slug: tools-fm-readme,
         summary, created, updated)
       - "What this folder is" (1 paragraph)
       - "Tools" table (name | one-line summary | link)
       - "Quick start" (3 lines: validate, extract, query)
       - "See also" (link to cookbook + SPEC)
  2. tools/fm/cookbook.md
       - frontmatter (type: note, status: active, slug: fm-cookbook, ...)
       - "When to reach for which tool" decision flow
       - eight workflows from the subtask file, each with:
           ## Workflow N — <Title>
           One-line when-to-use.
           ```shell snippet```
           See SPEC §X.

Acceptance:
  - Both files pass: python3 tools/fm/validate.py --check-body
  - Cookbook ≤ 300 lines, readme ≤ 100 lines.
  - No prose duplicates SPEC content; instead links to it.

Constraints:
  - Markdown only; no code edits.
  - Follow the existing voice in tools/readme.md (concise, present tense,
    minimal qualifier words).

When done:
  - python3 tools/fm/validate.py --check-body tools/
  - python3 tools/validate-frontmatter.py
  Commit "docs(fm): add tools/fm/readme.md + cookbook (Task 019 ST-7)".
  Do NOT push.
```
