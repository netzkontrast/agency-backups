---
type: research
status: completed
slug: pr27-governance-review
summary: "Governance code-review of PR #27. Verdict: APPROVE WITH REQUESTS — core fixes are correct; four issues need follow-up."
created: 2026-05-04
updated: 2026-05-04
research_phase: complete
research_executes_prompt: pr27-governance-review
research_friction_level: FL0
---

# Governance Review — PR #27

**PR:** `fix(governance): restore green check-governance + clarify spec semantics`
**Branch:** `claude/analyze-code-PfoLl` → `main`
**SHA:** `c6b146592aabe5c82d0ef786aadda5c315603af5`
**Reviewer:** claude-code (claude-sonnet-4-6), 2026-05-04
**Verdict:** ✅ **APPROVE WITH REQUESTS** — core mission accomplished; four issues require follow-up.

---

## § RFC 2119

The key words MUST, MUST NOT, REQUIRED, SHALL, SHALL NOT, SHOULD, SHOULD NOT, RECOMMENDED,
NOT RECOMMENDED, MAY, and OPTIONAL in this document are to be interpreted as described in
BCP 14 [RFC 2119] [RFC 8174] when, and only when, they appear in all capitals as shown here.

---

## Summary

PR #27 restores `tools/check-governance.sh` from 15 errors to a clean exit-0 state. It does
so through five coherent change clusters: linkage-bug fixes, spec-drift reconciliation,
a DRY refactor of the four governance linters, retroactive friction-log filing, and minor
housekeeping. The changes are technically correct and the spec clarifications are accurate.

However, the session that produced these repairs is itself ungoverned: no Task was opened
for the work, no run-log entry was committed, and the most-visible operational prompt in the
repo (`repo-coherence-check`) was not updated to conform to the very OPTIONAL-field convention
the PR introduces. These are process conformance gaps, not logic errors.

---

## Strengths

### S1 — Core Mission Accomplished

The PR fixes all 15 `check-governance.sh` failures. The three root causes (provider-subfolder
slug resolution, overloaded `prompt_relates_to_task`, missing `task_spawns_research` retrofit)
are each addressed minimally and correctly.

### S2 — DRY Refactor is Architecturally Sound

`tools/_frontmatter.py` introduces two parse modes that make semantic sense:

- `strict=True` — used by `validate-frontmatter.py`; raises `Diag` on any malformation.
  This is the gate.
- `strict=False` — used by downstream linters that trust the validator's gate; returns `{}`
  on malformed input rather than aborting.

The Python `sys.path` concern (importing `_frontmatter` when the script is invoked from the
repo root) is a non-issue: `python3 tools/X.py` adds `tools/` to `sys.path` automatically,
so `from _frontmatter import` resolves correctly in all invocation patterns used by
`check-governance.sh`.

Net line count: −207 / +65 across the four linter files. The refactor is strictly subtractive
in complexity.

### S3 — Spec Clarifications are Correct

The disambiguation of `prompt_relates_to_task` (encodes *uses*, requires reciprocity) versus
`prompt_spawned_from_research` (encodes *spawned-by*, no reciprocity) is the accurate
semantic reading of the linker's enforcement logic. Stating it explicitly in PROMPT.md §6.5
and §6.6 closes the spec-to-implementation gap that produced the original linkage failures.

### S4 — AGENTS.md RFC 2119 Fix is Correct

Lowercasing "SHOULD" in the L1 field-semantics table (AGENTS.md) correctly applies rule R2:
RFC 2119 keywords in uppercase MUST NOT appear in rationale or descriptive prose. The table
cell describes what the field is; it is not a normative sentence. This fix is correct.

### S5 — Friction Logs Correctly Retrofitted

Both retroactive friction logs (`tasks/002`, `tasks/003`) are well-formed, cite their
provenance explicitly, and assign FL1 declarations consistent with the events they describe.
`tasks/003`'s log is particularly valuable: it names all three friction types as governance
signals and maps each to the spec update applied in this PR.

### S6 — `.gitignore` Gap Closed

Adding `__pycache__/`, `*.pyc`, and `.agent_cache/` to `.gitignore` was a genuine missing
guard, especially now that `_frontmatter.py` is committed.

---

## Issues

### Issue 1 (SPEC CONFORMANCE — SELF-REFERENTIAL) — `repo-coherence-check/prompt.md` not updated

**Spec clause:** PROMPT.md §3, §6.6 (as updated by this PR).

The PR introduces the rule that `prompt_relates_to_task` and `prompt_spawned_from_research`
are OPTIONAL and SHOULD be omitted when not applicable. Yet
`prompts/repo-coherence-check/prompt.md` lines 11–12 still carry:

```yaml
prompt_relates_to_task: ""
prompt_spawned_from_research: ""
```

These empty strings are exactly the pattern the PR's own spec update deprecates. The validator
now no longer requires these keys (`L2_PROMPT` was trimmed to the trio), so this slips past
automated checks silently.

This is the most visible prompt in the repository — it is the entry point for the coherence
routine itself. Leaving it non-conformant with the convention it helped motivate is a
self-referential inconsistency that future agents will copy as a pattern.

**Requested action:** Update `prompts/repo-coherence-check/prompt.md` to omit
`prompt_relates_to_task` and `prompt_spawned_from_research` entirely. Similarly audit the
other prompts in the repo for lingering empty-string OPTIONAL fields.

---

### Issue 2 (AUDIT GRAPH — UNGOVERNED SESSION) — No Task covers this repair session

**Spec clause:** AGENTS.md CR.5.

AGENTS.md CR.5 requires: "The PR body created by `/sc:createPR` MUST reference (a) the
closed Task slug(s) under `/tasks/` if any."

The PR body cites `tasks/002-token-efficiency-tool-suite` and
`tasks/003-analyze-skillmd-novel-authoring` as "Closed Task slugs cited." But neither task
drove this session's work. Task 002 was about researching token-efficiency tools; Task 003
was about analyzing SKILL.md authoring research. Both are closed by the retroactive
friction-log additions — a T1/T2 bookkeeping action, not the primary session goal.

The actual session work — 15 governance-error fixes, a DRY refactor of four linters, and
five spec-drift reconciliations — corresponds to no Task in `/tasks/`. This is a
governance-of-governance gap: the governance repair itself is un-tasked. If a future audit
asks "which Task authorized the changes to `tools/lint-linkage.py`?", there is no answer
in the audit graph.

**Requested action:** Open a Task (e.g. `006-governance-coherence-repair-2026-05-04`) in
`/tasks/` that covers this session's work retroactively, or document the absence as a
deliberate exception in `maintenance/run-log.md`.

---

### Issue 3 (PROTOCOL CONFORMANCE) — No `maintenance/run-log.md` entry

**Spec clause:** `prompts/repo-coherence-check/prompt.md` Step 6 (MUST); `AGENTS.md §LOOP_LOG`
pattern.

The driving prompt (`repo-coherence-check`) Step 6 requires: every coherence-class run MUST
append a record to `maintenance/run-log.md` before committing. The last entry in the run-log
is from jules (2026-05-04, baseline commit `f620b6d`). This PR's 19 file changes — which are
entirely coherence-class repairs — are not traceable via the run-log audit trail.

Note: the session was triggered by `/sc:analyze` + `/sc:improve`, not by explicitly invoking
`prompts/repo-coherence-check/prompt.md`. If this is considered a different workflow, the
run-log requirement technically does not apply. However, the intent of the run-log is to
maintain a baseline for the *next* run. The next coherence-check run will use the last
`end_commit` in the log (`4c5e7e4`) as its baseline — which is now stale by one large commit.
This will cause the next run to re-scan the entire diff from `4c5e7e4..HEAD`, including all
19 files changed here.

**Requested action:** Append a run-log record to `maintenance/run-log.md` either in this PR
or as an immediate follow-up commit, so the audit trail and next-run baseline remain accurate.

---

### Issue 4 (DOCUMENTATION — MINOR) — `.frontmatter-waivers` deletion not logged in `tools/readme.md`

**Spec clause:** AGENTS.md §Folder Management ("You MUST log that assumption in the relevant
folder's readme.md").

The `.frontmatter-waivers` file contained its own provenance: "This list was burned to zero
by Task 001 (refactor-governance-from-specs) on 2026-05-04." The PR body explains the
deletion, but the `tools/readme.md` was not updated to document it. PR body text is transient
documentation; `tools/readme.md` is the durable, on-disk record.

**Requested action:** Add a note to `tools/readme.md` documenting that `.frontmatter-waivers`
was removed, why, and when. One sentence is sufficient.

---

### Style Note (NOT a defect) — README.md in a governance-fix commit

Adding a README.md orientation paragraph is benign and the content is accurate. However, it
is a content improvement mixed into a governance-repair commit. Per the `repo-coherence-check`
prompt's commit format (which distinguishes T1/T2/T3 tiers), content improvements are at
minimum T2 — a different category from the linter fixes. This is a commit hygiene observation
only; it does not affect correctness.

---

## Verdict

**APPROVE WITH REQUESTS.**

The core mission (restore check-governance.sh to green, clarify spec semantics) is
accomplished correctly. Issues 1–4 are process conformance gaps that do not block merge
but SHOULD be resolved in an immediate follow-up commit or in the next maintenance session.
Issues 2 and 3 are the most significant: together they mean this session's substantial
changes are not fully traceable via the repository's own governance tooling.

| Issue | Severity | Blocks merge? | Suggested resolution |
|---|---|---|---|
| 1 — `repo-coherence-check` empty-string fields | Spec conformance | No | Update prompt.md to omit OPTIONAL fields |
| 2 — No Task for repair session | Audit gap | No | Retroactive Task or run-log exception note |
| 3 — No run-log entry | Protocol | No | Append run-log record in follow-up commit |
| 4 — `tools/readme.md` not updated | Documentation | No | One-line note in tools/readme.md |
| README.md scope creep | Style | No | None required |
