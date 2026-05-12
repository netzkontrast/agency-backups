---
type: note
status: active
slug: adr-spec-research-synthesis-analysis
summary: "/sc:analyze output: implicit ADRs already in force, structural conventions any new ADR spec must honour, conflicts with the Gemini draft, and reusable tooling primitives."
created: 2026-05-05
updated: 2026-05-05
---

# Step 1 — `/sc:analyze` Root Specs and Tooling

Scope analysed (per the prompt's Input list):

1. Root specs: `AGENTS.md`, `TASK.md`, `PROMPT.md`, `RESEARCH.md`, `FOLDERS.md`, `PRE_COMMIT.md`, `MAINTENANCE.md`, `FRUSTRATED.md`, `README.md`.
2. Tooling: `tools/check-governance.sh`, `tools/fm/{validate,extract,edit,query}.py`, `tools/lint-{structure,linkage,runlog}.py`, `tools/validate-frontmatter.py`, `tools/check-trust.py`.
3. Schemas: `maintenance/schemas/header-ontology.json`.
4. Gemini draft (reference): `research/gemini/agency-adr-governance-spec/adr-governance-spec.md`.

Method: every finding below is confirmed in ≥ 2 source files per [M06] Source Triangulation. The triangulation evidence is recorded in [`../reflection/M06-source-triangulation.md`](../reflection/M06-source-triangulation.md).

## A. Architectural Decisions Already In Force (Implicit ADRs)

These are decisions the repo has already made. The ADR governance spec MUST honour them, formally surface them as the migration corpus, or explicitly supersede them.

| # | Implicit Decision | Source Evidence (≥ 2 files) |
|---|---|---|
| I1 | **Frontmatter is layered (L0/L1/L2/L3) with strict YAML depth ≤ 1.** | `TASK.md §3`, `AGENTS.md "Frontmatter Ontology"`, `maintenance/schemas/header-ontology.json` |
| I2 | **The audit graph flows Task → Prompt → Research only via frontmatter keys.** | `FOLDERS.md §6`, `TASK.md §3.3`, `RESEARCH.md §3` |
| I3 | **`docs/` is not a top-level folder; `/research/<slug>/` is the canonical home for synthesis artefacts.** | `FOLDERS.md §1`, `FOLDERS.md §8` (no `docs/` exemption), absence on disk |
| I4 | **Operational folders are exactly `/tasks/`, `/prompts/`, `/research/`. Adding a new top-level operational folder is itself an anti-pattern.** | `FOLDERS.md §7`, `FOLDERS.md §8` |
| I5 | **Specs use RFC 2119 (one keyword per sentence) + Gherkin (one `# anchor:` per scenario).** | `AGENTS.md "Spec Language Reference"`, `maintenance/language-spec.md` (referenced), every existing root spec |
| I6 | **Branching convention is `claude/<topic>-<date>`; PR closure goes through `/sc:createPR`.** | `AGENTS.md §"Closing Run Procedure"`, current branch `claude/adr-spec-research-NPwuc` |
| I7 | **Repair is tiered (T1/T2/T3/T4); root specs accept only T1/T2 in-place; T3 MUST be a Task.** | `MAINTENANCE.md §1`, `MAINTENANCE.md §3.5` |
| I8 | **Research workspaces are immutable once `research_phase: complete` (T4 prohibition).** | `MAINTENANCE.md §1`, `RESEARCH.md §7`, `PROMPT.md §7` |
| I9 | **The pre-commit hook is gated by `tools/check-governance.sh`, which composes four legacy linters plus an opt-in `FM_TOOLCHAIN=1` flexible validator.** | `PRE_COMMIT.md §7`, `tools/check-governance.sh`, `MAINTENANCE.md §1.1` |
| I10 | **`AGENTS.md` is partly hand-authored and partly accreted (LOOP_LOG section appended by Jules).** | `AGENTS.md` §"LOOP_LOG" (manual append-only), `AGENTS.md` §"Closing Run Procedure" (manual normative prose) |
| I11 | **Per-type required headings are encoded once in `header-ontology.json` v1.1.0; the prose tables in TASK.md §3 are a mirror.** | `TASK.md §3`, `maintenance/schemas/header-ontology.json` `$schema-note` |
| I12 | **Friction is mandatory at every closure (FL0–FL3) — no friction-log = no commit.** | `FRUSTRATED.md`, `RESEARCH.md §5.9`, `TASK.md §7.7` |
| I13 | **Task supersession uses `task_supersedes` / `task_superseded_by` reciprocally and traverses through `updated` to a terminal `done`.** | `TASK.md §4.7`, `TASK.md §8.7` (acceptance scenarios) |
| I14 | **External research is ingested under `/research/<provider>/<slug>/` and MUST spawn a downstream Task in the same commit.** | `RESEARCH.md §6`, `tasks/003-analyze-skillmd-novel-authoring/` precedent |

## B. Structural Conventions Any New ADR Spec MUST Honour

These are the non-negotiables. The ADR governance spec MUST encode every one of them; the Gemini draft violates several (flagged in §C).

| # | Convention | Why It Binds the ADR Spec |
|---|---|---|
| B1 | **L1 frontmatter (`type`, `status`, `slug`, `summary`, `created`, `updated`)** is mandatory on every operational file. | An ADR is an operational file. Its frontmatter MUST extend, not replace, L1. |
| B2 | **YAML depth ≤ 1**, lists of scalars only. | The Gemini-proposed `supersedes: array of strings` is compatible; any nested-object embedding is not. |
| B3 | **Slugs are kebab-case, max 5 tokens; equal to the folder name.** | An ADR file's slug MUST follow this; the Gemini-proposed `id: ADR-NNNN` becomes a *secondary* identifier, not the slug. |
| B4 | **One RFC 2119 keyword per sentence.** | The Gemini draft already complies. The repo-native spec MUST keep this. |
| B5 | **Every Gherkin Scenario MUST carry an `# anchor:` comment with a stable id.** | The Gemini draft uses Gherkin but inconsistently anchors. The repo-native spec MUST anchor every scenario. |
| B6 | **Mechanical enforcement is composed; legacy + flexible run in parallel during the migration window.** | Any ADR linter MUST plug into `tools/check-governance.sh` and respect the legacy/flexible toggle. |
| B7 | **Sequence numbers are monotonically increasing across the lifetime of the repo.** | Mirrors `<NNN>-<slug>` for tasks. ADR ids `ADR-NNNN` MUST follow the same monotonic rule. |
| B8 | **`/maintenance/schemas/header-ontology.json` is the binding source for tooling; prose tables are mirrors.** | The ADR JSON-Schema MUST live there (or be referenced from it), not be invented in a parallel file. |
| B9 | **Branch model `claude/<topic>-<date>`; closure via `/sc:createPR`.** | Already explicitly cited by the Gemini draft (§2.5). Inherited verbatim. |
| B10 | **The maintenance-bypass list lives in `tools/.frontmatter-waivers` and is burn-down only.** | The ADR validator MUST NOT reuse this list silently; any new waiver mechanism MUST be additive, with its own per-line rationale and tracking Task. |
| B11 | **Trust audit (`tools/check-trust.py`) gates closure-with-friction-log.** | The ADR closure protocol MUST surface FL declarations through this audit, not invent a parallel trust path. |

## C. Where the Gemini Draft Conflicts With the Repo

Each row records (a) Gemini's claim, (b) the repo evidence that contradicts it, (c) the resolution recorded in `output/SPEC.md`.

| # | Gemini Claim | Repo Evidence | Resolution in §2 of `output/SPEC.md` |
|---|---|---|---|
| C1 | "All ADRs MUST be stored within the directory specified by `FOLDERS.md` (conventionally `docs/decisions/`)." (Gemini §2) | `FOLDERS.md` does NOT name `docs/decisions/`. `FOLDERS.md §1` and §8 enumerate `/tasks/`, `/prompts/`, `/research/` plus four storage exemptions; `docs/` is not on either list. | Canonical path is `decisions/` at the repo root (no `docs/` parent). The non-operational storage exemption table in `FOLDERS.md §8` is extended to add `decisions/` as a fifth exempt folder. |
| C2 | "ADR YAML frontmatter MUST contain `id`, `title`, `status`, `date`, `tags` for programmatic extraction." (Gemini §4.1, A.2.2) | The repo's L1 contract uses `slug` (not `id`), `summary` (not `title`), `created` + `updated` (not `date`), and uses Obsidian L0 `tags` only. | The ADR L2 namespace `adr_*` extends L1: `slug` is canonical (kebab-case), `adr_id: ADR-NNNN` is the secondary stable identifier, `adr_status` enumerates the four lifecycle states, `adr_supersedes` is a list, `adr_tags` (≠ Obsidian L0 `tags`) is OPTIONAL. `created`/`updated` come from L1. |
| C3 | "The synthesis tooling MUST overwrite `AGENTS.md` automatically and idempotently." (Gemini A.3.5) | `AGENTS.md` contains hand-authored normative prose, a Closing Run Procedure block, and an append-only `LOOP_LOG`. Wholesale overwrite would destroy this. | The synthesis pipeline writes a guarded section between markers `<!-- BEGIN AGENCY-ADR SYNTHESIS -->` and `<!-- END AGENCY-ADR SYNTHESIS -->`. Outside the markers, content is preserved verbatim. The pipeline MUST refuse to write if the markers are absent (stops the destructive overwrite by construction). |
| C4 | "MDL synthesis tooling exists as a deterministic, idempotent CLI named `agency-adr`." (Gemini §7) | No such CLI exists; the repo's tooling lives under `tools/` (Python), is composed by `tools/check-governance.sh`, and exposes `tools/fm/{validate,extract,edit,query}.py`. | `agency-adr` is implemented as `tools/adr/cli.py` with sub-commands `validate` and `synthesize`. It MUST reuse `tools/fm/_core.py` for frontmatter parsing rather than reimplementing it. The CLI is registered as a step in `tools/check-governance.sh` once Task 028 ships. |
| C5 | "POSIX exit codes 0 / >0." (Gemini A.5.5) | Repo convention: 0 / 1 (binary), with diagnostics printed to stdout in the legacy linter style and `--format=json` for machine consumption (per `tools/fm/validate.py` argparse). | Inherit the repo convention: exit 0 on success, exit 1 on any ERROR diagnostic, `--strict` promotes WARN to non-zero. JSON output is OPTIONAL via `--format=json`. |
| C6 | "Cycles are detected during `PRE_COMMIT.md` validation phase." (Gemini A.4.5) | `PRE_COMMIT.md §7` and `tools/check-governance.sh` execute three linters before the trust audit. There is no separate "DAG validation phase". | Cycle detection runs inside `agency-adr validate`, which `check-governance.sh` invokes as `[6/6] ADR governance validator` after the trust audit. A cycle yields exit 1 with code `ADR.A.4.5`. |
| C7 | "Token-limit threshold is 2,000 tokens." (Gemini A.3.3) | The repo has no measurement of `AGENTS.md`'s current token count, no token-counter in `tools/`, and the existing `AGENTS.md` is empirically larger than 2,000 tokens (≈ 4,800 tokens by `wc -w` × 1.33 heuristic). | Token-limit applies only to the *synthesised* guarded section, not the whole `AGENTS.md`. The default limit is `--token-limit 2000` (matches Gemini) but it is configurable; when the corpus would overflow, the pipeline MUST exit 1 with `ADR.A.3.3` and propose a deprecation candidate. |
| C8 | "Semantic fidelity floor of 0.95 is enforceable." (Gemini A.3.4) | No fidelity metric is defined in the repo; no implementation exists. The Gemini draft itself flags this in §8 as an open question. | The fidelity floor is *declared* normative (MUST ≥ 0.95) but the *measurement algorithm* is parameterised: `--fidelity-mode {bcp14-keyword|adr-id-anchor|llm-pass}`. Initial implementation ships with `bcp14-keyword` (deterministic, no LLM dependency). The choice itself is an `[OPEN]` item routed to Task 029. |
| C9 | "ADR immutability is enforced by CI rejecting modifications to the Decision Outcome of an Accepted ADR." (Gemini A.4.1) | The repo has no CI for ADRs and no runtime enforcement of immutability. Closest analogue: research workspaces are T4-immutable per `MAINTENANCE.md §1`. | Reuse the T4 paradigm: an Accepted ADR is T4-immutable. `agency-adr validate` flags any frontmatter or Decision-Outcome diff against the repo HEAD as ERROR `ADR.A.4.1`. |
| C10 | "Tooling integrates with `PRE_COMMIT.md` hooks via implicit invocation." (Gemini §2) | `.githooks/pre-commit` invokes `tools/check-governance.sh` only. Anything else is invisible to the gate. | `agency-adr validate` MUST be invoked from `tools/check-governance.sh` to participate in the gate. Direct `.githooks` modification is prohibited. |

## D. Reusable Tooling Primitives

The synthesis pipeline MUST reuse, not reimplement.

| Primitive | Source | Reuse Path |
|---|---|---|
| Frontmatter parsing + L1/L2 validation | `tools/fm/_core.py` (679 lines) | Import in `tools/adr/schema.py` for ADR YAML validation. |
| Per-type body schema (required headings, shape, item-counts) | `maintenance/schemas/header-ontology.json` | Add an `"adr"` entry under `types` with `required_headings: ["Context and Problem Statement", "Decision Outcome", "Consequences"]`. |
| File traversal with frontmatter filter | `tools/fm/query.py` | `agency-adr synthesize` MUST query `type:adr,adr_status:Accepted` via this tool rather than re-walking the tree. |
| YAML mutation with file-lock and depth-1 enforcement | `tools/fm/edit.py` | Used by `agency-adr` to flip `adr_status: Accepted → Superseded` on supersession. |
| Diagnostic format (`Diag(rel, line, severity, code, message)`) | `tools/fm/_core.py` | All ADR diagnostics MUST follow this shape so they compose with the existing tooling output. |
| Run-log append protocol | `tools/lint-runlog.py`, `maintenance/run-log.md` | When a synthesis run rewrites the guarded section in `AGENTS.md`, it MUST append a record. |
| Trust audit bridge | `tools/check-trust.py` | Closure of an ADR PR is a Task closure under `TASK.md §7.7`; the friction-log requirement carries through. |
| Pre-commit shim composition | `tools/check-governance.sh` | New `[N/N] ADR governance validator` step is added after Step 4 (run-log) and before the trust audit. |

## E. Hook Integration Diagram

```text
                       ┌──────────────────────────────┐
git commit  ──────────►│ .githooks/pre-commit (gate)  │
                       └──────────────┬───────────────┘
                                      ▼
                       ┌──────────────────────────────┐
                       │ tools/check-governance.sh    │
                       └──┬───────┬───────┬───────┬───┘
                          ▼       ▼       ▼       ▼
                    [1] frontmatter     [2] structure
                    [3] linkage         [4] run-log
                    [5] narrative-ontology (gated on ontology.json)
                    [6] ADR validator   ◄── NEW (Task 028 ships this)
                    [7] trust audit (Spec-J/K/L)
```

The ADR validator MUST exit 0 if no `decisions/` folder exists yet (graceful degradation; the repo is permitted to live without ADRs).

## F. Findings Routed to Step 2

The five integration questions in the prompt map to the conflicts in §C as follows:

| Question | Primary conflicts |
|---|---|
| Storage path | C1 |
| CLI integration | C4, C10 |
| Frontmatter composition | C2, B1, B2, B3 |
| AGENTS.md ownership | C3, I10 |
| Migration path | I1–I14 (the implicit ADRs become ADR-0001..N candidates) |

These are answered in [`brainstorm.md`](./brainstorm.md).
