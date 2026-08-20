import json
from pathlib import Path

from models import Microstandard

DATA_FILE = Path(__file__).parent.parent / "data" / "microstandards.json"


def load_all() -> list[Microstandard]:
    if not DATA_FILE.exists():
        return []
    data = json.loads(DATA_FILE.read_text(encoding="utf-8"))
    return [Microstandard(**item) for item in data]


def save_all(items: list[Microstandard]) -> None:
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    DATA_FILE.write_text(
        json.dumps([m.model_dump() for m in items], ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def add_one(ms: Microstandard) -> None:
    items = load_all()
    if any(item.id == ms.id for item in items):
        raise ValueError(f"ID '{ms.id}' уже существует в базе")
    items.append(ms)
    save_all(items)


def format_for_llm(items: list[Microstandard]) -> str:
    parts = []
    for ms in items:
        block = (
            f"[{ms.id}] {ms.name} ({ms.domain})\n"
            f"Если: {ms.situation}\n"
            f"То: {ms.resolution}"
        )
        if ms.example:
            block += f"\nПример: {ms.example}"
        parts.append(block)
    return "\n\n---\n\n".join(parts)
