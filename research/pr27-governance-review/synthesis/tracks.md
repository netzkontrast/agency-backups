---
type: note
status: active
slug: pr27-governance-review
summary: "Per-cluster findings that feed output/REVIEW.md."
created: 2026-05-04
updated: 2026-05-04
---

# Analysis Tracks

## Track 1 — Linkage Fixes (tools/lint-linkage.py, 5 prompts, task.md)

- **Finding T1.1 (CORRECT):** `research_slug_resolves()` correctly expands slug resolution to
  provider subfolders. The prior implementation was a genuine linter bug; the fix is minimal
  and correctly scoped.
- **Finding T1.2 (CORRECT):** Dropping `prompt_relates_to_task` from follow-up prompts that
  have no adopting Task is semantically correct per PROMPT.md §6.6.
- **Finding T1.3 (ISSUE):** `task_spawns_research: []` in tasks/003 is functionally correct
  (linter accepts it) but creates an ambiguous "empty list vs. absent key" signal. The PR
  updates TASK.md §3 to describe `prompt_spawned_from_research` as OPTIONAL, but `task_spawns_research`
  is an L2 key whose presence/absence semantics are not clarified. Minor.

## Track 2 — Spec Drift Reconciliation (TASK.md, PROMPT.md, AGENTS.md)

- **Finding T2.1 (CORRECT):** TASK.md §2 change (friction-log MANDATORY for done/abandoned) is
  consistent with existing `lint-linkage.py:133` enforcement. The spec now matches its own linter.
- **Finding T2.2 (CORRECT):** TASK.md §7.7 change aligns the spec with enforcement already in
  `check-trust.py`. No behavioural regression.
- **Finding T2.3 (ISSUE — SELF-REFERENTIAL):** PROMPT.md §3 now specifies that OPTIONAL fields
  (`prompt_relates_to_task`, `prompt_spawned_from_research`) should be OMITTED when not applicable.
  Yet `prompts/repo-coherence-check/prompt.md` (lines 11-12 in the working tree) still carries
  `prompt_relates_to_task: ""` and `prompt_spawned_from_research: ""` — empty strings that the
  new convention explicitly deprecates. The validator no longer requires these keys, so the
  inconsistency passes automated checks silently. The most prominent operational prompt in the
  repo violates the convention the PR just introduced.
- **Finding T2.4 (CORRECT):** AGENTS.md L1 table change (lowercasing "should" in a descriptive
  cell) correctly applies RFC 2119 rule R2. The cell is rationale text, not a normative sentence.

## Track 3 — DRY Refactor (tools/_frontmatter.py + 4 linters)

- **Finding T3.1 (CORRECT):** The two parse-mode design (`strict=True` for validator,
  `strict=False` for downstream linters) is architecturally sound. The validator gates on
  malformed input; downstream tools trust the gate.
- **Finding T3.2 (CORRECT):** Python `sys.path` concern is a non-issue. `python3 tools/X.py`
  adds `tools/` to `sys.path`, so `from _frontmatter import` resolves correctly when called
  via `check-governance.sh`.
- **Finding T3.3 (CORRECT):** Removing `load_waivers()` and `.frontmatter-waivers` is justified
  since the waiver list was burned to zero by Task 001. The removal eliminates dead code.
- **Finding T3.4 (ISSUE — UNDOCUMENTED DELETION):** The `.frontmatter-waivers` file contained
  its own provenance comment ("burned to zero by Task 001 on 2026-05-04"). That explanation is
  now only in the PR body. Per AGENTS.md §Folder Management: "You MUST log that assumption in
  the relevant folder's readme.md." The `tools/readme.md` was not updated to document the
  deletion. The assumption is preserved in a transient PR body, not in the repo's own
  decentralized documentation.

## Track 4 — Friction Log Retrofit (tasks/002, tasks/003)

- **Finding T4.1 (CORRECT):** The retroactive friction logs are properly filed and correctly
  cite their provenance ("extracted from inline … verbatim" / "reconstructed in retrospect").
- **Finding T4.2 (CORRECT):** FL declarations in both logs are reasonable (FL1) and consistent
  with the events described.

## Track 5 — Audit Graph Integrity (AGENTS.md CR.5, run-log)

- **Finding T5.1 (ISSUE — GOVERNANCE GAP):** AGENTS.md CR.5 requires the PR body to reference
  "the closed Task slug(s) under /tasks/ if any". The PR cites tasks/002 and tasks/003 as
  "Closed Task slugs" but neither task was the primary driver of *this* session's work. The
  actual session work (15 linter errors fixed, DRY refactor, spec reconciliation) has no
  corresponding Task in `/tasks/`. This is the governance-of-governance gap: the governance
  repair itself is un-tasked.
- **Finding T5.2 (ISSUE — RUN LOG):** Per `prompts/repo-coherence-check/prompt.md` Step 6,
  every coherence-class repair run MUST append a record to `maintenance/run-log.md`. No such
  entry appears in the PR diff. The last entry in `maintenance/run-log.md` is from jules
  (2026-05-04). This session's repairs are not traceable via the run-log audit trail.

## Track 6 — Housekeeping (README.md, .gitignore)

- **Finding T6.1 (STYLE):** README.md expansion is out-of-scope for a governance-fix commit.
  The change is benign and accurate, but mixing a content improvement with a governance repair
  muddies the commit history. Not a defect; a style concern.
- **Finding T6.2 (CORRECT):** `.gitignore` additions (`__pycache__/`, `*.pyc`, `.agent_cache/`)
  are appropriate and were a genuine gap.
