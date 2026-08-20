#!/usr/bin/env python3
"""gen_hook_registry — мини-реестр хуков Claude Code.

Читает ~/.claude/settings.json (секция hooks) + docstring каждого .py-хука
и печатает markdown-таблицу: хук | событие/matcher | описание | есть тест 🟢/🔴.

«Есть тест» = имя файла хука упоминается в ~/.claude/hooks/tests/*.py.

Usage: python3 ~/.claude/hooks/gen_hook_registry.py
"""

from __future__ import annotations

import ast
import json
import re
from pathlib import Path

CLAUDE_DIR = Path.home() / ".claude"
HOOKS_DIR = CLAUDE_DIR / "hooks"
SETTINGS = CLAUDE_DIR / "settings.json"
TESTS_DIR = HOOKS_DIR / "tests"


def docstring_summary(path: Path) -> str:
    if path.suffix != ".py" or not path.is_file():
        return ""
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"))
        doc = ast.get_docstring(tree) or ""
        return doc.strip().splitlines()[0][:90] if doc.strip() else ""
    except (SyntaxError, OSError, UnicodeDecodeError):
        return ""


def tested_names() -> str:
    text = ""
    if TESTS_DIR.is_dir():
        for f in TESTS_DIR.glob("*.py"):
            try:
                text += f.read_text(encoding="utf-8")
            except OSError:
                continue
    return text


def main() -> int:
    settings = json.loads(SETTINGS.read_text(encoding="utf-8"))
    hooks_cfg = settings.get("hooks", {})
    tests_text = tested_names()

    rows: list[tuple[str, str, str, str]] = []
    for event, matcher_blocks in hooks_cfg.items():
        for block in matcher_blocks:
            matcher = block.get("matcher", "") or "*"
            for hook in block.get("hooks", []):
                cmd = hook.get("command", "")
                m = re.search(r"([\w.\-]+\.(?:py|sh))", cmd)
                name = m.group(1) if m else cmd[:40]
                path = HOOKS_DIR / name
                desc = docstring_summary(path)
                has_test = "🟢" if name and name in tests_text else "🔴"
                rows.append((name, f"{event} ({matcher})", desc, has_test))

    print("| Хук | Событие (matcher) | Описание | Тест |")
    print("|---|---|---|---|")
    for name, event, desc, has_test in rows:
        print(f"| {name} | {event} | {desc} | {has_test} |")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
