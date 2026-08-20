#!/usr/bin/env python3
"""Search micro-standards by problem description via LLM."""
import json
import sys
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import store
from models import SearchMatch

PROXY_URL = "http://localhost:8318/v1"
MODEL = "gpt-5.4"


def search(problem: str, top_n: int = 5) -> None:
    items = store.load_all()
    if not items:
        print("База пуста. Добавьте микростандарты через add.py")
        return

    from openai import OpenAI
    client = OpenAI(base_url=PROXY_URL, api_key="proxy")

    context = store.format_for_llm(items)

    response = client.chat.completions.create(
        model=MODEL,
        temperature=0.2,
        messages=[{
            "role": "user",
            "content": f"""Найди микростандарты из базы, которые подходят для решения задачи.

ЗАДАЧА ПОЛЬЗОВАТЕЛЯ:
{problem}

БАЗА МИКРОСТАНДАРТОВ:
{context}

Верни JSON-массив релевантных результатов (score >= 5), отсортированных по убыванию:
[{{"id": "...", "score": 1-10, "why": "кратко почему подходит"}}]

Включай только те, где есть реальная аналогия. Максимум {top_n}.
Отвечай ТОЛЬКО JSON-массивом без пояснений.""",
        }],
    )

    text = response.choices[0].message.content.strip()
    start, end = text.find("["), text.rfind("]") + 1
    if start == -1:
        print("Подходящих микростандартов не найдено")
        return

    try:
        results = [SearchMatch(**r) for r in json.loads(text[start:end])]
    except Exception as e:
        print(f"Ошибка парсинга ответа: {e}\nОтвет LLM: {text}")
        return

    if not results:
        print("Подходящих микростандартов не найдено")
        return

    ms_map = {ms.id: ms for ms in items}
    print(f"\n🔍 Найдено {len(results)} микростандартов:\n")
    for r in results:
        ms = ms_map.get(r.id)
        if not ms:
            continue
        print(f"{'─' * 60}")
        print(f"📌 [{r.score}/10]  {ms.name}  [{ms.domain}]")
        print(f"   Если: {ms.situation}")
        print(f"   То:   {ms.resolution}")
        if ms.example:
            print(f"   Пример: {ms.example}")
        print(f"   Почему: {r.why}")
    print()


def main() -> None:
    parser = argparse.ArgumentParser(description="Поиск микростандартов по задаче")
    parser.add_argument("problem", nargs="?", help="Описание задачи")
    parser.add_argument("-n", "--top", type=int, default=5, help="Сколько результатов")
    args = parser.parse_args()

    if args.problem:
        problem = args.problem
    else:
        print("Опишите задачу (ситуация + ограничения + ресурсы):", flush=True)
        problem = sys.stdin.read().strip()

    if not problem:
        parser.print_help()
        sys.exit(1)

    search(problem, args.top)


if __name__ == "__main__":
    main()
