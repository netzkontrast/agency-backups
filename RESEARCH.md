---
type: spec
status: active
slug: research-spec
summary: "Root specification for /research/. Research is execution-only: it consumes a prompt and produces a workspace of evidence, synthesis, reflection, and a final output. Prompt-craft and follow-up question generation are out of scope and live in /prompts/."
created: 2026-05-02
updated: 2026-05-07
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

> **Note:** Research that documents a skill MAY set `research_documents_skill: <slug>` once the schema is ratified (Task 011).

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

### 2.2 Spec-Chunking for Long Synthesis Runs

A synthesis run that produces an `output/SPEC.md` larger than approximately **50,000 tokens** MUST be chunked along RFC-2119 aspect boundaries (one aspect per file, one anchor per scenario), per `research/spec-driven-research-agentic-workflows/output/SPEC.md`. Chunking by paragraph count or character length is NOT acceptable — the canonical boundary is the §-aspect that owns a coherent set of normative clauses. Below the 50k threshold the agent MAY emit a single SPEC.md.

Rationale: synthesis-time agent context exhaustion is the dominant FL2+ friction surface on long-horizon spec runs. Aspect-boundary chunking gives every downstream consumer (linters, ADR synthesizer, human reviewers) a stable anchor surface that survives subsequent edits.

## 4. Workflow Requirements

1. **Resolve the Prompt** — Confirm `/prompts/<slug>/prompt.md` exists. If it does not, the agent MUST stop and create one per `PROMPT.md`. Research MUST NOT fabricate its own instruction set.
2. **Initialize Directory** — Create the `<slug>` folder and the four subfolders (`workspace/`, `synthesis/`, `reflection/`, `output/`).
3. **Snapshot the Prompt** — Copy the prompt body into `/research/<slug>/prompt.md` (this is the immutable run-start snapshot, not a re-author). The snapshot is **lock-at-start**: if `/prompts/<slug>/prompt.md` is edited mid-run (by another session or by a maintenance pass), the executing agent MUST NOT re-snapshot the workspace copy. The mid-run divergence MUST be recorded in `workspace/session.log` and surfaced as an open question per §4.9; if the divergence materially changes the run's instructions, the agent MUST stop the run, set `research_phase: archived`, and file a fresh prompt for a new run rather than continue against a stale snapshot.
4. **Work in Workspace** — Save planning scripts, search logs, downloaded pages, and tracking files into `/workspace`. Do not pollute the root directory. Execution scripts (`.py`, `.sh`) MUST be deleted before final commit. This rule is mechanically enforced by [`tools/check-workspace-cleanliness.py`](./tools/check-workspace-cleanliness.py) at commit time per [§5.0](#50-mechanical-enforcement-mapping).
5. **Log the Session** — Append to `/workspace/session.log` chronologically. This is the terminal-level audit trail.
6. **Synthesize Structurally** — Populate `/synthesis/` flat (per `FOLDERS.md`) unless 4+ files of the same type accumulate.
7. **Reflect** — Apply the critical-thinking methods named in the executing prompt; one flat file per method in `/reflection/`. Log friction in `friction-log.md`.
8. **Deliver** — Move the final completed artifact (`SPEC.md`, `REPORT.md`, etc.) into `/output/`.
9. **Surface Open Questions Outward** — For every unresolved question discovered during the run, the agent MUST file a new prompt under `/prompts/` with `prompt_kind: follow-up` and `prompt_spawned_from_research: <this-slug>`. List those new prompt slugs in this research's `readme.md` under an "Open Questions Surfaced" heading. The agent MUST NOT amend the research output post-closure to track follow-ups.
10. **Pause-and-Resume (cross-session continuity)** — A research run that pauses across sessions MUST drop a `state.md` file at `/research/<slug>/workspace/state.md` per [`research/session-continuity-protocol-instantiation/output/SPEC.md`](./research/session-continuity-protocol-instantiation/output/SPEC.md). The file is OPTIONAL for runs that complete in one continuous session. On resume, the agent MUST execute the §3 resume protocol (staleness probes + step replay) defined in that SPEC and MUST NOT issue any tool call until every probe matches. A probe mismatch MUST trigger explicit reconciliation logged in `workspace/session.log`.

## 5. Mandatory Pre-Commit Checks for Research Tasks

The agent MUST run `tools/check-governance.sh` before committing any change to `/research/`. The agent MUST NOT commit if that script exits non-zero. The ten checks below are mechanically enforced by the linters mapped in §5.0.

### 5.0 Mechanical Enforcement Mapping

| Check | Tool | Failure mode |
|---|---|---|
| §5.1 Prompt Snapshot Integrity | human review | No mechanical check — content equality |
| §5.2 Prompt Linkage | [`tools/lint-linkage.py`](./tools/lint-linkage.py) | `research_executes_prompt` doesn't resolve |
| §5.3 Workspace Cleanliness | [`tools/check-workspace-cleanliness.py`](./tools/check-workspace-cleanliness.py) | `.py`/`.sh`/`.log` straggler under `/research/<slug>/workspace/` (R.4.4) |
| §5.4 No Empty Files | human review | No mechanical check |
| §5.5 Batch Readme Audit | [`tools/lint-structure.py`](./tools/lint-structure.py) | Missing `readme.md` in research folder |
| §5.6 Session Logging | human review | No mechanical check |
| §5.7 Trust-Audit GATE | [`tools/check-trust-audit.py`](./tools/check-trust-audit.py) | Schema-conformance < 80%, behavioral < 90%, or governance < 95% at `research_phase: complete` (Spec-J/K/L) |
| §5.8 Output Verification | [`tools/validate-frontmatter.py`](./tools/validate-frontmatter.py) | Missing L1/L2 keys in `output/SPEC.md` |
| §5.9 Friction Reflection | [`tools/check-fl-declaration.py`](./tools/check-fl-declaration.py) | Missing `friction-log.md` or no parseable FL[0-3] declaration |
| §5.10 Open-Questions Outward Routing | [`tools/check-external-result-downstream-task.py`](./tools/check-external-result-downstream-task.py) | External `result.md` without back-linked Task (R.6.5) |

Before committing, the agent MUST satisfy:

1. **Prompt Snapshot Integrity** — `prompt.md` exists and matches the prompt body at run-start.
2. **Prompt Linkage** — `research_executes_prompt` resolves to `/prompts/<slug>/`.
3. **Workspace Cleanliness** — No execution scripts (`.py`, `.sh`) and no stray trace logs (`.log` other than `session.log`) remain in `/workspace`. Only raw notes, dumps, and `session.log` may stay. Mechanically enforced by [`tools/check-workspace-cleanliness.py`](./tools/check-workspace-cleanliness.py); a workspace MAY carry a `.cleanignore` listing legitimate long-lived `.py`/`.sh` files (each line a glob relative to the workspace root).
4. **No Empty Files** — No required file (`session.log`, `post-synthesis-log.md`, `state.md`, `readme.md`) is 0 bytes.
5. **Batch Readme Audit** — Every touched folder has an updated `readme.md` per `FOLDERS.md`.
6. **Session Logging** — `/workspace/session.log` is populated and chronological.
7. **Trust-Audit GATE** — On any commit that transitions `research_phase` to `complete`, [`tools/check-trust-audit.py <workspace>`](./tools/check-trust-audit.py) MUST exit 0. The gate enforces three thresholds drawn from [`research/agentic-eval-trust-improvement-spec/output/SPEC.md`](./research/agentic-eval-trust-improvement-spec/output/SPEC.md): schema-conformance ≥ 80%, behavioral ≥ 90%, governance ≥ 95%. Diagnostics MUST follow the `<relpath>::ERROR:TRUST.<code>:<message>` format. The GATE is per-workspace; cross-workspace aggregation belongs to MAINTENANCE.md and is out of scope here.
8. **Output Verification** — `/output/` contains the final deliverable with required frontmatter.
9. **Friction Reflection** — `/reflection/friction-log.md` exists and declares the highest FL experienced (FL0–FL3) at the top, per `FRUSTRATED.md`. Mandatory even at FL0. Mechanically enforced by [`tools/check-fl-declaration.py`](./tools/check-fl-declaration.py).
10. **Open-Questions Outward Routing** — For every unresolved question, a corresponding `/prompts/<slug>/` exists with `prompt_kind: follow-up`. For every external `/research/<provider>/<slug>/result.md`, a back-linked Task MUST exist per §6.5; mechanically enforced by [`tools/check-external-result-downstream-task.py`](./tools/check-external-result-downstream-task.py).

All steps in `/synthesis/state.md` MUST be checked off before this pre-commit can pass.

### 5.11 Acceptance Scenarios

The following Gherkin scenarios bind the section's normative anchors. Each `# anchor:` is stable across edits; linters reference them via the diagnostic codes (`R.4.4`, `R.6.5`, `TRUST.*`).

```gherkin
# anchor: R.B.1 — prompt resolution
Feature: Prompt resolves before research workspace is created
  Scenario: Researcher attempts to create /research/<slug>/ without an executing prompt
    Given the agent intends to start a research run named "<slug>"
    And `/prompts/<slug>/prompt.md` does not exist
    When the agent attempts to create `/research/<slug>/`
    Then the agent MUST stop and create the prompt under `/prompts/<slug>/` first
    And the agent MUST NOT fabricate the executing prompt inside the research workspace
```

```gherkin
# anchor: R.B.2 — workspace cleanliness
Feature: Workspace is free of execution-script stragglers at commit
  Scenario: Pre-commit scan finds a leftover .py file in workspace
    Given a research workspace at `/research/<slug>/workspace/`
    And the workspace contains a file `scratch.py`
    When `tools/check-workspace-cleanliness.py` runs as part of pre-commit
    Then the linter MUST emit `<path>::WARN:R.4.4:execution-script-not-cleaned`
    And the agent MUST either delete the file or list it in `.cleanignore` with rationale
```

```gherkin
# anchor: R.B.3 — follow-up filing
Feature: Follow-up questions go to /prompts/, not amended into closed research
  Scenario: An open question surfaces after research_phase: complete
    Given a research workspace with `research_phase: complete`
    When the agent discovers a follow-up question
    Then the agent MUST create a new prompt under `/prompts/<new-slug>/`
    And the new prompt MUST set `prompt_kind: follow-up`
    And the new prompt MUST set `prompt_spawned_from_research: <this-slug>`
    And the agent MUST NOT amend the closed research workspace to record the question
```

```gherkin
# anchor: R.B.4 — external ingestion
Feature: External result triggers a downstream Task in the same commit
  Scenario: Pre-commit verifies result.md is paired with a back-linked Task
    Given a staged file at `/research/<provider>/<slug>/result.md`
    When `tools/check-external-result-downstream-task.py` runs as part of pre-commit
    Then the linter MUST locate a Task whose frontmatter back-links to the result
        (via `task_affects_paths`, `task_uses_prompts`, `task_spawns_research`,
         or `task_spawns_prompts`)
    And on missing back-link the linter MUST emit `<path>::ERROR:R.6.5:no-downstream-task`
    And the commit MUST be blocked
```

```gherkin
# anchor: R.B.5 — trust-audit gate
Feature: Research closure is blocked on trust-audit failure
  Scenario: Researcher attempts to set research_phase: complete on a workspace with insufficient governance score
    Given a research workspace at `/research/<slug>/` with `research_phase: synthesis`
    And `output/SPEC.md` exists
    When the agent stages a frontmatter edit setting `research_phase: complete`
    Then `tools/check-trust-audit.py <workspace>` MUST run as part of pre-commit
    And the commit MUST be blocked if any of the three thresholds fail
        (schema-conformance ≥ 80%, behavioral ≥ 90%, governance ≥ 95%)
    And the diagnostic format MUST match `<relpath>::ERROR:TRUST.<code>:<message>`
```

```gherkin
# anchor: R.B.6 — session continuity
Feature: Multi-session resume validates staleness before executing
  Scenario: Agent resumes a paused research run
    Given a research workspace whose `workspace/state.md` records the prior checkpoint
    When the resuming agent loads `state.md`
    Then the agent MUST run the §3 resume protocol from
         `research/session-continuity-protocol-instantiation/output/SPEC.md`
    And the agent MUST verify every staleness probe (git-head, session-log-mtime,
        readme-updated, parent-task-status) before issuing any tool call
    And on any probe mismatch the agent MUST log a reconciliation entry in `session.log`
        and obtain explicit human acknowledgement before continuing
```

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
