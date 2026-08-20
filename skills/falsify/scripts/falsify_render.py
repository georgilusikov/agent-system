#!/usr/bin/env python3
"""falsify_render.py — механический эмиттер канонических таблиц /falsify.

JTBD (owner): «агент стабильно не собирает таблицы руками». Корень — SKILL.md чисто
декларативный: §1/§3/§3.1/§9/§10 зависят от того, вспомнит ли агент их собрать и
не соврёт ли в арифметике (gap count, met N/M, PASS при critical). Этот скрипт делает
таблицы ДЕТЕРМИНИРОВАННЫМИ: на вход — YAML/JSON с гипотезой и ожиданиями, на выход —
markdown ровно того формата, что описан в SKILL.md, который агент вставляет ДОСЛОВНО.

Контракт формата — `~/.claude/skills/falsify/SKILL.md` (§1 Expectations table,
§3 Gap table, §3.1 Gap count, §9 Next-Action Digest, §10 Verdict + FALSIFY_FINAL).
Эталон вывода — `examples/golden_basic.md`.

Использование:
    python3 falsify_render.py input.yaml       # из файла (YAML или JSON)
    python3 falsify_render.py < input.yaml     # из stdin
    python3 falsify_render.py --self-test      # smoke без внешних зависимостей

Формат входа:
    hypothesis: "claim под фальсификацию одной фразой"
    expectations:                      # 3-7 по канону §1
      - id: "E01 — запуск одной командой"      # ОБЯЗАТЕЛЬНО «E01 — подпись 3-15 слов»
        claim: "что должно быть истинно (observable, не интерпретация)"
        where: "файл / команда / лог — SoT"
        expected: "ожидаемое значение"
        actual: "наблюдение; пусто → NOT CHECKED, verdict строки = open"
        verdict: confirmed              # опц.: confirmed/partial/open/falsified
        next_action_if_unmet: "конкретный шаг"
        effort: 0                       # 0-100
        actor: agent                    # agent / owner / both
        gap_type: execution             # knowledge/execution/feedback/integration
        waste: inventory                # 7 lean + '-'
        severity: high                  # low / med(medium) / high / critical
        root_cause: "одна строка"       # опц. — колонка Root Cause в §3
        fix: "что сделать"              # опц. — колонка Fix в §3
    gaps:                               # опц. — переопределение строк §3
      - e_ref: E04
        id: "G01 — traceback на отсутствующем файле"
        severity: high
        status: open                    # open / partial / closed
        root_cause: "..."
        fix: "..."
    next_actions:                       # опц. — §9
      - id: "P01 — обернуть чтение в except"    # «P01 — подпись 3-15 слов»
        closes: [G01]
        effort: 0
        actor: agent
        why_first: "снимает high-severity"
    confidence_before: 70               # опц. — блок калибровки §10
    confidence_after: 88
    confidence_reason: "4 живых прогона со stdout и exit code"

Правила, которые скрипт держит механически (см. SKILL.md):
  * E-ID / P-ID без « — подписи 3-15 слов» → ошибка валидации, не догадка.
  * Невалидный enum (verdict / gap_type / waste / severity / actor / status) → ошибка.
  * actual пуст → Actual = `NOT CHECKED`, verdict строки = open (это перебивает даже
    явный `verdict: confirmed`: наблюдения нет — подтверждать нечем), глобальный
    verdict в этом случае не может быть PASS.
  * Явный verdict строки выигрывает у сравнения строк; сравнение — ТОЧНОЕ равенство
    (подстрочная защита: «0 open» ⊄ «30 open» не считается совпадением).
  * §3 пуста → одна строка `G00 — все ожидания met` с обоснованием.
  * §3.1 Gap count считается из строк §3 (G00 = 0 gap'ов), severity → шкала /5.
  * §10: PASS только если met == все E-ID И 0 незакрытых critical; met ≥50% → PARTIAL;
    иначе FAIL. Любой незакрытый critical → FAIL независимо от met.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

try:
    import yaml  # type: ignore

    def _load(text: str) -> dict:
        return yaml.safe_load(text)
except Exception:  # pragma: no cover — PyYAML почти всегда есть; иначе принимаем JSON
    def _load(text: str) -> dict:
        return json.loads(text)


ROW_VERDICTS = ("confirmed", "partial", "open", "falsified")
GAP_STATUSES = ("open", "partial", "closed")
GAP_TYPES = ("knowledge", "execution", "feedback", "integration")
WASTE_TYPES = (
    "overproduction", "motion", "transportation", "inventory",
    "over-processing", "waiting", "defect", "-",
)
ACTORS = ("agent", "owner", "both")
SEVERITY_SCALE = {"low": 1, "med": 2, "medium": 2, "high": 3, "critical": 5}

NOT_CHECKED = "NOT CHECKED"
EMPTY = "—"

_ID_RE = re.compile(r"^(?P<code>[EPG]\d{2,3})\s+—\s+(?P<label>\S.*)$")


class FalsifyInputError(ValueError):
    """Невалидный вход: скрипт не угадывает, а падает с внятным сообщением."""


def _norm(value: object) -> str:
    return str(value if value is not None else "").strip()


def _cell(value: object, default: str = EMPTY) -> str:
    """Ячейка markdown-таблицы: пайпы экранированы, переводы строк схлопнуты."""
    text = _norm(value).replace("|", "\\|").replace("\n", " ")
    return text if text else default


def _parse_id(raw: object, prefix: str, position: int) -> tuple[str, str]:
    """`E01 — подпись 3-15 слов` → ('E01', 'подпись 3-15 слов'). Иначе — ошибка."""
    text = _norm(raw)
    if not text:
        raise FalsifyInputError(
            f"{prefix}-ID пуст в записи #{position}: нужен формат "
            f"«{prefix}01 — подпись 3-15 слов» (SKILL.md §1)"
        )
    match = _ID_RE.match(text)
    if not match or not match.group("code").startswith(prefix):
        raise FalsifyInputError(
            f"невалидный {prefix}-ID «{text}» (запись #{position}): нужен формат "
            f"«{prefix}01 — подпись 3-15 слов» через ' — '; "
            f"«{prefix}01» без подписи невалидно (SKILL.md §1)"
        )
    label = match.group("label").strip()
    words = len(label.split())
    if not 3 <= words <= 15:
        raise FalsifyInputError(
            f"подпись {prefix}-ID «{text}» содержит {words} слов, нужно 3-15 "
            f"(SKILL.md §1)"
        )
    return match.group("code"), label


def _enum(value: object, allowed: tuple, field: str, where: str, default: str | None = None) -> str:
    text = _norm(value).lower()
    if not text:
        if default is None:
            raise FalsifyInputError(f"{where}: поле `{field}` обязательно, ожидается одно из {list(allowed)}")
        return default
    if text not in allowed:
        raise FalsifyInputError(
            f"{where}: невалидное значение `{field}` = «{_norm(value)}»; "
            f"допустимо только {list(allowed)} (угадывание запрещено)"
        )
    return text


def _effort(value: object, where: str) -> int:
    text = _norm(value)
    if not text:
        return 0
    try:
        number = int(text)
    except ValueError as exc:
        raise FalsifyInputError(f"{where}: effort = «{text}» не целое число 0-100") from exc
    if not 0 <= number <= 100:
        raise FalsifyInputError(f"{where}: effort = {number} вне диапазона 0-100")
    return number


def row_verdict(expectation: dict, where: str) -> str:
    """Verdict строки: пустой actual → open; иначе явный verdict > точное сравнение."""
    actual = _norm(expectation.get("actual"))
    explicit = _enum(expectation.get("verdict"), ROW_VERDICTS, "verdict", where, default="")
    if not actual:
        # Наблюдения нет → §2.2 NOT CHECKED. Перебивает даже явный confirmed.
        return "open"
    if explicit:
        return explicit
    # Подстрочная защита: только ТОЧНОЕ равенство считается подтверждением.
    return "confirmed" if _norm(expectation.get("expected")) == actual else "open"


def _validate(data: object) -> dict:
    if not isinstance(data, dict):
        raise FalsifyInputError("вход должен быть маппингом (YAML/JSON объект) с ключами hypothesis + expectations")
    hypothesis = _norm(data.get("hypothesis"))
    if not hypothesis:
        raise FalsifyInputError("поле `hypothesis` обязательно: claim под фальсификацию одной фразой")

    raw_expectations = data.get("expectations")
    if not isinstance(raw_expectations, list) or not raw_expectations:
        raise FalsifyInputError("`expectations` обязателен и должен быть непустым списком (SKILL.md §1: 3-7 ожиданий)")

    expectations = []
    seen_codes = set()
    for position, item in enumerate(raw_expectations, 1):
        if not isinstance(item, dict):
            raise FalsifyInputError(f"expectations[{position}] должен быть маппингом")
        code, label = _parse_id(item.get("id"), "E", position)
        if code in seen_codes:
            raise FalsifyInputError(f"дубликат E-ID «{code}» в expectations[{position}]")
        seen_codes.add(code)
        where = f"expectations[{position}] ({code})"
        if not _norm(item.get("claim")):
            raise FalsifyInputError(f"{where}: поле `claim` обязательно (что должно быть истинно)")
        expectations.append({
            "code": code,
            "label": label,
            "claim": _norm(item.get("claim")),
            "where": _norm(item.get("where")),
            "expected": _norm(item.get("expected")),
            "actual": _norm(item.get("actual")),
            "verdict": row_verdict(item, where),
            "next_action_if_unmet": _norm(item.get("next_action_if_unmet")),
            "effort": _effort(item.get("effort"), where),
            "actor": _enum(item.get("actor"), ACTORS, "actor", where, default="agent"),
            "gap_type": _enum(item.get("gap_type"), GAP_TYPES, "gap_type", where, default="execution"),
            "waste": _enum(item.get("waste"), WASTE_TYPES, "waste", where, default="-"),
            "severity": _enum(item.get("severity"), tuple(SEVERITY_SCALE), "severity", where, default="med"),
            "root_cause": _norm(item.get("root_cause")),
            "fix": _norm(item.get("fix")),
        })

    if not 3 <= len(expectations) <= 7:
        print(
            f"falsify_render: предупреждение — ожиданий {len(expectations)}, "
            f"канон SKILL.md §1 требует 3-7",
            file=sys.stderr,
        )

    overrides = {}
    reserved_gids = set()          # G-ID, занятые явными gaps[] — автонумерация их пропускает
    raw_gaps = data.get("gaps") or []
    if not isinstance(raw_gaps, list):
        raise FalsifyInputError("`gaps` должен быть списком, если задан")
    for position, item in enumerate(raw_gaps, 1):
        if not isinstance(item, dict):
            raise FalsifyInputError(f"gaps[{position}] должен быть маппингом")
        where = f"gaps[{position}]"
        e_ref = _norm(item.get("e_ref"))
        if e_ref not in seen_codes:
            raise FalsifyInputError(
                f"{where}: `e_ref` = «{e_ref}» не найден среди E-ID {sorted(seen_codes)}"
            )
        gap = {"status": _enum(item.get("status"), GAP_STATUSES, "status", where, default="")}
        if _norm(item.get("id")):
            code, _ = _parse_id(item.get("id"), "G", position)
            if code in reserved_gids:
                raise FalsifyInputError(f"{where}: дубликат G-ID «{code}» — идентификаторы §3 обязаны быть уникальны")
            reserved_gids.add(code)
            gap["id"] = _norm(item.get("id"))
        for field in ("root_cause", "fix", "expected", "actual", "next_action_if_unmet"):
            if _norm(item.get(field)):
                gap[field] = _norm(item.get(field))
        if _norm(item.get("severity")):
            gap["severity"] = _enum(item.get("severity"), tuple(SEVERITY_SCALE), "severity", where)
        if _norm(item.get("gap_type")):
            gap["gap_type"] = _enum(item.get("gap_type"), GAP_TYPES, "gap_type", where)
        if _norm(item.get("waste")):
            gap["waste"] = _enum(item.get("waste"), WASTE_TYPES, "waste", where)
        if _norm(item.get("effort")):
            gap["effort"] = _effort(item.get("effort"), where)
        overrides[e_ref] = gap

    next_actions = []
    raw_actions = data.get("next_actions") or []
    if not isinstance(raw_actions, list):
        raise FalsifyInputError("`next_actions` должен быть списком, если задан")
    for position, item in enumerate(raw_actions, 1):
        if not isinstance(item, dict):
            raise FalsifyInputError(f"next_actions[{position}] должен быть маппингом")
        where = f"next_actions[{position}]"
        code, label = _parse_id(item.get("id"), "P", position)
        closes = item.get("closes") or []
        if isinstance(closes, str):
            closes = [part.strip() for part in closes.split(",") if part.strip()]
        if not isinstance(closes, list):
            raise FalsifyInputError(f"{where}: `closes` должен быть списком G-ID или строкой через запятую")
        next_actions.append({
            "code": code,
            "label": label,
            "closes": [_norm(x) for x in closes],
            "effort": _effort(item.get("effort"), where),
            "actor": _enum(item.get("actor"), ACTORS, "actor", where, default="agent"),
            "why_first": _norm(item.get("why_first")),
        })

    return {
        "hypothesis": hypothesis,
        "expectations": expectations,
        "gap_overrides": overrides,
        "reserved_gids": reserved_gids,
        "next_actions": next_actions,
        "no_gap_reason": _norm(data.get("no_gap_reason")),
        "confidence_before": _norm(data.get("confidence_before")),
        "confidence_after": _norm(data.get("confidence_after")),
        "confidence_reason": _norm(data.get("confidence_reason")),
    }


def _build_gap_rows(model: dict) -> list:
    """Строки §3: каждое неподтверждённое ожидание = один gap, нумерация сквозная."""
    rows = []
    taken = set(model["reserved_gids"])
    next_number = 1
    for expectation in model["expectations"]:
        if expectation["verdict"] == "confirmed":
            continue
        override = model["gap_overrides"].get(expectation["code"], {})
        gid = override.get("id")
        if not gid:
            while f"G{next_number:02d}" in taken:   # не наступаем на явные G-ID из gaps[]
                next_number += 1
            gid = f"G{next_number:02d} — {expectation['label']}"
            taken.add(f"G{next_number:02d}")
        status = override.get("status") or ("partial" if expectation["verdict"] == "partial" else "open")
        rows.append({
            "gid": gid,
            "e_ref": expectation["code"],
            "expected": override.get("expected") or expectation["expected"],
            "actual": override.get("actual") or expectation["actual"] or NOT_CHECKED,
            "gap_type": override.get("gap_type") or expectation["gap_type"],
            "severity": override.get("severity") or expectation["severity"],
            "waste": override.get("waste") or expectation["waste"],
            "root_cause": override.get("root_cause") or expectation["root_cause"],
            "fix": override.get("fix") or expectation["fix"],
            "next_action_if_unmet": override.get("next_action_if_unmet") or expectation["next_action_if_unmet"],
            "effort": override.get("effort", expectation["effort"]),
            "status": status,
        })
    return rows


def compute_verdict(model: dict, gap_rows: list) -> dict:
    """§10 Verdict по правилам SKILL.md — механически, без интерпретации."""
    expectations = model["expectations"]
    total = len(expectations)
    met = [e["code"] for e in expectations if e["verdict"] == "confirmed"]
    open_critical = [g for g in gap_rows if g["severity"] == "critical" and g["status"] != "closed"]
    not_checked = [e["code"] for e in expectations if not e["actual"]]

    if open_critical:
        verdict = "FAIL"                       # ≥1 незакрытый critical → FAIL всегда
    elif len(met) == total:
        verdict = "PASS"
    elif len(met) * 2 >= total:
        verdict = "PARTIAL"
    else:
        verdict = "FAIL"
    if verdict == "PASS" and not_checked:      # страховка: PASS невозможен при NOT CHECKED
        verdict = "PARTIAL"
    return {
        "verdict": verdict,
        "met": met,
        "total": total,
        "critical": len(open_critical),
        "not_checked": not_checked,
    }


def render(data: object) -> str:
    model = _validate(data)
    gap_rows = _build_gap_rows(model)
    summary = compute_verdict(model, gap_rows)
    out = []

    out.append(f"**Claim под фальсификацию:** {model['hypothesis']}")
    out.append("")

    # ── §1 Expectations table ────────────────────────────────────────────────
    out.append("## §1. Expectations table (E-ID)")
    out.append("")
    out.append("| E-ID — название | Что должно быть истинно | Где подтверждать (SoT) | Next action if unmet | Effort (0-100) |")
    out.append("|---|---|---|---|---|")
    for expectation in model["expectations"]:
        out.append(
            f"| {expectation['code']} — {expectation['label']} | {_cell(expectation['claim'])} "
            f"| {_cell(expectation['where'])} | {_cell(expectation['next_action_if_unmet'])} "
            f"| {expectation['effort']} |"
        )
    out.append("")

    # ── §3 Gap table ─────────────────────────────────────────────────────────
    out.append("## §3. Gap table (G-ID)")
    out.append("")
    out.append("| G-ID — название | E-ID ref | Expected | Actual | Gap type | Severity (low/med/high/critical) | Root Cause (1 строка) | Fix | Next action if unmet | Effort |")
    out.append("|---|---|---|---|---|---|---|---|---|---|")
    if not gap_rows:
        reason = model["no_gap_reason"] or "все E-ID подтверждены наблюдением, расхождений не найдено"
        out.append(
            f"| G00 — все ожидания met | {', '.join(summary['met'])} | {EMPTY} | {EMPTY} | {EMPTY} "
            f"| {EMPTY} | {_cell(reason)} | {EMPTY} | {EMPTY} | 0 |"
        )
    for row in gap_rows:
        out.append(
            f"| {_cell(row['gid'])} | {row['e_ref']} | {_cell(row['expected'])} | {_cell(row['actual'])} "
            f"| {row['gap_type']} | {row['severity']} | {_cell(row['root_cause'])} | {_cell(row['fix'])} "
            f"| {_cell(row['next_action_if_unmet'])} | {row['effort']} |"
        )
    out.append("")
    wastes = [f"{row['gid'].split(' — ')[0]}: {row['waste']}" for row in gap_rows if row["waste"] != "-"]
    if wastes:
        out.append(f"Waste (7 lean): {' · '.join(wastes)}")
        out.append("")

    # ── §3.1 Gap count ───────────────────────────────────────────────────────
    statuses = [row["status"] for row in gap_rows]
    highest = max([SEVERITY_SCALE[row["severity"]] for row in gap_rows], default=0)
    out.append("### §3.1 Gap count")
    out.append("")
    out.append("```text")
    out.append("Gap count")
    out.append(f"- total: {len(gap_rows)}")
    out.append(f"- open: {statuses.count('open')}")
    out.append(f"- partial: {statuses.count('partial')}")
    out.append(f"- closed: {statuses.count('closed')}")
    out.append(f"- highest severity: {highest}/5")
    out.append("```")
    out.append("")

    # ── §9 Next-Action Digest ────────────────────────────────────────────────
    if model["next_actions"]:
        out.append("## §9. Next-Action Digest")
        out.append("")
        out.append("| P-ID — шаг | Closes gaps (G-ID list) | Effort (0-100) | Actor | Зачем первый |")
        out.append("|---|---|---|---|---|")
        for action in model["next_actions"]:
            closes = ", ".join(action["closes"]) if action["closes"] else EMPTY
            out.append(
                f"| {action['code']} — {action['label']} | {_cell(closes)} | {action['effort']} "
                f"| {action['actor']} | {_cell(action['why_first'])} |"
            )
        out.append("")

    # ── §10 Verdict ──────────────────────────────────────────────────────────
    met_list = ", ".join(summary["met"]) if summary["met"] else "нет"
    out.append("## §10. Verdict")
    out.append("")
    out.append(
        f"**{summary['verdict']}** — met {len(summary['met'])}/{summary['total']} E-ID ({met_list}), "
        f"{summary['critical']} незакрытых critical, {len(gap_rows)} gap-строк."
    )
    out.append("")
    if summary["not_checked"]:
        out.append(
            f"NOT CHECKED (actual не наблюдался): {', '.join(summary['not_checked'])} → "
            f"PASS невозможен по §2.2."
        )
        out.append("")
    out.append("```text")
    if model["confidence_before"] and model["confidence_after"]:
        reason = model["confidence_reason"] or "причина не задана на входе"
        out.append(
            f"Уверенность: {model['confidence_before']}% → {model['confidence_after']}% — {reason}"
        )
    else:
        out.append(
            "Уверенность: НЕ ЗАДАНА — заполни confidence_before/confidence_after/"
            "confidence_reason во входе (Hard fail SKILL.md: калибровка обязательна)"
        )
    out.append("```")
    out.append("")
    if summary["verdict"] in ("PARTIAL", "FAIL"):
        out.append(
            "Напоминание (Hard fail SKILL.md): при PARTIAL/FAIL обязательны §10.5 новая "
            "рабочая гипотеза и §8 Design Injection, если gap в инструкциях."
        )
        out.append("")
    out.append("```text")
    out.append(f"FALSIFY_FINAL: {summary['verdict']}")
    out.append("```")
    return "\n".join(out)


# ── self-test ────────────────────────────────────────────────────────────────

_FIXTURE = {
    "hypothesis": "demo: эмиттер держит формат таблиц /falsify",
    "expectations": [
        {
            "id": "E01 — точное совпадение подтверждает",
            "claim": "рендер печатает три канонические таблицы",
            "where": "stdout скрипта",
            "expected": "3 таблицы", "actual": "3 таблицы",
            "next_action_if_unmet": "починить render()", "effort": 0, "actor": "agent",
        },
        {
            "id": "E02 — подстрока не считается совпадением",
            "claim": "открытых PR не осталось",
            "where": "gh pr list",
            "expected": "0 open", "actual": "30 open",
            "next_action_if_unmet": "закрыть PR по одному", "effort": 0, "actor": "agent",
            "gap_type": "execution", "waste": "inventory", "severity": "high",
            "root_cause": "ветки не мержились после ревью", "fix": "мерж-очередь по одной",
        },
        {
            "id": "E03 — пустой actual даёт NOT CHECKED",
            "claim": "владелец подтвердил раздачу",
            "where": "чат владельца",
            "expected": "approved",
            "verdict": "confirmed",
            "next_action_if_unmet": "запросить решение владельца", "effort": 60, "actor": "owner",
            "gap_type": "integration", "waste": "waiting", "severity": "med",
        },
        {
            "id": "E04 — явный verdict выигрывает у сравнения",
            "claim": "структура каталога показана владельцу",
            "where": "ls -R",
            "expected": "дерево показано", "actual": "дерево показано + drift вскрыт",
            "verdict": "confirmed",
            "next_action_if_unmet": "дочитать вывод ls", "effort": 0, "actor": "agent",
        },
    ],
    "next_actions": [
        {"id": "P01 — закрыть открытые PR очередью", "closes": ["G01"], "effort": 0,
         "actor": "agent", "why_first": "снимает high-severity gap"},
    ],
    "confidence_before": 60, "confidence_after": 85,
    "confidence_reason": "прогон эмиттера с показанным stdout",
}


def _self_test() -> int:
    md = render(_FIXTURE)

    assert "## §1. Expectations table (E-ID)" in md, "§1 отсутствует"
    assert "## §3. Gap table (G-ID)" in md, "§3 отсутствует"
    assert "### §3.1 Gap count" in md, "§3.1 отсутствует"
    assert "## §9. Next-Action Digest" in md, "§9 отсутствует"
    assert "## §10. Verdict" in md, "§10 отсутствует"
    assert "FALSIFY_FINAL: PARTIAL" in md, "FALSIFY_FINAL отсутствует или не PARTIAL"

    # gap count сходится: total == open+partial+closed == число gap-строк
    assert "- total: 2" in md and "- open: 2" in md, "gap count не сошёлся"
    assert "- highest severity: 3/5" in md, "highest severity посчитан неверно"

    # подстрочная защита: «0 open» ⊄ «30 open»
    assert "| E02 |" in md, "подстрочный false-positive: E02 не попал в gap table"
    # пустой actual → NOT CHECKED, явный confirmed не спасает
    assert NOT_CHECKED in md, "пустой actual не помечен NOT CHECKED"
    assert "PASS невозможен по §2.2" in md, "нет предупреждения про NOT CHECKED"
    # подтверждённое ожидание не течёт в §3 (в т.ч. по явному verdict)
    assert "| E01 |" not in md, "confirmed-ожидание протекло в gap table"
    assert "| E04 |" not in md, "явный verdict=confirmed не учтён (проиграл сравнению строк)"

    # PASS невозможен при critical
    critical = json.loads(json.dumps(_FIXTURE))
    critical["expectations"][1]["severity"] = "critical"
    summary = compute_verdict(_validate(critical), _build_gap_rows(_validate(critical)))
    assert summary["verdict"] == "FAIL", f"critical не заблокировал PASS: {summary}"

    # все confirmed → G00 + PASS
    clean = {"hypothesis": "всё met", "expectations": [
        {"id": f"E0{n} — ожидание номер {n} подтверждено", "claim": "c", "where": "w",
         "expected": "ok", "actual": "ok", "next_action_if_unmet": "n"} for n in (1, 2, 3)]}
    clean_md = render(clean)
    assert "G00 — все ожидания met" in clean_md, "G00 не отрендерен"
    assert "FALSIFY_FINAL: PASS" in clean_md, "все met, но не PASS"
    assert "- total: 0" in clean_md, "G00 посчитан как gap"

    print("✅ self-test passed (§1/§3/§3.1/§9/§10 + gap count + critical→FAIL + G00→PASS + NOT CHECKED)")
    return 0


def main(argv: list) -> int:
    if "--self-test" in argv:
        return _self_test()
    args = [a for a in argv[1:] if not a.startswith("--")]
    if args and args[0] != "-":
        text = Path(args[0]).read_text(encoding="utf-8")
    else:
        text = sys.stdin.read()
    if not text.strip():
        print(
            "usage: falsify_render.py <input.yaml> | falsify_render.py < input.yaml | --self-test",
            file=sys.stderr,
        )
        return 1
    try:
        data = _load(text)
        print(render(data))
    except FalsifyInputError as exc:
        print(f"falsify_render: невалидный вход — {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
