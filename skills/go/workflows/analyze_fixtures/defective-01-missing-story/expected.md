# Expected output of analyze

## 🔴 GAPS

1. **US-3 "Export data to CSV" не реализована.**
   - В PRD есть user story US-3 с 3 acceptance criteria (кнопка Export CSV, raw-данные, имя файла по шаблону).
   - В plan.md нет ни одного step, упоминающего CSV или export.
   - В issues.md нет ни одного issue про export.
   - Это покрытие **0%** для US-3.

## 🟡 WARNS

Нет.

## ✅ Coverage

- Stories: **2 / 3** (US-1 покрыта через DASH-1..4, DASH-6; US-2 через DASH-5; US-3 **не покрыта**)
- NFR: 2/2 (Performance через DASH-9, Browser support имплицитно покрыт любым web-issue — технически 🟡 WARN за отсутствие явного browser test issue, но это допустимо)

## Verdict

🔴 **FAIL** — имплементация не должна начинаться, пока US-3 не добавлена в plan и issues.

## Why this fixture tests the detector

Этот набор проверяет, что analyze находит **потерянные stories** — самый частый реальный баг: длинный PRD, кто-то пропустил одну историю при декомпозиции, имплементация идёт дальше без этой функциональности, и заказчик обнаруживает отсутствие фичи только при приёмке.
