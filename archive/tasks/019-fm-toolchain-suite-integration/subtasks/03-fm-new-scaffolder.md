---
type: note
status: draft
slug: task-019-st3-fm-new
summary: "Subtask ST-3: ship tools/fm/new.py — a template-driven scaffolder that creates a new Task / Prompt / Research workspace with all required frontmatter and required headings pre-filled, satisfying fm-validate on first commit."
created: 2026-05-05
updated: 2026-05-05
---

# ST-3: `fm-new` — Template-Driven Scaffolder

## Goal

Ship `tools/fm/new.py` that scaffolds a new operational artifact (task / prompt / research / skill) from a template, pre-filling every required L1 + L2 key per the ontology, allocating the next free `task_id` (for tasks), and producing a tree that passes `fm-validate --check-body` immediately. Removes the manual "copy from /templates/, hand-edit YAML, fix five typos, run validator three times" loop.

## Falsification

Wrong cut **iff** templates are too few to justify a tool. Mitigation: even three templates today (task / prompt / research) save ~50 lines of frontmatter typing per scaffold and prevent slug-typo errors that the existing flow accidentally commits.

## Inputs

- [`/templates/`](../../../templates/) — existing template files (read what's there; they may need additions).
- [`/maintenance/schemas/header-ontology.json`](../../../maintenance/schemas/header-ontology.json) — required-keys + body_schema source of truth.
- [`/tools/fm/_core.py`](../../../tools/fm/_core.py) — reuse `iter_operational_files` for next-id allocation.
- [`/TASK.md`](../../../TASK.md) §2 (directory structure) and §8.1 (concurrent task numbering).

## Acceptance Criteria

1. **Surface.**
   - `tools/fm/new.py task --slug <kebab-case> --summary "…" [--owner <name>] [--priority P0|P1|P2|P3]`
   - `tools/fm/new.py prompt --slug <kebab-case> --summary "…" --kind <prompt_kind> --framework <prompt_framework>`
   - `tools/fm/new.py research --slug <kebab-case> --summary "…" --executes-prompt <slug>`
2. **Filesystem result.** Creates the canonical folder + `task.md` / `prompt.md` / `output/SPEC.md` + `readme.md`, each with frontmatter that passes `fm-validate` and a body that passes `fm-validate --check-body`. Also a `notes.md` stub.
3. **Next-id allocation (tasks only).** Reads `tasks/` and picks the next zero-padded id; refuses on collision (per TASK.md §8.1).
4. **No clobber.** If the target folder exists, exits 4 with a clear message; never overwrites.
5. **Tests.** New file `tests/fm/test_new.py`. Cover: each kind, the no-clobber refusal, next-id allocation, and that the produced tree passes `fm-validate --check-body`.
6. **Cookbook entry.** Add a one-paragraph "Scaffolding new artifacts" entry to whatever cookbook ST-7 produces (loose coupling — ST-3 produces the entry text in its own commit message; ST-7 picks it up).

## Dependencies

None. Phase A.

## Estimated Effort

Small (~120 LOC + 100 LOC tests).

## Agent Prompt

```text
You are implementing tools/fm/new.py for the netzkontrast/agency repo on
branch claude/execute-task-16-ZrBJe.

Repo root: /home/user/agency

Context files (read first):
  - templates/                                    (existing templates)
  - maintenance/schemas/header-ontology.json
  - tools/fm/_core.py
  - tools/fm/validate.py                          (the validator your output must satisfy)
  - TASK.md                                       (§2 directory structure, §8.1 task ids)
  - PROMPT.md, RESEARCH.md                        (per-type structure rules)

Acceptance criteria:
  1. Three subcommands: task, prompt, research. Flags as documented above.
  2. Output passes both:
       python3 tools/fm/validate.py <new-folder>
       python3 tools/fm/validate.py --check-body <new-folder>
  3. Next-id allocation: scan tasks/ for the highest numeric id, return id+1
     zero-padded. Refuse if the chosen folder name already exists.
  4. No clobber: target folder existence → exit 4 with clear stderr.
  5. Tests in tests/fm/test_new.py exercising each subcommand and the
     no-clobber/next-id paths.
  6. All existing tests still pass.

Constraints:
  - Python 3.11 stdlib only.
  - You MAY add new template files under templates/ if existing ones are
    insufficient — but DO NOT modify existing template files in this subtask.
  - Do NOT modify other tools/fm/*.py.

When done:
  - python3 -m unittest discover -s tests/fm -t .
  - python3 tools/validate-frontmatter.py
  - Smoke: tmpdir=$(mktemp -d) && cd $tmpdir && \
      python3 /home/user/agency/tools/fm/new.py task --slug test-x --summary "t" \
      && python3 /home/user/agency/tools/fm/validate.py tasks/
  Commit "feat(fm/new): template-driven scaffolder for task/prompt/research (Task 019 ST-3)".
  Do NOT push.
```
