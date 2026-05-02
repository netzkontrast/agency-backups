# Step 1: First-Principles Zerlegung der Kernbegriffe

## 1.1 Was ist „Obsidian Frontmatter"?
**Zerlegung:**
Auf der basalsten Ebene ist Obsidian Frontmatter ein reiner YAML-Block, der am absoluten Beginn einer Markdown-Datei steht, eingefasst durch `---` Delimiter. Er wird nicht als Markdown gerendert, sondern durch Obsidians Properties UI (seit v1.0) geparst und als visuelles Interface dargestellt.
**Unterschied zu Inline-YAML:** Inline-YAML (z.B. Dataview-Felder `Key:: Value`) wird direkt im Fließtext verwendet. Es ist nicht Teil der formalen, strukturierten Datei-Metadaten auf Dateisystem-Ebene, sondern wird durch Plugins zur Laufzeit interpretiert.
**Abhängigkeit zu Plugins:** Plugins wie Dataview oder Templater nutzen das Frontmatter für Queries oder Variablen, zwingen aber nicht das Format auf. Obsidian selbst validiert die grundlegende YAML-Syntax.

## 1.2 Was ist „tokeneffizientes Navigieren"?
**Zerlegung:**
- **Token:** Die atomare Informationseinheit eines LLMs (ca. 4 Zeichen). Context Windows haben harte Limits und Token-Verarbeitung kostet Zeit/Geld.
- **Navigieren:** Die Fähigkeit eines autonomen Agenten, die Relevanz einer Datei für eine spezifische Suchanfrage zu bewerten, *ohne* den vollständigen Dateiinheit laden zu müssen.
- **Differenz:** Ein YAML-Block mit 10 Feldern beansprucht ca. 50-100 Tokens. Das Laden einer durchschnittlichen 5k-Wort Datei beansprucht ca. 6.000-7.000 Tokens. Der Unterschied ist eine Größenordnung von 10^2. Ein Agent, der nur das Frontmatter liest, kann 100 Dateien "scannen" für das gleiche Tokenbudget einer komplett gelesenen Datei.

## 1.3 Was ist das „Expansion Pattern"?
**Zerlegung:**
- **Bedingung für Index-Node:** Eine Datei wird zu einem Index-Node, wenn ihre Informationsdichte oder ihre Verzweigungstiefe ein Maß überschreitet, das sinnvollerweise als ein einzelnes Konzept erfasst werden kann (Zersplitterung).
- **Was wandert:** Der operative Inhalt und detaillierte Gedanken wandern in granulare Unterdateien in einem spezifischen Unterordner, der denselben Namen trägt wie die Ursprungsdatei.
- **Was bleibt:** Die Ursprungsdatei behält ihre Identität (Dateiname), alle Metadaten (Frontmatter), eine Kurzzusammenfassung und Verweise (Links) auf die neuen Unterdateien.
- **Manifest / README.md:** Die `readme.md` in diesem neuen Unterordner dient nicht als Notiz an sich, sondern als technisches Manifest für Agenten und Menschen, das die Struktur dieses Sub-Graphen erklärt.

## 1.4 Was ist das Minimum einer „Spec"?
**Zerlegung:**
- **MUSS:** Ein Feld, das ausnahmslos zwingend vorhanden sein muss, damit das System (Agent, UI oder Mensch) nicht bricht. Fehlt es, ist die Datei defekt.
- **KANN:** Ein optionales Feld, das Mehrwert bietet (z.B. Domänen-Erweiterungen).
- **DARF NICHT:** Eine explizite Verbotsregel, meist basierend auf technischen Limits (z.B. keine 3-Ebenen-Verschachtelung im YAML, da Obsidians UI bricht).
- **Minimum für Konsumenten:**
  - *Mensch:* Braucht Titel und Tags für Verortung.
  - *Obsidian UI:* Braucht natives, valides YAML (sonst Parse Error).
  - *Agent:* Braucht eine Zusammenfassung (`summary`) und Status (`status`), um zu entscheiden, ob er die Datei öffnet.
