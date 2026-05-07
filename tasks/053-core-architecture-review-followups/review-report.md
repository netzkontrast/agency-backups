---
type: note
status: active
slug: 053-architectural-review-report
summary: "Verbatim architectural review of Agency's Machine/Actor/Space substrate, fm-toolchain, and governance pipeline. Captured 2026-05-07 against main@dbd996f. Findings B.1-B.10 are dispatched by Task 053 task.md Plan step 2-3."
created: 2026-05-07
updated: 2026-05-07
---

# Architectural Review — Agency Repository

> **Provenance.** Authored 2026-05-07 against `main@dbd996f93b01f3c2f5be98d068ab86e579a78234`. The line-anchor citations resolve at that commit; later readers SHOULD treat them as point-in-time references and re-verify before relying on them.

Here's an honest assessment based on reading the specs, tooling, and actual repo state.

---

## What's Good

**G.1 The core architecture is sound.**
The Machine/Actor/Space (Task/Prompt/Research) separation solves a real problem. Decoupling *what should be done* from *what the agent was told* from *what it produced* is the right mental model for long-horizon agent work. (`README.md` §1, lines 11–21.)

**G.2 Mechanical enforcement, not just social norms.**
The governance rules are actually enforced by linters (`validate-frontmatter.py`, `lint-structure.py`, `lint-linkage.py`) and a pre-commit hook. Reciprocity in the audit graph (e.g., a prompt must back-reference its task) is checked programmatically. (`tools/lint-linkage.py` lines 75–100.)

**G.3 The frontmatter ontology is clever.**
The L0–L3 layered schema with a hard YAML depth-1 constraint makes the filesystem queryable without a database, and the depth limit is a direct guard against LLM YAML-hallucination. (`AGENTS.md` lines 217–220.)

**G.4 The `fm/*` toolchain is well-engineered.**
The new toolchain (`tools/fm/`) is stdlib-only, has a proper `Diagnostic` type, a Levenshtein "did-you-mean" for typos, file locking for concurrent writes, and a real test suite including adversarial falsification tests. (`tools/fm/_core.py` lines 370–401; `tests/fm/test_falsification_attacks.py` lines 73–92.)

**G.5 The friction loop is a genuine self-improvement mechanism.**
FL0–FL3 logging is mandatory every session, and FL1+ entries are converted into Tasks by the maintenance run. The repo is designed to improve itself over time. (`MAINTENANCE.md` lines 99–103.)

**G.6 Maintenance bypass mode is pragmatic.**
The pre-commit hook allows commits with pre-existing errors *if* they're covered by an open Task — a sensible escape hatch that avoids blocking work while still tracking debt. (`MAINTENANCE.md` lines 140–141.)

---

## What's Bad / Limitations

**B.1 Dual-toolchain transition debt.**
There are two parallel linter stacks: the legacy `validate-frontmatter.py` / `lint-structure.py` / `lint-linkage.py` and the new `tools/fm/` suite. The new toolchain is only activated via `FM_TOOLCHAIN=1`. Tasks 017 and 019 are supposed to flip the default, but the gating in `tools/check-governance.sh:33` still defaults to legacy. This creates confusion about which tool is authoritative.

**B.2 The entry-point spec violates its own rules.**
`AGENTS.md` has a `LOOP_LOG` section appended at the bottom (lines 340–403) containing Jules session iteration records. This is runtime state living in a governance spec — exactly what `README.md §11.6 R.19` forbids. The very file that governs coherence has drifted.

**B.3 Duplicate task IDs are unresolved.**
There are multiple `006-*`, `009-*`, `031-*`, and `032-*` task folders. Tasks 013, 024, and 043 exist specifically to fix this, but the duplicates are still on disk. This undermines the `<NNN>-<slug>` naming convention that the tooling depends on.

**B.4 No CI/CD.**
There is no `.github/workflows/` or equivalent (a previous `adr-validate.yml` was deleted). Governance checks only run via the pre-commit hook, which must be manually installed per clone (`tools/install-hooks.sh`). Nothing enforces the rules on PRs automatically.

**B.5 Narrative ontology scope creep.**
The repo started as a governance substrate but now contains a full Dramatica narrative theory ontology (~215 entries), NCP bridge, novel-architect skills, Suno-lyric writer skills, and a `dramatica-nav` CLI. `AGENTS.md` has to explicitly warn agents *not* to load this for non-narrative work (rule `NO.5`, lines 249–252). This makes the repo significantly harder to understand for newcomers.

**B.6 Spec proliferation creates high onboarding cost.**
There are 9+ root spec files every agent must read before doing anything (`AGENTS.md`, `TASK.md`, `PROMPT.md`, `RESEARCH.md`, `FOLDERS.md`, `PRE_COMMIT.md`, `FRUSTRATED.md`, `MAINTENANCE.md`, `maintenance/language-spec.md`). The token cost of bootstrapping a session is substantial. (`README.md` §10, lines 179–190.)

**B.7 The hand-rolled YAML parser has silent failure modes.**
`read_fm()` calls `parse_frontmatter` with `strict=False` and silently returns `{}` on any error (`tools/fm/_core.py` lines 145–149). A file with malformed frontmatter will be treated as having no frontmatter, which can cause linters to emit misleading "missing keys" errors rather than "parse error".

**B.8 Research immutability is absolute.**
T4 protection means a completed research workspace can never be corrected — not even for typos. Errors in closed research are permanent by design. (`MAINTENANCE.md` line 33.)

**B.9 The closing procedure is Claude Code-specific.**
The mandatory `/sc:createPR` slash-command depends on the external SuperClaude Framework being installed. Jules and Gemini get vague "follow your own platform conventions" guidance. (`AGENTS.md` lines 74–77.) This is an asymmetry that makes the protocol incomplete for non-Claude agents.

**B.10 No integration tests.**
The test suite covers individual `fm/*` tools well, but there are no end-to-end tests simulating a full Task → Prompt → Research cycle through the governance pipeline.

---

## What I Would Do Differently

| Issue | Improvement |
|---|---|
| B.1 Dual toolchain | Complete the residual flip from `tools/check-governance.sh:33`, retire legacy linters, make `FM_TOOLCHAIN=1` the default. |
| B.4 No CI | Add a GitHub Actions workflow running `tools/check-governance.sh` on every PR. |
| B.2 `LOOP_LOG` in `AGENTS.md` | Move it to a dedicated `maintenance/session-logs/` file or a task's friction log. |
| B.3 Duplicate task IDs | Enforce uniqueness of `<NNN>` prefix in `tools/fm/check-duplicate-task-id.py` (gate, not advisory) so it can never happen again. |
| B.5 Narrative ontology | Extract it to a separate repo or at minimum a clearly isolated `skills/narrative/` sub-namespace with its own governance spec. |
| B.6 Spec count | Merge `PRE_COMMIT.md` into `AGENTS.md` as a section; merge `FRUSTRATED.md` into `MAINTENANCE.md`. |
| B.7 Silent YAML failures | Make `read_fm` emit a `WARN` diagnostic when `strict=False` parsing returns `{}` on a non-empty file. |
| B.9 Closing procedure | Define a platform-agnostic closing procedure (e.g., "create a PR via whatever mechanism your platform provides") and make `/sc:createPR` one implementation of it. |
| B.8 Research immutability | Allow T1/T2 repairs (frontmatter date bumps, broken links) on closed research; only block T3/T4 content changes. |
| B.10 Integration tests | Add a test that scaffolds a minimal Task → Prompt → Research graph and verifies `check-governance.sh` passes end-to-end. |

---

## Citations (Anchored to `main@dbd996f`)

**README.md (L11–21):**

```markdown
LLM agents lose coherence over long horizons. They forget intent, drift from prior decisions, blur the line between *what should be done*, *what the agent was told to do*, and *what running it produced*. They re-author prompts mid-research, inline instructions inside tasks, append follow-up questions to closed deliverables, and silently re-interpret governance.

This repository is an opinionated answer to that drift. It treats agentic work as a system with three intentionally **decoupled** concerns:

| Concept | Question it answers | Lives in |
|---|---|---|
| **Machine** — the *Task* | *What should be done?* (orchestration, plan, todo, ownership) | [`/tasks/`](./tasks) |
| **Actor** — the *Prompt* | *What is the agent told to do?* (executable instruction set) | [`/prompts/`](./prompts) |
| **Space** — the *Research* | *What did running it produce?* (evidence, synthesis, output) | [`/research/`](./research) |

The decoupling is enforced both socially (via specs) and mechanically (via linters and a pre-commit hook). A Task MUST NOT inline a prompt. Research MUST NOT author its own instructions. Follow-up questions MUST NOT be appended to a closed research workspace — they MUST be filed as new prompts. The audit graph that links the three is the source of truth.
```

**README.md (L179–190):**

```markdown
| Spec | Governs | Read it before… |
|---|---|---|
| [AGENTS.md](./AGENTS.md) | Entry-point routing, spec language, frontmatter, closing run procedure. | …doing anything in this repo. |
| [TASK.md](./TASK.md) | `/tasks/` — orchestration, lifecycle, Task frontmatter. | …creating a `task.md`. |
| [PROMPT.md](./PROMPT.md) | `/prompts/` — instruction-set authoring, prompt engineering principles. | …writing a `prompt.md`. |
| [RESEARCH.md](./RESEARCH.md) | `/research/` — execution workspaces, synthesis, reflection, output. | …executing a research run. |
| [FOLDERS.md](./FOLDERS.md) | Folder topology, slug rules, the `readme.md` rule, the audit graph. | …creating any new folder. |
| [PRE_COMMIT.md](./PRE_COMMIT.md) | Mandatory pre-commit checklist. | …every commit. |
| [FRUSTRATED.md](./FRUSTRATED.md) | FL0–FL3 friction logging. | …closing every session. |
| [MAINTENANCE.md](./MAINTENANCE.md) | Nightly maintenance + Repo Coherence Check. | …running self-improvement passes. |
| [`maintenance/language-spec.md`](./maintenance/language-spec.md) | Canonical RFC 2119 + Gherkin + frontmatter ontology. | …writing any normative clause. |
```

**tools/lint-linkage.py (L75–100):** linkage validation enforces that every `task_uses_prompts` slug resolves and that `task_spawns_research` is gated to closed Tasks only — confirms G.2.

**AGENTS.md (L74–77):** establishes `/sc:createPR` from the SuperClaude Framework as the canonical closing-run command — basis of B.9.

**AGENTS.md (L217–220):** YAML depth rule — basis of G.3.

**AGENTS.md (L249–252):** rules `NO.3`–`NO.6` partition the narrative ontology from non-narrative work — basis of B.5.

**AGENTS.md (L340–385):** `LOOP_LOG` runtime state appended to the entry-point spec — basis of B.2.

**tools/fm/_core.py (L145–149):** `read_fm` `try/except` collapses parse errors to `{}` — basis of B.7.

```python
def read_fm(path: Path, *, strict: bool = False) -> dict[str, Any]:
    try:
        return parse_frontmatter(path.read_text(encoding="utf-8"), strict=strict)
    except (OSError, Diag):
        return {}
```

**tools/fm/_core.py (L370–401):** Levenshtein implementation with transposition-cost adjustment — basis of G.4.

**tests/fm/test_falsification_attacks.py (L73–92):** P1 "`tpye` for `type`" adversarial test — basis of G.4.

**MAINTENANCE.md (L33):** T4 absolute-immutability clause for closed research — basis of B.8.

**MAINTENANCE.md (L99–103):** friction-to-Task conversion procedure — basis of G.5.

**MAINTENANCE.md (L140–141):** maintenance-bypass mode for pre-commit — basis of G.6.

**tools/check-governance.sh (L33–48):** legacy-default `FM_TOOLCHAIN` gating — basis of B.1 residual gap.

```shell
if [ "$FM_TOOLCHAIN" = "1" ]; then
  echo "(FM_TOOLCHAIN=1 — fm-validate is the gate; legacy runs advisory)"
  if ! "$PYTHON" tools/fm/validate.py; then
    FAIL=1
  fi
  echo "--- legacy validate-frontmatter.py (advisory) ---"
  "$PYTHON" tools/validate-frontmatter.py || true
else
  if ! "$PYTHON" tools/validate-frontmatter.py; then
    FAIL=1
  fi
  if [ -f "tools/fm/validate.py" ]; then
    echo "--- fm-validate (advisory; set FM_TOOLCHAIN=1 to gate) ---"
    "$PYTHON" tools/fm/validate.py >/dev/null 2>&1 || true
  fi
fi
```
