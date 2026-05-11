---
type: note
status: active
slug: review-pr28-readme-spec
summary: "Governance and quality review of PR #28 — detailed root README with self-update spec (commit 57dbae9). Identifies the R.13 self-referential violation, missing audit-graph artifacts, and non-conforming inline frontmatter."
created: 2026-05-04
updated: 2026-05-04
---

# PR #28 Review — `docs(readme): write detailed root README with self-update spec`

**Reviewed commit:** `57dbae940ce22c3b61f4e856118bec34b3ee3909`
**Branch:** `claude/add-readme-and-spec-erhmH → main`
**Reviewer:** Claude Code (session `claude/stoic-mendel-a7wVu`)
**Date:** 2026-05-04

---

## Executive Summary

The README content is well-crafted and serves the repository correctly — the
Machine/Actor/Space framing is articulate, §10 is accurate, and the §11
self-update spec is a genuine governance improvement. However, the *process* by
which this work was produced contains a self-referential governance violation
(R.13), is missing mandatory audit-graph artifacts (Task, Prompt, brief), and
carries a non-conforming inline YAML block (§11 frontmatter). These must be
addressed or explicitly waived before merge.

**Recommendation:** Request changes — specifically a retroactive Task entry and
an inline frontmatter correction. The content itself is approve-able.

---

## 1. Critical Finding: R.13 Self-Contradiction

README §11.4 R.13 states:

> "A non-trivial restructure of this README (adding or removing a top-level
> numbered section) MUST be performed via a Task in `/tasks/<NNN>-<slug>/` per
> TASK.md. It MUST NOT be performed inline as a 'drive-by' edit during another
> Task. The Task's `task_affects_paths` MUST list `README.md`."

This commit is precisely such a non-trivial restructure: it transforms a 2-line
stub into a 270-line document with 11 numbered sections and a normative spec
(§11). No Task was created.

The PR body acknowledges this: "this work was a single docs commit triggered by
a direct user request, not a /tasks/ orchestration entry." This is not an
exception clause — it is a description of exactly what R.13 prohibits.

**The violation is self-referential.** The agent wrote R.13 and simultaneously
violated it. The spec came into existence in the same commit that broke it.

**Why this matters beyond process formality:**
- `task_affects_paths` creates an auditable change surface for future agents.
- The Todo checklist in `task.md` is the only durable record of whether all
  seven test plan items in the PR body were verified by the author.
- Without a Task, the audit graph is broken at the highest-value link (the
  README is the entry point for every agent).

**Resolution required:**
Create a retroactive Task (e.g., `/tasks/009-document-readme-spec/`) with
`task_affects_paths: [README.md]` and close it as `done` in the same or a
follow-up commit. This satisfies R.13 retroactively and preserves the audit
trail.

---

## 2. Missing Audit-Graph Artifacts

The AGENTS.md routing table maps every work request to one of three layers:
orchestration (Task), instruction (Prompt), or execution (Research). This
commit produces a file of type `spec` (per §11 frontmatter) but has no
corresponding entry in any operational directory.

**Missing:**
- No `/prompts/<slug>/brief.md` — there is no immutable record of the original
  user request. PROMPT.md §1 requires this for any instruction-set authoring.
- No `/prompts/<slug>/prompt.md` — no framework declaration, no RFC 2119
  normativity in the instruction itself.
- No `/tasks/<NNN>-<slug>/task.md` — see Finding 1.

The PR body says the work was a "direct user request." Per PROMPT.md §4.2,
even direct requests MUST be saved into `brief.md` as the immutable record of
what was asked. The session link (`claude.ai/code/session_…`) is not a
substitute — it is ephemeral.

**Resolution:** At minimum, file a stub prompt under `/prompts/write-root-readme/`
with `brief.md` containing the original user request and `prompt.md` with
`prompt_kind: general`. This preserves traceability without requiring a full
RISEN/RISE-DX prompt.

---

## 3. Pre-Commit Gate: 15 Pre-Existing Errors

The PR author discloses 15 pre-existing errors (13 `lint-linkage` + 2
`check-trust`). This transparency is commendable. However:

**CR.3 (AGENTS.md):** "The agent MUST NOT invoke `/sc:createPR` if pre-commit
checks failed or were skipped."

The author's pragmatic argument is reasonable — the errors pre-date this branch
and are not introduced by it. But the correct governance mechanism for this
exception is `tools/.frontmatter-waivers` (or a dedicated "baseline waivers"
section in `tools/check-governance.sh`), not a prose disclosure in the PR body.

**What the PR should have done instead:**
1. Created a waiver entry in `tools/.frontmatter-waivers` covering the 15
   pre-existing paths, with rationale ("pre-existing on main; tracked in
   Task 00X").
2. Created a follow-up Task (open, P1) for resolving the 15 errors. The PR body
   says "the upstream baseline cleanup belongs in a follow-up Task" but does not
   actually create one — leaving the intent undocumented in the task graph.

Note: this reviewer (Task 009) does not itself create that follow-up Task, as
doing so would exceed the scope of a review. It is flagged here for the PR
author or merge approver to action.

---

## 4. Non-Conforming Inline Frontmatter Block (§11)

README §11 contains this YAML code block:

```yaml
---
type: spec
status: active
slug: readme-update-spec
scope: README.md (repository root, this file only)
---
```

Three issues:

**4a. `scope` is not in the ontology.**
The Frontmatter Ontology (AGENTS.md, TASK.md §3) defines L0, L1, and L2
namespaces. `scope` appears in none of them. Introducing it without extending
the ontology creates an undocumented key that future validators may flag as
unknown.

**4b. Missing mandatory L1 fields.**
L1 Vault Core requires: `type`, `status`, `slug`, `summary`, `created`,
`updated`. The inline block has `type`, `status`, `slug`, and `scope` — but
lacks `summary`, `created`, and `updated`.

**4c. R.15 is immediately un-fulfillable.**
R.15 states: "Every commit that modifies this README MUST update the `updated:`
field of any frontmatter blocks contained in this section to today's ISO-8601
date."

Because the inline block has no `updated:` field, R.15 cannot be satisfied by
any future commit. An agent following R.15 literally will look for `updated:` in
the §11 block, find none, and either hallucinate a compliance claim or error out.

**Resolution options (in order of preference):**
1. Add `summary`, `created`, `updated` to the inline block and remove `scope`.
2. Explicitly label the block as a documentation example ("This is illustrative
   only — this README's actual frontmatter is in the file header, not here.")
   and remove the `---` delimiters to prevent parser confusion.
3. Move the spec metadata to the file's actual YAML frontmatter (the README
   does not currently carry any frontmatter at its head).

---

## 5. §4 Topology: `.githooks/` Missing from Exemption Discussion

The topology tree correctly lists `.githooks/`. However, the prose below it
states: "The four **non-operational** directories (`/tools/`, `/templates/`,
`/maintenance/`, `/skills/`) are explicit exemptions enumerated in FOLDERS.md
§8."

`.githooks/` is a fifth non-operational exempt directory. It is in the tree but
not in the exemption count ("four"). This is a minor inaccuracy that would be
caught by R.11 if a future commit adds `.githooks/` to the FOLDERS.md §8
exemption list and then the prose here is not updated.

**Resolution:** Change "four" to "five" and add `.githooks/` to the
parenthetical list.

---

## 6. What the Agent Did Well

- **Content quality:** The Machine/Actor/Space framing is explained clearly and
  is internally consistent with the existing root specs. No normative content
  is duplicated (satisfying R.2).
- **RFC 2119 compliance in §11:** Each normative sentence carries exactly one
  keyword (satisfying AGENTS.md R1).
- **Gherkin validity:** Scenarios RM.1.1–RM.1.4 each carry at least one Given,
  one When, and one Then; `And` is never used as an opener (satisfying G1, G2).
  Anchors are present (G5). Scenarios are self-contained (G3, G4).
- **R.x identifier stability:** R.10 commits to never renumbering. This is
  the right call — stable identifiers prevent cross-reference rot.
- **Transparent pre-commit disclosure:** Disclosing 15 pre-existing errors in
  the PR body rather than silently ignoring them sets the right precedent.
- **§11 as a meta-governance innovation:** The idea of a self-update spec for
  the README is valuable and fills a real gap. The implementation just needs
  the process fixes above.

---

## 7. Summary of Required Actions

| Severity | Finding | Resolution |
|---|---|---|
| **MUST** | R.13 violation — no Task for non-trivial restructure | Create retroactive Task with `task_affects_paths: [README.md]` |
| **MUST** | Missing brief.md for original user request | Create stub prompt under `/prompts/write-root-readme/` |
| **MUST** | §11 inline frontmatter missing `summary`, `created`, `updated` | Add missing L1 fields; remove undefined `scope` key |
| **MUST** | R.15 un-fulfillable (no `updated:` in §11 block) | Fix inline frontmatter or label as illustrative |
| **SHOULD** | Pre-existing 15 errors not in waivers | Add entries to `tools/.frontmatter-waivers` + open follow-up Task |
| **SHOULD** | "four" non-operational directories in §4 prose (is five) | Change to "five", add `.githooks/` to list |

---

## Frustration Log (this review session)

**Highest Frustration Level: FL1**

The review itself was clear. The FL1 comes from the fact that there is no
formal "review a PR" workflow in the repository governance specs (AGENTS.md,
TASK.md, PROMPT.md, RESEARCH.md, RESEARCH.md). A PR review falls between the
cracks of the Machine/Actor/Space tripartite model — it is neither orchestration,
instruction authoring, nor research execution in the strict sense. This reviewer
had to improvise a Task (this one) to give the review artifact a proper home,
which is itself a minor governance gap worth noting for the next coherence run.
