---
schema_version: "3.1"
schema: research-prompt-render

provenance:
  created: "2026-05-07T00:00:00+00:00"
  skill_version: "3.3.1"
  phase: "phase3"
  slug: "pre-commit-readme-update-cadence"
  output_filename: "research-prompt.md"
  category_signal: "B"
  selected_methods: ["M07", "M01", "M04", "M12", "M13"]
  selected_framework_structural: "risen"
  cross_pollination_pair: ["a-into-b", "c-into-b"]
  previous_version: null
  revision_count: 0
  intent_ref: "(canonical — embedded inline; see §Research Objective)"
  meta_prompt_ref: "(rendered inline; no separate plan YAML produced)"

language: "en"
target_agent: "Claude Code (sc:agent dispatched executor)"
---

# Research Prompt — Pre-Commit Readme-Update Cadence (Wording Reconciliation)

> **For the executing AI:** You are dispatched to produce a single
> SPEC.md. This file is **self-contained**. You do NOT have access to
> the conversation that generated this prompt, the parent intent
> file, or the planning meta-prompt. Everything you need is below.
> All research is **CORPUS-INTERNAL**: read this repository (git log,
> spec files, recent PRs, recent commits). Do **NOT** invoke any
> external web-search tool — Tavily, WebFetch, WebSearch, or
> Context7 calls are out of scope and would be wasted budget.

---

## Meta-Header — Three Inline Layers

### Category Layer — B (Extraction / Plan-and-Execute)

This is a **deterministic-collection** task with a known target
schema (SPEC.md §1–§5). The shape is "compare ≥3 cadence options on
a defined token-cost axis, then lift one into two specs verbatim".
Treat findings as items to **collect and tabulate**, not hypotheses
to discover.

### Agentic Spine — ReAct (Reason · Act · Observe)

For every step below: state your **Reason** (which method
anchor — M07/M01/M04/M12/M13 — is firing and why), execute the
**Act** (the actual repo read / git query / file-write), then
**Observe** (write the structured finding to the workspace before
moving on). Anchors are listed under "Critical-Thinking Methods"
below.

### Structural Layer — RISEN (Role · Input · Steps · Expectations · Narrowing)

The R/I/S/E/N sections after CONSTRAINT BLOCKS carry the executable
plan. CONSTRAINT BLOCKS sit ABOVE RISEN because they are
load-bearing for every step.

---

## Research Objective

**Question:** When should an agent update operational `readme.md`
files in a multi-folder commit — per-touch (every file edit triggers
its folder readme), batched-at-pre-commit (one readme sweep right
before `git commit`), or hybrid (some touches eager, some lazy)?

**Question unpacked.** This is **NOT** "is documentation valuable?"
or "do readmes matter?" — those questions are settled. The two repo
specs disagree on **wording-level cadence**, not on policy:

- `PRE_COMMIT.md` §2 reads as "update *now*, right before the
  commit" — implying batched-at-pre-commit.
- `FRUSTRATED.md` (the operational protocol that names recurring
  friction patterns) lists per-file readme spam as an FL2-tier
  friction — implying eager per-touch updates are
  counter-productive.

The disagreement is **wording**, not policy direction. Resolve the
**wording**, do not relitigate the policy.

**Audience:** Repo maintainers and the dispatched executor for
**Task 037 ST-4** + **Task 062 B-1**. Those executors will lift §3
of your SPEC.md **verbatim** into PRE_COMMIT.md §2 and FRUSTRATED.md
§28. Your §3 paragraph MUST be **byte-identical between both
targets** (modulo a leading spec-name prefix the lifter inserts).

**Output format:** Markdown SPEC.md at the path declared in
CONSTRAINT BLOCK 4. Section shape is fixed (§1 → §5; see CONSTRAINT
BLOCK 3).

**Temporal scope:** corpus survey covers
`git log --since='2026-04-15' origin/main`. This is the
post-Task-031 era when the readme-cadence rule first started being
mechanically enforced. Earlier history is out of scope (different
governance regime, different incentives).

**Depth:** `standard`. Wording reconciliation, not greenfield
research. Do not expand.

**Success criterion:** Your SPEC.md §3 paragraph reads **identically**
(modulo spec-name prefix) into both PRE_COMMIT.md §2 and FRUSTRATED.md
§28, AND the falsification clause —
*"Wrong cut iff any choice yields >2× token cost vs. status quo"* —
does **not fire**.

**Known prior** (M05 surfaced upstream — no need to reopen): the
empirical corpus survey already shows the de-facto practice is
**batched-at-pre-commit**. In a recent 35-commit sample taken from
the temporal scope above, **zero** commits were per-file-readme-only
commits. Your job is to confirm or falsify that prior, not to
discover the answer cold.

**Known constraints** (binding):

- Do **NOT** propose schema changes (no new `readme.md` frontmatter
  keys, no path moves).
- Do **NOT** propose tool changes (no new linters, no new fm-toolchain
  flags). Wording reconciliation only.
- Do **NOT** modify the SPEC.md if it already exists at the output
  path — the parent task will tell you whether to overwrite.

---

## CONSTRAINT BLOCK 0 — Reflection Baseline (M0)

Before each major step, restate (in 1 line) what you are about to do
and why **this** step beats the cheapest alternative. After each
step, write a 1-line *post-act observation* into the workspace
session log. This is the audit trail the maintainer will read.

## CONSTRAINT BLOCK 1 — Source Priority Rules

Sources, in descending authority:

1. The two reconciliation targets: `PRE_COMMIT.md` §2 and
   `FRUSTRATED.md` (the section that contains the FL2 readme-spam
   pattern; identify by content, not number — the file's headings
   are RFC-2119/Gherkin, not numerical).
2. `MAINTENANCE.md` §3.2 (the static/dynamic partition rule the
   normative §2 text MUST stay consistent with).
3. `research/repo-maintenance-protocol-spec/output/SPEC.md` §3.1
   (prior research that already named the static/dynamic split).
4. `git log` output and the diffs of merged PRs in the temporal
   scope. **At least 3 PRs**: one with many readme updates, one
   with few, one between.
5. `tasks/037-pre-commit-spec-integration/task.md` and
   `prompts/research-pre-commit-readme-update-cadence/{prompt,brief}.md`
   for chain-level context.

External web sources: **forbidden** (corpus-internal scope).
Paywalled / external blogs / vendor docs: **forbidden**.

## CONSTRAINT BLOCK 2 — Temporal Scope

Corpus window: `git log --since='2026-04-15' origin/main`.
Rationale: post-Task-031, the era during which the readme-cadence
rule has been mechanically enforced; earlier commits ran under a
different governance regime and would skew the token-cost table.

Do **NOT** cite a commit older than 2026-04-15 in your token-cost
evidence (§1) without a written, in-line justification.

## CONSTRAINT BLOCK 3 — Output Section Shape (Hard)

SPEC.md must have these sections, **in this order, with these
headings**:

- `## 1. Token-cost comparison` — table with **≥3** cadence options
  (rows: `per-touch`, `batched-at-pre-commit`, `hybrid`, plus any
  additional you identify). Columns at minimum: `option`,
  `description`, `tokens-emitted-per-multi-folder-commit (estimate
  + sample)`, `friction-level (FL0–FL3)`, `corpus-evidence (commit
  SHA(s))`.
- `## 2. Normative rule` — exactly one paragraph naming the chosen
  cadence in **uppercase RFC-2119** keywords (`MUST` / `MUST NOT` /
  `SHOULD` / `MAY`). MUST stay consistent with `MAINTENANCE.md`
  §3.2's static/dynamic partition.
- `## 3. Drop-in wording (byte-identical)` — the verbatim paragraph
  that the executors of Task 037 ST-4 and Task 062 B-1 will lift
  into PRE_COMMIT.md §2 and FRUSTRATED.md §28. **A single fenced
  block.** Identical bytes for both targets, modulo a leading
  spec-name prefix (`From PRE_COMMIT.md §2:` / `From FRUSTRATED.md
  §28:`) which the lifter inserts. Do **not** include the prefix
  yourself.
- `## 4. Walkthrough on a recent corpus exemplar` — pick **one**
  commit from the temporal scope that touched ≥3 operational
  folders. Show: (a) which folders' readmes the rule would have
  touched, (b) at what cadence, (c) what the actual commit did, (d)
  whether actual matches rule (≥1 of the three options must match
  to keep falsification clean).
- `## 5. Acceptance` — Gherkin scenarios verifying §1, §2, §3, §4
  hold. One scenario per criterion in `brief.md`.

## CONSTRAINT BLOCK 4 — Output Location

Write SPEC.md to:

```
/home/user/agency/research/pre-commit-readme-update-cadence/output/SPEC.md
```

If a SPEC.md already exists at that path, **read it first**, then
either (a) supersede it via the maintainer's instruction, or (b)
escalate via `friction-log.md` and stop. Do NOT silently overwrite.

Frontmatter on SPEC.md MUST carry: `type: spec`, `status: active`,
`slug: pre-commit-readme-update-cadence`, `summary:` (1–2 sentences),
`created: <ISO-8601>`, `updated: <ISO-8601>`, `research_phase:
complete`, plus the L2 `research_*` keys mandated by RESEARCH.md.

---

## Critical-Thinking Methods (5 + M13 always-on)

You MUST anchor each non-trivial step in the loop on one of:

| Anchor | Method | When to choose |
|---|---|---|
| **M07-ContradictionLog** | Contradiction Log | Whenever PRE_COMMIT.md §2 wording and FRUSTRATED.md §28 wording diverge — log both sides verbatim, resolve in §3. |
| **M01-Falsification** | Falsification | When you propose a cadence rule, design **the** observation that would falsify it. The brief's clause `Wrong cut iff any choice yields >2× token cost vs. status quo` IS the falsification predicate; show your work. |
| **M04-ContrastClasses** | Contrast Classes | Every cadence claim is comparative ("X is cheaper than Y"). Make the baseline explicit in §1's table — never claim "cheaper" without naming the comparator. |
| **M12-BaseRate** | Base-Rate Anchoring | The "tokens-emitted-per-commit" column is a frequency claim. Anchor it on a **measured** sample (≥3 PRs from the corpus), not a guess. |
| **M13-AdversarialQueryExpansion** *(mandatory)* | Adversarial query expansion | Before settling §1's options table, expand axes: adjacent (per-PR? per-session?), opposing (no-readme-at-all? readme-frozen?), higher (whole-folder docs? README in repo root only?), lower (per-line readme update?). Discard cheap losers explicitly — leave the audit trail in workspace/session.log. |

Do not add methods. Do not drop methods. Method count is fixed at
5 + M13.

---

## R — Role (RISEN)

You are a **repo-historian + spec-writer hybrid** dispatched as
`/sc:agent`. Your output is a single SPEC.md. You write Markdown,
not code. You read git, you do not push commits — the parent task's
maintainer commits.

You SHOULD assume a repo-maintainer reading level: comfortable with
RFC-2119, Gherkin, ADRs, frontmatter, and the agency-repo's
four-layer separation (Task / Prompt / Research / Skill). You MUST
NOT teach those concepts in your output — link out instead.

## I — Input (RISEN)

Read these, in this order:

1. `PRE_COMMIT.md` §2 (the current "update now" wording).
2. `FRUSTRATED.md` — locate the section listing readme-spam as an
   FL2 friction (the file uses Gherkin Scenarios, not numbered
   headings; identify by content, then quote verbatim).
3. `MAINTENANCE.md` §3.2 (static/dynamic partition).
4. `research/repo-maintenance-protocol-spec/output/SPEC.md` §3.1.
5. `prompts/research-pre-commit-readme-update-cadence/brief.md` —
   the parent brief (you are executing the prompt this brief
   describes; treat it as ground truth for Acceptance Criteria).
6. `tasks/037-pre-commit-spec-integration/task.md` — chain context.
7. `git log --since='2026-04-15' --oneline origin/main` — sample at
   least **3 PRs**, deliberately diverse: one with many readme
   updates (the "high-water mark"), one with few/none (the "lazy"
   case), one in between.
8. `git show <sha> -- '**/readme.md'` for each sampled PR to count
   readme-byte deltas as a stand-in for token cost.

## S — Steps (RISEN)

For each step: emit a one-line ReAct **Reason** (cite the method
anchor), execute the **Act**, write the **Observe** to
`research/pre-commit-readme-update-cadence/workspace/session.log`.

### Step 1 — Verify the prior (M07 → M01)

- **Reason:** M07 — log the two divergent wordings side-by-side
  before resolving.
- **Act:** Open PRE_COMMIT.md §2 and FRUSTRATED.md §28 (locate by
  content), copy both verbatim.
- **Observe:** If the wordings disagree on cadence (not just style),
  proceed. If they actually agree on cadence and the disagreement is
  illusory, M01 has fired: STOP and escalate via friction-log.md
  ("research moot — specs already aligned"). The parent task lead
  decides whether to close the SPEC stub.

### Step 2 — Sample the corpus (M12 → M04)

- **Reason:** M12 — anchor the token-cost table on measured
  base-rates, not feel.
- **Act:** Sample ≥3 PRs from the temporal-scope window. For each:
  count distinct operational folders touched, count the readme byte
  delta, record commit SHA + date.
- **Observe:** Write the raw counts to workspace/session.log. These
  are the rows of §1's table.

### Step 3 — Build the cadence-options table (M13 + M04)

- **Reason:** M13 — expand axes before locking the option set.
- **Act:** Enumerate cadence options. **Mandatory rows:**
  `per-touch`, `batched-at-pre-commit`, `hybrid`. Optional rows
  surfaced via M13: `per-PR`, `per-session`, `frozen-readme`,
  others. For each: estimate tokens emitted on a typical
  three-folder commit, using the corpus sample as anchor.
- **Observe:** Write §1's table. Each row cites ≥1 commit SHA from
  the sample.

### Step 4 — Pick the cadence (M01)

- **Reason:** M01 — name the falsification predicate before naming
  the choice.
- **Act:** State: *"Cadence X is wrong iff X's token cost in §1's
  table exceeds 2× the status-quo column."* Then check each of the
  ≥3 options against that test. Pick the option that survives AND
  matches the corpus base rate (the prior says
  batched-at-pre-commit; if your evidence contradicts the prior,
  trust the evidence and document the surprise in friction-log.md).
- **Observe:** Write §2 — one paragraph, RFC-2119 keywords.

### Step 5 — Author the drop-in wording (M07 reconciliation)

- **Reason:** M07 — the wording must close the contradiction by
  being valid in BOTH spec contexts.
- **Act:** Write §3 — exactly one fenced paragraph. Constraints:
  - No section number ("§2", "§28") inside the paragraph; the
    surrounding spec already provides that.
  - No Markdown link to the other spec (would introduce a cycle).
  - Uppercase RFC-2119 keywords ONLY for normative force.
  - One named cadence option (the §2 winner), no waffle.
  - **Byte-identical** when read in either context — the only
    permitted variation is a leading spec-name prefix
    (`From PRE_COMMIT.md §2:` / `From FRUSTRATED.md §28:`) inserted
    by the lifter, NOT by you.
- **Observe:** Diff §3's wording against itself with a hypothetical
  prefix in each direction; the body bytes after the prefix MUST
  match. If they don't, rewrite.

### Step 6 — Walkthrough (M04 contrast)

- **Reason:** M04 — show §2's rule against the corpus baseline on a
  concrete commit.
- **Act:** Pick one commit from the sample that touched ≥3
  operational folders. For each touched folder: state which
  readme.md the §2 rule would update, at what cadence, vs. what the
  actual commit did. Annotate match / mismatch.
- **Observe:** Write §4. ≥1 of {per-touch, batched-at-pre-commit,
  hybrid} must MATCH actual behaviour, else falsification has
  fired.

### Step 7 — Acceptance (Gherkin)

- **Reason:** Spec convention — every acceptance criterion is a
  Scenario.
- **Act:** Write §5. One Scenario per acceptance criterion in
  `brief.md`. Anchor each with `# anchor: ac-NN`.
- **Observe:** Cross-check each Scenario against `brief.md`'s
  numbered acceptance list. Bijection MUST hold.

### Step 8 — Pre-Synthesis Integrity Check (M4)

Before declaring done, run the 8-item Pre-Synthesis Integrity Check:

1. Are §1's ≥3 options each anchored on a corpus commit SHA?
2. Does §2 use RFC-2119 keywords correctly (one normative claim
   per sentence)?
3. Is §2 consistent with MAINTENANCE.md §3.2's static/dynamic
   partition? (Read both; verify.)
4. Is §3 byte-identical-modulo-prefix in both target contexts?
5. Does §4 cite a commit from the temporal scope?
6. Does §4 show the rule's expected behaviour matches actual
   behaviour for ≥1 cadence option?
7. Is §5 a Gherkin bijection with `brief.md`'s acceptance list?
8. Does the falsification clause (>2× token cost vs. status quo)
   NOT fire on the chosen option?

If any item fails, loop the relevant step. Do NOT proceed to write
the final SPEC.md until all 8 pass. Log the integrity-check
results to workspace/session.log.

## E — Expectations (RISEN)

- A single `output/SPEC.md` with frontmatter conforming to RESEARCH.md.
- §1 ≥3 cadence options, each row with a commit SHA from the
  corpus.
- §2 unambiguous, RFC-2119, MAINTENANCE.md-§3.2-consistent.
- §3 byte-identical-modulo-prefix; one fenced paragraph; no cross-
  spec links.
- §4 walkthrough on a real, in-scope commit.
- §5 Gherkin bijection with `brief.md`'s acceptance list.
- `research_phase: complete` in SPEC.md frontmatter.
- A `reflection/friction-log.md` per FRUSTRATED.md FL[0–3] (FL0
  recorded explicitly if no friction occurred — silence is itself a
  defect under FRUSTRATED.md).
- `tools/check-governance.sh` exits 0 on the produced commit.
- A git commit (NOT pushed) whose message names "Task 037 ST-1" in
  its trailer.

## N — Narrowing (RISEN)

You are scoped to **wording reconciliation**, not a full audit of
the readme-cadence policy. **Out of scope:**

- Proposing new linters, new pre-commit checks, new fm-toolchain
  flags.
- Proposing schema changes (new frontmatter keys, path moves).
- Touching files outside
  `research/pre-commit-readme-update-cadence/` and
  `tasks/037-pre-commit-spec-integration/friction-log.md`.
- External web research (Tavily / WebFetch / WebSearch / Context7
  forbidden).
- Editing PRE_COMMIT.md or FRUSTRATED.md directly — those edits are
  Task 037 ST-4 / Task 062 B-1's remit, not yours. You produce the
  drop-in wording; you do not lift it.

If any of these become tempting mid-execution, that is a signal to
log to friction-log.md (FL1+), **not** to expand scope.

---

## Cross-Pollination — a-into-b + c-into-b (always-on for Cat-B)

### a-into-b — Hidden-items + Schema-gap pass

Before locking §1's table, ask: "Is there a cadence option I
haven't surfaced because the seed phrasing
(per-touch / batched / hybrid) hides it?" Specifically check
**per-PR** and **frozen-readme** as null-cases. Discard them
explicitly with a one-line rationale in workspace/session.log if
not used.

### c-into-b — World-Change Check

Before settling §3's wording, ask: "Has the underlying repo
practice changed mid-corpus?" If a major refactor in the temporal
window changed how readmes are touched (e.g., introduction of
fm-toolchain), split the corpus and weight recent commits more
heavily. Otherwise, single-window analysis stands.

---

## Batch Procedures (M3)

### Batch — Per-PR readme-touch survey

- **Cardinality:** ≥3 PRs from the temporal-scope window.
- **Per-iteration steps:**
  1. `git show <sha> --stat` — count touched folders.
  2. `git show <sha> -- '**/readme.md'` — count readme byte delta.
  3. Record `{sha, date, folders_touched, readmes_touched,
     readme_byte_delta}` to workspace/session.log.
- **Schema per row:**
  ```yaml
  sha: <40-char>
  date: <ISO-8601>
  folders_touched: <int>
  readmes_touched: <int>
  readme_byte_delta: <int signed>
  cadence_inferred: per-touch | batched-at-pre-commit | hybrid | none
  ```

These rows feed §1's table directly.

---

## Pre-Synthesis Integrity Check (M4)

(See Step 8 above. The same 8-item list applies — repeated here for
the final scan after §1–§5 are drafted but before SPEC.md is
written to disk.)

---

## Synthesis Schema — SPEC.md target shape

```markdown
---
type: spec
status: active
slug: pre-commit-readme-update-cadence
summary: "Wording reconciliation for the readme-update cadence
  rule shared by PRE_COMMIT.md §2 and FRUSTRATED.md §28; codifies
  the de-facto batched-at-pre-commit practice with a byte-identical
  drop-in paragraph."
created: 2026-05-07
updated: 2026-05-07
research_phase: complete
research_executes_prompt: research-pre-commit-readme-update-cadence
---

# Pre-Commit Readme-Update Cadence — Reconciliation SPEC

## 1. Token-cost comparison
<table; ≥3 rows; each row cites ≥1 corpus commit SHA>

## 2. Normative rule
<one paragraph; RFC-2119; consistent with MAINTENANCE.md §3.2>

## 3. Drop-in wording (byte-identical)
```
<one fenced paragraph; no section numbers; no cross-spec links;
 byte-identical-modulo-prefix in PRE_COMMIT.md §2 and FRUSTRATED.md §28>
```

## 4. Walkthrough — <commit SHA short>
<one in-scope commit; show rule-vs-actual; match/mismatch annotated>

## 5. Acceptance
<Gherkin Scenarios; bijection with brief.md acceptance list;
 # anchor: ac-NN on each>
```

---

## Self-Verification Checklist (11 items — for the executing AI)

Before declaring SPEC.md done, confirm each:

1. SPEC.md path is `/home/user/agency/research/pre-commit-readme-update-cadence/output/SPEC.md`.
2. SPEC.md frontmatter has `type: spec`, `status: active`,
   `research_phase: complete`, `slug:
   pre-commit-readme-update-cadence`.
3. §1 has ≥3 rows; each row cites ≥1 commit SHA from the temporal
   scope.
4. §2 uses RFC-2119 keywords (one normative keyword per sentence)
   AND is consistent with MAINTENANCE.md §3.2.
5. §3 is exactly one fenced block, no section-number references,
   no cross-spec Markdown links.
6. §3 wording is byte-identical-modulo-prefix when imagined inserted
   into both PRE_COMMIT.md §2 and FRUSTRATED.md §28.
7. §4 cites a commit whose date ≥ 2026-04-15.
8. §4 declares match/mismatch between rule and actual behaviour for
   ≥1 cadence option.
9. §5 contains one Gherkin Scenario per Acceptance Criterion in
   `brief.md`; each Scenario carries `# anchor: ac-NN`.
10. The falsification predicate (`>2× token cost vs. status quo on
    the chosen option`) is **NOT** triggered by §1's table.
11. `tools/check-governance.sh` exits 0 on the working tree before
    the maintainer commits.

If any item fails, loop the relevant step. Do not weaken the
criterion to make the item pass.

---

## End Marker

When all 11 checklist items pass and the friction log is written,
emit a final line to workspace/session.log:

```
RENDER_DONE pre-commit-readme-update-cadence <ISO-8601-utc>
```

The dispatching agent (Task 037 ST-1 driver) reads that line as the
hand-off signal.
