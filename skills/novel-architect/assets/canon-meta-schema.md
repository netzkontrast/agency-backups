# Canon-Status Schema (Dual-Kernel Pattern Adoption)

> **Implementiert:** Task 076 (v1.1.0)
> **Quelle:** Dual-Kernel `/home/user/Dual-Kernel/` canon-status conflict
> resolution pattern (siehe `Dual-Kernel/skill-audit/canon-status-schema.md` ⟶ adapted)
> **Anwendungsbereich:** `<workspace>/canon-meta.md` Frontmatter + Body

## §0 Wofür ein Canon-Status?

Roman-Projekte haben **nicht-strukturelle Canon-Daten** (DKT-Physik,
Prosa-Regeln, Worldbuilding-Lookups, Style-Konventionen), die nicht in der
NCP-JSON leben dürfen, weil sie keine Dramatica-Strukturen sind. Diese Daten
landen in `canon-meta.md`. Aber: sie verändern sich, sie widersprechen sich
manchmal, und Author-Entscheidungen müssen pro Eintrag nachverfolgbar sein.

Das **Canon-Status Schema** klassifiziert jeden canon-meta-Eintrag nach:

1. **Status:** `proposed` / `accepted` / `contested` / `superseded` / `archived`
2. **Provenance:** wer / wann / aus welcher Phase
3. **Conflict-Resolution:** wenn `contested`, wer ist der Schiedsrichter (User-only-Decision, Phase-7-Audit, oder Drafting-Discovery)

Dual-Kernel hat dieses Schema aus dem Kohärenz-Protokoll-Projekt entwickelt;
v1.1.0 adoptiert es für *alle* Romans (projekt-agnostisch).

## §1 Frontmatter-Felder

`canon-meta.md` MUSS folgende L1-Felder tragen:

```yaml
---
type: note
status: active
slug: <project-slug>-canon-meta
summary: "Non-structural canon for <project>. Lives outside NCP."
created: 2026-05-11
updated: 2026-05-11
canon_meta_version: "1.0"   # bumps when schema changes
---
```

Pro Body-Eintrag (im H2 oder H3-Header markiert) gehören diese Felder
**inline** (nicht im Frontmatter, weil pro Entry):

| Inline-Feld | Beispiel | Pflicht |
|-------------|----------|---------|
| `canon_id` | `canon-dkt-physik-001` | ja |
| `canon_status` | `accepted` | ja |
| `canon_added_phase` | `phase4` | ja |
| `canon_added_at` | `2026-05-11T14:23:00Z` | ja |
| `canon_added_by` | `claude-code` / `<user-id>` | ja |
| `canon_conflicts_with` | `[canon-dkt-physik-002]` | wenn `canon_status == contested` |
| `canon_resolved_by` | `phase7-audit-2026-05-12` | wenn `canon_status == superseded` |

## §2 Eintrag-Schablone

```markdown
## DKT-Physik: Lichtgeschwindigkeits-Constraint

> - `canon_id`: canon-dkt-physik-001
> - `canon_status`: accepted
> - `canon_added_phase`: phase4
> - `canon_added_at`: 2026-05-11T14:23:00Z
> - `canon_added_by`: claude-code

Im DKT-Universum ist die Lichtgeschwindigkeit nicht universal. In Kohärenz-
Zonen (Kapitel 12+) gilt c' = c · (1 - ρ_Kohärenz/ρ_max). Konsequenz:
FTL-Reisen möglich nur durch Decoherence-Tunneling.

**Provenance:** Phase 4 Research-Brief "Quantum Coherence Cosmology"
(siehe `research/briefs/quantum-coherence-cosmology.md`).

**Affects:** Kapitel 12-16, 23, 31-34. Per `scene-matrix.md` cross-ref.
```

## §3 Status-Lifecycle

```
proposed ──► accepted ──► contested ──► superseded ──► archived
                                          │
                                          └──► accepted (re-affirmed)
```

| Status | Bedeutung | Wann setzen |
|--------|-----------|-------------|
| `proposed` | Entry frisch geschrieben, noch nicht user-approved | Bei Phase-4/7 Research-Integration *vor* Author-Approval |
| `accepted` | User hat zugestimmt, Entry ist Canon | Nach Author-Approval; default für Phase-Output |
| `contested` | Späterer Entry widerspricht dem hier; `canon_conflicts_with` populiert | Bei Phase-7-Audit, wenn zwei accepted Entries kollidieren |
| `superseded` | Ein neuerer Entry hat diesen ersetzt; `canon_resolved_by` populiert | Wenn `contested` → User entschieden für den anderen Eintrag |
| `archived` | Historischer Reference, nicht mehr Canon | Bei Roman-Schluss-Cleanup oder Sub-Projekt-Wechsel |

## §4 Phase-7 Audit-Mode Integration

Phase 7 (`/novel-reflect` → audit) MUSS:

1. Alle `accepted` Canon-Einträge gegeneinander auf Konflikte prüfen
2. Bei Konflikt: beide auf `contested` setzen, `canon_conflicts_with` cross-link
3. askuser welcher behalten wird
4. Looser auf `superseded`; Sieger bleibt `accepted` mit notes-trace

Audit-Output landet in `<workspace>/canon-audit-report.md` (analog Hard-
Rules-Check).

## §5 Cross-Reference Index in canon-meta.md

`canon-meta.md` SOLL am Ende eine Index-Tabelle haben:

```markdown
## Index

| canon_id | Title | Status | Affects |
|----------|-------|--------|---------|
| canon-dkt-physik-001 | Lichtgeschwindigkeits-Constraint | accepted | Kapitel 12-16, 23, 31-34 |
| canon-dkt-physik-002 | (superseded by 001) | superseded | — |
| canon-stil-001 | Mosaic-POV-Convention | accepted | alle Kapitel |
```

Phase-7-Audit aktualisiert diesen Index automatisch.

## §6 Acceptance Scenarios (Normativ)

```gherkin
Feature: Canon-Status lifecycle preserves Author intent

  # anchor: T076.CS.1
  Scenario: New canon entry starts as proposed
    Given Phase 4 produces a research finding to be canonized
    When the agent writes the entry to canon-meta.md
    Then the entry's canon_status MUST be "proposed"
    And the agent MUST askuser for approval before flipping to "accepted"

  # anchor: T076.CS.2
  Scenario: Phase 7 audit catches contested canon
    Given canon-meta.md has two accepted entries with logically-incompatible content
    When /novel-reflect runs in audit-mode
    Then both entries' canon_status MUST be set to "contested"
    And canon_conflicts_with MUST be populated reciprocally
    And the agent MUST surface the conflict for User-resolution

  # anchor: T076.CS.3
  Scenario: Superseded entries are not silently deleted
    Given a contested entry is resolved against in favour of the other
    When the agent finalizes the audit
    Then the loser's canon_status MUST be set to "superseded" (not deleted)
    And canon_resolved_by MUST cite the audit run that decided
    And canon-meta.md MUST preserve the loser's body content for provenance
```

## §7 Open Questions (Sequel)

- Linter `tools/check-canon-status.py` für status-lifecycle-Konsistenz? — Sequel.
- Cross-Project-Canon-Sharing (z.B. wenn zwei Romans im selben DKT-Universum)? — Sequel-Decision.
- Automatic conflict-detection in Phase 7 via LLM, oder strictly user-driven? — askuser.
