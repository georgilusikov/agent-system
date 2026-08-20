#!/usr/bin/env python3
"""Batch extract micro-standards from NotebookLM TRIZ channel."""
import json
import sys
import subprocess
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import store
from models import Microstandard

NOTEBOOK_ID = "61055bf5-f2eb-4299-be00-d5105eb268e6"
PROXY_URL = "http://localhost:8318/v1"
MODEL = "gpt-5.4"

QUERIES = [
    ("transport-logistics",
     "Дай 8 примеров задач с решениями из видео, связанных с транспортом, логистикой, "
     "перевозками, навигацией. Для каждого: задача, ограничения, решение."),

    ("materials-chemistry",
     "Дай 8 примеров из материаловедения, химии, обработки поверхностей из видео. "
     "Для каждого: задача, ограничения, решение."),

    ("it-software",
     "Дай 8 примеров задач, которые можно применить в IT, программировании, проектировании систем. "
     "Для каждого: задача, ограничения, решение."),

    ("agriculture-food",
     "Дай 8 примеров из сельского хозяйства, пищевой промышленности, экологии из видео. "
     "Для каждого: задача, ограничения, решение."),

    ("energy-resources",
     "Дай 8 примеров из энергетики, ресурсосбережения, переработки из видео. "
     "Для каждого: задача, ограничения, решение."),

    ("construction-arch",
     "Дай 8 примеров из строительства, архитектуры, городского планирования из видео. "
     "Для каждого: задача, ограничения, решение."),

    ("military-strategy",
     "Дай 8 примеров военных хитростей, стратегических уловок, обмана противника из видео. "
     "Для каждого: задача, ограничения, решение."),

    ("education-pedagogy",
     "Дай 8 примеров из обучения, педагогики, передачи знаний, мотивации из видео. "
     "Для каждого: задача, ограничения, решение."),

    ("medicine-safety",
     "Дай 8 примеров из медицины, безопасности, спасения жизней из видео. "
     "Для каждого: задача, ограничения, решение."),

    ("manufacturing",
     "Дай 8 примеров из производства, автоматизации, контроля качества из видео. "
     "Для каждого: задача, ограничения, решение."),

    ("measurement-detection",
     "Дай 8 примеров задач измерения, обнаружения, диагностики из видео. "
     "Для каждого: задача, ограничения, решение."),

    ("contradictions-tricks",
     "Дай 8 самых хитрых примеров из видео, где решение было парадоксальным или "
     "противоречило здравому смыслу. Для каждого: задача, ограничения, решение."),
]


def query_notebooklm(question: str) -> str:
    result = subprocess.run(
        ["notebooklm", "ask", question],
        capture_output=True, text=True, timeout=300
    )
    output = (result.stdout or "").strip()
    if "Answer:" in output:
        output = output.split("Answer:", 1)[1].strip()
    lines = [
        l for l in output.splitlines()
        if not l.startswith("Conversation:")
        and not l.startswith("Resumed conversation:")
        and not l.startswith("Continuing conversation")
    ]
    return "\n".join(lines).strip()


def extract_batch(text: str, domain_hint: str) -> list[Microstandard]:
    from openai import OpenAI
    client = OpenAI(base_url=PROXY_URL, api_key="proxy")

    response = client.chat.completions.create(
        model=MODEL,
        temperature=0.2,
        max_tokens=4000,
        messages=[{
            "role": "user",
            "content": f"""Извлеки ВСЕ задачи-примеры из текста и преобразуй каждую в УНИВЕРСАЛЬНЫЙ микростандарт ТРИЗ.

Микростандарт = «Если [КЛАСС ситуаций + ограничения] → То [универсальная рекомендация]»

КРИТИЧЕСКИ ВАЖНО:
- situation и resolution описывают КЛАСС задач, применимый в разных областях
- НЕ упоминай конкретные объекты из примера (торф, суда, Финляндия) в situation/resolution
- Конкретика — ТОЛЬКО в поле "example"
- Паттерн должен быть применим минимум в 2-3 разных областях

Плохо: "Если нужно провести судно через шлюз..."
Хорошо: "Если нужно направить крупный объект в узком проходе без механического контакта..."

Подсказка по области: {domain_hint}

ТЕКСТ:
{text}

Верни JSON-массив (только задачи с конкретным решением):
[
  {{
    "id": "short-unique-slug",
    "name": "Название паттерна (рус, 3-5 слов)",
    "domain": "engineering|business|psychology|universal",
    "situation": "Если... (универсальный класс ситуаций + ограничения)",
    "resolution": "То... (универсальная рекомендация, применимая в разных областях)",
    "constraints": "Типичные ограничения класса задач или null",
    "resources": "Типичные ресурсы или null",
    "example": "Конкретный пример из источника + 1-2 из других областей через точку с запятой",
    "tags": ["тег1", "тег2"],
    "source": "ТРИЗ ДЛЯ ВСЕХ — YouTube канал"
  }}
]

Правила: формулировки УНИВЕРСАЛЬНЫЕ (класс задач), ID уникальный slug на латинице.
Отвечай ТОЛЬКО JSON-массивом без пояснений.""",
        }]
    )

    raw = response.choices[0].message.content.strip()
    start, end = raw.find("["), raw.rfind("]") + 1
    if start == -1:
        return []

    items = []
    for item in json.loads(raw[start:end]):
        try:
            items.append(Microstandard(**item))
        except Exception as e:
            print(f"  ⚠️  Пропускаю невалидный [{item.get('id','?')}]: {e}")
    return items


def main() -> None:
    # Ensure TRIZ notebook is active
    subprocess.run(["notebooklm", "use", NOTEBOOK_ID], capture_output=True)
    print(f"✓ Переключился на ноутбук ТРИЗД ЛЯ ВСЕХ")

    existing = store.load_all()
    existing_ids = {ms.id for ms in existing}
    print(f"Текущая база: {len(existing)} микростандартов\n")

    total_added = 0

    for i, (domain_hint, query) in enumerate(QUERIES, 1):
        print(f"{'='*60}")
        print(f"Запрос {i}/{len(QUERIES)} [{domain_hint}]")
        print(f"  {query[:100]}...")

        try:
            print("  📖 NotebookLM...", flush=True)
            answer = query_notebooklm(query)

            if len(answer) < 100:
                print(f"  ⚠️  Короткий ответ ({len(answer)} симв.), пропускаю")
                continue

            print(f"  ✓ Ответ: {len(answer)} символов")
            print(f"  🤖 Извлекаю микростандарты...", flush=True)

            batch = extract_batch(answer, domain_hint)
            print(f"  📋 Найдено: {len(batch)}")

            added_this = 0
            for ms in batch:
                # Deduplicate: make ID unique if needed
                base_id = ms.id
                suffix = 1
                while ms.id in existing_ids:
                    ms.id = f"{base_id}-{suffix}"
                    suffix += 1

                try:
                    store.add_one(ms)
                    existing_ids.add(ms.id)
                    total_added += 1
                    added_this += 1
                    print(f"    ✓ [{ms.domain}] {ms.name}")
                except Exception as e:
                    print(f"    ✗ {ms.id}: {e}")

            print(f"  → Добавлено: {added_this}")

            if i < len(QUERIES):
                print(f"  ⏳ Пауза 5 сек...")
                time.sleep(5)

        except subprocess.TimeoutExpired:
            print(f"  ✗ Таймаут NotebookLM")
        except Exception as e:
            print(f"  ✗ Ошибка: {e}")

    final = store.load_all()
    print(f"\n{'='*60}")
    print(f"✅ ГОТОВО!")
    print(f"   Добавлено новых: {total_added}")
    print(f"   Итого в базе: {len(final)} микростандартов")


if __name__ == "__main__":
    main()
