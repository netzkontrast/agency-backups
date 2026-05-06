---
type: note
status: active
slug: pr67-review
summary: "Code review of PR #67 (implement agency-adr CLI per Task 028 plan). Identifies governance violations, technical issues, and positive findings."
created: 2026-05-06
updated: 2026-05-06
---

# PR #67 Review — `agency-adr` Implementation

**PR:** [#67 feat(adr): implement agency-adr CLI per Task 028 plan](https://github.com/netzkontrast/agency/pull/67)
**Commits reviewed:** `97719e7` + `1643110`
**Reviewer:** claude-code (session `claude/stoic-mendel-4Fryj`)
**Date:** 2026-05-06

---

## Executive Summary

The implementation is technically solid: the module decomposition follows the plan exactly, test coverage is comprehensive (202 tests, all passing), and spec anchors are cited throughout. However, there are **two critical governance violations** that MUST be resolved before merge, plus several significant and minor technical findings.

---

## Critical — Governance Violations

### G.1 — No Task Entry for the Implementation

**Severity: ERROR / Blocker**

The implementation spans 33 files and 2,446 insertions including GitHub Actions, PRE_COMMIT.md hooks, header-ontology schema additions, and a full Python package. This is unambiguously a coordinated unit of work as defined in TASK.md §1:

> "When the agent is asked to perform a unit of work that is neither a pure prompt-craft nor a pure research execution, the agent MUST treat it as a Task."

No Task entry exists in `/tasks/` for this implementation. Consequences:

- No `friction-log.md` (required for all closed work, even FL0, per TASK.md §7.8)
- No `task_affects_paths` declaration (makes future audit impossible)
- No `task_status` lifecycle record
- `tasks/readme.md` was not updated (required per TASK.md §4.8 in the same commit as any new coordinated work)

**Required action:** Create `tasks/030-adr-tooling-impl/` (or next free slot if 030 is taken) with a `task.md`, close it as `done`, and add a `friction-log.md`. Update `tasks/readme.md` accordingly.

### G.2 — Prompt Boundary Violation

**Severity: ERROR**

The prompt governing this work is `prompts/adr-tooling-impl-plan/prompt.md`. Its `## N — Narrowing` section states:

> "Scope: implementation planning only. Do not modify the ADR governance spec produced by Task 027."

And its explicit non-goals block reads:

> **Non-goals:**
> - Writing any `tools/adr/*.py` code.
> - Writing any test fixtures.
> - Writing the GitHub Actions YAML.

This implementation crossed all three non-goals. Either:
1. The implementing agent used the Task 028 `implementation-plan.md` as an informal prompt without a registered prompt artifact — violating PROMPT.md §1 ("every artifact whose primary purpose is to instruct an agent MUST be stored under `/prompts/<slug>/`"); or
2. A separate unregistered prompt was used.

**Required action:** Register the instruction set that drove the implementation as a proper `prompt.md` under `/prompts/<slug>/`, with correct `prompt_kind: task-spec` frontmatter and a backward link to the Task entry created per G.1.

---

## Significant — Technical Findings

### T.1 — Token-count heuristic creates silent fidelity-floor drift

**Severity: WARN**

`compress.py:count_tokens` uses whitespace splitting:

```python
def count_tokens(text: str) -> int:
    return len(text.split())
```

The default `--token-limit` is 2000 and the default `--fidelity-floor` is 0.95. For governance-prose content (the synthesis block), BPE token counts (what LLMs actually count) typically run 1.2–1.5× higher than whitespace-split counts. A "2000-token" synthesis block under this heuristic may be 2600–3000 real tokens when fed to a model. The implementation plan acknowledges this as OD.7 with "sufficient for v0", but:

- The `count_tokens` docstring says "heuristic" without quantifying the expected divergence
- `--token-limit=2000` implies an LLM-budget ceiling, but the ceiling is measured with a mismatched ruler

**Suggested fix:** Add a one-line note to the docstring stating the expected BPE over-count range (e.g., "BPE counts for prose typically run 1.2–1.5× higher"). Consider renaming the default to `--token-limit=1400` to compensate for the heuristic gap, or document the calibration assumption in the CLI help text.

### T.2 — stdout/stderr split in `_emit` is undocumented

**Severity: WARN**

`cli.py:_emit` writes text diagnostics to `sys.stderr` but JSON output (`--format=json`) to `sys.stdout` (via `print()`). This split is reasonable CI practice — JSON is machine-readable output, text is human-readable status — but the function's behaviour is not documented, and the JSON output includes an implicit `"written": result.written` only in `run_synthesize_cmd`, not in `_emit`. A consumer piping `--format=json` output will capture only the JSON, while text-mode output leaks to stderr. Inconsistency: the text-mode `_emit` call passes `stream=sys.stderr` explicitly, but the json-mode print uses the default stdout without comment.

**Suggested fix:** Add a one-line comment in `_emit` ("JSON emitted to stdout; text diagnostics to stderr — intentional CI split") and ensure the CLI man-page (if added) documents this.

### T.3 — `decisions_root` default is a relative path in library function

**Severity: WARN**

`synthesize.py:synthesize` declares:

```python
def synthesize(
    *,
    agents_md: Path,
    decisions_root: Path = Path("decisions"),
    ...
)
```

`Path("decisions")` is relative to the current working directory at call time, not to `repo_root`. In practice, `load_corpus(decisions_root, repo_root=repo)` resolves this against `repo`, so the default is never used when called via `cli.py`. However, a caller invoking `synthesize()` directly from a different working directory would silently use the wrong path. Library functions should use `Path | None = None` and derive the path from `repo_root` inside the function body.

### T.4 — DFS cycle recovery may leave nodes unvisited across iterations

**Severity: INFO** (correctness is preserved; performance risk only)

In `graph.py:detect_cycles`, the nested `dfs()` function adds `node` to `seen` only on clean exit (the last line before returning `False`). When a cycle is found (`return True`), the nodes visited during that DFS call are **not** added to `seen`. The outer `for start in sorted(residual)` loop will therefore revisit those nodes in subsequent iterations, producing redundant (but idempotent) cycle reports for the same cycle. With a small ADR corpus this is inconsequential; with a large graph of cross-referencing ADRs it could produce duplicate diagnostics.

**Suggested fix:** Add `seen.add(node)` before the cycle-found `return True` path, or post-process `diags` to deduplicate by cycle membership.

---

## Minor — Code Quality

### Q.1 — `sys.path` mutation is repeated in every module

Every `tools/adr/*.py` file contains:

```python
_TOOLS = str(Path(__file__).resolve().parent.parent)
if _TOOLS not in sys.path:
    sys.path.insert(0, _TOOLS)
```

This is consistent with `tools/fm/` but creates a maintenance surface: if the package is ever moved or the `tools/fm` layout changes, every file needs updating. A centralized `tools/adr/__init__.py` boot-shim would reduce this to one location. Low priority given the repo's Python-script convention, but worth noting.

### Q.2 — `runlog.append_run_record` signature drifted from the plan

`implementation-plan.md §2` specifies:

```python
def append_run_record(result: SynthesizeResult) -> None:
```

The actual call in `synthesize.py` passes individual keyword arguments:

```python
append_run_record(
    run_log=run_log,
    contributing_adr_ids=section.contributing_adr_ids,
    token_count=section.token_count,
    fidelity=fid,
    ...
)
```

This is not a bug (the keyword-argument form is arguably cleaner), but it is an undocumented plan deviation. Future agents reading the plan and the code will see a mismatch.

---

## Positive Findings

The following are done correctly and should be preserved:

| Item | Verdict |
|---|---|
| Spec anchor citations in every module (`ADR.A.x.y`) | Compliant |
| Kahn's algorithm for cycle detection | Correct |
| 202 tests mapping to Gherkin anchors | Comprehensive |
| Idempotent synthesize (marker-bounded equality check) | Correct |
| `TokenLimitExceeded` exception carries deprecation candidates | Good UX |
| `llm-pass` raises `NotImplementedError` instead of returning 0 | Correct signal |
| Empty-corpus graceful no-op (exits 0) | Correct |
| `diagnostic-explanations.json` for `--explain` support | Forward-looking |
| `adr_id` deduplication in `compress` aggregates all citing ADRs | Correct (fixed in 1643110) |
| ADR.A.1.4 enforcement (≥2 options in Considered Options) | Correct (added in 1643110) |

---

## Required Actions Before Merge

1. **[BLOCKER G.1]** Create an implementation Task entry (next free `<NNN>-adr-tooling-impl`) with `task.md`, `friction-log.md`, and `tasks/readme.md` update.
2. **[BLOCKER G.2]** Register the instruction set that drove the implementation as a prompt artifact, or document why the implementation plan document served as the prompt and what governance rule covers that.
3. **[WARN T.1]** Document the whitespace-split token heuristic divergence in `count_tokens` and consider calibrating the default `--token-limit`.
4. **[WARN T.2]** Document the stdout/stderr split in `_emit`.
5. **[WARN T.3]** Fix `decisions_root` default to `None` and derive from `repo_root` inside `synthesize()`.

Items 3–5 SHOULD be resolved before merge but MAY be deferred to a follow-up task with documented justification.
