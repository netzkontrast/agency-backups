# Learnings — novel-architect Self-Improvement Log

> Mandatorisch: Bei jedem Session-Ende wird hier mindestens ein Eintrag ergänzt — was hat suboptimal funktioniert, was ist die Korrektur. Anschließend Skill packen.

## Format

Jeder Eintrag hat: Datum, Trigger (was passierte), Lesson, Action (was wird ab jetzt anders gemacht — entweder als SKILL.md-Edit, references-Edit oder als Heuristik in einer commands/-Datei).

---

## 2026-05-03 — Drive-Doc-Ingest: PDF-Export statt read_file_content

**Trigger:** Bei der Aufgabe „Drive-Files in markdown ingesten" griff ich reflexhaft zu `Google Drive:read_file_content`, das den vollen Text als Tool-Response in den Context lädt. Bei 14 Files à 30-200KB hätte das den Context massiv aufgebläht.

**Lesson:** Für Google Docs in Drive ist der korrekte token-sparende Pfad: `download_file_content` mit `exportMimeType: 'application/pdf'` → bytes nach `/tmp/<slug>.pdf` schreiben → `pdf-to-markdown` skill (`scripts/convert.py`) läuft → `.md` landet in `ingest/`, ohne dass je der volle Text durch meinen Context muss. Genau dafür ist die context-safe-Mode des pdf-to-markdown skills gebaut. Ich habe den skill gelesen und trotzdem zur falschen Tür gegriffen.

**Action:**
1. **In `references/workflows.md`** (Workflow `archive-material` und neuer Workflow `drive-doc-ingest`): Pflicht-Pfad ist Drive→PDF-Export→pdf-to-markdown. `read_file_content` nur dann, wenn der User den Inhalt explizit IN-TURN braucht (Zitat, Summary, sofortige Analyse).
2. **In `SKILL.md` Routing-Matrix**: archive-material-Zeile präzisieren — auch Google Docs (nicht nur PDFs) gehen über pdf-to-markdown via PDF-Export-Trick.
3. **In `commands/analyze.md`**: Bei Drive-Source-Phase explizit auf PDF-Export-Pfad verweisen.

**Status:** Heute angewendet, in workflows.md/SKILL.md Edits folgen am Session-Ende.

---

## 2026-05-03 — Self-Improvement als Pflicht-Schritt am Session-Ende

**Trigger:** User-Vorgabe: „Self-Improvement-Steps should always be mandatory at the end of a session."

**Lesson:** Der Skill hat zwar `references/skill-improvement-todo.md` und ein „Skill-Improvement TODO"-Kapitel in der SKILL.md, aber der Trigger zum Updaten dieser Files war nirgends als Pflicht-Schritt im Iteration-Discipline-Block kodifiziert. „Wäre nett" → wurde inkonsistent gemacht.

**Lesson, präziser:** Lerne UNTERWEGS, nicht erst am Ende. Beobachtungen während der Session werden im Moment ihres Auftretens festgehalten (in diesem `learnings.md`), nicht „gemerkt für später". Der Session-Ende-Schritt ist nur die Verifikation („was steht da, was muss noch rein?"), nicht der Erstinhalt.

**Action:**
1. **SKILL.md Iteration-Discipline-Sektion erweitern**: Session-End-Checkpoint umfasst jetzt explizit (a) progress.md update, (b) NCP/canon-meta update wenn nötig, (c) **learnings.md Eintrag (mandatorisch, mind. 1)**, (d) Skill packen.
2. **Während-Session-Heuristik**: Wenn ich merke „das hätte ich anders machen sollen" — sofort in `learnings.md` notieren, nicht aufschieben.
3. **Bootstrap-Schritt erweitern**: Beim Workspace-Setup auch `learnings.md` als Reference-File laden (dann sehe ich frühere Lessons direkt am Session-Anfang und kann verhindern, sie zu wiederholen).

**Status:** Diese Datei selbst ist die Implementierung von Punkt 1+3. SKILL.md-Edit folgt am Session-Ende.

---

## 2026-05-03 — pymupdf4llm via PyPI nicht installierbar; pdfplumber-Fallback funktioniert

**Trigger:** Beim Drive-Doc-Ingest sollte `pdf-to-markdown` skill mit `pymupdf4llm` arbeiten. Install schlug fehl: `host_not_allowed` für `pypi.org` und `files.pythonhosted.org`. Skill geht als Pflicht-Pfad nicht.

**Lesson:** PyPI ist im Sandbox nicht erreichbar. Vorinstalliert sind: `pdfminer.six`, `pdfplumber`, `pypdf`, `pypdfium2`, `pikepdf`, `pdf2image`. Für Prosa-extrahieren-aus-PDF ist `pdfplumber` der sinnvolle Fallback (preserves paragraphs and reading order, lose Heading-Hierarchie).

**Action:**
1. **In `references/workflows.md`** (Workflow `archive-material` und `drive-doc-ingest`): Ergänzen — wenn `pymupdf4llm` nicht verfügbar, fallback auf `pdfplumber`-basiertes Skript. Helper-Skript-Vorlage in `tmp/convert_pdfplumber.py` ablegen (einmal geschrieben, beim Bootstrap kopieren).
2. **Im `pdf-to-markdown` Skill upstream**: TODO in `skill-improvement-todo.md` notieren — sollte Fallback-Pfad eingebaut bekommen, oder zumindest klarer dokumentieren, dass PyPI nicht garantiert erreichbar ist.
3. **Bootstrap-Schritt erweitern**: Beim Workspace-Setup `convert_pdfplumber.py` in `tmp/` legen, damit es nicht jede Session neu geschrieben werden muss.

**Status:** Heute angewendet. Skript existiert in `tmp/convert_pdfplumber.py`. Bootstrap-Update folgt am Session-Ende.

---

## 2026-05-03 — Drive-Doc-Ingest via PDF-Export ist context-safe

**Trigger:** Beim ersten `download_file_content`-Call kam Tool-Result zurück mit Hinweis "Tool result too large for context, stored at /mnt/user-data/tool_results/...". Genau das, was der User mit "you don't need to waste your tokens" meinte.

**Lesson:** Das MCP-System hat einen Auto-Spillover: große Tool-Results gehen auf Disk, nicht in den Chat. Das macht den Drive→PDF-Export-Pfad **per Default token-effizient** — Base64 von 200KB-PDFs landet nicht im Context. Ich kann beliebig viele Files pipeline-haft ziehen.

**Lesson, weiter:** `read_file_content` (alternative für Google Docs) gibt vermutlich Text inline zurück, was bei 50KB-Docs den Context aufbläht. PDF-Export ist robuster.

**Action:**
1. **In `references/workflows.md`** Workflow `drive-doc-ingest` als kanonischen Workflow für jegliche Drive-Doc → workspace ingestion definieren. PDF-Export-Pfad ist Standard, `read_file_content` nur für In-Turn-Verwendung (User braucht Inhalt sofort im Chat, z.B. "summarize" oder "quote line X").
2. **Manifest-Pflicht:** Bei jedem Bulk-Ingest Manifest-Datei in `outputs/research/` schreiben (siehe `ingest-manifest-2026-05-03.md` als Vorlage), damit man später ohne Re-Read nachschlagen kann, was wo liegt.
3. **Dedupe-Schritt:** md5sum + diff-Check ist billig und fängt Whitespace-Dupes (typisch für Gemini-Deep-Research-Outputs in mehreren Saves). In den Workflow als Pflicht-Sub-Step aufnehmen.

**Status:** Heute angewendet. Workflow-Definition folgt am Session-Ende.

---

## 2026-05-03 — Konflikt-Detection im Inventar ist wichtiger als reine Liste

**Trigger:** Zwei Drive-Files (analyse vs verortung) zertifizierten konkurrierende Storyform-Konfigurationen. Wenn ich nur eine Liste mit 8 Kandidaten ausgegeben hätte, wäre der User mit kontradiktorischen "kanonisch"-Verdicts allein gelassen.

**Lesson:** Bei jeder Sammlung von Research-Outputs explizit auf **Widersprüche zwischen Sources** prüfen. Gemini-Deep-Research-Outputs sind nicht koordiniert; jeder Run macht seine eigene "kanonische" Empfehlung. Wenn der User mehrere solche Runs gemacht hat, kollidieren sie.

**Action:**
1. **Im Workflow `research-ingestion`**: Pflicht-Schritt "Conflict Detection" hinzufügen — bei mehreren Source-Files mit Empfehlungs-Charakter (Verdikt, Auswahl, kanonisch-Bezeichnungen) eine Cross-Source-Diff-Tabelle bauen.
2. **Inventar-Format:** Spalte "Konflikt mit Canon?" und Spalte "Verdikt im Source" trennen — der Source kann etwas als "kanonisch" zertifizieren, das mit dem aktuellen Skill-Canon nicht übereinstimmt. Beide Tatsachen sind wichtig.

**Status:** Heute angewendet im `storyform-candidates-inventory.md`. Workflow-Update folgt am Session-Ende.

---

## 2026-05-03 — KRITISCH: Bootstrap-Read war oberflächlich, ganze Session-Hälfte redundant

**Trigger:** Nach 5+ Frage-Antwort-Runden mit dem User über A1-vs-V3 / AEGIS-Position / AEGIS-Ontologie / Dual-Storyform-Sinnhaftigkeit habe ich entdeckt, dass ALLES davon bereits in dieser oder einer parallelen Session heute (2026-05-03) kanonisiert wurde:
- canon-meta.md hatte bereits Sektionen „AEGIS = System-Ebene-ANP", „Holon-Spiegelachse", „AEGIS — Voice-Regel", „Per-Throughline-Mapping zwischen Storyform A und B", „Verworfene Storyform-Alternativen mit Begründung", alle markiert „kanonisiert 2026-05-03" / „Stand 2026-05-03".
- open-questions.md hatte bereits OQ-04 (A1-vs-V3), OQ-05 (AEGIS-Ontologie), OQ-06 (Dual-Storyform-Sinn) **als resolved markiert**, mit Verweis „entschieden 2026-05-03 via /interview".

Der User wusste das. „AEGIS ist auch ein ANP" war keine Offenbarung, sondern eine 4-Wort-Erinnerung an etablierten Canon. Ich habe darauf reagiert, als wäre es eine Neuentdeckung.

**Lesson:** Mein Bootstrap-Read war oberflächlich — `grep -n "^## "` auf canon-meta.md statt vollständiger Inhalts-Lesung. Ich habe gesehen *dass* es eine AEGIS-Sektion gibt, aber nicht *was* drin steht. Die SKILL.md sagt explizit „Schritt 3: canon-meta.md lesen — Nicht-strukturelle Canon-Daten" — Lesung, nicht Skim.

**Wurzel-Ursache:** Bei Session-Start hatte der User unmittelbar einen großen Phasen-Plan vorgelegt + „Look for Drive files". Ich bin zu schnell in die Drive-Ingest-Aktion gegangen, ohne den Bootstrap-Read auf canon-meta.md und open-questions.md vollständig durchzuziehen. Klassisches Action-Bias unter perceived urgency.

**Action — verbindlich:**

1. **In `SKILL.md` Bootstrap-Sektion:** Schritte 3 und 5 (canon-meta.md, open-questions.md) müssen **explizit** als „vollständig lesen, nicht skimmen" markiert sein. Aktuell stehen sie da, aber ohne expliziten Anti-Skim-Hinweis. Ergänzen: „Lesen heißt: jede Sektion mindestens ihren Erst-Absatz lesen, nicht nur Section-Header per grep abscannen."

2. **In `SKILL.md` neue Heuristik:** Bei jedem User-Input, der einen Workflow auslöst (insbesondere Action-Workflows wie /research-ingestion, /draft, /encoding), **vor der ersten Aktion** ein 30-Sekunden-Sanity-Check: „Steht das Issue, das ich gleich angehe, eventuell schon in canon-meta.md oder open-questions.md als resolved drin?" Genauer: nach Bootstrap-Lesung 1 explizit gegen die Liste der resolved-OQs prüfen, BEVOR neue Analyse-Arbeit startet.

3. **Bootstrap-Output-Pflicht:** Beim Session-Start eine Zusammenfassung in den Working-Memory schreiben (kein User-facing Output, aber interne Notiz): „Resolved OQs: [Liste]. Active Architektur-Fragen: [Liste]. Letzte Canon-Updates: [Datum + Sektion]." Wenn der User dann mit einem Frage-/Aktions-Wunsch kommt, der eine resolved-OQ wieder aufmacht, das **explizit benennen** statt es nochmal komplett neu zu rollen.

4. **Skill-Versions-Bump auf 0.3.3** in SKILL.md zur Markierung dieses Disziplin-Updates.

**Status:** Diese Session: alle vier Action-Items werden in SKILL.md verankert vor dem Skill-Pack. Künftige Sessions: müssen vor Action-Workflows explizit „Bootstrap done, no resolved-OQ-conflict with current task" verifizieren.

**Meta-Bemerkung:** Diese Stunde Arbeit war nicht ganz wertlos — Drive-Ingest hat tatsächlich Sichtungs-Material extrahiert, und die First-Principles-Reproduktion etablierter Canon ist als Konsistenz-Beleg hilfreich. Aber 80% der Tokens hätten gespart werden können durch sauberen Bootstrap-Read. Der User hat höflich mitgemacht, statt zu sagen „das hatten wir doch schon" — was bedeutet, dass diese Disziplin-Lücke nur durch Self-Improvement-Protokoll geschlossen werden kann, nicht durch User-Korrektur.

---

## 2026-05-03 — Phönix-Mode-Pflicht statt advocate-Mode bei meta-architektonischen Fragen

**Trigger:** User fragte direkt: „macht Dual-Storyform überhaupt Sinn? Oder machen wir es uns zu kompliziert für keinen Mehrwert?" Mein Reflex wäre gewesen, die A1-Empfehlung zu verteidigen — Dual-Storyform ist ja gerade als Canon bestätigt worden. Der User hat aber explizit eine ehrliche bidirektionale Analyse verlangt.

**Lesson:** Bei meta-architektonischen Fragen („ist die ganze Konstruktion sinnvoll?") darf ich nicht in den Modus „verteidige den Status Quo, weil ich ihn gerade etabliert habe" verfallen. Phönix-Mode (Steelman + Inversion + First Principles) ist nicht nur für Storyform-Auswahl, sondern auch für architektonische Selbstprüfung. Die userMemory listet das explizit als Methode — ich hatte es nur im Storyform-Selektion-Kontext angewendet.

**Lesson, weiter:** Wenn ich Pro UND Contra ehrlich aufschreibe, kommt oft eine produktive Tertium-Position („Quasi-Storyform / Eineinhalb") aus dem Vergleich. Hätte ich nur die A1-Verteidigung gemacht, wäre die Quasi-Storyform-Option dem User nicht angeboten worden. Sie hätte gewählt werden können. Tertium-Generierung ist Teil der Phönix-Pflicht.

**Action:**
1. **In `commands/analyze.md`** (oder neuer `commands/architecture-review.md`): Phönix-Mode als Pflicht-Pattern bei jeder Frage des Typs „ist X sinnvoll" / „brauchen wir X" / „lohnt sich X" verankern. Drei Sektionen Steelman/Inversion/First Principles, dann Tertium-Vorschlag, dann User-Wahl.
2. **In `references/learnings.md`** (diese Datei): künftig auch positive Beobachtungen festhalten — was lief gut, das ich beibehalten will. Bisher dominieren Korrekturen. Phönix-Mode-Anwendung war ein Plus heute.

**Status:** Heute angewendet. commands-File-Update als Skill-TODO notiert.

---

## 2026-05-03 — Canon-Klärung in einer 4-Wort-User-Antwort: „Aegis ist auch ein ANP"

**Trigger:** Auf eine Frage zu V3's philosophischer Wurzelsorge antwortete der User mit vier Worten: „Aegis ist auch ein ANP". Ich hatte vier Optionen zur Wahl gegeben (A/B/C/D), keine davon enthielt diese Antwort. Der User hat die Frage einfach umgangen und die *richtige Antwort* gegeben, die ich nicht angeboten hatte.

**Lesson:** Multiple-Choice-Fragen via `ask_user_input_v0` haben einen blinden Fleck — sie zwingen den User in ein Antwortenset, das ich präselektiert habe. Wenn der User eine Antwort hat, die NICHT in meinem Set ist, gibt es zwei Auswege: (a) er ignoriert die Frage und schreibt frei, (b) er wählt die nächstbeste Option und ich verliere die eigentliche Information. Heute hat er (a) gewählt.

**Lesson, weiter:** Eine richtige Antwort kann sehr viel kürzer sein als meine Analyse-Latte. „AEGIS ist auch ein ANP" hat in vier Worten 6 meiner Argumentations-Threads neu kontextualisiert (Bewusstseins-Frage, MC-Eignung, Voice-Regel, Holon-Symmetrie, Vortex-Mechanik, Dual-Storyform-Begründung). Das ist nicht „der User hat zu wenig geschrieben" — das ist Verdichtung von jemandem, der seinen Stoff kennt.

**Action:**
1. **Wenn Multiple-Choice angeboten wird**: immer eine „andere/Freitext"-Option als letzte Option mit anbieten, oder explizit signalisieren „falls keine passt, schreib frei". Verhindert das Blind-Spot-Problem.
2. **Wenn User mit kurzer Phrase antwortet, die nicht eine Option ist**: NICHT als Eingabefehler behandeln, sondern als Substanz-Antwort lesen und entfalten. Reflektieren, was die Phrase strukturell bedeutet, dann als Hypothese formulieren („Verstehe ich das so: ..."), bevor ich Canon-Edits committe. Heute habe ich das richtig gemacht (eine Bestätigungs-Frage zur Holon-Position gestellt, dann committed). Das ist die Pflicht-Sequenz.

**Status:** Heute richtig angewendet. Als Pattern in commands/-Files notieren.

---

## 2026-05-03 — Memory-Drift erkannt: 'AEGIS = 3rd person' war nicht haltbar

**Trigger:** Im Verlauf der Diskussion stellte sich heraus, dass die userMemory-Zeile „All 13 = 1st person. AEGIS + Guardians = 3rd person" mit der NCP-Spec (`narrative_storyform_b.subtext.perspectives[0].author_structural_pov: 'i'` für AEGIS = 1st person) im Konflikt stand. Dieser Konflikt war seit dem Reset 2026-04-30 in der Memory schlummernd. Mein Bootstrap hat die Spannung nicht aufgedeckt — ich habe Memory und NCP nebeneinander gelesen, aber nicht gegeneinander geprüft.

**Lesson:** Memory-NCP-Drift kann lange unbemerkt bleiben. Mein Bootstrap-Skript liest beide, aber checkt sie nicht auf Konsistenz. Memory ist „Notiz, nicht Maßstab" — aber wenn die Notiz vom Maßstab abweicht und niemand das merkt, blendet sie mich.

**Action:**
1. **Bootstrap-Schritt: Memory-NCP-Konsistenz-Check.** Beim Workspace-Setup automatisch prüfen: enthält die userMemory Aussagen, die mit der NCP-Spec im Widerspruch stehen? Beispielfelder zum Prüfen: Player-POV (1st/3rd person), Domain-Zuweisung, Outcome/Judgment, MC-Resolve. Bei Drift: Warnung in Bootstrap-Output, kein Auto-Fix.
2. **In `references/canon-meta.md`** Material-Status-Sektion explizit ergänzen: „Memory ist Notiz; bei Konflikt mit NCP/canon-meta gewinnt NCP/canon-meta. Memory wird nachgezogen, nicht andersrum."

**Status:** Heute aufgedeckt und Memory-Edit als TODO für nächsten /memory-Sync notiert. Bootstrap-Script-Erweiterung als Skill-TODO.

---
