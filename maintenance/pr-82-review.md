---
type: note
status: active
slug: pr-82-review
summary: "Code review for PR #82 — Task 034 close (prompt-spec-integration) + Task 049 filing. One critical folder-index omission, one critical decision-tree logic defect, two moderate gaps, two minor inconsistencies."
created: 2026-05-07
updated: 2026-05-07
---

# Code Review — PR #82: Close Task 034 (prompt-spec-integration); file Task 049 successor

**PR:** [#82 Close Task 034 (prompt-spec-integration); file Task 049 successor](https://github.com/netzkontrast/agency/pull/82)
**Branch:** `claude/close-prompt-spec-integration-bLV3Z` → `main`
**Head commit:** `02b54d5`
**Reviewer:** claude-code (session `claude/brave-darwin-74YJm`)
**Date:** 2026-05-07

---

## § RFC 2119

The key words MUST, MUST NOT, SHOULD, and MAY in this document are to be
interpreted as described in RFC 2119 when, and only when, they appear in all
capitals.

---

## Summary Verdict

A substantial, well-tested delivery: 27 unit tests pass, corpus runs confirm
the expected 0/72 self-containedness hit-rate and 1/72 framework-declaration
WARN, PROMPT.md §4.3 now has a machine-readable decision tree, and nine Gherkin
scenarios (P.B.1–P.B.6 plus three variant suffixes) anchor every pre-commit
check. Task 049 is cleanly filed as the successor with an Assumptions Log that
correctly documents the subprocess-composition architecture.

**Two issues require fixes before merge:**

- R-1 (CRITICAL) — `tools/readme.md` was not updated. Neither
  `check-prompt-self-containedness.py` nor `check-prompt-framework-declaration.py`
  appear in the `## Contents` section, making both tools invisible to agents
  scanning the folder index. Identical class of defect to PR #79 R-2.
- R-2 (CRITICAL) — The §4.3 framework-selection decision tree is logically
  broken: the Q3 (RISE-DX) branch is unreachable. Q1's "No" arc routes
  directly to Q4, bypassing Q3. No path through the tree can produce
  `RISE-DX`. Any agent following the tree will never select that framework.

Two moderate gaps and two minor inconsistencies are non-blocking but SHOULD
be addressed in-branch or immediately post-merge.

---

## Positive Findings

### P-1 — Test Coverage is Thorough and Authentic

Both linters ship real `tempfile`-backed tests via `importlib.util.spec_from_file_location`
— 17 for self-containedness, 10 for framework declaration, totalling 27 passing
tests. The corpus regression commands in the PR test-plan are reproducible and
the expected outcomes (0/72 and 1/72 respectively) are cited with exact slug
names, enabling future bisection.

### P-2 — SPEC §2 FPR Methodology Is Reproducible

The `research/prompt-engineering-principle-mechanizability/output/SPEC.md` §2
documents the corpus size (N=72), the stratified sample construction (n=15,
seed=7, 15 slug-prefix buckets), the exact `find` command, the triage Python
snippet, and the explicit sample-power caveat for P.5.1's 0/0 hit count. Future
agents can re-run the measurement mechanically.

### P-3 — False-Positive Suppression is Well-Scoped

Both linters skip YAML frontmatter, fenced code blocks (triple-backtick and
triple-tilde per the refactor commit), and blockquote lines. The suppression
rules are documented in each script header. The refactor commit (`c9e3535`)
correctly adds OSError handling parity and the tilde-fence test before closing.

### P-4 — Import Mechanism Upgraded Over PR #79 Pattern

Unlike the PR #79 linters that used bare `import _core` after a raw
`sys.path.insert`, both new linters use the fully-qualified
`from tools.fm._core import …` form with a guarded `sys.path.insert`
(`if str(_REPO_ROOT) not in sys.path`). This prevents duplicate-path
contamination in the test suite and is the correct pattern.

### P-5 — Task 049 Successor Filed Cleanly

Task 049 carries a well-scoped Goal, correct `task_status: open`,
`task_owner: unassigned`, and a substantive four-item Assumptions Log.
The subprocess-composition decision (keeping ST-2 + ST-3 as independent
CLIs rather than in-process imports) is explicitly documented and is the
right architectural call.

### P-6 — Chore Commit Clears Pre-Existing Governance Noise

`02b54d5` fixes the Task 031 friction-log FL form and the
tasks 045 / 046 index-drift in a single, clearly-labelled chore commit,
providing a clean governance baseline for this PR's substantive changes.

---

## Critical Findings

### R-1 (CRITICAL) — `tools/readme.md` Does Not List the Two New Linters

**Location:** `tools/readme.md`, `## Contents` section.

**Symptom.** `tools/readme.md` was not modified in any commit in this PR.
Its `## Contents` section currently lists four tools:

```
validate-frontmatter.py
check-narrative-ontology-load.py
check-rfc2119-polarity.py
check-assumption-log.py
```

The PR ships `check-prompt-self-containedness.py` and
`check-prompt-framework-declaration.py` directly into `/tools/` but neither
appears in the index.

**Rule violated.** FOLDERS.md §3: "EVERY folder MUST contain a `readme.md`
that lists every file/subfolder via relative Markdown links." Both new linters
are invisible to any agent scanning the folder index.

**Impact.** An agent looking for "the self-containedness pre-commit linter"
will find no entry in `tools/readme.md`. It may conclude the tool does not
exist and either (a) author a duplicate or (b) skip the check. This is the
exact failure mode documented for PR #79 R-2 (which was CRITICAL and blocked
that merge).

Note: `README.md §6` WAS correctly updated with two rows for the new tools
(commit `75f72f4`), but `README.md` is the repo-level surface; `tools/readme.md`
is the folder-local index. Both MUST be updated per FOLDERS.md §3.

**Required fix.** Add two entries to `tools/readme.md` `## Contents`, following
the format of the existing entries. The `updated:` frontmatter date MUST be
bumped to `2026-05-07`. Example:

```md
- [`check-prompt-self-containedness.py`](./check-prompt-self-containedness.py) — WARN-tier (exit 2). Detects external-context phrases in `/prompts/<slug>/prompt.md` per PROMPT.md §5.1 / §6.4. Phrase list: 8 canonical forms. False-positive suppression: frontmatter, fenced code blocks, blockquotes. (Task 034 ST-2.)
- [`check-prompt-framework-declaration.py`](./check-prompt-framework-declaration.py) — WARN-tier (exit 2). Verifies `prompt_framework` ∈ canonical set (`RISEN`, `RISE-DX`, `ReAct`, `RISEN+ReAct`, `CoT`), `## Framework` section presence, frontmatter↔section consistency, and ≥10-word rationale per PROMPT.md §5.2 / §6.4.b. (Task 034 ST-3.)
```

---

### R-2 (CRITICAL) — §4.3 Decision Tree: Q3 (RISE-DX) Is Unreachable

**Location:** `PROMPT.md`, §4.3 "Framework-Selection Decision Tree".

**Symptom.** The tree routes as follows:

```
Q1 (iterative tool use?) → Yes → Q2 → RISEN+ReAct or ReAct
                         → No  → Q4 → RISEN or CoT
```

Q3 (agentic-spine / RISE-DX) appears in the ASCII art as a sibling of Q2 and
Q4, but Q1's "No" branch explicitly routes to Q4 — there is no arc that enters
Q3. The Q3 node is a dead branch. An agent following the tree can never reach
`RISE-DX`.

**Evidence.** The tree text at §4.3:

```
├── Q1. …
│     ├── Yes → Q2.
│     └── No  → Q4.        ← skips Q3 entirely
│
├── Q2. …
│     ├── Yes → choose `RISEN+ReAct`.
│     └── No  → choose `ReAct`.
│
├── Q3. Does the prompt belong to the agentic-spine …?   ← unreachable
│     ├── Yes → choose `RISE-DX`.
│     └── No  → fall through to Q4.
│
└── Q4. …
```

**Rule violated.** PROMPT.md §4 (Framework-Selection is a MUST-apply
decision procedure); AGENTS.md R4 (spec statements MUST carry a stable ID
allowing agents to resolve the procedure unambiguously).

**Impact.** Every agent authoring a RISE-DX prompt (agentic-spine,
reflection-driven spec) will select RISEN+ReAct or ReAct instead, because
Q3 is never entered. The existing 2 RISE-DX prompts in the corpus are
protected only by their pre-existing frontmatter; any new prompt authored
against this tree will never declare RISE-DX.

**Likely intended routing.** Based on the "fall through to Q4" phrase in Q3's
"No" branch, the intended tree is:

```
Q1 (iterative?) → Yes → Q2 (structured up-front?)
                           → Yes → Q3 (agentic-spine?)
                                     → Yes → RISE-DX
                                     → No  → RISEN+ReAct
                           → No  → ReAct
               → No  → Q4 (single-shot artefact?)
                           → Yes → RISEN
                           → No  → CoT
```

**Required fix.** Rewrite the §4.3 decision tree so Q3 is reachable.
The ASCII art and the prose section MUST be consistent. The mechanical gate
`check-prompt-framework-declaration.py` does not validate the decision tree
itself, so this is a pure spec-document fix.

---

## Moderate Findings

### R-3 (MODERATE) — Research `readme.md` Missing `research_executes_prompt`

**Location:** `research/prompt-engineering-principle-mechanizability/readme.md`
frontmatter.

**Symptom.** The newly added research readme carries:

```yaml
research_phase: complete
research_friction_level: FL0
```

but is missing `research_executes_prompt`.

**Rule violated.** TASK.md §3.3: "Research namespace (mandatory in
`/research/<slug>/output/SPEC.md` and `readme.md`)." All three keys —
`research_phase`, `research_executes_prompt`, `research_friction_level` — are
mandatory on both files. `output/SPEC.md` carries all three correctly
(`research_executes_prompt: research-prompt-engineering-principle-mechanizability`);
the root `readme.md` omits the middle key.

**Impact.** An agent reading the readme to determine which prompt produced this
research workspace will find no `research_executes_prompt` pointer and must
either scan `output/SPEC.md` or guess. The audit trail from prompt → research
is broken at the readme level.

**SHOULD fix.** Add `research_executes_prompt: research-prompt-engineering-principle-mechanizability`
to `readme.md` frontmatter, between `research_phase` and `research_friction_level`.

---

### R-4 (MODERATE) — No `ImportError` Guard on `tools.fm._core` Import

**Location:**
- `tools/check-prompt-self-containedness.py:54`
- `tools/check-prompt-framework-declaration.py:41-44`

**Symptom.** Both linters import `tools.fm._core` via a top-level module
import after a guarded `sys.path.insert`. If `tools/fm/_core.py` is absent
(e.g., during the two-toolchain migration window referenced in MAINTENANCE.md §2,
or in a shallow checkout), both scripts crash with an unhandled `ImportError`
rather than degrading gracefully.

**Improvement over PR #79.** These linters correctly use the fully-qualified
`tools.fm._core` form and the guarded path-insert pattern; PR #79 R-3 and
R-4 do not apply here. However, neither script wraps the import in
`try/except ImportError`.

**Impact.** `check-governance.sh` calls both linters via `|| true`, masking
the crash. The advisory checks silently become no-ops rather than producing
an actionable diagnostic. An operator relying on these WARN-tier gates to
catch self-containedness or framework-mismatch violations receives no signal.

**SHOULD fix.** Wrap the import in a `try/except ImportError` block and emit
a one-line stderr diagnostic before `raise SystemExit(0)`:

```python
try:
    from tools.fm._core import split_frontmatter_and_body  # or the relevant names
except ImportError:
    import sys as _sys
    print(
        "check-prompt-self-containedness: tools/fm/_core.py not importable — "
        "skipping (advisory linter, exit 0).",
        file=_sys.stderr,
    )
    raise SystemExit(0)
```

---

## Minor Findings

### M-1 (MINOR) — Research Friction Log Uses Old FL Form

**Location:** `research/prompt-engineering-principle-mechanizability/reflection/friction-log.md`, FL Declaration section.

**Symptom.** The friction log declares `**FL: 0**` (colon-space form). The
`02b54d5` chore commit in this same PR fixes the identical pattern in
Task 031's friction-log: `**FL: 1**` → `**FL1**`. The newly introduced
friction log perpetuates the form that was just corrected elsewhere.

**SHOULD fix.** Change `**FL: 0**` to `**FL0**` for consistency with the
canonical form enforced by the Task 044 F14 mitigation in this very PR.

---

### M-2 (MINOR) — `P.B.5.provider` Anchor Collides with RFC-2119 Namespace

**Location:** `PROMPT.md` §6.9 Gherkin block, scenario anchors.

**Symptom.** `# anchor: P.B.5` labels the RFC-2119 keyword-count scenario
(maps to principle §5.3). `# anchor: P.B.5.provider` labels the §6.5
backward-link-through-provider scenario. The `.provider` suffix creates a
false implication that the provider scenario is a sub-variant of the RFC-2119
check, when it is actually an independent §6 gate (backward-link resolution).

The PR body states: "anchors P.B.1..P.B.6 mirror the §6 pre-commit-check
namespace". §6.5 = Backward Link Resolves, which is the parent check for
the `.provider` scenario. A less ambiguous anchor would be `P.B.6.5.provider`
or `P.B.3.provider` (since P.B.3 = follow-up filing, and §6.5 governs the
backward-link that P.B.3 posts).

**SHOULD fix.** Rename the anchor to avoid the RFC-2119 namespace collision.
Any consistent alternative is acceptable; the key constraint is that the
anchor MUST NOT share a prefix with an unrelated check.

---

## Action Items

| Finding | Severity | Fix Target | Blocks merge? |
|---------|----------|------------|---------------|
| R-1: `tools/readme.md` missing 2 linters | Critical | Fix in-branch before merge | YES |
| R-2: §4.3 decision tree Q3 unreachable | Critical | Fix in-branch before merge | YES |
| R-3: `readme.md` missing `research_executes_prompt` | Moderate | Fix in-branch; trivial one-liner | SHOULD fix in-branch |
| R-4: No `ImportError` guard on `_core` import | Moderate | File Task or fix here | No |
| M-1: Research friction log old FL form | Minor | One-char edit | No |
| M-2: `P.B.5.provider` anchor namespace collision | Minor | Rename anchor | No |

---

## Conclusion

Merge is **conditional on R-1 and R-2**. R-1 is a one-file folder-index edit;
R-2 requires a targeted rewrite of the §4.3 ASCII tree and the Q1 routing
prose, but does not affect any linter logic or test suite. Both are in-branch
fixes that take < 15 minutes combined. R-3 is a single-field frontmatter
addition and SHOULD be absorbed while the branch is open. R-4 mirrors the
PR #79 R-3 pattern and SHOULD be addressed via a follow-up Task (or here,
given the branch is already open). The core work — 27 passing tests, accurate
FPR empirics, well-structured PROMPT.md §6.9 scenarios, clean Task 049 filing
— is solid and ready to land once the two blocking items are resolved.

> **@jules** — R-2 warrants a quick look before any future RISE-DX prompt is
> authored: the decision tree as merged would silently steer all agentic-spine
> prompts to RISEN+ReAct instead of RISE-DX. R-1 repeats the PR #79 R-2
> pattern; the fix is the same one-file index update.
