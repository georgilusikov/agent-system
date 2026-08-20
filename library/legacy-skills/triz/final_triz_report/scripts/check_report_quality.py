#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


FORBIDDEN_SUBSTRINGS = (
    "Next Step",
    "Handoff",
    "TBD",
    "TODO",
)

REQUIRED_MARKERS = (
    "Принцип действия",
    "Конструкция",
    "Сценарий",
    "Рекомендация",
)

LATIN_LOWER_RE = re.compile(r"[a-z]")


def looks_like_russian(text: str) -> bool:
    return bool(re.search(r"[А-Яа-яЁё]", text))

def strip_markdown_code(text: str) -> str:
    text = re.sub(r"(?s)```.*?```", "", text)
    text = re.sub(r"`[^`]*`", "", text)
    return text


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Lightweight lint for TRIZ final reports (Russian, no placeholders, required sections)."
    )
    parser.add_argument("path", type=Path, help="Path to a Markdown report")
    parser.add_argument(
        "--no-latin",
        action="store_true",
        help="Fail if the report contains Latin lowercase letters a-z (strict 'no English words' mode).",
    )
    args = parser.parse_args()

    if not args.path.exists():
        print(f"ERROR: file not found: {args.path}", file=sys.stderr)
        return 2

    text = args.path.read_text(encoding="utf-8", errors="replace")

    problems: list[str] = []

    if not looks_like_russian(text):
        problems.append("no-cyrillic: report does not look like Russian text")

    if args.no_latin:
        strict_text = strip_markdown_code(text)
        if LATIN_LOWER_RE.search(strict_text):
            problems.append("latin-lowercase-found: report contains English words (Latin lowercase letters)")

    for forbidden in FORBIDDEN_SUBSTRINGS:
        if forbidden in text:
            problems.append(f"forbidden-placeholder: contains {forbidden!r}")

    for marker in REQUIRED_MARKERS:
        if marker not in text:
            problems.append(f"missing-marker: {marker!r}")

    solution_count = len(
        re.findall(r"^#{1,6}\s*(?:\d+\s*[.)]\s*)?Решение\b", text, flags=re.MULTILINE)
    )
    if solution_count < 3:
        problems.append(f"too-few-solutions: found {solution_count}, expected >= 3 (headings like '## Решение ...')")

    if problems:
        print("FAIL", file=sys.stderr)
        for problem in problems:
            print(f"- {problem}", file=sys.stderr)
        return 1

    print("OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
