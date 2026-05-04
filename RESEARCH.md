---
type: spec
status: active
slug: research-spec
summary: "Root specification for /research/. Research is execution-only: it consumes a prompt and produces a workspace of evidence, synthesis, reflection, and a final output. Prompt-craft and follow-up question generation are out of scope and live in /prompts/."
created: 2026-05-02
updated: 2026-05-04
---

# Research Task Specification

> **Mechanical Enforcement Notice:** This spec is mechanically enforced by `tools/check-governance.sh`. Before editing any file under `/research/`, install the pre-commit hook once with `tools/install-hooks.sh`. See [§5 Mandatory Pre-Commit Checks](#5-mandatory-pre-commit-checks-for-research-tasks) for the per-clause linter mapping.

A **Research Task** *executes* a prompt. It does not author one. The prompt that triggered this run lives in `/prompts/<slug>/prompt.md`; the workspace produced by running it lives in `/research/<slug>/`. Open questions or follow-up prompts surfaced during a run are NOT appended to the research workspace — they are filed as new prompts in `/prompts/` per `PROMPT.md` §1.

## 1. Scope (What `/research/` Is and Is Not)

`/research/` IS:

- The workspace where a prompt is executed.
- The home of synthesis, reflection, friction logs, and final deliverables.
- A read-mostly archive once a run is `complete` or `archived`.

`/research/` IS NOT:

- A place to draft prompts (those live in `/prompts/`).
- A place to coordinate work across runs (that lives in `/tasks/`).
- A place to amend with follow-up questions after closure (file a new prompt instead).

## 2. Directory Structure

For every new research run, create a dedicated subfolder under `/research/`. The folder name is the `slug` of the *prompt* that triggered the run (matching the `/prompts/<slug>/` it executes). Folders MUST adhere to `FOLDERS.md`.

```text
/research
└── /<slug>
    ├── readme.md             # Directory index with relative links and assumption logs.
    ├── prompt.md             # Snapshot of the executing prompt at run-start (immutable).
    ├── /workspace            # Temporary work artifacts, scratch notes, session logs.
    │   ├── readme.md
    │   ├── session.log       # Chronological terminal/tool trace.
    │   └── ...               # Scratchpad notes; execution scripts MUST be deleted before commit.
    ├── /synthesis            # Structured, flattened synthesis artifacts.
    │   ├── readme.md
    │   ├── post-synthesis-log.md  # Chronological merge log.
    │   ├── methodology.md    # Methods applied (e.g., M06, M13).
    │   ├── tracks.md         # Per-track work breakdown.
    │   └── state.md          # Checklist of synthesis steps.
    ├── /reflection           # Critical-thinking reflection artifacts.
    │   ├── readme.md
    │   ├── friction-log.md   # Mandatory FL0–FL3 log per FRUSTRATED.md.
    │   └── M<XX>-*.md        # One file per critical-thinking method.
    └── /output               # Final deliverables.
        ├── readme.md
        └── SPEC.md           # Or REPORT.md, depending on the prompt.
```

## 3. Mandatory Frontmatter

`/research/<slug>/output/SPEC.md` and `/research/<slug>/readme.md` MUST carry L1 Vault Core keys plus the L2 `research_*` namespace defined in `TASK.md` §3:

```yaml
---
type: research
status: active | completed | archived
slug: <research-slug>            # MUST equal the executing prompt slug.
summary: "Token-cheap tl;dr."
created: YYYY-MM-DD
updated: YYYY-MM-DD
research_phase: kickoff | synthesis | reflection | complete
research_executes_prompt: <prompt-slug>   # MUST resolve to /prompts/<slug>/.
research_friction_level: FL0 | FL1 | FL2 | FL3
---
```

YAML MUST NOT nest beyond one level.

## 4. Workflow Requirements

1. **Resolve the Prompt** — Confirm `/prompts/<slug>/prompt.md` exists. If it does not, the agent MUST stop and create one per `PROMPT.md`. Research MUST NOT fabricate its own instruction set.
2. **Initialize Directory** — Create the `<slug>` folder and the four subfolders (`workspace/`, `synthesis/`, `reflection/`, `output/`).
3. **Snapshot the Prompt** — Copy the prompt body into `/research/<slug>/prompt.md` (this is the immutable run-start snapshot, not a re-author).
4. **Work in Workspace** — Save planning scripts, search logs, downloaded pages, and tracking files into `/workspace`. Do not pollute the root directory. Execution scripts (`.py`, `.sh`) MUST be deleted before final commit.
5. **Log the Session** — Append to `/workspace/session.log` chronologically. This is the terminal-level audit trail.
6. **Synthesize Structurally** — Populate `/synthesis/` flat (per `FOLDERS.md`) unless 4+ files of the same type accumulate.
7. **Reflect** — Apply the critical-thinking methods named in the executing prompt; one flat file per method in `/reflection/`. Log friction in `friction-log.md`.
8. **Deliver** — Move the final completed artifact (`SPEC.md`, `REPORT.md`, etc.) into `/output/`.
9. **Surface Open Questions Outward** — For every unresolved question discovered during the run, the agent MUST file a new prompt under `/prompts/` with `prompt_kind: follow-up` and `prompt_spawned_from_research: <this-slug>`. List those new prompt slugs in this research's `readme.md` under an "Open Questions Surfaced" heading. The agent MUST NOT amend the research output post-closure to track follow-ups.

## 5. Mandatory Pre-Commit Checks for Research Tasks

The agent MUST run `tools/check-governance.sh` before committing any change to `/research/`. The agent MUST NOT commit if that script exits non-zero. The ten checks below are mechanically enforced by the linters mapped in §5.0.

### 5.0 Mechanical Enforcement Mapping

| Check | Tool | Failure mode |
|---|---|---|
| §5.1 Prompt Snapshot Integrity | human review | No mechanical check — content equality |
| §5.2 Prompt Linkage | [`tools/lint-linkage.py`](./tools/lint-linkage.py) | `research_executes_prompt` doesn't resolve |
| §5.3 Workspace Cleanliness | human review | No mechanical check — file content |
| §5.4 No Empty Files | human review | No mechanical check |
| §5.5 Batch Readme Audit | [`tools/lint-structure.py`](./tools/lint-structure.py) | Missing `readme.md` in research folder |
| §5.6 Session Logging | human review | No mechanical check |
| §5.7 Synthesis Verification | human review | No mechanical check |
| §5.8 Output Verification | [`tools/validate-frontmatter.py`](./tools/validate-frontmatter.py) | Missing L1/L2 keys in `output/SPEC.md` |
| §5.9 Friction Reflection | human review (currently); [`tools/check-trust.py`](./tools/check-trust.py) when wrapped by a Task | Missing `friction-log.md` |
| §5.10 Open-Questions Outward Routing | [`tools/lint-linkage.py`](./tools/lint-linkage.py) | External `result.md` without downstream task |

Before committing, the agent MUST satisfy:

1. **Prompt Snapshot Integrity** — `prompt.md` exists and matches the prompt body at run-start.
2. **Prompt Linkage** — `research_executes_prompt` resolves to `/prompts/<slug>/`.
3. **Workspace Cleanliness** — No execution scripts (`.py`, `.sh`) remain in `/workspace`. Only raw notes, dumps, and `session.log` may stay.
4. **No Empty Files** — No required file (`session.log`, `post-synthesis-log.md`, `state.md`, `readme.md`) is 0 bytes.
5. **Batch Readme Audit** — Every touched folder has an updated `readme.md` per `FOLDERS.md`.
6. **Session Logging** — `/workspace/session.log` is populated and chronological.
7. **Synthesis Verification**
   - `/synthesis/` is structured and flattened.
   - `/synthesis/readme.md` contains hard results.
   - `/synthesis/post-synthesis-log.md` traces the merge sequence.
   - `/synthesis/state.md` shows every step `[x]`.
8. **Output Verification** — `/output/` contains the final deliverable with required frontmatter.
9. **Friction Reflection** — `/reflection/friction-log.md` exists and declares the highest FL experienced (FL0–FL3) at the top, per `FRUSTRATED.md`. Mandatory even at FL0.
10. **Open-Questions Outward Routing** — For every unresolved question, a corresponding `/prompts/<slug>/` exists with `prompt_kind: follow-up`.

All steps in `/synthesis/state.md` MUST be checked off before this pre-commit can pass.

## 6. External Research Ingestion (Third-Party Sources)

An **External Research Result** is a completed analysis produced by a third-party agent or model (e.g. Google Gemini, a contracted researcher) rather than by executing an in-house prompt from `/prompts/`. These results are raw material — they bypass the full `workspace / synthesis / reflection / output` pipeline but MUST still be traceable and MUST always trigger a downstream analysis Task.

### 6.1 Storage Path

External results live under a provider subfolder inside `/research/`:

```text
/research
└── /<provider>          # Normalized provider name: gemini | gpt | human | other
    └── /<slug>
        └── result.md    # Raw external output with required frontmatter
```

- `<provider>` is lowercase and normalized (e.g. `gemini`, `gpt`, `human`).
- `<slug>` is kebab-case derived from the research topic (max 6 tokens), NOT an internal prompt slug.

**Path-namespaced resolution:** Any linkage pointing to a research slug (e.g., `prompt_spawned_from_research` or `task_spawns_research`) MUST resolve if either `/research/<slug>/` exists OR `/research/<provider>/<slug>/` exists.

### 6.2 result.md Frontmatter

`result.md` MUST carry L1 Vault Core keys plus the `research_*` namespace. Set `research_executes_prompt` to the slug of the stub prompt created in §6.3.

```yaml
---
type: research
status: completed
slug: <slug>
summary: "Token-cheap tl;dr of the external result."
created: YYYY-MM-DD
updated: YYYY-MM-DD
research_phase: complete
research_executes_prompt: <slug>
research_friction_level: FL0
---
```

YAML MUST NOT nest beyond one level.

### 6.3 Stub Prompt

Create a minimal stub at `/prompts/<slug>/prompt.md` with:

- `prompt_kind: research-proposal`
- `prompt_target_agent: external`

This preserves the `Prompt → Research` audit graph even when execution happened outside the repository.

### 6.4 Ingestion Workflow

1. **Derive a slug** from the research topic (kebab-case, max 6 tokens).
2. **Store the result** — Create `/research/<provider>/<slug>/result.md`, paste the raw external output verbatim beneath the required frontmatter.
3. **Create a stub prompt** — Create `/prompts/<slug>/prompt.md` per §6.3.
4. **Update indexes** — Update `/research/readme.md` to reference the new provider folder or entry.
5. **Define a downstream Analysis Task** — Every ingested external result MUST be followed immediately by a new Task per §6.5. This step is not optional.

### 6.5 Mandatory Downstream Analysis Task

External results are unprocessed raw material. Every `result.md` MUST have a corresponding **open Task** in `/tasks/<NNN>-<slug>/` created in the same commit. The Task MUST satisfy:

| Requirement | Value |
|---|---|
| `task_status` | `open` |
| `task_priority` | `P1` (minimum) |
| `task_affects_paths` | MUST include path to `result.md` |
| Goal | Analyze the external result, cross-reference with in-house research, extract actionable recommendations, and define follow-up prompts for unresolved questions |

The analysis Task MAY be accompanied by a research workspace under `/research/<slug>/` if the analysis merits a full synthesis run; in that case the Task MUST list the spawned research slug in `task_spawns_research`.

## 7. Anti-Patterns

- **MUST NOT** craft prompts inside `/research/`. Prompts live in `/prompts/`.
- **MUST NOT** edit a `/research/<slug>/` workspace after `research_phase: complete` to insert follow-up questions. File a new prompt instead.
- **MUST NOT** treat a Research run as a standalone Task. If coordination across runs is needed, create a Task in `/tasks/` per `TASK.md`.
- **MUST NOT** ingest an external `result.md` without immediately creating a downstream analysis Task per §6.5 in the same commit.
