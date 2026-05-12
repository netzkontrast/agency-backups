---
type: note
status: active
slug: codex-pr-review-notes
summary: "Governance critique of PR #110 — CODEX.md root spec and Codex platform note in AGENTS.md."
created: 2026-05-12
updated: 2026-05-12
---

# Review: PR #110 — CODEX.md Onboarding Spec & Codex Platform Note

**Reviewed by:** Claude Code (Task 090)
**PR branch:** `codex/init-repo-for-codex-with-root-specs`
**Commit:** `dec2f37`
**Review date:** 2026-05-12

---

## What the PR Does

1. **Creates `CODEX.md`** — a new root-level agent onboarding file for Codex, analogous to `CLAUDE.md`. It covers mandatory startup, layer routing, frontmatter expectations, and the session-close contract.
2. **Amends `AGENTS.md`** — adds a `#### Codex` subsection under "Platform Implementation Notes", describing how Codex satisfies Closing Run Procedure step 4 via the `make_pr` runtime primitive.

The intent is correct and valuable: Codex needs an explicit onboarding path, and AGENTS.md must enumerate the platform.

---

## Critical Defects — Closing Run Procedure Violations

These are binding spec failures per AGENTS.md CR.1–CR.7.

### D1 — No Friction Log (CR.1, Step 1 — MUST)

AGENTS.md CR.1 requires every session to satisfy all four steps of the Closing Run Procedure **before declaring completion**. Step 1 states:

> "The session's `friction-log.md` MUST exist with a parseable `Highest Frustration Level: FL[0-3]` declaration in the body."

Neither this commit nor the PR body contains a friction log, a `## Frustration Log` section, or any FL declaration. FRUSTRATED.md is explicit: "absence of a log is itself a defect."

**Required fix:** Add a `friction-log.md` to an appropriate location (e.g., this task folder) carrying a parseable `Highest Frustration Level: FL[n]` declaration, and reference it in the PR body.

---

### D2 — PR Body Lacks FL Declaration (CR.5(b) — MUST)

AGENTS.md CR.5 requires the PR body to include "(b) the FL declaration from the friction log." The PR body (`#110`) contains a motivation section, description, testing notes, and a link to an external Codex task — but no FL declaration. This is a hard requirement, not advisory.

---

### D3 — No Repo-Internal Task Slug (CR.5(a) — MUST)

AGENTS.md CR.5 requires the PR body to reference "(a) the closed Task slug(s) under `/tasks/`." The PR body links to:

```
https://chatgpt.com/codex/cloud/tasks/task_e_6a03113596008324aa681061e8c2350b
```

This is an external URL on `chatgpt.com`, not a path within this repository's `/tasks/` tree. The spec is unambiguous: the citation must be a slug under `/tasks/`. External task-management URLs do not satisfy CR.5(a).

**Required fix:** Create a Task (e.g., `tasks/090-codex-platform-spec/task.md`) in this repo that tracks the work, and reference its slug in the PR body.

---

### D4 — PR Opened as Non-Draft (Contradicts Own Commit)

The `#### Codex` section added by this very commit states:

> "Codex sessions satisfy step 4 by opening a **draft pull request** via the runtime's native PR primitive."

The PR `#110` was opened with `draft: false`. The session therefore violated the rule it was simultaneously creating, in the same change set.

---

## Structural Gaps

### G1 — No ADR for New Root-Level Spec File

CLAUDE.md §6 states:

> "any change to repo-architecture conventions (storage paths, frontmatter schemas, hook integration) MUST go through `/decisions/<NNNN>-<slug>.md` per MADR 4.0.0."

`CODEX.md` is a new root-level spec file — it establishes a new platform-specific onboarding contract and extends the governance topology. The amendment to `AGENTS.md` similarly modifies how the Closing Run Procedure is implemented across platforms. Both are repo-architecture convention changes. No ADR was created or referenced.

**Required fix:** File an ADR (e.g., `decisions/0011-codex-platform-onboarding.md`) documenting the decision context, options considered, and rationale for the CODEX.md approach. Reference it from CODEX.md.

---

### G2 — Broken Audit Graph (No Repo-Internal Task Exists)

The repository's fundamental design principle is the audit graph:

```
/tasks/<NNN>-<slug>/task.md
    │ task_uses_prompts ──► /prompts/<slug>/prompt.md
                                    │ executed by agent ──► /research/<slug>/
```

This work was coordinated entirely via an external Codex task URL (chatgpt.com). There is no `/tasks/` entry, no `/prompts/` entry, and no `/research/` evidence artifact in this repo. The audit graph is completely absent for this change.

This doesn't mean every Codex session must produce research; but the orchestration entry (Task) is the minimum traceability unit the repo requires.

---

### G3 — CODEX.md Omits `decisions/readme.md` from the Governance Chain

CLAUDE.md §1 includes `decisions/readme.md` in its spec chain and routes architectural decisions there. CODEX.md's routing table (Section 2) maps only to the four operational layers (TASK.md / PROMPT.md / RESEARCH.md / SKILLS.md) — the ADR ledger is entirely absent.

A Codex agent reading only CODEX.md would be unaware that repo-architecture changes require an ADR, which compounds G1.

**Required fix:** Add an entry to Section 2's routing table:
> - Architecture decisions & convention changes → [`decisions/readme.md`](./decisions/readme.md) and `/decisions/`

---

## Content / Quality Issues

### Q1 — Section Numbering Style Inconsistency

CODEX.md uses `## 1)`, `## 2)`, `## 3)`, `## 4)` (closing-parenthesis notation). The analogous `CLAUDE.md` uses `## 1.`, `## 2.`, etc. (period notation). No functional impact, but a style inconsistency with the established root-spec pattern.

---

### Q2 — Section 3 Frontmatter Attribution Incomplete

Section 3 states: "follow the layered schema defined in **TASK.md §3**."

The L1+L2 frontmatter schema is defined across multiple specs: `AGENTS.md` (Frontmatter Ontology), `TASK.md §3`, `PROMPT.md §3`, `RESEARCH.md`, and `SKILLS.md §3`. Attributing it solely to TASK.md §3 under-specifies the full schema and will mislead Codex agents working on prompts, research, or skills.

**Suggested fix:** "…follow the layered schema defined in `AGENTS.md` (Frontmatter Ontology), with L2 namespace keys in the layer-specific spec for each directory."

---

### Q3 — Section 4 Step 4 Uses Circular / Vague Primitive Reference

The close of Section 4 reads:

> "For Codex usage in this repo, step 4 is satisfied via the platform PR primitive **used by this runtime**."

"Used by this runtime" is circular — it tells a Codex agent nothing actionable. AGENTS.md explicitly names `make_pr` as the primitive. CODEX.md should echo that name.

**Suggested fix:** "…step 4 is satisfied by calling the `make_pr` runtime primitive per [AGENTS.md § Codex](./AGENTS.md#codex)."

---

## What Was Done Well

- `CODEX.md` frontmatter is structurally correct: all L1 Vault Core keys present (`type`, `status`, `slug`, `summary`, `created`, `updated`), `type: spec` matches the root-spec pattern of `CLAUDE.md` and `AGENTS.md`.
- Section 1 correctly names both mandatory startup commands (`./install.sh` + `tools/check-governance.sh`) and correctly characterises `install.sh` as idempotent.
- Section 2's four-layer routing table maps correctly to all operational directories.
- The AGENTS.md Codex platform note correctly cites CR.5 and CR.6 requirements, and the governance check was run before the PR was opened (even if pre-existing errors were present).
- The PR body provides a clear motivation and description, which simplifies triage.

---

## Summary Score

| Category | Status |
|---|---|
| Friction log (CR.1 step 1) | FAIL — absent |
| FL declaration in PR body (CR.5(b)) | FAIL — absent |
| Repo-internal Task slug in PR body (CR.5(a)) | FAIL — external URL only |
| PR opened as draft (platform note) | FAIL — non-draft |
| ADR for new root spec / platform (CLAUDE.md §6) | FAIL — absent |
| Audit graph traceability | FAIL — no Task/Prompt in repo |
| CODEX.md `decisions/` routing | WARN — omitted |
| Style / content quality | WARN — 3 minor issues |
| Frontmatter validity | PASS |
| Startup command accuracy | PASS |
| Layer routing correctness | PASS |

**Recommendation:** Block merge until D1–D4 and G1–G2 are resolved. G3 and Q1–Q3 SHOULD be addressed in the same patch.
