#!/usr/bin/env python3
"""Disposable regression check for installer deployment-parent escapes."""

from __future__ import annotations

import json
import hashlib
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

        invalid_home = root / "invalid-home"
        invalid_home.mkdir()
        invalid_backup = root / "invalid-backups"
        invalid_journal = root / "invalid-install-receipts.jsonl"
        invalid_journal.write_text("{not-json}\n", encoding="utf-8")
        result = run(
            "--apply",
            "--home",
            str(invalid_home),
            "--backup-root",
            str(invalid_backup),
            "--receipt-journal",
            str(invalid_journal),
            "--run-id",
            "run-invalid-install",
            "--task-id",
            "task-install",
        )
        assert result.returncode != 0
        assert not invalid_backup.exists()
        assert not (invalid_home / ".dsh" / "AGENTS.md").exists()

        explicit_home = root / "explicit-home"
        explicit_home.mkdir()
        explicit_backup = root / "explicit-backups"
        receipt_journal = root / "install-receipts.jsonl"
        result = run(
            "--apply",
            "--home",
            str(explicit_home),
            "--backup-root",
            str(explicit_backup),
            "--receipt-journal",
            str(receipt_journal),
            "--run-id",
            "run-install",
            "--task-id",
            "task-install",
        )
        assert result.returncode == 0
        snapshots = list(explicit_backup.glob("*/rollback.json"))
        assert snapshots
        records = [json.loads(line) for line in receipt_journal.read_text(encoding="utf-8").splitlines()]
        assert [record["operation"] for record in records] == ["install.apply"]
        apply_receipt = records[0]
        rollback_manifest_hash = hashlib.sha256(snapshots[0].read_bytes()).hexdigest()
        assert apply_receipt["after_hash"] != rollback_manifest_hash

        missing_target = explicit_home / ".dsh" / "AGENTS.md"
        missing_target.unlink()
        result = run(
            "--apply",
            "--home",
            str(explicit_home),
            "--backup-root",
            str(explicit_backup),
            "--receipt-journal",
            str(receipt_journal),
            "--run-id",
            "run-install",
            "--task-id",
            "task-install",
        )
        assert result.returncode == 0
        assert len(list(explicit_backup.glob("*/rollback.json"))) == 1
        assert not missing_target.exists()
        records = [json.loads(line) for line in receipt_journal.read_text(encoding="utf-8").splitlines()]
        assert [record["operation"] for record in records] == ["install.apply"]

        missing_target.parent.mkdir(parents=True, exist_ok=True)
        missing_target.symlink_to(REPO / "AGENTS.md")
        blocked_rollback_journal = root / "blocked-rollback-receipts.jsonl"
        blocked_rollback_journal.with_name(f"{blocked_rollback_journal.name}.mode").write_text(
            "disabled\n", encoding="utf-8")
        protected_target = explicit_home / ".codex" / "AGENTS.md"
        assert protected_target.is_symlink()
        result = run(
            "--rollback",
            str(snapshots[0].parent),
            "--receipt-journal",
            str(blocked_rollback_journal),
            "--run-id",
            "run-install",
            "--task-id",
            "task-install",
        )
        assert result.returncode != 0
        assert protected_target.is_symlink()
        assert snapshots[0].is_file()

        result = run(
            "--rollback",
            str(snapshots[0].parent),
            "--receipt-journal",
            str(receipt_journal),
            "--run-id",
            "run-install",
            "--task-id",
            "task-install",
        )
        assert result.returncode == 0
        records = [json.loads(line) for line in receipt_journal.read_text(encoding="utf-8").splitlines()]
        assert [record["operation"] for record in records] == ["install.apply", "install.rollback"]
        rollback_receipt = records[1]
        assert rollback_receipt["before_hash"] == apply_receipt["after_hash"]

        missing_target.parent.mkdir(parents=True, exist_ok=True)
        missing_target.symlink_to(REPO / "AGENTS.md")
        result = run(
            "--rollback",
            str(snapshots[0].parent),
            "--receipt-journal",
            str(receipt_journal),
            "--run-id",
            "run-install",
            "--task-id",
            "task-install",
        )
        assert result.returncode == 0
        assert missing_target.is_symlink()
        records = [json.loads(line) for line in receipt_journal.read_text(encoding="utf-8").splitlines()]
        assert [record["operation"] for record in records] == ["install.apply", "install.rollback"]

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
