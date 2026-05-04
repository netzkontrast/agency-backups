# Notes — Task NNN-<slug>

Running notes captured during execution. Append dated entries; do not edit prior entries.

---

## Session — YYYY-MM-DD

_What was done in this session, what was discovered, what was left in-flight._

---

## Blocker Entry — YYYY-MM-DD (required if task_status: blocked)

**Blocker description:** REPLACE — one paragraph explaining what is blocking progress.

**Last reproducible state:** REPLACE — steps another agent can take to verify the state as of this date.

**Unblocked by:** REPLACE (fill in when resuming).

---

## Resumption Checklist — YYYY-MM-DD (required on re-entry per Spec-I.3.1)

Per Spec-I.3.1 (Cross-Session Continuity), an agent resuming a blocked task MUST verify:

- [ ] World-model staleness check: re-read affected files and confirm they match assumed state.
- [ ] Environment consistency: verify no other agent or human modified `task_affects_paths` since the blocker was logged.
- [ ] Frontmatter updated: `task_status` changed back to `in_progress`, `updated` set to today.
- [ ] Prior assumptions documented below.

**Assumed prior state:**

REPLACE — list every file path and the state the resuming agent is assuming it to be in.
