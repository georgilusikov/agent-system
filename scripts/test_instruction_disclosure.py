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
    # Outcome-first owner clarification raises the candidate budget, not repo gates.
    assert len(text.splitlines()) <= 100
    assert text.index("## Shorter route") < text.index("## Load when needed")
    policy = text.split("## Shorter route", 1)[1].split("## Authorization", 1)[0]
    assert policy.index("Point B first") < policy.index("Route second") < policy.index("Function when needed")
    for rule in ["requested purpose and final observable state B", "separate that end from assumed means",
                 "explicit deliverables, success metrics, mandatory methods, and safety",
                 "never optimize a proxy instead of B", "Infer from context",
                 "ask only if unresolved uncertainty changes the chosen route",
                 "seek the fastest viable path to the same B", "avoid new work", "ready open source/CLI/services",
                 "end-to-end delivery time (setup/adoption/integration included)", "total maintenance burden",
                 "Bound primary-source search to plausible reuse", "verify capability/runtime/license fit",
                 "first sufficient short route", "B may be expressed as IKR when useful",
                 "not a mandatory framework pass",
                 "during route comparison, only when identifying reusable mechanisms requires it",
                 "action → object → measurable effect", "functional analogues, including other domains",
                 "smallest test in local conditions", "Exact trivial transformations/calculations",
                 "material method changes in one line", "goal stays optional until the owner approves",
                 "assumed expensive means, the wrong task", "point-B ideality without extra intervention",
                 "conditional function clarification / functional analogue search",
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
