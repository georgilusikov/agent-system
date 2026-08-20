#!/usr/bin/env python3
"""Assemble the reviewed canonical tree from the source allowlist."""

from __future__ import annotations

import hashlib
import json
import shutil
import tempfile
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
HOME = Path.home()
SKILL_ROOTS = (HOME / ".agents/skills", HOME / ".codex/skills", HOME / ".claude/skills")
WINNERS = {"writing-plans": HOME / ".claude/skills/writing-plans"}
EXTERNAL = {"fusion": HOME / "Projects/fusion"}
EXCLUDED_ACTIVE = {
    "skill-creator": "incomplete and overridden by native vendor skill creators",
    "writing-skills": "depends on archived using-superpowers references; owner canon is how-to-write-skills",
}
DIR_NAMES = {
    "0-how-to-write-skills": "how-to-write-skills",
    "1-critical-chain-design": "critical-chain-design",
    "2-hypothesis-eval-loop": "hypothesis-eval-loop",
}
GENERIC_MEMORY = {
    "blind-eval-pairwise-beats-scale.md",
    "canon-purity-degrades-skill-output.md",
    "feedback_delegate_over_diy.md",
    "patterns.md",
    "project_skills_normalization_2026_07_09.md",
    "skill-examples-no-measured-effect.md",
    "skill-triggers-owner-language.md",
    "skills_consolidation_2026_07_10.md",
    "subagent-model-tiering.md",
    "worktrees_cleanup_2026_07_29.md",
}
TEXT_SUFFIXES = {".md", ".mdc", ".txt", ".json", ".yaml", ".yml", ".py", ".sh", ".js", ".html", ".css", ".dot"}


def tree_hash(root: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(root.rglob("*")):
        if path.is_file():
            digest.update(path.relative_to(root).as_posix().encode())
            digest.update(path.read_bytes())
    return digest.hexdigest()


def copy_tree(source: Path, target: Path, *extra_ignores: str) -> None:
    if target.exists():
        shutil.rmtree(target)
    shutil.copytree(source, target, symlinks=False, ignore=shutil.ignore_patterns(
        ".git", ".env", "__pycache__", ".pytest_cache", "*.pyc", "*.log", "*.lock", *extra_ignores
    ))


def backup_source(original: Path) -> Path:
    relative = original.relative_to(HOME)
    for root in sorted((HOME / ".agent-system-backups").glob("*/files"), reverse=True):
        candidate = root / relative
        if candidate.is_dir():
            return candidate
    return original


def normalize_text(root: Path) -> None:
    for path in root.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        normalized = "\n".join(line.rstrip() for line in text.splitlines()).rstrip() + "\n"
        path.write_text(normalized, encoding="utf-8")


def select_skills() -> tuple[dict[str, Path], list[dict[str, str]]]:
    lock_path = REPO / "sources.lock.json"
    if lock_path.exists():
        locked = json.loads(lock_path.read_text(encoding="utf-8"))["active_skills"]
        selected: dict[str, Path] = {}
        records: list[dict[str, str]] = []
        backups = sorted((HOME / ".agent-system-backups").glob("*/files"), reverse=True)
        for row in locked:
            name = row["name"]
            if name in EXCLUDED_ACTIVE:
                continue
            original = Path(row["source"])
            source = original
            if not source.is_dir() or REPO in source.resolve().parents:
                relative = original.relative_to(HOME)
                source = next((root / relative for root in backups if (root / relative).is_dir()), source)
            if not source.is_dir():
                raise SystemExit(f"locked skill source unavailable: {name}: {original}")
            selected[name] = source
            records.append({"name": name, "source": str(original), "sha256": tree_hash(source)})
        return selected, records

    candidates: dict[str, list[Path]] = {}
    for root in SKILL_ROOTS:
        for path in sorted(root.iterdir()):
            if path.name.startswith(".") or path.name in EXTERNAL or path.name in EXCLUDED_ACTIVE or not path.is_dir():
                continue
            candidates.setdefault(path.name, []).append(path.resolve())
    selected: dict[str, Path] = {}
    records: list[dict[str, str]] = []
    for name, paths in sorted(candidates.items()):
        unique = list(dict.fromkeys(paths))
        winner = WINNERS.get(name)
        if winner:
            source = winner.resolve()
        elif len({tree_hash(path) for path in unique}) == 1:
            source = unique[0]
        elif len(unique) == 1:
            source = unique[0]
        else:
            raise SystemExit(f"unresolved skill collision: {name}: {unique}")
        if not (source / "SKILL.md").is_file():
            raise SystemExit(f"skill has no SKILL.md: {name}: {source}")
        canonical_name = DIR_NAMES.get(name, name)
        if canonical_name in selected:
            raise SystemExit(f"canonical skill collision: {name} -> {canonical_name}")
        selected[canonical_name] = source
        records.append({"name": canonical_name, "source": str(source), "sha256": tree_hash(source)})
    return selected, records


def main() -> int:
    skills, records = select_skills()
    staged = Path(tempfile.mkdtemp(prefix="agent-system-skills-"))
    for name, source in skills.items():
        copy_tree(source, staged / name)
    if (REPO / "skills").exists():
        shutil.rmtree(REPO / "skills")
    shutil.move(str(staged), str(REPO / "skills"))

    triz = REPO / "skills/triz/SKILL.md"
    triz.write_text(triz.read_text(encoding="utf-8").replace(
        "**Канон-корень (`<T>` ниже):**\n`/Users/georgijlusikov/Documents/курсор/_agent_shared/skills/triz/`",
        "**Канон-корень (`<T>` ниже):** resolve this file's repository root, then use\n"
        "`library/legacy-skills/triz/`.",
    ), encoding="utf-8")
    meta = REPO / "skills/meta/SKILL.md"
    text = meta.read_text(encoding="utf-8")
    replacements = {
        "T  = /Users/georgijlusikov/Documents/курсор/_agent_shared/skills/triz": "R  = repository root containing this skill\nT  = R/library/legacy-skills/triz",
        "J  = /Users/georgijlusikov/Documents/курсор/_agent_shared/skills/jtbd": "J  = R/library/legacy-skills/jtbd",
        "CC = /Users/georgijlusikov/.claude/skills": "CC = R/skills",
        "AG = /Users/georgijlusikov/.claude/agents": "AG = R/agents",
        "/Users/georgijlusikov/.claude/skills/1-critical-chain-design/SKILL.md": "R/skills/critical-chain-design/SKILL.md",
        "/Users/georgijlusikov/.claude/skills/leverage/SKILL.md": "R/skills/leverage/SKILL.md",
        "/Users/georgijlusikov/.claude/agents/outcome-designer.md": "R/agents/outcome-designer.md",
        "/Users/georgijlusikov/.claude/skills/anti-bias/SKILL.md": "R/skills/anti-bias/SKILL.md",
        "/Users/georgijlusikov/.claude/skills/pizdej/SKILL.md": "R/skills/pizdej/SKILL.md",
        "/Users/georgijlusikov/.claude/skills/triz/SKILL.md": "R/skills/triz/SKILL.md",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    meta.write_text(text, encoding="utf-8")
    roadmap = REPO / "skills/roadmap-planning/SKILL.md"
    roadmap.write_text(roadmap.read_text(encoding="utf-8").replace(
        "When running this workflow as a guided conversation, use [`workshop-facilitation`](../workshop-facilitation/SKILL.md) as the interaction protocol.",
        "When running this workflow as a guided conversation, ask one focused question at a time.",
    ), encoding="utf-8")

    current = Path("/Users/georgijlusikov/Documents/курсор/_agent_shared")
    old = Path("/Users/georgijlusikov/code/cursor-workspace/_agent_shared")
    copy_tree(current / "skills", REPO / "library" / "legacy-skills", "tests")
    copy_tree(current / "rules", REPO / "library" / "legacy-rules")
    copy_tree(current / "standards", REPO / "standards" / "domain")
    copy_tree(HOME / ".claude/rules", REPO / "rules" / "operational")
    copy_tree(HOME / ".claude/standards", REPO / "standards" / "operational")
    copy_tree(backup_source(HOME / ".claude/agents"), REPO / "agents")
    copy_tree(backup_source(HOME / ".codex/hooks"), REPO / "hooks/codex")
    copy_tree(backup_source(HOME / ".claude/hooks"), REPO / "hooks/claude")
    adapters = REPO / "adapters/hooks"
    if not adapters.exists():
        adapters.mkdir(parents=True)
        for runtime, path in {
            "codex": HOME / ".codex/hooks.json",
            "claude": HOME / ".claude/settings.json",
            "gemini": HOME / ".gemini/settings.json",
        }.items():
            data = json.loads(path.read_text(encoding="utf-8"))
            (adapters / f"{runtime}.json").write_text(
                json.dumps({"hooks": data.get("hooks", {})}, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
        grok_adapters = adapters / "grok"
        grok_adapters.mkdir()
        for path in sorted((HOME / ".grok/hooks").glob("*.json")):
            shutil.copy2(path, grok_adapters / path.name)
    copy_tree(HOME / ".claude/memory/incidents", REPO / "memory" / "incidents")
    (REPO / "memory" / "learnings").mkdir(parents=True, exist_ok=True)
    for name in sorted(GENERIC_MEMORY):
        source = current / "memory" / name
        if source.is_file():
            shutil.copy2(source, REPO / "memory" / "learnings" / name)

    legacy_standard = old / "standards/agent-state-contract-standard.md"
    if legacy_standard.is_file():
        shutil.copy2(legacy_standard, REPO / "standards/domain" / legacy_standard.name)
    legacy_rule = old / "rules/agent-state-contracts.mdc"
    if legacy_rule.is_file():
        shutil.copy2(legacy_rule, REPO / "library/legacy-rules" / legacy_rule.name)
    copy_tree(old / "templates/agent-state-contract", REPO / "library/templates/agent-state-contract")

    lock = {
        "version": 1,
        "active_skills": records,
        "external_skills": {name: str(path) for name, path in EXTERNAL.items()},
        "excluded_active": EXCLUDED_ACTIVE,
        "legacy_library": str(current),
        "legacy_additions": str(old),
    }
    (REPO / "sources.lock.json").write_text(
        json.dumps(lock, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    for name in ("skills", "library", "rules", "standards", "memory", "hooks", "agents", "adapters"):
        normalize_text(REPO / name)
    print(f"imported {len(skills)} active skills; external: {', '.join(EXTERNAL)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
