---
type: task
status: archived
slug: fm-section-editor
summary: "Build the fm-section editor (replace/append/insert/delete/rename) per SPEC §13. Promote --check-body from opt-in to default-on once the corpus is migrated (Task 019)."
created: 2026-05-05
updated: 2026-05-12
task_id: "018"
task_status: archived
task_owner: "claude-code"
task_priority: P2
task_uses_prompts: []
task_spawns_research: []
task_spawns_prompts: []
task_affects_paths:
  - tools/fm/section.py
  - tools/fm/_core.py
  - tests/fm/test_section.py
  - research/flexible-frontmatter-toolchain/output/SPEC.md
---

# Task 018 — fm-section Editor + Body-Schema Phasing

## Goal

Ship the body-side complement to fm-edit: a single CLI (`tools/fm/section.py`) that mutates one named section per invocation while preserving every byte outside that section's heading-line-through-next-`## ` span. Land the schema-validation phasing flip (Phase 2 → Phase 3, per SPEC §12.6) once the corpus is clean.

## Plan

1. **Implement `tools/fm/section.py`** with the surface in SPEC §13.1: `--replace`, `--append-to`, `--append-list-item`, `--check-task`, `--insert-after`, `--insert-before`, `--delete`, `--rename`. Reuse `_core.find_all_section_bodies` for addressing.
2. **Address resolution** per SPEC §13.3: support `--nth N` and `--anchor <id>`. Refuse ambiguous writes with exit 5.
3. **Invariant guard**: byte-identical preservation outside the addressed section, mirroring fm-edit's pattern. Wrap in `_core.FileLock`.
4. **Schema gate**: every mutation MUST satisfy the §12 body_schema for the file's type. Reject mutations that would violate the schema with exit 4.
5. **Tier guard** per SPEC §13.2: refuse `--rename` when other files reference the heading; instruct caller to file a Task.
6. **Tests**: cover every operation, the byte-preservation invariant (analogue of `test_F_6_5_append_three_times`), the ambiguous-address refusal, and the schema-gate refusal.
7. **Phase 3 flip**: when the corpus is clean (Task 019 territory), default `--check-body` to ON in `tools/check-governance.sh` behind `FM_TOOLCHAIN=1`. Retire the legacy validator in the same commit.
8. **SPEC amendments** flagged in Task 016 §10 Q4/Q5: amend `Levenshtein-distance 1` → `Optimal String Alignment distance 1`; amend §3.2 vs §6.1 skill-key disagreement.

## Todo

- [x] 1. Implement `tools/fm/section.py` per SPEC §13.1.
- [x] 2. Address resolution: `--nth`, `--anchor`, ambiguity → exit 5.
- [x] 3. Body-bytes-outside-section invariant + FileLock.
- [x] 4. Schema gate: refuse mutations that break §12.
- [x] 5. Tier guard: refuse cross-file `--rename`.
- [x] 6. Tests: every op + invariants.
- [x] 7. Flip `--check-body` default-on behind `FM_TOOLCHAIN=1`. *(Deferred to Task 020 per SPEC §12.6 — Phase 3 requires Task 019 to migrate the corpus first; recorded in friction-log.)*
- [x] 8. SPEC amendments for Q4 and Q5.
- [x] 9. Friction-log + run-log entry on close.

## Links

- Source SPEC: [`/research/flexible-frontmatter-toolchain/output/SPEC.md`](../../research/flexible-frontmatter-toolchain/output/SPEC.md) (§12, §13, §14)
- Predecessor: [`/tasks/016-flexible-frontmatter-toolchain/`](../016-flexible-frontmatter-toolchain/)
- Migration peer: [`/tasks/017-migrate-repo-to-flexible-toolchain/`](../017-migrate-repo-to-flexible-toolchain/)
- Body-schema validator already shipped at: [`tools/fm/_core.py`](../../tools/fm/_core.py) (`detect_shape`, `validate_section_body`)
