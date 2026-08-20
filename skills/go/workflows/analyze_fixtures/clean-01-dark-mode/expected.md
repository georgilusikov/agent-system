# Expected output of analyze

## 🔴 GAPS

Нет.

## 🟡 WARNS

Нет.

## ✅ Coverage

- Stories: 2/2
  - US-1 "Toggle theme from settings" → DARK-2, DARK-3 (три опции, System слушает prefers-color-scheme)
  - US-2 "Persist theme across sessions" → DARK-4 (localStorage), DARK-5 (FOUC prevention покрывает "no flash")
- NFR: 1/1 (Accessibility → DARK-6)

## Verdict

✅ **PASS** — все stories и NFR покрыты, orphan issues нет, dependency graph валиден (нет циклов, нет ссылок на несуществующие).

## Why this fixture tests the detector

Этот набор — **false-positive check**. analyze должен корректно распознать полное покрытие и НЕ галлюцинировать gaps. Если на этом наборе analyze выдаёт 🔴 или 🟡 — значит детектор слишком агрессивный, его нельзя использовать (будет блокировать валидные плана имплементации).
