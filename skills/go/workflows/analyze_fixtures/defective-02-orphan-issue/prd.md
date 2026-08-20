# PRD: Invite teammate via link

## Problem

Сейчас админ добавляет members руками через admin panel: вводит email, выставляет роль, жмёт Save. На командах >20 человек это съедает десятки минут и приводит к ошибкам в ролях.

## User stories

### US-1: Generate invite link
Как админ, я хочу сгенерировать одноразовую ссылку-приглашение с предустановленной ролью, чтобы отправить её новому коллеге.

**Acceptance:**
- В admin panel кнопка "Generate invite link"
- Выбор роли (admin/editor/viewer) перед генерацией
- Ссылка вида `https://app.example.com/invite/{token}`
- Token валиден 7 дней, одноразовый

### US-2: Accept invite and sign up
Как приглашённый пользователь, я хочу перейти по ссылке и зарегистрироваться, автоматически получив нужную роль в нужной команде.

**Acceptance:**
- Переход по ссылке открывает signup-форму с pre-filled team name
- После регистрации пользователь попадает в dashboard с правильной ролью
- Просроченный/использованный token → экран "Invite expired"

## NFR

- **Security:** token — 32-байтный случайный id, не угадываемый. HTTPS only.
- **Observability:** событие "invite_generated" и "invite_accepted" в analytics.
