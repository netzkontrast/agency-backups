---
type: note
status: active
slug: adr-spec-research-synthesis-m07
summary: "M07 Contradiction Log: conflicts between the Gemini draft, the existing repo conventions, and emerging brainstorm conclusions, with the resolution adopted in output/SPEC.md."
created: 2026-05-05
updated: 2026-05-05
---

# [M07] Contradiction Log

Each row records a tension and its resolution. C1–C10 are between the Gemini draft and the repo; B1–B3 are between brainstorm conclusions that surfaced internally; G1–G2 are higher-order tensions inherited from the originating Gemini research.

## Gemini ↔ Repo Contradictions

| ID | Claim A (Gemini) | Claim B (Repo) | Characterisation | Resolution in `output/SPEC.md` |
|---|---|---|---|---|
| C1 | ADRs live at `docs/decisions/`. | `FOLDERS.md §1` does not authorise `docs/`. | Topology mismatch. | `decisions/` at the repo root; `FOLDERS.md §8` exemption table extended via Task 028. (`output/SPEC.md §2.1`) |
| C2 | Frontmatter keys: `id`, `title`, `status`, `date`, `tags`. | L1 keys: `slug`, `summary`, `created`, `updated`. | Schema collision. | New L2 namespace `adr_*`; `slug` canonical, `adr_id` secondary; `summary` replaces `title`; `created`/`updated` replace `date`. (§7.4) |
| C3 | `AGENTS.md` is wholesale-overwritten. | `AGENTS.md` mixes hand-authored normative prose + an append-only LOOP_LOG. | Destructive-write risk. | Guarded section between markers; pipeline refuses to write if markers absent. (§2.3, §5.1 ADR.A.3.5) |
| C4 | `agency-adr` is a standalone CLI. | All tools live under `tools/` and compose via `check-governance.sh`. | Co-location mismatch. | `tools/adr/cli.py` reusing `tools/fm/_core.py`. (§7.1, §7.2) |
| C5 | Exit codes 0 / >0. | Repo convention: 0 / 1 binary, with `--strict` promoting WARN to non-zero. | Convention mismatch. | Inherit repo convention; `--strict` promotes WARN. (§7.1 ADR.A.5.5) |
| C6 | Cycles detected during PRE_COMMIT.md "validation phase". | No such phase exists; `check-governance.sh` runs linters in numbered steps. | Process mismatch. | Cycle detection runs inside `agency-adr validate`, invoked as a numbered step in `check-governance.sh`. (§6.1 ADR.A.4.5) |
| C7 | Token-limit 2,000 is the strict ceiling. | Current `AGENTS.md` ≈ 4,800 tokens. | Empirical mismatch. | 2,000 applies to the *guarded section only*; configurable via `--token-limit`; overflow → exit 1. (§5.1 ADR.A.3.3) |
| C8 | Semantic fidelity floor of 0.95 is enforceable. | No fidelity metric exists in the repo. | Implementation gap. | Floor declared normative; algorithm parameterised via `--fidelity-mode`; default `bcp14-keyword`. (§5.1 ADR.A.3.4; `[OPEN]` in §8) |
| C9 | ADR immutability enforced by CI rejecting Decision-Outcome diffs. | Repo has no CI; closest analogue is T4 immutability of completed research workspaces. | Enforcement-mechanism mismatch. | Reuse T4 paradigm: `agency-adr validate` flags any frontmatter or Decision-Outcome diff against HEAD as ERROR `ADR.A.4.1`. (§6.1) |
| C10 | Tooling integrates with `PRE_COMMIT.md` "implicitly". | `.githooks/pre-commit` invokes only `tools/check-governance.sh`. | Hook integration mismatch. | `agency-adr validate` MUST be invoked from `tools/check-governance.sh`. Direct `.githooks` modification prohibited. (§2.4, §7.1) |

## Internal Brainstorm Contradictions

| ID | Claim A | Claim B | Resolution |
|---|---|---|---|
| B1 | "ADRs should be one-per-implicit-decision (Strategy A, 14 ADRs)." | "ADRs should be clustered by surface (Strategy B, ≈ 5 ADRs)." | `[OPEN]` — routed to Task 029. The spec works for both strategies. |
| B2 | "The synthesis pipeline should overwrite the entire `AGENTS.md`." (Gemini-aligned) | "The synthesis pipeline should write only a guarded section." (repo-safety-aligned) | Resolved in favour of guarded section (`output/SPEC.md §2.3`). The Gemini position is explicitly rejected here with rationale: the repo has hand-authored content that is not derivable from ADRs. |
| B3 | "ADRs should live at `decisions/` (flat root)." | "ADRs should live at `docs/decisions/` (industry convention)." | Resolved in favour of `decisions/` (flat root) per `FOLDERS.md §4` "Prefer Flat Structures". The industry-convention argument is acknowledged but does not override the repo's existing flat-folder bias. |

## Higher-Order Tensions Inherited from Gemini

| ID | Claim A | Claim B | Repo-aware resolution |
|---|---|---|---|
| G1 | ADRs are immutable historical records. | Documentation should be living and editable. | The repo *already* resolves this via the dual-state model (immutable research workspaces + editable root specs). Adopt the same pattern: ADRs immutable; the synthesised guarded section in `AGENTS.md` is regenerated per run. |
| G2 | Long-context LLMs make MDL compression obsolete. | Empirical "needle in a haystack" degradation persists. | The repo's existing token-efficiency tooling (`tools/fm/query.py`, `summary` field as primary token-saving lever per `AGENTS.md` "L1 Field Semantics") already endorses Claim B. The ADR spec inherits this stance. |

## Method Audit

Every contradiction above is either (a) resolved in `output/SPEC.md` with a section reference, or (b) explicitly surfaced in §8 as `[OPEN]` for human resolution. No contradiction is silently absorbed.
