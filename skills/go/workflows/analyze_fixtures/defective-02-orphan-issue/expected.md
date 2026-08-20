# Expected output of analyze

## 🔴 GAPS

Нет.

## 🟡 WARNS

1. **INV-9 "Add Redis caching layer for invite lookups" — orphan issue.**
   - Не привязан ни к одной фазе плана (в поле `Phase:` указано "не указано в плане").
   - В PRD нет performance-требований, упоминающих кэш, rate limits или латентность lookup-операций.
   - В plan.md нет упоминания кэша или Redis.
   - Est 3 дня — значительный scope creep.

## ✅ Coverage

- Stories: 2/2 (US-1 через INV-1..5; US-2 через INV-6..7)
- NFR: 2/2 (Security через 32-байтный token в INV-2; Observability через INV-8)

## Verdict

🟡 **WARN** — имплементация может стартовать, но INV-9 должен быть либо
(a) удалён из scope,
(b) обоснован добавлением NFR в PRD (например "consume lookup < 50ms p95"), либо
(c) перенесён в отдельный backlog.

## Why this fixture tests the detector

Этот набор проверяет детектор **orphan issues** — скрытый scope creep. Разработчик добавляет "а давайте ещё кэш прикрутим" в процессе декомпозиции, и это утекает в имплементацию без обоснования. 3 дня работы, не требуемой PRD, — типичная причина срыва сроков.
