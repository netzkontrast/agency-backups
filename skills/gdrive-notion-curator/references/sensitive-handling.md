# Sensitive-Topic-Handling

> **Hard Rule:** Files mit sensitiven Topics (z.B. `trauma-dis-material`) werden NICHT inhaltlich gelesen oder als Sub-Page mit Inhalt indexiert. Title-only Klassifikation, Sub-Page mit nur Metadaten.

## Welche Topics sind sensitive

In `assets/topics-config.yaml` markiert mit `sensitive: true`. Default sensitiv:
- `trauma-dis-material`

User kann weitere als sensitive markieren — dann gelten die gleichen Regeln.

## Erkennungs-Algorithmus (Title-only)

```python
def is_sensitive(title: str, topics_config: dict) -> tuple[bool, str | None]:
    """
    Returns (is_sensitive, matched_topic_slug)
    """
    title_normalized = normalize(title.lower())
    for topic in topics_config['topics']:
        if not topic.get('sensitive', False):
            continue
        for keyword in topic['keywords']:
            kw_normalized = normalize(keyword.lower())
            if kw_normalized in title_normalized:
                return True, topic['slug']
    return False, None


def normalize(s: str) -> str:
    """Umlaut-normalize + Unicode-strip für robusten Match."""
    s = s.translate({ord('ä'): 'ae', ord('ö'): 'oe', ord('ü'): 'ue', ord('ß'): 'ss'})
    import unicodedata
    s = unicodedata.normalize('NFKD', s)
    s = ''.join(c for c in s if not unicodedata.combining(c))
    return s
```

Wichtig: Title-Match muss **vor jedem Content-Read** passieren. Wenn match: kein download_file_content für dieses File.

## Workflow für sensitive Files

```
1. Title-Match → sensitive=true, topic_slug=trauma-dis-material
2. Slug-Filename generieren (normales Slug, KEIN Sonder-Handling)
3. copy_file nach /curated/ (normaler Copy — Drive-Curated-Layer hat Files trotzdem)
4. Files-DB-Entry mit:
   - Sensitive: __YES__
   - Topic: trauma-dis-material
   - Confidence: high (Title-Match war eindeutig)
   - Match Reason: "title-match sensitive keyword"
   - Sort Status: indexed
5. KEIN download_file_content
6. KEIN Sprach-Detection (haben keinen Content)
7. Sub-Page in Topics-DB anlegen mit Sensitive-Template (siehe unten)
8. Sub-Page Link in Files-DB setzen
```

## Sub-Page-Template (sensitive)

Markdown-Inhalt der Sub-Page unter Topic-Page:

```markdown
# <Filename>

⚠️ **Sensitive Topic — Inhalt wird nicht von Claude gelesen oder indexiert.**

**Original:** [<original-title>](<original-drive-link>)
**Curated:** [<slug-filename>](<curated-drive-link>)
**Erstellt:** <created-date>
**Run:** <run-id>

Zugriff erfolgt direkt über die Drive-Links oben.
Diese Page enthält bewusst keinen inhaltlichen Auszug.

---

**Topic:** <topic-slug>
**Match:** Title-only sensitive keyword
```

## Wenn Title KEINEN sensitive-Keyword matcht aber Content sensitive ist

**Problem:** Skill liest Content (weil Title harmlos), erkennt erst dann dass Inhalt sensitive ist.

**Mitigation (aktuell):**
- Pure Title-Match. Wenn Content sensitive ist aber Title nicht, wird es als non-sensitive verarbeitet.
- User kann manuell nachträglich `Sensitive=__YES__` setzen in Files-DB
- Wenn User das tut: Sub-Page-Inhalt wird beim nächsten `repair`-Call mit dem Sensitive-Template überschrieben (askuser)

**v0.4.1-Idee:** Pre-Read-Check via Token-Sample (lese nur erste 200 Tokens, prüfe ob sensitive-Keywords drin → dann full sensitive-Treatment)

## Sensitive-Topic-Pages selbst

Die Topics-Page für `trauma-dis-material` selbst hat in der Topics-DB ein Sensitive-Flag = true. Anzeige in Notion-Views: kann gefiltert werden.

Topic-Page-Inhalt (vom Setup):
```markdown
# trauma-dis-material

⚠️ **Sensitive Topic.** Files werden Title-only klassifiziert. Inhalte sind nicht indexiert in Notion.

Files in diesem Topic erscheinen als Sub-Pages mit nur Metadaten.

Direkter Zugriff erfolgt via Drive-Links in den Sub-Pages.
```

## User-Override

User kann jederzeit:
- In Files-DB: `Sensitive` Checkbox toggeln (in beide Richtungen)
- In Files-DB: `Pinned=true` setzen → Skill rührt nichts mehr an

Bei Toggle `Sensitive` von false → true: nächster Sweep oder Repair-Call:
- Sub-Page wird mit askuser-Confirmation überschrieben (Inhalts-Auszug wird durch Sensitive-Template ersetzt)
- Files-DB: Match Reason wird angereichert "manually marked sensitive on <date>"

Bei Toggle von true → false: nichts automatisch — User muss separat triggern dass Content nachgeladen werden soll. Sub-Page bleibt im Sensitive-Template Format. (askuser bei nächstem Sweep: "Re-index file content?")

## Datenschutz-Eigenschaften

| Garantie | Wie sichergestellt |
|---|---|
| Sensitive-Title → kein Content-Read | Pre-Check vor download_file_content |
| Sub-Page enthält keinen Inhalt | Template mit nur Metadaten |
| Read by Claude bleibt false | Wir setzen es nie auf true für sensitive |
| Notes-Field vom User wird nicht überschrieben | Wir touchen Notes nie |

## Logging

Sensitive-Files erscheinen im Run-Log als:
```
[run-20260503-091500] Processed sensitive file: <filename> (topic=trauma-dis-material, content-read=skipped)
```

KEIN Inhalts-Snippet im Log, KEIN Hinweis auf Inhalt.
