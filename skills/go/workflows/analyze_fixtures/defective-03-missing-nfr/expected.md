# Expected output of analyze

## 🔴 GAPS

1. **NFR "Security: JWT auth on all endpoints" не покрыт.**
   - PRD явно требует: JWT в header, 401 без/с невалидным токеном, привязка токена к partner_id.
   - plan.md **не содержит** фазы аутентификации.
   - issues.md **не содержит** ни одного issue про JWT middleware, валидацию токенов, 401-семантику.
   - Фактически repository фильтрует по partner_id (API-4), но откуда берётся этот partner_id в handler — не определено. Это классический security gap.

## 🟡 WARNS

1. **API-2 и US-2 acceptance criteria покрыты частично.**
   - US-2 явно требует "чужой id → 404 (не раскрываем факт существования)". API-4 фильтрует по partner_id, но acceptance check на "404 для чужого ордера" может быть пропущен при тестировании. Рекомендуется явный unit-тест на этот кейс.

## ✅ Coverage

- Stories: 3/3 (US-1 → API-1; US-2 → API-2; US-3 → API-3)
- NFR: **2/3** (Rate limiting → API-5; Observability → API-6+API-7; **Security НЕ покрыт**)

## Verdict

🔴 **FAIL** — имплементация не должна начинаться. Security NFR самый критический из трёх, его пропуск означает публичный API без аутентификации. Нужна отдельная phase "Auth middleware" + issue API-0 "JWT auth middleware" с блокировкой всех остальных API-issues.

## Why this fixture tests the detector

Этот набор проверяет детектор **непокрытых NFR** — самый опасный класс пропусков. NFR в PRD обычно вынесены в отдельный раздел, их легко прочитать и кивнуть, не декомпозировав на issues. Security NFR особенно часто теряются — функциональные фичи проще визуализировать, auth middleware "и так понятно что нужен", поэтому не попадает в trackable issue.
