---
type: note
status: draft
slug: task-030-st5-build-term-editor
summary: "Subtask ST-5: ship tools/dramatica-nav/term.py — a CLI for create / edit / move / deprecate workflows on per-term entries (frontmatter + body coordination + ontology.json sync). Removes the manual hand-edit-then-validate loop currently required for any term mutation."
created: 2026-05-05
updated: 2026-05-05
subtask_id: "ST-5"
subtask_phase: "B"
subtask_recommended_agent: "python-expert"
subtask_status: not-started
subtask_depends_on:
  - "ST-1"
  - "ST-2"
  - "ST-3"
  - "ST-4"
subtask_falsification: "Wrong cut iff the term-editor surface conflicts with tools/fm/edit.py ergonomics. Mitigation: tool reuses tools/fm/edit.py for frontmatter-only operations and only adds new code for term-spanning operations (create/move/deprecate)."
---

# ST-5: `term.py` — Per-Term Editor

## Goal

Ship `tools/dramatica-nav/term.py` that mechanises the create / edit / move / deprecate workflows on per-term entries. Today these workflows require:

- hand-editing the source file under `skills/dramatica-vocabulary/references/`,
- hand-editing the `nav-ontology` YAML block,
- hand-running `tools/dramatica-nav/ontology-build.py` to project frontmatter changes into `ontology.json`,
- hand-running `tools/dramatica-nav/validate.py` to catch drift,
- and praying you didn't forget any of the above.

`term.py` collapses this to one CLI invocation per workflow.

CLI surface:

```text
tools/dramatica-nav/term.py create  --id <ontology-id> --kind <kind> --label <Label> [--file <target-md>] [--scenarios <list>]
tools/dramatica-nav/term.py edit    --id <ontology-id> [--add-alias <locale>:<value>] [--remove-alias <locale>:<value>] [--set-scenario <list>]
tools/dramatica-nav/term.py move    --id <ontology-id> --to-file <target-md> [--rename-anchor <new-slug>]
tools/dramatica-nav/term.py deprecate --id <ontology-id> --reason "<one-line>" [--alias-on <successor-id>]
```

Per-subcommand contracts:

- **`create`** mints a `## <Label>` heading + `<!-- nav-ontology -->` YAML block in the target source file, AND a matching ontology entry in `ontology.json`. Refuses if `<ontology-id>` already exists. Refuses if `<target-md>` doesn't exist. Defaults `<target-md>` based on `kind` (element → `elements.md`, variation → `variations.md`, etc.).
- **`edit`** is alias / scenario manipulation only. For frontmatter / body field edits, defer to `tools/fm/edit.py` (the existing tool). The new tool's job is to keep ontology.json in sync after `fm/edit.py` has written changes — i.e., `term.py edit --refresh <ontology-id>` re-reads frontmatter and updates ontology.
- **`move`** rewrites the `term_file` pointer, optionally renames the heading anchor, and physically moves the heading + body + frontmatter block from one source file to another. Refuses if the target file lacks a clean section break to insert at; emits a hint to re-run with `--position before-section <slug>` or `--position end-of-file`.
- **`deprecate`** marks an entry as deprecated. Two lifecycles:
  - With `--alias-on <successor-id>`: deletes the source heading, adds the deprecated label as `deprecated_aliases_en` on the successor's ontology entry, removes the original ontology entry. (Same pattern ST-4 applies to Female Mental Sex.)
  - Without `--alias-on`: keeps the source heading + frontmatter, adds `status: deprecated` to the YAML block, prefixes the source body with a `> **Deprecated** — <reason>` admonition. **NOTE:** this requires an ontology schema bump for term-level `status` field — IF the schema doesn't yet support it, `term.py deprecate` MUST file the schema-bump request as an ADR via the `agency-adr` CLI shipped by [Task 028](../../028-adr-tooling-impl-plan/) (see the §Dependencies Pre-dispatch Gate). The ADR carries the proposed schema delta + the term that triggered the request; `term.py` then falls back to the alias-on path so the user is never blocked. If the dispatcher honoured the Pre-dispatch Gate, `agency-adr` will be on PATH; if (against the gate) it isn't, this branch emits a `# TODO(after-028)` stderr line and the alias-on fallback runs unconditionally. Schema bumps are explicitly out of scope here.

After every subcommand, `term.py`:
1. Re-runs `ontology-build.py --check` (existing tool).
2. Re-runs `validate.py` and surfaces any new diagnostics.
3. Either commits the result (if `--commit "<msg>"` is passed) or leaves the working tree dirty for the user.

## Falsification

Wrong cut **iff** the term-editor surface conflicts with `tools/fm/edit.py` ergonomics. Mitigation: ST-5 explicitly DELEGATES frontmatter-field edits to `tools/fm/edit.py`. The new tool is term-spanning operations only (create / move / deprecate). The `edit` subcommand is a thin wrapper that calls `tools/fm/edit.py` then re-syncs the ontology — it does NOT re-implement edit logic.

## Inputs

- `tools/fm/edit.py` and `tools/fm/_core.py` — reuse helpers; do not re-implement.
- `tools/dramatica-nav/ontology-build.py`, `validate.py`, `nav.py`, `lib/` — reuse the ontology load/index helpers.
- `maintenance/schemas/narrative-ontology/term-frontmatter.schema.json` — the YAML block contract.
- `maintenance/schemas/narrative-ontology/ontology.schema.json` — the table entry contract.
- `tools/dramatica-nav/tests/fixtures/` — existing test fixtures; extend, don't replace.

## Acceptance Criteria

1. **Surface complete.** All four subcommands implemented with the documented flag set.
2. **Tests.** `tools/dramatica-nav/tests/test_term.py` covers:
   - happy path per subcommand (4 tests),
   - edge cases: duplicate ID on create (1), missing file on create (1), no-clean-break on move (1), schema-bump-required on deprecate-without-alias-on (1),
   - integration: a sequence `create` → `edit` → `move` → `deprecate` produces a clean diff (1).
3. **Reuse, not duplicate.** `term.py` imports from `tools/fm/_core.py` (`iter_operational_files` or equivalent) and `tools/dramatica-nav/lib/ontology.py`. No new YAML parser, no new schema validator.
4. **No clobber.** Every subcommand refuses to overwrite without explicit `--force`.
5. **Idempotent.** Running the same `term.py edit --refresh <id>` twice produces no diff.
6. **Gates pass.** `pytest tools/dramatica-nav/tests/`, `tools/check-governance.sh`, and `python3 tools/dramatica-nav/validate.py` all exit 0 after ST-5 lands.
7. **Single commit.** Title: `feat(dramatica-nav): term.py for create/edit/move/deprecate (Task 030 ST-5)`.

## Dependencies

Phase B (parallel with ST-6 and ST-7) — but with two gates:

1. **Phase A merged.** ST-1 / ST-2 / ST-3 / ST-4 must have landed on the integration branch before ST-5 dispatches. Building the term-editor against an artefact-bearing corpus would produce false-positive validate.py warnings that the editor's smoke tests would have to whitelist.
2. **Pre-dispatch Gate — Task 028.** ST-5's `term.py deprecate` files schema-bump requests as ADRs via the `agency-adr` CLI shipped by [Task 028](../../028-adr-tooling-impl-plan/). The dispatching agent MUST verify Task 028 is `task_status: done` before opening a worktree for ST-5; if Task 028 is not yet done, the dispatch MUST defer ST-5 (and ONLY ST-5 — the other Phase B subtasks remain dispatchable). Per [PR #55 review C1](https://github.com/netzkontrast/agency/pull/55) and parent task §Background.

## Estimated Effort

Medium (~250 LOC + ~150 LOC tests).

## Agent Prompt

```text
You are implementing ST-5 of Task 030 (cleanup-dramatica-skills-corpus) for
the netzkontrast/agency repo on branch claude/cleanup-dramatica-skills-1cEOO.

This subtask runs in worktree isolation.

Repo root: /home/user/agency
Working directory: /home/user/agency

Context files (read first):
  - tasks/030-cleanup-dramatica-skills-corpus/task.md
  - tasks/030-cleanup-dramatica-skills-corpus/subtasks/05-build-term-editor.md (this file)
  - tools/fm/edit.py (the existing frontmatter editor — DO REUSE)
  - tools/fm/_core.py (helper module)
  - tools/dramatica-nav/lib/ontology.py (the existing ontology load/index)
  - tools/dramatica-nav/ontology-build.py (the existing rebuild script)
  - tools/dramatica-nav/validate.py (the existing validator)
  - maintenance/schemas/narrative-ontology/term-frontmatter.schema.json
  - maintenance/schemas/narrative-ontology/ontology.schema.json

Goal:
  Ship tools/dramatica-nav/term.py with four subcommands: create / edit /
  move / deprecate. Each performs the term-spanning operation (markdown
  heading + YAML block + ontology.json table entry coordination). Delegate
  frontmatter-field edits to tools/fm/edit.py — do NOT re-implement.

Acceptance criteria (reproduce verbatim from this file's Acceptance Criteria
section). All seven must be true.

Implementation approach:
  1. Sketch the subcommand surface; pin per-subcommand flag sets.
  2. Implement using stdlib + existing tools/fm/_core.py + existing
     tools/dramatica-nav/lib/ontology.py. No third-party deps beyond what
     these modules already use.
  3. For deprecate without --alias-on, the schema-bump required path: emit
     a clear friction error and fall back to alias-on if a successor was
     identifiable; otherwise refuse with exit code 5 and stderr message.
  4. Author tools/dramatica-nav/tests/test_term.py with 8 tests as
     specified in Acceptance §2.
  5. Run pytest. Run validate.py. Run check-governance.sh.
  6. Commit one focused commit; do NOT push.

Constraints:
  - Python 3.11 stdlib + jsonschema only (jsonschema is already vendored
    per Task 015).
  - Do NOT bump the ontology or term-frontmatter schemas. New fields
    (status: deprecated) are forbidden here.
  - Do NOT modify tools/fm/edit.py or tools/dramatica-nav/{nav,extract,
    validate,ontology-build}.py — reuse only.
  - All four subcommands must be importable from a Python REPL without
    side effects (they're argparse-driven main()-functions).

When done:
  - pytest tools/dramatica-nav/tests/                 (must pass)
  - python3 tools/dramatica-nav/validate.py           (must exit 0)
  - tools/check-governance.sh                         (must exit 0)
  - python3 tools/dramatica-nav/term.py create --id el.smoke --kind element \
      --label "Smoke" --file /tmp/test-elements.md   (smoke test)
  - Commit "feat(dramatica-nav): term.py for create/edit/move/deprecate (Task 030 ST-5)"
  - Do NOT push.
```
