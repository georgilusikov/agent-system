#!/usr/bin/env python3
"""Disposable regression check for installer deployment-parent escapes."""

from __future__ import annotations

import os
import subprocess
import tempfile
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
INSTALLER = REPO / "scripts" / "install.py"


def run(*arguments: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["python3", str(INSTALLER), *arguments],
        cwd=REPO,
        env={
            "PATH": os.environ["PATH"],
            "HOME": "/nonexistent-agent-system-test-home",
            "PYTHONDONTWRITEBYTECODE": "1",
        },
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="agent-system-install-") as root_name:
        root = Path(root_name)
        home = root / "home"
        outside = root / "outside"
        home.mkdir()
        outside.mkdir()
        sentinel = outside / "AGENTS.md"
        sentinel.write_text("outside sentinel\n", encoding="utf-8")
        (home / ".dsh").symlink_to(outside, target_is_directory=True)

        result = run("--apply", "--home", str(home), "--backup-root", str(root / "backups"))
        assert result.returncode != 0
        assert sentinel.is_file() and not sentinel.is_symlink()
        assert sentinel.read_text(encoding="utf-8") == "outside sentinel\n"
        assert (home / ".dsh").is_symlink()
        assert not (root / "backups").exists()

        default_home = root / "default-home"
        default_home.mkdir()
        default_outside = root / "default-outside"
        default_outside.mkdir()
        (default_home / ".agent-system-backups").symlink_to(default_outside, target_is_directory=True)
        result = run("--apply", "--home", str(default_home))
        assert result.returncode != 0
        assert not any(default_outside.iterdir())

        internal_home = root / "internal-home"
        internal_home.mkdir()
        internal_backup = internal_home / "real-backups"
        internal_backup.mkdir()
        (internal_home / ".agent-system-backups").symlink_to(internal_backup, target_is_directory=True)
        result = run("--apply", "--home", str(internal_home))
        assert result.returncode != 0
        assert not any(internal_backup.iterdir())

        explicit_home = root / "explicit-home"
        explicit_home.mkdir()
        explicit_backup = root / "explicit-backups"
        result = run(
            "--apply",
            "--home",
            str(explicit_home),
            "--backup-root",
            str(explicit_backup),
        )
        assert result.returncode == 0
        assert list(explicit_backup.glob("*/rollback.json"))

        linked_backup = root / "linked-backups"
        linked_backup.symlink_to(root / "linked-backups-target", target_is_directory=True)
        result = run(
            "--apply",
            "--home",
            str(explicit_home),
            "--backup-root",
            str(linked_backup),
        )
        assert result.returncode != 0
        assert not (root / "linked-backups-target").exists()
    print("PASS installer symlink escape rejected")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
