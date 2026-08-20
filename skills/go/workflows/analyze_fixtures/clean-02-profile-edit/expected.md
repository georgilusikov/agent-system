# Expected output of analyze

## 🔴 GAPS

Нет.

## 🟡 WARNS

Нет.

## ✅ Coverage

- Stories: 4/4
  - US-1 "Edit basic fields" → PROF-4
  - US-2 "Change email with verification" → PROF-5
  - US-3 "Change password" → PROF-6 (явно включает session invalidation)
  - US-4 "Delete account" → PROF-7 (soft + hard delete job)
- NFR: 2/2
  - Validation → покрыт через AC "валидирует name (required) и bio (max 500)", "400 с per-field errors" в PROF-4, аналогично в остальных
  - Audit log → PROF-2 (инфраструктура) + каждый из PROF-4/5/6/7 явно упоминает audit_log запись; PROF-3 имеет unit-тест на гарантию записи

## Dependency graph

- PROF-1 → независим
- PROF-2 → независим
- PROF-3 → blocked by PROF-1, PROF-2
- PROF-4, PROF-5, PROF-6, PROF-7 → blocked by PROF-3 (могут параллельно)
- Нет циклов. Нет ссылок на несуществующие issues.

## Verdict

✅ **PASS** — все stories и NFR покрыты, 7 issues с валидным dependency graph. Можно стартовать имплементацию.

## Why this fixture tests the detector

Этот набор — **false-positive check на более сложном кейсе**. 4 stories, 2 cross-cutting NFR (audit log затрагивает каждый story), non-trivial dependency graph с параллельными ветками. Если analyze выдаёт gap или warn на этом наборе — значит детектор ошибается на реалистичных средних фичах, не только на тривиальных. Это второй уровень защиты от false-positives.
