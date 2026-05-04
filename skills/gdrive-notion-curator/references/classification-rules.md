# Klassifikations-Regeln

> Title + Content gegen `topics-config.yaml` matchen. Output: `{topic, confidence, suggested, reason}`.

## Confidence-Levels

| Level | Bedeutung | Routing |
|---|---|---|
| `high` | Eindeutiger Match (1 Topic, mehrere primary keywords im Title) | Auto-indexiert |
| `medium` | Klarer Match (1 Topic, 1+ keyword) | Auto-indexiert |
| `low` | Schwacher Match (mehrere Topics oder nur secondary keyword) | → Inbox |
| `none` | Kein Match überhaupt | → Inbox mit Suggested Slug |

## Algorithmus

```python
def classify(title: str, content: str, topics_config: dict) -> ClassificationResult:
    """
    Returns:
      ClassificationResult(
        topic: str | None,         # Primary topic slug, None if no match
        confidence: str,           # high|medium|low|none
        suggested: list[str],      # All matching slugs (could be multiple)
        reason: str                # Human-readable explanation
      )
    """

    title_norm = normalize(title.lower())
    content_norm = normalize(content[:5000].lower())  # cap content size

    scores = {}  # topic_slug → score

    for topic in topics_config['topics']:
        slug = topic['slug']
        topic_score = 0
        matched_kws = []

        for kw in topic['keywords']:
            kw_norm = normalize(kw.lower())

            # Title-Match wertet 3x
            if kw_norm in title_norm:
                topic_score += 3
                matched_kws.append(f"title:{kw}")

            # Content-Match wertet 1x (nur erste 5k chars)
            if kw_norm in content_norm:
                topic_score += 1
                matched_kws.append(f"content:{kw}")

        if topic_score > 0:
            scores[slug] = (topic_score, matched_kws)

    # Sortiere nach Score absteigend
    ranked = sorted(scores.items(), key=lambda x: -x[1][0])

    # No match
    if not ranked:
        return ClassificationResult(
            topic=None, confidence="none",
            suggested=[],
            reason="no keywords matched in title or content (first 5k chars)"
        )

    top_slug, (top_score, top_kws) = ranked[0]

    # Single high-confidence match
    if top_score >= 6:  # min 2 title-matches
        return ClassificationResult(
            topic=top_slug, confidence="high",
            suggested=[s for s, _ in ranked],
            reason=f"strong match {top_slug} ({top_score} pts): {', '.join(top_kws[:3])}"
        )

    # Single medium-confidence match
    if top_score >= 3 and (len(ranked) == 1 or ranked[1][1][0] < top_score - 2):
        return ClassificationResult(
            topic=top_slug, confidence="medium",
            suggested=[s for s, _ in ranked],
            reason=f"match {top_slug} ({top_score} pts): {', '.join(top_kws[:3])}"
        )

    # Multiple competing matches → low
    if len(ranked) > 1 and ranked[1][1][0] >= top_score - 2:
        all_close = [(s, sc) for s, (sc, _) in ranked if sc >= top_score - 2]
        return ClassificationResult(
            topic=None, confidence="low",
            suggested=[s for s, _ in all_close],
            reason=f"multiple competing matches: {', '.join(s for s, _ in all_close)}"
        )

    # Single weak match → low
    return ClassificationResult(
        topic=top_slug, confidence="low",
        suggested=[top_slug],
        reason=f"weak match {top_slug} ({top_score} pts): {', '.join(top_kws[:2])}"
    )
```

## Scoring-Details

| Match-Type | Punkte |
|---|---|
| Keyword in Title (lowercased, normalized) | 3 |
| Keyword in Content (erste 5000 Zeichen) | 1 |

Schwellen:
- `high`: Score ≥ 6 (mind. 2 Title-Matches)
- `medium`: Score ≥ 3 UND deutlich vor #2 (Differenz ≥ 2 Punkte)
- `low`: Sonst, oder mehrere Topics ähnlich nah

## Sprach-Detection

Separate Funktion. Pure-Python ohne externe Dependencies.

```python
def detect_language(text: str) -> str:
    """
    Returns: de | en | mixed | unknown
    Heuristik: zähle stop-words pro Sprache.
    """
    de_stopwords = set("der die das ein eine und oder aber wenn dann als auch noch nur schon doch werden wird ist sind hat haben war waren wurde wurden würde könnte sollte müsste".split())
    en_stopwords = set("the a an and or but if then as also only just yet still will would could should might been being have has had was were is are".split())

    text_lower = text.lower()
    import re
    words = re.findall(r'\b\w+\b', text_lower)
    word_set = set(words)

    de_hits = len(word_set & de_stopwords)
    en_hits = len(word_set & en_stopwords)

    if de_hits == 0 and en_hits == 0:
        return "unknown"

    total = de_hits + en_hits
    de_ratio = de_hits / total

    if de_ratio > 0.7:
        return "de"
    elif de_ratio < 0.3:
        return "en"
    else:
        return "mixed"
```

## Topic-Konflikt-Beispiele

| Title | Content-Sample | Erwartete Klassifikation |
|---|---|---|
| `"Kohärenz Protokoll Kapitel 5.md"` | "...AEGIS reagiert auf Kael..." | high → kohaerenz-protokoll (Title 2x kw + Content 2x kw) |
| `"Notes on Dramatica.md"` | "Storyform analysis for character arc" | medium → dramatica-theory (Title 1x, Content 2x) |
| `"Some Thoughts.md"` | "Working on music production today, also kohaerenz progress" | low → multiple matches kohaerenz-protokoll, music-production |
| `"Random.md"` | "weather is nice today" | none → empty, Inbox |
| `"Trauma Notes.md"` | (sensitive — kein content-read) | high sensitive → trauma-dis-material (Title 1x kw bei sensitive Topic = automatisch high) |

## Sensitive-Override

**Wichtig:** Bei Title-Match auf sensitive Topic (siehe `sensitive-handling.md`) wird Klassifikation **VOR** Content-Read entschieden:
- Confidence = high (bei mind. 1 keyword-match)
- Topic = sensitive-Topic
- Kein Content-Match-Scoring (kein Content gelesen)

## CLI-Tool

`scripts/classify.py`:

```bash
python3 scripts/classify.py \
  --title "Kohärenz Protokoll Kapitel 5" \
  --content "AEGIS reagiert auf Kael..." \
  --topics-yaml assets/topics-config.yaml
```

Output (JSON):
```json
{
  "topic": "kohaerenz-protokoll",
  "confidence": "high",
  "suggested": ["kohaerenz-protokoll"],
  "reason": "strong match kohaerenz-protokoll (8 pts): title:kohaerenz, title:protokoll, content:aegis"
}
```

## Inbox-Trigger

Wenn `confidence in ('low', 'none')` und nicht-sensitive:
- Inbox-DB-Entry mit:
  - `Suggested Slug`: lowercased ersten 1-2 distinct nouns aus Title (siehe `topics-initial.md` für Stopword-Liste)
  - `Sample File IDs`: aktuelle Drive-ID
  - `Sample File Count`: 1 (oder Increment wenn schon Inbox-Entry mit gleichem Suggested Slug)
  - `Status`: pending-review
  - `Suggested Keywords`: top 3-5 distinct nouns aus Title + Content-Auszug (Token-Häufigkeit)

## Score-Tuning

Wenn User sagt "klassifiziert immer falsch": justierbar in der Funktion oben. Spezifisch:
- Title-Gewicht 3 → höher (z.B. 5) wenn Titel gewöhnlich aussagekräftig
- Content-Gewicht 1 → höher wenn viele kurze Files mit knappen Titeln
- Schwelle high (6) → niedriger (4) wenn Klassifikation zu konservativ
