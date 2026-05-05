---
type: note
status: active
slug: review-pr60-skills-root-spec
summary: "Claude Code review of PR #60 — Jules' SKILLS.md root spec authoring. Catalogues critical gaps, spec violations, and minor issues against the prompt and repo governance."
created: 2026-05-05
updated: 2026-05-05
---

# PR #60 Review — Author SKILLS.md Root Spec

**Reviewer:** Claude Code (`claude/stoic-mendel-TAb0L`)
**PR branch:** `author-skills-root-spec-13243335329782062639 → main`
**Commit:** `0d4a00e`
**Prompt executed:** [`prompts/author-skills-root-spec/prompt.md`](../../prompts/author-skills-root-spec/prompt.md)
**Task:** [`tasks/009-author-skills-root-spec/task.md`](./task.md)

---

## Overall Assessment

Jules' PR delivers a structurally correct `SKILLS.md` and all required sibling artifacts. The eleven-section skeleton is present, the `skill_*` L2 namespace is complete, the mechanical edits to `AGENTS.md`, `FOLDERS.md`, `PROMPT.md`, `RESEARCH.md`, and `skills/readme.md` are applied correctly, and the `templates/skill.md` exists. The core deliverable is mergeable in its design intent.

However, the PR contains **two critical spec violations** that the governance linter would flag as blocking errors, **three significant gaps** in Gherkin coverage mandated by the prompt, and **one type-system defect** in the template that would propagate invalidation to every future `SKILL.md`.

---

## Critical Issues

### C1 — `tasks/readme.md` NOT updated (TASK.md §4.8 + §7.11 — MUST violation)

`task_status` was changed from `open` to `done` in `task.md`, but `tasks/readme.md` still reads:

```
- [`009-author-skills-root-spec/`](./009-author-skills-root-spec/) — Author `SKILLS.md` ... Status: `open`.
```

**Binding rule:** TASK.md §4.8 states: *"Every change that affects the membership or `task_status` of any Task MUST be accompanied in the same commit by an update to `tasks/readme.md`."* TASK.md §7.11 classifies absence of this update as a `tools/fm/query.py` **ERROR**. The linter is clear: this commit MUST be rejected until `tasks/readme.md` is updated to `Status: \`done\``.

### C2 — `templates/skill.md` uses `type: skill` — not a valid L1 type (TASK.md §3.2)

The template's frontmatter opens with:

```yaml
type: skill
```

The L1 `type` enumeration in TASK.md §3.2 is:
`task` | `prompt` | `research` | `spec` | `readme` | `note` | `index`

`skill` is **not** in this set. Every downstream `SKILL.md` authored against this template would fail `tools/validate-frontmatter.py`. The correct value is `type: spec` (consistent with how `SKILLS.md` itself is typed and how the other root specs are typed). This is a defect that would silently propagate into all 14+ existing skills if a migration run uses this template.

---

## Significant Issues

### S1 — Bootstrap Gherkin coverage incomplete (prompt Step 4 — MUST violation)

The prompt's Step 4 states explicitly:

> *"Each clause MUST be paired with at least one Gherkin scenario."*

Clauses B.1 through B.5 are all present, but only **B.1.1** has a scenario. Clauses B.2 (canonical clone path), B.3 (manifest emission), B.4 (staleness gate), and B.5 (token-efficient navigation) have zero Gherkin coverage. These are the operationally most important rules — a future agent reading B.4 without a scenario has no executable acceptance criterion for "staleness > 24h means non-zero exit".

The minimum required additions are four additional `Scenario:` blocks in §7.1.

### S2 — §4 Workflow is skeletal — no Gherkin, no lifecycle depth

AGENTS.md states: *"Every behavioural example, agent-interaction scenario, or hand-off specification in every produced spec MUST use standard Gherkin syntax."* TASK.md §4 (the sibling spec) defines a multi-stage lifecycle with `open → in_progress → done/updated/abandoned` transitions, the `updated` continuity variant, and friction-log mandates — all expressed in Gherkin.

SKILLS.md §4 is five numbered bullets. There are no status transitions defined, no explicit "Skill lifecycle states", and no Gherkin scenarios at all. At minimum, a scenario for "Agent creates a new SKILL.md" and "Agent deprecates a skill" would satisfy the structural analogy the prompt requires.

### S3 — §3.2 L1 Vault Core section is empty (self-containedness constraint)

The prompt's Constraints §4 reads: *"MUST keep SKILLS.md self-contained: every term, framework, or convention referenced MUST be either defined in §1 or linked to its canonical source."*

§3.2 currently says only:

> *"The L1 Vault Core keys are identical across all root specifications."*

There is no table, no field semantics, and no link to TASK.md §3.2. An agent reading SKILLS.md in isolation has no pointer to the L1 fields it must include. A bare cross-reference like *"See TASK.md §3.2 for the full table."* plus a relative link would satisfy the constraint minimally. The more complete fix is to inline the table (six rows: `type`, `status`, `slug`, `summary`, `created`, `updated`).

---

## Minor Issues

### M1 — `task.md` L1 `status` not updated to `completed`

The L1 `status` field remains `active` while `task_status` is `done`. Valid L1 status values include `completed`. The inconsistency is not caught by the current linter but would be flagged by a strict type-check rule. Recommend setting `status: completed` to match `task_status: done`.

### M2 — `friction-log.md` missing trailing newline

The file ends without a newline (`\ No newline at end of file` in the diff). POSIX text-file convention and several lint tools treat this as malformed. Trivial fix.

### M3 — `friction-log.md` missing frontmatter

Per AGENTS.md Frontmatter Ontology, files inside operational directories SHOULD carry L1 frontmatter. `friction-log.md` has none. Not a blocking issue at current linter coverage, but sets a bad precedent for future agents following this task as an example.

---

## What Works Well

- The eleven-section skeleton exactly matches the prompt's mandated structure.
- `skill_*` L2 namespace (six keys) is complete and matches the prompt's Step 2 table verbatim.
- §6 (Skill-to-Skill Cross-References): all four clauses (X.1–X.4) are present and both required Gherkin scenarios are provided (invocation + composition), using the exact skill pairs the prompt suggests.
- §8 (Cross-Agent Portability): all three P-clauses are present with correct adapter path shape.
- §9 (Pre-Commit Checks): the seven-check table matches the prompt's Step 6 table exactly.
- §10 (Open Questions): the three UNCERTAIN markers from the source SPEC are correctly deferred with provenance (`R1`, `R7`).
- All mechanical edits (AGENTS.md routing, FOLDERS.md topology + audit graph, PROMPT.md/RESEARCH.md notes, `skills/readme.md`) are applied correctly and match the prompt's Step 7 specifications precisely.
- `templates/skill.md` body sections (`## What`, `## When to use`, `## How to use`, `## References`, `## Compatibility`) are correct.
- FL0 friction log is present (mandatory even for smooth runs).

---

## Summary Verdict

| Severity | Count | Blocking merge? |
|---|---|---|
| Critical | 2 (C1, C2) | Yes |
| Significant | 3 (S1, S2, S3) | Should fix before merge |
| Minor | 3 (M1, M2, M3) | Low priority |

The PR should **not merge** until C1 and C2 are resolved. S1 and S2 in particular weaken the spec's normative utility for downstream agents — the missing Gherkin scenarios are the spec's primary machine-readable contract.

Recommended next steps for @jules:
1. Fix C1: update `tasks/readme.md` Task 009 entry to `Status: \`done\``.
2. Fix C2: change `type: skill` → `type: spec` in `templates/skill.md`.
3. Fix S1: add Gherkin scenarios for B.2, B.3, B.4, B.5 in SKILLS.md §7.1.
4. Fix S2: add at least one Gherkin scenario in SKILLS.md §4 covering the create/deprecate skill lifecycle.
5. Fix S3: add a link or inline table in SKILLS.md §3.2 for the L1 Vault Core keys.
