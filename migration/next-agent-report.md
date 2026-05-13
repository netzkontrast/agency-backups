---
type: note
status: active
slug: next-agent-report
summary: "Deep reflection on the design conversation that produced /migration/. Synthesises user intent, revision patterns, robust-vs-fragile decisions, inherited risks, and likely failure modes for the next agent."
created: 2026-05-13
updated: 2026-05-13
---

# Next-agent report — read this before doing anything

This file is a **structured reflection** on the session that produced `/migration/`. Read it in addition to [`handover.md`](./handover.md), not as a substitute. The handover is the operational summary; this report is the meta-commentary that lets the next agent avoid the failure modes the previous agent only saw at the end.

> **The user's directive that produced this file:** *"please also add the original prompt of this Session into the Migration folder - and /sc:reflect deeply on this Session - and Create a detailed Report for the Next Agent."* See turn 13 in [`original-prompt.md`](./original-prompt.md).

---

## 1. What was actually achieved versus what was asked

The user's stated requests evolved across 13 turns (see [`original-prompt.md` §2](./original-prompt.md#2-earliest-user-turns-visible-to-the-agent)). Cross-tabulating ask vs. delivered:

| Turn | Asked | Delivered |
|---|---|---|
| 2 | Revise L11.43 to tasks-only, frontmatter ULID, archive-first preserving NNN. | Lock revised in place; recap document marked superseded. |
| 4 | Decide which open question to tackle next: chose Decision 4 (promoted-type ID convention). | Two question rounds closed: per-type natural fit / `roles/<slug>/` / preserve `L<round>.<sub>`. |
| 7 | Make folders readable + navigable. Suggested `agency`-CLI-generated readme. | L11.44 v1 designed with four-question round (all "Recommended" picks). |
| 9 | Draft ADR + lock files now. Revised L11.44 to v2 (full auto-generation, frontmatter = sole source of truth). | ADR draft started but interrupted by turn 10's pivot. |
| 10 | Write everything into `/migration/` folder; create handover; banner CLAUDE.md + AGENTS.md. | 8-file `/migration/` workspace + banners + supersede pointer. |
| 11 | (Interrupted question round.) Click answers: all-ULID for promoted types / round = conversation round / both parented. | Captured as **provisional** revision history at end of `locks-ratified.md`. |
| 12 | Add a waiver for governance blocks. | `waiver.md` authored. |
| 13 | Governance fully revoked + original prompt + reflect + mandatory banner. | This file + `original-prompt.md` + `waiver.md` v2 + CLAUDE.md banner upgraded to MANDATORY. |

**Pattern:** the user's request crystallised one or two turns *after* the agent produced an artifact. Each artifact revealed what the user actually wanted by what was missing. The agent's safest move at every turn was to produce **something** and let the user redirect — pre-discussion rarely converged faster than post-artifact iteration.

**Implication for the next agent:** when this user requests an artifact, produce a complete version on the first pass even if the design space isn't fully resolved. Don't stall on edge cases; the user will iterate.

---

## 2. The revision pattern — what it signals about the user's mental model

Three locks were revised mid-session, and one decision was reversed:

### L11.43 — three versions in one session

- **v1 (Roundtable 7, prior session):** ULID convention for all 12 types except ADR. Folder shape `<slug>-<ulid>/`. Archive-first big-bang.
- **v2 (turn 2, this session):** Tasks-only. Bare-slug folder. ULID in frontmatter. Archive-first preserving original NNN-slug names. No retroactive ULIDs.
- **v3 (turn 11, provisional):** Extended to 6 types (task + 5 promoted). Same bare-slug-folder + frontmatter-ULID pattern.

### L11.44 — two versions in one session

- **v1 (turn 7):** Hand-written body + auto-managed nav block inside marker comments.
- **v2 (turn 9):** Fully auto-generated; frontmatter is sole source of truth; schemas expand to carry narrative.

### Decision 4 — reversed mid-session

- **First answer (turn 6):** Per-type natural fit. role=slug; lock=L<round>.<sub>; gherkin=anchor-id; friction-log=parent+date; hook=event-name.
- **Reversal (turn 11, provisional):** All 5 promoted types adopt ULID, extending L11.43.

### What this signals

The user is **converging from one extreme toward uniformity** as the design space becomes visible. Pattern:

1. Initial answer favours minimal change ("only tasks", "per-type natural fit", "hand-written body + auto-nav").
2. Once the implications surface (or the agent proposes a halfway artifact), the user expands to the maximal-uniformity version ("all 6 types get ULID", "all readmes fully auto-generated").

This is **not indecision**. It's calibration against the full design space. The first answer is the user's intuitive default; the second answer is the user's considered position after seeing how the first answer interacts with the rest of the design.

**Implication for the next agent:** when this user picks a "minimal" or "Recommended" option, **flag the next-bigger version as a likely follow-up**. Either pre-emptively design for the maximal version, or surface "if you later want X, here's what changes" in the same turn. The user appreciates the heads-up and will sometimes pre-empt the second iteration.

---

## 3. Robust versus fragile decisions

### Robust decisions (highly unlikely to revise)

These have **evidence anchors** — either Gemini D-citations or multi-turn confirmation. The next agent should treat them as binding:

| Lock | Evidence |
|---|---|
| L11.32‴ (12-type ontology) | Gemini D1 + Roundtable-7 question round |
| L11.36′ (three placement modes) | Gemini D2 + multi-turn |
| L11.37′ (SQLite uniform graph) | Gemini D5 + D6 |
| L11.38′ (Pandoc fenced divs) | Gemini D4 |
| L11.40′ (locks content-addressed) | Gemini D3 |
| L11.42 (closed schemas) | Gemini D8 |
| L11.44 v2 (auto-generated readmes principle) | 4-question round confirmed; user upgraded to v2 in next turn |

### Fragile decisions (likely to revise)

These were **single-click answers** that haven't yet crossed the implication threshold. The next agent should re-confirm before lock-in:

| Decision | Why fragile |
|---|---|
| L11.43 v3 (6-type ULID scope) | Just-reversed turn 11; user interrupted before fully integrating. Provisional. |
| Decision 4 reversal (per-type → all-ULID) | Same as L11.43 v3; the implication "L11.43 v2's tasks-only framing is now wrong" was never user-acknowledged. |
| `gherkin` / `friction-log` always-parented (turn 11) | Confirmed by click but no design pressure-tested. SUBFILE-only vs SUBFILE+SUBDOC matrix detail still TBD. |
| Q1 mode matrix (12×3) | Never asked. The recommendation in [`open-questions.md`](./open-questions.md) is the agent's draft, not user input. |
| Q2–Q4, Q5, Q6, Q7 | Same — never engaged. |

### Decisions that exist only in artifacts, not in user confirmation

- **`roles/` as new top-level folder** — agent inferred from "where do roles live" answer (`roles/<slug>/role.md`). The decision to make `roles/` a top-level operational folder is correct but not separately ratified.
- **L1 schema additions (`purpose`, `assumptions`)** — implied by L11.44 v2 (frontmatter = sole source of truth) but the specific field names and types are agent-drafted in [`schemas-delta.md`](./schemas-delta.md).
- **`Assumption` shape** (`{claim, status, date, evidence?}`) — entirely agent-drafted.
- **The ADR's Open Issues numbering (Q1–Q7)** — agent-drafted; user has only engaged with the subset Q1, Q4-detail.

---

## 4. Risks the next agent inherits

### R.1 — The L11.43 v3 revision lives in `§Revision history` at the bottom of `locks-ratified.md`

The main body of `locks-ratified.md` still describes L11.43 v2 (tasks-only). The v3 expansion (6 types) is appended as a "Revision history" section at the end. **A next agent who reads only the body of the lock will work from v2 and miss the v3 expansion.**

**Mitigation:** [`handover.md` §2](./handover.md#2-whats-the-immediate-state-of-play) flags L11.43 as "revised" but does not surface that the in-body text is now stale. Consider rewriting the L11.43 lock body inline once the user confirms v3.

### R.2 — Provisional answers from turn 11 may be rescinded

The user interrupted the question round at turn 11 to request the waiver (turn 12). The three answers given mid-round (`all-ULID for promoted types`, `round = conversation round`, `both always parented`) were **clicked** but the user may not have fully digested the L11.43 cascade implication before redirecting attention to the waiver.

**Mitigation:** these are marked "provisional" in `locks-ratified.md §Revision history`. Re-confirm with the user in the next session — single AskUserQuestion: "Confirm turn-11 answers: 6-type ULID scope, conversation-round counter, gherkin/friction-log always-parented? (Yes/Revise)".

### R.3 — Governance is fully revoked, not just bypassed

`waiver.md` v2 (post turn 13) escalates from "bypass blocks for migration commits" to "all governance is revoked during the refactor". This means `tools/check-governance.sh` will not catch agent errors. **The next agent has no safety net.** A mistake (a malformed frontmatter, a broken link, a missing field) will land in a commit and only be detected if the agent self-audits or a reviewer catches it.

**Mitigation:** the next agent should run `tools/check-governance.sh` even when not gating commits, scan the output for `migration/` references, and self-correct anything attributable to migration-phase changes.

### R.4 — `/migration/` is intentionally outside operational governance

A next agent who has not read this report might "fix" `/migration/` by adding `type: task` frontmatter, moving files into `tasks/<NNN>-<slug>/`, or running `tools/fm/index_diff.py` against it. **Don't.** `/migration/` is a top-level planning workspace, not an operational folder. Its frontmatter uses `type: note` and `type: index` deliberately. Operational rules apply when content **promotes** to `decisions/`, `tools/`, root specs, or the live tree.

### R.5 — Banner drift between `CLAUDE.md` and `AGENTS.md`

Two banners exist with near-identical content. If a future edit updates only one, agents reading different entry points will see different instructions. **Maintain both in lockstep** until the migration retires both.

### R.6 — The ADR draft is now incorrect on L11.43 scope

`adr-draft.md` describes L11.43 as "tasks-only ULID convention" — that was correct at the time of writing, but is now stale after turn 11's provisional reversal. **Promoting the ADR draft as-is would land an incorrect ADR.**

**Mitigation:** rewrite the L11.43 section in `adr-draft.md` before promotion. Also rewrite the corresponding §Decision Outcome bullet. Look for any cross-references to "tasks-only" or "scope: tasks" and reconsider.

### R.7 — `schemas-delta.md` precedes Decision 4 reversal

The schema delta catalogue assumes per-type natural fit (where lock has L-notation and friction-log has parent+date). If 5 promoted types adopt ULID uniformly, the L2 schemas all need a uniform `id:` field; the catalogue's L2 sketches don't reflect that yet.

**Mitigation:** revise [`schemas-delta.md` §3](./schemas-delta.md#3-new-l2-schemas--one-per-promoted-type) after R.2 confirms.

### R.8 — Iteration tempo is fast

This user can revise a lock between two consecutive `AskUserQuestion` rounds. **Do not lock in plans without verifying current state with the user.** The handover represents a moment in time. Always re-read the latest revision history before acting.

---

## 5. Failure modes likely if the next session does not read the handover

### F.1 — Treating `/migration/` as a regular operational folder

Symptom: next agent runs `tools/check-governance.sh` against `/migration/`, finds "errors", attempts to "fix" them.

Cost: wasted session; possible damage to the planning workspace.

Prevention: handover §5 (operational rules); banner mentions `/migration/` is outside governance.

### F.2 — Missing the banner

Symptom: agent reads `CLAUDE.md` body without noticing the banner above § 1; works from pre-migration rules; designs changes that conflict with locks.

Cost: produces work that the user has to reject. Wastes the session.

Prevention: turn 13 directive — banner upgraded to MANDATORY-READ. Plus this report's existence is itself a re-flag.

### F.3 — Reading one lock file without context

Symptom: agent reads only `locks-ratified.md` (without `session-log.md`, `original-prompt.md`, or this file); applies the in-body L11.43 description; misses the v3 revision in `§Revision history`.

Cost: produces an ADR or schema delta based on tasks-only scope, when the user actually meant 6 types. Has to redo the work.

Prevention: handover §3 mandates reading the four files in order. Banner cites handover.

### F.4 — Burning effort fixing pre-existing governance failures

Symptom: agent sees `tools/check-governance.sh` exit non-zero; spends the session fixing research-workspace trust scores, the tasks-index staleness, the FL declaration linter, etc.

Cost: entire session lost on yellow-paint work; migration design progress = 0.

Prevention: `waiver.md` explicitly scopes the pre-existing failures as out-of-scope for migration commits.

### F.5 — Committing to `/migration/` via standard pre-commit hook

Symptom: agent attempts to commit `/migration/` changes; pre-commit hook blocks; agent reaches for `--no-verify` without authorisation.

Cost: violates [CLAUDE.md §11](../CLAUDE.md) "NEVER use --no-verify unless explicitly requested".

Prevention: `waiver.md` is the explicit authorisation. Cite it in the commit message body per the waiver's §4 mechanism.

### F.6 — Promoting `adr-draft.md` without revision

Symptom: agent reads `adr-draft.md`, sees the ADR structure looks ratified, copies it to `decisions/0013-twelve-type-ontology.md` with `adr_status: Proposed`. The text describes tasks-only L11.43, which is now wrong.

Cost: inconsistent ADR lands; reviewers spot the mismatch later; need a corrective ADR or in-place edit (which violates T4-immutability for `Accepted` ADRs — and `Proposed` is still under change-control discipline).

Prevention: this report's §4 R.6 plus `handover.md` §3 (read this report).

### F.7 — Running `/sc:createPR` before reading the waiver

Symptom: agent closes the session via standard CR.1–CR.7 procedure; `/sc:createPR` opens a PR whose title cites "task slug" but there is no Task — only `/migration/`.

Cost: malformed PR; reviewer confusion.

Prevention: this file. Cite `/migration/handover.md` as the closing reference in PR body (no Task slug citation required during migration phase per `waiver.md`).

### F.8 — Carrying forward provisional R1/R2/R3 as binding

Symptom: agent treats turn-11 answers as ratified; promotes L11.43 v3 in the ADR; structures all promoted-type schemas around ULID identity. User then reverses again because they didn't fully digest the cascade.

Cost: wasted artifact + user frustration.

Prevention: re-confirm before lock-in. Recommended one-shot AskUserQuestion at the top of the next session.

---

## 6. Recommended next-session arc

A defensible session-start sequence for whoever picks this up:

1. **Bootstrap:** `./install.sh` + `tools/check-governance.sh` (informational only — note the FAIL state is waivered).
2. **Read in order:** [`handover.md`](./handover.md) → this file → [`locks-ratified.md`](./locks-ratified.md) **including §Revision history** → [`open-questions.md`](./open-questions.md). Then [`session-log.md`](./session-log.md) and [`original-prompt.md`](./original-prompt.md) for context. Then [`adr-draft.md`](./adr-draft.md) and [`schemas-delta.md`](./schemas-delta.md) to see the current synthesis.
3. **Re-confirm turn-11 provisional answers** via a single `AskUserQuestion`:
   - "Decision 4 reversed in turn 11 — all 5 promoted types adopt ULID (extends L11.43 scope to 6 types). Confirm?"
   - "Gherkin and friction-log always-parented (no STANDALONE mode). Confirm?"
   - "Lock-round counter tracks design-conversation rounds (next round = L12.x). Confirm?"
4. **If confirmed:** rewrite the L11.43 lock body inline (drop the v2-vs-v3 split); fix `adr-draft.md` accordingly; update `schemas-delta.md` §3.
5. **If revised:** capture the revision in `locks-ratified.md §Revision history` (append, do not overwrite).
6. **Open the next decision** per `open-questions.md` Q1–Q7. Recommended order: Q1 (mode matrix) → Q4 (slug-collision tooling) → Q2 (`agency promote`) → Q3 (parallel-edit) → Q5 (defer assumption-entry) → Q6 (gherkin/friction-log/hook detail) → Q7 (sequencing).
7. **Close session** with `/migration/`-aware closing procedure: FL log inline in PR body; cite `/migration/handover.md` instead of a Task slug; do **not** invoke `/sc:createPR` without checking the waiver first.

---

## 7. Self-critique — what this agent did wrong

Captured here so the next agent inherits the lessons:

- **Asked too many AskUserQuestion rounds before producing artifacts.** The user repeatedly responded "what's left" rather than "here's the answer to Q5" — that's a hint to deliver value rather than seek more input. The session would have closed faster if the agent had drafted the ADR + locks **earlier**, then iterated on user feedback.
- **Wrote the original `/migration/handover.md` assuming the next agent has the same context as the current one.** The next agent does **not** have the conversation transcript. Files should be self-sufficient. This `next-agent-report.md` retroactively fixes that — but it's a remediation, not a clean design.
- **Did not preserve the user's literal opening prompt.** No mechanism in the session captured turn 1 verbatim. The next session loses 1–2 turns to re-establishing context. Future sessions: write `original-prompt.md` at session start, not at session close.
- **Accepted Decision 4 reversal in turn 11 mid-question-round without flagging the L11.43 scope cascade.** The agent click-captured the answers without surfacing "wait — this means L11.43 v2's tasks-only framing is now wrong". By the time the agent flagged it (in this report), the user had already moved on to the waiver request.
- **Created `waiver.md` as a per-failure carve-out, then had to escalate to "all governance revoked" one turn later.** Should have proposed the larger framing the first time given the user's pattern of expanding from minimal to maximal.
- **Conflated `/sc:reflect` invocation with the act of reflecting.** The Skill tool fetched the framework spec, not a reflection — the actual reflection (this file) was still the agent's work to produce manually.

---

## 8. Cross-references

- Entry point: [`handover.md`](./handover.md)
- Session genesis: [`original-prompt.md`](./original-prompt.md)
- Canonical lock text: [`locks-ratified.md`](./locks-ratified.md) (**read §Revision history** for L11.43 v3)
- Open questions: [`open-questions.md`](./open-questions.md)
- ADR draft (needs L11.43 v3 revision before promotion): [`adr-draft.md`](./adr-draft.md)
- Schema deltas (needs Decision 4 reversal revision): [`schemas-delta.md`](./schemas-delta.md)
- Evidence: [`gemini-evidence.md`](./gemini-evidence.md)
- Session arc: [`session-log.md`](./session-log.md)
- Governance waiver: [`waiver.md`](./waiver.md)

## Assumptions Log

- **Assumption NR1.** The next agent reads files in the order recommended in §6. *Status: not enforced; trust-based.*
- **Assumption NR2.** The user is open to re-confirming turn-11 answers via a single AskUserQuestion at session start. *Status: consistent with user's iteration pattern (§2); not separately validated.*
- **Assumption NR3.** No silent context-summarisation occurred between turn 1 and the earliest visible turn for this agent. *Status: cannot verify; possible the SDK did automatic summary that the agent does not see.*
