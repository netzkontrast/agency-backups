# tests/integration/

End-to-end governance suite for the Task -> Prompt -> Research triptych.

The suite is gated on `INTEGRATION=1` in `tools/check-governance.sh` so the
default governance run stays fast. Run it directly with:

```
INTEGRATION=1 tools/check-governance.sh   # via the gate
pytest tests/integration/                  # directly
```

## Files

- `conftest.py` — `triptych_fixture` materialises `fixtures/seed/` into a
  fresh `tmp_path`, copies the live `maintenance/schemas/` files in, and
  runs `git init`.
- `test_governance_e2e.py` — one happy-path test plus a parametrised
  mutator-test per row of `TASK.md §7.0`. Each mutator inverts a single
  invariant and asserts the documented diagnostic ID surfaces.
- `fixtures/seed/` — minimal valid triptych (one Task, one Prompt, one
  Research workspace) that passes every §7.0 row when run unmodified.

## Row coverage

| Row | Mutator | Linter | Expected diagnostic |
|---|---|---|---|
| §7.1 | typo `tpye:` | `fm-validate` | `F.3.4` |
| §7.2 | body-schema item-count violation | `fm-validate --check-body` | `F.B.2` |
| §7.3 | dangling `task_uses_prompts` | `fm-validate --type-check` | `F.T.1` |
| §7.4 | dangling `task_spawns_research` | `fm-validate --type-check` | `F.T.1` |
| §7.5 | (no mechanical check — human review) | — | skipped |
| §7.6 | all `[x]` but `task_status: in_progress` | `fm-validate --check-body --strict` | `F.B.7` |
| §7.7 | remove `readme.md` | `lint-structure.py` | `missing required readme.md` |
| §7.8 | remove `friction-log.md` | `check-trust.py` | `has no friction-log.md` |
| §7.9 | dangling `task_blocked_by` | `fm-validate --type-check` | `F.T.1` |
| §7.10 | dangling `task_supersedes` | `fm-validate --type-check` | `F.T.1` (see note) |
| §7.11 | delete index entry | `fm/index_diff.py` | `099-fixture-task` |
| §8.1 | clone task with same `task_id` | `fm/check-duplicate-task-id.py` | `duplicate` |

§7.10 currently downgrades to `F.T.1` (dangling) because the
`task_supersedes` ↔ `task_superseded_by` reciprocity rule is not yet wired
into `maintenance/schemas/header-ontology.json:reciprocity.rules`. When
that rule lands, swap the expected token to `F.T.2` and the mutator can
add a non-reciprocating sibling Task instead of a non-existent slug.
