<!-- Golden example. Регрессионный якорь: изменение скилла → сверить новый вывод -->
<!-- с этим файлом (gate ≥85%). Кейс учебный, пути и хеши вымышленные. -->

# /debug — Mode L: тест падает после мержа

## Режим-роутер

Симптом один, traceback точный, конкурирующих причин нет → **Mode L** (линейная
цепочка, 5 Whys). Ни на одном «почему» не выросло ≥3 параллельных ветки —
переключение в Mode H не потребовалось.

Anti-freeze: не сработал (первая попытка, повторов той же команды нет, timeout'ов нет).

## 1. Факты

Команда:

```bash
pytest -q tests/test_invoice.py::test_total_with_discount
```

Output (хвост):

```
E       TypeError: apply_discount() got an unexpected keyword argument 'percent'

src/billing/invoice.py:142: TypeError
1 failed, 213 passed in 12.41s
```

Контекст: падение появилось на `main` сразу после мержа ветки
`feature/invoice-split`; до мержа оба родителя зелёные (проверено ниже, Why-4).

## 2. 5 Whys

| # | Почему | Evidence [O] |
|---|---|---|
| 1 | Тест падает, потому что вызов передаёт kwarg `percent` | `src/billing/invoice.py:142` — `apply_discount(order, percent=rate_pct)` |
| 2 | ...потому что сигнатура `apply_discount` больше не принимает `percent` | `src/billing/discounts.py:31` — `def apply_discount(order, *, rate: Decimal)` |
| 3 | ...потому что параметр переименован `percent` → `rate` (и сменил семантику: проценты → доля) | `git log -3 --oneline -- src/billing/discounts.py` → `a1b2c3d align discount API on rate fraction` |
| 4 | ...потому что вызывающая строка `invoice.py:142` добавлена параллельно, в другой ветке, после точки ветвления | `git log -1 --oneline -- src/billing/invoice.py` → `d4e5f6a split invoice totals`; `git merge-base a1b2c3d d4e5f6a` → `9f0e1d2` (общий предок раньше обоих) |
| 5 | ...потому что мерж прошёл без конфликта (правки в разных файлах), а pre-merge CI гонял только targeted-набор ветки, не полный прогон | `.github/workflows/pr.yml:24` — `pytest tests/${{ matrix.area }}` |

**Root cause:** семантический конфликт мержа. Переименование kwarg
`percent` → `rate` (`discounts.py:31`) не дошло до нового вызова
`invoice.py:142`, добавленного в параллельной ветке. Ни один родитель по
отдельности несовместимость не видит; текстовый CLEAN у git ≠ семантическая
корректность, а targeted-CI шов не покрывает.

## 3. Fix

Chesterton fence (fix касается существующего кода):
`git log -5 --oneline -- src/billing/discounts.py` → переименование намеренное,
commit `a1b2c3d align discount API on rate fraction`, возраст 6 дней (свежий
коммит той же недели = вероятно намеренное решение). Значит откат rename
запрещён — выравнивается вызывающая сторона.

Правка одна, точечная — `src/billing/invoice.py:142`:

```diff
-    total = apply_discount(order, percent=rate_pct)
+    total = apply_discount(order, rate=rate_pct / Decimal(100))
```

Деление на 100 обязательно: новый контракт принимает долю (`0.10`), старый —
проценты (`10`). Переименовать только ключ = молчаливая ошибка в 10 раз.

## 4. Verify

```bash
pytest -q tests/test_invoice.py::test_total_with_discount
# 1 passed in 1.83s

pytest -q
# 214 passed in 96.2s
```

Полный прогон, а не только targeted-набор: правка лежит ровно на шве двух
веток, targeted-тесты его и пропустили.

## 5. Document

```
Command:   pytest -q tests/test_invoice.py::test_total_with_discount
Error:     TypeError: apply_discount() got an unexpected keyword argument 'percent'
           (src/billing/invoice.py:142)
Root Cause: семантический конфликт мержа — kwarg переименован percent→rate
           со сменой семантики (проценты→доля) в discounts.py:31 (a1b2c3d),
           новый вызов invoice.py:142 (d4e5f6a) из параллельной ветки не обновлён;
           targeted-CI шов не покрывает.
Fix:       invoice.py:142 — apply_discount(order, rate=rate_pct / Decimal(100))
Status: Verified
```

`Verified` поставлен после реального повторного прогона (см. §4), не по факту
правки.

## Handoff

- Fix применён → `/check` (верификация + регрессии вокруг расчёта скидок).
- Root cause процессная и повторяемая (targeted-CI не ловит семантический шов):

```bash
~/.claude/bin/log-incident.sh --kind rca --severity medium --source /debug \
  --summary "merge CLEAN != semantic: renamed kwarg + new caller from parallel branch; targeted-only CI missed the seam"
```

**Уверенность в root cause: 95%** — цепочка целиком на [O]-фактах
(файл:строка, git log, merge-base), подтверждена зелёным повторным прогоном.
