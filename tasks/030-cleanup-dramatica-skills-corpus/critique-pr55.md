---
type: note
status: active
slug: critique-pr55-cleanup-dramatica-skills
summary: "Structured code-review critique of PR #55 (Task 030 — cleanup-dramatica-skills-corpus). Two critical findings (over-blocking + incomplete subtask dependency graph), two significant findings, four minor findings. Overall: strong plan; C1 and C2 block safe Phase-A dispatch."
created: 2026-05-05
updated: 2026-05-05
---

# PR #55 — Code-Review Critique

**PR:** `claude/cleanup-dramatica-skills-1cEOO → main`  
**Title:** `plan(dramatica): Task 030 cleanup-corpus + nine /sc:agent subtasks`  
**Reviewer:** claude-sonnet-4-6 (session `claude/stoic-mendel-DFH4X`)  
**Grade:** ✅ APPROVE WITH REQUESTS — two critical gaps must be resolved before Phase A dispatches.

---

## Summary

Task 030 is a well-scoped Phase-0 maintenance plan. The baseline measurements are concrete and verifiable (§notes.md §2), the falsification clauses per subtask are honest, the Gherkin acceptance gates are valid, and the meta-frustration log (FE-1…FE-10) is exactly the pattern-surfacing raw material Task 029 needs. The PR body is thorough and the governance linters are green.

Two findings are critical — they would cause a dispatching agent to behave incorrectly without human intervention.

---

## Critical Findings

### C1 — `task_blocked_by: ["028"]` over-blocks Phase A

**File:** `tasks/030-cleanup-dramatica-skills-corpus/task.md` (frontmatter, line 17–18)

The frontmatter sets `task_blocked_by: ["028"]` at the whole-task level. This prevents ANY subtask from dispatching until Task 028 (ADR tooling — `agency-adr` CLI) ships. But Phase A is entirely independent of `agency-adr`:

| Subtask | agency-adr needed? |
|---|---|
| ST-1 strip-pdf-artifacts | No — pure regex deletion on markdown |
| ST-2 fix-corrupted-headings | No — prose editing |
| ST-3 fix-anchor-mismatches | No — ontology pointer repair |
| ST-4 resolve-empty-redirects | No — alias/delete decision |
| **ST-5 build-term-editor** | **Yes — `term.py deprecate` files schema-bump requests as ADRs** |
| **ST-6 build-cleanup-linter** | **Yes — `cleanup.py` routes lint-rule additions through ADR records** |
| ST-7 bulk-alias-loader | No — synonym file parsing |
| ST-8 scenario-tag-coverage | No — tagging loop |
| ST-9 precompile-encoding-hints | No — JSON generation |

Only ST-5 and ST-6 have a real dependency on Task 028. The `task_blocked_by` field on the parent task currently serialises all nine subtasks behind the ADR tooling work, which is unnecessary.

**Impact:** An operator following TASK.md §8.7 (no `open → in_progress` transition while blockers are `task_status ≠ done`) will hold all nine subtasks idle until Task 028 ships. Phase A's low-risk, high-value cleanup is delayed with no benefit.

**Recommended fix (two options):**

_Option A (minimal change):_ Set `task_blocked_by: []` on task.md. Move the Task-028 dependency to ST-5 and ST-6's `subtask_depends_on` field explicitly (e.g., `subtask_depends_on: ["task-028"]`). Document the rationale in A-4 or a new assumption entry A-11.

_Option B (stronger):_ Split Task 030 into two halves:
- Task 030a (Phase A, unblocked): ST-1…ST-4 + ST-7.
- Task 030b (Phase B+C, blocked by `["028", "030a"]`): ST-5, ST-6, ST-8, ST-9.

Option A is lower-friction; Option B has a cleaner audit graph.

---

### C2 — Phase dependency ordering is prose-only; subtask frontmatter encodes it incorrectly

**Files:** `tasks/030-cleanup-dramatica-skills-corpus/subtasks/05-build-term-editor.md`, `06-build-cleanup-linter.md`, `07-bulk-alias-loader.md` (Phase B); `08-scenario-tag-coverage.md`, `09-precompile-encoding-hints.md` (Phase C)

`task.md §Plan` states:
- "Phase B — Tooling Extensions (**parallel, depends on Phase A merging**)"
- "Phase C — Content Coverage (**sequential, depends on Phase B**)"

But the subtask frontmatter disagrees:

| Subtask | Phase | `subtask_depends_on` (actual) | Expected |
|---|---|---|---|
| ST-5 | B | `[]` | `["ST-1","ST-2","ST-3","ST-4"]` |
| ST-6 | B | `[]` | `["ST-1","ST-2","ST-3","ST-4"]` |
| ST-7 | B | `[]` | `["ST-1","ST-2","ST-3","ST-4"]` |
| ST-8 | C | `["ST-1","ST-2","ST-3"]` | + `["ST-5","ST-6","ST-7"]` |
| ST-9 | C | `["ST-1","ST-2","ST-3"]` | + `["ST-5","ST-6","ST-7"]` |

A dispatcher agent reading only the subtask files (which is the documented self-contained contract per PROMPT.md §5 rule 1) would conclude all nine subtasks are independently dispatchable and fan them out in parallel. Phase B tools would run concurrently with Phase A cleanup, meaning `term.py` and `cleanup.py` would be built against a corrupted corpus — the opposite of what the task intends.

The `subtask_phase` field alone is not machine-checkable without a phase-ordering spec that currently doesn't exist (FE-1, FE-2). The `subtask_depends_on` field is the machine-checkable fallback and is currently wrong for six of the nine subtasks.

**Recommended fix:** Before Phase A dispatches, update the six affected subtask files:

```yaml
# ST-5, ST-6, ST-7 — add Phase A deps
subtask_depends_on:
  - "ST-1"
  - "ST-2"
  - "ST-3"
  - "ST-4"

# ST-8 — add Phase B deps (keeping existing Phase A deps)
subtask_depends_on:
  - "ST-1"
  - "ST-2"
  - "ST-3"
  - "ST-5"
  - "ST-6"
  - "ST-7"

# ST-9 — same
subtask_depends_on:
  - "ST-1"
  - "ST-2"
  - "ST-3"
  - "ST-5"
  - "ST-6"
  - "ST-7"
```

---

## Significant Findings

### S1 — YAML comment in `subtask_depends_on` of ST-3 is a parsing hazard

**File:** `tasks/030-cleanup-dramatica-skills-corpus/subtasks/03-fix-anchor-mismatches.md` (frontmatter)

```yaml
subtask_depends_on:
  - "ST-2"  # via commit body — ST-3 needs ST-2's coordination note for character-dynamic.approach
```

YAML comments survive most parsers but are stripped silently — they cannot be read back programmatically. More importantly, `tools/validate-frontmatter.py` and `tools/lint-linkage.py` do not test for them, so this information is invisible to tooling. The rationale ("ST-3 needs ST-2's coordination note") should be in the prose body of `03-fix-anchor-mismatches.md` under a **Dependencies** section, not in a frontmatter comment.

**Recommended fix:** Move the comment text to the prose `## Dependencies` section of the file. Keep frontmatter as data-only:
```yaml
subtask_depends_on:
  - "ST-2"
```

---

### S2 — `notes.md §FE-5` "Workaround" describes a state that was not applied

**File:** `tasks/030-cleanup-dramatica-skills-corpus/notes.md` (§FE-5, "Workaround" paragraph)

FE-5's workaround writes: "Set Task 030's `task_spawns_prompts: ['agency-adr-governance-spec']` (it spawned the prompt while planning)". But the actual `task.md` has `task_spawns_prompts: []`, and the PR body explicitly confirms "No spawned prompts on this branch." The workaround describes a decision that was revised between writing the notes and writing the final frontmatter.

This creates a false-negative for a future agent auditing FE-5: the workaround text implies the field was set, but it wasn't. FE-5 and FE-9 together already expose the underlying schema ambiguity; the incorrect workaround text adds confusion on top.

**Recommended fix:** Amend the FE-5 "Workaround" paragraph to reflect the final decision:
> "Final decision: `task_spawns_prompts: []` because the prompt is owned by `main` and was authored outside this branch's scope. The FE-5 schema question remains open for Task 029."

---

## Minor Findings

### M1 — `subtask_status` absent from all subtask frontmatter

The FE-1 "Suggested rule" proposes `subtask_status` as part of the L2.1 namespace. All nine subtask files carry only the L1 `status: draft` field. Without `subtask_status`, a coherence-check agent scanning for in-progress work has no way to distinguish a subtask that is actively being executed from one that hasn't started yet. The lifecycle gap is real now, not hypothetical. Adding `subtask_status: not-started` to all nine files costs one line each and closes the gap without waiting for Task 029 to ratify.

---

### M2 — `subtask_depends_on: null` vs `[]` inconsistency

`ST-3`, `ST-8`, `ST-9` use the YAML scalar-null form (bare `subtask_depends_on:` with a list on the next line). `ST-1`, `ST-2`, `ST-4`, `ST-5`, `ST-6`, `ST-7` use `subtask_depends_on: []`. Both are valid YAML but produce different types when parsed (`list` vs. `null` in PyYAML). `tools/validate-frontmatter.py` may not catch this if it only tests for field presence. Standardise on `subtask_depends_on: []` for empty lists throughout.

---

### M3 — `task.md §Plan` references `tools/dramatica-nav/deprecate.py` but §Goal item 3 and ST-5's CLI surface do not include `deprecate.py` as a separate script

`task.md §Goal item 3` lists five scripts: `term.py`, `aliases.py`, `cleanup.py`, `precompile.py`, `deprecate.py`. But ST-5's CLI surface for `term.py` already includes `term.py deprecate` as a subcommand. If `deprecate.py` is a separate script, ST-5's scope must explicitly include it; if it's a `term.py deprecate` subcommand alias, then `deprecate.py` in the §Goal item 3 list is misleading. The acceptance gate `Scenario CL.1.4` references `deprecate.py` as a standalone path, which would fail if the implementation puts deprecation inside `term.py` only.

**Recommended fix:** Clarify in §Goal item 3 whether `deprecate.py` is a thin wrapper (`#!/usr/bin/env python3\nfrom term import deprecate_cmd…`) or a duplicate CLI surface. Update `CL.1.4` accordingly.

---

### M4 — Gherkin scenario `CL.1.5` token-cost gate uses bytes, not tokens

```gherkin
Then the precompiled path MUST consume ≤60% of the bytes the prose-only path consumes
```

The §Goal item 4 rationale talks about "Token cost" and "≈1 KB target". The Gherkin gate measures **bytes**. In practice, bytes ≈ tokens for plain ASCII prose, but the mismatch could cause debate at gate time. Consider either (a) harmonising the prose to say "bytes" consistently, or (b) replacing the Gherkin gate with a token-count measure using `tiktoken` or similar (already a potential dependency under `tools/requirements.txt`).

---

## Positive Observations (do not change)

1. **Baseline numbers are concrete and verifiable.** §notes.md §2 gives exact grep commands and per-file hit counts. This is exactly the right level of specificity for a falsifiable acceptance gate.

2. **Falsification clauses are honest.** Every subtask's falsification clause identifies a specific condition that would invalidate the cut. ST-1's "load-bearing copyright footer" and ST-4's "historic German author search" concerns are non-obvious; surfacing them before dispatch is sound engineering.

3. **FE-1…FE-10 are high-quality pattern inputs.** The meta-frustration log correctly separates planning-session friction from execution friction (the separate `friction-log.md`). FE-3 (readme drift), FE-6 (undocumented `/sc:*` lifecycle), and FE-8 (ratification loop) are the three most systemically useful entries for Task 029.

4. **`task_blocked_by` dependency chain is auditable.** Even if C1's over-blocking is a problem, the declared dependency on `["028"]` is at least visible. A maintainer can unblock explicitly. Compare this to a task that silently assumes agency-adr is available without any declared dependency.

5. **Anti-Patterns section is normative and binding.** The copyright-respect rule (no >1 line of Dramatica prose), the prohibition on new `kind:` values without an ADR, and the PROVISIONAL convention warning are all correctly framed as `MUST NOT` rules, not suggestions.

6. **Subtask agent-prompt blocks are self-contained.** ST-1's agent-prompt block includes repo root, file paths, acceptance criteria by reference, and constraint list. A fresh subagent can act on it without reading any other file. This satisfies PROMPT.md §5 rule 1.

---

## Summary of Requests

| ID | Severity | File | Request |
|---|---|---|---|
| C1 | Critical | `task.md` | Move `task_blocked_by` to subtask level for ST-5/ST-6 only; unblock Phase A |
| C2 | Critical | `subtasks/05…07*.md`, `08…09*.md` | Fix `subtask_depends_on` to encode phase ordering |
| S1 | Significant | `subtasks/03-fix-anchor-mismatches.md` | Move YAML comment to prose body |
| S2 | Significant | `notes.md §FE-5` | Correct workaround text to match final state |
| M1 | Minor | All subtask files | Add `subtask_status: not-started` |
| M2 | Minor | All subtask files | Normalise `subtask_depends_on: []` vs null |
| M3 | Minor | `task.md §Goal item 3` + `CL.1.4` | Clarify `deprecate.py` vs `term.py deprecate` |
| M4 | Minor | `task.md §CL.1.5` | Harmonise bytes vs. tokens |

C1 and C2 MUST be resolved before Phase A dispatches. S1, S2, M1–M4 SHOULD be resolved at the same time; they don't block merge.
