#!/usr/bin/env python3
"""Validate the canonical repository and optional deployed consumer paths."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
HOME = Path.home()
FRONTMATTER = re.compile(r"\A---\s*\n(?P<body>.*?)\n---\s*\n", re.DOTALL)


def check_repo() -> list[str]:
    errors: list[str] = []
    required = ["AGENTS.md", "README.md", "sources.json", "skills", "scripts"]
    for relative in required:
        if not (REPO / relative).exists():
            errors.append(f"missing:{relative}")
    agents = REPO / "AGENTS.md"
    if agents.exists() and len(agents.read_text(encoding="utf-8").splitlines()) > 245:
        errors.append("AGENTS.md exceeds 245 lines")
    skills = REPO / "skills"
    if skills.exists():
        names: set[str] = set()
        for skill_file in sorted(skills.glob("*/SKILL.md")):
            text = skill_file.read_text(encoding="utf-8")
            match = FRONTMATTER.match(text)
            if not match:
                errors.append(f"invalid-frontmatter:{skill_file.relative_to(REPO)}")
                continue
            fields: dict[str, str] = {}
            for line in match.group("body").splitlines():
                if ":" in line and not line.startswith((" ", "\t")):
                    key, value = line.split(":", 1)
                    fields[key.strip()] = value.strip().strip("'\"")
            name = fields.get("name", "")
            description = fields.get("description", "")
            if not name or not description:
                errors.append(f"missing-name-description:{skill_file.relative_to(REPO)}")
            if name and name != skill_file.parent.name:
                errors.append(f"name-dir-mismatch:{skill_file.parent.name}:{name}")
            if name in names:
                errors.append(f"duplicate-skill-name:{name}")
            names.add(name)
    for path in REPO.rglob("*"):
        if path.is_symlink() and not path.exists():
            errors.append(f"broken-symlink:{path.relative_to(REPO)}")
    manifest = REPO / "migration" / "union-manifest.json"
    if manifest.exists():
        data = json.loads(manifest.read_text(encoding="utf-8"))
        if data.get("source_config_sha256") is None or not data.get("entries"):
            errors.append("invalid-union-manifest")
    return errors


def check_deployed() -> list[str]:
    expected = {
        HOME / ".codex" / "AGENTS.md": REPO / "AGENTS.md",
        HOME / ".gemini" / "GEMINI.md": REPO / "AGENTS.md",
        HOME / ".claude" / "CLAUDE.md": REPO / "AGENTS.md",
        HOME / ".grok" / "rules" / "00-agent-system.md": REPO / "AGENTS.md",
        HOME / ".gemini" / "config" / "hooks.json": REPO / "adapters/hooks/agy.json",
    }
    errors: list[str] = []
    for target, source in expected.items():
        if not target.is_symlink():
            errors.append(f"not-symlink:{target}")
            continue
        if target.resolve() != source.resolve():
            errors.append(f"wrong-target:{target}:{target.resolve()}")
    for root in (
        HOME / ".agents" / "skills",
        HOME / ".codex" / "skills",
        HOME / ".claude" / "skills",
        HOME / ".gemini" / "config" / "skills",
        HOME / ".grok" / "skills",
    ):
        if not root.is_dir():
            errors.append(f"missing-skill-root:{root}")
            continue
        for skill in (REPO / "skills").iterdir():
            if not skill.is_dir():
                continue
            target = root / skill.name
            if not target.is_symlink() or target.resolve() != skill.resolve():
                errors.append(f"skill-not-deployed:{target}")
    gemini_guard = HOME / ".gemini" / "hooks" / "guard.py"
    if not gemini_guard.is_symlink() or gemini_guard.resolve() != (REPO / "hooks/gemini/guard.py").resolve():
        errors.append(f"hook-not-deployed:{gemini_guard}")
    gemini_settings = HOME / ".gemini" / "settings.json"
    if gemini_settings.exists():
        actual = json.loads(gemini_settings.read_text(encoding="utf-8"))
        desired = json.loads((REPO / "adapters/hooks/gemini.json").read_text(encoding="utf-8"))
        for key in ("context", "hooks"):
            if actual.get(key) != desired[key]:
                errors.append(f"settings-drift:{gemini_settings}:{key}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", action="store_true")
    parser.add_argument("--deployed", action="store_true")
    args = parser.parse_args()
    errors: list[str] = []
    if args.repo or not args.deployed:
        errors.extend(check_repo())
    if args.deployed:
        errors.extend(check_deployed())
    if errors:
        for error in errors:
            print(f"ERROR {error}")
        return 1
    print("PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
