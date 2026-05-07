---
type: prompt
status: active
slug: tooling-adr-mirror-roundtrip-check
summary: "Ship tools/check-adr-mirror-roundtrip.py — a linter that verifies every SPEC.md mirror row in research/adr-corpus-extraction-from-governance-specs/output/SPEC.md matches its corresponding decisions/<NNNN>-<slug>.md body on adr_id, source citation, and slug. Closes PR #79 review R-5."
created: 2026-05-07
updated: 2026-05-07
prompt_kind: task-spec
prompt_framework: RISEN+ReAct
prompt_target_agent: "Claude Code"
---

# tooling-adr-mirror-roundtrip-check — Task-Spec Prompt

## Framework

RISEN+ReAct. The prompt declares the framework in frontmatter (`prompt_framework: RISEN+ReAct`) and restates it here for `fm-validate` header conformance. The R/I/S/E sections below carry the canonical roles; a final **Constraints** section groups normative scope/failure rules per repo convention.

## R — Role

You are the **main-agent** (or a `python-expert` subagent) dispatched to ship `tools/check-adr-mirror-roundtrip.py`. Your remit is bounded by the Acceptance Criteria in [`brief.md`](./brief.md); you MUST NOT expand scope beyond those criteria without surfacing the divergence in `friction-log.md`. This prompt is unbound to a parent task at authoring time; the successor Task that adopts it MUST add this prompt to its `task_uses_prompts` list and back-reference itself in this prompt's `prompt_relates_to_task` field.

## I — Input

- [`research/adr-corpus-extraction-from-governance-specs/output/SPEC.md`](../../research/adr-corpus-extraction-from-governance-specs/output/SPEC.md) — the IADR mirror.
- [`decisions/`](../../decisions/) — the ratified `<NNNN>-<slug>.md` bodies.
- [`research/adr-spec-research-synthesis/output/SPEC.md`](../../research/adr-spec-research-synthesis/output/SPEC.md) — canonical MADR shape; cites the `path/to/file.ext:Lstart-Lend` citation form expected.
- [`tools/fm/_core.py`](../../tools/fm/_core.py) — frontmatter parser.
- [`maintenance/pr-79-review.md`](../../maintenance/pr-79-review.md) §"Minor Finding" — origin of this prompt.

## S — Steps

1. The agent MUST parse every "ratified" row in the SPEC mirror — heuristic: rows whose recommended `ADR-NNNN` appears as a filename under `decisions/`. Non-ratified rows are skipped (those are intentionally body-less).
2. The agent MUST extract `(adr_id, slug, source_citation)` from each ratified row deterministically. If the row schema is ambiguous, the agent MUST exit 2 with `MIRROR.SCHEMA` rather than guess.
3. The agent MUST open the corresponding `decisions/<NNNN>-<slug>.md`, parse its frontmatter `adr_id`, and verify equality. On mismatch, emit `MIRROR.ID_MISMATCH`.
4. The agent MUST resolve the mirror's `file:line` source citation, read the cited region, and verify that the body's `## Context and Problem Statement` section quotes the region (whitespace-tolerant substring match). On drift, emit `MIRROR.SOURCE_DRIFT`.
5. The agent MUST verify that the row's slug stem equals the filename slug stem. On mismatch, emit `MIRROR.SLUG_MISMATCH`.
6. The agent MUST author `tools/tests/test_adr_mirror_roundtrip.py` covering all four diagnostic codes plus a positive (no-drift) case.
7. The agent MUST integrate the linter as an advisory `[adv]` block in `tools/check-governance.sh` after the `[5/6]` ADR validator; the call MUST be wrapped in `|| true` so it never sets `FAIL=1`.
8. The agent MUST add a one-line cookbook entry to `tools/readme.md`.
9. The agent MUST run `tools/check-governance.sh` and `python3 -m pytest tools/tests/test_adr_mirror_roundtrip.py -v` before committing.
10. The agent MUST commit with a message naming this prompt and the parent task (the parent task is filed at adoption time; reference it as `Task NNN <slug>` in the trailer).
11. The agent MUST author or update the parent task's `friction-log.md` per FRUSTRATED.md FL[0-3] before closing the run.

## E — Expectations

- `tools/check-adr-mirror-roundtrip.py` exists; exits 0 / 2; emits one of `MIRROR.{ID_MISMATCH,SOURCE_DRIFT,SLUG_MISMATCH,SCHEMA}`.
- `tools/tests/test_adr_mirror_roundtrip.py` exists with ≥5 cases (4 negative + 1 positive); `pytest -q` passes.
- `tools/check-governance.sh` invokes the linter advisory-tier; `bash tools/check-governance.sh` does not regress.
- `tools/readme.md` lists the new linter under `## Contents`.
- The friction log declares FL[0-3] per FRUSTRATED.md.

## Constraints

- Dependency: none. Builds atop Task 032 ST-1 artefacts.
- MUST NOT modify the SPEC mirror, the `decisions/` bodies, or the AGENTS.md guarded section as part of this work — the linter is read-only.
- MUST NOT promote the linter to gating tier without a corresponding AGENTS.md / PRE_COMMIT.md amendment (R.7 gating-pipeline trigger).
- SHOULD reuse `tools/fm/_core.py`'s frontmatter parser; SHOULD wrap `import _core` in a `try/except ImportError` per the repo's advisory-linter graceful-degradation convention (see `tools/check-narrative-ontology-load.py`).
- SHOULD cite the parent task's `task_id` in any commit-message trailer for traceability.
