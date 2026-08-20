# 🔴 TRIZ Pizdej — Самокритика для TRIZ/DE-скиллов

> **Когда запускать:** После любого изменения в `_agent_shared/skills/triz/` или `_agent_shared/skills/forecasting/`.
> **Кто запускает:** Агент — автоматически после `@core-pizdej`, или вручную по триггеру `@triz_pizdej`.

---

## 0) Blast Radius Check (Радиус поражения)

Для КАЖДОГО изменённого файла ответь:

| Вопрос | Где проверять |
|---|---|
| Обновлён ли **Router Table** в `master_triz_orchestrator/core_instructions.md`? | § ROUTER TABLE + § КАРТА КОМПЕТЕНЦИЙ |
| Есть ли изменённый скилл в **workspace_router** (`.agent/workspace_router.md`)? | § Доступные skills |
| Есть ли скилл в **README.md** (`_agent_shared/skills/README.md`)? | Таблица всех скиллов |
| Есть ли дублирующая концепция в другом скилле (пример: `zrts` vs `dynamization`)? | grep по ключевому слову |
| Обновлён ли **triz_router** в Boris v5 (`boris_v5/config/triz_router.md`)? | § Phase routing |

---

## 1) Output Format ↔ Theory Sync

> **Паттерн ошибки:** Добавляешь Phase/Step в теорию, но не в OUTPUT FORMAT → агент проигнорирует.

Для каждого изменённого скилла проверь:
- [ ] Каждая новая Phase/Step отражена в `## OUTPUT FORMAT` (шаблон ответа)?
- [ ] Каждая новая Phase/Step имеет чек в `## Quality Gate`?
- [ ] Если есть `validators/gate_check.md` — он синхронизирован с inline Quality Gate?
- [ ] Есть ли **Reflection Gate** (2Q: CRITICAL + BLIND SPOT)? BLIND SPOT контекстуализирован под конкретный набор инструментов скилла?

---

## 1.5) Reflection Gate Template (Канонический шаблон)

> **Полный протокол:** см. `@reflection_gate` (`reflection_gate/core_instructions.md`) — standalone skill с картой контекстуализации для 14+ скиллов.
>
> **Каждый** skill с Output Format ДОЛЖЕН содержать эту секцию в конце шаблона, ПЕРЕД «➡️ Следующий шаг».
> BLIND SPOT обязательно конкретизируется под инструменты данного скилла (а не generic «что-то забыл»).

```markdown
### 🔍 Reflection Gate
- **CRITICAL (Самое слабое звено):** [Какой шаг/допущение в этом анализе — самый хрупкий? Что сломается первым?]
- **BLIND SPOT (Я не посмотрел):** [Какую область/ресурс/уровень я мог проигнорировать? Конкретно для инструментов ЭТОГО скилла]
```

**Примеры контекстуализации BLIND SPOT:**
- `@contradictions`: «Проверил ли я ТП на уровне надсистемы, а не только компонента?»
- `@resource_analysis`: «Проверил ли я ресурсы на микро-уровне (структура вещества)?»
- `@mmch`: «Человечки не превратились ли в абстракцию? Есть ли физический аналог?»
- `@zrts`: «Не применил ли я закон для неправильной стадии S-кривой?»

---

## 2) Handoff Integrity (Целостность передач)

- [ ] Каждый `→ @skill_name` в выводе и Next Step — ссылается на **существующий** скилл (не опечатка, не deprecated)?
- [ ] Если скилл передаёт «Full Task List» или «Веер ИКР» — принимающий скилл знает об этом формате?
- [ ] Если скилл ссылается на внешний файл (`bank_of_evolutionary_alternatives.md`, `metodolog_evolution_lines.md`) — файл существует и путь верный?

Быстрая проверка:
```bash
# Найти все handoff-ссылки
grep -rn "@[a-z_]*" _agent_shared/skills/triz/*/core_instructions.md | grep "→\|Next Step\|Передать\|handoff"
```

---

## 3) Cross-Reference Consistency

- [ ] Если konzept описан в 2+ файлах (пример: «Matching/Mismatching» в `dynamization` И `zrts`) — есть ли кросс-ссылка между ними?
- [ ] Если формула/таблица добавлена в Boris v5, есть ли зеркальное обновление в Elena (и наоборот)?
- [ ] Evolution Radar (`evolution_radar`) и ZRTS (`zrts`) — не дублируют ли одни и те же законы без ссылок?

---

## 4) Registry Freshness (Актуальность реестров)

| Реестр | Путь | Что проверить |
|---|---|---|
| Skills README | `_agent_shared/skills/README.md` | Все ли скиллы перечислены? |
| Workspace Router | `.agent/workspace_router.md` | Forecasting: boris_v5? TRIZ: evolution_radar? |
| TRIZ Orchestrator Skill Map | `master_triz_orchestrator/core_instructions.md` | Появляются ли новые скиллы в § КАРТА КОМПЕТЕНЦИЙ? |
| Boris v5 TRIZ Router | `boris_v5/config/triz_router.md` | Phase 1/4 routing актуален? |

---

## 5) Anti-Patterns (Что запрещено)

- ❌ **Theory-Only Injection:** Добавить Phase без обновления Output Format = мёртвый код.
- ❌ **SKILL.md-Only Fix:** Редактировать SKILL.md, но не core_instructions.md = агент не увидит.
- ❌ **Orphan Handoff:** `→ @skill_name`, но скилл не существует или не настроен принимать этот формат.
- ❌ **Registry Drift:** Добавить скилл в файловую систему, но не в README / workspace_router / orchestrator.
- ❌ **Dual Source of Truth:** Одна концепция описана в двух местах без cross-reference → рассинхрон неизбежен.

---

## 6) Quick Verification Script

```bash
# 1. Посчитать core_instructions vs README entries
echo "=== File system ===" && find _agent_shared/skills/triz/ -name "core_instructions.md" | wc -l
echo "=== README entries ===" && grep -c "\[.*\](triz/" _agent_shared/skills/README.md

# 2. Проверить что boris_v5 в workspace_router
grep "boris_v5" .agent/workspace_router.md

# 3. Проверить что все handoffs валидны
grep -roh "@[a-z_]*" _agent_shared/skills/triz/*/core_instructions.md | sort -u

# 4. Найти Skills без Quality Gate
for f in _agent_shared/skills/triz/*/core_instructions.md; do
  grep -qL "Quality Gate" "$f" && echo "NO GATE: $f"
done

# 5. Найти Skills без Reflection Gate (2Q: CRITICAL + BLIND SPOT)
for f in _agent_shared/skills/triz/*/core_instructions.md; do
  grep -qL "Reflection Gate" "$f" && echo "NO REFLECTION GATE: $f"
done
```
