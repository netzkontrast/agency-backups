# Skill-Improvement TODO

Beobachtungen über die Skill-Pipeline hinweg, die hier nicht akut gefixt werden,
aber dokumentiert gehören. Liste wächst über Zeit.

Stand: 2026-05-11 (novel-architect v1.0.0 — Refactor zu methoden-zentriert)

---

## novel-architect (this skill)

### Done in v1.0.0 (2026-05-11)
- [x] Komplettes Refactor von v0.3.3 zu methoden-zentriert
- [x] 8 Phasen mit Hard Exit Gates implementiert (`phases/phase{0..7}-*.md`)
- [x] AskUserQuestion-Pattern adaptiert von `research-prompt-optimizer`
- [x] Methoden-Bibliothek (`methods/character/`, `methods/structure/`, `methods/conflict/`, `methods/research/`)
- [x] Project-Workspace-Abstraktion (`/home/claude/novel-projects/<slug>/`)
- [x] NCP-Integration-Contract dokumentiert
- [x] /sc:-Command-Mapping pro Phase
- [x] Asset-Templates (intent, architecture, character, scene-matrix, draft, research-brief, project-config, progress)
- [x] References (routing-matrix, ncp-contract, sc-mapping) neu geschrieben
- [x] Legacy als `novel-architect-legacy@0.3.3-deprecated` parallel
- [x] Bootstrap-Script für Projekt-Workspace-Setup + Legacy-Migration

### Done from v0.x (übernommen)
- [x] Bootstrap-Protocol generalisiert
- [x] Significance-Heuristik generalisiert
- [x] NCP als State-Management-Layer (zwingend)
- [x] Memory-Sync outward-only Pattern
- [x] Constraint: NCP-Mutation NUR via ncp-author

### Open (Roadmap v1.1+)

- [ ] **commands/novel-*.md Volltexte**: Aktuell als Stubs angelegt; voller Prompt-Content fehlt für jeden Sub-Command
- [ ] **render/io_helpers.py vollständig**: Aktuell minimal; analog `research-prompt-optimizer/render/io_helpers.py` ausbauen (append-only revisions, status-views, plan-views, audit-reports)
- [ ] **render/render_intent.py, render_architecture.py, render_scene_matrix.py**: Aktuell minimal-Skelett; volle Implementierung
- [ ] **examples/ mit project-agnostischen worked examples**: Nicht Kohärenz-spezifisch (z.B. generisches Hard-SF, generisches Literary)
- [ ] **methods/ erweitern**: weitere Charakter-Modelle (MBTI, Schema Therapy), Strukturen (3-Akt, 7-Point), Konflikt-Engines (Mythology-as-Engine)
- [ ] **Eval-Test-Suite via /skill-creator**: Min. 5 Test-Prompts, qualitative + quantitative Bewertung
- [ ] **NCP-Schema-Update auf v1.4.0 (sobald upstream)**: Pinning prüfen
- [ ] **Versionierungs-Konvention**: v1.0 = Refactor done; v1.1 = commands ausgebaut; v1.2 = render-helpers vollständig; v2.0 = mehrere Roman-Projekte erfolgreich
- [ ] **Migration-Audit-Mode**: Phase 7 audit für Legacy-Migration (validiert Kohärenz-Protokoll-Daten)

---

## Cross-Skill (skill-pipeline gaps)

### ncp-author Reifegrad-Risiko
- `ncp-author@0.4.0` ist MVP (Path A); kein eigener Validator über ajv hinaus
- Schema-Drift Risiko bei upstream NCP changes
- Workaround: pin schema_version in `project-config.yaml`, re-pin bei Updates

### Cross-Skill Inter-Skill Handoff Schema
- Es gibt keinen kanonisierten Hand-off-Standard zwischen den Roman-Skills
- Vorschlag (offen): YAML mit `from_skill`, `to_skill`, `operation`, `payload`, `expected_return`
- Würde Phase 4 (research-prompt-optimizer Delegation) und Phase 2/3/5 (ncp-author Delegation) standardisieren

### Memory-Sync Outward-Only Disziplin
- Aktuell: Skill→Memory broadcast Pattern dokumentiert
- Offen: Tooling für „Memory Diff" zwischen Skill und Memory (zeigt drift)
