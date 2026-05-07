---
type: spec
status: completed
slug: pre-commit-readme-update-cadence-spec
summary: "Token-cost analysis of three readme-update cadence options, ratifies batched-at-pre-commit, and provides byte-identical drop-in wording for PRE_COMMIT.md §2 and FRUSTRATED.md §28."
created: 2026-05-07
updated: 2026-05-07
---

# SPEC — Pre-Commit Readme-Update Cadence

## §1 Token-Cost Comparison (≥3 cadence options)

The repository governs four operational layers (Tasks, Prompts, Research, Skills); each touched folder MUST carry an updated `readme.md`. A typical merged feature PR on `main` lands ≈30 file changes spanning ≈10 distinct operational folders (sample: PR #87, PR #88, PR #89). Mean readme size ≈150 tokens (operational readmes are short by spec — title, contents block, assumptions log, frontmatter).

| Option | Cadence | Tokens reloaded per 30-file PR | Multiplier vs. status quo |
|---|---|---|---|
| **A — Per-touch (immediate)** | Update the relevant `readme.md` in the same commit as the file change that triggers it. | 30 × ~150 ≈ **4 500** | ≈3.0× |
| **B — Batched-at-pre-commit** ⭐ | Hold all readme updates until the pre-commit phase; then update every touched-folder `readme.md` as a single staged group right before `git commit`. | 10 × ~150 ≈ **1 500** | 1.0× (status quo) |
| **C — Hybrid** | Per-touch on substantive folder-purpose changes (e.g., a new `task.md` or `SKILL.md`); batched on incidental touches. | (5 × ~150) + (10 × ~150) ≈ **2 250** | ≈1.5× |

**Empirical control.** A `git log --since='2026-04-15' --name-only origin/main` survey of the 35 most recent commits found **zero** commits performing per-file readme-only sequencing for organic feature work; the heavy-readme commits (top quartile: 9–33 readme touches each) are uniformly batched. The corpus norm therefore already implements Option B.

**Falsification clause.** The prompt brief defined the wrong choice as "any cadence yielding >2× token cost vs. status quo". Status quo is Option B (1.0×); Option A is 3.0× (over the 2× threshold — wrong); Option C is 1.5× (under threshold but still dominated by B); Option B is by definition 1.0× (right). The clause did not fire.

## §2 Normative Rule

The **batched-at-pre-commit** cadence is canonical. Stated in RFC 2119 form for spec adoption:

> Every operational folder (under `/tasks/`, `/prompts/`, `/research/`, `/skills/`) whose contents change during a session MUST have its `readme.md` updated as part of a single batched audit performed during the pre-commit phase. The agent MUST NOT create a per-file commit whose only purpose is to update an adjacent `readme.md`. The agent MAY iterate the staged readme content during the pre-commit phase before producing the commit, but the readme update MUST land in the same commit as the file changes that triggered it.

This rule is consistent with `MAINTENANCE.md` §3.2 (static metadata is reconciled at session boundaries, not per-file) and with the corpus norm.

## §3 Drop-In Wording (byte-identical, modulo spec-name prefix)

The two amendments below MUST land byte-for-byte identical (see [Task 062 B-1](../../../tasks/062-frustrated-spec-followup-ac1-ac5/task.md) for the diff-test contract). The only permitted divergence is the spec-name prefix line (`PRE_COMMIT.md §2 — Readme Cadence` vs. `FRUSTRATED.md §28 — Readme Cadence`); the body paragraph is locked.

```
**Readme Cadence (canonical, batched-at-pre-commit).** Every operational folder
(under `/tasks/`, `/prompts/`, `/research/`, `/skills/`) whose contents change
during a session MUST have its `readme.md` updated as part of a single batched
audit performed during the pre-commit phase. The agent MUST NOT create a
per-file commit whose only purpose is to update an adjacent `readme.md`. The
agent MAY iterate the staged readme content during the pre-commit phase before
producing the commit, but the readme update MUST land in the same commit as
the file changes that triggered it. Per-file readme spam is FL2 bloat per
FRUSTRATED.md §FL.Special.
```

## §4 Walkthrough — PR #88 (Task 035 close, 2026-05-07)

PR #88 (`feat(task-035): close research-spec-integration`, commit `45c17fa`) landed 25 files spanning 7 operational folders (`tasks/035-…/`, `prompts/research-spec-integration/`, `research/research-spec-integration/`, plus four touched-by-side-effect task readmes for cross-references). Under Rule §2:

- The agent did NOT make 25 per-file commits; it landed one batched commit. ✓
- Each touched operational folder's `readme.md` was updated in the same commit as the substantive file change. ✓
- The pre-commit phase re-ran `tools/check-readme-frontmatter.py` to confirm L1 conformance on all 7 readmes; no per-file iteration. ✓

The rule yields the expected behaviour on the corpus exemplar. The same reasoning applies to PR #87 (Task 038), PR #89 (Task 036), and PR #85 (Tasks 051+052).

## §5 Acceptance

Subtask ST-1 acceptance criteria from [`prompts/research-pre-commit-readme-update-cadence/brief.md`](../../../prompts/research-pre-commit-readme-update-cadence/brief.md):

| AC | Met? | Evidence |
|---|---|---|
| 1. SPEC.md at `/research/pre-commit-readme-update-cadence/output/SPEC.md` | ✓ | this file |
| 2. §1 token-cost comparison covers ≥3 cadence choices | ✓ | three rows (A, B, C) |
| 3. §2 normative rule unambiguous and consistent with MAINTENANCE.md §3.2 | ✓ | §2; references §3.2 |
| 4. §3 contains drop-in wording for FRUSTRATED.md §28 AND PRE_COMMIT.md §2 | ✓ | §3 (one paragraph, both consumers) |
| 5. §4 walkthrough on a recent session shows the rule yields expected behaviour | ✓ | PR #88 walkthrough |
| 6. `research_phase: complete`; reflection friction-log | ✓ | `../readme.md` and `../reflection/friction-log.md` |
