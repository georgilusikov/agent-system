---
name: mac-mini-deploy
description: Методология deploy кода и агентов на Mac Mini runtime (`/Users/georgilusikov/agentnet-v2-runtime/`) + операции с Antigravity instance. Покрывает version mismatch, asyncio gotchas, Antigravity restart/unfreeze, runner safety.
version: 0.0.1
created: 2026-04-19
incident_trigger: Compile-trigger — 5 правил по теме deploy/runtime/Antigravity накопилось в ~/.claude/rules/ (deploy-remote, agentnet-ops, antigravity-cdp, antigravity-worktreeconfig, asyncio-atomicity, runner-safety). Решение — компилировать в единую методологию для облегчения onboarding и снижения когнитивной нагрузки при deploy.
---

# Mac Mini Deploy Standard v0.0.1

## Job-to-be-done сценарии

Когда применять этот стандарт:

- **JTBD-1: Deploy нового кода/фичи на Mac Mini runtime** — пушнул код локально, нужно прогнать на target host, проверить что работает с Python 3.9 и live runtime
- **JTBD-2: Reset/restart Antigravity instance после изменений** — поменял config, нужно перезапустить чисто без зависших gates от прошлой сессии
- **JTBD-3: Debug когда Antigravity молчит** — UI работает, агент не отвечает на промпты, нужна triage worktreeconfig vs другие причины
- **JTBD-4: Verify deploy через test dispatch** — деплой прошёл, надо доказать что один реальный prompt → реальный ответ от агента

## Точка G (output critria)

После применения стандарта (бинарные критерии PASS/FAIL):

- [ ] `ssh macmini 'python3 --version'` показал актуальную версию target (≥ 3.9, не 3.13 локальной)
- [ ] Все новые `.py` файлы содержат `from __future__ import annotations` (если target Python ≤ 3.10)
- [ ] AgentNet runtime запускается на target без `ImportError` / `SyntaxError`
- [ ] Один live dispatch до изменений + один после = оба вернули результат (не timeout, не prose_only)
- [ ] Если killали Antigravity — restart прошёл, surface_ready, нет pending gates от старой сессии
- [ ] `git status` на target чистый или объяснены неожиданные файлы

## Методология

### §1. Pre-flight check (обязательно ДО любого изменения кода)

```bash
# 1. Версия Python на target
ssh macmini 'python3 --version'
# Если 3.9 → обязательно `from __future__ import annotations` в новых файлах
# Если < 3.10 → НЕ использовать `X | None` без `eval_type_backport`

# 2. Состояние target git
ssh macmini 'cd /Users/georgilusikov/agentnet-v2-runtime/agentnet && git status'
# Чистый? Если есть uncommitted — выяснить что это перед pull

# 3. Активная сессия Antigravity
ssh macmini 'pgrep -lf Antigravity'
# Если активная — решить: убивать или работать с running

# 4. Логи runtime
ssh macmini 'tail -50 /Users/georgilusikov/Library/Logs/agentnet/dispatcher.log'
```

Чек-лист:
- [ ] target Python version известна
- [ ] target git status чистый или объяснён
- [ ] Antigravity состояние известно (running / dead)
- [ ] последние 50 строк лога runtime прочитаны

### §2. Adapt code to target (если target Python < 3.11)

```python
# ✅ Mac Mini Python 3.9 — ОБЯЗАТЕЛЬНО для type hints
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .types import SomeType  # avoid runtime import cost

def foo(x: int | None) -> str:  # works with future annotations on 3.9
    ...
```

```python
# ❌ Сломается на Python 3.9 без future annotations
def foo(x: int | None) -> str:  # SyntaxError или TypeError
    ...
```

### §3. Atomic asyncio gotchas (на Mac Mini agent dispatcher часто asyncio)

- **Read-modify-write в одной synchronous секции БЕЗ await** = атомарно в event loop. **Не помечать как race condition.**
- **`except Exception` НЕ ловит `KeyboardInterrupt` / `SystemExit`** (они BaseException). Это not bug.
- Перед static analysis от агента: предупреди что asyncio code, иначе агент будет ложно flag-ать «races».

### §4. Runner / dispatcher safety

Файлы backlog перемещаются между статусами `pending → processing → completed/failed` конкурентно. Перед чтением задачи из ФС:

```python
# ✅ Guard pattern
def process_task(path: Path) -> None:
    if not path.exists():
        return  # task moved to another status concurrently
    data = path.read_text()
    ...
```

```python
# ❌ FileNotFoundError в проде
def process_task(path: Path) -> None:
    data = path.read_text()  # crashes if task moved
    ...
```

### §5. Antigravity restart / unfreeze workflow

**Сценарий A: Antigravity молчит, UI работает**

```bash
# 1. Diagnose worktreeconfig issue
grep worktreeconfig ~/Library/Application\ Support/Antigravity/logs/*/ls-main.log | tail -5

# Если вижу:
# core.repositoryformatversion does not support extension: worktreeconfig
# workspace infos is nil
# → known bug, fix:

fix-antigravity  # alias или ~/bin/antigravity-unbreak.sh
# Удаляет [extensions] секцию из main .git/config
# НЕ бампать repositoryformatversion=1 — ломает одинаково

# 2. В Antigravity: Cmd+Shift+P → Developer: Reload Window
```

**Сценарий B: Restart Antigravity для применения изменений**

```bash
# 1. Kill чисто
killall Antigravity || pkill -9 -f Antigravity

# 2. Если патчишь state.vscdb — ТОЛЬКО сейчас (после kill)
sqlite3 ~/Library/Application\ Support/Antigravity/User/state.vscdb "..."

# 3. Старт
open -a Antigravity

# 4. Wait + verify
sleep 30  # surface_ready timing
# Проверь surface_ready через CDP перед первым dispatch:
curl -s http://localhost:9222/json | jq '.[] | select(.title == "...") | .url'

# 5. Pending gates от прошлой сессии блокируют новый input → проверь
```

**Запрет:** патчить `state.vscdb` пока Antigravity жив — IDE перезаписывает DB при shutdown, твои изменения потеряются.

### §6. Antigravity gate approval (если требуется автоматизация)

CDP synthetic clicks (`Input.dispatchMouseEvent`, JS `.click()`) **НЕ работают** на approval buttons из-за `isTrusted` check React-а.

**Работающие варианты:**
- `cliclick` с granted accessibility permissions
- Settings patch (`autoApprove: true` в Antigravity settings)

### §7. Verify deploy (обязательно ПОСЛЕ изменений)

Без этого шага deploy не считается выполненным:

```bash
# 1. Один реальный dispatch на простой задаче
agentnet dispatch --agent claude --prompt "echo test" --timeout 60

# 2. Проверь output
agentnet metrics --last 1
# task_status должен быть "completed", не "timeout" / "prose_only" / "failed"

# 3. Проверь логи на ошибки от старого кода
ssh macmini 'tail -100 /Users/georgilusikov/Library/Logs/agentnet/dispatcher.log | grep -E "Error|Exception|Traceback"'
```

## Когнитивные искажения агента в этой области

### Local Python version bias
**Симптом:** агент использует `X | None` в новом файле, не проверив что target Python — 3.9. Локально это работает (Python 3.13), на target — `TypeError: unsupported operand type(s) for |`.

**Защита:** ВСЕГДА `ssh target python3 --version` ДО написания кода с современным синтаксисом. Если ≤ 3.10 → `from __future__ import annotations` в каждом новом файле.

### False race condition flag (asyncio)
**Симптом:** агент видит `count = self.count; self.count = count + 1` в async function без await между и помечает как race condition. На самом деле — атомарно в event loop.

**Защита:** при анализе asyncio кода — не флажить read-modify-write секции без await. Если хочешь race — нужен await между.

### Confidence через ssh без verification
**Симптом:** «задеплоил, должно работать» без проверки `agentnet dispatch ... && check status`. Реально код может не подняться из-за version mismatch / missing dependency / corrupted state.

**Защита:** §7 verify обязателен. Один реальный dispatch до и после deploy. Без этого confidence в deploy = 50%.

### Premature `kill -9` без backup
**Симптом:** при freeze Antigravity сразу `pkill -9`. Незакоммиченные state и pending tasks теряются.

**Защита:** перед killall:
```bash
cp -R ~/Library/Application\ Support/Antigravity /tmp/antigravity-backup-$(date +%s)
agentnet metrics --last 5  # знать что было активно
```

### Worktreeconfig false positive
**Симптом:** Antigravity молчит → агент сразу делает RCA на «глюк CDP» / «зависший gate» / «сетевая ошибка» вместо проверки worktreeconfig в логах.

**Защита:** ПЕРВАЯ команда при «Antigravity молчит» — `grep worktreeconfig` в логах. Знакомая ошибка → знакомый fix.

## Связанные скиллы

- `/why` — для RCA когда deploy упал (читать этот стандарт перед §1)
- `/check` — для §7 verify (open dispatch artefact, gap table)
- `/falsify` — для critical-stakes deploy (например prod-критичный fix)
- `/clean` — финальная уборка после deploy (Problems = 0, нет дубликатов файлов)

## Changelog

- **0.0.1** (2026-04-19) — начальная версия. Compile из 6 rules: deploy-remote, agentnet-ops (deploy parts), antigravity-cdp, antigravity-worktreeconfig, asyncio-atomicity, runner-safety.

## FORBIDDEN в этой области

- Deploy без `ssh target python3 --version` (version mismatch гарантирован)
- Использование `X | None` синтаксиса в новом файле без `from __future__ import annotations` (если target Python ≤ 3.10)
- Patching `state.vscdb` пока Antigravity жив (изменения будут перезаписаны)
- Бамп `core.repositoryformatversion=1` как fix worktreeconfig (ломает одинаково)
- Маркировать deploy как «готово» без §7 verify через реальный dispatch
- `pkill -9 Antigravity` без backup state и без знания что было активно
- Помечать asyncio read-modify-write без await между как race condition

## Hard fail

- Стандарт прочитан, но §1 pre-flight пропущен → output невалиден
- §7 verify не выполнен (нет реального dispatch до/после) → deploy не считается завершённым
- Agent code на 3.9 target без future annotations → известная ошибка, повтор инцидента
