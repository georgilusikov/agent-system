#!/usr/bin/env python3
"""Build a content-only union manifest without following external symlinks."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import tempfile
from pathlib import Path
from typing import Any, Iterable


REPO = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG = REPO / "sources.json"
DEFAULT_OUTPUT = REPO / "migration" / "union-manifest.json"


CLASS_PATHS: dict[str, tuple[str, ...]] = {
    "agents": ("agents",),
    "instructions": ("AGENTS.md", "CLAUDE.md", "Claude.md", "GEMINI.md"),
    "skills": ("skills", "config/skills"),
    "hooks": ("hooks", "hooks.json"),
    "rules": ("rules",),
    "standards": ("standards",),
    "memory": ("memory", "memories"),
    "library": ("data", "lib", "scripts", "templates", "tools"),
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def is_denied(path: Path, config: dict[str, Any]) -> str | None:
    names = set(config["deny_names"])
    suffixes = tuple(config["deny_suffixes"])
    fragments = tuple(part.lower() for part in config["deny_fragments"])
    for part in path.parts:
        lowered = part.lower()
        if part in names:
            return f"deny-name:{part}"
    for part in path.parts[:-1]:
        lowered = part.lower()
        if any(fragment in lowered for fragment in fragments):
            return f"deny-fragment:{part}"
    if path.name.endswith(suffixes):
        return f"deny-suffix:{path.suffix}"
    return None


def candidate_paths(root: Path, classes: Iterable[str]) -> Iterable[tuple[str, Path]]:
    seen: set[Path] = set()
    for artifact_class in classes:
        for relative in CLASS_PATHS[artifact_class]:
            candidate = root / relative
            if not candidate.exists() and not candidate.is_symlink():
                continue
            if candidate in seen:
                continue
            seen.add(candidate)
            yield artifact_class, candidate


def disposition(source_id: str, artifact_class: str, relative: str) -> str:
    if artifact_class == "instructions":
        return "merge-core"
    if artifact_class == "skills":
        return "library-candidate" if source_id.startswith("shared-") else "active-candidate"
    if artifact_class in {"agents", "hooks", "memory", "library"}:
        return "review"
    if artifact_class in {"rules", "standards"}:
        return "migrate-candidate"
    return "review"


def scan(config: dict[str, Any], config_path: Path) -> dict[str, Any]:
    entries: list[dict[str, Any]] = []
    excluded: dict[str, int] = {}
    for source in config["allow"]:
        source_id = source["id"]
        root = Path(source["path"])
        if not root.exists():
            entries.append({
                "source": source_id,
                "source_root": str(root),
                "relative": ".",
                "type": "missing-root",
                "class": None,
                "disposition": "blocked",
            })
            continue
        for artifact_class, candidate in candidate_paths(root, source["classes"]):
            paths = [candidate]
            if candidate.is_dir() and not candidate.is_symlink():
                paths = sorted(candidate.rglob("*"))
            for path in paths:
                if path.is_dir() and not path.is_symlink():
                    continue
                relative_path = path.relative_to(root)
                denied = is_denied(relative_path, config)
                if denied:
                    excluded[denied] = excluded.get(denied, 0) + 1
                    continue
                row: dict[str, Any] = {
                    "source": source_id,
                    "source_root": str(root),
                    "relative": relative_path.as_posix(),
                    "class": artifact_class,
                    "mode": oct(path.lstat().st_mode & 0o777),
                }
                if path.is_symlink():
                    target = os.readlink(path)
                    row.update({
                        "type": "symlink",
                        "target": target,
                        "external": Path(target).is_absolute(),
                        "disposition": "external" if Path(target).is_absolute() else "alias-candidate",
                    })
                elif path.is_file():
                    row.update({
                        "type": "file",
                        "size": path.stat().st_size,
                        "sha256": sha256(path),
                        "disposition": disposition(source_id, artifact_class, relative_path.as_posix()),
                    })
                else:
                    continue
                entries.append(row)
    entries.sort(key=lambda row: (row["source"], row["relative"]))
    return {
        "version": 1,
        "source_config_sha256": sha256(config_path),
        "entry_count": len(entries),
        "excluded_counts": dict(sorted(excluded.items())),
        "entries": entries,
    }


def write_atomic(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(data, ensure_ascii=False, indent=2) + "\n"
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=path.parent, delete=False) as stream:
        stream.write(payload)
        temporary = Path(stream.name)
    temporary.replace(path)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    config = json.loads(args.config.read_text(encoding="utf-8"))
    data = scan(config, args.config)
    write_atomic(args.output, data)
    print(f"wrote {args.output}: {data['entry_count']} entries")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
