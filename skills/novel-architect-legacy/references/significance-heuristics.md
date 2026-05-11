# Significance Heuristics

Wann lohnt es, den Skill neu zu packen und via `present_files` zurückzugeben? Wann reicht ein progress.md-Update? Wann nicht mal das?

Drei Stufen: **Cheap update**, **Checkpoint**, **No-op**.

---

## Drei Stufen

### Stufe 1: Cheap update (häufig, fast immer)

Update von `references/progress.md` mit ein paar Sätzen. Kein Packaging, kein present_files. Reine Notiz für die nächste Session.

**Wann**:
- Nach jedem Workflow-Schritt, der mehr als nur Lookup war
- Nach einem nicht-trivialen Brainstorm
- Nach einer Architektur-Diskussion, die noch nicht in Entscheid mündet
- Nach jedem Teilfortschritt innerhalb eines Workflows

**Aufwand**: ~30 Sekunden (str_replace in progress.md). Praktisch frei.

### Stufe 2: Checkpoint (selten, nur bei substantieller Wirkung)

Volle Packaging-Sequenz:
1. progress.md final updaten (was ist passiert, was kommt als nächstes)
2. **NCP-Datei** updaten via `ncp-author` — falls strukturelle Mutation
3. **canon-meta.md** updaten — falls nicht-strukturelle Canon-Mutation
4. open-questions.md updaten (falls OQ resolved)
5. memory-sync NUR wenn User explizit Memory-Broadcast verlangt (Memory ist nicht Teil des Canon-Pfads)
6. `python tmp/skills-ref/skill-creator/scripts/package_skill.py novel-architect/`
7. `present_files` mit der `.skill`-Datei (und den relevanten Output-Artefakten)

**Wann (5 Trigger — EIN Trigger reicht)**:

**A. Canon-Shift (strukturell)** — irgendetwas, das die NCP-Datei ändert:
- Storyform-Slot festgelegt oder verfeinert (`narratives[].subtext.dynamics[]`)
- Storypoint encoded (`narratives[].subtext.storypoints[]`)
- Player-Detail entschieden (`narratives[].subtext.players[]` — name, role, visual, audio, bio, motivations)
- Storybeat positioniert (`narratives[].subtext.storybeats[]`)
- Moment definiert (`narratives[].storytelling.moments[]`)
- Cross-narrative Beat-Reference gesetzt (Slot-16-Mechanik)

**B. Canon-Shift (nicht-strukturell)** — irgendetwas, das `canon-meta.md` ändert:
- DKT-Regel-Änderung
- Alter-Somatik gefüllt (z. B. Lia/Isabelle/Argus/Silas/Oblivion-FEHLT-Einträge gefüllt)
- Riss-Mandate-Anpassung
- Prosa-Regel hinzugefügt oder geändert
- Mandate-Update
- Projekt-Meta-Änderung (Drive-Pfade, Material-Status)
- Vortex-Beat-Übersicht aktualisiert

**C. Phase-Unit complete** — eine atomare Einheit:
- 1 Throughline encoded für 1 narrative (Phase 1-4: 8 atomare Units, je 4 Storypoints in NCP)
- 1 Dynamic verfeinert (Phase 5: 16 atomare Units)
- 10 Kapitel storywoven (Phase 6: ~4 Milestones — Storybeats + Moments in NCP)
- 1 Vortex-Beat operationalisiert (Phase 7: 5 atomare Units — Storybeats in NCP)
- 1 OQ resolved (Phase 8: variable)
- 1 Chapter draft fertig

**D. Workflow-Pivot** — User wechselt zu anderem Workflow:
- Encoding → Storyweaving
- Storyweaving → Vortex-Architecture
- Drafting → Canon-Update
- Beliebig zwischen den 10 Workflows

**E. Volume threshold** — Aufaddiertes:
- 3+ neue Files in `outputs/` seit letztem Checkpoint, ODER
- ~2000+ Wörter substantielles Material, ODER
- 10+ NCP-Mutationen seit letztem Checkpoint

**F. Session-End** — IMMER:
- User sagt „lass uns aufhören", „save and close", „Session-Ende"
- User wechselt erkennbar das Projekt
- Auch wenn die Session „nichts ergab": ein Checkpoint mit „nichts geändert" als progress-Eintrag ist besser als kein Checkpoint

### Stufe 3: No-op (häufig, gar nichts tun)

Weder progress.md noch Packaging.

**Wann**:
- Term-Lookup in dramatica-vocabulary
- Q&A ohne Canon-Berührung
- Reading-mode (User liest References, fragt zu Verständnis)
- Triviale Klarstellung
- Interview-Antwort-Phase (Antworten geben, ohne dass etwas entschieden wird)

---

## Heuristik-Beispiele

### Eindeutig signifikant → Checkpoint

**Beispiel A (Phase-Unit complete + NCP-Mutation)**:
> User: „OK, MC-Encoding für narrative_a ist durch. Alle 4 Storypoints in Szenen-Keimen, Block-4-Anker abstrahiert."

→ Phase-Unit complete (Throughline-Encoding A-MC fertig).
→ NCP-Mutation: 4 neue Storypoints in `narrative_storyform_a.subtext.storypoints[]` + Player-Updates für Kael.
→ Checkpoint.

**Beispiel B (Canon-Shift strukturell — OQ + NCP)**:
> User: „Slot 16 ist jetzt entschieden: Per-Chapter Dual-POV via cross-narrative Storybeat-Referenzen in Moments."

→ Canon-Shift strukturell (Architektur-Frage gelöst, NCP-Schema-Verwendung definiert).
→ open-questions.md update (Slot 16 als gelöst markieren).
→ NCP-Datei bekommt einen Beispiel-Moment mit cross-narrative storybeats[].
→ Memory-Broadcast: nur wenn User extra verlangt.
→ Checkpoint.

**Beispiel C (Canon-Shift nicht-strukturell — canon-meta)**:
> User: „Lia's Somatik füllen wir jetzt: Superposition-Schwindel, Hände wechseln zwischen Faust und offen."

→ Canon-Shift nicht-strukturell (Alter-Somatik-Tabelle in canon-meta.md aktualisiert).
→ canon-meta.md update.
→ Memory-Broadcast: nur wenn User extra verlangt.
→ Checkpoint.

**Beispiel D (Workflow-Pivot)**:
> User: „Gut, jetzt lass uns zur Storyweaving-Phase wechseln."

→ Workflow-Pivot von Encoding zu Storyweaving.
→ Letzten Encoding-Stand checkpointen, bevor neuer Workflow startet.
→ Checkpoint.

**Beispiel E (Session-End)**:
> User: „Lass uns aufhören für heute, speicher alles."

→ Session-End. Checkpoint.

### Eindeutig nicht signifikant → No-op

**Beispiel F (Term-Lookup)**:
> User: „Was ist nochmal der Driver-Pivot?"

→ dramatica-vocabulary konsultieren, antworten. Kein progress, kein package.

**Beispiel G (Q&A)**:
> User: „Erklär mir kurz, warum Storyform B Failure/Bad als Outcome/Judgment hat."

→ Antwort geben (aus NCP `dynamic_b_outcome` und `dynamic_b_judgment` ableitbar). Kein progress, kein package.

**Beispiel H (Reading)**:
> User: „Zeig mir den aktuellen NCP-Stand."

→ NCP-Datei lesen / zeigen. Kein progress, kein package.

### Grenzfälle

**Beispiel I (Brainstorm ohne Entscheid)**:
> User: „Brainstorm: drei mögliche Bilder für Kael in Ch3 — sterile Behörde, Antiquariat, U-Bahn-Schacht."

→ Cheap update in progress.md. Kein package, keine NCP-Mutation.

→ Wenn der User später entscheidet: „OK, U-Bahn-Schacht für Ch3" → DAS ist Canon-Shift strukturell (Moment.setting in NCP) → Checkpoint.

**Beispiel J (Tiefe Architektur-Diskussion ohne Entscheid)**:
> User: 90 Minuten Diskussion über Reader-Function-Layers, viele Hypothesen, viele Verwerfungen, kein Resolution.

→ Cheap update mit Zusammenfassung der Diskussions-Achsen. Kein package — es ist nichts entschieden.

→ ABER: Wenn die Session zu Ende geht: Session-End-Trigger → Checkpoint trotzdem.

**Beispiel K (Volume-Threshold)**:
> 5 Stunden Session, 8 Output-Files, 5000 Wörter, 12 NCP-Mutationen.

→ Volume threshold reached → Checkpoint.

---

## NCP-spezifische Anti-Pattern

- **Hand-Edit der NCP-Datei**: Verboten. Nur via ncp-author. Bei Schema-Drift fällt das Skeleton-Dokument auseinander.
- **Strukturelle Daten in canon-meta.md schmuggeln**: Wenn etwas in NCP gehört (Player-Detail, Storypoint, Storybeat), MUSS es in NCP. canon-meta.md ist NICHT die Backup-Heimat für strukturelle Inhalte.
- **canon-meta-Daten in NCP zwingen**: Umgekehrt auch. DKT-Persistenzgleichung passt nicht in `dynamic.storytelling`. Riss-Mandate sind keine Storypoints. Mandate bleiben Markdown.
- **Validierung überspringen**: Nach NCP-Mutation per ncp-author idealerweise upstream-Validator laufen lassen. Wenn das nicht geht (z. B. weil Node nicht verfügbar): explizit notieren, dass nicht validiert wurde.

## Memory-Hierarchie Anti-Pattern

- **Memory automatisch updaten**: Memory ist NICHT Teil des Canon-Pfads. Auch nicht „nebenbei". Nur auf explizites User-Kommando.
- **Memory als Vergleichsmaßstab nehmen**: Bei Diskrepanz NCP/canon-meta vs. Memory: Skill-Files gewinnen. Nicht „Memory says X, also ist X richtig".
- **Aus Memory in den Skill kopieren ohne User-Bestätigung**: Wenn der User auf etwas in Memory verweist, das nicht im Skill steht, NACHFRAGEN ob das Canon werden soll. Nicht stillschweigend übernehmen.
- **Memory-Slot-Strukturen nachbauen**: Memory hat Slot #1-#13 als grobe Themen-Felder. Skill hat NCP-Pfade + canon-meta-Sektionen. Das sind zwei verschiedene State-Modelle. Nicht versuchen, sie 1:1 abzubilden.

---

## Anti-Pattern: Über-Eager Packaging

NICHT machen:
- Nach jedem User-Turn packen
- Bei jeder Frage „soll ich packen?" fragen
- Aus Übervorsicht packen, wenn nichts entschieden ist
- Bei trivialen Klarstellungen packen

Packaging hat Kosten:
- Token-Aufwand
- User-Aufmerksamkeit
- Versions-Inflation

---

## Anti-Pattern: Under-Eager Packaging

Auch NICHT machen:
- Phase-Unit complete + nicht packen
- Session-End ohne Checkpoint
- Canon-Shift „in den Wind" entscheiden
- 5000 Wörter Output ohne Persistenz
- 10 NCP-Mutationen ohne Validierung und Package

Was nicht gepackt ist, geht beim nächsten Bootstrap verloren.

---

## Skill-interne vs. workspace-externe Persistenz

Wichtig zu unterscheiden:

- **Skill-intern** (überlebt via packaging): SKILL.md, references/, commands/ — inklusive der NCP-Datei in references/canon/
- **Workspace** (lebt nur in der Session): tmp/, outputs/, archive/

Wenn ein Output kanonisch werden soll: Inhalt → NCP via ncp-author (strukturell) oder canon-meta.md (nicht-strukturell). Sonst: Drive-Sync via drive-markdown-converter.

`outputs/` ist Werkbank — nichts dort ist permanent ohne aktive Archivierung.
