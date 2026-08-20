#!/usr/bin/env python3
"""Deploy canonical files with reversible backups and no source deletion."""

from __future__ import annotations

import argparse
import json
import os
import shutil
from datetime import datetime, timezone
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
DEFAULT_HOME = Path.home()
INSTRUCTIONS = {
    ".codex/AGENTS.md": REPO / "AGENTS.md",
    ".gemini/GEMINI.md": REPO / "AGENTS.md",
    ".claude/CLAUDE.md": REPO / "AGENTS.md",
    ".grok/rules/00-agent-system.md": REPO / "AGENTS.md",
    ".gemini/config/hooks.json": REPO / "adapters/hooks/agy.json",
}
SETTING_MERGES = {
    ".claude/settings.json": (REPO / "adapters/hooks/claude.json", ("hooks",)),
    ".gemini/settings.json": (REPO / "adapters/hooks/gemini.json", ("context", "hooks")),
}
SKILL_ROOTS = (
    ".agents/skills",
    ".codex/skills",
    ".claude/skills",
    ".gemini/config/skills",
    ".grok/skills",
)
RETIRED_ALIASES = (
    "0-how-to-write-skills",
    "1-critical-chain-design",
    "2-hypothesis-eval-loop",
    "grill-with-docs",
    "pizdej-protocol",
    "tdd",
    "to-issues",
    "to-prd",
)
RETIRED_SKILLS = ("skill-creator", "writing-skills")


def targets(home: Path) -> list[tuple[Path, Path | None]]:
    result = [(home / target, source) for target, source in INSTRUCTIONS.items()]
    result.append((home / ".codex/hooks.json", REPO / "adapters/hooks/codex.json"))
    result.extend(
        (home / ".grok/hooks" / path.name, path)
        for path in sorted((REPO / "adapters/hooks/grok").glob("*.json"))
    )
    result.append((home / ".gemini/skills/find-skills", None))
    skills = [path for path in sorted((REPO / "skills").iterdir()) if path.is_dir()]
    external = json.loads((REPO / "sources.lock.json").read_text(encoding="utf-8"))["external_skills"]
    for root_name in SKILL_ROOTS:
        root = home / root_name
        result.extend((root / skill.name, skill) for skill in skills)
        result.extend((root / name, Path(path)) for name, path in sorted(external.items()))
        result.extend((root / alias, None) for alias in RETIRED_ALIASES)
        result.extend((root / name, None) for name in RETIRED_SKILLS)
    result.extend((home / ".claude/agents" / path.name, path) for path in sorted((REPO / "agents").glob("*.md")))
    for runtime in ("codex", "claude", "gemini"):
        result.extend(
            (home / f".{runtime}/hooks" / path.name, path)
            for path in sorted((REPO / "hooks" / runtime).iterdir()) if path.is_file()
        )
    return result


def backup_path(snapshot: Path, home: Path, target: Path) -> Path:
    return snapshot / "files" / target.relative_to(home)


def apply(home: Path, backup_root: Path, dry_run: bool) -> Path | None:
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    snapshot = backup_root / timestamp
    operations: list[dict[str, str | None]] = []
    for target, source in targets(home):
        if source is None and not target.exists() and not target.is_symlink():
            continue
        if source is not None and target.is_symlink() and target.resolve() == source.resolve():
            continue
        backup: Path | None = None
        if target.exists() or target.is_symlink():
            backup = backup_path(snapshot, home, target)
        operations.append({
            "kind": "retire" if source is None else "link",
            "target": str(target),
            "source": str(source) if source is not None else None,
            "backup": str(backup) if backup is not None else None,
        })
    for target_name, (adapter, keys) in SETTING_MERGES.items():
        target = home / target_name
        current = json.loads(target.read_text(encoding="utf-8")) if target.exists() else {}
        desired = json.loads(adapter.read_text(encoding="utf-8"))
        if all(current.get(key) == desired[key] for key in keys):
            continue
        backup = backup_path(snapshot, home, target) if target.exists() else None
        operations.append({
            "kind": "merge",
            "target": str(target),
            "source": str(adapter),
            "keys": list(keys),
            "backup": str(backup) if backup is not None else None,
        })
    for operation in operations:
        if operation["kind"] == "retire":
            print(f"retire {operation['target']}")
        elif operation["kind"] == "merge":
            print(f"merge settings into {operation['target']}")
        else:
            print(f"link {operation['target']} -> {operation['source']}")
    if dry_run:
        print(f"dry-run: {len(operations)} changes")
        return None
    if not operations:
        print("no changes")
        return None
    snapshot.mkdir(parents=True, exist_ok=True)
    manifest = {"version": 1, "home": str(home), "repo": str(REPO), "operations": operations}
    (snapshot / "rollback.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    for operation in operations:
        target = Path(operation["target"])
        source = Path(operation["source"]) if operation["source"] else None
        backup = Path(operation["backup"]) if operation["backup"] else None
        if backup is not None:
            backup.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(target), str(backup))
        if operation["kind"] == "link" and source is not None:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.symlink_to(source, target_is_directory=source.is_dir())
        elif operation["kind"] == "merge" and source is not None:
            current = json.loads(backup.read_text(encoding="utf-8")) if backup else {}
            desired = json.loads(source.read_text(encoding="utf-8"))
            for key in operation["keys"]:
                current[key] = desired[key]
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(json.dumps(current, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"snapshot: {snapshot}")
    return snapshot


def rollback(snapshot: Path) -> None:
    manifest = json.loads((snapshot / "rollback.json").read_text(encoding="utf-8"))
    home = Path(manifest["home"])
    for operation in reversed(manifest["operations"]):
        target = Path(operation["target"])
        source = Path(operation["source"]) if operation["source"] else None
        backup = Path(operation["backup"]) if operation["backup"] else None
        kind = operation.get("kind", "link" if source is not None else "retire")
        if kind == "merge":
            current = json.loads(target.read_text(encoding="utf-8")) if target.exists() else {}
            previous = json.loads(backup.read_text(encoding="utf-8")) if backup and backup.exists() else {}
            for key in operation.get("keys", ["hooks"]):
                if key in previous:
                    current[key] = previous[key]
                else:
                    current.pop(key, None)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(json.dumps(current, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            continue
        installed = source is not None and target.is_symlink() and target.resolve() == source.resolve()
        if installed:
            target.unlink()
        if backup is not None and backup.exists():
            if target.exists() or target.is_symlink():
                drift = snapshot / "drift" / target.relative_to(home)
                drift.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(target), str(drift))
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(backup), str(target))
    print(f"rolled back: {snapshot}")


def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--dry-run", action="store_true")
    mode.add_argument("--apply", action="store_true")
    mode.add_argument("--rollback", type=Path)
    parser.add_argument("--home", type=Path, default=DEFAULT_HOME)
    parser.add_argument("--backup-root", type=Path)
    args = parser.parse_args()
    if args.rollback:
        rollback(args.rollback)
        return 0
    backup_root = args.backup_root or args.home / ".agent-system-backups"
    apply(args.home, backup_root, args.dry_run)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
