# PRD: User profile editing

## Problem

Пользователи не могут менять свои данные после регистрации — только через support-тикет. Это создаёт ~30 тикетов/неделю и задержку 2-3 дня на обновление элементарных полей.

## User stories

### US-1: Edit basic fields
Как пользователь, я хочу редактировать name, bio, avatar, чтобы поддерживать профиль актуальным.

**Acceptance:**
- В /profile/edit форма с полями name (required), bio (optional, max 500 chars), avatar upload
- Save обновляет данные на сервере, показывает toast "Saved"
- Cancel возвращает на /profile без изменений

### US-2: Change email with verification
Как пользователь, я хочу сменить email, подтвердив новый через ссылку.

**Acceptance:**
- Ввод нового email запускает отправку verification-письма на него
- До клика по ссылке старый email остаётся актуальным
- После клика новый email становится primary, старый инвалидируется
- Verification-ссылка валидна 24 часа

### US-3: Change password
Как пользователь, я хочу сменить пароль, введя текущий и новый (дважды).

**Acceptance:**
- Форма с полями: current password, new password, confirm new password
- Неверный current → 400 с явной ошибкой
- new != confirm → client-side error
- Успех → все существующие сессии этого пользователя инвалидируются, кроме текущей

### US-4: Delete account
Как пользователь, я хочу удалить аккаунт с подтверждением.

**Acceptance:**
- Кнопка "Delete account" в /profile/edit → модалка подтверждения
- Требуется ввести текущий пароль и фразу "DELETE MY ACCOUNT"
- Soft delete: запись помечается `deleted_at`, через 30 дней — hard delete job
- Немедленный logout и редирект на /goodbye

## NFR

- **Validation:** все input-поля валидируются на сервере (doубный контроль поверх client-side). Невалидный payload → 400 с per-field errors.
- **Audit log:** каждое изменение профиля (все 4 stories) пишется в `audit_log` с `user_id`, `action`, `before/after`, `timestamp`, `ip`.

## Out of scope

- Bulk edit через admin panel
- Two-factor auth
- Social accounts linking
