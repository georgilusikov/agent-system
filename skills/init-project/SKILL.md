---
name: init-project
description: 'Создаёт AGENTS.md (универсальный, для всех AI-агентов) + CLAUDE.md (Claude-специфичный) + опционально PROJECT_BRIEF.md (state snapshot для long-running проектов) по рамке концептуализации. Запускай в корне проекта. Триггеры: init project, создай claude md, настрой проект, project setup, инициализируй проект. Triggers: "init project", "создай CLAUDE.md для проекта", "настрой проект под агентов", "напиши AGENTS.md", "инициализируй проект", "нужен PROJECT_BRIEF". NOT for: постановка цели и гейтов по уже настроенному проекту (/goal-plan) и разовая правка одного правила без пересборки файлов проекта (/go).'
---

# Создание проектных AGENTS.md + CLAUDE.md (+ опционально PROJECT_BRIEF.md)

Генерирует **два-три файла**:
- **AGENTS.md** — универсальные правила проекта. Читают: Codex CLI, Jules, GitHub Copilot, Cursor, Windsurf. Gemini CLI — через настройку `context.fileName`.
- **CLAUDE.md** — импортирует AGENTS.md через `@AGENTS.md` + добавляет Claude-специфичное (skills, MCP серверы, sub-agents).
- **PROJECT_BRIEF.md** (опционально) — state snapshot. Phase / Maturity / deliverables / scope guardrails / open questions. Обновляется регулярно. Генерируй когда проект long-running с фазами и async open questions; пропусти для одноразовых скриптов и фикстур.

Рамка основана на философской концептуализации: КТО, ЧТО, КАК, РАДИ ЧЕГО, РЕЗУЛЬТАТ. Каждая секция предотвращает конкретный класс ошибок.

## Логика: чем руководствоваться

### Принцип отбора
Каждая строка должна предотвращать ошибку или менять поведение агента. Если строку убрать и ничего не изменится — она не нужна. Не пиши очевидное, не дублируй линтер.

### Что куда

| Контент | Файл | Почему |
|---|---|---|
| Цель, приоритет, нарратив | AGENTS.md | Универсально, stable contract |
| Среда, структура, команды | AGENTS.md | Универсально |
| Стиль, checkpoints, definition of done | AGENTS.md | Универсально |
| Принятые решения, грабли, не трогать | AGENTS.md | Универсально |
| MCP серверы, skills | CLAUDE.md | Только Claude Code |
| Другие исполнители (AgentNet, Jules) | CLAUDE.md | Claude Code оркестрирует агентов |
| Sub-agent инструкции | CLAUDE.md | Только Claude Code |
| Phase / Maturity / Last milestone | PROJECT_BRIEF.md | State snapshot, меняется чаще чем contract |
| Deliverables (capabilities) | PROJECT_BRIEF.md | Конкретный список того что проект умеет |
| Scope & Guardrails (что в/НЕ в scope) | PROJECT_BRIEF.md | Граница для решений (≠ "не трогать" в AGENTS.md) |
| Open Questions / Unknowns | PROJECT_BRIEF.md | Чтобы агент не принял нерешённое за решённое |

### Как думать по секциям

**РАДИ ЧЕГО** — определяет trade-off. "Приоритет: скорость" → не тратить час на типы. Пиши то, что разрешает конфликты.

**НАРРАТИВ** — направление. "Идём к микросервисам" → не добавлять shared state. Одно предложение: откуда → где → куда.

**ДЛЯ КОГО** — определяет UX. "Для студентов" = дружелюбные ошибки. "Для агентов" = машиночитаемые ответы.

**КТО** — пиши только неочевидное: Python 3.9 на target (если локально 3.12) — да. "Ты senior dev" — нет (не влияет).

**ЧТО** — текущая фаза, принятые решения (предотвращает scope creep), грабли (предотвращает повторение тупиков), что не трогать, лимиты.

**КАК** — команды (агент не угадает), следствия приоритетов (ПОЧЕМУ правило существует), checkpoints.

**РЕЗУЛЬТАТ** — конкретная команда проверки, не "убедись что работает".

## Шаг 1: Разведка

1. Прочитай файлы проекта:
   - `ls` корня, `README.md`, `package.json` / `pyproject.toml` / `Cargo.toml` / `go.mod`
   - `Dockerfile` / `docker-compose.yml`, `.env.example`
   - Существующие `AGENTS.md`, `CLAUDE.md` — если есть, обновляй, не перезаписывай

2. `git log --oneline -10` — текущая фаза

3. Определи из кода: язык, фреймворк (с версией!), entrypoints, структуру, внешние зависимости

## Шаг 2: Спроси пользователя

```
Для проектных файлов мне нужно уточнить:

1. **Ради чего**: Какую проблему решает проект? (если есть description в pyproject.toml/package.json — предложи, спроси "верно?")
2. **Направление**: Откуда начали → где сейчас → куда идём?
3. **Приоритет**: Скорость / качество / надёжность — что важнее?
4. **Для кого**: Кто пользователь? (студенты, B2B, внутренний, другие агенты)
5. **Среда**: Target host отличается от localhost?
6. **Агенты**: Кто ещё работает над проектом? (AgentNet, Jules, Codex, Gemini CLI, люди)
7. **Готово когда**: Как проверить что фаза завершена?
8. **Не трогать**: Frozen zones?
9. **Решения**: Что уже выбрано и не обсуждается?
10. **Грабли**: Что пробовали и не сработало?
11. **State snapshot**: Long-running проект с фазами (ideation → MVP → production → maintenance) и async open questions? Если да — генерирую PROJECT_BRIEF.md. Если одноразовый скрипт / фикстура — пропускаю.
```

НЕ спрашивай то, что есть в коде.

## Шаг 3: Сгенерируй два файла

### Файл 1: AGENTS.md (универсальный)

```markdown
# {Project Name}

## Ради чего
{Одно предложение: проблема.}
Приоритет: {скорость > качество / качество > скорость / надёжность > всё}.

## Нарратив проекта
{Откуда → где сейчас → куда. Определяет направление решений.}

## Для кого
{Кто пользователь. Определяет UX, тон ошибок, уровень детализации.}

## Среда
- Runtime: {язык} {версия} на {host}
- Фреймворк: {name} {version}
- БД/сервисы: {если есть}
{Если target host ≠ localhost:}
- Target: `ssh {host}` — проверь `{lang} --version` перед началом

## Роль агента
{Конкретная функция: "backend на FastAPI", "CLI утилита", "React dashboard".}

## Текущее состояние
{Прототип / MVP / Production}

## Принятые решения
{Что выбрано и не обсуждается:}
{- SQLite, не PostgreSQL — single-user}
{- Монолит — MVP, не время для микросервисов}

## Известные грабли
{Что пробовали и не работает:}
{- X не работает потому что Y}

## Структура
```
{смысловая карта ключевых директорий}
```

## Зависимости и лимиты
{API rate limits, внешние сервисы, что в .env}

## Не трогать
{Frozen zones: legacy, чужой код, auto-generated}

## Команды
```bash
dev:    {команда запуска}
test:   {команда тестов}
lint:   {линтер}
deploy: {деплой}
```

## Тестирование
{Фреймворк, как запускать, где fixtures}

## Порядок работы
1. {Blueprint first? Код first?}
2. {TDD? Manual?}
3. {Deploy flow}

## Следствия приоритетов
{Приоритет X → поэтому Y}
{Target Z → поэтому W}

## Checkpoints
- Перед кодом: {что проверить}
- Перед деплоем: {что проверить}
- Перед "готово": {финальная верификация}

## Стиль
{Только если отличается от стандарта языка}

## Готово когда
{Конкретные критерии:}
- {API 200 на /health}
- {CLI выводит результат}

## Как проверить
```bash
{команда верификации}
```
```

### Файл 2: CLAUDE.md (Claude-специфичный)

```markdown
@AGENTS.md

## Другие исполнители
{Только если есть — Claude Code оркестрирует:}
- AgentNet: {задачи, workdir}
- Jules: {isolated tasks}
- Codex: {review/gate, не код}
- Gemini CLI: {deep research}

## Инструменты Claude Code
{MCP серверы: chrome, playwright, context7, etc.}
{Skills: /check, /bouncer, etc.}

## Sub-agent инструкции
{Как разделять работу между агентами: non-overlapping files, parallel batches}
```

**Правило: CLAUDE.md должен быть коротким (10-20 строк).** Всё универсальное — в AGENTS.md. Если нет Claude-специфичного контента — CLAUDE.md = просто `@AGENTS.md`.

### Файл 3: PROJECT_BRIEF.md (опционально — только если на вопрос #11 был "да")

Назначение: state snapshot. Меняется чаще чем AGENTS.md. AGENTS.md = stable contract (правила работы), PROJECT_BRIEF.md = текущая фотография (где мы сейчас, что не решено).

**Не дублировать AGENTS.md.** Если содержимое строки уже есть в AGENTS.md — не повторяй, ссылайся.

```markdown
<!-- Owner: {имя}  |  Last reviewed: {YYYY-MM-DD}  |  Read next: AGENTS.md -->

# {Project Name}

## Суть
{Одно-два предложения: что это и какую проблему решает. Может слегка перекликаться с AGENTS.md "Ради чего", но здесь — конкретнее: с deliverables, не только mission.}

## Для кого
- Primary user: {основной пользователь}
- Secondary: {если есть}

## Что делает (deliverables)
- {Capability 1 — конкретная функция}
- {Capability 2}
- {Capability 3}

## Текущий статус
- **Phase:** ideation | prototype | active_dev | production | maintenance | archived
- **Maturity:** spec_only | MVP | beta | stable
- **Last milestone:** {YYYY-MM-DD — что было достигнуто}

## Scope & Guardrails
**В scope:** {что именно делаем сейчас}
**НЕ в scope:** {явно отвергнутые направления — чтобы агент не предложил}
**Можно менять без согласования:** {зоны для autonomous работы}
**Нельзя менять без согласования:** {protected — отличается от AGENTS.md "Не трогать" тем, что здесь — про ручной approval, а не про "никогда"}

## Open Questions / Unknowns
Что ещё не решено. Агент: не принимай это за решённое.
- [ ] {Open question 1}
- [ ] {Open question 2}
```

**Правило длины:** PROJECT_BRIEF.md = 20-50 строк. Длиннее — выноси детали в `docs/`. Короче — возможно, проект ещё не нуждается в brief, удали.

**Правило обновления:** Owner обновляет `Last reviewed` дату при пересмотре (раз в спринт / раз в месяц). Phase меняется на milestone'ах. Open Questions — checklist для async ответа.

## Шаг 4: Проверка на противоречия

- Приоритет "скорость" + "обязательный TDD" = конфликт
- "Не трогать: X" + checkpoint "рефакторить X" = конфликт
- Нарратив "автоматизация" + workflow "ручной деплой" = напряжение

Противоречие → спроси пользователя.

## Шаг 5: Валидация

1. Покажи все сгенерированные файлы (2 или 3 в зависимости от ответа на #11)
2. Спроси: "Что упущено? Что лишнее? Противоречия? Дублирование между AGENTS.md и PROJECT_BRIEF.md?"
3. Скорректируй
4. Напомни: "Чтобы Gemini CLI читал AGENTS.md, добавь в `~/.gemini/settings.json`: `{\"context\": {\"fileName\": [\"AGENTS.md\", \"GEMINI.md\"]}}`"
5. Если сгенерирован PROJECT_BRIEF.md — напомни owner'у: "Last reviewed обновляется руками при пересмотре. Phase меняется на milestone'ах. Open Questions — checklist для ответа."

## Правила

- Удаляй пустые секции
- Данные из кода, не из головы
- Версии — из package.json/pyproject.toml, не гадать
- Target host → выполни `ssh {host} '{lang} --version'`
- AGENTS.md: 40-80 строк. CLAUDE.md: 5-20 строк. PROJECT_BRIEF.md: 20-50 строк (если генерируется).
- Если CLAUDE.md = только `@AGENTS.md` без добавлений — так и пиши, это нормально
- Если сомневаешься нужен ли PROJECT_BRIEF.md — НЕ генерируй. Лучше его добавить позже когда проект созреет, чем создать пустой шаблон с TBD во всех полях
- PROJECT_BRIEF.md vs AGENTS.md "Не трогать": AGENTS.md = вечные frozen zones (legacy, чужой код); PROJECT_BRIEF.md "Нельзя менять без согласования" = scope guardrails текущего спринта (может разморозиться в следующем)

## Пример: Telegram бот

### AGENTS.md
```markdown
# QuizBot

## Ради чего
Telegram quiz-бот для engagement в образовательном проекте.
Приоритет: скорость запуска > качество кода.

## Нарратив проекта
Идея → MVP с 5 квизами → цель: 50 активных пользователей за первую неделю.

## Для кого
Студенты 18-25. Дружелюбный тон, без технических ошибок в UI.

## Среда
- Runtime: Python 3.9 на Mac Mini (`ssh macmini`)
- Фреймворк: aiogram 3.x (НЕ 2.x — DI через `dp.workflow_data`, не `bot[]`)
- БД: SQLite
- IMPORTANT: `from __future__ import annotations` в каждом файле (Python 3.9)

## Роль агента
Backend: Telegram Bot API + aiogram 3.x + async Python.

## Принятые решения
- aiogram 3.x, не Telegraf — Python ecosystem
- SQLite, не PostgreSQL — single-user MVP
- Webhook, не polling — работает за NAT

## Известные грабли
- `bot["key"] = value` — TypeError в aiogram 3.x. Использовать `dp.workflow_data`
- Polling mode — не работает за NAT

## Структура
src/
├── bot.py          # entrypoint
├── handlers/       # aiogram routers
├── models/         # Pydantic
└── state.py        # game_manager singleton

## Не трогать
- `handlers/legacy_poll.py` — будет удалён после миграции

## Команды
dev:    ssh macmini 'cd ~/quiz-bot && python -m bot'
test:   ssh macmini 'cd ~/quiz-bot && python -m pytest tests/'
deploy: scp -r src/ macmini:~/quiz-bot/ && ssh macmini 'systemctl restart quizbot'

## Следствия приоритетов
Скорость → нет TDD, тестирование через реальный /start в Telegram
Python 3.9 → eval_type_backport + `from __future__ import annotations`

## Checkpoints
- Перед кодом: `ssh macmini 'python3 --version'` (3.9.x)
- Перед деплоем: `python -c "from src.bot import main"`
- Перед "готово": /start → квиз → score в Telegram

## Готово когда
- Бот отвечает на /start
- Deep link `t.me/bot?start=quiz_1` работает

## Как проверить
ssh macmini 'curl -s http://localhost:8080/health'
```

### CLAUDE.md
```markdown
@AGENTS.md

## Другие исполнители
- AgentNet: standalone квизы (отдельные handlers), workdir = этот проект
- Jules: тесты, документация — isolated tasks

## Инструменты
- MCP: chrome (для тестирования deep links в браузере)
```

### PROJECT_BRIEF.md (поскольку проект long-running с фазами и open questions)
```markdown
<!-- Owner: Georgij  |  Last reviewed: 2026-04-26  |  Read next: AGENTS.md -->

# QuizBot

## Суть
Telegram quiz-бот: 5 квизов, deep links, scoreboard. MVP для оценки engagement в курсе.

## Для кого
- Primary user: студенты курса 18-25
- Secondary: преподаватель (получает scoreboard для группы)

## Что делает (deliverables)
- /start с deep link → запуск квиза
- 5 квизов по 10 вопросов
- scoreboard в Telegram (топ-10 студентов)
- сохранение прогресса между сессиями

## Текущий статус
- **Phase:** prototype
- **Maturity:** MVP
- **Last milestone:** 2026-04-20 — первый студент прошёл квиз end-to-end

## Scope & Guardrails
**В scope:** 5 квизов, scoreboard, deep links
**НЕ в scope:** биллинг, групповые игры, real-time чат, мобильное приложение
**Можно менять без согласования:** handlers/*, content квизов
**Нельзя менять без согласования:** структуру БД (есть данные первых студентов), webhook URL

## Open Questions / Unknowns
- [ ] Нужна ли регистрация по invite-коду или /start свободно?
- [ ] Сохранять ли результаты после удаления чата?
- [ ] Стоит ли добавить голосовые ответы (whisper API)?
```
