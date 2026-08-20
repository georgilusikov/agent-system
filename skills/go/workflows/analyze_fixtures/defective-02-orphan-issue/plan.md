# Plan: Invite teammate via link

## Phase 1: Token model

- **Step 1.1.** Таблица `invite_tokens(id, team_id, role, expires_at, used_at, created_by)`.
- **Step 1.2.** Сервис `InviteService.generate(team_id, role)` → возвращает 32-байтный token.
- **Step 1.3.** Сервис `InviteService.consume(token)` → возвращает team_id + role или raise `InviteExpired`/`InviteUsed`.

## Phase 2: Admin UI

- **Step 2.1.** Кнопка "Generate invite link" в admin panel. Модалка с селектом роли.
- **Step 2.2.** После генерации показать ссылку + кнопка "Copy to clipboard".

## Phase 3: Signup flow

- **Step 3.1.** Роут `/invite/:token` — валидирует token, показывает signup-форму или "expired".
- **Step 3.2.** После успешной регистрации — `consume(token)` и присвоение роли.

## Phase 4: Observability

- **Step 4.1.** События `invite_generated` и `invite_accepted` в analytics (Segment).
