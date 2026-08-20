#!/usr/bin/env python3
"""Universal runner — ensures scripts run in the correct virtual environment."""
import os
import sys
import subprocess
from pathlib import Path


def get_venv_python() -> Path:
    venv_dir = Path(__file__).parent.parent / ".venv"
    if os.name == "nt":
        return venv_dir / "Scripts" / "python.exe"
    return venv_dir / "bin" / "python"


def ensure_venv() -> Path:
    skill_dir = Path(__file__).parent.parent
    venv_dir = skill_dir / ".venv"
    requirements = skill_dir / "requirements.txt"

    if not venv_dir.exists():
        print("🔧 Создаю виртуальное окружение...")
        subprocess.run([sys.executable, "-m", "venv", str(venv_dir)], check=True)
        venv_python = get_venv_python()
        subprocess.run([str(venv_python), "-m", "pip", "install", "-q", "-r", str(requirements)], check=True)
        print("✅ Окружение готово!")

    return get_venv_python()


def main() -> None:
    if len(sys.argv) < 2:
        print("Использование: python run.py <скрипт> [аргументы]\n")
        print("Доступные скрипты:")
        print("  search.py   — поиск микростандартов по описанию задачи")
        print("  extract.py  — извлечь микростандарт из текста/решения")
        print("  add.py      — управление базой (list/add/remove)")
        sys.exit(1)

    script_name = sys.argv[1]
    if not script_name.endswith(".py"):
        script_name += ".py"

    skill_dir = Path(__file__).parent.parent
    script_path = skill_dir / "scripts" / script_name

    if not script_path.exists():
        print(f"❌ Скрипт не найден: {script_name}")
        sys.exit(1)

    venv_python = ensure_venv()
    cmd = [str(venv_python), str(script_path)] + sys.argv[2:]

    try:
        result = subprocess.run(cmd)
        sys.exit(result.returncode)
    except KeyboardInterrupt:
        print("\n⚠️ Прервано")
        sys.exit(130)


if __name__ == "__main__":
    main()
