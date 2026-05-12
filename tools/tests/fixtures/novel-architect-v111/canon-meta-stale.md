---
type: note
status: active
slug: example-canon-meta-stale
summary: "Synthetic-violation canon-meta fixture: missing fields + bad enum + reciprocity violation."
created: 2026-05-12
updated: 2026-05-12
canon_meta_version: "1.0"
---

# Stale Canon Meta — exercises CANON.* diagnostics

## Entry missing canon_added_by

> - `canon_id`: canon-missing-001
> - `canon_status`: accepted
> - `canon_added_phase`: phase4
> - `canon_added_at`: 2026-05-11T14:23:00Z

Body. Note: `canon_added_by` is intentionally absent to trigger CANON.MISSING_FIELD.

## Bad status enum

> - `canon_id`: canon-bad-enum-002
> - `canon_status`: unconfirmed
> - `canon_added_phase`: phase4
> - `canon_added_at`: 2026-05-11T14:23:00Z
> - `canon_added_by`: claude-code

`canon_status=unconfirmed` is not in the valid enum — triggers CANON.STATUS_ENUM.

## Bad phase pattern + bad timestamp

> - `canon_id`: canon-bad-shapes-003
> - `canon_status`: accepted
> - `canon_added_phase`: phase42
> - `canon_added_at`: 2026/05/11 14:23
> - `canon_added_by`: claude-code

`canon_added_phase=phase42` (out of range) → CANON.PHASE_PATTERN.
`canon_added_at` is not ISO-8601 with Z → CANON.TIMESTAMP_FORMAT.

## Contested without conflicts_with

> - `canon_id`: canon-contested-no-conflicts-004
> - `canon_status`: contested
> - `canon_added_phase`: phase4
> - `canon_added_at`: 2026-05-11T14:23:00Z
> - `canon_added_by`: claude-code

Contested but `canon_conflicts_with` absent → CANON.CONFLICT_EMPTY.

## Superseded without resolved_by

> - `canon_id`: canon-superseded-no-resolved-005
> - `canon_status`: superseded
> - `canon_added_phase`: phase4
> - `canon_added_at`: 2026-05-11T14:23:00Z
> - `canon_added_by`: claude-code

Superseded but `canon_resolved_by` absent → CANON.SUPERSEDED_NO_RES.

## Reciprocity-A (lists B but B does not list A)

> - `canon_id`: canon-reciprocity-a-006
> - `canon_status`: contested
> - `canon_added_phase`: phase4
> - `canon_added_at`: 2026-05-11T14:23:00Z
> - `canon_added_by`: claude-code
> - `canon_conflicts_with`: [canon-reciprocity-b-007]

A lists B in conflicts but B does not list A → CANON.RECIPROCITY.

## Reciprocity-B (does NOT list A back)

> - `canon_id`: canon-reciprocity-b-007
> - `canon_status`: contested
> - `canon_added_phase`: phase4
> - `canon_added_at`: 2026-05-11T14:23:00Z
> - `canon_added_by`: claude-code
> - `canon_conflicts_with`: []

B says no conflicts; should list A → caught by the reciprocity check on A.
