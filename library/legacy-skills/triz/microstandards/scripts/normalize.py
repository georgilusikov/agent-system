#!/usr/bin/env python3
"""Re-abstract existing micro-standards: convert specific examples to universal patterns."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import store
from models import Microstandard

PROXY_URL = "http://localhost:8318/v1"
MODEL = "gpt-5.4"

# Original 7 hand-crafted ones — already well abstracted, skip
SKIP_IDS = {
    "joint-size-reduction", "thread-protector", "fish-in-jar",
    "block-key-resource", "shah-or-donkey", "sour-grapes", "hide-in-crowd",
}


def normalize_one(ms: Microstandard) -> Microstandard:
    from openai import OpenAI
    client = OpenAI(base_url=PROXY_URL, api_key="proxy")

    response = client.chat.completions.create(
        model=MODEL,
        temperature=0.2,
        messages=[{
            "role": "user",
            "content": f"""Улучши формулировку микростандарта ТРИЗ: сделай её универсальной, применимой в разных областях.

ТЕКУЩАЯ ФОРМУЛИРОВКА:
Название: {ms.name}
Если: {ms.situation}
То: {ms.resolution}
Пример: {ms.example}

ПРОБЛЕМА: situation и resolution слишком привязаны к конкретному примеру.

ПРАВИЛО: situation/resolution должны описывать КЛАСС задач (не упоминать конкретные объекты из примера — торф, суда, страны, компании). Конкретика — только в "example".

Хорошие образцы:
- "Если нужно скрыть объект, но прямое укрытие невозможно → То разместить среди похожих объектов" (не "если нужно спрятать флягу на полке с флягами")
- "Если нужно создать спрос у людей, не осознающих потребность → То бесплатно отдать часть системы" (не "если нужно продать корм для рыб")

Верни JSON с улучшенными полями (остальные оставь как есть):
{{
  "id": "{ms.id}",
  "name": "Краткое название паттерна (можно улучшить)",
  "domain": "{ms.domain}",
  "situation": "Если... (универсальный класс ситуаций)",
  "resolution": "То... (универсальная рекомендация)",
  "constraints": "Типичные ограничения или null",
  "resources": "Типичные ресурсы или null",
  "example": "Исходный пример + ещё 1-2 из других областей через точку с запятой",
  "tags": {json.dumps(ms.tags, ensure_ascii=False)},
  "source": {json.dumps(ms.source, ensure_ascii=False)}
}}

Отвечай ТОЛЬКО JSON без пояснений.""",
        }]
    )

    raw = response.choices[0].message.content.strip()
    start, end = raw.find("{"), raw.rfind("}") + 1
    data = json.loads(raw[start:end])
    return Microstandard(**data)


def main() -> None:
    items = store.load_all()
    to_normalize = [ms for ms in items if ms.id not in SKIP_IDS]
    print(f"Нормализую {len(to_normalize)} микростандартов...\n")

    updated = 0
    for i, ms in enumerate(to_normalize, 1):
        print(f"[{i}/{len(to_normalize)}] {ms.name}", end="  ", flush=True)
        try:
            normalized = normalize_one(ms)
            # Replace in the list
            for j, item in enumerate(items):
                if item.id == ms.id:
                    items[j] = normalized
                    break
            updated += 1
            print(f"✓  →  {normalized.name}")
        except Exception as e:
            print(f"✗ {e}")

    store.save_all(items)
    print(f"\n✅ Обновлено: {updated} микростандартов")
    print(f"   Итого в базе: {len(items)}")


if __name__ == "__main__":
    main()
