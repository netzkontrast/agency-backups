---
type: note
status: active
slug: task-016-implementation-notes
summary: "Implementation decisions and resolutions for SPEC §10 Q1/Q2 captured during Task 016 execution."
created: 2026-05-05
updated: 2026-05-05
---

# Task 016 — Implementation Notes

## Resolution of SPEC §10 Open Questions

### Q1 — Submodule / sparse-checkout interaction

**Question.** "How does fm-query interact with submodules or sparse checkouts?"

**Resolution.** `fm-query` walks the filesystem from the resolved
operational roots (`/tasks/`, `/prompts/`, `/research/`, `/skills/`,
`/maintenance/`, `/tools/`, `/templates/`). Three concrete behaviours:

1. **Submodules.** `Path.rglob("*.md")` follows submodule worktrees the
   same way it follows ordinary subdirectories: any `.md` file present
   on disk is read. We do not consult `.gitmodules`, do not call out to
   `git`, and do not skip submodule paths. If a submodule is checked
   out, its frontmatter participates in queries; if it isn't, the path
   simply doesn't exist on disk and is skipped silently.
2. **Sparse checkouts.** Identical semantics — if the file is not in
   the working tree, it isn't queried. There is no fallback to
   `git ls-files` because `fm-query` MUST NOT depend on git
   availability (per SPEC §9 anti-pattern: "depend on git availability
   inside skill containers"). This matches the no-git constraint from
   `research/skills-skill-container-capabilities/output/SPEC.md §3.1`.
3. **Implication for callers.** A coherence run executed inside a
   sparse checkout sees only the materialised slice of the repo. This
   is by design: the toolchain is intentionally local and stateless.
   If a future caller needs whole-tree visibility from a sparse
   checkout, they MUST materialise the relevant cone first.

This resolution is additive: it documents existing behaviour rather
than adding new code paths. No SPEC amendment is required.

### Q2 — `fm-edit --batch` mode

**Question.** "Should fm-edit grow a --batch mode reading mutations
from stdin/JSON? Default answer: not in v1."

**Resolution.** **Not in v1.** The reasoning that the SPEC defaulted
to "no" survives review:

- A batch mode would weaken the "one diagnostic per problem, one
  command per mutation" property that makes shell pipelines auditable.
- Concurrency safety in v1 is anchored on the OS file lock around
  *one* read-modify-write per invocation. A batch mode would either
  hold the lock across many mutations (long-running write lock,
  starves readers) or take/release the lock per mutation (no
  cross-mutation atomicity). Neither is appealing without a concrete
  caller demanding it.
- Callers that want batch semantics today can compose: `xargs -n1`,
  `for path in $(fm-query …); do fm-edit "$path" --bump-updated; done`.
  The token cost of these compositions is marginal (each `fm-edit`
  invocation is < 50 ms in CPython 3.11).

The decision is revisitable when a concrete caller (likely the
coherence-check prompt) shows a benchmark where shell-loop overhead
dominates. Until then, `--batch` is intentionally absent.

## Implementation deviations from prose SPEC

The following choices preserve the SPEC's intent while differing
slightly from the prose. They are documented here so Task 017 can
fold them back into a SPEC amendment if desired.

1. **Levenshtein flavour.** SPEC §3.4 says "Levenshtein-distance 1".
   The §6.1 example uses `tpye` → `type`, which is *Damerau*-Levenshtein
   1 (transposition) but standard Levenshtein 2. The implementation
   uses Optimal String Alignment (Damerau-restricted) so the SPEC's
   own example passes. SPEC §3.4 should be amended to read
   "OSA distance 1" or "transposition-aware Levenshtein 1".
2. **Skill required keys.** SPEC §3.2 says skill requires
   `skill_kind, skill_target_agents`. SPEC §6.1 example treats
   `name` as required. The header-ontology JSON encodes `name` and
   `description` as REQUIRED for `type=skill`, and
   `skill_kind, skill_target_agents` as RECOMMENDED. This matches the
   live SKILL.md format (Anthropic) and what §6.1 actually tests.
3. **Heading punctuation stripping.** SPEC §4.2 says
   "stripping em-dashes and surrounding whitespace". The
   implementation also strips trailing colons (matching the §4.2
   example `## Goal:` ↔ `## Goal`), trailing en-dashes, and trailing
   hyphens. Embedded em-dashes (`I — Input`) are preserved so that
   composite headings still match exactly.
4. **Heading walker skips fenced code.** A `## ` literal inside a
   triple-backtick or triple-tilde fence is NOT counted as a heading.
   Authors paste shell or markdown samples into prose; we MUST NOT
   treat their `## …` lines as heading constraints.

## Known fm-validate failures on the live tree

Running `python3 tools/fm/validate.py` against the staged tree at
task close emits 146 diagnostics. They fall into two buckets, both
expected:

- **35 × F.3.3** — readme.md files inside `/research/<slug>/{workspace,
  reflection,synthesis,output}/` are not currently required to carry
  frontmatter (the legacy validator only checks the slug-level
  readme). The flexible toolchain takes the stricter view that any
  `*.md` whose path resolves to an operational pattern needs FM.
  Migration is Task 017 / Batch 2.
- **111 × F.4.2** — prompt.md files use parenthetical heading hints
  (e.g., `## I — Input (to flesh out)`) that don't match the §4.1
  required headings under strict normalisation. Migration is Task 017.

Both buckets were already present before this task — they are
visible-but-unblocked because `tools/check-governance.sh` continues
to use the legacy validator unless `FM_TOOLCHAIN=1` is set. Task 017
is responsible for fixing the underlying files (or relaxing the
required-headings list) before flipping the gate.
