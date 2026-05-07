---
type: note
status: active
slug: pr-80-review
summary: "Code review for PR #80 — Task 032 follow-up: address PR #79 findings R-1..R-5. All five findings correctly resolved; three minor observations remain."
created: 2026-05-07
updated: 2026-05-07
---

# Code Review — PR #80: Task 032 Follow-Up (PR #79 Findings R-1..R-5)

**PR:** [#80 chore(task-032): address PR #79 review (R-1..R-5)](https://github.com/netzkontrast/agency/pull/80)
**Branch:** `claude/task-032-pr79-followup-Dv725` → `main`
**Head commit:** `d9c4398`
**Reviewer:** claude-sonnet-4-6 (session `claude/brave-darwin-2gKSt`)
**Date:** 2026-05-07

---

## § RFC 2119

The key words MUST, MUST NOT, SHOULD, and MAY in this document are to be
interpreted as described in RFC 2119 when, and only when, they appear in all
capitals.

---

## Summary Verdict

A precise follow-up that correctly addresses all five findings from the
[PR #79 review](./pr-79-review.md). The two critical folder-index violations
(R-1, R-2) are fixed. The two moderate tooling-consistency gaps (R-3, R-4)
are resolved with clean, consistent code. The minor audit-graph gap (R-5) is
closed by filing a well-formed RISEN+ReAct prompt. No regressions are
introduced: 24/24 existing tests pass and `check-governance.sh` reports no
new ERRORs beyond the three pre-existing baseline issues.

**Verdict: LGTM — merge is unblocked.**

Three minor observations below are non-blocking and SHOULD be addressed
either in the merging window or as a follow-up task.

---

## Positive Findings

### P-1 — Complete Finding Coverage

Every finding from the PR #79 review is addressed in a single focused commit.
The commit message maps each change explicitly to its finding code (R-1 through
R-5). This is exactly the traceability model the repo's governance expects; a
future agent picking up `maintenance/pr-79-review.md` can confirm closure
without reading the full diff.

### P-2 — `ImportError` Guard Pattern Is Consistent

Both `tools/check-narrative-ontology-load.py` and `tools/check-assumption-log.py`
now use the same graceful-degradation pattern:

```python
try:
    import _core
except ImportError:
    print("...: tools/fm/_core.py not importable — skipping (advisory linter, exit 0).", file=sys.stderr)
    raise SystemExit(0)
```

The diagnostic message format `<linter-name>: tools/fm/_core.py not importable — skipping (advisory linter, exit 0).` is identical between both linters, which is the right call for grep-ability in operator run-logs.

### P-3 — `sys.path` Guard Alignment (R-4)

`check-narrative-ontology-load.py` now uses the guarded form:

```python
_FM_PATH = str(Path(__file__).resolve().parent / "fm")
if _FM_PATH not in sys.path:
    sys.path.insert(0, _FM_PATH)
```

This matches `check-assumption-log.py`'s established pattern and prevents
`sys.path` contamination in test-suite processes that import the module via
`importlib`. The fix is minimal (three lines replacing one) and carries no
risk of behavioral regression.

### P-4 — New Prompt Follows PROMPT.md Contract

`prompts/tooling-adr-mirror-roundtrip-check/` ships all three required files
(`brief.md`, `prompt.md`, `readme.md`) with:

- Correct L1 Vault Core frontmatter on all three files.
- `prompt.md` carrying every required `prompt_*` L2 key (kind, framework,
  target_agent). The OPTIONAL `prompt_relates_to_task` field is correctly
  absent given the unbound state.
- Framework declared in BOTH frontmatter (`prompt_framework: RISEN+ReAct`)
  and body header — per PROMPT.md §5 rule 2.
- A complete RISEN+ReAct structure: R (Role), I (Input), S (Steps),
  E (Expectations), and a separate Constraints section serving the N slot.
- Self-contained: every input reference resolves to a relative path or
  named tool within the repo.

### P-5 — `prompts/readme.md` Proactively Updated

The PR author added `tooling-adr-mirror-roundtrip-check/` to the
`prompts/readme.md` index in the same commit, preventing a FOLDERS.md §3
violation identical to R-2. This shows the R-2 finding was internalized as a
behavioral correction, not just a mechanical fix.

### P-6 — Verification Attestation Is Specific

The commit message cites exact command invocations and results:

```
python3 -m pytest tools/tests/test_{narrative_ontology_load,assumption_log,rfc2119_polarity}.py → 24/24 pass
python3 tools/adr/cli.py validate → exit 0 (5 ADRs, 0 diagnostics)
python3 tools/fm/validate.py --type-check prompts/tooling-adr-mirror-roundtrip-check/ → 0 diagnostics
bash tools/check-governance.sh: no NEW ERRORs
```

This level of specificity lets a reviewer reproduce each check independently.

---

## Minor Observations

### O-1 (MINOR) — No Test for the New `ImportError` Path

**Location:** `tools/tests/test_narrative_ontology_load.py`,
`tools/tests/test_assumption_log.py`

**Observation.** R-3 introduces `ImportError` guards in both linters, but
neither test file contains a scenario that exercises this path (confirmed by
searching both files for `ImportError`, `_core`, and `not_importable` — zero
hits). The existing 24 tests all run against an environment where `_core` is
importable.

**Impact.** The guard can silently regress (e.g. the exit code could be
changed from 0 to 1 without a test failing). The risk is low because the
logic is trivial (catch → print → raise SystemExit(0)), but the pattern is
not self-testing.

**Recommendation.** A follow-up task SHOULD add a test for each linter that
patches `sys.modules` to force `ImportError` on `_core` and asserts:
(a) exit code is 0, (b) stderr contains the expected diagnostic message.
This is a two-case addition per linter (≤ 30 lines total).

---

### O-2 (MINOR) — `prompts/tooling-adr-mirror-roundtrip-check/readme.md` Lacks `## Assumptions Log`

**Location:** `prompts/tooling-adr-mirror-roundtrip-check/readme.md`

**Observation.** The new prompt's `readme.md` does not carry an
`## Assumptions Log` section. AGENTS.md §"Folder Management & Workflow Drift"
states that every operational folder's `readme.md` SHOULD log assumptions.
FOLDERS.md F.3 binds the section heading. The mechanical linter
(`tools/check-assumption-log.py`) only enforces this for `tasks/<NNN>-<slug>/`
and `research/<slug>/` readmes — `prompts/<slug>/` readmes are outside the
linter's current scope — so no automated gate will catch this today.

**Impact.** The omission is consistent with the existing prompt readmes in
this repository (none appear to carry an `## Assumptions Log`), which means
this is a systemic gap, not a deviation introduced by this PR. However, a new
prompt readme is a clean opportunity to set the correct pattern.

**Recommendation.** Adding a minimal section:

```md
## Assumptions Log

(none)
```

would satisfy the AGENTS.md SHOULD requirement and establish the pattern for
future prompt readmes. This is a 2-line addition.

---

### O-3 (OBSERVATION) — `prompt_kind: task-spec` on an Unbound Prompt

**Location:** `prompts/tooling-adr-mirror-roundtrip-check/prompt.md:9`

**Observation.** The prompt is filed as `prompt_kind: task-spec`. PROMPT.md
§1 defines a task-spec as "Prompts referenced by a Task in `/tasks/` via
`task_uses_prompts`." Since no Task currently references this prompt, calling
it a `task-spec` is semantically anticipatory.

An argument exists for `prompt_kind: follow-up` since the prompt was surfaced
as a follow-up question from a review finding (analogous to a follow-up
question from a prior research run, per PROMPT.md §1 item 2). However, the
prompt body contains a detailed implementation specification rather than an
open question, making `task-spec` reasonable in terms of content shape.

**Impact.** This is a labelling ambiguity, not a correctness issue. The YAML
validator will accept either value. The `follow-up` kind would have required
setting `prompt_spawned_from_research` (which doesn't apply here — this came
from a review, not a research run), so `task-spec` may in fact be the better
fit.

**Recommendation.** No action required. Document the labelling decision in
the prompt's `brief.md` or `readme.md` if a future agent queries the lineage.
The `prompt.md` body already explains the unbound state clearly via the R-Role
section.

---

## Scope Check: Was Anything Missed from PR #79?

| Finding | Addressed? | Notes |
|---------|-----------|-------|
| R-1 (CRITICAL) — `decisions/readme.md` stale | ✅ | All 5 ADRs listed with links and one-line summaries; `updated:` bumped |
| R-2 (CRITICAL) — `tools/readme.md` missing 2 linters | ✅ | Both `check-rfc2119-polarity.py` and `check-assumption-log.py` added |
| R-3 (MODERATE) — No `ImportError` guard | ✅ | Both affected linters patched; `check-rfc2119-polarity.py` correctly exempt |
| R-4 (MODERATE) — `sys.path.insert` inconsistency | ✅ | `check-narrative-ontology-load.py` now uses guarded form |
| R-5 (MINOR) — Round-trip gap not in audit graph | ✅ | New prompt filed; `prompts/readme.md` updated |

All five findings are closed. No finding from the PR-79 review was left open
or partially addressed.

---

## Conclusion

PR #80 is a clean, minimal follow-up that resolves all PR #79 review findings
without introducing new complexity. The code is correct, the verification is
attestable, and the new prompt artifact is spec-conformant. The three
observations above (O-1 test gap, O-2 missing Assumptions Log, O-3 label
ambiguity) are non-blocking and SHOULD be addressed in a future maintenance
window rather than held against this PR.

**Merge recommendation: APPROVED.**
