---
type: note
status: active
slug: task-041-pr72-review
summary: "Post-merge code review of PR #72 (Task 041 — extract 35 subtask briefs to /prompts/<slug>/). Documents four findings: invalid `type: brief` across 40 files, empty-string OPTIONAL fields in 44 prompts, shallow RISEN+ReAct migration in S-sections, and unclaimed task_owner."
created: 2026-05-06
updated: 2026-05-06
---

# PR #72 — Code Review: Task 041 Extract Subtask Prompts

**Reviewer:** Claude Code (session claude/brave-darwin-AZvTs)
**PR:** https://github.com/netzkontrast/agency/pull/72
**Branch reviewed:** `claude/execute-close-task-41-87B8n` @ `ecb1919`
**Scope:** PROMPT.md §3, AGENTS.md Frontmatter Ontology §L1, TASK.md §6

---

## Summary

The extraction of 35 subtask execution briefs into `/prompts/<slug>/` folder triples
is structurally complete: governance passes (0 diagnostics on 370 files), the three-file
scaffold is present everywhere, `task_uses_prompts ↔ prompt_relates_to_task` reciprocity
is verified, and the slug-manifest decision is well-reasoned. The work closes the
audit-graph debt identified in PR #70 C.3.

Four findings follow, ordered by severity. Findings **F-A** and **F-B** are specification
violations that survive into the corpus undetected because the validator's
`path_classification` table and its OPTIONAL-field handling create a blind spot.
Findings **F-C** and **F-D** are quality concerns that do not block merge but should
inform the next maintenance pass.

---

## F-A — CRITICAL: `type: brief` is not a valid Frontmatter Ontology type (40 files)

### What

Every `brief.md` produced by `scripts/extract.py` carries `type: brief` in its
YAML frontmatter. The L1 Vault Core ontology defines a **closed enum** of valid
type values:

```
task | prompt | research | spec | readme | note | index | skill | adr
```

(`maintenance/schemas/header-ontology.json` → `"type_values"` key; canonically
restated in `AGENTS.md §Frontmatter Ontology` and `TASK.md §3.2`.)

`brief` is not in this set. All 40 `brief.md` files therefore carry an
**invalid type declaration**.

### Why it passed the linter

`tools/fm/validate.py --type-check` enforces the `type_values` enum only for
files that match a rule in `path_classification.rules`. That table contains a
rule for `prompts/*/prompt.md` and `prompts/*/readme.md`, but **no rule for
`prompts/*/brief.md`**. Files without a matching rule return
`Classification(expected_type=None)` — they are outside the validator's scope
and the type-value check is skipped entirely.

The 370-file, 0-diagnostic pass cited in the PR test plan is therefore correct
but does not certify the `brief.md` files.

### Impact

- Any future tool that reads `type:` to route files (e.g. an Obsidian graph
  query, a corpus-wide `fm/query.py type=note` sweep) will either skip or
  misroute these 40 files.
- The `header-ontology.json` `type_values` invariant is silently violated in
  production, making it untrustworthy as a schema source.

### Recommended fix

Option A (minimal): Change all 40 `brief.md` files to `type: note`. `note` is
the closest valid type for contextual documentation that does not fit
`task`/`prompt`/`research`. This can be done in one pass:

```bash
find prompts/*/brief.md -exec sed -i 's/^type: brief$/type: note/' {} +
```

Option B (additive): File a spec-amendment to add `brief` to the closed enum
in `header-ontology.json` + `AGENTS.md §Frontmatter Ontology` + `TASK.md §3.2`,
and add a `path_classification` rule for `prompts/*/brief.md`. This is the
correct long-term fix if `brief.md` is a first-class artifact type.

Option C (belt-and-suspenders): Do Option A now and file Option B as a follow-up
Task so the type is properly canonicalised. This avoids corpus drift while
deferring the ontology extension decision.

---

## F-B — `prompt_spawned_from_research: ""` should be omitted, not empty-string (44 files)

### What

44 `prompt.md` files carry:

```yaml
prompt_spawned_from_research: ""
```

`PROMPT.md §3` declares this field **OPTIONAL**: "only when a Task already lists
this prompt" / "OPTIONAL: research that produced this prompt as a follow-up."
The spec's intent for optional fields that don't apply is **omission**, not an
empty-string sentinel.

The template `templates/prompt.md` itself has `prompt_spawned_from_research: ""`
as a placeholder — `scripts/extract.py` faithfully propagated this placeholder
into all 35 newly extracted prompts (plus 9 pre-existing prompts that inherited it
from the same template).

### Why it matters

1. `tools/lint-linkage.py` resolves `prompt_spawned_from_research` values. If it
   ever strict-validates optional fields (checking that non-empty values resolve
   to existing research slugs), the current code that skips empty strings would
   become a gap.
2. Tools that query `fm/query.py prompt_spawned_from_research=<slug>` to traverse
   the research-spawn lineage graph will silently enumerate these 44 files as
   having an unresolvable parent rather than no parent.
3. It signals that the template has a latent bug that will recur with every future
   prompt authored from `templates/prompt.md`.

### Recommended fix

Remove the `prompt_spawned_from_research: ""` line from every affected `prompt.md`
(35 new + 9 pre-existing). Fix the template simultaneously:

```bash
sed -i '/^prompt_spawned_from_research: ""$/d' prompts/*/prompt.md templates/prompt.md
```

---

## F-C — RISEN+ReAct migration is shallow: `## S — Steps` wraps the original brief verbatim

### What

PROMPT.md §5 requires every prompt to satisfy **Self-Containedness**, **Framework
Declaration**, and **RFC 2119 Normativity** — meaning the RISEN+ReAct `S — Steps`
section MUST contain organised, RFC-2119-normative steps that an executor can
follow without external context.

All 35 extracted `prompt.md` files implement `## S — Steps` as:

```markdown
1. Execute the following instruction block faithfully — it is the verbatim
   Execution Brief from the parent subtask file:

   ```text
   [original inline execution brief, copied verbatim]
   ```
2. Verify every Acceptance Criterion in [`brief.md`](./brief.md) is satisfied...
3. Run `tools/check-governance.sh` and resolve every ERROR before committing.
```

Step 1 is not a RISEN-native step — it is a pass-through wrapper around the
original pre-extraction brief text. The content was migrated in structure only
(moved from subtask file to prompt file), not in form (not decomposed into
RISEN+ReAct steps). The verbatim code block inside the prompt re-introduces the
very opacity the RISEN framework is meant to remove.

### Impact

An executing agent reads Step 1 and encounters an unstructured prose block with
no RFC 2119 keywords, no discrete deliverable per step, and no failure-handling
rule — violating PROMPT.md §5 items 3 (RFC 2119 Normativity), 4 (Deliverable
Lock), and 7 (Failure Handling) for the inline content.

### Recommended fix

This is the highest-effort remediation. For each prompt, expand the verbatim
code block into numbered RISEN-native steps (one deliverable per step, one RFC
2119 keyword per sentence). Given 35 prompts, this work is best scoped as a
follow-up Task rather than a fix to this PR. The current state is better than
the pre-extraction state (content is at least in the right file) but is a
partial migration.

---

## F-D — `task_owner: "unassigned"` on a closed task; `task_uses_prompts: []` on Task 041 itself

### task_owner

`tasks/041-extract-subtask-prompts/task.md` closes with `task_status: done` but
`task_owner: "unassigned"`. TASK.md §6 Gherkin "Agent picks up an open Task"
requires:

> Then the agent MUST set "task_owner" to its identifier

The executing agent never claimed the task by updating `task_owner`. For audit
purposes (who produced this extraction?), the owner field should name the agent
that ran `scripts/extract.py` and committed `ecb1919`.

### task_uses_prompts: []

Task 041 closes the audit-graph debt of tasks that inline their prompts rather
than linking to them — yet Task 041 itself carries `task_uses_prompts: []`.
The extraction was driven by `tasks/041-extract-subtask-prompts/scripts/extract.py`
using `tasks/041-extract-subtask-prompts/task.md` as its own spec, with no
`/prompts/extract-subtask-prompts/prompt.md` in existence.

This is not a spec violation (TASK.md allows `task_uses_prompts` to be empty
for coordination tasks with no external instruction set). It is an irony that
the policy-enforcement task exempt itself from the policy it enforces, and worth
noting for the next coherence pass.

---

## Unchecked test plan item

The PR test plan leaves one item unchecked:

```
[ ] Reviewer sanity-check: spot-read 2-3 generated prompts (one research,
    one tooling, one spec-amendment) for content fidelity vs the corresponding
    pre-extraction subtask body.
```

This review constitutes that sanity-check. Three prompts were read:
- `prompts/research-adr-corpus-extraction/prompt.md` (research)
- `prompts/tooling-duplicate-task-id-linter/prompt.md` (tooling)
- `prompts/spec-amendment-agents-md/prompt.md` (spec-amendment)

Content fidelity is **high**: all Goal, Falsification, Inputs, Acceptance
Criteria, Dependencies, and Effort sections are preserved in `brief.md`; the
`## E — Expectations` section accurately mirrors the acceptance criteria; the
`## Constraints` section correctly transcribes dependencies and falsification.
The shallow-migration concern (F-C) is a structural critique, not a content-loss
finding.

---

## Disposition

| Finding | Severity | Blocks merge? | Recommended action |
|---|---|---|---|
| F-A: `type: brief` invalid | HIGH | No — linter blind spot means no current failure, but corpus correctness is impaired | Fix in a follow-up commit or immediate patch |
| F-B: `prompt_spawned_from_research: ""` | MEDIUM | No | One-liner sed pass; fix template simultaneously |
| F-C: Shallow RISEN migration | MEDIUM | No | File follow-up Task for proper RISEN decomposition |
| F-D: `task_owner` + `task_uses_prompts` on 041 | LOW | No | Set `task_owner` in a follow-up commit; note irony in 041's closure |

The PR may merge as-is given that the primary deliverable (audit-graph repair,
reciprocity verified, governance green) is satisfied. The four findings above
SHOULD be addressed in a follow-up pass before the downstream Tasks 032–039 are
dispatched, because F-A and F-B affect the integrity of the prompt corpus that
those tasks will consume.
