# Verification Methods Standard

**Название:** Verification Methods — Cross-Check, Test-by-Change-Type, Failure Triage
**Класс:** micro
**Дата создания:** 2026-06-11
**Контекст:** generic-методы верификации (3-method cross-check, таксономия тестов по типу
изменения, разбор падающего теста) ранее лежали в `rules-validation-standard.md` §11-13, хотя
они **не про валидацию правил**, а про проверку любого результата. Вынесены в отдельный
micro-стандарт; в `rules-validation` оставлен cross-ref.

> **Связь с каноном.** Это таксономия методов. **Процесс** верификации (expected-state-first,
> positive/negative/edge, gap-таблица, negative space, калибровка) — в скилле `/check`
> (`_agent_shared/skills/dev/check/SKILL.md`). Верификация **данных** (схема + примеры) — в
> `research-data-standard.md`. Здесь — только методы; для «как проверять» зови `/check`.

---

## 1. 3-method cross-check

Любое утверждение «всё работает» должно опираться на ≥2 независимых метода. Эталонный набор из трёх:
1. **Manual file inspection** — открой артефакт лично, проверь содержимое.
2. **Automated test run** — запусти тест/квери, зафиксируй вывод.
3. **Compare with expected schema** — сверь с заранее зафиксированной схемой/golden.

Все 3 метода должны согласиться. Несогласие → gap analysis (см. `/check` §4), не «округление».

---

## 2. What to test by change type

| Слой | Что тестируем |
|---|---|
| Backend — Unit | чистая функция / класс изолированно |
| Backend — Integration | связь модулей + БД / внешний сервис |
| Backend — Contract | контракт API / схема ввода-вывода |
| Frontend — Component | компонент изолированно (props/state) |
| Frontend — User-Flow | путь пользователя через 2-3 экрана |
| Frontend — Visual | скриншот / визуальная регрессия |

---

## 3. When tests fail (worked example)

`TypeError: cannot read property 'x' of null` →
1. Анализ: объект приходит `null`, а код считает, что не-null.
2. Root cause: отсутствует guard / неверное предположение об источнике данных (углубление — `/why`).
3. Fix: optional chaining `obj?.x` или явный guard `if (obj === null) return …`.
4. Verify: добавить негативный тест на `null`-вход, прогнать снова до зелёного.

---

## 🔄 История изменений

| Дата | Изменение | Причина |
|------|-----------|---------|
| 2026-06-11 | Создание стандарта | Вынос generic-методов из `rules-validation-standard.md` §11-13 (они не про валидацию правил) |
