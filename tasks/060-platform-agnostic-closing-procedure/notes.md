---
type: note
status: active
slug: 060-platform-agnostic-closing-procedure-notes
summary: "Implementation notes for Task 060 — extraction of the implicit /sc:createPR checklist, audit of Jules + Gemini PR primitives, and the four-step platform-agnostic procedure landed in AGENTS.md."
created: 2026-05-11
updated: 2026-05-11
---

# Task 060 — Implementation Notes

## 1. Implicit `/sc:createPR` checklist extracted

`/sc:createPR` is provided by the SuperClaude Framework (`src/superclaude/commands/createPR.md`). Reading the prior CR.1–CR.6 normative rules in AGENTS.md and the wrapper behaviour described in CLAUDE.md §10, the skill performs the following composable steps:

1. Verify the working tree is clean and the friction log exists with a parseable FL declaration.
2. Verify `tasks/readme.md` reflects current `task_status` frontmatter (PRE_COMMIT.md §7.11 gate).
3. Re-run `tools/check-governance.sh` and abort if it exits non-zero (defence-in-depth on CR.3).
4. Open a pull request via the GitHub primitive available in the session (cloud MCP `mcp__github__create_pull_request` or local `gh` if present); the body cites Task slug(s) + FL.

These four primitives are the platform-agnostic checklist. None of them is Claude-specific. The previous CR.1–CR.6 rules conflated "what every agent must do" with "how Claude implements step 4", which made the procedure illegible to Jules and Gemini.

## 2. Jules + Gemini PR-primitive audit

- **Jules**: ships native GitHub integration; the agent can open a draft PR with a body string directly. No `/sc:` equivalent; the implementation note is "use the Jules-native primitive with the body shape this section mandates." Steps 1–3 are achievable in Jules's runtime without modification.
- **Gemini Deep Research**: executes against an external research surface, not a Git working tree. There is no on-platform `git push` or PR-creation primitive. The recovery pattern in this repo is RESEARCH.md §6.5: the Gemini artefact lands in `research/gemini/<slug>/` via a follow-on integration Task whose own agent (typically Claude) satisfies step 4 against the integration commit. Documented in the new "Gemini" subsection of AGENTS.md "Platform Implementation Notes".

No genuinely Claude-only step survives once steps 1–3 are factored out from `/sc:createPR`. The PR-creation primitive itself is platform-specific, which is exactly what step 4 + the per-platform notes formalise.

## 3. Changes landed in this Task

- **`AGENTS.md`**:
  - Top-of-file pointer at line 18 rewritten from "Last step of every Claude Code run" to "Last step of every session (all agents)".
  - `## Closing Run Procedure (Claude Code)` renamed to `## Closing Run Procedure` (anchor: `closing-run-procedure`).
  - Added four-step platform-agnostic checklist with bullets keyed to FRUSTRATED.md §FL.Log, PRE_COMMIT.md §7.11, and `tools/check-governance.sh`.
  - CR.1–CR.6 generalised and a new CR.7 added requiring new platforms to be introduced via implementation notes rather than new normative rules.
  - New `### Platform Implementation Notes` subsection with Claude Code / Jules / Gemini / "Adding a new platform" entries.
  - Gherkin scenarios expanded from 2 → 5 to cover Claude Code, Jules, Gemini delegation, and idempotency (anchors CR.1.1–CR.1.5).
- **`CLAUDE.md` §10**: section renamed from "Closing run procedure (Claude Code only)" → "Closing run procedure (all platforms)"; checklist mirrored; quick-rules bullet at line 244 updated.
- **`README.md` §8**: section renamed from "(Claude Code only)" → "(all platforms)"; per-platform implementation paragraph added.
- No changes needed in `MAINTENANCE.md` / `FRUSTRATED.md` / `PRE_COMMIT.md`: a grep against the four-spec set showed no exclusive `/sc:createPR` references in those files.

## 4. Anchors preserved / changed

- `#closing-run-procedure-claude-code` → `#closing-run-procedure` (one-letter heading rename invalidated the prior anchor).
- Two external citation paths to the old anchor were updated:
  - `CLAUDE.md:176`
  - `README.md:193`
- A `git grep "closing-run-procedure-claude-code"` post-edit returns zero hits.

## 5. Falsifiability check

The Goal's falsifiable outcome was: "`AGENTS.md` defines a platform-agnostic closing-run procedure as a numbered checklist […] and `/sc:createPR` is reframed as one implementation that satisfies the checklist — with at least one parallel implementation note for Jules and Gemini." Both clauses are now satisfied:

1. The numbered checklist is at `AGENTS.md` "Platform-Agnostic Checklist" (4 steps).
2. `/sc:createPR` appears once in the section, inside the "Claude Code" implementation-note subsection, demoted from the headline rule.
3. Jules + Gemini each have their own implementation-note subsection; a "Adding a new platform" subsection documents the extension point.

The Task is closeable on this evidence.
