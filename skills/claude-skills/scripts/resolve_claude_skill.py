#!/usr/bin/env python3
"""Resolve Claude Code skills from repo-local and global skill roots."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:  # pragma: no cover - fallback for minimal Python envs
    yaml = None


def normalize(raw: str) -> str:
    """Normalize slash, at, or dollar skill names to hyphen-case lookup keys."""
    value = raw.strip().lstrip("/@$").lower()
    value = re.sub(r"[^a-z0-9_-]+", "-", value)
    value = value.replace("_", "-").strip("-")
    return re.sub(r"-{2,}", "-", value)


def parse_frontmatter(skill_md: Path) -> dict[str, Any]:
    """Parse YAML frontmatter from a SKILL.md file."""
    text = skill_md.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return {}
    match = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
    if not match:
        return {}
    frontmatter = match.group(1)
    if yaml is not None:
        try:
            loaded = yaml.safe_load(frontmatter)
            return loaded if isinstance(loaded, dict) else {}
        except Exception:
            pass

    result: dict[str, Any] = {}
    current_key: str | None = None
    for line in frontmatter.splitlines():
        key_match = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
        if key_match:
            current_key = key_match.group(1).strip()
            value = key_match.group(2).strip().strip("\"'")
            if value in {">", "|"}:
                value = ""
            result[current_key] = value
            continue
        if current_key and line.startswith((" ", "\t")):
            value = line.strip().strip("\"'")
            if value:
                existing = str(result.get(current_key) or "")
                result[current_key] = f"{existing} {value}".strip()
            continue
    return result


def candidate_roots(cwd: Path) -> list[Path]:
    """Return repo-local .claude/skills roots from cwd upward, then global root."""
    roots: list[Path] = []
    seen: set[Path] = set()

    for parent in [cwd, *cwd.parents]:
        root = parent / ".claude" / "skills"
        if root.exists():
            resolved = root.resolve()
            if resolved not in seen:
                roots.append(root)
                seen.add(resolved)

    global_root = Path.home() / ".claude" / "skills"
    if global_root.exists():
        resolved = global_root.resolve()
        if resolved not in seen:
            roots.append(global_root)
    return roots


def discover(cwd: Path) -> list[dict[str, str]]:
    """Discover Claude skills, preserving root precedence."""
    found: dict[str, dict[str, str]] = {}

    for root in candidate_roots(cwd):
        for child in sorted(root.iterdir(), key=lambda item: item.name.lower()):
            skill_md = child / "SKILL.md"
            if not skill_md.exists():
                continue
            frontmatter = parse_frontmatter(skill_md)
            name = str(frontmatter.get("name") or child.name)
            key = normalize(name)
            if key in found:
                continue
            found[key] = {
                "name": name,
                "key": key,
                "path": str(skill_md.resolve()),
                "root": str(root.resolve()),
                "description": str(frontmatter.get("description") or "").strip(),
            }

    return sorted(found.values(), key=lambda item: item["key"])


def print_table(rows: list[dict[str, str]]) -> None:
    """Print a compact markdown table."""
    print("| Skill | Source | Description |")
    print("|---|---|---|")
    for row in rows:
        description = " ".join(row["description"].split())
        if len(description) > 120:
            description = f"{description[:117]}..."
        print(f"| /{row['key']} | `{row['path']}` | {description} |")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("skill", nargs="?", help="Skill name such as /why, @check, or go")
    parser.add_argument("--cwd", default=".", help="Working directory for repo-local lookup")
    parser.add_argument("--list", action="store_true", help="List discovered Claude skills")
    parser.add_argument("--json", action="store_true", help="Emit JSON")
    args = parser.parse_args()

    rows = discover(Path(args.cwd).expanduser().resolve())

    if args.list or not args.skill:
        if args.json:
            print(json.dumps(rows, ensure_ascii=False, indent=2))
        else:
            print_table(rows)
        return 0

    target = normalize(args.skill)
    matches = [row for row in rows if row["key"] == target or normalize(row["name"]) == target]
    if not matches:
        print(f"Claude skill not found: {args.skill}")
        print("Known skills:")
        print(", ".join(f"/{row['key']}" for row in rows))
        return 1

    selected = matches[0]
    if args.json:
        print(json.dumps(selected, ensure_ascii=False, indent=2))
    else:
        print(f"name: /{selected['key']}")
        print(f"path: {selected['path']}")
        print(f"root: {selected['root']}")
        print(f"description: {' '.join(selected['description'].split())}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
