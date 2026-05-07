---
type: task
status: active
slug: github-workflow-research
summary: "Research and decide a maintainable GitHub Actions strategy for the repo (governance gate + pytest + ADR synthesis check) and replace the deleted adr-validate.yml."
created: 2026-05-07
updated: 2026-05-07
task_id: "046"
task_status: open
task_owner: "unassigned"
task_priority: P2
task_uses_prompts: []
task_spawns_research: []
task_spawns_prompts: []
task_affects_paths:
  - .github/workflows/
  - decisions/
---

# Task 046 — GitHub Workflow Research

## Goal

Research and decide on a *good* GitHub Actions strategy for `netzkontrast/agency` and
land an ADR + replacement workflow(s). The previous CI surface was a single
`.github/workflows/adr-validate.yml` that triggered on every push touching
`tests/adr/**`, `decisions/**`, `AGENTS.md`, `tools/adr/**`, or
`maintenance/schemas/header-ontology.json`. It was removed on branch
`claude/update-root-readme-Qufdr` because piecemeal MCP commits during the
`/tests/` → `/tools/tests/` relocation each fired the workflow against
half-moved trees, generating noisy failures. The replacement MUST be designed
holistically rather than re-introduced ad-hoc.

The Task is `done` when:

1. An ADR (`decisions/<NNNN>-github-actions-strategy.md`) is `Accepted` and synthesised
   into the AGENTS.md guarded section via `tools/adr/cli.py synthesize`.
2. One or more workflow files under `.github/workflows/` implement that ADR's
   contract and pass on `main` and a representative feature branch.
3. README.md §6 (or §6.2 if the strategy lives in a sub-section) cites the
   workflow set so humans know what fires when.
4. `tools/check-governance.sh` exits 0 on the final commit.
5. The PR opened by `/sc:createPR` cites this Task slug and the FL declaration.

## Plan

The goal is to *design before reintroducing*. No workflow file is to be
authored before the ADR is `Accepted`.

1. **Inventory the gates.** Catalogue every check that should run in CI:
   - `./install.sh` succeeds
   - `tools/check-governance.sh --no-trust` exits 0
   - `python -m pytest tools/tests/adr/ -q` passes
   - `python -m pytest tools/tests/fm/ -q` passes
   - `python3 tools/adr/cli.py synthesize --dry-run` and the AGENTS.md
     guarded-section diff gate (the "synthesise is committed" check)
   - Optional: narrative-ontology validator when the ontology file exists
     (`tools/dramatica-nav/validate.py`)
2. **Inventory the trigger surfaces.** Decide which paths each gate should
   trigger on. Avoid the prior failure mode where unrelated edits to
   `tests/adr/**` re-ran the whole gate; group gates by *what they protect*,
   not by *what they read*.
3. **Author research/<slug>/output/SPEC.md** under `/research/github-actions-strategy/`
   per [RESEARCH.md](../../RESEARCH.md). The SPEC MUST address:
   - Single workflow vs. multiple workflows (one per gate vs. one omnibus)
   - Path filters vs. always-run
   - Concurrency control (`concurrency:` group on branch-name to cancel
     superseded runs — relevant for rapid push sequences)
   - Failure surfacing (job summaries, annotations, artefacts)
   - Whether to gate PR merging on green CI via branch protection (out of
     scope of the workflow file itself but in-scope for the ADR's "consequences")
   - Cost / minutes budget
   - Caching (pip cache, `actions/setup-python` cache, etc.)
   - How CI relates to the local pre-commit hook — the hook is currently the
     authoritative gate; CI was advisory. Decide whether that stays.
4. **Author the ADR.** `decisions/<NNNN>-github-actions-strategy.md` with the
   canonical MADR sections, citing the SPEC for evidence. `adr_status: Proposed`
   first; flip to `Accepted` after review.
5. **Implement the workflow(s)** under `.github/workflows/` matching the ADR.
   Verify each fires only when intended on a feature branch with surgical
   path-touches.
6. **Update README.md** to mention the workflow set per R.7 / R.9 (whichever
   triggers apply once the implementation lands).
7. **Spec-panel review** (`/sc:spec-panel`) of the candidate diff.
8. **Closing run** per AGENTS.md CR.1: `git push` → `/sc:createPR`.

## Todo

- [ ] 1. Inventory the gates per Plan §1.
- [ ] 2. Inventory the trigger surfaces per Plan §2.
- [ ] 3. Author `research/github-actions-strategy/output/SPEC.md` per Plan §3.
- [ ] 4. Author the ADR (`decisions/<NNNN>-github-actions-strategy.md`) and flip to `Accepted` after review.
- [ ] 5. Implement workflow(s) under `.github/workflows/` matching the ADR.
- [ ] 6. Update `README.md` to mention the workflow set.
- [ ] 7. Run `/sc:spec-panel` review of the candidate diff.
- [ ] 8. Closing run per AGENTS.md CR.1: `git push` → `/sc:createPR`.

## Open Questions (for the ADR to answer)

- **OQ-1.** Should the ADR-synthesis diff gate (the "AGENTS.md guarded section
  is stale" check from the deleted workflow) live in the same job as the
  pytest run, or in its own workflow? The prior coupling meant a flaky test
  run blocked an unrelated ADR diff check.
- **OQ-2.** Should we run the FM toolchain tests (`tools/tests/fm/`) on every
  push, or only on `tools/fm/**` and `tools/tests/fm/**` changes?
- **OQ-3.** Branch-protection: should `main` require this workflow green
  before merge? If yes, who has permission to override?
- **OQ-4.** Do we want a separate "lint" job (frontmatter-only) that's fast
  and gates everything else? `tools/check-governance.sh` already does the
  full sweep — splitting it may or may not be worth the YAML.
- **OQ-5.** What's the policy for workflows on `claude/**` branches? The
  prior workflow ran on every `claude/**` push, which was useful for
  ground-truth feedback but expensive when the branch generated many
  intermediate commits.

## Halt Condition

If during step 1 the inventory reveals that `tools/check-governance.sh`
itself needs significant refactoring before CI can wrap it, STOP and file a
predecessor Task that hardens the local gate first. CI MUST NOT diverge from
the local hook in *what* it runs — only in *when*.

## Links

- Branch context: `claude/update-root-readme-Qufdr` removed `.github/workflows/adr-validate.yml`
  in the same commit that moved `/tests/` → `/tools/tests/`.
- Predecessor failure mode: PR #76 webhook history shows seven failed runs
  caused by piecemeal MCP commits firing the workflow against half-moved trees.
- Governing specs: [`TASK.md`](../../TASK.md), [`RESEARCH.md`](../../RESEARCH.md),
  [`PROMPT.md`](../../PROMPT.md), [`MAINTENANCE.md`](../../MAINTENANCE.md).
- ADR target: [`decisions/readme.md`](../../decisions/readme.md), [`tools/adr/cli.py`](../../tools/adr/cli.py).
- Local gate (already authoritative): [`tools/check-governance.sh`](../../tools/check-governance.sh).
