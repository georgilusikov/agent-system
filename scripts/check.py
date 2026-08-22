#!/usr/bin/env python3
"""Validate the canonical repository and optional deployed consumer paths."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
HOME = Path.home()
FRONTMATTER = re.compile(r"\A---\s*\n(?P<body>.*?)\n---\s*\n", re.DOTALL)


def check_repo() -> list[str]:
    errors: list[str] = []
    required = [
        "AGENTS.md", "README.md", "sources.json", "skills", "scripts",
        "scripts/agent_run_state.py", "scripts/runtime_receipts.py",
        "scripts/change_receipts.py", "scripts/memory_candidates.py",
        "scripts/memory_capture.py", "scripts/evaluate_before_after.py",
        "scripts/provider_canary.py", "hooks/claude/test-privacy-hooks.sh",
        "scripts/test_runtime_acceptance.py",
    ]
    for relative in required:
        if not (REPO / relative).exists():
            errors.append(f"missing:{relative}")
    acceptance = REPO / "scripts/test_runtime_acceptance.py"
    if acceptance.exists():
        try:
            result = subprocess.run(
                [sys.executable, str(acceptance)], cwd=REPO,
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                timeout=10, check=False,
            )
        except subprocess.TimeoutExpired:
            errors.append("runtime-acceptance-timeout")
        else:
            if result.returncode:
                errors.append(f"runtime-acceptance-failed:{result.returncode}")
    hook_privacy = REPO / "hooks/claude/test-privacy-hooks.sh"
    if hook_privacy.exists():
        try:
            result = subprocess.run(
                ["bash", str(hook_privacy)], cwd=REPO,
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                timeout=10, check=False,
            )
        except subprocess.TimeoutExpired:
            errors.append("hook-privacy-timeout")
        else:
            if result.returncode:
                errors.append(f"hook-privacy-failed:{result.returncode}")
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
        HOME / ".dsh" / "AGENTS.md": REPO / "AGENTS.md",
        HOME / ".codex" / "AGENTS.md": REPO / "AGENTS.md",
        HOME / ".gemini" / "GEMINI.md": REPO / "AGENTS.md",
        HOME / ".claude" / "CLAUDE.md": REPO / "AGENTS.md",
        HOME / ".grok" / "rules" / "00-agent-system.md": REPO / "AGENTS.md",
        HOME / ".codex" / "hooks.json": REPO / "adapters/hooks/codex.json",
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
    for runtime in ("codex", "claude", "gemini"):
        for source in (REPO / "hooks" / runtime).iterdir():
            if not source.is_file() or source.name.startswith(("test-", "test_")):
                continue
            target = HOME / f".{runtime}" / "hooks" / source.name
            if not target.is_symlink() or target.resolve() != source.resolve():
                errors.append(f"hook-not-deployed:{target}")
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
