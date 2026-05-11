# Significance Heuristics

> Wann lohnt es, den Skill neu zu packen und via `present_files` zurückzugeben?
> Wann reicht ein progress.md-Update? Wann nicht mal das?

Drei Stufen: **Cheap update**, **Checkpoint**, **No-op**.

---

## Drei Stufen

### Stufe 1: Cheap update (häufig, fast immer)

Update von `progress.md` im Projekt-Workspace mit ein paar Sätzen. Kein Packaging,
kein present_files. Reine Notiz für die nächste Session.

**Wann:**
- Nach jedem Phase-Schritt, der mehr als nur Lookup war
- Nach einem nicht-trivialen Brainstorm
- Nach einer Architektur-Diskussion, die noch nicht in Entscheid mündet
- Nach jedem Teilfortschritt innerhalb einer Phase

**Aufwand:** ~30 Sekunden. Praktisch frei.

### Stufe 2: Checkpoint (selten, nur bei substantieller Wirkung)

Volle Packaging-Sequenz:
1. `progress.md` final updaten (was ist passiert, was kommt als nächstes)
2. **NCP-Datei** updaten via `ncp-author` — falls strukturelle Mutation
3. **canon-meta.md** updaten — falls nicht-strukturelle Canon-Mutation
4. `open-questions.md` updaten (falls OQ resolved)
5. `memory-sync` NUR wenn User explizit Memory-Broadcast verlangt
6. `learnings.md` Eintrag (mandatorisch bei Session-End)
7. Skill packen via `bash scripts/package_skill.sh`
8. `present_files` mit der `.skill`-Datei + relevanten Output-Artefakten

**Wann (6 Trigger — EIN Trigger reicht):**

**A. Canon-Shift (strukturell)** — irgendetwas, das die NCP-Datei ändert:
- Storyform-Slot festgelegt oder verfeinert (`dynamics[]`)
- Storypoint encoded (`storypoints[]`)
- Player-Detail entschieden (`players[]`)
- Storybeat positioniert (`storybeats[]`)
- Moment definiert (`moments[]`)
- Cross-narrative Beat-Reference gesetzt (bei dual storyform)

**B. Canon-Shift (nicht-strukturell)** — irgendetwas, das `canon-meta.md` ändert:
- Welt-Regel-Änderung (Physik, Magie-System, etc.)
- Charakter-Detail außerhalb NCP gefüllt
- Prosa-Regel hinzugefügt oder geändert
- Mandate-Update
- Projekt-Meta-Änderung

**C. Phase-Unit complete** — eine atomare Einheit:
- 1 Throughline encoded (Phase 2)
- 1 Character architecture komplett (Phase 3)
- 1 Domain-Research-Cycle complete (Phase 4)
- 1 Akt-Block gemapped (Phase 5: 10 Kapitel + Storybeats + Moments)
- 1 OQ resolved (Phase 7)
- 1 Chapter draft fertig (Phase 6)

**D. Workflow-Pivot** — User wechselt zu anderem Phase:
- Phase 2 → Phase 3
- Phase 5 → Phase 4 (Research-Loop-back)
- Beliebige Phase → Phase 7 (Iteration/Audit)

**E. Volume threshold** — Aufaddiertes:
- 3+ neue Files in Projekt-Workspace seit letztem Checkpoint, ODER
- ~2000+ Wörter substantielles Material, ODER
- 10+ NCP-Mutationen seit letztem Checkpoint

**F. Session-End** — IMMER:
- User sagt „lass uns aufhören", „save and close", „Session-Ende"
- User wechselt erkennbar das Projekt
- Auch wenn die Session „nichts ergab": ein Checkpoint mit „nichts geändert"
  als progress-Eintrag ist besser als kein Checkpoint

### Stufe 3: No-op (häufig, gar nichts tun)

Weder progress.md noch Packaging.

**Wann:**
- Term-Lookup in `dramatica-vocabulary`
- Q&A ohne Canon-Berührung
- Reading-mode (User liest References, fragt zu Verständnis)
- Triviale Klarstellung
- Phase-1-Antworten geben, ohne dass approved-Slot gesetzt wird

---

## Heuristik-Beispiele

### Eindeutig signifikant → Checkpoint

**Beispiel A (Phase-Unit complete + NCP-Mutation):**
> User: „OK, MC-Encoding ist durch. Alle 4 Storypoints in Szenen-Keimen."

→ Phase-Unit complete (Throughline-Encoding fertig)
→ NCP-Mutation: 4 neue Storypoints + Player-Updates
→ Checkpoint.

**Beispiel B (Canon-Shift):**
> User: „Die Magie-Regel ist jetzt: Magie kostet Erinnerungen."

→ Canon-Shift (nicht-strukturell) — canon-meta.md update
→ Cascading: Storybeats in Phase 5 prüfen (verletzen sie die Regel?)
→ Checkpoint.

**Beispiel C (OQ resolved):**
> User: „OQ-12 ist entschieden: Antagonist ist Mentor's Schwester."

→ Phase-Unit complete (OQ resolved) + character-architecture.yaml update
→ Eventuell NCP-Mutation (player relationship)
→ Checkpoint.

### Eindeutig cheap update → progress.md only

**Beispiel D:**
> User: „Schreibe noch in progress, dass ich heute drei Szenen-Keime brainstormed habe."

→ Brainstorm ohne Festlegung
→ progress.md update, kein Package.

### Eindeutig no-op → gar nichts

**Beispiel E:**
> User: „Was war nochmal der Driver-Pivot?"

→ Term-Lookup in dramatica-vocabulary
→ Antwort geben, kein progress.md-update.

---

## Heuristik bei Unsicherheit

Wenn unklar, ob „Cheap" oder „Checkpoint":
- **Bei Canon-Berührung**: Checkpoint (Sicherheit-Bias)
- **Ohne Canon-Berührung**: Cheap update
- **Wenn nur diskutiert wurde**: Cheap update
