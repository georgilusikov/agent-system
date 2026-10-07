#!/usr/bin/env python3
"""Check instruction reachability and guards without deploying live aliases."""

import os
import re
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Callable

import install

REQUIRED = {
    "CODING_STANDARDS.md",
    "rules/operational/shared-task-protocol.md",
    "standards/operational/decision-alternatives-standard.md",
    "skills/reframing-problems/SKILL.md",
    "skills/triz/SKILL.md",
}


def read_documents(alias: Path) -> dict[str, str]:
    source = alias.resolve(strict=True)
    text = alias.read_text(encoding="utf-8")
    pointers = set(re.findall(r"`([^`]+\.md)`", text))
    assert REQUIRED <= pointers, "required root reference disappeared"
    return {name: (source.parent / name).read_text(encoding="utf-8")
            for name in REQUIRED}


def must_fail(check: Callable[[], object]) -> None:
    try:
        check()
    except (AssertionError, FileNotFoundError):
        return
    raise AssertionError("negative case unexpectedly passed")


def main() -> None:
    source = install.REPO / "AGENTS.md"
    text = source.read_text(encoding="utf-8")
    flat = " ".join(text.split())
    # Check routes first: retained guards are useful only if their documents load.
    for trigger in ["before modifying any file", "recording owner acceptance",
                    "revising accepted work", "updating canon", "code, documents, or config",
                    "after a correction, false completion, or recurrence",
                    "before read-only investigation, batch/long work",
                    "external, financial, or irreversible actions", "**Inspect and scale**"]:
        assert trigger in flat, trigger
    # Owner-added always-on shortcut policy raises this candidate budget, not repo gates.
    assert len(text.splitlines()) <= 90
    assert text.index("## Shorter route") < text.index("## Load when needed")
    for rule in ["Before each task", "requested outcome and fixed constraints",
                 "explicit deliverables, success metrics, mandatory methods, and safety",
                 "outcome already holds or can happen without new work", "installed tools",
                 "bounded primary-source search only when plausible reuse can improve the choice",
                 "otherwise compare existing resources/helpers, native features, stdlib, installed tools",
                 "end-to-end delivery time (including setup/adoption/integration)",
                 "total adoption + integration + maintenance effort", "verify capability/runtime/license fit",
                 "Prefer ready reuse when materially faster or less effort, with acceptable trade-offs",
                 "Stop at the first sufficient short route", "exact trivial transformations/calculations",
                 "material method changes in one line", "goal stays optional until the owner approves",
                 "assumed expensive means, hidden obstruction, or a cheaper route",
                 "useful function without added stages/components", "simplification, or contradiction",
                 "canon is available", "report absent canon; never invent it"]:
        assert rule in flat, rule
    assert "explicit owner instruction in the current task" in flat
    assert "Never weaken security, release, or quality gates" in flat
    assert "Keep private reasoning private" in flat
    assert "A timeout is unknown: inspect partial files, logs, and process state" in flat
    assert all(label in text for label in ["⚡ Лучше:", "🕳 Пробелы:", "✂️ Скоуп:"])
    aliases = {name: target for name, target in install.INSTRUCTIONS.items()
               if target == source}
    assert len(aliases) == 5, "installer instruction alias coverage changed"
    previous = Path.cwd()
    with TemporaryDirectory(prefix="instruction-disclosure-") as directory:
        home = Path(directory)
        unrelated = home / "unrelated"
        unrelated.mkdir()
        actual = {target: origin for target, origin in install.targets(home)
                  if origin == source}
        assert actual == {home / name: target for name, target in aliases.items()}
        os.chdir(unrelated)
        try:
            for alias, target in actual.items():
                alias.parent.mkdir(parents=True, exist_ok=True)
                alias.symlink_to(target)
                assert alias.read_text(encoding="utf-8") == text
                documents = read_documents(alias)
                assert all(documents.values())
                for name in REQUIRED:
                    must_fail(lambda: (alias.parent / name).read_text())
                    must_fail(lambda: Path(name).read_text())
            protocol = " ".join(documents["rules/operational/shared-task-protocol.md"].split())
            for guard in ["TARGET:", "NON-GOALS:", "STOP RECEIPT:", "at most five lines",
                          "three different failures", "ACCEPTED:", "REOPEN ONLY IF:",
                          "persist it only with owner approval", "offline/dry-run"]:
                assert guard in protocol, guard
            dangling = home / "dangling.md"
            dangling.symlink_to(home / "absent.md")
            must_fail(lambda: read_documents(dangling))
            missing = home / "AGENTS.md"
            missing.write_text(text, encoding="utf-8")
            must_fail(lambda: read_documents(missing))
            missing.write_text(text.replace("`CODING_STANDARDS.md`", "standards"), encoding="utf-8")
            must_fail(lambda: read_documents(missing))
        finally:
            os.chdir(previous)
    print("PASS: five installer aliases, unrelated cwd, and negative cases")


if __name__ == "__main__":
    main()
