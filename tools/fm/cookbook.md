---
type: note
status: active
slug: fm-cookbook
summary: "Recipe-first cookbook for the fm toolchain: eight worked workflows with shell snippets, each linked back to the normative SPEC clause."
created: 2026-05-05
updated: 2026-05-05
---

# fm Cookbook

Recipes own the *how*. The [SPEC](../../research/flexible-frontmatter-toolchain/output/SPEC.md) owns the *why*. Every workflow below leads with a one-line trigger, a runnable snippet, and a SPEC pointer.

## When to reach for which tool

- Need to know if a file or tree is well-formed? → `fm-validate` (see SPEC §5.1).
- Need to read one piece of a file without parsing the whole thing? → `fm-extract` (SPEC §5.2).
- Need to mutate a frontmatter scalar or list? → `fm-edit` (SPEC §5.3).
- Need to find files matching a selector? → `fm-query` (SPEC §5.4).
- Need to mutate a body section (replace, append, check off a task)? → `fm-section` (SPEC §13).

A rough decision flow:

```text
read?  ──────── one section ──────── fm-extract --section
       └── one frontmatter key ──── fm-extract --frontmatter KEY
write? ──────── frontmatter ──────── fm-edit
       └── body section ─────────── fm-section
search?────────── fm-query
lint?  ──────── fm-validate (+ --check-body once migrated)
```

## Workflow 1 — Validate before commit

When the pre-commit hook is bypassed or you want a fast local check before staging.

```shell
python3 tools/fm/validate.py tools/fm/             # path-scoped
python3 tools/fm/validate.py                       # whole tree
```

See SPEC §5.1 for exit codes and §7.1 for the canonical pre-commit wiring.

## Workflow 2 — Extract a section by name

When an agent needs to read just `## Goal` or `## Plan` from a task without slurping the whole file.

```shell
python3 tools/fm/extract.py tasks/019-fm-toolchain-suite-integration/task.md --section Goal
python3 tools/fm/extract.py path/to/file.md --sections Goal,Plan,Todo   # batch, \f-separated
```

See SPEC §5.2 for the section-addressing contract and §13.3 for duplicate-heading rules.

## Workflow 3 — Query open tasks

When you need a list of every task that is not yet done.

```shell
python3 tools/fm/query.py "type=task,task_status=open" --format paths
python3 tools/fm/query.py "type=task,status=active" --format json --limit 50
```

See SPEC §5.4 for selector grammar and supported output formats.

## Workflow 4 — Edit a frontmatter scalar

When you need to flip `status:` or set any single key — never hand-edit YAML if `fm-edit` can do it.

```shell
python3 tools/fm/edit.py tasks/019-fm-toolchain-suite-integration/task.md --set status=done
python3 tools/fm/edit.py path/to/file.md --unset draft_field
```

See SPEC §5.3 for write semantics, scalar quoting, and the file-lock guarantee.

## Workflow 5 — Bump-updated sweep on changed files

When you finish a working session and need every touched file's `updated:` to reflect today.

```shell
git diff --name-only --diff-filter=AM HEAD \
  | grep -E '\.md$' \
  | xargs -I{} python3 tools/fm/edit.py {} --bump-updated
```

See SPEC §5.3 for `--bump-updated` semantics (UTC, idempotent within the same day).

## Workflow 6 — Section-edit a single Plan step (check-task)

When closing one Plan/Todo item without touching the rest of the section.

```shell
python3 tools/fm/section.py tasks/019-.../task.md \
  --check-task Todo "ST-7"
```

See SPEC §13.1 for the `fm-section` surface and §13.2 for the invariants (no other lines touched, idempotent re-run).

## Workflow 7 — Did-you-mean response

When `fm-validate` flags `did-you-mean: 'tpye' → 'type'` (or similar) on a key you typoed.

```shell
python3 tools/fm/validate.py path/to/file.md          # see the diagnostic
python3 tools/fm/edit.py path/to/file.md --unset tpye  # remove the typo
python3 tools/fm/edit.py path/to/file.md --set type=note
```

See SPEC §3.4 for the OSA-1 distance rule that powers the suggestion.

## Workflow 8 — `--check-body` promotion path

When migrating a corpus from frontmatter-only validation to full §12 body schemas.

```shell
python3 tools/fm/validate.py --check-body tasks/      # opt-in, surface F.B.* codes
python3 tools/fm/validate.py --check-body --strict    # promote WARN to non-zero
```

See SPEC §12 for the per-type body schema, §12.4 for the `F.B.*` diagnostic codes, and §12.6 for the phasing toward default-on.

## See also

- [`readme.md`](./readme.md) — folder index and tool table.
- [`SPEC.md`](../../research/flexible-frontmatter-toolchain/output/SPEC.md) — normative behaviour.
- [`../readme.md`](../readme.md) — wider tooling layer.
