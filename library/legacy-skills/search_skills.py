#!/usr/bin/env python3
"""
🔍 Skills Search Tool

Утилита для поиска навыков в INDEX.yaml по категориям, тегам и ключевым словам.

Использование:
    python search_skills.py --category product_business
    python search_skills.py --tag design
    python search_skills.py --keyword "api"
    python search_skills.py --list-all
"""

import yaml
import os
import sys
from pathlib import Path


class SkillsSearcher:
    def __init__(self, index_path: str):
        """Инициализация поисковика."""
        self.index_path = Path(index_path)
        self.index = self._load_index()

    def _load_index(self) -> dict:
        """Загрузка INDEX.yaml."""
        with self.index_path.open('r', encoding='utf-8') as f:
            return yaml.safe_load(f)

    def list_categories(self) -> None:
        """Вывести все категории."""
        print("📚 Доступные категории:\n")
        for cat_id, cat_data in self.index['categories'].items():
            name = cat_data['name']
            desc = cat_data['description']
            tags = ', '.join(cat_data.get('tags', []))

            # Подсчёт навыков в категории
            total_skills = self._count_skills_in_category(cat_data)

            print(f"🏷️  {cat_id}")
            print(f"   Название: {name}")
            print(f"   Описание: {desc}")
            print(f"   Теги: {tags}")
            print(f"   Навыков: {total_skills}")
            print()

    def _count_skills_in_category(self, cat_data: dict) -> int:
        """Подсчитать количество навыков в категории."""
        count = 0
        for subcat in cat_data.get('subcategories', {}).values():
            skills = subcat.get('skills', [])
            count += len(skills)
        return count

    def search_by_category(self, category_id: str) -> None:
        """Поиск по категории."""
        if category_id not in self.index['categories']:
            print(f"❌ Категория '{category_id}' не найдена")
            self.list_categories()
            return

        cat_data = self.index['categories'][category_id]
        print(f"📂 Категория: {cat_data['name']}")
        print(f"📝 {cat_data['description']}\n")

        for subcat_name, subcat_data in cat_data.get('subcategories', {}).items():
            print(f"  📋 {subcat_data['name']}")
            for skill in subcat_data.get('skills', []):
                skill_path = self._get_skill_path(skill)
                print(f"     - {skill}")
                print(f"       📁 {skill_path}")
            print()

    def search_by_tag(self, tag: str) -> None:
        """Поиск по тегу."""
        print(f"🔍 Поиск по тегу: '{tag}'\n")

        found = False
        for cat_id, cat_data in self.index['categories'].items():
            tags = cat_data.get('tags', [])
            if tag in tags:
                found = True
                print(f"✅ {cat_data['name']} ({cat_id})")
                self._print_category_skills(cat_data)

        if not found:
            print(f"❌ Никто не использует тег '{tag}'")

    def search_by_keyword(self, keyword: str) -> None:
        """Поиск по ключевому слову."""
        print(f"🔍 Поиск по ключевому слову: '{keyword}'\n")

        found = False
        for cat_id, cat_data in self.index['categories'].items():
            for subcat_name, subcat_data in cat_data.get('subcategories', {}).items():
                for skill in subcat_data.get('skills', []):
                    if keyword.lower() in skill.lower():
                        found = True
                        print(f"✅ {skill}")
                        print(f"   Категория: {cat_data['name']}")
                        print(f"   Подкатегория: {subcat_data['name']}")
                        print(f"   📁 {self._get_skill_path(skill)}")
                        print()

        if not found:
            print(f"❌ Ничего не найдено по '{keyword}'")

    def _print_category_skills(self, cat_data: dict) -> None:
        """Вывести все навыки категории."""
        for subcat_data in cat_data.get('subcategories', {}).values():
            for skill in subcat_data.get('skills', []):
                print(f"   - {skill}")
        print()

    def _get_skill_path(self, skill_name: str) -> str:
        """Получить полный путь к навыку."""
        base_path = self._skill_base_path()
        return f"{base_path}/{skill_name}"

    def _skill_base_path(self) -> str:
        """Resolve the external reference library path."""
        env_path = os.environ.get("SKILLS_STUDY_LIBRARY")
        if env_path:
            return env_path

        external = Path.home() / "reference" / "skills_study_library"
        if external.exists():
            return str(external)

        fallback = self.index['metadata'].get('repo_local_fallback')
        return fallback or self.index['metadata']['skill_base_path']

    def generate_agent_config(self, skills: list[str]) -> None:
        """Сгенерировать конфиг для агента."""
        print("📝 Конфигурация для агента:\n")
        print("skills:")

        base_path = self._skill_base_path()

        for skill in skills:
            skill_path = f"{base_path}/{skill}"
            print(f"  - {skill_path}")

        print()

    def export_to_markdown(self, output_path: str) -> None:
        """Экспортировать INDEX.yaml в Markdown."""
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("# 📚 Skills Index - Полный каталог\n\n")
            f.write(f"**Дата:** {self.index['last_updated']}\n")
            f.write(f"**Всего навыков:** {self.index['metadata']['total_skills']}\n\n")
            f.write("---\n\n")

            for cat_id, cat_data in self.index['categories'].items():
                f.write(f"## {cat_data['name']} (`{cat_id}`)\n\n")
                f.write(f"{cat_data['description']}\n\n")
                f.write(f"**Теги:** {', '.join(cat_data.get('tags', []))}\n\n")

                for subcat_name, subcat_data in cat_data.get('subcategories', {}).items():
                    f.write(f"### {subcat_data['name']}\n\n")
                    for skill in subcat_data.get('skills', []):
                        f.write(f"- `{skill}`\n")
                    f.write("\n")

                f.write("---\n\n")

        print(f"✅ Экспортировано в {output_path}")


def main():
    """Главная функция."""
    index_path = Path(__file__).parent / "INDEX.yaml"

    if not index_path.exists():
        print(f"❌ INDEX.yaml не найден: {index_path}")
        sys.exit(1)

    searcher = SkillsSearcher(index_path)

    # Обработка аргументов командной строки
    if len(sys.argv) < 2:
        print("Использование:")
        print("  python search_skills.py --list-all")
        print("  python search_skills.py --category <category_id>")
        print("  python search_skills.py --tag <tag>")
        print("  python search_skills.py --keyword <word>")
        print("  python search_skills.py --agent-config <skill1>,<skill2>")
        print("  python search_skills.py --export-md <output.md>")
        sys.exit(1)

    arg = sys.argv[1]

    if arg == "--list-all":
        searcher.list_categories()

    elif arg == "--category" and len(sys.argv) > 2:
        searcher.search_by_category(sys.argv[2])

    elif arg == "--tag" and len(sys.argv) > 2:
        searcher.search_by_tag(sys.argv[2])

    elif arg == "--keyword" and len(sys.argv) > 2:
        searcher.search_by_keyword(sys.argv[2])

    elif arg == "--agent-config" and len(sys.argv) > 2:
        skills = sys.argv[2].split(',')
        searcher.generate_agent_config(skills)

    elif arg == "--export-md" and len(sys.argv) > 2:
        searcher.export_to_markdown(sys.argv[2])

    else:
        print("❌ Неверные аргументы")
        sys.exit(1)


if __name__ == "__main__":
    main()
