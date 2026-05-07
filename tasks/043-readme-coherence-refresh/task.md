---
type: task
status: active
slug: readme-coherence-refresh
summary: "R.13/R.14-gated README restructure: reframe §1+§3 to a four-concern model (add Capability/Skills) and add §12 Narrative Ontology pointer."
created: 2026-05-07
updated: 2026-05-07
task_id: "043"
task_status: open
task_owner: "unassigned"
task_priority: P2
task_uses_prompts: []
task_spawns_research: []
task_spawns_prompts: []
task_affects_paths:
  - README.md
  - FOLDERS.md
  - decisions/0001-agency-system-prototype-exemption.md
---

# Task 043 — README Coherence Refresh (Wave B)

## Goal

Reframe the README's mental-model from a three-concern model (Machine / Actor / Space)
to a four-concern model that elevates `/skills/` to a peer **Capability** layer, in lockstep with
[FOLDERS.md §1](../../FOLDERS.md) and [AGENTS.md Task Type Routing](../../AGENTS.md). Add a new
top-level §12 *Narrative Ontology (load-gated)* that points at AGENTS.md NO.1–NO.6 + the schema
directory under `maintenance/schemas/narrative-ontology/`. Open the backing ADRs that legitimise
`/Agency-System/` and (if accepted) `/tests/` as exempt non-operational folders.

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
6. **Disposition for `/tests/`.** Either (a) author ADR 0002 adding it to FOLDERS.md §8
   (consistent with where the pytest suites for `tools/adr/` and `tools/fm/` live), or
   (b) move the suites under `tools/tests/`. Decision is captured in the ADR; the README
   topology note flagging `/tests/` as "unreconciled" is removed.
7. **Spec-panel review** (`/sc:spec-panel`) of the candidate diff against R.1–R.20 and the
   §11.5 Gherkin acceptance criteria.
8. **Self-review** (`/sc:reflect`) before the closing run.
9. **Closing run** per AGENTS.md CR.1: `git push` → `/sc:createPR`. The PR body MUST cite
   this Task slug and the FL declaration.

## Todo

- [ ] 1. Refresh `/sc:analyze` finding table on this branch's HEAD; pin to line numbers.
- [ ] 2. Reframe README §1 + §3 to the four-concern model (Capability = `/skills/`).
- [ ] 3. Update the strapline and §2 to match the new framing.
- [ ] 4. Remove the "pending reframe" callout added in Wave A.
- [ ] 5. Add §12 Narrative Ontology (load-gated) per AGENTS.md NO.1–NO.6.
- [ ] 6. Append R.21 (or similar) to §11.3 if a new trigger emerges; respect R.10.
- [ ] 7. Draft `decisions/0001-agency-system-prototype-exemption.md` (`adr_status: Proposed`).
- [ ] 8. Decide `/tests/` disposition; capture in ADR 0002 or move suites under `tools/tests/`.
- [ ] 9. Run `python3 tools/adr/cli.py validate` then `synthesize` once ADRs are `Accepted`.
- [ ] 10. Run `/sc:spec-panel` on the candidate diff.
- [ ] 11. Run `/sc:reflect` for the final pass.
- [ ] 12. `tools/check-governance.sh` MUST exit 0.
- [ ] 13. Close with `/sc:createPR`; PR body cites this slug + FL declaration.

## Links

- Upstream Wave A commits on this branch: `4401cdd` (README), `3a5c09a` (FOLDERS.md §8).
- Governing specs: [`TASK.md`](../../TASK.md), [`PROMPT.md`](../../PROMPT.md), [`RESEARCH.md`](../../RESEARCH.md), [`FOLDERS.md`](../../FOLDERS.md), [`SKILLS.md`](../../SKILLS.md), [`MAINTENANCE.md`](../../MAINTENANCE.md).
- ADR target: [`decisions/readme.md`](../../decisions/readme.md), [`tools/adr/cli.py`](../../tools/adr/cli.py).
- Narrative ontology source of truth: [`AGENTS.md` Narrative Ontology section](../../AGENTS.md), `maintenance/schemas/narrative-ontology/`.
- README binding spec: [README.md §11](../../README.md#11-spec--how-this-readme-must-be-updated) (R.13, R.14, R.10, R.15).
