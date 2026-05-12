---
type: note
status: active
slug: review-pr109-archive-spec
summary: "Governance critique of PR #109 (codex/create-/archive.md-governance-specification). Identifies 3 critical violations, 6 structural gaps, and 4 minor issues. The spec is incomplete and cannot be merged without remediation."
created: 2026-05-12
updated: 2026-05-12
task_id: "090"
task_status: done
task_owner: "claude-sonnet-4-6"
task_priority: P1
task_uses_prompts: []
task_spawns_research: []
task_spawns_prompts: []
task_affects_paths: []
---

# Review — PR #109 (`codex/create-/archive.md-governance-specification → main`)

**Reviewer:** `claude-sonnet-4-6`, session `claude/brave-darwin-xqiWW`
**Date:** 2026-05-12
**PR:** [#109](https://github.com/netzkontrast/agency/pull/109) — `codex/create-/archive.md-governance-specification → main`
**Commit reviewed:** `faa0e15` — "Add archive governance spec and route mapping"
**Files changed:** `ARCHIVE.md` (new, 79 lines), `AGENTS.md` (+3 / -1)
**Governing specs:** `AGENTS.md`, `TASK.md`, `PROMPT.md`, `CLAUDE.md §3–§6`, `decisions/readme.md`

---

## 1. Verdict

The intent is sound: a persistent archiving spec belongs in this repo.
However, the PR **cannot be merged as-is**. It introduces a root-level governance
spec via an external Codex agent without the governance graph that the repo
requires — no Task, no Prompt, no ADR — and the spec body itself violates the
spec-language contract on four dimensions. The routing-table addition to
`AGENTS.md` is also inconsistent with the surrounding English-language table.

Three Critical violations must be resolved before merge. Six Structural gaps
should be closed in the same pass. Four Minor items are advisory.

---

## 2. Critical Violations

### C.1 — No Task in `/tasks/` (Missing Audit Graph Root)

**Rule:** `AGENTS.md §Task Type Routing`, `CLAUDE.md §3`, `TASK.md §1`

Every piece of coordinated work — including authoring a new root-level spec —
MUST be governed by a Task file in `/tasks/<NNN>-<slug>/task.md`. The Task is
the root of the audit graph (`Task → Prompt → Research`). PR #109 was generated
by a Codex agent operating from an external task at
`chatgpt.com/codex/cloud/tasks/task_e_6a030b644b208324a7e2ad7938219657`.

That external task is **not** a spec-compliant artifact in this repository.
No `/tasks/` entry was created before, during, or after the commit. The
pre-commit hook does not mechanically gate on this (it is a social contract),
but the audit graph is broken: there is no way to trace authorship, rationale,
or acceptance criteria through the repo's own tooling.

**Required fix:** Create `/tasks/090-review-pr109-archive-spec/task.md` (or a
higher-numbered slot) with `task_status: done`, `task_owner` identifying the
Codex agent session, and `task_affects_paths` listing `ARCHIVE.md` and
`AGENTS.md`. Alternatively, the Codex agent should re-submit with a proper
Task bootstrap.

---

### C.2 — No Prompt in `/prompts/` (Missing Actor Artifact)

**Rule:** `PROMPT.md §1`, `AGENTS.md §Task Type Routing`, `CLAUDE.md §3`

Every executable instruction set given to an agent MUST be materialised as a
three-file scaffold in `/prompts/<slug>/{prompt.md, brief.md, readme.md}`.
The Codex task description (an external ChatGPT URL) is the de-facto prompt,
but it does not exist in this repository.

No `/prompts/` entry was created. The Machine–Actor–Space separation
(`CLAUDE.md §1`) is violated: the Actor layer is invisible.

**Required fix:** The instruction given to the Codex agent MUST be transcribed
into `/prompts/archive-spec-authoring/{prompt.md,brief.md,readme.md}` and
`task_uses_prompts` on the governing Task MUST reference it. This is not
retroactive bureaucracy — it is what makes the spec auditable and re-executable.

---

### C.3 — No ADR for a New Root-Level Governance Spec

**Rule:** `CLAUDE.md §3` ("Change a repo-architecture convention → `decisions/`"),
`decisions/readme.md`, MADR 4.0.0

Introducing `ARCHIVE.md` as a new top-level governance spec is a
**repo-architecture convention change** — it adds a new normative authority
to the root spec layer, expands the routing table in `AGENTS.md`, and implies
a new operational lifecycle that existing tooling does not implement.
Per `CLAUDE.md §3` and `decisions/readme.md`, such changes MUST go through the
MADR 4.0.0 process in `/decisions/<NNNN>-<slug>.md` with `adr_status: Proposed`
before the spec is created.

No ADR was filed. The decision record is absent.

**Required fix:** File `/decisions/0006-archive-governance-spec.md` (or the
next free slot) with the standard MADR 4.0.0 frontmatter, document the context,
options considered, and decision outcome, then reference it from `ARCHIVE.md`.

---

## 3. Structural Gaps

### S.1 — Language Inconsistency: German in an English Spec Layer

**Rule:** `AGENTS.md §Spec Language Reference`, `maintenance/language-spec.md`

Every other root governance spec (`AGENTS.md`, `TASK.md`, `PROMPT.md`,
`RESEARCH.md`, `SKILLS.md`, `FOLDERS.md`, `MAINTENANCE.md`, `FRUSTRATED.md`,
`PRE_COMMIT.md`) is authored in English. `ARCHIVE.md` is primarily in German.

The routing-table row added to `AGENTS.md` is also in German:

```
| Archivierung/Stilllegung von Artefakten inkl. Trigger und Ablauf | … |
```

This breaks the language contract of the governance layer. Agents scanning
`AGENTS.md` expecting English routing entries will fail pattern-match heuristics
against this row.

**Required fix:** Rewrite `ARCHIVE.md` in English. Update the `AGENTS.md`
routing row to English, consistent with all other rows in that table.

---

### S.2 — RFC 2119 Keywords Missing Throughout

**Rule:** `AGENTS.md §Spec Language Reference`, `CLAUDE.md §5`

> Every normative clause uses **uppercase RFC 2119 keywords** (`MUST`,
> `MUST NOT`, `SHOULD`, `MAY`, …). Lowercase prose is non-normative.

`ARCHIVE.md` uses German lowercase equivalents throughout:

- "müssen" (should be **MUST**)
- "muss" (should be **MUST**)
- "werden ausgelöst" (normative trigger, needs **MUST** framing)

Only one uppercase `MUST` appears in the entire spec (`"Die gewählte Operation
MUST pro Archivierungsaktion begründet…"`) — and even that is a hybrid
German/English sentence, making the scope of the keyword ambiguous.

**Required fix:** Every normative clause MUST use uppercase RFC 2119 keywords.
Non-normative explanatory prose SHOULD remain lowercase. Review each sentence
in `ARCHIVE.md` and classify accordingly.

---

### S.3 — Zero Gherkin Acceptance Criteria

**Rule:** `CLAUDE.md §5`, `AGENTS.md §Spec Language Reference`

> Every acceptance criterion is a **Gherkin scenario** (`Feature: / Scenario: /
> Given / When / Then`), not a bullet list. Scenarios MUST be self-contained
> and executable. Anchor with `# anchor: <stable-id>` on the line above.

`ARCHIVE.md` contains no Gherkin scenarios. All acceptance criteria are
rendered as bullet lists under the "Checkliste" heading. Bullet lists are not
executable. Compare `TASK.md §6`, `PROMPT.md §6.9`, `MAINTENANCE.md §6` for
the expected pattern (5–15 Gherkin scenarios per spec).

**Required fix:** Add a `## Acceptance Criteria` section with ≥ 4 Gherkin
scenarios covering: (a) trigger evaluation, (b) Mode selection and
documentation, (c) link-integrity invariant, (d) governance-check pass.

---

### S.4 — Archive Path Undefined

**Rule:** Internal consistency; `FOLDERS.md §1` (operational folder topology)

The "Move" operation mode requires "einen definierten Archivpfad" (a defined
archive path), but `ARCHIVE.md` never defines that path. No `/archive/` directory
is listed in `CLAUDE.md §12` topology. No `FOLDERS.md` exemption is cited.

Without a defined archive path, the "Move" mode is unimplementable. Agents
executing the spec will invent arbitrary paths, breaking the audit graph.

**Required fix:** Either (a) specify the canonical archive path (e.g.,
`/archive/<layer>/<slug>/`) and add it to `CLAUDE.md §12`, or (b) remove the
"Move" mode until the path is decided via ADR.

---

### S.5 — No Enforcement Tooling Shipped

**Rule:** Pattern established by all 032–039 spec-integration Tasks

Every root spec that introduces new normative invariants ships enforcement
tooling in the same PR or defers it explicitly to a numbered follow-up Task.
For example:

- `TASK.md` → `tools/fm/check-task-lifecycle-classification.py`
- `PROMPT.md` → `tools/check-prompt-self-containedness.py`
- `FOLDERS.md` → `tools/check-readme-frontmatter.py`
- `MAINTENANCE.md` → `tools/maintenance/staleness-audit.py`

`ARCHIVE.md` defines four invariants (link integrity, audit-graph
preservation, frontmatter validity, provenance) but ships **zero** linters.
The spec is advisory-only at merge time.

**Required fix:** Either ship `tools/check-archive-invariants.py` (at minimum:
verify that moved/index-only artifacts have a `archive_reason` frontmatter key
and that no links to archived artifacts are dangling), or file a numbered
follow-up Task (`task_blocked_by: ["090"]`) and reference it from `ARCHIVE.md`.

---

### S.6 — `CLAUDE.md §12` Topology Not Updated

**Rule:** `CLAUDE.md §12`, `CLAUDE.md §14 quick non-negotiable #7`

`CLAUDE.md §12` enumerates every top-level file in the repository topology.
`ARCHIVE.md` is a new top-level file but was not added to that list. Agents
bootstrapping from `CLAUDE.md` will not discover `ARCHIVE.md` through the
canonical read path.

**Required fix:** Add `ARCHIVE.md` to the `agency/` topology block in
`CLAUDE.md §12`, with a one-line descriptor consistent with the other entries.

---

## 4. Minor Issues

### M.1 — `updated` as Archive Trigger Is Ambiguous

`task_status: updated` (§ "Task-Trigger") means "superseded by a successor
Task" — not "completed". A superseded task may have an active successor, making
archiving premature. The trigger should clarify: "updated AND no active
`task_superseded_by` successor" or use `done`/`abandoned` only.

---

### M.2 — "Snapshot" Mode Is Under-Defined

The Snapshot mode ("Ein unveränderlicher Snapshot wird erzeugt") does not
specify the mechanism. In a Git repo, snapshots are natural (every commit is
immutable). The mode needs to state whether this means a tagged commit, a
copied directory, or just a frontmatter marker. Without this, agents cannot
implement it consistently.

---

### M.3 — "7-Tage-Cooldown" Is Unimplementable Without Tooling

The 7-day cooldown since `updated:` has no tooling to enforce it and no
frontmatter key to record it. It will silently be ignored. Either mechanize
it (`tools/check-archive-invariants.py` reading `updated:` dates) or
document it as a human-review step, not an automated invariant.

---

### M.4 — PR Was Not Submitted as a Draft

**Rule:** `AGENTS.md §Closing Run Procedure CR.4`, `CLAUDE.md §10`

> Open a **draft PR** via the platform's primitive.

PR #109 was opened as a non-draft (`"draft": false`). The closing-run procedure
requires all agent-opened PRs to start as drafts pending human review.

---

## 5. Summary Table

| ID | Severity | Title | Blocking? |
|---|---|---|---|
| C.1 | Critical | No Task in `/tasks/` — audit graph root missing | Yes |
| C.2 | Critical | No Prompt in `/prompts/` — Actor layer invisible | Yes |
| C.3 | Critical | No ADR for new root-level governance spec | Yes |
| S.1 | Structural | German language in an English spec layer | Yes |
| S.2 | Structural | RFC 2119 keywords absent throughout | Yes |
| S.3 | Structural | Zero Gherkin acceptance criteria | Yes |
| S.4 | Structural | Archive path undefined ("Move" mode unimplementable) | Yes |
| S.5 | Structural | No enforcement tooling or deferred Task | Conditional |
| S.6 | Structural | `CLAUDE.md §12` topology not updated | Yes |
| M.1 | Minor | `updated` trigger is ambiguous | No |
| M.2 | Minor | "Snapshot" mode under-defined | No |
| M.3 | Minor | 7-day cooldown unimplementable without tooling | No |
| M.4 | Minor | PR opened as non-draft | No |

**Merge recommendation: ✗ NOT READY — resolve C.1–C.3 and S.1–S.4 first.**

---

## 6. What Good Looks Like

A well-formed version of this PR would include:

1. A Task in `/tasks/090-archive-spec-authoring/task.md` (created first, with
   `task_status: in_progress`, flipped to `done` at close).
2. A Prompt in `/prompts/archive-spec-authoring/prompt.md` (three-file scaffold,
   containing the instruction text currently only in the external Codex URL).
3. An ADR in `/decisions/0006-introduce-archive-spec.md` recording the decision
   rationale and options.
4. `ARCHIVE.md` rewritten in English with RFC 2119 keywords, ≥ 4 Gherkin
   scenarios, a defined archive path, and a reference to the ADR.
5. `AGENTS.md` routing row in English.
6. `CLAUDE.md §12` updated to include `ARCHIVE.md`.
7. Either `tools/check-archive-invariants.py` shipped, or a follow-up Task filed.

The archive-spec concept deserves to be in this repo. The implementation path
to get there is longer than a single Codex commit.

---

## Frustration Log

Highest Frustration Level: FL0 — No friction. The spec is easy to evaluate
against the published governance contract; all findings trace directly to
normative rules.
