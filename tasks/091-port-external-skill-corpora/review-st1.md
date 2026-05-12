---
type: note
status: active
slug: task-091-st1-review
summary: "Peer review of PR #115 (Task 091 ST-1): Phase 1 corpus — 14 sc-* skills + skill_source validator. Two blocking issues: missing readme.md × 14 and incorrect T4 repair guidance in friction-log."
created: 2026-05-12
updated: 2026-05-12
---

# Review — PR #115 · Task 091 ST-1: Phase 1 Corpus

**Reviewer:** claude-sonnet-4-6  
**PR:** [#115](https://github.com/netzkontrast/agency/pull/115)  
**Branch:** `claude/execute-task-91-PI6hI` → `main`  
**Commit:** `680f24b`  
**Date:** 2026-05-12

---

## Verdict: CHANGES REQUESTED

The core deliverables (validator extension, 14 skill folders, sc-research adaptation) are
technically correct and governance passes. Two blocking issues prevent clean merge:

1. All 14 `skills/sc-*/` folders are **missing required `readme.md`** files.
2. The friction-log's remediation recommendation for `FL1.1` is **categorically wrong**
   under the repo's own T4-immutability rule: it proposes a T2 edit to an Accepted ADR,
   which is prohibited.

A third non-blocking issue (TA.1.4 unverifiable AC) is correctly logged but the subtask
file itself has not been updated to reflect the changed outcome; this creates silent divergence.

---

## What works

### Validator extension (`tools/fm/validate.py`)

The `_check_skill_source()` function is clean, well-scoped, and correctly hooks into the
existing `validate()` entry point alongside `_check_skill_bundles`. The constants:

```python
VENDOR_PREFIXES = ("sc-", "superpowers-")
SKILL_SOURCE_RE = re.compile(r"^(superclaude|superpowers)@v\d+\.\d+\.\d+$")
```

are forward-compatible with Phase 2 (Superpowers corpus). The renumber of F.B.7 → F.B.8 /
F.B.9 was the correct local decision — sharing a diagnostic code across two unrelated checks
would have made grep-triage impossible.

### Test coverage

6 tests in `tools/tests/fm/test_validate_skill_source.py`, all green:

```
6 passed in 0.27s
```

The sixth test (`test_superpowers_vendor_prefix_accepted`) is a bonus beyond the 5
required by the spec — a useful forward-compat regression guard. The sandbox pattern
(in-memory repo, canonical ontology mirrored from REPO) is consistent with the existing
test architecture.

### 14 skill folders — structure and frontmatter

All 14 `skills/sc-*/SKILL.md` files:

- carry `skill_source: "superclaude@v4.3.0"` (ADR-0011 D.2 ✓)
- validate clean via `python3 tools/fm/validate.py skills/sc-*/` (TA.1.1 ✓)
- have bodies ≤ 5 KB — largest observed is `sc-research` at 2455 B (BR.9.5 ✓)
- archive verbatim upstream body at `references/upstream-sc-<slug>.md` (ADR-0011 D.3 ✓)

The tier landing order (L1 leaves → L2 → L3/L4) matches the DAG in
`references/full-plan-part-4.md §10.6`.

### sc-research Agency adaptation (ADR-0011 D.8)

The body rewrite is correct:

- `## How to use` lists `WebSearch` + `WebFetch` as primary surface
- `Tavily` appears only in `## Compatibility` marked OPTIONAL
- Verbatim Tavily-first upstream body archived at
  `skills/sc-research/references/upstream-sc-research.md`

TA.1.3 satisfied. ✓

### Ontology + JSON-Schema mirror

`header-ontology.json` now documents `skill_source` in `skill.recommended_keys` with
the ADR-0011 anchor. The JSON-Schema mirror was regenerated. Governance exits 0. ✓

### Honest friction log

`tasks/091-port-external-skill-corpora/friction-log.md` is frank and specific about both
friction points — the code-clash forced renumber, and the unimplementable manifest AC.
The "what worked smoothly" section is also useful signal for future Epic implementers.

---

## Issue 1 (BLOCKING): Missing `readme.md` in all 14 `skills/sc-*/` folders

**Severity:** Blocking — violates MUST-level spec requirement.

**Evidence:**

```bash
$ for d in skills/sc-*/; do
    [ -f "${d}readme.md" ] && echo "${d}: ok" || echo "${d}: MISSING readme.md"
  done
skills/sc-backend-architect/: MISSING readme.md
skills/sc-createPR/: MISSING readme.md
skills/sc-deep-research-agent/: MISSING readme.md
skills/sc-frontend-architect/: MISSING readme.md
skills/sc-implement/: MISSING readme.md
skills/sc-improve/: MISSING readme.md
skills/sc-performance-engineer/: MISSING readme.md
skills/sc-pm-agent/: MISSING readme.md
skills/sc-quality-engineer/: MISSING readme.md
skills/sc-refactoring-expert/: MISSING readme.md
skills/sc-research/: MISSING readme.md
skills/sc-security-engineer/: MISSING readme.md
skills/sc-system-architect/: MISSING readme.md
skills/sc-test/: MISSING readme.md
```

**Spec basis:**

> SKILLS.md §2: canonical layout explicitly lists `readme.md # Directory index.` as a
> top-level entry (non-OPTIONAL, unlike `adapters/` and `references/` which are marked
> OPTIONAL).

> CLAUDE.md §7: "EVERY operational folder MUST contain a `readme.md`."

> SKILLS.md §9.6 — Readme Audit maps to `tools/lint-structure.py`; the linter does not
> currently enforce this for skill subfolders (see Observation 1 below), so governance
> exits 0 despite the violation. Passing the gate ≠ compliance.

**Comparison:** Every pre-existing native skill (e.g. `novel-architect/`, `dramatica-theory/`,
`prompt-optimizer/`) carries a `readme.md`. The 14 new `sc-*/` folders are the only ones in
the repo without it.

**Required repair (T1 — Mechanical):** Add a minimal `readme.md` to each of the 14 folders.
Each file SHOULD carry L1 Vault Core frontmatter (`type: index`) and contain:

1. What and Why — single paragraph linking to the upstream skill and ADR-0011
2. Linked Navigation — `SKILL.md`, `references/` subfolder, each upstream file
3. Assumptions Log — at minimum the literal `(none)` line (CLAUDE.md §7 sub-requirement)

A templated one-liner body is fine; the goal is navigation + assumption-log completeness,
not rich documentation.

---

## Issue 2 (BLOCKING): Friction-log FL1.1 recommends a T4-prohibited repair

**Severity:** Blocking — the friction log's own remediation path for FL1.1 violates the
repo's T4-immutability rule. If a downstream agent follows this recommendation it will
corrupt governance.

**What the friction log says (`tasks/091-port-external-skill-corpora/friction-log.md` line 26):**

> "A T2 follow-up (additive edit to the Accepted ADR's `## Acceptance Criteria` Gherkin block)
> should reconcile the code to `F.B.8` so the ADR's executable test matches the validator
> emit code."

**Why this is wrong:**

MAINTENANCE.md §1 Repair Tiers:

| Tier | Action |
|---|---|
| **T4** | Accepted ADRs — **T4-immutable**. MUST NOT touch. Supersede via a successor ADR. |

The T1/T2 repair allowance in MAINTENANCE.md §1.0.1 applies to *metadata-and-link repairs on
**closed research*** (`updated:` bumps, broken relative links) — not to the normative body of
an Accepted ADR. Editing the Acceptance Criteria Gherkin of ADR-0011 (even "additively") is a
**T4 edit** because it changes the normative record of what the ADR's acceptance test asserts.

**Correct remediation path:**

File a **new ADR** (e.g. `decisions/0012-skill-source-validator-diagnostic-codes.md`) with:
- `adr_status: Accepted`
- `adr_supersedes: []` (amendment, not supersession)
- Body: "ADR-0011 §10.2 referenced F.B.7/F.B.8; implementation used F.B.8/F.B.9 due to
  F.B.7 pre-existing use. This ADR ratifies F.B.8/F.B.9 as the authoritative code pair."

Alternatively: the ADR-0011 Gherkin block at anchor `ADR.11.2` states F.B.7 in `Then`
clauses. The diagnostic explanation registry (`maintenance/schemas/diagnostic-explanations.json`,
if it exists) may also need to be checked for the F.B.7 entry.

The friction log MUST be updated to reflect this correct path before ST-2 starts, otherwise
the ST-2 implementer will inherit a flawed repair recommendation and may follow it.

---

## Issue 3 (Non-blocking): TA.1.4 divergence undocumented in subtask spec

**Severity:** Advisory — not a merge-blocker, but creates silent spec drift.

AC `TA.1.4` in `tasks/091-port-external-skill-corpora/subtasks/01-phase-1-corpus.md` still reads
(verbatim from the design plan):

```gherkin
Given the 14 skill folders are committed
When the manifest is regenerated
Then the manifest entry for sc-system-architect MUST list referenced_by: [sc-implement]
And the manifest entry for sc-quality-engineer MUST list referenced_by: [sc-test, sc-improve]
```

The friction log correctly documents that this AC cannot be verified against the current
toolchain (no manifest emitter, `sync.sh --emit-manifest` does not exist). However the
subtask file itself is unchanged. A future reviewer reading the subtask file without the
friction log will see an unsatisfied MUST and incorrectly flag the deliverable as incomplete.

**Recommended repair:** Update `subtasks/01-phase-1-corpus.md` TA.1.4 to add a note:

```markdown
> **Status:** forward references correctly declared in YAML (derivable via `grep`); manifest
> emitter not yet implemented. See `friction-log.md FL1.2`. Manifest verification deferred to
> a follow-up Task per the two closure paths documented in the friction log.
```

This is a T2 additive edit to the subtask note — NOT an Accepted ADR body edit.

---

## Observation 1: SKILLS.md §9.6 Readme Audit not enforced by `tools/lint-structure.py`

**Severity:** Advisory — tooling debt, not a failure in this PR.

SKILLS.md §9.6 maps "Missing readme.md in skill folder" to `tools/lint-structure.py`, but the
linter does not actually check skill subfolders for readme.md (confirmed by running the linter
against the current state — 0 errors for any skill folder, despite 14 missing files). This
explains why governance exits 0 despite Issue 1.

A follow-up T2 commit to `tools/lint-structure.py` (or `tools/fm/validate.py` via `_check_skill_structure()`) should add the skill readme check so it is mechanically enforced.
This is out of scope for ST-1 but should be filed as a maintenance Task.

---

## Observation 2: `templates/skill.md` not extended with `skill_source` example

ADR-0011 §D.7 notes:

> "`templates/skill.md` MAY be extended in a follow-up T2 commit to show a `skill_source`
> commented-example line; not blocking on the first port."

The commit did not extend the template. This is explicitly non-blocking per ADR-0011, but a
follow-up T2 commit should add the commented example so future skill authors are not surprised
by the key.

---

## Checklist against TA.1.1–TA.1.4 and BR.9.*

| Criterion | Status | Notes |
|---|---|---|
| **TA.1.1** — 14 folders, valid SKILL.md, skill_source pin | ✅ | `python3 tools/fm/validate.py skills/sc-*/` → 0 diagnostics |
| **TA.1.2** — no regression on pre-existing skills | ✅ | `python3 tools/fm/validate.py skills/` → 35 files, 0 diagnostics |
| **TA.1.3** — sc-research Agency-adapted | ✅ | WebSearch primary; Tavily OPTIONAL; upstream archived |
| **TA.1.4** — manifest reciprocity | ⚠️ | Forward refs in YAML; manifest emitter absent — see FL1.2 |
| **BR.9.1** — 5 dangling refs resolve to local skill bodies | ✅ | sc-createPR, sc-implement, sc-test, sc-improve, sc-research all present |
| **BR.9.2** — AGENTS.md remote URL removed | 🔲 | ST-2 scope |
| **BR.9.3** — sc-research not Tavily-mandatory | ✅ | TA.1.3 ✓ |
| **BR.9.4** — audit graph reciprocity | ⚠️ | YAML correct; manifest layer absent (same as TA.1.4) |
| **BR.9.5** — T2 body cap ≤ 5 KB | ✅ | Max 2455 B (sc-research) |

---

## Summary of required actions before merging

| # | Severity | Action | File(s) |
|---|---|---|---|
| 1 | **Blocking** | Add `readme.md` to each of the 14 `skills/sc-*/` folders | `skills/sc-*/readme.md` (×14) |
| 2 | **Blocking** | Update `friction-log.md` FL1.1 to replace T2-edit recommendation with new-ADR path | `tasks/091-port-external-skill-corpora/friction-log.md` |
| 3 | Advisory | Add divergence note to TA.1.4 in subtask file | `tasks/091-port-external-skill-corpora/subtasks/01-phase-1-corpus.md` |
| 4 | Advisory | File T2 maintenance Task for SKILLS.md §9.6 linter gap | `tasks/readme.md` + new task |
