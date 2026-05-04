---
type: research
status: active
slug: pr-21-mandate-review-output
summary: "Critical review of PR #21: 8 findings across Gherkin coverage, anchor numbering, scope creep, and enforcement blind spots in the /sc:createPR mandate."
created: 2026-05-04
updated: 2026-05-04
research_executes_prompt: ""
research_relates_to_task: refactor-governance-from-specs
research_output_kind: review
research_confidence: high
---

# Code Review — PR #21: Governance Linters + `/sc:createPR` Mandate

**Reviewed by:** Claude Code (session stoic-mendel-hNRGr)  
**Date:** 2026-05-04  
**Scope:** All three commits on branch `claude/execute-next-task-8BVif`:
- `5698ac7` — `feat(task-001)`: linters, pre-commit, templates  
- `9b2e080` — `docs(governance)`: bind root specs to enforcement  
- `f7e6efe` — `docs(agents)`: `/sc:createPR` mandate  

**Original executing prompt:** [`/prompts/refactor-governance-from-specs/prompt.md`](../../prompts/refactor-governance-from-specs/prompt.md)

---

## Summary Verdict

The linter suite and pre-commit hook (commits 1–2) are solid, well-structured, and correctly bind to the three source specs. The `/sc:createPR` mandate (commit 3, `f7e6efe`) contains **8 findings** — two of which are `MUST`-level spec violations against the repo's own language spec. The mandate should not merge as-is without addressing findings F1 and F2.

---

## Findings

### F1 — MUST-level: Incomplete Gherkin Coverage (G6 violation)

**Severity:** High  
**Clause violated:** `AGENTS.md §Gherkin Validity Rules G6`: "Acceptance criteria in this repository MUST be written as Gherkin scenarios."

Rules CR.2, CR.4, and CR.5 have **no corresponding Gherkin scenarios**:

- **CR.2**: The "no-op confirmation" path (an existing PR already covers the push) has no scenario.
- **CR.4**: The `/sc:createPR` errors-out path ("MUST be reported to the user") has no scenario.
- **CR.5**: The PR body content check ("MUST reference closed Task slug(s) and the FL declaration") has no scenario.

The two scenarios that do exist (`CR.1.1`, `CR.1.2`) cover only CR.1 and half of CR.3. A reader cannot verify CR.2, CR.4, or CR.5 without additional documentation that does not exist.

**Recommended fix:** Add three Gherkin scenarios, one per missing rule. Suggested anchors: `CR.2.1`, `CR.4.1`, `CR.5.1`.

---

### F2 — MUST-level: Anchor Numbering Violates R3

**Severity:** High  
**Clause violated:** `AGENTS.md §Usage Rules R3`: "Each normative statement SHOULD be addressable by a stable identifier of the form `<Spec-Letter>.<Section>.<Index>`."

The two Gherkin anchors are `CR.1.1` and `CR.1.2`. However:
- Scenario `CR.1.1` tests rule CR.1 ✓ (correct)
- Scenario `CR.1.2` tests rule **CR.3** (pre-commit failure blocks PR creation) ✗

`CR.1.2` implies it is the second scenario for rule CR.1, but it is actually the only scenario for CR.3. This creates ambiguous cross-referencing: a future agent or linter cannot tell which normative rule `CR.1.2` is verifying.

**Recommended fix:** Rename `# anchor: CR.1.2` → `# anchor: CR.3.1`.

---

### F3 — SHOULD-level: Scope Creep Without Prompt Amendment

**Severity:** Medium  
**Reference:** `PROMPT.md §5`: deliverables must be locked; `PROMPT.md §1.4`: task-specs are instruction sets executed by an agent.

The executing prompt (`/prompts/refactor-governance-from-specs/prompt.md`) enumerates concrete deliverables in its `E — Expectations` block:
- `tools/lint-frontmatter.{sh,py}`
- `tools/lint-structure.{sh,py}`
- `tools/lint-linkage.{sh,py}`
- `.githooks/pre-commit`
- `templates/task.md`, `templates/prompt.md`, `templates/research-readme.md`
- Updates to `PRE_COMMIT.md`
- Continuity-hook artifacts (Spec-G/H/I)
- Trust-audit script (Spec-J/K/L)

**AGENTS.md additions are not listed.** Commit 3 is out-of-prompt-scope work. The correct protocol per `PROMPT.md §4.5` ("if a source spec is missing or unparseable, file a follow-up prompt") extends to scope: out-of-scope changes SHOULD be filed as a new task-spec prompt, not bundled silently into the executing run.

The friction-log.md for Task 001 does not mention this scope extension, so there is no documented rationale for why this was added.

**Recommended fix:** Either (a) amend the prompt retrospectively to include the AGENTS.md deliverable, or (b) file a follow-up prompt documenting the Closing Run Procedure change as its own scope.

---

### F4 — SHOULD-level: Jules/Gemini Exemption Without Reference

**Severity:** Medium

The text reads: "It applies to Claude Code only; Jules and Gemini agents follow their own platform conventions."

This is normatively empty. A Jules agent reading AGENTS.md cannot determine what it is required to do at session end. No link to a Jules-specific closing procedure is provided. If Jules and Gemini operate under different rules, those rules MUST either be cited inline or linked to a canonical document.

The LOOP_LOG in AGENTS.md shows Jules as an active agent in this repository (Iterations 0–5). This omission affects a real agent operating on this codebase today.

**Recommended fix:** Add a link: "See `tasks/002-*/task.md` [or similar]" — or explicitly state "no closing procedure is currently defined for Jules/Gemini; this is a known gap."

---

### F5 — SHOULD-level: CR.3 Has No Mechanical Enforcement

**Severity:** Medium

CR.3: "The agent MUST NOT invoke `/sc:createPR` if pre-commit checks failed or were skipped."

The Gherkin scenario for CR.3 (`CR.1.2`) relies on an agent *self-reporting* that `tools/check-governance.sh` exited non-zero. But:
- An agent using `git commit --no-verify` silently bypasses the pre-commit hook.
- No linter or tool in the newly added toolchain detects whether the last commit was made with `--no-verify`.

The existing `tools/check-governance.sh` does not check commit history for hook-bypass flags. CR.3 is therefore a normative rule with no mechanical enforcement path — it depends entirely on agent honesty.

**Recommended fix:** Document this as a known limitation in `PRE_COMMIT.md §enforcement`. Alternatively, add a check to `tools/check-trust.py` that warns when a commit message lacks the governance-run signature.

---

### F6 — MAY-level: CR.2 References Undefined Skill Behavior

**Severity:** Low

CR.2: "…until `/sc:createPR` has either (a) opened a new pull request, or (b) returned an **explicit no-op confirmation** that an existing PR already covers the pushed commits."

The behavior of `/sc:createPR` when a PR already exists is implementation-defined in Claude Code's skill layer, not documented in this repository. Encoding it as normative text in AGENTS.md creates a brittleness: if the skill's output format changes, CR.2 becomes incorrect without any file in this repo changing.

**Recommended fix:** Add an inline note: "The no-op behavior of `/sc:createPR` is platform-defined; verify current behavior in Claude Code skill documentation before relying on CR.2(b)."

---

### F7 — MAY-level: No Audit Trail to Source Spec

**Severity:** Low

The Closing Run Procedure does not cite which source spec (A/B/C, G/H/I, or J/K/L) motivated the `/sc:createPR` requirement. All other additions in this PR trace back to named specs. CR.1–CR.5 appear to have been authored de novo rather than derived from an existing research artifact.

If this rule was motivated by observed agent behavior (e.g., agents forgetting to create PRs), that context is lost. Future agents or maintainers cannot determine whether CR.1–CR.5 are backed by empirical evidence or are speculative.

**Recommended fix:** Add a brief source attribution in the section preamble, e.g., "Motivated by [observed pattern X / Task Y / operator instruction Z]."

---

### F8 — MAY-level: Missing Friction Log Entry for Commit 3

**Severity:** Low

The friction-log.md for Task 001 (`tasks/001-refactor-governance-from-specs/friction-log.md`) covers only the linter and template work. The AGENTS.md addition (commit 3) is substantive enough to warrant its own FL entry — especially since it is out-of-scope relative to the prompt.

Per `FRUSTRATED.md`, every session change MUST be logged. FL0 is acceptable, but the entry must exist.

**Recommended fix:** Add an FL entry to the friction-log covering commit 3's authoring experience.

---

## What the PR Gets Right

- **Linter architecture** (commit 1): Clean separation of concerns across `validate-frontmatter.py`, `lint-structure.py`, `lint-linkage.py`, `check-trust.py`. The four-tool design correctly mirrors the four enforcement categories.
- **Mechanical enforcement mapping tables**: Each root spec now has a `§N.0` table linking prose rules to the tool that enforces them. This is exactly what the repo needed.
- **Frontmatter retrofit**: Backfilling 14 research files is unglamorous work that was done correctly and completely (waiver list burned to zero).
- **CR.1 / CR.3 Gherkin**: The two scenarios that exist are syntactically valid Gherkin with proper `Given/When/Then` structure.
- **FL1 honesty**: The friction-log accurately records the waiver-backfill burden and the over-aggressive linkage check — a genuine contribution to the repo's self-improvement loop.

---

## Recommendation

**Block on F1 and F2; request changes on F3 and F4; note F5–F8 as follow-up.**

The linter suite and spec-binding work (commits 1–2) can merge as-is. Commit 3 should be amended to add the three missing Gherkin scenarios and fix the anchor label before merge.
