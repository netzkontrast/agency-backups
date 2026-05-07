---
type: research
status: completed
slug: research-cross-spec-contradiction-baseline
summary: "Pre-chain contradiction baseline: 16 inter-spec normative conflicts cataloged across the 8 root governance specs before the 032–039 amendment chain. 5 High-severity (CONTR-001,004,005,006,014). 15 newly discovered. Feeds chain falsification criterion #3."
created: 2026-05-07
updated: 2026-05-07
research_phase: complete
research_executes_prompt: research-cross-spec-contradiction-baseline
research_friction_level: FL0
---

# Cross-Spec Normative Contradiction Baseline Report

**Repository:** `/home/user/agency`
**Report Date:** 2026-05-07
**Specs Analyzed:** AGENTS.md, TASK.md, RESEARCH.md, PROMPT.md, FOLDERS.md, FRUSTRATED.md, PRE_COMMIT.md, MAINTENANCE.md
**Chain Tasks in Scope:** 032 (AGENTS.md) through 039 (MAINTENANCE.md)

---

## §1 Methodology

All 8 root specification files were read in full. Normative clauses (those containing MUST, MUST NOT, SHOULD, SHOULD NOT, or MAY in uppercase, per RFC 2119) were extracted systematically. Clauses were then cross-indexed by topic domain.

Four contradiction classes were applied:

**Direct conflict** — Spec A says MUST X; Spec B says MUST NOT X (or vice versa) on the identical topic and same actor. The two obligations cannot simultaneously be satisfied.

**Indirect conflict** — Spec A says MUST X; Spec B says SHOULD NOT X (or Spec A says SHOULD X; Spec B says MUST NOT X). Full compliance with the MUST forces violation of the SHOULD NOT, creating an agent that cannot be simultaneously well-behaved under both.

**Scope-overlap conflict** — Two specs make normative claims about the same file, path, or structural artifact but with incompatible requirements (e.g. different slug-length ceilings, different required file counts at creation, different frontmatter mandate levels).

**Lifecycle/timing conflict** — Two specs mandate different orderings or timing for the same action (e.g. when readme.md updates must happen, when friction logs must be produced).

The known validation anchor — FRUSTRATED.md §28 ↔ PRE_COMMIT.md §2 — was used to verify the methodology before cataloging additional findings.

---

## §2 Contradiction Catalog

---

### CONTR-001 *(Validation Anchor)*

**ID:** CONTR-001
**Type:** Direct
**Spec A clause:** FRUSTRATED.md §28 (Special Triggers)
> "If a prompt demands deeply nested folder structures with less than 3 files per folder, or requires tedious administrative overhead (e.g., updating a `readme.md` for every single minor file change *instead of batching them at the pre-commit stage*), the agent MUST log this as FL2."

**Spec B clause:** PRE_COMMIT.md §2 (File Integrity & Decentralized Documentation)
> "**Global Readme Audit:** EVERY folder that has been touched during this session MUST have its `readme.md` updated *now*, right before the commit."

**Conflict description:** PRE_COMMIT.md §2 mandates per-folder readme updates on every commit that touches those folders (an unconditional MUST). FRUSTRATED.md §28 treats exactly this behavior — updating a readme for every individual file change rather than batching — as a structural-bloat trigger that MUST cause an FL2 log entry, signaling it is a bad-practice imposition. The two clauses define the same per-folder readme-update action as simultaneously mandatory and friction-inducing-enough-to-flag.

**Severity:** High — an agent executing PRE_COMMIT.md §2 faithfully will also be simultaneously required by FRUSTRATED.md §28 to log FL2 for obeying the rule, creating a permanent false-positive friction signal on every compliant commit.

---

### CONTR-002

**ID:** CONTR-002
**Type:** Scope-overlap
**Spec A clause:** FOLDERS.md §3 (Update Trigger)
> "**Update Trigger:** Pre-commit batching. Agents update touched folders' `readme.md` as a single pre-commit step, not on every file change. This protects context window from administrative bloat."

**Spec B clause:** PRE_COMMIT.md §2 (File Integrity & Decentralized Documentation)
> "**Global Readme Audit:** EVERY folder that has been touched during this session MUST have its `readme.md` updated *now*, right before the commit."

**Conflict description:** Both clauses agree on timing (pre-commit), but FOLDERS.md §3 explicitly says updates are batched "not on every file change," using that exact phrase to justify the batching design. PRE_COMMIT.md §2 expresses the same batching requirement without qualification, making it ambiguous whether it applies to every commit in a session or just the final one. When an agent does multiple commits in a single session, PRE_COMMIT.md §2 ("every commit") and FOLDERS.md §3 ("single pre-commit step") diverge: FOLDERS.md implies one batch at the end of the session while PRE_COMMIT.md implies a batch before each individual commit.

**Severity:** Medium — most sessions produce one commit, but multi-commit sessions expose the discrepancy.

---

### CONTR-003

**ID:** CONTR-003
**Type:** Scope-overlap
**Spec A clause:** FOLDERS.md §2 (Slug & Folder Naming)
> "All operational folders use the form `/<top-level>/<slug>/`. Slugs are kebab-case, max 5 tokens."

**Spec B clause:** RESEARCH.md §6.1 (Storage Path — External Research)
> "`<slug>` is kebab-case derived from the research topic (max 6 tokens), NOT an internal prompt slug."

**Conflict description:** FOLDERS.md §2 establishes a universal max-5-token ceiling for all operational folder slugs. RESEARCH.md §6.1 creates a specific carve-out for external research result slugs permitting 6 tokens. An external research slug that is exactly 6 tokens passes RESEARCH.md but violates FOLDERS.md, and the enforcement tool (`tools/lint-structure.py`) enforces FOLDERS.md. The specs do not state which takes precedence.

**Severity:** Medium — affects any external research ingestion using a 6-token slug.

---

### CONTR-004

**ID:** CONTR-004
**Type:** Direct
**Spec A clause:** MAINTENANCE.md §1 (Repair Permission Tiers — T3)
> "**T3 — Structural** … MUST NOT fix directly. Write a Task in `/tasks/` instead."

and §3.1 (Nightly Maintenance Run Scope — DON'T)
> "**DON'T:** Apply T3 or T4 changes directly. Write Tasks for them."

**Spec B clause:** MAINTENANCE.md §3.4 (Stale-Task Audit — Drifted re-frame bucket)
> "This is a **T3 action** (§1) — the agent MUST file the lifecycle transition itself as a Task only if the supersession spans more than the typical two-Task pair … For ordinary 1→1 supersessions, the maintenance agent **MAY perform the transition directly** because every step is mechanical (frontmatter mutations + a one-paragraph friction log) and reversible."

**Conflict description:** Within MAINTENANCE.md itself, §1 and §3.1 impose an unqualified MUST NOT on direct T3 work, while §3.4 carves out a MAY-perform-directly exception for 1→1 task supersessions that §1 classifies as T3. The exception in §3.4 is not reflected as a listed exemption in the T3 tier table of §1, creating an internal contradiction.

**Severity:** High — an agent reading §1 will refuse to do what §3.4 says it MAY do. An agent reading §3.4 first will perform an action that §1 says it MUST NOT.

---

### CONTR-005

**ID:** CONTR-005
**Type:** Direct
**Spec A clause:** AGENTS.md §Session Setup, rule SS.2
> "An agent MUST run `tools/check-governance.sh` immediately after `install.sh` completes and **MUST NOT proceed** if it exits non-zero."

**Spec B clause:** MAINTENANCE.md §4.1 (Maintenance Bypass Mode)
> "However, if the repository has pre-existing errors, the hook will allow the commit **if and only if** every file causing an error has a corresponding `open` Task in `/tasks/` whose `task_affects_paths` array covers the offending file."

**Conflict description:** AGENTS.md SS.2 is an absolute gate: a non-zero exit from `check-governance.sh` at session start MUST halt all further work. MAINTENANCE.md §4.1 defines a bypass that allows commits to proceed when pre-existing errors are covered by open Tasks. If a repository has pre-existing covered errors, AGENTS.md requires the agent to stop while MAINTENANCE.md permits it to continue and commit.

**Severity:** High — a maintenance agent that obeys AGENTS.md SS.2 will be permanently blocked on any repository with tracked pre-existing errors, defeating the entire purpose of the maintenance bypass.

---

### CONTR-006

**ID:** CONTR-006
**Type:** Lifecycle
**Spec A clause:** FRUSTRATED.md §When and How to Log, item 2 (Standard Tasks)
> "**Standard Tasks:** You MUST include a section named `## Frustration Log` in your final PR description or submit message."

**Spec B clause:** TASK.md §7 (pre-commit check 7 — Friction Log)
> "`friction-log.md` MUST exist for every closed task (`done`, `updated`, or `abandoned`) and MUST contain an `FL[0-3]` declaration … An inline declaration in the commit message is NOT a substitute."

**Conflict description:** FRUSTRATED.md §32 (standard tasks) mandates friction logging in the PR description or submit message (an inline location). TASK.md §7 explicitly states that an inline declaration in the commit message is NOT a substitute for a standalone `friction-log.md` file. For a standard task that closes as `done`, both specs apply simultaneously but require incompatible artifacts.

**Severity:** High — an agent satisfying FRUSTRATED.md will fail TASK.md §7.8's mechanical linter check (`tools/check-trust.py`).

---

### CONTR-007

**ID:** CONTR-007
**Type:** Scope-overlap
**Spec A clause:** FRUSTRATED.md §When and How to Log, item 2
> "**Standard Tasks:** You MUST include a section named `## Frustration Log` in your final PR description or **submit message**."

**Spec B clause:** PRE_COMMIT.md §3 (Mandatory Agent Feedback & Frustration Logging)
> "For standard tasks, include a `## Frustration Log` section in your final PR description or **commit message**."

**Conflict description:** Both specs agree on placement for standard tasks, but FRUSTRATED.md says "PR description or submit message" while PRE_COMMIT.md says "PR description or commit message." A "submit message" could refer to a non-git submission mechanism (e.g. Jules/Gemini platform conventions), while PRE_COMMIT.md's "commit message" is unambiguously the git commit message.

**Severity:** Low — in practice Claude Code sessions use git, so the distinction rarely matters. But the wording divergence creates ambiguity for non-Claude Code agents.

---

### CONTR-008

**ID:** CONTR-008
**Type:** Scope-overlap
**Spec A clause:** FRUSTRATED.md §28 (Special Triggers — Structural Bloat)
> "If a prompt demands deeply nested folder structures with **less than 3 files per folder** … the agent MUST log this as FL2."

**Spec B clause:** FOLDERS.md §4 (Subfolder Heuristics)
> "**Prefer Flat Structures** — Do not create a subfolder unless **4+ files** of the exact same category accumulate."

and TASK.md §2
> "Subfolders inside a Task directory MUST NOT be created unless **4+ files** of the same category accumulate (per FOLDERS.md)."

**Conflict description:** FOLDERS.md and TASK.md set the subfolder-creation threshold at 4+ files. FRUSTRATED.md's bloat trigger fires at "less than 3 files per folder." A folder containing exactly 3 files of a single category is below FOLDERS.md's 4-file threshold (so no subfolder would yet be created), but FRUSTRATED.md's trigger would have already fired at 2 or fewer files. An agent that follows FOLDERS.md and ends up with a folder holding exactly 2 files should FL2-log the situation per FRUSTRATED.md, even though FOLDERS.md explicitly prohibits the subfolder that would remedy it.

**Severity:** Medium — creates a permanent false-positive FL2 window for any folder that holds 2–3 files, which is a common, correctly-structured state per FOLDERS.md.

---

### CONTR-009

**ID:** CONTR-009
**Type:** Scope-overlap
**Spec A clause:** AGENTS.md §Frontmatter Ontology (Summary)
> "Every Markdown file in this repository **SHOULD** carry frontmatter. Files inside operational directories (`/tasks/`, `/prompts/`, `/research/`) **MUST** carry frontmatter."

**Spec B clause:** FOLDERS.md §5
> "Operational-folder `readme.md` files **SHOULD** carry L1 Vault Core frontmatter."

**Conflict description:** AGENTS.md and TASK.md agree that operational-directory files MUST carry frontmatter. FOLDERS.md §5 downgrades the requirement for `readme.md` files inside operational folders to SHOULD. A `readme.md` inside `/tasks/<NNN>-<slug>/` is in an operational directory (AGENTS.md: MUST) but FOLDERS.md §5 treats it as merely SHOULD.

**Severity:** Medium — the conflict surfaces specifically for `readme.md` files inside operational directories. Most linting tools enforce L1+L2 for `task.md`, `prompt.md`, `output/SPEC.md`; the conflict is most visible on readme files.

---

### CONTR-010

**ID:** CONTR-010
**Type:** Lifecycle
**Spec A clause:** RESEARCH.md §6.5 (Mandatory Downstream Analysis Task)
> "Every `result.md` MUST have a corresponding **open Task** in `/tasks/<NNN>-<slug>/` created **in the same commit**."

**Spec B clause:** TASK.md §4.8
> "Every change that affects the membership or `task_status` of any Task … MUST be accompanied **in the same commit** by an update to `tasks/readme.md`."

**Conflict description:** When an external `result.md` is committed, RESEARCH.md §6.5 mandates that a new Task folder also be created in the same commit. TASK.md §4.8 mandates that any new Task folder be accompanied by a `tasks/readme.md` update in the same commit. RESEARCH.md §6.5 presents the Task-creation requirement as the only same-commit obligation, never mentioning the tasks/readme.md update — implying it is complete while it is in fact incomplete. An agent following RESEARCH.md §6.5 without TASK.md §4.8 in mind will produce a commit that violates §7.11's linter check.

**Severity:** Medium — the omission will cause linter failures on any external research ingestion commit.

---

### CONTR-011

**ID:** CONTR-011
**Type:** Direct
**Spec A clause:** RESEARCH.md §3 (Mandatory Frontmatter — slug field)
> "`slug: <research-slug>` — MUST equal the executing prompt slug."

**Spec B clause:** RESEARCH.md §6.1 (External Research Storage Path)
> "`<slug>` is kebab-case derived from the research topic (max 6 tokens), **NOT an internal prompt slug**."

**Conflict description:** Within RESEARCH.md itself, §3 states the research slug MUST equal the prompt slug, while §6.1 explicitly states that external research slugs are NOT the internal prompt slug but are derived independently from the research topic. The `slug` constraint in §3 is stated universally, not scoped to internal research only, creating an internal contradiction within the same spec.

**Severity:** Medium — requires careful reading to understand the internal/external split; the risk is an agent applying §3's MUST-equal constraint to external results.

---

### CONTR-012

**ID:** CONTR-012
**Type:** Indirect
**Spec A clause:** AGENTS.md §Session Setup, rule SS.1 and SS.3
> "**SS.1** An agent MUST run `./install.sh` at the start of every session before reading or writing any repository file."
> "**SS.3** An agent MUST NOT skip setup on the assumption that dependencies are already installed."

**Spec B clause:** MAINTENANCE.md §2.1 (When to Run — Repo Coherence Check)
> "The prompt MUST be configured as a Claude Code SessionStart hook or invoked via `/loop` at the operator's discretion."

**Conflict description:** AGENTS.md SS.1 requires `./install.sh` as the MUST-run first action before any file read or write. MAINTENANCE.md §2.1 recommends the Repo Coherence Check at session start via a SessionStart hook — but the Coherence Check reads `maintenance/run-log.md` (a file), which means it reads a repository file before `install.sh` would have run under AGENTS.md SS.1's ordering. MAINTENANCE.md does not acknowledge or defer to the SS.1 ordering requirement.

**Severity:** Low — affects agents where the Coherence Check is wired as an automatic SessionStart hook. The install.sh call must be part of the hook itself, but this is not stated in either spec.

---

### CONTR-013

**ID:** CONTR-013
**Type:** Scope-overlap
**Spec A clause:** TASK.md §4 (Workflow, step 5 — Block)
> "**Distinction**: Tasks blocked by **another Task in this repo** SHOULD use `task_blocked_by` instead of the `blocked` status — `blocked` is reserved for conditions outside the Task graph."

**Spec B clause:** TASK.md §8.7 (Blocker Tasks — item 2)
> "A Task **MAY be both** `task_status: blocked` *and* carry `task_blocked_by` entries."

**Conflict description:** This is an internal TASK.md conflict. §4 Step 5 says tasks blocked by another in-repo task SHOULD use `task_blocked_by` (implying `task_status: blocked` is NOT appropriate for in-repo blockers). §8.7 explicitly says a Task MAY be both `task_status: blocked` AND carry `task_blocked_by` entries — directly contradicting §4. An agent following §4 would never set `task_status: blocked` when a `task_blocked_by` entry is present; an agent following §8.7 would know it can.

**Severity:** Medium — the practical consequence is inconsistent `task_status` values for tasks waiting on in-repo dependencies AND an external condition simultaneously.

---

### CONTR-014

**ID:** CONTR-014
**Type:** Scope-overlap
**Spec A clause:** PROMPT.md §6.8 (Friction Log pre-commit check)
> "**Friction Log** — A `## Frustration Log` section in the PR/commit message (or a `friction-log.md` adjacent for standalone runs), per `FRUSTRATED.md`. FL0 declarations are still mandatory."

**Spec B clause:** TASK.md §7 (Friction Log pre-commit check 7)
> "`friction-log.md` MUST exist for every closed task (`done`, `updated`, or `abandoned`) and MUST contain an `FL[0-3]` declaration … An inline declaration in the commit message is NOT a substitute."

**Conflict description:** PROMPT.md §6.8 explicitly offers a PR/commit message section as a valid friction log location for prompt tasks. TASK.md §7 explicitly states that a commit-message location is NOT a substitute for a `friction-log.md` file. For a Prompt Task linked to a Task closing as `done`, both specs apply simultaneously but require incompatible artifacts. This is the same root mechanism as CONTR-006 but arises from PROMPT.md specifically, making it a separate entry because chain tasks 033 and 034 can resolve it independently.

**Severity:** High — an agent satisfying PROMPT.md §6.8 by writing a commit-message frustration section will fail TASK.md §7's mechanical `tools/check-trust.py` check.

---

### CONTR-015

**ID:** CONTR-015
**Type:** Scope-overlap
**Spec A clause:** AGENTS.md §Frontmatter Ontology, Usage Rule R4
> "**R4.** A spec file MUST include a verbatim `§ RFC 2119` declaration section before its first normative clause."

**Spec B clause:** All 7 other root specs — none contain a verbatim `§ RFC 2119` section. Only TASK.md §1 has a brief inline declaration: "The keywords MUST, MUST NOT, SHOULD, SHOULD NOT, and MAY in this document are to be interpreted as described in RFC 2119."

**Conflict description:** AGENTS.md R4 mandates that every spec file include verbatim RFC 2119 boilerplate. None of the other 7 root specs comply — including PRE_COMMIT.md and FRUSTRATED.md which have no RFC 2119 declaration at all. By AGENTS.md R4, all 7 other root specs are currently non-compliant with an AGENTS.md MUST.

**Severity:** Low — the linter does not currently check for this section in root specs. The practical risk is future spec authors omitting the section, but existing specs are already in violation without operational consequence.

---

### CONTR-016

**ID:** CONTR-016
**Type:** Lifecycle
**Spec A clause:** RESEARCH.md §4 (Workflow Requirements, step 4)
> "**Work in Workspace** — Save planning scripts, search logs, downloaded pages, and tracking files into `/workspace`. … Execution scripts (`.py`, `.sh`) MUST be deleted before final commit."

**Spec B clause:** PRE_COMMIT.md §1 (Clean Working Directory)
> "Verify there are no unintended temporary files, `.py` or `.sh` script scratchpads, or loose log dumps. Ensure that you have explicitly deleted any temporary execution scripts used to generate data."

**Conflict description:** RESEARCH.md §4 permits execution scripts to remain in `/workspace` *during* execution ("Save planning scripts … into `/workspace`"), while PRE_COMMIT.md §1 is phrased as a general check without scoping to the pre-commit phase, which an agent could read as prohibiting `.py`/`.sh` files from ever being in the repository working tree. The "during execution vs. at commit" lifecycle distinction is only explicit in RESEARCH.md; PRE_COMMIT.md's wording implies the prohibition is always active.

**Severity:** Low — a timing ambiguity rather than a hard logical conflict.

---

## §3 Per-Spec Risk Table

### AGENTS.md

| Metric | Value |
|---|---|
| Contradictions involving this spec | 4 (CONTR-005, CONTR-009, CONTR-012, CONTR-015) |
| Riskiest clauses | SS.2 (MUST NOT proceed on non-zero exit — conflicts with MAINTENANCE.md §4.1 bypass); R4 (RFC 2119 section requirement — all other specs violate it); Frontmatter Ontology MUST (incomplete compared to TASK.md L2 requirement) |
| Pending chain task | 032 — any amendment to SS.2 must address MAINTENANCE.md §4.1 bypass; any amendment to R4 scope must clarify whether it applies to root specs |

### TASK.md

| Metric | Value |
|---|---|
| Contradictions involving this spec | 5 (CONTR-006, CONTR-009, CONTR-010, CONTR-013, CONTR-014) |
| Riskiest clauses | §7 Friction Log check 7 ("commit message is NOT a substitute" — conflicts with FRUSTRATED.md and PROMPT.md); §4 Step 5 / §8.7 blocker semantics (internal self-contradiction); §4.8 same-commit tasks/readme.md update (omitted from RESEARCH.md §6.5) |
| Pending chain task | 033 — must clarify whether §7's prohibition applies when no linked Task exists; must reconcile §4 Step 5 vs §8.7 blocker language |

### PROMPT.md

| Metric | Value |
|---|---|
| Contradictions involving this spec | 2 (CONTR-007 minor, CONTR-014) |
| Riskiest clauses | §6.8 Friction Log (PR/commit-message location — conflicts with TASK.md §7's prohibition) |
| Pending chain task | 034 — must harmonize §6.8 with TASK.md §7; add explicit scoping for standalone prompt tasks vs Task-linked ones |

### RESEARCH.md

| Metric | Value |
|---|---|
| Contradictions involving this spec | 4 (CONTR-003, CONTR-010, CONTR-011, CONTR-016) |
| Riskiest clauses | §6.1 slug max-6-token (conflicts with FOLDERS.md §2 max-5-token); §6.5 same-commit requirement (incomplete — omits tasks/readme.md update per TASK.md §4.8); §3 slug MUST-equal-prompt (conflicts with §6.1 in the same spec) |
| Pending chain task | 035 — must resolve the internal §3-vs-§6.1 slug contradiction by scoping §3's MUST-equal to internal research only; must cross-reference TASK.md §4.8 in §6.5 |

### FOLDERS.md

| Metric | Value |
|---|---|
| Contradictions involving this spec | 4 (CONTR-001, CONTR-002, CONTR-003, CONTR-008) |
| Riskiest clauses | §3 Update Trigger (batching language vs PRE_COMMIT.md §2 per-commit reading); §2 max-5-token slug (conflicts with RESEARCH.md §6.1 max-6); §5 SHOULD for readme.md (weaker than AGENTS.md/TASK.md MUST for operational files) |
| Pending chain task | 036 — must resolve the batching unit ambiguity in §3; must align §2's slug ceiling with RESEARCH.md §6.1 or add explicit scoped exemption; must reconcile §5 SHOULD with AGENTS.md/TASK.md MUST |

### FRUSTRATED.md

| Metric | Value |
|---|---|
| Contradictions involving this spec | 4 (CONTR-001, CONTR-006, CONTR-007, CONTR-008) |
| Riskiest clauses | §28 Special Triggers (FL2 trigger for per-file readme updates conflicts with PRE_COMMIT.md §2 which mandates that exact behavior); §32 item 2 ("PR description or submit message" vs TASK.md §7 prohibition of inline declarations); §28 "less than 3 files per folder" subfolder-count trigger (misaligned with FOLDERS.md 4-file threshold) |
| Pending chain task | 038 — must revise §28 to exclude MUST-mandated batch readme updates from the FL2 trigger; must align the "< 3 files" trigger with FOLDERS.md's 4-file threshold |

### PRE_COMMIT.md

| Metric | Value |
|---|---|
| Contradictions involving this spec | 4 (CONTR-001, CONTR-002, CONTR-007, CONTR-016) |
| Riskiest clauses | §2 Global Readme Audit (MUST update every touched folder — conflicts with FRUSTRATED.md §28 FL2 trigger); §2 per-commit vs per-session ambiguity (conflicts with FOLDERS.md §3 batching intent); §3 "PR description or commit message" (wording divergence from FRUSTRATED.md §32) |
| Pending chain task | 037 — must clarify the batching unit in §2; must add a note that MUST-mandated batch updates do not trigger FL2 under FRUSTRATED.md §28 |

### MAINTENANCE.md

| Metric | Value |
|---|---|
| Contradictions involving this spec | 3 (CONTR-004, CONTR-005, CONTR-012) |
| Riskiest clauses | §1 T3 tier MUST NOT (absolute prohibition conflicts with §3.4's MAY-perform-directly exception for 1→1 supersessions); §4.1 bypass mode (conflicts with AGENTS.md SS.2 MUST NOT proceed requirement); §2.1 SessionStart Coherence Check (conflicts with AGENTS.md SS.1 install.sh-first sequencing) |
| Pending chain task | 039 — must add the 1→1 supersession exception explicitly to the §1 T3 tier table; must cross-reference AGENTS.md SS.2 in §4.1 with a bypass-scope clarification |

---

## §4 Amendment Safety Recommendations

### Task 032 — Amending AGENTS.md

- **CONTR-005:** Do not tighten SS.2 further without simultaneously amending MAINTENANCE.md §4.1, or add explicit scoping: "MUST NOT proceed except when all errors are covered by open Tasks per MAINTENANCE.md §4.1."
- **CONTR-015:** Any amendment that reaffirms R4 should also file a T3 Task to bring the other 7 specs into compliance, rather than silently increasing the non-compliance count.
- **CONTR-012:** If the amendment touches Session Setup (SS.1–SS.3), clarify the ordering relationship with the Coherence Check SessionStart hook in MAINTENANCE.md §2.1.

### Task 033 — Amending TASK.md

- **CONTR-006 / CONTR-014:** The "commit message is NOT a substitute" clause in §7 directly conflicts with FRUSTRATED.md §32 and PROMPT.md §6.8. Either narrow the prohibition to "task-linked sessions" or add a cross-reference that explicitly supersedes FRUSTRATED.md §32 for closed Tasks.
- **CONTR-013:** Resolve the §4 Step 5 / §8.7 internal blocker-status contradiction in the same amendment pass. Pick one authoritative statement and delete the conflicting language.
- **CONTR-010:** When amending §7's pre-commit checks or §4.8's same-commit requirements, ensure RESEARCH.md §6.5 is referenced so agents know the tasks/readme.md update is also required during external result ingestion.

### Task 034 — Amending PROMPT.md

- **CONTR-014:** §6.8's "PR/commit message" friction log location is the primary risk. If the standalone-prompt case is genuinely different from Task-linked cases, add explicit scoping: "for Prompt Tasks not linked to any Task, the commit message is sufficient; for Prompt Tasks linked to a Task closing as done, a friction-log.md is required."
- **CONTR-007:** Align the "submit message" vs "commit message" wording with FRUSTRATED.md §32 and PRE_COMMIT.md §3.

### Task 035 — Amending RESEARCH.md

- **CONTR-011:** §3's "slug MUST equal the executing prompt slug" must be scoped to internal research. Add: "For internal research runs, the research slug MUST equal the executing prompt slug. For external research (§6), the slug is derived from the research topic and is not the prompt slug."
- **CONTR-003:** §6.1's max-6-token slug ceiling contradicts FOLDERS.md §2's max-5-token universal ceiling. Either align to 5, or file a FOLDERS.md exemption that explicitly carves out external research slugs.
- **CONTR-010:** §6.5's same-commit requirement must be augmented with a mention of TASK.md §4.8's tasks/readme.md update obligation.

### Task 036 — Amending FOLDERS.md

- **CONTR-001 / CONTR-002:** §3's "Update Trigger" wording should explicitly clarify the unit of batching. Consider: "A 'pre-commit step' means immediately before the commit that stages the relevant changes; within a single session with multiple commits, each commit triggers its own readme batch for the folders it touches."
- **CONTR-003:** Add an explicit carve-out: "External research result slugs (RESEARCH.md §6.1) MAY use up to 6 tokens as a documented exception to this ceiling."
- **CONTR-009:** §5's SHOULD for readme.md frontmatter in operational folders should be reconciled with AGENTS.md and TASK.md's MUST. Either upgrade §5 to MUST or add language to AGENTS.md clarifying that readme.md files in operational folders are a SHOULD exception.

### Task 037 — Amending PRE_COMMIT.md

- **CONTR-001:** §2's Global Readme Audit is the mechanical source of CONTR-001. Adding a clarifying note would neutralize it: "This batch update satisfies the pre-commit batching contract in FOLDERS.md §3 and does NOT constitute the per-file administrative overhead that FRUSTRATED.md §28 flags as FL2; the FL2 trigger applies only to prompts that require per-file updates as an inline task step, not to the single pre-commit batch step itself."
- **CONTR-005:** §7 references check-governance.sh but does not mention the bypass mode. Add a cross-reference to MAINTENANCE.md §4.1.
- **CONTR-007:** Harmonize §3's "PR description or commit message" wording with FRUSTRATED.md §32's "PR description or submit message."

### Task 038 — Amending FRUSTRATED.md

- **CONTR-001:** §28's FL2 trigger should be revised to clarify that the example parenthetical refers to *mid-session inline* readme updates, not the mandatory single pre-commit batch mandated by PRE_COMMIT.md §2 and FOLDERS.md §3.
- **CONTR-006 / CONTR-007:** §32 item 2 should note: "When a session produces a Task closed as done/updated/abandoned, a `friction-log.md` is required per TASK.md §7 and supersedes this inline-log guidance."
- **CONTR-008:** §28's "less than 3 files per folder" trigger should be aligned with FOLDERS.md §4's 4-file subfolder threshold. Change to "less than 4 files per folder" or adjust the prose to describe the pattern more precisely.

### Task 039 — Amending MAINTENANCE.md

- **CONTR-004:** §1's T3 tier table has an absolute "MUST NOT fix directly" that conflicts with §3.4's 1→1 supersession exception. Add a footnote: "Exception (§3.4): ordinary 1→1 Task supersessions, where all mutations are frontmatter-only and reversible, MAY be performed directly by the maintenance agent without filing a separate Task."
- **CONTR-005:** §4.1's bypass mode should cross-reference AGENTS.md SS.2: "The bypass described in this section applies to the pre-commit hook's commit-blocking behavior, not to the session-start governance check mandated by AGENTS.md SS.2."
- **CONTR-012:** §2.1's SessionStart Coherence Check recommendation should note: "The Coherence Check MUST be preceded by `./install.sh` per AGENTS.md SS.1. If wired as a SessionStart hook, the hook itself MUST invoke `./install.sh` before reading `maintenance/run-log.md`."

---

## §5 Summary Statistics

### Total Contradictions Found

**16 contradictions cataloged** (CONTR-001 through CONTR-016).

### By Type

| Type | Count | Entries |
|---|---|---|
| Direct | 4 | CONTR-001, CONTR-004, CONTR-005, CONTR-011 |
| Indirect | 2 | CONTR-008, CONTR-012 |
| Scope-overlap | 7 | CONTR-002, CONTR-003, CONTR-007, CONTR-009, CONTR-013, CONTR-014, CONTR-015 |
| Lifecycle | 3 | CONTR-006, CONTR-010, CONTR-016 |

### By Severity

| Severity | Count | Entries |
|---|---|---|
| High | 5 | CONTR-001, CONTR-004, CONTR-005, CONTR-006, CONTR-014 |
| Medium | 7 | CONTR-002, CONTR-003, CONTR-008, CONTR-009, CONTR-010, CONTR-011, CONTR-013 |
| Low | 4 | CONTR-007, CONTR-012, CONTR-015, CONTR-016 |

### Previously Known vs Newly Discovered

| Category | Count | Entries |
|---|---|---|
| Previously known (documented anchor) | 1 | CONTR-001 |
| Newly discovered by this analysis | 15 | CONTR-002 through CONTR-016 |

### Spec Involvement Heat Map

| Spec | Contradictions Involving It |
|---|---|
| TASK.md | 5 (CONTR-006, CONTR-009, CONTR-010, CONTR-013, CONTR-014) |
| PRE_COMMIT.md | 4 (CONTR-001, CONTR-002, CONTR-007, CONTR-016) |
| AGENTS.md | 4 (CONTR-005, CONTR-009, CONTR-012, CONTR-015) |
| FRUSTRATED.md | 4 (CONTR-001, CONTR-006, CONTR-007, CONTR-008) |
| FOLDERS.md | 4 (CONTR-001†, CONTR-002, CONTR-003, CONTR-008) |
| RESEARCH.md | 4 (CONTR-003, CONTR-010, CONTR-011, CONTR-016) |
| MAINTENANCE.md | 3 (CONTR-004, CONTR-005, CONTR-012) |
| PROMPT.md | 2 (CONTR-007, CONTR-014) |

† CONTR-001 names FOLDERS.md §3 as an agreeing party: §3's "Update Trigger" prose is the direct source of the batching-unit conflict.

### High-Risk Cluster

The three specs most likely to generate agent errors on existing tasks are **FRUSTRATED.md**, **PRE_COMMIT.md**, and **TASK.md** — they share the friction-log-placement cluster (CONTR-001, CONTR-006, CONTR-014) where mechanical linter checks conflict with spec-mandated informal locations. Any agent that reads FRUSTRATED.md §32 before TASK.md §7 will produce commits that fail `tools/check-trust.py`.
