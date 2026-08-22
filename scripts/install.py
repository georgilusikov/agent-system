#!/usr/bin/env python3
"""Deploy canonical files with reversible backups and no source deletion."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import stat
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

if __package__:
    from .runtime_receipts import ReceiptContext, emit_change, file_hash, preflight
else:
    from runtime_receipts import ReceiptContext, emit_change, file_hash, preflight


REPO = Path(__file__).resolve().parents[1]
DEFAULT_HOME = Path.home()
INSTRUCTIONS = {
    ".dsh/AGENTS.md": REPO / "AGENTS.md",
    ".codex/AGENTS.md": REPO / "AGENTS.md",
    ".gemini/GEMINI.md": REPO / "AGENTS.md",
    ".claude/CLAUDE.md": REPO / "AGENTS.md",
    ".grok/rules/00-agent-system.md": REPO / "AGENTS.md",
    ".gemini/config/hooks.json": REPO / "adapters/hooks/agy.json",
}
SETTING_MERGES = {
    ".claude/settings.json": (REPO / "adapters/hooks/claude.json", ("hooks",)),
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
            and not path.name.startswith(("test-", "test_"))
        )
    return result


def backup_path(snapshot: Path, home: Path, target: Path) -> Path:
    return snapshot / "files" / target.relative_to(home)


def ensure_target_parent(home: Path, target: Path) -> None:
    try:
        target.parent.resolve().relative_to(home.resolve())
    except (OSError, RuntimeError, ValueError) as error:
        raise ValueError(f"deployment parent escapes --home: {target.parent}") from error


def ensure_target(home: Path, target: Path) -> None:
    ensure_target_parent(home, target)
    if not target.is_symlink():
        return
    try:
        target.resolve().relative_to(home.resolve())
    except (OSError, RuntimeError, ValueError) as error:
        raise ValueError(f"deployment target escapes --home: {target}") from error


def ensure_backup_root(home: Path, backup_root: Path, require_inside_home: bool) -> Path:
    if backup_root.is_symlink():
        raise ValueError(f"backup root must not be a symlink: {backup_root}")
    try:
        resolved = backup_root.resolve()
    except (OSError, RuntimeError) as error:
        raise ValueError(f"cannot resolve backup root: {backup_root}") from error
    if require_inside_home:
        try:
            resolved.relative_to(home.resolve())
        except (OSError, RuntimeError, ValueError) as error:
            raise ValueError(f"backup root escapes --home: {backup_root}") from error
    return resolved


def apply(home: Path, backup_root: Path, dry_run: bool,
          receipt_context: ReceiptContext | None = None) -> Path | None:
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    snapshot = backup_root / timestamp
    operations: list[dict[str, str | None]] = []
    for target, source in targets(home):
        ensure_target_parent(home, target)
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
        ensure_target(home, target)
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
    if receipt_context is not None and preflight(
            receipt_context, _deployment_event_id(receipt_context, "apply")) is not None:
        return None
    before_hash = _deployment_fingerprint(home, (Path(operation["target"]) for operation in operations))
    snapshot.mkdir(parents=True, exist_ok=True)
    manifest = {"version": 1, "home": str(home), "repo": str(REPO), "operations": operations}
    (snapshot / "rollback.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    for operation in operations:
        target = Path(operation["target"])
        if operation["kind"] == "merge":
            ensure_target(home, target)
        else:
            ensure_target_parent(home, target)
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
    after_hash = _deployment_fingerprint(home, (Path(operation["target"]) for operation in operations))
    if receipt_context is not None and before_hash != after_hash:
        emit_change(
            receipt_context,
            _deployment_event_id(receipt_context, "apply"),
            "install.apply",
            "class:installer-deployment",
            before_hash,
            after_hash,
            "applied",
        )
    print(f"snapshot: {snapshot}")
    return snapshot


def rollback(snapshot: Path, receipt_context: ReceiptContext | None = None) -> None:
    manifest = json.loads((snapshot / "rollback.json").read_text(encoding="utf-8"))
    home = Path(manifest["home"])
    if receipt_context is not None and preflight(
            receipt_context, _deployment_event_id(receipt_context, "rollback")) is not None:
        return
    affected_targets = tuple(Path(operation["target"]) for operation in manifest["operations"])
    before_hash = _deployment_fingerprint(home, affected_targets)
    for operation in manifest["operations"]:
        target = Path(operation["target"])
        if operation.get("kind", "link" if operation.get("source") else "retire") == "merge":
            ensure_target(home, target)
        else:
            ensure_target_parent(home, target)
    for operation in reversed(manifest["operations"]):
        target = Path(operation["target"])
        source = Path(operation["source"]) if operation["source"] else None
        backup = Path(operation["backup"]) if operation["backup"] else None
        kind = operation.get("kind", "link" if source is not None else "retire")
        if kind == "merge":
            ensure_target(home, target)
        else:
            ensure_target_parent(home, target)
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
    after_hash = _deployment_fingerprint(home, affected_targets)
    if receipt_context is not None and before_hash != after_hash:
        emit_change(
            receipt_context,
            _deployment_event_id(receipt_context, "rollback"),
            "install.rollback",
            "class:installer-deployment",
            before_hash,
            after_hash,
            "applied",
        )
    print(f"rolled back: {snapshot}")


def _deployment_event_id(context: ReceiptContext, operation: str) -> str:
    return f"deployment-{hashlib.sha256(f'{context.run_id}:{operation}'.encode()).hexdigest()}"


def _deployment_fingerprint(home: Path, targets_to_hash: Iterable[Path]) -> str:
    states = []
    for target in sorted((Path(target) for target in targets_to_hash), key=lambda path: str(path)):
        try:
            relative = str(target.relative_to(home))
        except ValueError as error:
            raise ValueError(f"deployment target is outside --home: {target}") from error
        try:
            target_stat = target.lstat()
        except FileNotFoundError:
            state = {"type": "absent"}
        else:
            if stat.S_ISLNK(target_stat.st_mode):
                state = {"type": "symlink", "target": os.readlink(target)}
            elif stat.S_ISREG(target_stat.st_mode):
                state = {"type": "file", "hash": file_hash(target)}
            elif stat.S_ISDIR(target_stat.st_mode):
                state = {"type": "directory"}
            else:
                state = {"type": "other"}
        states.append({"target": relative, "state": state})
    canonical = json.dumps(states, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--dry-run", action="store_true")
    mode.add_argument("--apply", action="store_true")
    mode.add_argument("--rollback", type=Path)
    parser.add_argument("--home", type=Path, default=DEFAULT_HOME)
    parser.add_argument("--backup-root", type=Path)
    parser.add_argument("--receipt-journal", type=Path)
    parser.add_argument("--run-id")
    parser.add_argument("--task-id")
    parser.add_argument("--bead-id")
    args = parser.parse_args()
    try:
        if args.receipt_journal and (not args.run_id or not (args.task_id or args.bead_id)):
            raise ValueError("--receipt-journal requires --run-id and --task-id or --bead-id")
        receipt_context = ReceiptContext(
            journal=args.receipt_journal,
            repo_root=REPO,
            run_id=args.run_id,
            actor="system",
            runtime="system",
            task_id=args.task_id,
            bead_id=args.bead_id,
        ) if args.receipt_journal else None
        if args.rollback:
            rollback(args.rollback, receipt_context)
            return 0
        backup_root = args.backup_root or args.home / ".agent-system-backups"
        backup_root = ensure_backup_root(
            args.home,
            backup_root,
            require_inside_home=args.backup_root is None,
        )
        apply(args.home, backup_root, args.dry_run, receipt_context)
    except ValueError as error:
        parser.error(str(error))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
