---
type: prompt
status: active
slug: core-architecture-review-2026-05
summary: "Audit Agency's Machine/Actor/Space substrate, the tools/fm/ toolchain, and the governance pipeline. Produce a 10-finding architectural review with line-anchored citations and a triage matrix mapping each finding to an existing or new follow-up Task."
created: 2026-05-07
updated: 2026-05-07
prompt_kind: research-proposal
prompt_framework: RISEN+ReAct
prompt_target_agent: "Claude Code"
prompt_relates_to_task: "core-architecture-review-followups"
---

# Core Architecture Review (2026-05) — Prompt

## Framework

**RISEN+ReAct.** RISEN scopes the audit (Role, Input, Steps, Expectations, Constraints); ReAct is required because the executor MUST traverse the live spec corpus and tooling (grep, file-reads, line-anchor verification) iteratively before synthesising findings. The output is structured (10 findings) but the path to those findings is exploratory.

## R — Role

You are an architectural auditor reviewing the `agency` repository as a long-horizon governance substrate. You critique boundary discipline (Machine/Actor/Space), tooling, spec coherence, and audit-graph completeness — and you call out the repo's own self-violations the same way you call out external defects.

## I — Input

You MUST read these files at the commit pinned in `task.md` `## Provenance` (`main@dbd996f` for the 2026-05-07 run):

- `README.md` — the four-concern model, the spec catalogue, the rules R.1–R.19.
- `AGENTS.md` — entry-point routing, narrative-ontology rules NO.1–NO.6, closing-run procedure.
- `TASK.md`, `PROMPT.md`, `RESEARCH.md`, `FOLDERS.md`, `PRE_COMMIT.md`, `FRUSTRATED.md`, `MAINTENANCE.md`.
- `tools/fm/_core.py`, `tools/fm/validate.py` — the canonical frontmatter toolchain.
- `tools/check-governance.sh`, `tools/lint-linkage.py`, `tools/check-maintenance-bypass.py` — the gate.
- `tests/fm/test_falsification_attacks.py` — adversarial test pattern.
- `tasks/readme.md` — Task index (membership, statuses, lineage).

You SHOULD use `git log --oneline -50 main`, `grep -rn`, and `ls tasks/` to triangulate which findings already have an owning Task before asserting a "no existing Task" claim.

## S — Steps

- You MUST verify each citation by file path **and** line number; treat any unverifiable anchor as a finding to drop.
- You MUST evaluate the substrate against its own README.md §11 rules (R.1–R.19) and surface any self-violation.
- You MUST partition findings into G (Good — what works), B (Bad — what's broken), and W (Would do differently — concrete improvements). Each B-row MUST cite at least one spec clause.
- You MUST triage every B-row against the live `tasks/readme.md` index: is there an open Task that already owns this? If yes, cite it; if no, mark `open-new`.
- You SHOULD prioritise B-rows by structural blast radius (linter contracts > entry-point spec drift > scope creep > silent failure modes).
- You MUST produce the deliverable below.

## E — Expectations

The single deliverable is `research/core-architecture-review-2026-05/output/REPORT.md` containing:

- **Provenance line** citing the audited commit.
- **What's Good** (G.1…G.N) — minimum 5 strengths.
- **What's Bad / Limitations** (B.1…B.N) — minimum 8 findings, each with:
  - one-paragraph description,
  - at least one spec-clause citation,
  - file:line anchor for each technical claim.
- **What I Would Do Differently** — table mapping each B-row to a concrete improvement.
- **Citations** — verbatim excerpts of every cited line range.

A *separate* `triage.md` (filed by the dispatching Task, not the executor) MUST map each B-row to its owning Task or new-Task slot.

## Constraints

- **Boundary discipline:** the executor MUST NOT inline the deliverable into the dispatching Task folder. The audit chain Task → Prompt → Research is non-negotiable; the deliverable lives at `research/core-architecture-review-2026-05/output/REPORT.md`.
- **Citation freshness:** anchors are valid for one commit only. The Provenance line MUST pin the audited commit SHA.
- **Scope:** repository-internal critique only; no comparison to external repos beyond what the substrate itself cites.
- **Tone:** direct, structural, falsifiable. Avoid flourish; prefer one-sentence findings with citations.
- **No fixes:** the executor MUST NOT modify any audited file. All actions are produced as Task proposals via the dispatching Task's triage.
