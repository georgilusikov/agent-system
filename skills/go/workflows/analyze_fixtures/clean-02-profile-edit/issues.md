# Issues: User profile editing

## PROF-1 — users table migration
- **Phase:** 1.1
- **Est:** 0.5 day
- **Blocked by:** —
- **AC:** Миграция добавляет `deleted_at`, `pending_email`, `email_verification_token`, `email_verification_expires_at`. Все nullable, дефолты осмысленные.

## PROF-2 — audit_log table and helper
- **Phase:** 1.2
- **Est:** 0.5 day
- **Blocked by:** —
- **AC:** Таблица создана. Функция `log_audit(user_id, action, before, after, ip)` — атомарная запись. Индекс на `(user_id, created_at)`.

## PROF-3 — ProfileService skeleton
- **Phase:** 1.3
- **Est:** 1 day
- **Blocked by:** PROF-1, PROF-2
- **AC:** Класс с методами-заглушками. Каждый метод вызывает `log_audit`. Unit-тесты на то, что audit_log пишется при успехе и не пишется при validation error.

## PROF-4 — Update basic fields (US-1)
- **Phase:** 2.1, 2.2, 2.3
- **Est:** 2 days
- **Blocked by:** PROF-3
- **AC:** PATCH /api/profile валидирует name (required) и bio (max 500). Avatar upload через S3 signed URL. На успех — toast "Saved", audit_log запись. Невалидный payload → 400 с per-field errors.

## PROF-5 — Email change with verification (US-2)
- **Phase:** 3.1, 3.2, 3.3
- **Est:** 3 days
- **Blocked by:** PROF-3
- **AC:** Ввод нового email → письмо. Token валиден 24 часа. До подтверждения старый email остаётся primary. После клика — новый активен, старый инвалид. Audit_log записывает событие.

## PROF-6 — Change password and invalidate sessions (US-3)
- **Phase:** 4.1, 4.2
- **Est:** 2 days
- **Blocked by:** PROF-3
- **AC:** Форма валидирует current на сервере. Неверный current → 400. Успех → bcrypt hash обновлён, все sessions пользователя (кроме текущей) инвалидированы. Audit_log записывает.

## PROF-7 — Delete account with soft delete and hard-delete job (US-4)
- **Phase:** 5.1, 5.2
- **Est:** 2 days
- **Blocked by:** PROF-3
- **AC:** Модалка с паролем и фразой "DELETE MY ACCOUNT". Soft delete. Немедленный logout и редирект /goodbye. Cron-job ежедневно удаляет записи с `deleted_at < now - 30d`. Audit_log записывает soft и hard delete.
