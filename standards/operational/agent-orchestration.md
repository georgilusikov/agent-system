---
name: agent-orchestration
description: Методология делегирования и оркестрации AI-агентов (Claude Code, Codex, Gemini CLI, Kimi CLI, Droid, Antigravity, Jules) через AgentNet. Покрывает health check перед dispatch, parallel split по файлам, bridge vs CDP transport, prompt design, mission coordinator recovery, audit patterns.
version: 0.0.1
created: 2026-04-19
incident_trigger: Compile-trigger — 4 правила по теме оркестрации агентов в ~/.claude/rules/ (agent-rotation, agentnet-ops orchestration parts, parallel-agents, runner-safety) + AgentNet — основной проект пользователя. Без единого стандарта каждый dispatch собирается с нуля, типичные ошибки (мёртвый агент в rotation, race на файле, абстрактный prompt) повторяются.
---

# Agent Orchestration Standard v0.0.1

## Job-to-be-done сценарии

Когда применять этот стандарт:

- **JTBD-1: Делегирование задачи AI-агенту** — выбрать правильный агент, написать prompt, получить рабочий output (не prose_only / scope creep)
- **JTBD-2: Параллельная работа нескольких агентов** — разбить большую задачу на N независимых частей без race conditions на файлах
- **JTBD-3: Mission coordinator recovery в AgentNet** — coordinator завис, нужно восстановить state без manual JSON хирургии
- **JTBD-4: Audit большой кодовой базы** — нужно ≥5 параллельных агентов с непересекающимися ролями, фазированный подход
- **JTBD-5: Fallback chain при отказе primary agent** — primary упал/занят, выбрать backup без потери retry-слотов на мёртвых агентах

## Точка G (output critria)

После применения стандарта:

- [ ] Каждый агент в dispatch rotation прошёл `check_readiness()` (не expired / not missing binary / has API key)
- [ ] Файлы между параллельными агентами не пересекаются (один файл — один агент)
- [ ] SSH operations и локальные правки запускаются в параллель (независимы)
- [ ] Bridge transport используется ПЕРЕД CDP при доступности
- [ ] Промпты содержат конкретный код (snippets, heredoc), не абстрактные описания
- [ ] Если mission coordinator завис — `force-reset --new-mission` использован ДО ручного JSON-hacking
- [ ] Агент редактирует только файлы внутри opened workspace ИЛИ передан явный project_path / inline-code
- [ ] Для audit: ≥5 ролей, фаза 1 = баги, фаза 2 = improvements
- [ ] Все file-based dispatchers имеют `if not path.exists(): skip` guard

## Методология

### §1. Health check перед добавлением агента в rotation

```python
def check_readiness(agent_id: str) -> bool:
    """Cache result для всей сессии (не дёргать на каждый retry)."""
    cached = _readiness_cache.get(agent_id)
    if cached is not None:
        return cached

    checks = {
        'binary_exists': _check_binary(agent_id),  # which claude / codex / gemini ...
        'subscription_active': _check_subscription(agent_id),  # API key valid
        'quota_available': _check_quota(agent_id),  # not throttled
        'config_valid': _check_config(agent_id),  # ~/.config/agent_id/config.toml
    }
    ready = all(checks.values())
    _readiness_cache[agent_id] = ready
    if not ready:
        log.warning(f"Agent {agent_id} not ready: {[k for k, v in checks.items() if not v]}")
    return ready

# В fallback chain:
agents_to_try = [a for a in PREFERRED_ORDER if check_readiness(a)]
# Мёртвый агент в chain = потерянный retry слот, длительный timeout перед fallback
```

**Запрет:** добавлять агента в fallback chain без health check. Каждый мёртвый агент = `dispatch_timeout` перед фактическим fallback.

### §2. Parallel split по файлам (no two agents touch same file)

**Принцип:** ни один файл не трогают два агента одновременно. Иначе — потерянные правки или merge conflicts.

```python
# ✅ Правильно: чёткое разделение по owned files
tasks = [
    {'agent': 'codex', 'owned_files': ['src/auth/login.py', 'src/auth/session.py']},
    {'agent': 'claude', 'owned_files': ['src/api/handlers.py', 'src/api/router.py']},
    {'agent': 'gemini', 'owned_files': ['tests/test_auth.py', 'tests/test_api.py']},
]
# Запускаем параллельно — collisions невозможны
```

```python
# ❌ Неправильно: оба агента могут править один файл
tasks = [
    {'agent': 'codex', 'task': 'add login endpoint'},  # → src/api/handlers.py
    {'agent': 'claude', 'task': 'add logout endpoint'},  # → src/api/handlers.py (race!)
]
```

**Контрольный вопрос перед параллельным запуском:**
- [ ] Для каждого task я знаю owned_files?
- [ ] Пересечений между tasks нет?
- [ ] Если есть пересечение — это явное dependency (sequential), не race

### §3. SSH || local parallelism

SSH-операции на remote host и локальные правки кода — **всегда параллелить**, они независимы по контексту:

```python
# Параллельно в одном сообщении (не sequential):
results = await asyncio.gather(
    ssh_remote_check_status(macmini),       # SSH operation
    edit_local_file('src/dispatcher.py'),   # Local edit
    update_local_tests('tests/'),           # Local edit
)
```

### §4. Bridge transport vs CDP

**Используй bridge first.** Bridge transport (например `sendPromptToAgentPanel` в Antigravity) **надёжнее CDP**:

| | Bridge | CDP |
|---|---|---|
| Reliability | High (direct API) | Medium (через DOM) |
| Speed | Fast | Slow (DOM updates) |
| Approval gates | Native handling | Часто failing (`isTrusted` check) |
| Use when | Доступен | Bridge недоступен ИЛИ нужен fine-grained control |

**Workflow:**
1. Try bridge first
2. Если bridge не отвечает 30s → fallback в CDP
3. Если CDP gate approval не работает (synthetic clicks) → cliclick с accessibility ИЛИ settings patch

### §5. Prompt design — конкретный код, не абстракции

**Правило:** давай агенту **конкретный код** (snippet, heredoc, точные file paths). Абстрактные prompts → scope creep ИЛИ prose_only output.

```python
# ✅ Правильно: конкретный код в prompt
prompt = """
CONTEXT: src/auth/login.py имеет stub функцию verify_password() на строке 42.
TASK: Заменить stub на:

```python
def verify_password(plain: str, hashed: str) -> bool:
    import bcrypt
    return bcrypt.checkpw(plain.encode(), hashed.encode())
```

OWNED FILES: src/auth/login.py
DONE WHEN: pytest tests/test_auth.py::test_verify_password passes
VERIFY: pytest tests/test_auth.py -v
"""
```

```python
# ❌ Неправильно: абстрактный prompt
prompt = "Пожалуйста, реализуй проверку пароля в auth модуле."
# Что получишь:
# - prose_only ("Вот как я бы это сделал...") без actual code change
# - Scope creep (рефакторит весь auth модуль вместо одной функции)
# - Wrong file (создал src/auth/password.py вместо edit в login.py)
```

### §6. Workspace boundary — где агент может редактировать

**Правило:** Agent редактирует файлы **только в opened workspace**. Для внешних проектов:

| Сценарий | Решение |
|---|---|
| Edit в opened workspace | Прямой prompt с file paths |
| Edit во внешнем проекте | Передай `project_path` + terminal routing В promt |
| Маленький fix во внешнем проекте | Inline-код в prompt с инструкцией "apply to /external/path" |
| Read-only изучение внешнего проекта | OK — read через ssh + paste output в context |

### §7. Mission coordinator recovery

**Workflow при freeze AgentNet mission coordinator:**

```bash
# 1. Сначала пробуй force-reset (НЕ ручной JSON-хакинг)
agentnet mission force-reset --new-mission

# 2. Только если force-reset не помог — diagnose state
agentnet mission status --verbose
ls /Users/georgilusikov/agentnet-v2-runtime/agentnet/data/missions/

# 3. Backup state перед manual edit
cp -R /Users/georgilusikov/agentnet-v2-runtime/agentnet/data/missions /tmp/missions-backup-$(date +%s)

# 4. Только теперь — ручной JSON edit (последний resort)
```

**Запрет:** ручное редактирование `mission_state.json` без backup и без попытки `force-reset` сначала.

### §8. Audit pattern для большой кодовой базы

Для systematic audit крупного codebase:

**Фаза 1 — Bug hunt (параллельно):**

| Агент | Роль | Owned area |
|---|---|---|
| codex | Security vulnerabilities | src/auth, src/api |
| claude | Logic bugs | src/business_logic |
| gemini | Performance issues | src/services |
| droid | Test coverage gaps | tests/ |
| jules | Configuration errors | configs/, .env files |

**Фаза 2 — Improvements (параллельно, после фазы 1):**

| Агент | Роль | Owned area |
|---|---|---|
| codex | Refactor security findings | dependent on phase 1 codex output |
| claude | Implement business logic fixes | ... |
| gemini | Performance optimizations | ... |
| droid | Add missing tests | ... |
| jules | Fix configurations | ... |

**Правило фазирования:** фаза 2 НЕ начинается пока фаза 1 не завершилась И findings не консолидированы. Иначе агенты фазы 2 работают по устаревшему контексту.

### §9. File-based dispatcher safety

Backlog файлы перемещаются между статусами `pending → processing → completed/failed` конкурентно. ВСЕГДА:

```python
# ✅ Guard pattern (обязательно)
def process_task(path: Path) -> None:
    if not path.exists():
        return  # task moved to another status concurrently
    data = path.read_text()
    ...
```

**Без guard:** `FileNotFoundError` в production при concurrent dispatch.

## Когнитивные искажения агента в этой области

### Dead agent in rotation
**Симптом:** Codex API key expired, но агент остался в fallback chain. Каждый failover = 60s timeout перед next agent. 5 уровней fallback × 60s = 5 минут на dispatch.
**Защита:** §1 — `check_readiness()` перед добавлением. Cache на сессию.

### Race condition через abstract task split
**Симптом:** «два агента, разные задачи в одном модуле» — оба правят `handlers.py`, второй overwrites первого.
**Защита:** §2 — owned_files ОБЯЗАТЕЛЬНО в task definition. Перед запуском — проверка пересечений.

### Bridge bypass illusion
**Симптом:** «bridge не работает, нужно через CDP» без реальной диагностики bridge. Уход в slow path без причины.
**Защита:** §4 — sequence (bridge first → 30s timeout → CDP fallback). Не сразу в CDP без причины.

### Abstract prompt = scope creep
**Симптом:** «Реализуй фичу X» → агент рефакторит 20 файлов «по пути» вместо одного fix.
**Защита:** §5 — CONSTRAINTS секция в каждом prompt с явным «DO NOT touch X, Y, Z».

### Premature manual JSON hacking
**Симптом:** mission завис → сразу `vim mission_state.json`. Backup нет, force-reset не пробовали.
**Защита:** §7 — force-reset обязательно ДО любого manual edit. Backup ОБЯЗАТЕЛЬНО.

### Cross-phase audit contamination
**Симптом:** Запустил фазу 2 (improvements) до того как фаза 1 (bugs) завершилась. Агенты фазы 2 работают по non-final code.
**Защита:** §8 — фазы строго sequential. Между ними — консолидация findings.

### File-not-found in concurrent dispatcher
**Симптом:** task file moved status concurrently → `FileNotFoundError` → dispatcher crash.
**Защита:** §9 — `if not path.exists(): return` guard перед каждым read.

## Связанные скиллы

- `/why` — для RCA когда dispatch упал (читать этот стандарт перед §1)
- `/check` — для §5 verify (правильно ли сформулирован prompt — gap table между task и output)
- `/triage` — если ≥3 гипотез почему агент не отвечает (bridge / CDP / health / config / network)
- `/falsify` — перед запуском большого audit (§8) для проверки что роли действительно непересекающиеся
- `/clean` — после фазы 1 audit перед фазой 2 (Problems = 0 после bugs phase)

## Changelog

- **0.0.1** (2026-04-19) — начальная версия. Compile из 4 rules: agent-rotation, agentnet-ops (orchestration parts), parallel-agents, runner-safety.

## FORBIDDEN в этой области

- Добавление агента в fallback chain без `check_readiness()` (потеря retry-слотов на мёртвых агентах)
- Запуск параллельных tasks без явного `owned_files` (race conditions)
- CDP-first вместо bridge-first без диагностики bridge
- Абстрактный prompt («реализуй X», «улучши Y») вместо конкретного кода
- Edit во внешнем проекте без `project_path` или inline-кода (agent изменит файл в неправильном месте)
- Ручной JSON-edit `mission_state.json` без backup и без `force-reset`
- Запуск phase 2 audit до завершения phase 1
- File-based dispatcher без `if not path.exists(): return` guard

## Hard fail

- §1 health check пропущен → каждый dispatch с long fallback timeouts
- §2 параллельные tasks без owned_files split → race на shared file
- §5 prompt без конкретного кода → prose_only output, потеря времени
- §7 ручной mission JSON edit без backup → потеря state, нет undo
- §9 file-based dispatcher без guard → FileNotFoundError crash в production
