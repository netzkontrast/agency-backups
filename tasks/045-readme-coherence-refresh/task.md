---
type: task
status: active
slug: readme-coherence-refresh
summary: "R.13/R.14-gated README restructure: reframe §1+§3 to a four-concern model (add Capability/Skills) and add §12 Narrative Ontology pointer."
created: 2026-05-07
updated: 2026-05-08
task_id: "045"
task_status: done
task_owner: "claude-opus-4-7"
task_priority: P2
task_uses_prompts: []
task_spawns_research: []
task_spawns_prompts: []
task_affects_paths:
  - README.md
  - FOLDERS.md
  - decisions/0001-agency-system-prototype-exemption.md
---

# Task 045 — README Coherence Refresh (Wave B)

## Goal

Reframe the README's mental-model from a three-concern model (Machine / Actor / Space)
to a four-concern model that elevates `/skills/` to a peer **Capability** layer, in lockstep with
[FOLDERS.md §1](../../FOLDERS.md) and [AGENTS.md Task Type Routing](../../AGENTS.md). Add a new
top-level §12 *Narrative Ontology (load-gated)* that points at AGENTS.md NO.1–NO.6 + the schema
directory under `maintenance/schemas/narrative-ontology/`. Open the backing ADR that legitimises
`/Agency-System/` as an exempt non-operational folder.

> **Update — `/tests/` resolved upstream.** The `/tests/` disposition originally bundled
> here was resolved on the parent branch `claude/update-root-readme-Qufdr` by relocating
> the suites under `/tools/tests/` (per PR #76 review F2, option b2). `/tools/tests/` is
> exempt-by-inheritance through the `/tools/` row in FOLDERS.md §8; no ADR is required.
> Steps 1.6 and Todo item 8 below are therefore complete; Task 046 picks up the related
> CI/workflow question.

The Task is `done` when:

1. README §1 + §3 frame the repo as four decoupled concerns (Machine / Actor / Space / Capability).
2. README §12 exists, describes the load-gated narrative ontology, and links to AGENTS.md NO.1–NO.6.
3. README rule identifiers R.1–R.20 retain their numeric values; new rules append at R.21+ if any.
4. `decisions/0001-agency-system-prototype-exemption.md` is `Accepted` and `tools/adr/cli.py synthesize`
   has rewritten the AGENTS.md guarded block accordingly.
5. `tools/check-governance.sh` exits 0 on the final commit.
6. The PR opened by `/sc:createPR` cites this Task slug and a friction log declaration.

## Plan

This Task is the **R.13/R.14 vehicle** for changes that the upstream session
(branch `claude/update-root-readme-Qufdr`, Wave A commits 4401cdd + 3a5c09a)
explicitly deferred. Wave A closed the inline-safe drift fixes; this Task
covers everything that requires a Task per R.13 or that crosses the T3
Structural threshold per R.14.

The plan is executed via the SuperClaude command chain documented in
**§ SuperClaude Command Chain** below. The numbered steps here describe
*what* changes; the command chain describes *how* and in *what order*.

1. **Audit pass.** Re-run `/sc:analyze` against README.md + FOLDERS.md + AGENTS.md to confirm
   the gap inventory (F1 reframe, F4 ADR backing, F7 narrative ontology, plus `/tests/` disposition).
   Output: an updated finding table referencing exact line numbers on this branch.
2. **Reframe §1 + §3** (R.14 — T3 Structural; this Task is the authorised vehicle).
   - §1 table grows to four rows (`Machine / Actor / Space / Capability`).
   - §3 gains a sub-section 3.4 — *Capability — `/skills/`* — summarising SKILLS.md.
   - Every textual occurrence of the three-concern slogan is updated; the strapline at
     the top of README.md is rewritten to match.
   - The "pending reframe" callout added to §1 in Wave A is removed.
3. **Add §12 Narrative Ontology (load-gated)** (R.13 — new top-level numbered section).
   - One paragraph stating the ontology is *separate from* the Frontmatter Ontology and
     load-gated by AGENTS.md NO.1–NO.6.
   - Link to `maintenance/schemas/narrative-ontology/` and `tools/dramatica-nav/nav.py`.
   - Explicit non-load rule for non-narrative work (NO.5).
4. **Append rule R.21** to §11.3 if a new trigger emerges (e.g. *"a new schema corpus is
   added under `maintenance/schemas/<name>/` — §12 MUST mention it"*). Existing R.x identifiers
   MUST remain stable per R.10.
5. **Author ADR 0001** — `decisions/0001-agency-system-prototype-exemption.md`:
   - MADR 4.0.0 sections (Context, Drivers, Considered Options, Decision Outcome, Consequences).
   - `adr_status: Proposed` first; flip to `Accepted` after review.
   - Records that `/Agency-System/` is a frontend-prototype storage folder consumed by
     `skills/the-agency-system-architect/` and exempt from §1 / §7 of FOLDERS.md.
   - Run `python3 tools/adr/cli.py validate` and then `synthesize`.
6. ~~**Disposition for `/tests/`.**~~ **Resolved upstream** on
   branch `claude/update-root-readme-Qufdr`: option (b) was chosen and the suites were
   moved under `/tools/tests/`. No ADR was needed — `/tools/tests/` is exempt-by-
   inheritance through the `/tools/` row in [FOLDERS.md §8](../../FOLDERS.md). The
   README topology note flagging `/tests/` as "unreconciled" was removed in the same
   commit. The CI/workflow question raised by the relocation moves to **Task 046**
   ([github-workflow-research](../046-github-workflow-research/)).
7. **Spec-panel review** (`/sc:spec-panel`) of the candidate diff against R.1–R.20 and the
   §11.5 Gherkin acceptance criteria.
8. **Self-review** (`/sc:reflect`) before the closing run.
9. **Closing run** per AGENTS.md CR.1: `git push` → `/sc:createPR`. The PR body MUST cite
   this Task slug and the FL declaration.

## SuperClaude Command Chain

Execute these in order. Each step's output feeds the next; do not parallelise.

| # | Command | Purpose | Plan steps | Inputs | Outputs |
|---|---|---|---|---|---|
| 1 | [`/sc:analyze`](../../skills/sc-analyze/) `target=README.md,FOLDERS.md,AGENTS.md focus="reframe + ADR backing + narrative ontology" depth=deep` | Refresh the gap inventory against this branch's HEAD; pin findings to line numbers. | 1 | Branch HEAD; README §11 R.x rules; FOLDERS.md §1 + §8; AGENTS.md NO.1–NO.6. | Updated finding table; severity ratings; explicit cross-references for the reframe. |
| 2 | [`/sc:workflow`](../../skills/sc-workflow/) `task=045 source=task.md format=structured` | Sequence plan steps 2–6 with dependencies + commit boundaries. | 2–6 | Step 1's finding table; this Task's plan. | Ordered workflow: §3 reframe ⇒ §12 add ⇒ R.21 (if any) ⇒ ADR 0001 ⇒ `/tests/` disposition. |
| 3a | [`/sc:document`](../../skills/sc-document/) `target=README.md sections="strapline,§1,§3,§3.4,§12" style=spec-aligned` | Draft the four-concern reframe and the new §12 prose. | 2, 3 | Workflow from step 2; SKILLS.md §3.3 + §4; AGENTS.md NO.1–NO.6. | Candidate README diff; preserves R.1–R.20; appends R.21 if needed. |
| 3b | [`/sc:document`](../../skills/sc-document/) `target=decisions/0001-agency-system-prototype-exemption.md style=madr-4.0.0` | Author ADR 0001 (and ADR 0002 if `/tests/` decision requires one). | 5, 6 | `decisions/readme.md`; `research/adr-spec-research-synthesis/output/SPEC.md`; FOLDERS.md §8. | `adr_status: Proposed` ADR(s) ready for `tools/adr/cli.py validate`. |
| 4 | `python3 tools/adr/cli.py validate && python3 tools/adr/cli.py synthesize` | Validate the ADR(s); once `Accepted`, rewrite the AGENTS.md guarded block. | 5, 6 | Step 3b ADR(s). | Validated ADRs; rewritten `<!-- BEGIN AGENCY-ADR SYNTHESIS -->` block in AGENTS.md. |
| 5 | [`/sc:spec-panel`](../../skills/sc-spec-panel/) `target=README.md,decisions/0001-*.md acceptance=README.md#115-acceptance-criteria` | Multi-expert review against R.1–R.20 and the §11.5 Gherkin scenarios (RM.1.1–RM.1.4). | 7 | Steps 3a/3b candidate diff + step 4 synthesis output. | Pass/fail per Gherkin scenario; required revisions. |
| 6 | [`/sc:reflect`](../../skills/sc-reflect/) `scope=task-045 acceptance=goal-conditions` | Validate goal conditions 1–6; re-run `tools/check-governance.sh`. | 8 | Working tree after step 5 revisions. | Goal-condition checklist; final friction log entry (FL0–FL3). |
| 7 | [`/sc:createPR`](../../skills/sc-createPR/) | Closing run per AGENTS.md CR.1. | 9 | All preceding outputs; clean working tree. | PR citing Task 045 slug + FL declaration; CR.1.1 satisfied. |

**Branching note.** This Task currently lives on `claude/update-root-readme-Qufdr`
alongside Wave A. The next session MAY split it onto its own branch
(suggested: `claude/task-045-readme-coherence-refresh`) before step 1; the
command chain is branch-agnostic.

**Halt conditions.** If step 1's finding table contradicts this plan
(e.g. the `/skills/` peer-elevation has been reverted upstream, or AGENTS.md
NO.1–NO.6 has been removed), STOP and re-scope this Task before continuing.
The chain is not robust to silent upstream drift; that's by design — R.20
forbids the README from contradicting any root spec.

## Todo

- [ ] 1. **(Step 1)** Refresh `/sc:analyze` finding table on this branch's HEAD; pin to line numbers.
- [ ] 2. **(Step 2)** Run `/sc:workflow` to sequence the §3 reframe + §12 add + ADR work with commit boundaries.
- [ ] 3. **(Step 3a)** Draft README §1 + §3 four-concern reframe via `/sc:document`.
- [ ] 4. **(Step 3a)** Add README §12 *Narrative Ontology (load-gated)* via `/sc:document`.
- [ ] 5. **(Step 3a)** Update strapline + §2 to match the new framing; remove the Wave A "pending reframe" callout.
- [ ] 6. **(Step 3a)** Append R.21 (or similar) to §11.3 if a new trigger emerges; respect R.10.
- [ ] 7. **(Step 3b)** Draft `decisions/0001-agency-system-prototype-exemption.md` (`adr_status: Proposed`).
- [x] 8. **(Step 3b)** ~~Decide `/tests/` disposition~~ — done upstream: suites moved to `/tools/tests/`; CI/workflow follow-up tracked by [Task 046](../046-github-workflow-research/).
- [ ] 9. **(Step 4)** Run `python3 tools/adr/cli.py validate`; flip ADR(s) to `Accepted`; run `synthesize`.
- [ ] 10. **(Step 5)** Run `/sc:spec-panel` on the candidate diff against §11.5 Gherkin (RM.1.1–RM.1.4).
- [ ] 11. **(Step 6)** Run `/sc:reflect`; verify goal conditions 1–6; `tools/check-governance.sh` MUST exit 0.
- [ ] 12. **(Step 7)** Close with `/sc:createPR`; PR body cites this slug + FL declaration.

## Links

- Upstream Wave A commits on this branch: `4401cdd` (README), `3a5c09a` (FOLDERS.md §8).
- Upstream main between branch-cut and Task open: includes `043-renumber-duplicate-task-ids-v3` and `044-improve-maintenance-spec-may-07-2026`; this Task takes slot `045` after a same-day rename from `043` to avoid collision.
- Governing specs: [`TASK.md`](../../TASK.md), [`PROMPT.md`](../../PROMPT.md), [`RESEARCH.md`](../../RESEARCH.md), [`FOLDERS.md`](../../FOLDERS.md), [`SKILLS.md`](../../SKILLS.md), [`MAINTENANCE.md`](../../MAINTENANCE.md).
- ADR target: [`decisions/readme.md`](../../decisions/readme.md), [`tools/adr/cli.py`](../../tools/adr/cli.py).
- Narrative ontology source of truth: [`AGENTS.md` Narrative Ontology section](../../AGENTS.md), `maintenance/schemas/narrative-ontology/`.
- README binding spec: [README.md §11](../../README.md#11-spec--how-this-readme-must-be-updated) (R.13, R.14, R.10, R.15).
