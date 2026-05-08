---
type: prompt
status: active
slug: toolchain-flip-criteria-research-prompt
summary: "Phase 1-3 render of the executing prompt /prompts/research-toolchain-flip-criteria/prompt.md per the run preamble (research-prompt-optimizer; askuser skipped because intent is canonical)."
created: 2026-05-08
updated: 2026-05-08
prompt_kind: research-rendered
prompt_target_agent: "Claude Code"
prompt_relates_to_task: maintenance-spec-integration
---

# Research-Prompt Render — toolchain-flip-criteria

This file is the Phase 1–3 render produced by the executing-prompt preamble (Step S.1 of [`./prompt.md`](./prompt.md)): "Run research-prompt-optimizer Phase 1–3. Skip Phase 1 askuser; intent canonical."

## Phase 1 — Intent (askuser skipped)

The executing prompt is canonical; the run does not need clarification from a human. Intent restated for the audit graph:

> Produce a deterministic, mechanically-verifiable flip-criteria SPEC for the Legacy column of the three-way Legacy / Flexible / ADR toolchain matrix governing `tools/check-governance.sh`. Output landing path is `research/toolchain-flip-criteria/output/SPEC.md`. Falsification surface: any criterion that requires LLM judgment.

## Phase 2 — Decomposition

The deliverable decomposes into four strictly-ordered subtasks, each owning one §-aspect of the SPEC:

1. **§1 ≤7-item checklist.** Enumerate the gating-vs-advisory boundary in `tools/check-governance.sh`; collapse closely-related criteria; cap at seven items.
2. **§2 single-commit flip procedure.** Author the file-change enumeration as a strict tree-diff; specify the commit-message shape; pin pre-commit and post-commit verification.
3. **§3 post-flip cleanup checklist.** Separate "linters to retire" (deleted in §2) from "WARN→ERROR promotions" (sequenced after §2 as separate Tasks). Include doc re-numbering and ADR-column hygiene.
4. **§4 rollback procedure.** Mentally execute `git revert <flip-sha>` against §2; confirm the inverse tree-diff restores pre-flip state; specify trigger conditions and re-flip preconditions.

## Phase 3 — Render

The render (this file's existence) satisfies the preamble's "Render to /research/toolchain-flip-criteria/research-prompt.md" instruction. The actual SPEC text was authored directly into [`./output/SPEC.md`](./output/SPEC.md); this render exists for audit-graph traceability of the preamble execution.

## Cross-references

- Executing prompt (verbatim snapshot): [`./prompt.md`](./prompt.md).
- Source prompt (mutable): [`../../prompts/research-toolchain-flip-criteria/prompt.md`](../../prompts/research-toolchain-flip-criteria/prompt.md).
- Brief: [`../../prompts/research-toolchain-flip-criteria/brief.md`](../../prompts/research-toolchain-flip-criteria/brief.md).
- Parent task: [`../../tasks/039-maintenance-spec-integration/task.md`](../../tasks/039-maintenance-spec-integration/task.md).
