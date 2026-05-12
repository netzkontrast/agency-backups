# Friction Log — flexible-frontmatter-toolchain

**Highest FL reached this run: FL1.**

Per `FRUSTRATED.md`, this declaration is mandatory even at FL0.

## FL Declaration

- **FL1 — minor friction recovered without scope change.**

## Concrete Friction Encountered

1. **Anthropic GitHub API parse glitch (FL1).** The first attempt at `curl -sSL https://api.github.com/.../skill-creator/scripts | python3 -c '... [i["name"] for i in json.load(sys.stdin)]'` failed because the response was a single dict (rate-limited) on one shell, but a list on a parallel shell. Resolved by re-issuing the call with explicit error-handling. Time lost: ~30s.
2. **Skills-skill-bootstrap sync expectation (FL0).** The new `/skills/skill-creator/` mirror is a manual import, not driven through `skills-skill-bootstrap/sync.sh`. Documented in the per-skill readme so a future coherence run does not flag it as orphan content.

## Friction Surfaces (None Blocking)

- **Slug-length squeeze.** `migrate-repo-to-flexible-toolchain` is exactly 5 tokens — the maximum allowed by `language-spec.md §4.3`. Acceptable; if a sixth token were needed, the convention would force an abbreviation. Logged so the convention's edge is visible.

## Disposition

- No follow-up prompts filed.
- Three open questions deferred into Task 016's todo list (`§Open Questions` in `output/SPEC.md`).
- The reversal of task 010's persisted-index strategy is documented in `M07-contradiction-log.md §C1`; the maintainer of task 010 should re-read its scope before continuing.
