# Правила построения скиллов (Krasinsky R1-R15)

> Применять при создании или переработке любого скилла в `~/.claude/skills/`.
> Источник: обратный инжиниринг системы Ильи Красинского (`hypothesis-gap-falsification` skill + ai-prompts + стандарт 2.6).

**Главный принцип:** скилл — это **контракт** (обязательства по входу/процессу/выходу), а не documentation. Без всех элементов `Output MUST include` скилл считается невыполненным.

---

## R1. Frontmatter = контракт, не описание

`description` обязан содержать:
- `Use when <N условий>` — когда вызывать
- `Based on <теоретическая база>` — на чём основан (Gap Theory / 5 Whys / JTBD / Popper / Bayes / TRIZ)
- `Output MUST include: - <артефакт 1> - <артефакт 2> ...` — обязательные артефакты
- `Trigger phrases: "...", "..."` — русские + английские триггеры в кавычках

**Зачем:** агент читает description как обязательства по output, не как "что делает скилл".

---

## R2. Триггер-фразы на русском и английском

`"проверь гипотезу"`, `"опровергни"`, `"challenge this"`, `"show the gap"`.

**Зачем:** покрыть весь инпут. Языковой барьер = потерянный триггер.

---

## R3. Input Checklist с `[ ]` ДО работы

Скилл начинается с `## Input checklist` — чеклист `[ ]` preconditions. Если чего-то нет — агент останавливается и добирает данные.

**Пример:**
```markdown
## Input checklist
- [ ] Понятен конкретный claim или гипотеза
- [ ] Понятны слои проверки (repo / runtime / tests / external)
- [ ] 3-7 наблюдаемых ожиданий, не абстрактная цель
- [ ] Доступ к source-of-truth (не к памяти агента)
```

---

## R4. Build expected state FIRST (conditional)

Перед сбором фактов — выписать 3-7 **наблюдаемых ожиданий** в таблицу. Это критерии приёмки, а не пост-хок оправдание.

**Обязательно**, если skill:
- проверяет результат (`/check`, `/falsify`, QA / acceptance)
- исполняет протокол или workflow (`/go`, delivery / implementation)
- принимает решение между вариантами (`/triage`, prioritization / release decision)

**Не обязательно** для pure discovery skills, где ещё нет expected state:
- `/anti-bias`, `/brain-dump`, `/deep-research`, `/task-format`
- exploratory research / ideation / raw data sensemaking

Для discovery вместо Expected State допустимо `§1. Discovery frame`: что ищем, почему сейчас, source-of-truth, stop-criteria.

**Обязательные колонки:**

| E-ID — название | Что должно быть истинно | Где подтверждать | Next action if unmet | Actor | Effort (0-100) |

**Применяется в:** `/check`, `/falsify`, `/go`, `/triage`, любой QA / execution / decision skill.

**Зачем:** ломает ловушку "сделал → посмотрел → сказал всё ок".

---

## R5. Макрос «ID + человекочитаемое имя»

Везде в таблицах и в чате — код и подпись в одной ячейке через ` — ` (пробел, длинное тире, пробел). Подпись = **3-15 слов на русском**.

**Правильно:** `G01 — тикет не читается из same bead`
**Запрещено:** голый `G01` без подписи (кроме строки `Technical refs` для копипасты).

**Распространяется на:** `E-ID`, `G-ID` (gap), `P-ID` (priority), `H-ID` (hypothesis), тикеты (`pr-123 — короткий title`).

**Hard fail:** нарушение макроса = output не засчитан.

---

## R6. Обязательные колонки таблиц (conditional)

Таблицы в verify / execute / decision skills имеют фиксированный набор колонок, которые **нельзя пропускать**:

- `Next action if unmet` — что делать при провале (заполняется ДО сбора фактов, не после)
- `Effort (0-100)` или `Усилие человека (0-100)` — шкала, где любой клик owner = минимум 50
- `Actor (agent / owner / both)` — кто действует

Таблица без одной из них = **неполная** = output невалиден.

Для pure discovery skills эти колонки не обязательны, если таблица не является acceptance / gap / action таблицей. Тогда вместо `Next action if unmet` допустимы discovery-колонки: `Signal`, `Missing data`, `Counterexample`, `Stop criteria`, `Follow-up question`.

---

## R7. Precedent Scan обязателен

Перед design injection — поиск в `~/.claude/memory/incidents/` похожих симптомов / процессных сбоев / design injections.

**Если не найдено** — написать явно: `"Похожих инцидентов не найдено в ~/.claude/memory/incidents/"`.

**Зачем:** заставляет использовать базу знаний, не изобретать с нуля.

---

## R8. 5 Whys с fact-basis

Каждое "почему" обосновано **файлом / логом / коммитом / сообщением**, не догадкой.

**Правильно:** `Почему X? → потому что в tests/test_foo.py:42 мок возвращает None, а real API — объект (строка 118)`
**Запрещено:** `Почему X? → видимо, что-то с конфигурацией`

Продолжать до **процессной / системной** корневой причины — не останавливаться на поверхностной ошибке.

---

## R9. Минимум 3 альтернативные гипотезы

Для RCA и triage скиллов — таблица гипотез:

| Гипотеза | Факты за | Факты против | Вероятность (0.0-1.0) | Влияние (1-5) | Вердикт |

`Вердикт`: `accepted / rejected / needs-data`.

**Зачем (anti-bias):** принуждает не захлопнуться на первой версии.

---

## R10. Причинная цепочка из 5 звеньев

`Симптом → Промежуточная причина → Процессный дефект → Корневая причина → Design Injection`

Если веток несколько — явно выделить `primary chain` и `secondary chain`.

---

## R11. Blast radius перед фиксом

Таблица зон:

| Зона | Статус (не сломано / требует проверки / сломано) | Что проверить |

**Зачем:** фикс не должен раздувать scope. Проверить, что не задели соседнее.

---

## R12. Design injection point ≤ 50 символов

Формат: `{файл/скилл/правило} → {секция/шаг} → {что изменить}`

**Правильно:** `rca-incidents.md → §7.2 → убрать голый ID`
**Запрещено:** `поправить систему` / `улучшить документацию`

**Зачем:** принудительная конкретность.

---

## R13. Нумерованные секции §0, §1, §2…

Стабильные ID для cross-ref между скиллами: `см. falsify §4`, `шкала в rca-incidents §7.2`.

**Зачем:** эволюционный тормоз на рефактор ради рефактора. Если перенумеровать — другие скиллы сломаются.

---

## R14. FORBIDDEN + Hard fail

Каждый скилл **явно** объявляет:

- `## FORBIDDEN` — что никогда не должно появиться в output (голый ID без подписи, «всё ок» без таблицы, fact-free why)
- `## Hard fail` — условия, при которых output считается **неисполненным** (нет §1, таблица без Next action, <3 гипотез в /triage)

**Зачем:** агент не может "почти-выполнить" скилл.

---

## R15. Cross-ref между скиллами и стандартами

Shared definitions (шкалы, форматы, определения) лежат в **одном** скилле и цитируются из остальных.

`(см. falsify §1)`, `(шкала effort в rca-incidents §7.2; любой клик owner ≥ 50)`.

**Зачем:** скиллы — часть экосистемы, не самодостаточные артефакты.

---

## Мини-шаблон `SKILL.md` (base skeleton)

```markdown
---
name: skill-name
description: "Use when <условия>. Based on <теория>.
  Output MUST include:
    - <артефакт 1>
    - <артефакт 2>
    - verdict
    - Next-Action Digest
  Trigger phrases: \"<ru1>\", \"<ru2>\", \"<en1>\", \"<en2>\""
---

# Skill Name

## Назначение
<1 абзац: зачем нужен>

## When to Use
- "<триггер 1>"
- "<триггер 2>"

## Input checklist
- [ ] <precondition 1>
- [ ] <precondition 2>

## §0. Макрос «ID + имя» (ОБЯЗАТЕЛЬНО)
см. ~/.claude/skills/0-how-to-write-skills/references/skill-construction.md R5

## §1. Build expected state first
| E-ID — название | Что истинно | Где подтверждать | Next action if unmet | Actor | Effort (0-100) |
|---|---|---|---|---|---|

## §2. Gather actual evidence
1. repo / file
2. Precedent scan в ~/.claude/memory/incidents/ (R7)
3. runtime / logs

## §3-§N. <контент скилла>

## FORBIDDEN
- голый ID без подписи
- таблица без Next action if unmet
- «всё ок» без таблицы

## Hard fail
- отсутствует §1 Expected State
- таблица неполная
- <skill-specific>
```

---

## Pre-review Checklist (при создании/правке скилла)

- [ ] R1: frontmatter содержит `Output MUST include` + `Trigger phrases` с RU+EN?
- [ ] R3: есть `## Input checklist` с `[ ]`?
- [ ] R4 (для verify / execute / decision skills): есть `§1 Build expected state first` с таблицей? Для discovery есть `§1 Discovery frame`?
- [ ] R5: в примерах таблиц использован `ID — подпись`, не голый ID?
- [ ] R6: таблицы содержат `Next action if unmet` + `Effort (0-100)` + `Actor`?
- [ ] R7 (для RCA-скиллов): есть шаг precedent scan с fallback текстом?
- [ ] R9 (для RCA-скиллов): есть `§N Alt hypotheses` с min 3?
- [ ] R13: секции пронумерованы `§0, §1, §2…`?
- [ ] R14: есть явный `## FORBIDDEN` и `## Hard fail`?
- [ ] R15: shared definitions — это cross-ref, не копия?

**Если хоть один `[ ]` пуст — скилл не готов.**

---

## FORBIDDEN при написании скиллов

- Frontmatter без `Output MUST include`
- Скилл без `Input checklist`
- Verify-скилл без `Build expected state first`
- Таблицы без `Next action if unmet`
- Голые `G01` / `E03` / `P0` без подписи
- Секции без `§` нумерации
- Дубли shared definitions (вместо cross-ref)

## Hard fail — скилл считается непостроенным

- Нет `Output MUST include` в frontmatter
- Нет `FORBIDDEN` или `Hard fail` секций
- Skill >500 строк без progressive disclosure (разбить на references/)
- Нет RU+EN триггеров одновременно

---

## Когда применять

- Создание нового скилла в `~/.claude/skills/*`
- Рефакторинг существующего скилла
- Review сделанного skill-creator'ом скилла перед коммитом
- Проверка через `/skill-validator-krasinsky` (финальный гейт)
