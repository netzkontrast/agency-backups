#!/usr/bin/env python3
"""Classify a Drive-File against topics-config.yaml.

Usage:
    python3 classify.py --title "<title>" --content "<content>" --topics-yaml <path>

Output (JSON):
    {
      "topic": "kohaerenz-protokoll" | null,
      "confidence": "high" | "medium" | "low" | "none",
      "suggested": [list of slugs],
      "reason": "human-readable explanation",
      "is_sensitive": bool,
      "sensitive_topic": "trauma-dis-material" | null
    }
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from pathlib import Path

try:
    import yaml
except ImportError:
    print(json.dumps({"error": "PyYAML not installed. Run: pip install --break-system-packages pyyaml"}))
    sys.exit(1)


def normalize(s: str) -> str:
    s = s.translate({
        ord('ä'): 'ae', ord('ö'): 'oe', ord('ü'): 'ue', ord('ß'): 'ss',
        ord('Ä'): 'ae', ord('Ö'): 'oe', ord('Ü'): 'ue',
    })
    s = unicodedata.normalize('NFKD', s)
    s = ''.join(c for c in s if not unicodedata.combining(c))
    return s.lower()


def check_sensitive(title_norm: str, topics: list[dict]) -> tuple[bool, str | None]:
    """Title-only check for sensitive topics."""
    for topic in topics:
        if not topic.get('sensitive', False):
            continue
        for kw in topic.get('keywords', []):
            kw_norm = normalize(kw)
            if kw_norm in title_norm:
                return True, topic['slug']
    return False, None


def classify(title: str, content: str, topics: list[dict]) -> dict:
    title_norm = normalize(title)
    content_norm = normalize(content[:5000])  # cap

    # Sensitive-Check vorab
    is_sensitive, sensitive_topic = check_sensitive(title_norm, topics)
    if is_sensitive:
        return {
            "topic": sensitive_topic,
            "confidence": "high",
            "suggested": [sensitive_topic],
            "reason": f"sensitive title-match: {sensitive_topic}",
            "is_sensitive": True,
            "sensitive_topic": sensitive_topic,
        }

    # Normal scoring
    scores = {}
    for topic in topics:
        slug = topic['slug']
        score = 0
        matched = []
        for kw in topic.get('keywords', []):
            kw_norm = normalize(kw)
            if kw_norm in title_norm:
                score += 3
                matched.append(f"title:{kw}")
            if kw_norm in content_norm:
                score += 1
                matched.append(f"content:{kw}")
        if score > 0:
            scores[slug] = (score, matched)

    if not scores:
        return {
            "topic": None,
            "confidence": "none",
            "suggested": [],
            "reason": "no keywords matched in title or content (first 5k chars)",
            "is_sensitive": False,
            "sensitive_topic": None,
        }

    ranked = sorted(scores.items(), key=lambda x: -x[1][0])
    top_slug, (top_score, top_kws) = ranked[0]

    # high
    if top_score >= 6:
        return {
            "topic": top_slug,
            "confidence": "high",
            "suggested": [s for s, _ in ranked],
            "reason": f"strong match {top_slug} ({top_score} pts): {', '.join(top_kws[:3])}",
            "is_sensitive": False,
            "sensitive_topic": None,
        }

    # medium
    if top_score >= 3 and (len(ranked) == 1 or ranked[1][1][0] < top_score - 2):
        return {
            "topic": top_slug,
            "confidence": "medium",
            "suggested": [s for s, _ in ranked],
            "reason": f"match {top_slug} ({top_score} pts): {', '.join(top_kws[:3])}",
            "is_sensitive": False,
            "sensitive_topic": None,
        }

    # low — multiple competing
    if len(ranked) > 1 and ranked[1][1][0] >= top_score - 2:
        all_close = [(s, sc) for s, (sc, _) in ranked if sc >= top_score - 2]
        return {
            "topic": None,
            "confidence": "low",
            "suggested": [s for s, _ in all_close],
            "reason": f"multiple competing: {', '.join(s for s, _ in all_close)}",
            "is_sensitive": False,
            "sensitive_topic": None,
        }

    # low — weak single
    return {
        "topic": top_slug,
        "confidence": "low",
        "suggested": [top_slug],
        "reason": f"weak match {top_slug} ({top_score} pts): {', '.join(top_kws[:2])}",
        "is_sensitive": False,
        "sensitive_topic": None,
    }


def main():
    parser = argparse.ArgumentParser(description="Classify file against topics-config.yaml")
    parser.add_argument('--title', required=True)
    parser.add_argument('--content', default='', help="Content sample (first 3-5k chars). Empty for sensitive files.")
    parser.add_argument('--topics-yaml', required=True, help="Path to topics-config.yaml")
    args = parser.parse_args()

    yaml_path = Path(args.topics_yaml)
    if not yaml_path.exists():
        print(json.dumps({"error": f"topics-yaml not found: {yaml_path}"}))
        return 1

    config = yaml.safe_load(yaml_path.read_text(encoding='utf-8'))
    topics = config.get('topics', [])

    if not topics:
        print(json.dumps({"error": "no topics in config"}))
        return 1

    result = classify(args.title, args.content, topics)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    sys.exit(main())
