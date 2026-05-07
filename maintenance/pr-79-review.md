---
type: note
status: active
slug: pr-79-review
summary: "Code review for PR #79 — Task 032 AGENTS.md spec integration + 3 enforcement linters. Two critical folder-index violations, two moderate tooling-consistency gaps, one minor provenance gap."
created: 2026-05-07
updated: 2026-05-07
---

# Code Review — PR #79: Task 032 AGENTS.md Spec Integration

**PR:** [#79 Task 032: Integrate research findings and enforce governance discipline](https://github.com/netzkontrast/agency/pull/79)
**Branch:** `claude/agents-spec-integration-Dv725` → `main`
**Head commit:** `f57580e`
**Reviewer:** claude-code (session `claude/brave-darwin-z8eoZ`)
**Date:** 2026-05-07

---

## § RFC 2119

The key words MUST, MUST NOT, SHOULD, and MAY in this document are to be
interpreted as described in RFC 2119 when, and only when, they appear in all
capitals.

---

## Summary Verdict

A disciplined, five-subtask delivery. The mechanics are sound: AGENTS.md edits
land outside the synthesis markers, all 24 unit tests pass, ADR files are
correctly held at `adr_status: Proposed` so the guarded synthesis block stays
empty, and the Jaccard-heuristic polarity linter is the most sophisticated piece
of tooling shipped in this repository to date.

**Two critical omissions prevent a clean merge:**

- R-1 (CRITICAL) — `decisions/readme.md` index was never updated; it still
  reads "_(empty — no ADRs authored yet)_" despite 5 new ADR files landing in
  the same commit.
- R-2 (CRITICAL) — `tools/readme.md` lists only 1 of the 3 new linters
  (`check-narrative-ontology-load.py`); the other two are invisible in the
  folder index.

Both are FOLDERS.md §3 violations. Three further moderate/minor findings are
non-blocking but SHOULD be addressed before or shortly after merge.

---

## Positive Findings

### P-1 — Single-Commit Atomic Delivery

All 23 changed files — five ADRs, research workspace, three linters + their
unit tests, AGENTS.md amendments, task state — land in one commit (`f57580e`).
This satisfies the MAINTENANCE.md T2-Additive single-commit discipline and makes
the diff fully bisectable.

### P-2 — Polarity Heuristic Is Production-Grade

`tools/check-rfc2119-polarity.py` uses Jaccard similarity over stopworded token
sets rather than naive string matching. The boilerplate-window exclusion (lines
around `BCP 14 / RFC 2119` declarations), table-row skip, and fenced-code-block
exclusion are all correct countermeasures against the three highest-volume
false-positive vectors. The corpus run against the 8 root specs returned 0/65
candidate pairs — empirically validating the calibration before shipping.

### P-3 — Advisory-Tier Design Holds

All three new linters are WARN-tier (`exit 2`, never `FAIL=1`). The task's
readme Assumptions Log correctly documents that this means `README §6 R.7`
(pre-commit gating pipeline change notice) does NOT fire. The operator retains
the option to promote any linter to gating via `--strict` without a governance
amendment.

### P-4 — ADR Guard Rails Respected

`tools/adr/cli.py validate AGENTS.md → exit 0` is cited in the commit message.
The `<!-- BEGIN AGENCY-ADR SYNTHESIS -->` markers are intact. Filing the 5 P1
ADRs as `Proposed` rather than `Accepted` is the right call: it exercises the
full ADR workflow without cascading T3 changes into the synthesis block.

### P-5 — Test Coverage Is Authentic

`tools/tests/test_{rfc2119_polarity,assumption_log,narrative_ontology_load}.py`
use real `tempfile.TemporaryDirectory` fixtures and call into the actual modules
via `importlib.util.spec_from_file_location`. No mocks, no patching of the
subjects under test. 9 + 10 + 5 = 24 tests, all passing.

### P-6 — Friction Log Is Honest and Actionable

The FL1 declaration correctly names all three friction sources: pre-existing
baseline ERRORs, the SPEC-mirror ↔ `decisions/` round-trip gap, and the missing
`./install.sh` preamble in subagent briefings. Each friction is traced to a root
cause rather than described in vague terms. The "What Could Be Better" section
produces two concrete, actionable recommendations.

---

## Critical Findings

### R-1 (CRITICAL) — `decisions/readme.md` Index Not Updated

**Location:** `decisions/readme.md`, line 34.

**Symptom.** The `## Index` section in `decisions/readme.md` currently reads:

```
_(empty — no ADRs authored yet. The first batch is sequenced by
tasks/029-adr-assumption-audit/ PD-005 and the implementation Task that
succeeds Task 028.)_
```

This is verbatim from before this PR. The commit `f57580e` added five new files
(`decisions/0001-...md` through `decisions/0005-...md`) but `decisions/readme.md`
was not touched (it does not appear in `git show f57580e --name-only`).

**Rule violated.** FOLDERS.md §3 ("EVERY folder MUST contain a `readme.md`")
requires the readme to list "every file/subfolder via relative Markdown links."
The folder now has 5 files whose existence is invisible to any agent or human
scanning the folder index. The `lint-structure.py` linter does not check index
currency (only presence), so no automated gate catches this.

**Impact.** An agent picking up a successor task that involves promoting an ADR
from `Proposed` to `Accepted` will correctly run `tools/adr/cli.py validate`
but may scan `decisions/readme.md` first (per AGENTS.md AG.1.1, `summary` before
body). Reading the stale index, the agent may conclude no ADRs exist and proceed
to re-author them, producing duplicate records.

**Required fix.** `decisions/readme.md` `## Index` MUST list all five files with
relative Markdown links and one-line summaries. The `updated:` frontmatter field
MUST be bumped to today's date. Example entry format (per the repo's existing
`maintenance/readme.md` navigation convention):

```md
- [0001-mandatory-session-bootstrap.md](./0001-mandatory-session-bootstrap.md) — Session bootstrap and governance gate (SS.1–SS.3). `adr_status: Proposed`.
```

---

### R-2 (CRITICAL) — `tools/readme.md` Lists Only 1 of 3 New Linters

**Location:** `tools/readme.md`, `## Contents` section.

**Symptom.** The commit adds `check-narrative-ontology-load.py`,
`check-rfc2119-polarity.py`, and `check-assumption-log.py` to `/tools/`. The
`tools/readme.md` `## Contents` section was updated to include
`check-narrative-ontology-load.py` (1 insertion) but `check-rfc2119-polarity.py`
and `check-assumption-log.py` are absent from the listing.

**Rule violated.** FOLDERS.md §3: "every file/subfolder [must be] listed via
relative Markdown links." Two of the three newly landed linters are invisible
in the folder index.

**Impact.** The tools folder index is the primary discovery surface for agents
and operators scanning available governance tooling. An agent looking for
"the RFC 2119 polarity checker" will find no entry in `tools/readme.md` and
must fall back to `ls` or `grep` — bypassing the standard navigation contract.

**Required fix.** `tools/readme.md` MUST be updated to add entries for
`check-rfc2119-polarity.py` and `check-assumption-log.py`, following the same
format already used for `check-narrative-ontology-load.py`. The `updated:`
frontmatter date MUST be bumped.

---

## Moderate Findings

### R-3 (MODERATE) — No `ImportError` Guard for `_core` Import in All Three Linters

**Location:**
- `tools/check-narrative-ontology-load.py:37-40`
- `tools/check-assumption-log.py:43`
- (implicitly) `tools/check-rfc2119-polarity.py` — this linter does not import
  `_core` and is exempt.

**Symptom.** Both linters that depend on `tools/fm/_core.py` import it with a
bare `import _core` after a `sys.path.insert`. If `tools/fm/_core.py` is renamed
or removed (a plausible future event given the two-toolchain migration window in
MAINTENANCE.md §2), both scripts crash with an unhandled `ImportError` rather
than exiting 0 (the documented graceful-degradation path for unresolvable context).

**Impact.** `check-governance.sh` swallows the crash via `|| true`, making the
failure invisible to the operator. The WARN-tier linters silently become no-ops
rather than producing an actionable error. An operator who relies on the advisory
checks to catch NO.5 violations or stale assumption logs would receive no signal.

**SHOULD fix.** Each linter SHOULD wrap the `import _core` in a
`try/except ImportError` and emit a diagnostic to stderr (and exit 0) when the
import fails:

```python
try:
    import _core  # type: ignore  # noqa: E402
    read_fm = _core.read_fm
    str_list = _core.str_list
except ImportError:
    import sys as _sys
    print(
        "check-narrative-ontology-load: tools/fm/_core.py not found — "
        "skipping (advisory linter, exit 0).",
        file=_sys.stderr,
    )
    raise SystemExit(0)
```

---

### R-4 (MODERATE) — `sys.path.insert` Inconsistency Between the Two `_core`-Dependent Linters

**Location:**
- `tools/check-narrative-ontology-load.py:37`:
  `sys.path.insert(0, str(Path(__file__).resolve().parent / "fm"))` (unconditional)
- `tools/check-assumption-log.py:37-41`:
  uses a guarded `if str(_FM) not in sys.path:` before inserting.

**Symptom.** Both linters were authored in the same task (ST-2 and ST-4) and
serve analogous roles, but they use different path-insertion patterns. The
guarded form in `check-assumption-log.py` is strictly more correct: it prevents
duplicate entries in `sys.path` when the script is imported by the test suite
(which itself manipulates `sys.path`). The unconditional form in
`check-narrative-ontology-load.py` can produce duplicate entries.

**Impact.** In production, `check-governance.sh` invokes each linter in a fresh
subprocess, so duplicate entries cause no immediate malfunction. But the test
suite (`test_narrative_ontology_load.py`) imports the module via
`importlib.util.spec_from_file_location`, and the unconditional insert
contaminates the test process's `sys.path` with a duplicate entry on every test
run.

**SHOULD fix.** `check-narrative-ontology-load.py:37` SHOULD adopt the guarded
form used in `check-assumption-log.py`. A one-line patch:

```python
# Before:
sys.path.insert(0, str(Path(__file__).resolve().parent / "fm"))

# After:
_FM_PATH = str(Path(__file__).resolve().parent / "fm")
if _FM_PATH not in sys.path:
    sys.path.insert(0, _FM_PATH)
```

---

## Minor Finding

### R-5 (MINOR) — Round-Trip Check Gap Filed as FL1 but No Downstream Task Created

**Location:** `tasks/032-agents-spec-integration/friction-log.md`, FL1 friction
item 2.

**Symptom.** The friction log documents: "There is no mechanical check that a
SPEC entry's source `file:line` citation matches its corresponding `decisions/`
body." This is correctly identified as a quality risk. However, no downstream
Prompt or Task was filed to address it (the Todo list has no item for a new
`tooling-*` prompt or Task in `/prompts/` covering this gap).

**Context.** Under the repo's operating model, every unsolved problem surfaced
during a task MUST surface as a new Prompt or Task if it requires follow-up work
(per AGENTS.md AG.2.1 routing and PROMPT.md §1 item 2: "Follow-up questions
MUST be filed as new prompts in `/prompts/`"). The gap is currently only in
the friction log, which is not part of the audit graph.

**SHOULD fix.** File a new `prompts/tooling-adr-mirror-roundtrip-check/` entry
(or add a finding to an existing open Task) so the gap enters the audit graph.
This is non-blocking for the merge itself but SHOULD be addressed in the same
release window.

---

## Action Items

| Finding | Severity | Fix Target | Blocks merge? |
|---------|----------|------------|---------------|
| R-1: `decisions/readme.md` index stale | Critical | Fix in this branch before merge | YES |
| R-2: `tools/readme.md` missing 2 linters | Critical | Fix in this branch before merge | YES |
| R-3: No `ImportError` guard on `_core` import | Moderate | File new Task or fix here | No |
| R-4: `sys.path.insert` pattern inconsistency | Moderate | File new Task or fix here | No |
| R-5: Round-trip check gap not in audit graph | Minor | New Prompt under `/prompts/` | No |

---

## Conclusion

Merge is **conditional**: R-1 and R-2 MUST be resolved in this branch. Both are
one-file text edits; neither requires a new commit structure or spec change.
R-3 and R-4 do not block merge but SHOULD be absorbed into a follow-up Task
(or fixed here while the branch is open). R-5 is informational. The core work —
five ADRs, three linters, AGENTS.md amendments, 24 passing tests — is solid and
ready to land once the folder-index hygiene is corrected.
