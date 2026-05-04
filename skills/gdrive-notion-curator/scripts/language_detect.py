#!/usr/bin/env python3
"""Detect language of text. DE/EN heuristic via stopwords.

Usage:
    python3 language_detect.py "<text>"
    cat file.txt | python3 language_detect.py -

Output: de | en | mixed | unknown
"""
from __future__ import annotations

import argparse
import re
import sys

DE_STOPWORDS = set("der die das ein eine einen und oder aber wenn dann als auch noch nur schon doch werden wird ist sind hat haben war waren wurde wurden würde könnte sollte müsste mit von zu auf im in an bei aus für über unter durch zum zur des den dem ich du er sie es wir ihr mich dich sich".split())

EN_STOPWORDS = set("the a an and or but if then as also only just yet still will would could should might been being have has had was were is are of in on at by for from to with about i you he she it we they me him her us them this that these those".split())


def detect_language(text: str) -> str:
    text_lower = text.lower()
    words = re.findall(r'\b[a-zA-Zäöüß]+\b', text_lower)
    word_set = set(words)

    de_hits = len(word_set & DE_STOPWORDS)
    en_hits = len(word_set & EN_STOPWORDS)

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


def main():
    parser = argparse.ArgumentParser(description="Detect language (de/en/mixed/unknown)")
    parser.add_argument('text', nargs='?', default=None, help="Text to analyze. Use '-' for stdin.")
    args = parser.parse_args()

    if args.text == '-' or args.text is None:
        text = sys.stdin.read()
    else:
        text = args.text

    print(detect_language(text))
    return 0


if __name__ == '__main__':
    sys.exit(main())
