# Plan: User profile editing

## Phase 1: Backend foundation

- **Step 1.1.** Миграция таблицы `users`: добавить `deleted_at`, `pending_email`, `email_verification_token`, `email_verification_expires_at`.
- **Step 1.2.** Таблица `audit_log(id, user_id, action, before, after, ip, created_at)`.
- **Step 1.3.** Сервис `ProfileService` с методами `update_basic`, `request_email_change`, `confirm_email_change`, `change_password`, `delete_account`. Каждый метод пишет в audit_log.

## Phase 2: Basic profile fields UI

- **Step 2.1.** Страница /profile/edit с формой (name, bio, avatar upload).
- **Step 2.2.** Endpoint PATCH /api/profile — вызывает `ProfileService.update_basic`, возвращает 200 или 400 с per-field errors.
- **Step 2.3.** Avatar storage — S3 uploader через signed URL.

## Phase 3: Email change with verification

- **Step 3.1.** UI "Change email" в /profile/edit. Ввод нового email → request.
- **Step 3.2.** Endpoint POST /api/profile/email — генерирует token (24h expiry), отправляет verification-mail на новый адрес через transactional SES.
- **Step 3.3.** Endpoint GET /api/profile/email/confirm?token=... — валидирует token, свопает email.

## Phase 4: Password change and session invalidation

- **Step 4.1.** UI "Change password" форма (current, new, confirm).
- **Step 4.2.** Endpoint POST /api/profile/password — проверяет current, меняет hash, инвалидирует все сессии пользователя кроме текущей.

## Phase 5: Account deletion

- **Step 5.1.** UI модалка подтверждения с паролем и кодовой фразой.
- **Step 5.2.** Endpoint DELETE /api/profile — soft delete (`deleted_at`), немедленный logout. Background job `hard_delete_expired_accounts` запускается ежедневно, удаляет записи с `deleted_at < now - 30d`.

## Dependencies

- Phases 2, 3, 4, 5 все blocked by Phase 1
- Phase 2, 3, 4, 5 могут идти параллельно после Phase 1
