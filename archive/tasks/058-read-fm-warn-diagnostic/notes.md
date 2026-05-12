---
type: note
status: active
slug: 058-read-fm-warn-diagnostic-notes
summary: "Surface decision (a) module-level diagnostic sink vs (b) tuple return; selected (b) for purity and back-compat."
created: 2026-05-08
updated: 2026-05-08
---

# Surface Decision — `read_fm` WARN Diagnostic

## Options Evaluated

(a) **Module-level diagnostic sink.** `read_fm()` would push a WARN
    `Diag` into a process-global list that callers drain at the end of
    the run.

(b) **Tuple return.** Add `read_fm_with_diag(path, *, strict=False) ->
    tuple[dict, Diagnostic | None]`. Keep `read_fm()` as a thin
    back-compat wrapper that drops the second value.

## Decision

**(b) — tuple return.** Pure-functional, no module-level mutable
state, trivially testable, no ordering hazards across threads
(`fm_edit` ships a P4 thread-race test that already exercises
`parse_frontmatter` from multiple workers — option (a) would force us
to scope the sink per-thread to keep that test deterministic).
Back-compat for the dozen existing `read_fm` callers is preserved by
leaving the legacy single-return signature intact.

The new function also normalises the previously-swallowed `OSError`
into a structured WARN, so callers that pass paths from a stale glob
get a diagnostic instead of an empty dict.

## Threading Into `validate.py`

`check_file()` already raises `Diag` via `parse_frontmatter(strict=True)`
on malformed YAML and emits an ERROR `F.3.3`, so the main per-file
path needs no change. The cross-file `_build_slug_index()` pass uses
`read_fm(strict=False)`; under the old code, a malformed task file
disappeared silently and downstream `F.T.1` dangling-reference errors
would mention the *referencing* files instead of the broken one. The
new path now collects WARN diagnostics from `read_fm_with_diag()`,
attaches them to the offending file's relative path, and surfaces
them through `type_check()`'s diagnostics list. Under `--strict` the
WARNs promote to ERROR via the existing `--strict` plumbing.

## Falsification Coverage

`tools/tests/fm/test_falsification_attacks.py::TestP6ReadFmDiagnoses`
adds five cases covering the empty / no-frontmatter / well-formed /
malformed-strict / malformed-non-strict / legacy-API distinctions plus
a back-compat smoke test for the single-return wrapper.
