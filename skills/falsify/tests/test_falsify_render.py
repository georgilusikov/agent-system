#!/usr/bin/env python3
"""Тесты механического эмиттера таблиц /falsify (falsify_render.py).

Каждый тест = закреплённое правило SKILL.md (урок-как-assert), а не «проверка кода»:
падает тест → изменился контракт вывода, а не деталь реализации.

Запуск:
    python3 -m pytest ~/.claude/skills/falsify/tests/test_falsify_render.py -q
    python3 ~/.claude/skills/falsify/tests/test_falsify_render.py     # без pytest
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = SKILL_ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

import falsify_render as fr  # noqa: E402


def _expectation(code: str, label: str, **overrides) -> dict:
    base = {
        "id": f"{code} — {label}",
        "claim": "наблюдаемое утверждение об артефакте",
        "where": "Bash: команда и её stdout",
        "expected": "ok",
        "actual": "ok",
        "next_action_if_unmet": "починить и перезапустить прогон",
        "effort": 0,
        "actor": "agent",
    }
    base.update(overrides)
    return base


def _data(*expectations, **extra) -> dict:
    payload = {"hypothesis": "тестовый claim под фальсификацию", "expectations": list(expectations)}
    payload.update(extra)
    return payload


def _assert_raises(exc_type, fn, *args) -> Exception:
    try:
        fn(*args)
    except exc_type as caught:
        return caught
    raise AssertionError(f"ожидалось {exc_type.__name__}, исключения не было")


# ── 1. Валидный рендер: все пять секций канона на месте ───────────────────────
def test_valid_render_emits_all_canonical_sections():
    """SKILL.md Output Shape: §1, §3, §3.1, §9, §10 + строка FALSIFY_FINAL."""
    data = _data(
        _expectation("E01", "первое ожидание подтверждено прогоном"),
        _expectation("E02", "второе ожидание подтверждено прогоном"),
        _expectation("E03", "третье ожидание подтверждено прогоном"),
        next_actions=[{"id": "P01 — закрыть остаточный хвост работы", "closes": ["G01"],
                       "effort": 0, "actor": "agent", "why_first": "разблокирует релиз"}],
        confidence_before=60, confidence_after=90, confidence_reason="живой прогон",
    )
    md = fr.render(data)
    for section in ("## §1. Expectations table (E-ID)", "## §3. Gap table (G-ID)",
                    "### §3.1 Gap count", "## §9. Next-Action Digest", "## §10. Verdict"):
        assert section in md, f"нет секции {section}"
    assert "FALSIFY_FINAL:" in md, "нет строки FALSIFY_FINAL"
    assert "Уверенность: 60% → 90% — живой прогон" in md, "блок калибровки не отрендерен"


# ── 2. G00-ветка: gap=none всё равно даёт строку ──────────────────────────────
def test_no_gaps_still_emits_g00_row_and_zero_count():
    """SKILL.md §3: «Если gap = none — одна строка G00 — все ожидания met»."""
    md = fr.render(_data(
        _expectation("E01", "ожидание номер один подтверждено"),
        _expectation("E02", "ожидание номер два подтверждено"),
        _expectation("E03", "ожидание номер три подтверждено"),
    ))
    assert "G00 — все ожидания met" in md, "нет обязательной строки G00"
    assert "- total: 0" in md and "- highest severity: 0/5" in md, "G00 посчитан как настоящий gap"
    assert "FALSIFY_FINAL: PASS" in md, "все ожидания met, но verdict не PASS"


# ── 3. Critical блокирует PASS ───────────────────────────────────────────────
def test_critical_gap_forces_fail_even_with_majority_met():
    """SKILL.md §10 FORBIDDEN: «Verdict PASS при наличии critical gap = самообман»."""
    data = _data(
        _expectation("E01", "ожидание один подтверждено прогоном"),
        _expectation("E02", "ожидание два подтверждено прогоном"),
        _expectation("E03", "ожидание три подтверждено прогоном"),
        _expectation("E04", "критическое ожидание не выполнено", actual="сервис не отвечает",
                     severity="critical", gap_type="integration"),
    )
    md = fr.render(data)
    assert "FALSIFY_FINAL: FAIL" in md, "critical gap не опустил verdict до FAIL"
    assert "- highest severity: 5/5" in md, "critical не отражён в шкале severity"


# ── 4. Нет actual → NOT CHECKED, open, PASS невозможен ───────────────────────
def test_missing_actual_becomes_not_checked_and_caps_verdict():
    """SKILL.md §2.2: actual не наблюдался → NOT CHECKED, Verdict не может быть PASS.

    Явный `verdict: confirmed` при пустом actual НЕ спасает: подтверждать нечем.
    """
    data = _data(
        _expectation("E01", "ожидание один подтверждено прогоном"),
        _expectation("E02", "ожидание два подтверждено прогоном"),
        _expectation("E03", "ожидание без наблюдения актуального значения",
                     actual="", verdict="confirmed"),
    )
    md = fr.render(data)
    assert "NOT CHECKED" in md, "пустой actual не помечен NOT CHECKED"
    assert "FALSIFY_FINAL: PARTIAL" in md, "NOT CHECKED не опустил verdict ниже PASS"
    assert "PASS невозможен по §2.2" in md, "нет явной ссылки на правило §2.2"


# ── 5. Битый E-ID отклонён ───────────────────────────────────────────────────
def test_bare_e_id_without_label_is_rejected():
    """SKILL.md §1: «ID всегда с подписью через ' — ' (3-15 слов). E01 без подписи = невалидно»."""
    err = _assert_raises(fr.FalsifyInputError, fr.render, _data(
        _expectation("E01", "нормальная подпись ожидания здесь"),
        _expectation("E02", "нормальная подпись ожидания здесь"),
        dict(_expectation("E03", "x"), id="E03"),
    ))
    assert "E03" in str(err) and "подпис" in str(err), f"невнятное сообщение: {err}"
    # слишком короткая подпись (<3 слов) тоже невалидна
    short = _assert_raises(fr.FalsifyInputError, fr.render, _data(
        _expectation("E01", "нормальная подпись ожидания здесь"),
        _expectation("E02", "нормальная подпись ожидания здесь"),
        dict(_expectation("E03", "коротко"), id="E03 — коротко"),
    ))
    assert "3-15" in str(short), f"не проверена длина подписи: {short}"


# ── 6. Битый enum — ошибка, а не угадывание ──────────────────────────────────
def test_invalid_enum_raises_instead_of_guessing():
    """Правило владельца: невалидное значение → ошибка, не «догадка о намерении»."""
    for field, value in (("severity", "blocker"), ("gap_type", "process"),
                         ("waste", "bureaucracy"), ("actor", "team"), ("verdict", "maybe")):
        err = _assert_raises(fr.FalsifyInputError, fr.render, _data(
            _expectation("E01", "нормальная подпись ожидания здесь"),
            _expectation("E02", "нормальная подпись ожидания здесь"),
            _expectation("E03", "ожидание с битым перечислением значений",
                         actual="расхождение", **{field: value}),
        ))
        assert field in str(err) and value in str(err), f"{field}: невнятное сообщение — {err}"


# ── 7. JSON и YAML входы дают одинаковый вывод ───────────────────────────────
def test_json_and_yaml_inputs_render_identically():
    """Вход читается и как YAML, и как JSON (YAML — надмножество JSON)."""
    data = _data(
        _expectation("E01", "ожидание один подтверждено прогоном"),
        _expectation("E02", "ожидание два подтверждено прогоном"),
        _expectation("E03", "ожидание три не подтвердилось прогоном", actual="иначе",
                     severity="high", gap_type="execution"),
    )
    from_obj = fr.render(data)
    from_json = fr.render(fr._load(json.dumps(data, ensure_ascii=False)))
    assert from_obj == from_json, "JSON-вход рендерится иначе, чем объект"

    yaml_text = (
        "hypothesis: тестовый claim под фальсификацию\n"
        "expectations:\n"
        "  - id: \"E01 — ожидание один подтверждено прогоном\"\n"
        "    claim: наблюдаемое утверждение об артефакте\n"
        "    where: 'Bash: команда и её stdout'\n"
        "    expected: ok\n"
        "    actual: ok\n"
        "    next_action_if_unmet: починить и перезапустить прогон\n"
        "  - id: \"E02 — ожидание два подтверждено прогоном\"\n"
        "    claim: наблюдаемое утверждение об артефакте\n"
        "    where: 'Bash: команда и её stdout'\n"
        "    expected: ok\n"
        "    actual: ok\n"
        "    next_action_if_unmet: починить и перезапустить прогон\n"
        "  - id: \"E03 — ожидание три не подтвердилось прогоном\"\n"
        "    claim: наблюдаемое утверждение об артефакте\n"
        "    where: 'Bash: команда и её stdout'\n"
        "    expected: ok\n"
        "    actual: иначе\n"
        "    severity: high\n"
        "    gap_type: execution\n"
        "    next_action_if_unmet: починить и перезапустить прогон\n"
    )
    try:
        import yaml  # noqa: F401
    except ImportError:  # PyYAML нет → YAML-ветка недоступна, JSON-ветка уже проверена
        return
    from_yaml = fr.render(fr._load(yaml_text))
    assert "| E03 |" in from_yaml and "- total: 1" in from_yaml, "YAML-вход разобран неверно"


# ── 8. Подстрочная защита ────────────────────────────────────────────────────
def test_substring_is_not_a_match():
    """«0 open» ⊂ «30 open» — подстрока НЕ подтверждение (false-positive прототипа)."""
    md = fr.render(_data(
        _expectation("E01", "ожидание один подтверждено прогоном"),
        _expectation("E02", "ожидание два подтверждено прогоном"),
        _expectation("E03", "открытых пулл-реквестов не осталось",
                     expected="0 open", actual="30 open", severity="high"),
    ))
    assert "| E03 |" in md, "подстрочный false-positive: «0 open» засчитан как «30 open»"
    assert "- total: 1" in md, "gap не попал в счётчик"


# ── 9. Явный verdict строки выигрывает у сравнения строк ─────────────────────
def test_explicit_row_verdict_beats_string_comparison():
    """Истину строки определяет агент: строгое сравнение — только страховка."""
    md = fr.render(_data(
        _expectation("E01", "ожидание один подтверждено прогоном"),
        _expectation("E02", "ожидание два подтверждено прогоном"),
        _expectation("E03", "дерево показано плюс вскрыт дрейф",
                     expected="дерево показано", actual="дерево показано + drift вскрыт",
                     verdict="confirmed"),
    ))
    assert "G00 — все ожидания met" in md, "явный verdict=confirmed проиграл сравнению строк"


# ── 10. Gap count сходится арифметически ─────────────────────────────────────
def test_gap_count_arithmetic_matches_rows():
    """SKILL.md §3.1: счётчик обязан сходиться с числом строк §3 (total = open+partial+closed)."""
    data = _data(
        _expectation("E01", "ожидание один подтверждено прогоном"),
        _expectation("E02", "первое расхождение с ожиданием зафиксировано", actual="не то",
                     severity="high"),
        _expectation("E03", "второе расхождение с ожиданием зафиксировано", actual="",
                     severity="low"),
        gaps=[{"e_ref": "E02", "status": "partial", "root_cause": "частично починено",
               "fix": "довести до конца"}],
    )
    md = fr.render(data)
    rows = [line for line in md.splitlines() if line.startswith("| G0")]
    assert len(rows) == 2, f"ожидалось 2 gap-строки, получено {len(rows)}"
    assert "- total: 2" in md and "- open: 1" in md and "- partial: 1" in md and "- closed: 0" in md, md


# ── 11. G-ID уникальны: автонумерация не наступает на явные gaps[] ───────────
def test_auto_gid_never_collides_with_explicit_one():
    """Регрессия: автонумерация выдавала G01 первому gap'у, а gaps[] — тот же G01 другому.

    Два одинаковых G-ID в §3 делают §9 «Closes gaps» неразрешимым.
    """
    md = fr.render(_data(
        _expectation("E01", "первое расхождение с ожиданием зафиксировано", actual="не то"),
        _expectation("E02", "второе расхождение с ожиданием зафиксировано", actual="не то"),
        _expectation("E03", "третье расхождение с ожиданием зафиксировано", actual="не то"),
        gaps=[{"e_ref": "E03", "id": "G01 — явно названный разрыв тут"}],
    ))
    codes = [line.split(" — ")[0].removeprefix("| ") for line in md.splitlines()
             if line.startswith("| G0")]
    assert len(codes) == len(set(codes)), f"дубликаты G-ID: {codes}"
    assert sorted(codes) == ["G01", "G02", "G03"], codes

    dup = _assert_raises(fr.FalsifyInputError, fr.render, _data(
        _expectation("E01", "первое расхождение с ожиданием зафиксировано", actual="не то"),
        _expectation("E02", "второе расхождение с ожиданием зафиксировано", actual="не то"),
        _expectation("E03", "третье расхождение с ожиданием зафиксировано", actual="не то"),
        gaps=[{"e_ref": "E01", "id": "G05 — первый явно названный разрыв"},
              {"e_ref": "E02", "id": "G05 — второй явно названный разрыв"}],
    ))
    assert "дубликат G-ID" in str(dup), dup


# ── 12. CLI: self-test и stdin ───────────────────────────────────────────────
def test_cli_self_test_and_stdin_roundtrip():
    """--self-test зелёный; stdin-режим печатает те же таблицы; битый вход → exit 2."""
    script = SCRIPTS / "falsify_render.py"
    smoke = subprocess.run([sys.executable, str(script), "--self-test"],
                           capture_output=True, text=True)
    assert smoke.returncode == 0, smoke.stderr
    assert "self-test passed" in smoke.stdout, smoke.stdout

    payload = json.dumps(_data(
        _expectation("E01", "ожидание один подтверждено прогоном"),
        _expectation("E02", "ожидание два подтверждено прогоном"),
        _expectation("E03", "ожидание три подтверждено прогоном"),
    ), ensure_ascii=False)
    piped = subprocess.run([sys.executable, str(script)], input=payload,
                           capture_output=True, text=True)
    assert piped.returncode == 0, piped.stderr
    assert "FALSIFY_FINAL: PASS" in piped.stdout, piped.stdout

    broken = subprocess.run([sys.executable, str(script)], input='{"hypothesis": "x"}',
                            capture_output=True, text=True)
    assert broken.returncode == 2, f"битый вход не дал exit 2: {broken.returncode}"
    assert "expectations" in broken.stderr, broken.stderr


# ── 13. Пример из examples/ рендерится ───────────────────────────────────────
def test_bundled_example_renders():
    """examples/emitter_input_example.yaml — живой контракт формата, должен рендериться."""
    example = SKILL_ROOT / "examples" / "emitter_input_example.yaml"
    if not example.exists():
        return
    md = fr.render(fr._load(example.read_text(encoding="utf-8")))
    assert "FALSIFY_FINAL:" in md and "## §1. Expectations table (E-ID)" in md, md[:400]


if __name__ == "__main__":
    failures = 0
    for name, fn in sorted(globals().items()):
        if not name.startswith("test_") or not callable(fn):
            continue
        try:
            fn()
        except Exception as exc:  # noqa: BLE001 — прямой запуск = мини-раннер
            failures += 1
            print(f"❌ {name}: {type(exc).__name__}: {exc}")
        else:
            print(f"✅ {name}")
    print(f"\n{'FAILED' if failures else 'PASSED'}: {failures} провал(ов)")
    raise SystemExit(1 if failures else 0)
