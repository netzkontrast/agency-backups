---
type: task
status: active
slug: deepwiki-integration-artifact
summary: "Reflect on the Gemini DeepWiki research result; derive the Machine/Actor/Space isomorphic map for this repository; produce .devin/wiki.json that steers DeepWiki to generate human-readable documentation covering current state, how we got here, and what is next."
created: 2026-05-07
updated: 2026-05-07
task_id: "052"
task_status: open
task_owner: "claude"
task_priority: P1
task_uses_prompts:
  - deepwiki-rendering-conventions-agentic-workflows
task_spawns_research: []
task_spawns_prompts: []
task_supersedes: []
task_superseded_by: []
task_blocked_by:
  - "051"
task_affects_paths:
  - .devin/wiki.json
  - tasks/052-deepwiki-integration-artifact/
  - research/gemini/deepwiki-rendering-conventions-agentic-workflows/result.md
---

# Task 052 — DeepWiki Integration Artifact

## Goal

Produce `.devin/wiki.json` — a deterministic steering file that causes DeepWiki to
generate human-readable documentation about **how this repository works, how to
navigate it, how we got here, and what is next**. DeepWiki's role is integrator and
consolidator, not author.

The artifact must be grounded in a prior reflection pass over the Gemini research
result (`research/gemini/deepwiki-rendering-conventions-agentic-workflows/result.md`)
and must encode a **Machine · Actor · Space** isomorphic map as explicit indexer
context.

---

## Two-Phase Execution Plan

### Phase 1 — Reflection (input: Task 051 analysis + Gemini result)

Produce `tasks/052-deepwiki-integration-artifact/reflection.md`.

The reflection answers five questions, each grounded in the Gemini research:

1. **Which `.devin/wiki.json` conventions apply directly to this repo?**
   Identify which `repo_notes` / `pages` patterns from the research fit the
   `netzkontrast/agency` folder topology. Note any that do NOT apply and why.

2. **What is the correct page budget?**
   Validate against the 30-page standard limit. Count the proposed pages below
   and confirm budget compliance. Flag any pages that could be merged.

3. **What are the highest-risk indexer blind spots?**
   Apply M03 Pre-Mortem: if DeepWiki produced wrong documentation for this repo,
   what would the top three failure modes be? Map each to a mitigation in the
   `repo_notes` array.

4. **Where does the human-vs-agent utility dichotomy bite us?**
   The research benchmarks show DeepWiki optimises for human presentation at the
   cost of agent referencing density. For this repo the primary audience is human.
   Confirm this is the correct optimisation target and note any agent-utility
   concessions that should still be made (e.g. explicit file paths in `purpose`
   fields).

5. **Is the Machine · Actor · Space map isomorphic?**
   Verify that the three columns below are in 1:1:1 correspondence — no Space
   without a canonical Actor, no Space without a canonical Machine. Flag gaps.

The reflection document is the audit trail for every `repo_notes` entry and every
`pages` entry in the deliverable. Every claim in `.devin/wiki.json` must be
traceable to a line in `reflection.md`.

---

### Phase 2 — Integration Artifact (deliverable: `.devin/wiki.json`)

Produce `.devin/wiki.json` at the repository root using the structure below.
All `purpose` fields MUST reference exact file paths or directory names.

---

## The Machine · Actor · Space Map

This isomorphic three-column map is the conceptual core of the documentation.
It MUST appear verbatim as a `repo_notes` entry so the DeepWiki LLM indexer
has it as explicit context.

| Space (directory) | Actor (canonical operator) | Machine (enforcement layer) |
|---|---|---|
| `/` root | Human maintainer | `tools/check-governance.sh`, `.githooks/pre-commit` |
| `/prompts/` | Human (intent author) + Claude Code | `tools/lint-linkage.py`, `tools/fm/validate` |
| `/research/` | Claude Code + External agents (Gemini) | `tools/lint-structure.py`, `tools/fm/validate` |
| `/tasks/` | Claude Code + Human reviewer | `tools/lint-linkage.py`, `tools/fm/validate`, `tools/check-task-lifecycle-classification.py` |
| `/decisions/` | Human architect + Claude Code | `tools/adr/` CLI (`agency-adr`) |
| `/skills/` | Human + Claude Code | `tools/fm/validate` |
| `/tools/` | Claude Code (implementation) | `tools/tests/` (pytest), `tools/lint-runlog.py` |
| `/Agency-System/` | Frontend/backend product layer | Separate from governance framework |
| `/maintenance/` | Claude Code (maintenance runs) | `tools/lint-runlog.py`, `tools/check-maintenance-bypass.py` |
| `/templates/` | Human + Claude Code | `tools/fm/validate` |

**Isomorphism invariant:** every Space has exactly one canonical Actor role and
exactly one canonical Machine enforcer. Gaps in either column are governance debt.

---

## Proposed `.devin/wiki.json` Page Structure

Sixteen pages, organised as a three-level hierarchy. Parent pages provide
orientation; child pages provide depth.

### Tier 1 — Repository Identity (root pages, no parent)

| # | Title | Key files to reference |
|---|---|---|
| 1 | Repository Overview | `README.md`, `AGENTS.md §1` |
| 2 | How This Repo Works | `PROMPT.md`, `RESEARCH.md §1`, `TASK.md §1` |
| 3 | How to Navigate | `FOLDERS.md`, root spec file list |
| 4 | Machine · Actor · Space Map | `tools/check-governance.sh`, `tools/fm/`, `tools/adr/`, `decisions/` |

### Tier 2 — Governance Layer (parent: "Governance Layer")

| # | Title | Key files to reference |
|---|---|---|
| 5 | The Nine Root Specs | All nine root `*.md` governance files |
| 6 | Session Protocol | `AGENTS.md §Session Setup`, `install.sh` |
| 7 | Frontmatter Schema | `decisions/0003-frontmatter-source-of-truth.md`, `tools/fm/SPEC.md` |
| 8 | Pre-Commit Enforcement | `PRE_COMMIT.md`, `.githooks/pre-commit`, `tools/check-governance.sh` |

### Tier 3 — Working Layers (parent: their respective layer name)

| # | Title | Parent | Key files to reference |
|---|---|---|---|
| 9 | Prompts — The Intent Layer | How This Repo Works | `PROMPT.md`, `prompts/readme.md` |
| 10 | Research — The Evidence Layer | How This Repo Works | `RESEARCH.md §2-§6`, `research/readme.md` |
| 11 | Tasks — The Coordination Layer | How This Repo Works | `TASK.md §3`, `tasks/readme.md` |
| 12 | Decisions (ADRs) | How This Repo Works | `decisions/0001-0005`, `tools/adr/` |
| 13 | Skills — Capability Registry | How This Repo Works | `SKILLS.md`, `skills/readme.md` |
| 14 | Toolchain — The Machine Layer | Machine · Actor · Space Map | `tools/readme.md`, `tools/fm/`, `tools/adr/` |

### Tier 4 — History & Horizon

| # | Title | Key files to reference |
|---|---|---|
| 15 | How We Got Here | `decisions/0001-0005`, `maintenance/run-log.md`, Tasks 032–039 amendment chain |
| 16 | What Is Next | `tasks/readme.md` (open tasks), `prompts/` (in-flight prompts) |

---

## `repo_notes` Injection Strategy

The `repo_notes` array should carry five notes, in priority order:

| Priority | Note content | Mitigation target |
|---|---|---|
| N1 | The Machine · Actor · Space map verbatim (table above) | Prevents indexer from conflating governance layer with product layer |
| N2 | "This repo is spec-first: AGENTS.md, TASK.md, RESEARCH.md, PROMPT.md, FOLDERS.md, SKILLS.md, FRUSTRATED.md, MAINTENANCE.md, PRE_COMMIT.md are the nine root governance specs. Every file in /prompts/, /research/, /tasks/ carries frontmatter that cross-references these specs. The tools/ layer mechanically enforces these cross-references." | Prevents spec files being treated as casual documentation |
| N3 | "The Prompt → Research → Task pipeline is the core workflow: a prompt in /prompts/ is executed by an agent to produce a workspace in /research/; coordination and sequencing lives in /tasks/. Each step requires frontmatter linkage validated by tools/lint-linkage.py." | Prevents pipeline stages being documented in isolation |
| N4 | "The 032–039 amendment chain (May 2026) updated all eight root governance specs in a coordinated sequence. See tasks/032-039 and decisions/0001-0005 for the rationale. Do not interpret any single spec in isolation from this chain." | Prevents outdated or partial spec interpretation |
| N5 | "Agency-System/ is a separate product layer (frontend HTML/JS + Python/FastAPI backend). It is NOT part of the governance framework. FOLDERS.md §8 exempts it from frontmatter requirements." | Prevents indexer treating Agency-System as core governance |

---

## Acceptance Criteria

- [ ] `tasks/052-deepwiki-integration-artifact/reflection.md` exists and answers all five reflection questions with file-path citations.
- [ ] `.devin/wiki.json` exists at repo root and is valid JSON.
- [ ] `repo_notes` contains ≥ 5 entries, each ≤ 10 000 characters.
- [ ] `pages` contains exactly 16 entries (within the 30-page standard limit).
- [ ] Every `purpose` field in `pages` references at least one exact file path or directory name.
- [ ] The Machine · Actor · Space table appears verbatim in `repo_notes[0].content`.
- [ ] `reflection.md` traces each `repo_notes` entry and each `pages` entry to a finding or mitigation.
- [ ] `tasks/readme.md` updated to include Task 052.
