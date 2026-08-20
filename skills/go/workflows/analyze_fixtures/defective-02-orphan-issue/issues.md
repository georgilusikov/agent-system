# Issues: Invite teammate via link

## INV-1 — invite_tokens migration
- **Phase:** 1.1
- **Est:** 0.5 day
- **Blocked by:** —
- **AC:** Миграция создаёт таблицу с индексами на `token` и `team_id`. Unique constraint на `token`.

## INV-2 — InviteService.generate
- **Phase:** 1.2
- **Est:** 0.5 day
- **Blocked by:** INV-1
- **AC:** `generate(team_id, role)` возвращает 32-байтный urlsafe token. Token сохраняется с `expires_at = now + 7d`.

## INV-3 — InviteService.consume
- **Phase:** 1.3
- **Est:** 1 day
- **Blocked by:** INV-2
- **AC:** `consume(token)` выставляет `used_at`. Просроченный token → `InviteExpired`. Использованный → `InviteUsed`.

## INV-4 — Admin UI modal
- **Phase:** 2.1
- **Est:** 1 day
- **Blocked by:** INV-2
- **AC:** Кнопка "Generate invite link" открывает модалку с селектом роли (admin/editor/viewer). По кнопке Generate — запрос на API, показ ссылки.

## INV-5 — Copy to clipboard button
- **Phase:** 2.2
- **Est:** 0.25 day
- **Blocked by:** INV-4
- **AC:** Кнопка "Copy" копирует ссылку. Toast "Copied!" на 2 сек.

## INV-6 — /invite/:token route
- **Phase:** 3.1
- **Est:** 1 day
- **Blocked by:** INV-3
- **AC:** Валидный token → signup-форма. Invalid/expired/used → экран "Invite expired".

## INV-7 — Consume token on signup
- **Phase:** 3.2
- **Est:** 0.5 day
- **Blocked by:** INV-6
- **AC:** После успешной регистрации пользователь получает роль из token, попадает в dashboard команды.

## INV-8 — Analytics events
- **Phase:** 4.1
- **Est:** 0.5 day
- **Blocked by:** INV-4, INV-7
- **AC:** Segment event `invite_generated` на генерации, `invite_accepted` на успешной регистрации.

## INV-9 — Add Redis caching layer for invite lookups
- **Phase:** (не указано в плане)
- **Est:** 3 days
- **Blocked by:** INV-3
- **AC:** Redis cache для `InviteService.consume`. TTL 10 минут. Cache hit rate > 70%.
