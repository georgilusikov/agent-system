#!/usr/bin/env python3
"""Add or list micro-standards in the database."""
import json
import sys
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import store
from models import Microstandard


def cmd_list(domain: str | None) -> None:
    items = store.load_all()
    if not items:
        print("База пуста")
        return

    if domain:
        items = [ms for ms in items if ms.domain == domain]

    print(f"\n📚 Микростандарты в базе ({len(items)}):\n")
    by_domain: dict[str, list[Microstandard]] = {}
    for ms in items:
        by_domain.setdefault(ms.domain, []).append(ms)

    for dom, group in sorted(by_domain.items()):
        print(f"  [{dom.upper()}]")
        for ms in group:
            tags = f"  #{' #'.join(ms.tags)}" if ms.tags else ""
            print(f"    {ms.id} — {ms.name}{tags}")
        print()


def cmd_add_json(json_str: str) -> None:
    ms = Microstandard(**json.loads(json_str))
    store.add_one(ms)
    print(f"✅ Добавлен: {ms.name} [{ms.id}]")


def cmd_add_interactive() -> None:
    print("Добавление нового микростандарта\n")
    ms = Microstandard(
        id=input("ID (slug латиницей): ").strip(),
        name=input("Название (рус): ").strip(),
        domain=input("Область [engineering/business/psychology/universal]: ").strip(),
        situation=input("Если... (ситуация + ограничения): ").strip(),
        resolution=input("То... (рекомендация): ").strip(),
        constraints=input("Ограничения (Enter чтобы пропустить): ").strip() or None,
        resources=input("Ресурсы (Enter чтобы пропустить): ").strip() or None,
        example=input("Пример (Enter чтобы пропустить): ").strip() or None,
        tags=[t.strip() for t in input("Теги через запятую: ").split(",") if t.strip()],
        source=input("Источник (Enter чтобы пропустить): ").strip() or None,
    )
    store.add_one(ms)
    print(f"\n✅ Добавлен: {ms.name}")


def cmd_remove(ms_id: str) -> None:
    items = store.load_all()
    before = len(items)
    items = [ms for ms in items if ms.id != ms_id]
    if len(items) == before:
        print(f"ID '{ms_id}' не найден")
        return
    store.save_all(items)
    print(f"✅ Удалён: {ms_id}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Управление базой микростандартов")
    sub = parser.add_subparsers(dest="cmd")

    sub.add_parser("list").add_argument("--domain", help="Фильтр по области")
    p_add = sub.add_parser("add")
    p_add.add_argument("--json", dest="json_str", help="JSON строка с микростандартом")
    p_rm = sub.add_parser("remove")
    p_rm.add_argument("id", help="ID микростандарта для удаления")

    args = parser.parse_args()

    if args.cmd == "list":
        cmd_list(getattr(args, "domain", None))
    elif args.cmd == "add":
        if args.json_str:
            cmd_add_json(args.json_str)
        else:
            cmd_add_interactive()
    elif args.cmd == "remove":
        cmd_remove(args.id)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
