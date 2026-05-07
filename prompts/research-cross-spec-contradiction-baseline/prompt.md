---
type: prompt
status: active
slug: research-cross-spec-contradiction-baseline
summary: "Produce research/research-cross-spec-contradiction-baseline/output/REPORT.md cataloging every existing inter-spec normative contradiction across the 8 root governance specs before the 032–039 amendment chain lands, enabling falsification criterion #3 to be mechanically verified."
created: 2026-05-07
updated: 2026-05-07
prompt_kind: research-proposal
prompt_framework: RISEN+ReAct
prompt_target_agent: "Claude Code"
prompt_relates_to_task: ""
---

# Research — Cross-Spec Normative Contradiction Baseline — Prompt

## Framework

RISEN+ReAct. Declared in frontmatter (`prompt_framework: RISEN+ReAct`); restated here for `fm-validate` header conformance.

## R — Role

You are the **main-agent** executing a standalone research run. Your remit is bounded by the Acceptance Criteria in [`brief.md`](./brief.md). You MUST NOT expand scope beyond those criteria without surfacing the divergence in `friction-log.md`.

**Context:** The tasks 032–039 spec-amendment chain has a falsification criterion: "Root specs MUST NOT end up with mutually contradictory normative clauses *introduced by this chain*." Without a pre-chain contradiction catalog, "new" cannot be distinguished from "pre-existing." This research establishes that baseline.

## I — Input

- All 8 root specs: `AGENTS.md`, `TASK.md`, `RESEARCH.md`, `PROMPT.md`, `FOLDERS.md`, `FRUSTRATED.md`, `PRE_COMMIT.md`, `MAINTENANCE.md` (total ~1644 lines).
- `tasks/readme.md` §Chain-Level Falsification (criteria 1–4).
- Known anchor contradiction: `FRUSTRATED.md §28` ↔ `PRE_COMMIT.md §2` (readme-update cadence). Use as CONTR-001 and as a validation anchor.

## S — Steps

1. Read all 8 root specs in full.
2. For each pair of specs, scan for: (a) direct RFC 2119 conflicts on the same topic, (b) scope-overlap where both specs make normative claims about the same path/file/event with incompatible obligations, (c) lifecycle/timing conflicts where both specs mandate an order for the same action.
3. Catalog each contradiction in §2 of the REPORT with ID, type, severity, spec-A clause (with quote), spec-B clause (with quote), and conflict description.
4. Build §3 per-spec risk table and §4 amendment-safety recommendations per task 032–039.
5. Write §5 summary statistics consistent with §2 catalog.
6. Populate `/research/research-cross-spec-contradiction-baseline/workspace/session.log` chronologically.
7. Populate `/research/research-cross-spec-contradiction-baseline/synthesis/` (methodology, post-synthesis-log, state, tracks).
8. Write `/research/research-cross-spec-contradiction-baseline/reflection/friction-log.md`.
9. Deliver REPORT.md to `/research/research-cross-spec-contradiction-baseline/output/REPORT.md`.
10. Run `tools/check-governance.sh`. Fix every ERROR. Commit with message: `research(cross-spec-contradiction-baseline): pre-chain normative conflict catalog (brainstorm → new proposal)`. Do NOT push.

## E — Expectations

- `REPORT.md` at `/research/research-cross-spec-contradiction-baseline/output/REPORT.md`.
- §2 contains ≥1 entry (CONTR-001 = FRUSTRATED §28 ↔ PRE_COMMIT §2).
- Every §2 entry cites exact section + quoted clause from both specs.
- §3 covers all 8 specs.
- §4 names ≥1 amendment-safety note per task 032–039.
- §5 statistics are internally consistent with §2 count.
- `research_phase: complete` in workspace readme.
- `tools/check-governance.sh` exits 0.

## Constraints

- MUST NOT fabricate spec text — every quote MUST be verbatim from the file.
- MUST flag CONTR-001 as the known anchor (FRUSTRATED §28 ↔ PRE_COMMIT §2).
- MUST run `tools/check-governance.sh` before committing.
- MUST NOT push — the maintainer pushes after review.
- SHOULD record FL0 in friction-log.md even if no friction arises.
