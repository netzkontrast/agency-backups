# M01 — Falsification

Each surviving primitive was attacked. The attack and response are recorded below.

## P1 — Required-only validation

**Attack.** "An author adds a required key with a typo (`tpye:` instead of `type:`); the validator's set-difference flags `type` as missing — but is `tpye` an extra key (pass) or a malformed-author signal (fail)?"

**Response.** SPEC §3.4 requires the validator to fail on *unknown* keys whose names are within Levenshtein-distance 1 of any required key, with a "did you mean" diagnostic. This preserves the "extras pass" rule (intentional extras like `tags:`, `aliases:` are not near-misses) while catching typo-introduced regressions. Survives.

## P2 — Stateless filesystem scan

**Attack.** "On a 50,000-file vault the scan is no longer < 200 ms; the agent's budget is busted."

**Response.** SPEC §5.4 caps the operational scope at `/tasks/`, `/prompts/`, `/research/`, `/skills/`, `/maintenance/`, `/tools/`, and `/templates/`. Scope-out anything else with a `--scope` flag default-set to those roots. Even at 50 K files the per-file frontmatter parse is bounded; the OS page cache makes the second run free. Survives with a documented assumption: if the operational corpus exceeds 5 K files, revisit (re-add an opt-in cache, NOT a stored authoritative index).

## P3 — Required-headings only

**Attack.** "An L2 H3 heading inside a required L2 H2 section gets renamed; the validator misses it."

**Response.** SPEC §4 only walks `## ` (level-2) headings by default and treats deeper levels as content the author owns. The required-headings list is intentionally short (≤ 5 per `type:`). Required deeper headings live in *content* prose and are author-owned, not validator-enforced. This is the explicit cost of "flexibility" — and the user agreed to it.

## P4 — `fm-edit` idempotency

**Attack.** "Two parallel `fm-edit --append-list task_uses_prompts foo` runs race; the file ends up with `foo, foo`."

**Response.** SPEC §5.3 requires `fm-edit` to take an OS file lock for the duration of the read-modify-write. It also requires deduplication on `--append-list` operations regardless of the lock. Survives.

## P5 — Skill-creator loop adaptation

**Attack.** "Skill-creator's loop assumes subagents and a browser; this repo's pre-commit hook has neither."

**Response.** SPEC §7 binds the loop to existing repository surfaces: `friction-log.md` is the feedback channel; `maintenance/run-log.md` is the run record; `tools/check-governance.sh` is the validator. No subagents required. Survives.
