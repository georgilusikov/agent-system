#!/usr/bin/env python3
"""Extract a new micro-standard from a solved problem description."""
import json
import sys
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import store
from models import Microstandard

PROXY_URL = "http://localhost:8318/v1"
MODEL = "gpt-5.4"


def extract(text: str, auto_save: bool = False) -> Microstandard | None:
    from openai import OpenAI
    client = OpenAI(base_url=PROXY_URL, api_key="proxy")

    response = client.chat.completions.create(
        model=MODEL,
        temperature=0.2,
        messages=[{
            "role": "user",
            "content": f"""Извлеки микростандарт из описания решённой задачи.

Микростандарт — это УНИВЕРСАЛЬНЫЙ паттерн, применимый в разных областях.
Формат: «Если [класс ситуаций + ограничения] → То [универсальная рекомендация]»

КРИТИЧЕСКИ ВАЖНО:
- situation/resolution описывают КЛАСС задач, а не конкретный пример
- Конкретный пример идёт только в поле "example"
- Паттерн должен быть применим хотя бы в 2-3 разных областях
- Не упоминай в situation/resolution конкретные объекты из примера (торф, суда, Финляндия)

Плохо: "Если нужно провести судно через шлюз без буксиров..."
Хорошо: "Если нужно направить крупный объект в узком проходе без механического контакта..."

ОПИСАНИЕ ЗАДАЧИ / РЕШЕНИЯ:
{text}

Верни JSON (строго):
{{
  "id": "short-slug-latinitsey",
  "name": "Название паттерна на русском (3-5 слов)",
  "domain": "engineering|business|psychology|universal",
  "situation": "Если... (универсальный класс ситуаций + ограничения)",
  "resolution": "То... (универсальная рекомендация, применимая в разных областях)",
  "constraints": "Типичные ограничения класса задач или null",
  "resources": "Типичные ресурсы или null",
  "example": "Конкретный пример из источника + ещё 1-2 из других областей",
  "tags": ["тег1", "тег2", "тег3"],
  "source": null
}}

Отвечай ТОЛЬКО JSON без пояснений.""",
        }],
    )

    raw = response.choices[0].message.content.strip()
    start, end = raw.find("{"), raw.rfind("}") + 1
    if start == -1:
        print("Не удалось извлечь микростандарт из текста")
        return None

    try:
        ms = Microstandard(**json.loads(raw[start:end]))
    except Exception as e:
        print(f"Ошибка парсинга: {e}\nОтвет LLM:\n{raw}")
        return None

    print("\n📋 Извлечённый микростандарт:")
    print(f"  ID:        {ms.id}")
    print(f"  Название:  {ms.name}")
    print(f"  Область:   {ms.domain}")
    print(f"  Если:      {ms.situation}")
    print(f"  То:        {ms.resolution}")
    if ms.constraints:
        print(f"  Огранич.:  {ms.constraints}")
    if ms.resources:
        print(f"  Ресурсы:   {ms.resources}")
    if ms.example:
        print(f"  Пример:    {ms.example}")
    if ms.tags:
        print(f"  Теги:      {', '.join(ms.tags)}")

    if auto_save:
        store.add_one(ms)
        print(f"\n✅ Сохранён в базу: {ms.id}")
    else:
        print("\nДобавить в базу? [y/N] ", end="", flush=True)
        if sys.stdin.readline().strip().lower() == "y":
            store.add_one(ms)
            print(f"✅ Сохранён: {ms.id}")
        else:
            print("Не сохранён")

    return ms


def main() -> None:
    parser = argparse.ArgumentParser(description="Извлечение микростандарта из текста")
    parser.add_argument("text", nargs="?", help="Описание решённой задачи")
    parser.add_argument("--save", action="store_true", help="Сохранить без подтверждения")
    args = parser.parse_args()

    if args.text:
        text = args.text
    else:
        print("Опишите решённую задачу (или вставьте текст из видео):", flush=True)
        text = sys.stdin.read().strip()

    if not text:
        parser.print_help()
        sys.exit(1)

    extract(text, args.save)


if __name__ == "__main__":
    main()
