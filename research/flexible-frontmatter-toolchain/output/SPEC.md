---
type: research
status: completed
slug: flexible-frontmatter-toolchain
summary: "Spec for a flexible (required-only) maintenance contract plus a stateless validate/edit/extract/query toolchain that supersedes count-based linters and stored indexes."
created: 2026-05-05
updated: 2026-05-05
research_phase: complete
research_executes_prompt: flexible-frontmatter-toolchain
research_friction_level: FL1
---

# Flexible Frontmatter Toolchain Specification

## §1. Normative Conventions

The key words MUST, MUST NOT, REQUIRED, SHALL, SHALL NOT, SHOULD, SHOULD NOT, RECOMMENDED, NOT RECOMMENDED, MAY, and OPTIONAL in this document are to be interpreted as described in BCP 14 [RFC 2119] [RFC 8174] when, and only when, they appear in all capitals as shown here.

Spec letter for normative-clause anchors: **F** (Flexible-toolchain). Each clause carries a `# anchor: F.<section>.<index>` comment in this document and SHOULD be cited by external references.

## §2. Executive Summary

This spec defines two coupled deliverables:

1. **A flexible maintenance contract.** Validation passes when every *required* part is present; it ignores extras. There is no count-based check (no "fails when more than N headings"). Required parts are enumerated per `type:` and are short by design.
2. **A stateless toolchain.** Four CLI tools (`fm-validate`, `fm-extract`, `fm-edit`, `fm-query`) operate on the live filesystem with no persisted index. Token efficiency comes from *what* the tools return (one heading body, not a whole file), not from caching.

The spec inherits the L0/L1/L2/L3 frontmatter ontology from `maintenance/language-spec.md §4` and the T1/T2/T3/T4 repair ladder from `MAINTENANCE.md §1`. It supersedes the persistent-index strategy proposed in `tasks/010-skills-frontmatter-index-suite/` (see `reflection/M07-contradiction-log.md §C1`).

## §3. Required Frontmatter Keys (Per `type:`)

A file's **required key set** is the union of L1 (always required for operational files) and the L2 namespace selected by its `type:` value.

```text
# anchor: F.3.1
L1 (required for every operational file):
  type, status, slug, summary, created, updated

# anchor: F.3.2
L2 by type (required when present in the matching directory):
  type: task        →  task_id, task_status, task_owner, task_priority,
                       task_uses_prompts, task_spawns_research,
                       task_spawns_prompts, task_affects_paths
  type: prompt      →  prompt_kind, prompt_framework, prompt_target_agent
  type: research    →  research_phase, research_executes_prompt,
                       research_friction_level
  type: skill       →  skill_kind, skill_target_agents
                       (further skill_* keys are RECOMMENDED, not required)
  type: spec        →  (no L2 required; L1 only)
  type: index       →  (no L2 required; L1 only)
  type: readme      →  (no L2 required; L1 only)
  type: note        →  (no L2 required; L1 only)
```

### §3.3 Pass / Fail Semantics

```text
# anchor: F.3.3
fm-validate MUST FAIL when, for the file under inspection:
  - the YAML frontmatter block is absent, malformed, or nests deeper than 1 level;
  - any L1 required key is absent;
  - any L2 required key for the file's type+location is absent;
  - the slug field contains whitespace or characters outside [a-z0-9-];
  - the value of `type:` is outside the closed set in §3.2;
  - the value of `status:` is outside { draft, active, blocked, completed, archived };
  - any required-headings test in §4 fails.

fm-validate MUST PASS when:
  - all required keys are present (extras are ignored);
  - extra optional keys appear (e.g., `tags`, `aliases`, `cssclasses`, custom L0/L2);
  - the file body is longer than any historical norm;
  - the file contains more than 9 — or more than 99 — `## ` headings.
```

### §3.4 Typo Detection (Did-You-Mean)

```text
# anchor: F.3.4
fm-validate MUST emit a `did-you-mean` diagnostic (severity: ERROR) when an
unknown key's name is within Levenshtein-distance 1 of any required key.
This rule preserves the "extras pass" principle (intentional optional keys
like `tags`, `aliases` are not near-misses) while catching typo regressions.
```

## §4. Required Headings (Per `type:`)

The validator walks only `## ` (level-2) headings. Deeper levels are author-owned.

```text
# anchor: F.4.1
type: task        →  ## Goal, ## Plan, ## Todo, ## Links
type: prompt      →  ## Framework, ## R — Role, ## I — Input, ## S — Steps,
                     ## E — Expectations, ## Constraints
type: research    →  (output/SPEC.md only) §1 declaration block + at least
                     ## 1, ## 2, ... up to and including the highest §
                     referenced by the executing prompt; no count cap
type: skill       →  none required (Anthropic SKILL.md format owns the body)
type: spec        →  ## §1, plus any further sections the spec authors choose
type: index       →  none required
```

### §4.2 Pass / Fail Semantics

```text
# anchor: F.4.2
fm-validate MUST FAIL when any required heading from §4.1 is missing
(matched case-insensitively after stripping em-dashes and surrounding
whitespace; e.g., `## Goal:` matches `## Goal`).

fm-validate MUST PASS when:
  - the file contains additional `## ` headings beyond the required set;
  - the order of headings differs from the order in §4.1;
  - the file contains `### ` or deeper subsections in any structure.
```

### §4.3 Heading Ontology Source

```text
# anchor: F.4.3
The required-heading sets in §4.1 are encoded in
`maintenance/schemas/header-ontology.json`. Implementation authors
(Task 016) MUST sync the ontology with this section; if §4.1 and the
JSON drift, the JSON wins for tooling and §4.1 is amended in the next
coherence run. The JSON SHALL be the canonical machine-readable source;
this prose is the human-readable source.
```

## §5. The Toolchain (Stateless CLI Surface)

Four tools, each a single-file Python 3.11 stdlib script, located under `tools/fm/`.

### §5.1 `fm-validate`

```text
# anchor: F.5.1
fm-validate [PATH ...] [--scope=tasks,prompts,research,skills,maintenance,tools,templates]
            [--strict] [--format=text|json]

Behaviour: walk PATH (or the default scope), classify each file by type+location,
apply §3 + §4 checks, emit diagnostics. Exit 0 only when zero ERROR-level
diagnostics. WARN-level diagnostics never affect the exit code unless --strict.

Diagnostic shape (one per problem):
  <path>:<line?>:<severity>:<code>:<message>
Examples:
  prompts/foo/prompt.md::ERROR:F.3.1:missing L1 keys ['summary']
  tasks/021-bar/task.md::ERROR:F.4.2:missing required heading '## Plan'
  skills/baz/SKILL.md::WARN:F.3.4:unknown key 'tpye' — did you mean 'type'?
```

### §5.2 `fm-extract`

```text
# anchor: F.5.2
fm-extract <path> --section <heading-name>
fm-extract <path> --frontmatter
fm-extract <path> --frontmatter <key>
fm-extract <path> --whole-file

Behaviour:
  --section : print the body of the named `## heading` (case-insensitive,
              em-dash-tolerant). Stops at the next `## ` heading. Heading
              MUST resolve; missing heading exits 3.
  --frontmatter : print the YAML frontmatter block with --- fences.
  --frontmatter <key> : print the scalar or list value of <key>; missing
              key exits 3.
  --whole-file : print the entire file (used by package_skill-style flows).

Token budget: --section response MUST be ≤ 4 KB; --frontmatter MUST be ≤ 2 KB.
If the body of a single section exceeds the cap, the tool emits the first
4 KB plus a `… [truncated; original N bytes]` marker.
```

### §5.3 `fm-edit`

```text
# anchor: F.5.3
fm-edit <path> --set <key>=<value>
fm-edit <path> --unset <key>
fm-edit <path> --append-list <key> <value>
fm-edit <path> --remove-from-list <key> <value>
fm-edit <path> --bump-updated

Behaviour: load frontmatter, apply mutation, write back the file in place.
Operations MUST be idempotent: --append-list never appends a duplicate;
--bump-updated sets `updated:` to today's UTC date and is a no-op if it
already matches. --set on a list-valued key fails with exit 4 (use the
list operations). The tool MUST take an OS-level file lock for the
duration of read-modify-write.

Constraint: fm-edit MUST NOT alter any line outside the frontmatter block.
The body bytes after the closing `---\n` MUST be byte-identical pre/post.
```

### §5.4 `fm-query`

```text
# anchor: F.5.4
fm-query <selector> [--scope=…] [--limit=N] [--format=text|json|paths]

Selectors:
  type=<value>                     : files whose frontmatter has matching type
  status=<value>                   : files whose status matches
  slug=<value>                     : exact slug
  has-key=<key>                    : files with the key present
  missing-key=<key>                : files where required+absent (delta-only)
  refers-to=<slug>                 : files whose any *_<list> includes slug
  referenced-by=<slug>             : reverse: files referenced from slug's lists
  stale-since=<N>d                 : updated older than N days
  type=<v>,status=<v>              : commas are AND
Output default: relative paths, one per line, sorted, ≤ 1 KB.

Statelessness: fm-query MUST scan the filesystem fresh on every invocation.
It MUST NOT read or write `.agent_cache/` or any persisted index. It MAY
use the OS page cache (incidental). Cap default scope to operational roots
(/tasks/, /prompts/, /research/, /skills/, /maintenance/, /tools/, /templates/).
```

### §5.5 Library Reuse

```text
# anchor: F.5.5
All four tools MUST share `tools/fm/_core.py` for: frontmatter parsing,
heading walking, type classification, diagnostic shaping. The existing
`tools/_frontmatter.py` MUST be moved into this package and the old
import path MUST be preserved as a thin re-export for one release window
(deprecation handled by Task 017).
```

## §6. Acceptance Criteria (Gherkin)

Feature: Flexible Frontmatter Toolchain

  Background:
    Given the toolchain is installed at /tools/fm/
    And the operational scope is the default (tasks/prompts/research/skills/maintenance/tools/templates)

```gherkin
  # anchor: F.6.1
  Scenario Outline: Required-only key validation
    Given a markdown file at "<path>" with type "<type>"
    When that file's frontmatter is missing key "<missing>"
    Then fm-validate MUST exit 1
    And the diagnostic MUST cite anchor "F.3.1" or "F.3.2"

    Examples:
      | path                              | type     | missing |
      | tasks/099-x/task.md               | task     | summary |
      | prompts/y/prompt.md               | prompt   | slug    |
      | research/z/output/SPEC.md         | research | type    |
      | skills/abc/SKILL.md               | skill    | name    |

  # anchor: F.6.2
  Scenario: Extras do not fail validation
    Given a task.md whose frontmatter has all required keys
    And whose body contains 17 `## ` headings beyond the required four
    And whose frontmatter contains `tags: [foo, bar]` and `aliases: [old-slug]`
    When fm-validate runs
    Then fm-validate MUST exit 0
    And no diagnostic MUST cite anchor "F.4.2"

  # anchor: F.6.3
  Scenario: Required heading missing
    Given a task.md whose body has `## Goal`, `## Plan`, `## Links` but no `## Todo`
    When fm-validate runs
    Then fm-validate MUST exit 1
    And the diagnostic MUST cite anchor "F.4.2"

  # anchor: F.6.4
  Scenario: Section extraction respects token cap
    Given a SKILL.md whose `## Reference files` section is 6 KB long
    When fm-extract <path> --section "Reference files" runs
    Then the output MUST be ≤ 4 KB
    And the output MUST end with a "[truncated; original N bytes]" marker

  # anchor: F.6.5
  Scenario: Idempotent list append
    Given a task.md whose `task_uses_prompts:` list contains ["foo"]
    When fm-edit --append-list task_uses_prompts foo runs three times
    Then `task_uses_prompts:` MUST still equal ["foo"]
    And the body bytes MUST be byte-identical to the pre-edit file

  # anchor: F.6.6
  Scenario: Stateless query under live mutation
    Given fm-query has just listed files where missing-key=task_spawns_prompts
    And a coherence run then writes that key into one of the listed files
    When fm-query is invoked again with the same selector
    Then the just-fixed file MUST NOT appear
    And no `.agent_cache/` artefact MUST have been created or consulted

  # anchor: F.6.7
  Scenario: Did-you-mean typo catch
    Given a prompt.md whose frontmatter contains `tpye: prompt`
    When fm-validate runs
    Then fm-validate MUST exit 1
    And the diagnostic MUST cite anchor "F.3.4"
    And the diagnostic message MUST include the substring "did you mean 'type'"
```

## §7. Integration With Existing Surfaces

### §7.1 Pre-Commit Hook

```text
# anchor: F.7.1
.githooks/pre-commit MUST invoke `tools/check-governance.sh` which MUST
invoke fm-validate over the changed-files set. fm-validate MUST be
delta-aware: it walks only the union of (a) every file in the staged
diff and (b) every file referenced in those files' lists. Whole-tree
scans are reserved for `tools/check-governance.sh --full` (e.g.,
nightly maintenance).
```

### §7.2 Repair Tier Ladder

```text
# anchor: F.7.2
fm-edit MUST NEVER apply a T3 or T4 change. The tool surface is intentionally
limited to T1 (mechanical) and T2 (additive) operations:
  - --bump-updated, --set status, --set summary  → T1
  - --set type=…, --append-list <list>, --set slug → T2 (only on creation)
  - any change that requires renaming an existing slug, rewriting a heading,
    or touching root governance is T3 and MUST be filed as a Task instead.
```

### §7.3 Maintenance Bypass Mode

```text
# anchor: F.7.3
The maintenance-bypass clause in MAINTENANCE.md §4.1 is preserved verbatim:
the pre-commit hook MAY allow a commit that fails fm-validate IFF every
failing file has a corresponding open Task whose `task_affects_paths`
covers the file. The check is performed by `tools/check-maintenance-bypass.py`
which MUST be re-pointed at fm-validate in Task 017.
```

### §7.4 Coherence Check

```text
# anchor: F.7.4
The Coherence Check prompt at /prompts/repo-coherence-check/prompt.md
MUST adopt fm-query as its T1/T2 worklist generator (per Task 014 finding F3:
"Linter-First Triage"). The prompt's Step 2.5 SHOULD invoke:
  fm-query missing-key=task_spawns_prompts --scope=tasks --limit=200
  fm-query stale-since=30d --scope=research --format=paths
…and reserve manual file-by-file inspection for the patterns fm-query cannot detect.
```

## §8. Migration Ladder (Hand-Off to Task 017)

```text
# anchor: F.8.1
Migration is additive-only. Existing files MUST continue to validate after
migration. The migration MUST be split into three batches:

Batch 1 (T1, mechanical, automatable):
  - fm-edit --bump-updated on every operational file the migration touches;
  - introduce tools/fm/ alongside the legacy linters; both run in CI.

Batch 2 (T2, additive, automatable with review):
  - retire tools/validate-frontmatter.py and tools/lint-structure.py by
    re-pointing tools/check-governance.sh at fm-validate;
  - move tools/_frontmatter.py into tools/fm/_core.py with re-export shim.

Batch 3 (T3, structural, requires Task review):
  - drop the persisted index proposed in Task 010 (or scope-narrow Task 010
    to a stateless query CLI on top of fm-query);
  - update maintenance/run-log.md format, MAINTENANCE.md §3.2, and the
    repo-coherence-check prompt's Step 2.5 to reference fm-* commands.
```

```text
# anchor: F.8.2
The migration is `done` when:
  - tools/check-governance.sh exits 0 on the staged tree using fm-* tools only;
  - the four legacy linters under tools/legacy/ are removed in a final cleanup commit;
  - every existing operational file passes fm-validate without --strict;
  - the friction-log entries from the migration session are merged into
    tasks/014-improve-maintenance-spec-from-session/notes.md.
```

## §9. Anti-Patterns

```text
# anchor: F.9.1
The implementations and successor specs MUST NOT:

- introduce any check that *counts* rather than *enumerates* (no "fails when
  more than N headings/keys/lines" rules);
- introduce a persisted authoritative index (caches with TTL ≤ session-length
  and `--no-cache` opt-out are acceptable; persisted indexes that gate commits
  are not);
- treat WARN-severity diagnostics as required (every required check MUST be
  ERROR-severity and MUST have a reproducible failure path);
- use fm-edit to apply T3/T4 changes, even if the YAML edit would be trivial;
- store L3 metadata (embeddings, vectors, scores) inside YAML frontmatter
  (this is restated from `language-spec.md §4.5` and remains in force);
- depend on git availability inside skill containers (see
  research/skills-skill-container-capabilities/output/SPEC.md §3.1);
- re-author prompts inside /research/ (RESEARCH.md §7 invariant preserved);
- couple `fm-extract --section` output to a specific font, locale, or terminal
  width — the output MUST be plain UTF-8 markdown.
```

## §10. Open Questions

```text
# anchor: F.10.1
Q1. How does fm-query interact with submodules or sparse checkouts?
    Resolved by Task 016 (see tasks/016-flexible-frontmatter-toolchain/notes.md).
    Summary: walks the materialised filesystem only, never consults git.

Q2. Should fm-edit grow a --batch mode reading mutations from stdin/JSON?
    Resolved by Task 016: not in v1. Concurrency safety is anchored on the
    per-invocation OS file lock; batch semantics would either hold the lock
    too long or abandon cross-mutation atomicity. Revisitable when a concrete
    caller demonstrates a workload where shell-loop overhead dominates.

Q3. How does the toolchain expose a programmatic API for non-Python callers
    (e.g., gemini-cli scripts)? (Task 017 todo; candidate: a thin JSON-RPC
    over stdio wrapper, deferred to a follow-up.)

Q4. Should `Levenshtein-distance 1` in §3.4 be amended to read
    `Optimal String Alignment distance 1` (transposition-aware)? The §6.1
    example (`tpye` → `type`) is OSA 1, not standard Levenshtein 1.
    Task 016 implementation uses OSA; this clause should be amended for
    consistency. (Task 018 follow-up.)

Q5. Should the §6.1 row for `type=skill` require `name` (per the example) or
    `skill_kind, skill_target_agents` (per §3.2)? The Anthropic SKILL.md
    format only carries `name` + `description`. Task 016 encoded
    `name`/`description` as REQUIRED for `type=skill` and the skill_* keys
    as RECOMMENDED. (Task 018 follow-up.)
```

## §12. Body Data Schema (Per Section)

This section is **additive on top of §4**: §4 enumerates the *required*
`## ` headings per type; §12 specifies what the body of each required
section MUST look like. Every clause here is opt-in for v1
(`fm-validate --check-body`), gated for default-on by Task 019 once the
existing corpus is migrated.

### §12.1 Closed Shape Vocabulary

```text
# anchor: F.12.1
Each typed body section MUST declare exactly one shape from the closed set:

  - paragraph      : prose, no top-level list markers
  - ordered_list   : top-level lines start with `1.` / `2.` / …
  - unordered_list : top-level lines start with `- ` or `* `
                     (NOT `- [ ]` / `- [x]` — that is task_list)
  - task_list      : top-level lines start with `- [ ]` or `- [x]`
  - link_list      : an unordered_list whose items each contain at
                     least one Markdown link `[text](url)`
  - gherkin_block  : at least one fenced ```gherkin code block
  - code_block     : at least one fenced code block (any language)
  - definition_list: lines of the form `**Term**: definition`
                     (reserved for future glossary use)
  - mixed          : any combination — the catch-all default

Shape detection MUST ignore content inside fenced code blocks (mirrors
the rule already established for `## ` heading detection in §4).
```

### §12.2 Per-Type Body Schema

```text
# anchor: F.12.2
type: task — body_schema (§4.1: Goal, Plan, Todo, Links)

  Goal :  shape=paragraph,    min_chars=20, max_paragraphs=3
  Plan :  shape=ordered_list, min_items=1
  Todo :  shape=task_list,    min_items=1, completion_field=task_status
  Links:  shape=link_list,    min_items=1, link_pattern="^(\\.\\.?\\/|/)"

type: prompt — body_schema (§4.1: Framework, R — Role, I — Input,
                            S — Steps, E — Expectations, Constraints)

  Framework      : shape=paragraph, max_paragraphs=2
  R — Role       : shape=paragraph, min_chars=20
  I — Input      : shape=unordered_list, min_items=1
  S — Steps      : shape=ordered_list,   min_items=3
  E — Expectations: shape=unordered_list, min_items=1
  Constraints    : shape=unordered_list, min_items=1,
                   item_pattern="\\b(MUST|MUST NOT|SHOULD|SHOULD NOT|MAY|REQUIRED|SHALL)\\b",
                   item_pattern_severity=WARN

type: research — body_schema (output/SPEC.md)

  §1: shape=paragraph,     must_contain="RFC 2119"
  §6: shape=gherkin_block, min_blocks=1

type: skill   — body owned by Anthropic SKILL.md format; no body_schema.
type: spec    — body_schema empty (§ structure is author-owned).
type: index   — body_schema empty.
type: readme  — body_schema empty.
type: note    — body_schema empty.
```

### §12.3 Field Reference

```text
# anchor: F.12.3
Per-section schema fields (all OPTIONAL except `shape`):

  shape                  : required; one value from §12.1
  min_items, max_items   : list-shape count constraints
  min_chars              : minimum body length after stripping whitespace
  max_paragraphs         : guard against accidental shape drift in `paragraph`
  item_pattern           : regex each list item MUST match
  item_pattern_severity  : "ERROR" (default) | "WARN" — overrides emit level
  link_pattern           : regex against URL portion of each link in link_list
  must_contain           : case-insensitive substring assertion against the
                           whole section body
  min_blocks             : minimum count of fenced code blocks
  completion_field       : task_list-only; names the FM field whose value MUST
                           equal "done" when every checkbox is `[x]`. Auto-
                           derivation is INFORMATIONAL only — the validator
                           emits a WARN if the file's task_status disagrees
                           with checkbox completion, never an ERROR.
  doc                    : free-form note surfaced by `fm-validate --explain`
```

### §12.4 Diagnostic Codes

```text
# anchor: F.12.4
fm-validate --check-body emits diagnostics with codes in the F.B.* family:

  F.B.1 : shape mismatch (expected X, found Y)
  F.B.2 : item-count below min_items / above max_items
  F.B.3 : item_pattern miss (one diagnostic per failing item)
  F.B.4 : min_chars / max_paragraphs miss
  F.B.5 : must_contain assertion failed
  F.B.6 : link_pattern miss in link_list
  F.B.7 : task_list completion disagrees with completion_field (WARN only)

Diagnostic shape mirrors §5.1:
  <path>:<line?>:<severity>:<code>:<message>
Examples:
  tasks/099-x/task.md::ERROR:F.B.1:section '## Plan' shape mismatch: expected ordered_list, found paragraph
  prompts/y/prompt.md::WARN:F.B.3:section '## Constraints' item 3 missing RFC 2119 keyword
  tasks/099-x/task.md::WARN:F.B.7:Todo all checked but task_status='active' (expected 'done')
```

### §12.5 Pass / Fail Semantics

```text
# anchor: F.12.5
fm-validate --check-body MUST FAIL when, for any required section in §12.2:
  - the section's body shape does not match the declared shape;
  - any item-count, link_pattern, item_pattern (severity=ERROR), min_chars,
    max_paragraphs, must_contain, or min_blocks constraint is violated.

fm-validate --check-body MUST PASS when:
  - the section is absent (already a §4 ERROR — F.4.2 wins over F.B.*;
    do not double-count);
  - extra non-required sections appear with any shape;
  - WARN-level diagnostics fire and `--strict` is unset.

Default state: --check-body is OFF. Phasing per §12.6.
```

### §12.6 Phasing

```text
# anchor: F.12.6
Phase 1 (Task 018): ship --check-body as opt-in. WARN-only by default,
  ERROR-promotion via --strict. Existing files surface their drift but
  do not block CI.

Phase 2 (Task 019): migrate the corpus — every existing operational file
  passes --check-body. Add a separate Task per type if the diff is large.

Phase 3 (Task 020): flip --check-body ON by default in
  tools/check-governance.sh, behind FM_TOOLCHAIN=1. Legacy validator
  retired in the same Task.
```

## §13. Section Operations (fm-section, deferred)

`fm-edit` only mutates frontmatter (§5.3 invariant). The body equivalent
is a separate tool, `fm-section`, scoped to Task 018. The interface is
specified here so callers and reviewers have a stable contract to reason
about while implementation is queued.

### §13.1 Tool Surface

```text
# anchor: F.13.1
fm-section <path> --replace <name> --from-stdin
fm-section <path> --append-to <name> --text <str>
fm-section <path> --append-list-item <name> <item>
fm-section <path> --check-task <name> <item-substring>
fm-section <path> --insert-after <name> --new-heading <h> --from-stdin
fm-section <path> --insert-before <name> --new-heading <h> --from-stdin
fm-section <path> --delete <name>
fm-section <path> --rename <old> <new>

Section addressing accepts:
  --section <name>            : first match (back-compat with fm-extract)
  --section <name> --nth N    : 1-indexed match
  --anchor <id>               : match by `# anchor: <id>` comment
                                (binding for spec files per §1)
```

### §13.2 Invariants

```text
# anchor: F.13.2
fm-section MUST preserve, byte-for-byte:
  - the YAML frontmatter block (open fence through closing fence);
  - every byte outside the address[ed] section's heading-line-through-
    next-`## `-or-EOF span.

fm-section MUST take an OS file lock for the whole read-modify-write,
identical to fm-edit (§5.3).

fm-section MUST NOT execute T3/T4 changes (mirrors §7.2). --rename is
T2 only when no other file references the old heading; otherwise it
MUST refuse and instruct the caller to file a Task.

fm-section's mutations MUST satisfy the §12 body_schema for the file's
type. A mutation that would leave the section in violation MUST be
rejected with exit 4 (type error), regardless of --check-body state.
```

### §13.3 Section Addressing Under Duplicates

```text
# anchor: F.13.3
fm-extract and fm-section MUST support the following disambiguation
when more than one `## ` heading shares a normalised name:

  default                  : first match (back-compat)
  --nth N                  : 1-indexed
  --all                    : every match (fm-extract only); separator is a
                             single `\\f` form-feed byte between bodies
  --anchor <id>            : match by `# anchor: <id>` comment on the line
                             above the heading

Unaddressable duplicates (no anchor, no --nth) on a write operation
MUST exit 5 (ambiguous address).
```

## §14. Reading Extensions

```text
# anchor: F.14.1
fm-extract grows three additional modes (additive, no behavioural
change to existing flags):

  --body                   : print everything after the closing `---\\n`
                             (no truncation, no FM, no headings stripped)
  --toc                    : print one normalised `## ` heading per line,
                             optional anchor in trailing parens
  --sections <a,b,c>       : batch read; output is the concatenation of
                             each named section's body, separated by a
                             single `\\f` form-feed

Token caps (per §5.2) extend:
  --toc                    : ≤ 1 KB
  --sections               : the section cap (4 KB) is per-section; total
                             output is uncapped (caller controls the count)
```

## §15. Sources

In-house, cited by repo path:

- `maintenance/language-spec.md` (frontmatter ontology, RFC 2119, Gherkin)
- `MAINTENANCE.md` (T1/T2/T3/T4 ladder, coherence check, bypass mode)
- `PRE_COMMIT.md` (eight-checklist baseline)
- `RESEARCH.md` (research workspace structure)
- `research/obsidian-frontmatter-agentic-spec/output/SPEC.md` (L0/L1/L2/L3 ontology)
- `research/repo-maintenance-protocol-spec/output/SPEC.md` (run-log + coherence design)
- `research/skills-skill-architecture/output/SPEC.md` (three-tier disclosure)
- `research/skills-skill-container-capabilities/output/SPEC.md` (no-git constraint)
- `research/skills-namespace-ontology/output/SPEC.md` (skill_* closed vocabulary)
- `research/skills-navigation-bootstrap/output/SPEC.md` (manifest-driven nav, superseded)
- `research/token-efficiency-tool-suite/output/SPEC.md` (four-stage pipeline)
- `tools/dramatica-nav/{extract,validate,nav}.py` (direct prior art)
- `tools/validate-frontmatter.py`, `tools/_frontmatter.py` (current linter)

External (mirrored locally):

- `skills/skill-creator/SKILL.md` and `references/schemas.md` — verbatim mirror of
  [anthropics/skills · skills/skill-creator](https://github.com/anthropics/skills/tree/main/skills/skill-creator).
