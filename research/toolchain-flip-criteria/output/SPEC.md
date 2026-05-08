---
type: spec
status: active
slug: toolchain-flip-criteria
summary: "Mechanical flip criteria, single-commit flip procedure, post-flip cleanup checklist, and rollback procedure for retiring the Legacy column of the three-way Legacy / Flexible / ADR toolchain matrix governing tools/check-governance.sh."
created: 2026-05-08
updated: 2026-05-08
---

# Toolchain Flip Criteria

## §0. RFC 2119

The keywords **MUST**, **MUST NOT**, **REQUIRED**, **SHALL**, **SHALL NOT**, **SHOULD**, **SHOULD NOT**, **RECOMMENDED**, **MAY**, and **OPTIONAL** are interpreted per BCP 14 (RFC 2119 + RFC 8174) when, and only when, they appear in all capitals.

## §0.1. Scope

This SPEC defines the deterministic, mechanically-verifiable conditions under which the **Legacy** column of the three-way [`PRE_COMMIT.md §7.A`](../../../PRE_COMMIT.md) Legacy / Flexible / ADR toolchain matrix is retired. The **Flexible** column (`tools/fm/validate.py --type-check`, `tools/lint-structure.py`, `tools/lint-runlog.py`, `tools/fm/index_diff.py`, plus the §7.A WARN-tier opt-blocks) is canonical and gating before, during, and after the flip. The **ADR** column (`tools/adr/cli.py validate`) runs unconditionally as step `[5/6]` of [`tools/check-governance.sh`](../../../tools/check-governance.sh) before the flip and as step `[5/5]` after; the flip MUST NOT alter ADR semantics.

The "flip" is the single atomic commit that:

1. Removes the dual-gate `if [ "$FM_TOOLCHAIN" = "1" ]; then … else …` branch in `tools/check-governance.sh` step `[1/6]`.
2. Deletes [`tools/legacy/`](../../../tools/legacy/) (`validate-frontmatter.py`, `lint-structure.py`, `lint-linkage.py`).
3. Strips the `FM_TOOLCHAIN` environment variable and the legacy advisory block from the hook.
4. Updates the prose in [`MAINTENANCE.md`](../../../MAINTENANCE.md) §1.1 and [`PRE_COMMIT.md`](../../../PRE_COMMIT.md) §7 / §7.A to declare the Legacy column retired.

After the flip, the matrix is two-way (Flexible canonical + ADR unconditional). All criteria below are git/grep-extractable (waiver count, `task_status`, lint exit codes), per the prompt's Falsification clause.

## §1. Flip-Criteria Checklist (≤7 mechanically-verifiable items)

The maintenance agent MUST satisfy every criterion below. Each criterion is a single command whose exit code or numeric output is the gating predicate; an LLM judgment call is NOT permitted at any step.

```text
# anchor: TFC.1.1 — gating-step coverage
F-1. Every numbered step in tools/check-governance.sh ([1/6] … [6/6])
     MUST exit 0 against HEAD with FM_TOOLCHAIN=1.
     Verifier: `tools/check-governance.sh; echo $?` MUST print `0`.
```

```text
# anchor: TFC.1.2 — legacy is no-op under the gate
F-2. tools/check-governance.sh step [1/6] MUST exit 0 against HEAD when
     FM_TOOLCHAIN=0 is forced (dual-gate symmetry probe; the legacy
     validator MUST agree with fm-validate on the corpus).
     Verifier: `FM_TOOLCHAIN=0 tools/check-governance.sh; echo $?`
     MUST print `0`. Failure means the legacy column would gate a
     working tree the canonical column accepts; the flip MUST be
     blocked until the divergence is resolved by a Task.
```

```text
# anchor: TFC.1.3 — waivers carry no legacy diagnostic codes
F-3. tools/.frontmatter-waivers MUST contain zero TSV rows whose
     `rule-id` column is a diagnostic code emitted only by
     tools/legacy/* (i.e. anything that is not an `F.*`, `R.*`,
     `ADR.A.*`, `TRUST.*`, or `*` wildcard understood by
     `tools/fm/_core.load_waivers`).
     Verifier: `awk -F'\t' 'NR>0 && !/^#/ && NF>=2' \
       tools/.frontmatter-waivers | \
       awk -F'\t' '{print $2}' | \
       grep -Ev '^(F\.|R\.|ADR\.A\.|TRUST\.|\*$)' | wc -l`
     MUST print `0`. Header-only file (NF<2) trivially satisfies this.
```

```text
# anchor: TFC.1.4 — Tasks 016 / 017 / 019 are closed
F-4. Each of Task 016, Task 017, Task 019 MUST carry frontmatter
     `task_status: done` and MUST appear in `tasks/readme.md`'s
     done section.
     Verifier:
       `for n in 016 017 019; do
          grep -q '^task_status: done$' tasks/$n-*/task.md || exit 1;
        done`
     MUST exit 0.
```

```text
# anchor: TFC.1.5 — no live consumer of tools/legacy/ outside the gate
F-5. The only file in the working tree that imports or invokes
     `tools/legacy/*.py` MUST be `tools/check-governance.sh` itself
     (the advisory branch slated for removal in §2).
     Verifier:
       `grep -RIl 'tools/legacy/' \
          --exclude-dir=.git \
          --exclude=tools/check-governance.sh \
          . | wc -l`
     MUST print `0`. Documentation-only mentions in MAINTENANCE.md /
     PRE_COMMIT.md are addressed in §2; once the prose is updated,
     this verifier remains green by construction.
```

```text
# anchor: TFC.1.6 — pytest under tools/tests/ green on canonical-only
F-6. The pytest suite under `tools/tests/` MUST exit 0 with
     `FM_TOOLCHAIN=1` (the default) and MUST NOT fail any test that
     mocks the legacy code path.
     Verifier: `python3 -m pytest tools/tests/ -q; echo $?`
     MUST print `0`.
```

```text
# anchor: TFC.1.7 — trust-audit AGGREGATOR or threshold tightening
F-7. Either (a) Task 039 ST-5 (AGGREGATOR) MUST have landed
     (frontmatter `task_status: done` on tasks/039-*/task.md and
     `tools/maintenance/trust-audit.py` existing) AND
     `tools/check-trust-audit.py:DIAGNOSTIC_SCHEMA["thresholds"]
     ["behavioral"]` MUST equal `0.90`; OR (b) the flip commit MUST
     include the threshold raise to `0.90` and a one-paragraph
     friction-log note explaining why the raise rides the flip.
     Verifier:
       `python3 -c "from tools.check_trust_audit import \
        DIAGNOSTIC_SCHEMA as S; \
        import sys; \
        sys.exit(0 if S['thresholds']['behavioral']>=0.90 else 1)"`
     MUST exit 0 against the post-flip working tree.
```

The checklist is **closed at seven items**. Adding an eighth criterion is a T3 action that MUST go through a successor SPEC (this one is `status: active`; supersession via the `task_supersedes` / `task_superseded_by` linkage in a follow-up Task).

## §2. Flip Procedure (single atomic commit)

The maintenance agent MUST execute the flip as a single git commit whose tree-diff matches the file-change enumeration below. No additional changes MAY ride the flip commit. The agent MUST verify §1 F-1 through F-7 against HEAD *before* staging, and re-verify F-1 against the staged tree *before* the commit.

### §2.1 File-change enumeration

```text
# anchor: TFC.2.1
File changes that compose the flip commit (deletions, edits, no
additions):

D  tools/legacy/validate-frontmatter.py
D  tools/legacy/lint-structure.py
D  tools/legacy/lint-linkage.py
D  tools/legacy/                                (empty directory removed)
M  tools/check-governance.sh                    (legacy block + FM_TOOLCHAIN
                                                 dispatcher removed; step
                                                 numbering re-flowed [N/5])
M  MAINTENANCE.md                               (§1.1 table loses the
                                                 Legacy row; FM_TOOLCHAIN
                                                 escape-hatch paragraph
                                                 deleted; §1.1.2 three-way
                                                 table re-shaped to two-way
                                                 Flexible+ADR with a
                                                 "retired YYYY-MM-DD"
                                                 footnote pointing at this
                                                 SPEC)
M  PRE_COMMIT.md                                (§7 code block drops the
                                                 `FM_TOOLCHAIN=0` example
                                                 and the legacy `python3
                                                 tools/legacy/*.py`
                                                 invocations; §7.A matrix
                                                 drops the Legacy column;
                                                 §7.B Rule 6
                                                 "Re-expression at
                                                 toolchain flip" updates
                                                 to past tense and points
                                                 at this SPEC)
M  tools/check-trust-audit.py                   (DIAGNOSTIC_SCHEMA
                                                 ["thresholds"]
                                                 ["behavioral"] = 0.90 if
                                                 §1 F-7 path (b) applies;
                                                 unchanged if path (a))
A  research/toolchain-flip-criteria/output/
   SPEC.md                                      (this file — must already
                                                 be on disk before flip;
                                                 added by Task 039 ST-1
                                                 which is THIS run)
```

### §2.2 Commit-message shape

The commit message MUST follow the shape:

```text
chore(toolchain): retire Legacy column; canonical=Flexible (Task NNN)

Per research/toolchain-flip-criteria/output/SPEC.md §2. Closes
the dual-gate window opened by Tasks 016/017/019. ADR column
unaffected.

https://claude.ai/code/session_<id>
```

`Task NNN` is the parent Task that runs the flip — almost certainly a successor of Task 039 (ST-1 produces this SPEC; the actual flip is a separate Task with `task_supersedes` set on the predecessor Task 017 lineage).

### §2.3 Pre-commit verification

The agent MUST run `tools/check-governance.sh` against the staged tree before invoking `git commit`. Exit 0 is mandatory. If non-zero, the agent MUST NOT use `--no-verify` and MUST NOT split the commit; the flip is atomic by design.

### §2.4 Post-commit verification

Immediately after the commit lands, the agent MUST verify:

- `tools/check-governance.sh; echo $?` prints `0`.
- `git log -1 --name-status` matches the §2.1 enumeration exactly.
- `grep -RIl 'tools/legacy/' --exclude-dir=.git . | wc -l` prints `0`.
- `grep -RIl 'FM_TOOLCHAIN' --exclude-dir=.git . | wc -l` prints `0`.

A non-zero result on any verifier triggers §4 rollback.

## §3. Post-Flip Cleanup Checklist

The cleanup actions below MUST be filed as separate Tasks; they MUST NOT be bundled into the §2 flip commit (rollback safety — keeping the flip minimal lets `git revert <flip-sha>` restore the dual-gate exactly).

### §3.1 Linters to retire (deleted in §2; this section confirms no follow-on debt)

- [`tools/legacy/validate-frontmatter.py`](../../../tools/legacy/validate-frontmatter.py) — superseded by `tools/fm/validate.py`. **Action:** none post-flip; the file is deleted in §2.
- [`tools/legacy/lint-structure.py`](../../../tools/legacy/lint-structure.py) — note this is **not** the same file as `tools/lint-structure.py`. The `tools/legacy/` shim is deleted in §2; the canonical `tools/lint-structure.py` remains as the directory-structure linter step `[2/6]`.
- [`tools/legacy/lint-linkage.py`](../../../tools/legacy/lint-linkage.py) — folded into `tools/fm/validate.py --type-check`; deleted in §2.

### §3.2 WARN-tier promotions to ERROR-tier (sequenced after the flip)

Each row below names an `[opt]` block in `tools/check-governance.sh` that is currently advisory (WARN-tier; controlled by an `FM_*_STRICT` env var that defaults to `0`). Each promotion is a separate Task whose Plan flips the env-var default to `1` and removes the toggle once the corpus is clean.

| `[opt]` block | Env var (current default) | Promotion Task ownership |
|---|---|---|
| RFC 2119 polarity audit | `--strict` flag (default off) | Task 032 ST-3 lineage |
| Audit-graph consistency linter | `FM_AUDIT_GRAPH_STRICT=0` | Task 036 ST-2 follow-up |
| Assumption-log substance linter | (no toggle; runs `\|\| true`) | New Task — wire `FM_ASSUMPTION_LOG_STRICT=1` |
| Prompt self-containedness linter | (no toggle; runs `\|\| true`) | Task 034 ST-2 follow-up |
| Prompt framework-declaration linter | (no toggle; runs `\|\| true`) | Task 034 ST-3 follow-up |
| Duplicate `task_id` linter | `FM_DUPLICATE_TASK_ID_STRICT=0` | Task 043 (renumber) → then promote |
| Workspace cleanliness linter | `FM_WORKSPACE_CLEANLINESS_STRICT=0` | Task 035 ST-2 follow-up |
| External-result downstream-Task linter | `FM_EXTERNAL_RESULT_STRICT=0` | Task 035 ST-3 follow-up |
| Trust-audit GATE | `FM_TRUST_AUDIT_STRICT=0` | Task 035 ST-4 follow-up (paired with §3.3 below) |
| FL declaration linter | `FM_FL_DECLARATION_STRICT=0` | Task 038 ST-2 follow-up |

The promotion ordering MUST be: corpus-clean check → flip the env-var default → keep the toggle for one release window → delete the toggle. Each promotion Task MUST cite this §3.2 row in its `task_supersedes` chain so the audit graph traces the WARN→ERROR transition.

### §3.3 Trust-audit threshold tightening

If §1 F-7 path (b) applied (the flip commit raised `behavioral` to `0.90`), no §3.3 work is required. If path (a) applied (Task 039 ST-5 already raised the threshold), §3.3 is also a no-op. The §3.3 row exists to enumerate the ledger of "things flagged as toolchain-bound debt"; the actual normative bump rides §1 F-7.

### §3.4 Documentation re-numbering

After the legacy advisory step is removed, the `[N/M]` step counts in `tools/check-governance.sh` re-flow from `[*/6]` to `[*/5]`. PRE_COMMIT.md §7.C currently anchors `step [5/6]` for the ADR validator; after the flip the anchor is `step [5/5]`. Every cross-reference MUST be updated:

- [`PRE_COMMIT.md`](../../../PRE_COMMIT.md) §7.A bullet "ADR runs unconditionally as step `[5/6]`" → `[5/5]`.
- [`PRE_COMMIT.md`](../../../PRE_COMMIT.md) §7.C heading text "Composed inside `tools/check-governance.sh` as step `[5/6]`" → `[5/5]`.
- [`PRE_COMMIT.md`](../../../PRE_COMMIT.md) §8 PC.B.2 scenario "every step `[1/6]` through `[6/6]`" → `[1/5]` through `[5/5]`.
- [`tools/check-governance.sh`](../../../tools/check-governance.sh) banner strings.

This is a T1 mechanical action and MAY land in a separate post-flip cleanup commit per §3.

### §3.5 ADR column hygiene check (no flip required)

ADR runs unconditionally; it has no `FM_TOOLCHAIN`-style toggle. Post-flip, the agent MUST verify that:

- `tools/adr/cli.py validate` is still invoked unconditionally inside the (re-numbered) `[5/5]` step.
- The graceful-no-op behaviour for an empty `decisions/` directory is preserved.
- No `ADR.A.*` rule-id appears as `*`-wildcard suppressed in `tools/.frontmatter-waivers`.

These are advisory hygiene checks; no code change is required if the verifications pass.

## §4. Rollback Procedure

The flip is reversible by design — the §2 commit is atomic, and §3 cleanup is sequenced *after* the flip into separate commits. A single revert restores the dual-gate.

### §4.1 Trigger conditions

The agent MUST execute rollback if **any** of the following surface within 24 hours of the flip:

- `tools/check-governance.sh` exits non-zero on `main` (`HEAD == flip-sha`).
- A live consumer of `tools/legacy/` is discovered that was missed by §1 F-5 (e.g., a script in `Agency-System/` or a CI workflow not previously enumerated).
- A research workspace at `research_phase: complete` newly fails `tools/check-trust-audit.py` because the §1 F-7 threshold raise tripped a previously-passing workspace.

### §4.2 Procedure

The mental rehearsal against §2 confirms that a single `git revert` undoes every file change:

```text
# anchor: TFC.4.1
1. Run `git revert <flip-sha>` on `main`.
   This produces an inverse commit that:
     A  tools/legacy/validate-frontmatter.py
     A  tools/legacy/lint-structure.py
     A  tools/legacy/lint-linkage.py
     M  tools/check-governance.sh   (legacy block + FM_TOOLCHAIN restored)
     M  MAINTENANCE.md              (§1.1 dual-gate prose restored)
     M  PRE_COMMIT.md               (§7 / §7.A Legacy column restored)
     M  tools/check-trust-audit.py  (behavioral threshold restored to 0.80
                                     if F-7 path (b) was used)
2. Verify the inverse tree-diff matches the pre-flip working tree.
   `git diff <flip-sha>^ HEAD -- tools/legacy/ \
                                  tools/check-governance.sh \
                                  MAINTENANCE.md PRE_COMMIT.md`
   MUST be empty.
3. Run `tools/check-governance.sh` against the reverted tree.
   `echo $?` MUST print `0`.
4. The file research/toolchain-flip-criteria/output/SPEC.md (this file)
   is NOT reverted — it remains as the historical anchor for the next
   flip attempt. The reverting commit message MUST cite this anchor.
```

### §4.3 Re-flip preconditions

Re-attempting the flip after a rollback MUST satisfy:

- The §4.1 trigger condition is documented in a new friction-log entry under the closing Task's reflection layer.
- A new Task SHOULD be filed (or the original re-opened) that addresses the trigger condition (e.g., the missed consumer of `tools/legacy/` is removed; the failing trust-audit workspace is repaired).
- §1 F-1 through F-7 are re-verified against the post-rollback HEAD.

The agent MUST NOT re-attempt the flip on the same calendar day as the rollback unless the trigger condition was a documentation typo (e.g., a missed `[5/6]` → `[5/5]` re-numbering caught by the polarity audit). Same-day re-attempts on substantive triggers risk losing the rollback's diagnostic signal.

## §5. Falsification

The criteria above are git/grep-extractable predicates only. If any criterion in §1 cannot be evaluated mechanically (i.e., requires LLM judgment to decide pass/fail), this SPEC is falsified and MUST be reissued under a successor slug. The verifiers in §1 F-1 through F-7 are the canonical falsification surface; any reviewer who finds a verifier that cannot be evaluated as a single shell command on a Unix-like system has surfaced a defect that MUST be filed as a Task before the flip is attempted.

## §6. Open Questions

None. Every counter-question raised during synthesis (`synthesis/methodology.md` M13) was resolvable from the on-disk corpus.
