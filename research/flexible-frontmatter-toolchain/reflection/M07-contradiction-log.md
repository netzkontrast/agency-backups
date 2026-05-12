# M07 — Contradiction Log

Three contradictions surfaced during synthesis. Each is logged, attributed, and resolved.

## C1 — Stored Index vs. Stateless

- **Claim A** (`tasks/010-skills-frontmatter-index-suite/task.md`, lines 28–37): the repo SHOULD persist `.agent_cache/frontmatter-index.json` and gate commits on its freshness, because Jules and Gemini cannot run repo-local Python.
- **Claim B** (this prompt's mandate): there is no need to store an index file; stored indexes drift, and freshness is impossible to guarantee mechanically.
- **Hypothesised cause.** Claim A optimises for cross-agent portability assuming a closed file budget; Claim B optimises for *correctness under drift* — accepting a small per-query cost to remove an entire failure class.
- **Evidence to resolve.** A live filesystem scan over the operational roots completes in well under the agent's per-query budget. The drift-protection cost (rebuild-on-every-commit, fail-on-staleness) imposed by Claim A is itself non-trivial — it adds a pre-commit step that must walk the same files anyway.
- **Resolution.** Drop the persisted index. **Narrow Task 010 to the *query-CLI* contract only** (every command must work as a stateless function over the live tree). Cross-agent portability is preserved because the CLI is a thin Python script with no external dependencies. Recorded in `output/SPEC.md §5.4`.

## C2 — Count-Based Failure vs. Required-Only

- **Claim A** (implicit in early drafts of MAINTENANCE.md not present in the current version, but referenced by the user's mandate as a pattern to avoid): "if a spec has more than 9 headings it fails".
- **Claim B** (this prompt's mandate): the spec MUST fail only when *required* parts are missing.
- **Hypothesised cause.** Count-based heuristics were a proxy for "is this spec under control?" before there was a concrete required-section list. Now that we can enumerate the required sections, the proxy is harmful.
- **Resolution.** SPEC §4 enumerates required `## ` headings per `type:`. Validators MUST NOT count headings; they MUST set-difference against the required list. Recorded in `output/SPEC.md §4`.

## C3 — Root-Spec Immutability vs. T2 Repair

- **Claim A** (`MAINTENANCE.md §1`): root governance specs are subject to T1/T2 repairs only.
- **Claim B** (the migration described in this synthesis): the new spec **adds new required sections** to `RESEARCH.md` / `TASK.md` / `PROMPT.md` headers (specifically, `## Constraints` becomes required on every prompt; current prompts have it but the rule isn't enforced).
- **Hypothesised cause.** A T2 fix is "additive frontmatter"; a T3 fix is "structural". Adding a required section to root specs straddles these tiers.
- **Resolution.** This change is **T3** — it cannot be applied during a coherence run and must be carried out by the migration task (017). The migration task's pre-flight verifies that the new required sections are already present in every existing root spec; if any are missing the task pauses and writes a follow-up Task. Recorded in `output/SPEC.md §8`.
