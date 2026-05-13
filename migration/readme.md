---
type: index
status: active
slug: migration
summary: "In-flight design workspace for the 12-type ontology + tasks-only ULID + auto-generated readmes refactor. Plan-of-record; not yet ratified."
created: 2026-05-13
updated: 2026-05-13
---

# Migration workspace

**Read [`handover.md`](./handover.md) first if you are picking this up in a new session.**

## What is this folder?

`/migration/` is the in-flight design workspace for a repo-wide refactor of Agency's artifact ontology, placement model, identifier convention, and readme-generation strategy. It is **not** a regular operational folder — the artifacts here are plan-of-record documents staged for promotion into `decisions/`, root specs, and tooling once the open questions in [`open-questions.md`](./open-questions.md) are resolved.

Nothing in this folder is binding yet. Current conventions (numbered task folders, hand-written readmes, no `lock` first-class type) still apply to the rest of the repo. The locks captured in [`locks-ratified.md`](./locks-ratified.md) are **user-confirmed** but not yet operationalised.

## Why does it exist?

Roundtables 7 and 8 of the ontology design conversation produced 11 ratified locks (L11.32‴ through L11.44 plus Decision 4) over multiple sessions. The locks are too numerous and interdependent to land via a single ADR + cascade in one session. Capturing them in `/migration/` lets the work cross session boundaries without losing context, with a single handover document as the entry point.

When the migration is executed, this folder is deleted — locks promote to `decisions/locks/`, the ADR draft promotes to `decisions/0013-…md`, schema deltas land in `maintenance/schemas/`, and root specs get cascaded.

## Files in this folder

| File | Purpose |
|---|---|
| [`readme.md`](./readme.md) | This file. Index + governance status. |
| [`handover.md`](./handover.md) | **Next-session entry point — MANDATORY first read.** What's done, what's open, where to resume. |
| [`next-agent-report.md`](./next-agent-report.md) | **MANDATORY second read.** Deep reflection on revision patterns, robust-vs-fragile decisions, inherited risks, and failure modes for the next agent. |
| [`locks-ratified.md`](./locks-ratified.md) | All 11 user-confirmed locks (L11.32‴..L11.44 + Decision 4). **Read §Revision history** at the bottom — L11.43 v3 lives there, not in the main body. |
| [`open-questions.md`](./open-questions.md) | Q1–Q7 still pending; each blocks ADR ratification. |
| [`waiver.md`](./waiver.md) | Authorisation to bypass `tools/check-governance.sh`. **All governance revoked** for the refactor window. |
| [`adr-draft.md`](./adr-draft.md) | Draft of ADR-0013 (Twelve-Type Ontology + Three-Mode Placement + ULID Convention). Status `Proposed`. **Stale on L11.43 scope — needs revision before promotion.** |
| [`schemas-delta.md`](./schemas-delta.md) | Proposed schema additions (type enum +5, L1 `purpose`/`assumptions` fields, `l2-lock.schema.json`, …). **Predates Decision 4 reversal — needs revision.** |
| [`gemini-evidence.md`](./gemini-evidence.md) | The 8 Gemini D-citations (D1–D8) anchoring the ontology decisions. |
| [`session-log.md`](./session-log.md) | Chronological log of the design conversation that produced this workspace. |
| [`original-prompt.md`](./original-prompt.md) | Best-effort reconstruction of session genesis. Verbatim user turns where preserved. |

## Banner location

The corresponding **MIGRATION IN PROGRESS** banner has been added at the top of [`../CLAUDE.md`](../CLAUDE.md) and [`../AGENTS.md`](../AGENTS.md), pointing every agent that bootstraps a session here.

## Predecessor document

This folder supersedes [`../.claude/plans/roundtable-7-ontology-locks-recap.md`](../.claude/plans/roundtable-7-ontology-locks-recap.md), which captured the state after Roundtable 7. That document is now **historical** — it represents the L11.43 *original* form (12 types except ADR, `<slug>-<ulid>/` shape) which was revised in Roundtable 8 to tasks-only with bare-slug folders and frontmatter ULID. See [`session-log.md §2`](./session-log.md) for the revision trail.

## Assumptions Log

(none)
