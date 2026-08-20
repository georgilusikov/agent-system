---
skill_id: delegation_brief
skill_name: Delegation Brief (external executor protocol)
version: 1.0.0
category: workflow
triggers:
  - "делегируй"
  - "dispatch"
  - "запусти агента"
  - "поручи субагенту"
  - "бриф для"
  - "headless прогон"
dependencies: []
description: "Briefing protocol for delegating a task to an external executor (another agent, headless CLI, subagent, script). Three gates BEFORE dispatch: full domain canon read, expected output built as few-shot exemplar, executor constraints verified (permissions, workdir, runtime). Post-verify by artifacts, not self-report. Output MUST include: executor preflight checklist, brief in order exemplar -> prohibitions -> task, command-verifiable acceptance criterion, post-verify by files. NOT for: parallelizing own work across worktrees; choosing what to delegate (use ISRICE prioritization)."
---

# Delegation Brief — брифинг внешнего исполнителя

Root cause большинства провалов делегации — брифинг, не исполнитель: неполный канон,
нет эталона, неизвестные ограничения, permission gate. Три гейта ДО dispatch, один ПОСЛЕ.

## Когда НЕ применять

- Задача — 1 файл / 15 минут своей работы → делай сам
- Research-вопрос без артефакта → обычный вопрос субагенту, протокол избыточен

## §1. Expected State (до dispatch)

3-5 наблюдаемых ожиданий: какие файлы/строки/тесты будут существовать при успехе,
какой командой проверишь. Формулируется ДО dispatch.

## §2. Гейт 1 — Read-before-delegate

Прочитай ВСЕ файлы канона домена сам: схема + валидатор + скрипты + 2-3 образца из базы.
Один файл = частичный канон. Что не читал ты — не попадёт в бриф; исполнитель
восстановит семантику из СВОЕГО training, не твоего.

## §3. Гейт 2 — Expected output FIRST

До вызова напиши эталонный результат на 1 реальном примере руками, включи в бриф
как few-shot. Порядок брифа строго: **эталон → запреты → задача**.
Не можешь построить эталон = не понимаешь задачу = делегировать рано.

## §4. Гейт 3 — ограничения исполнителя (preflight)

| Проверка | Типовой fail |
|---|---|
| Права на запись (флаги, permission mode) | «goal-режим ничего не сделал» = permission gate |
| Workdir / контекст исполнения | backlog lane работает в окне агента, не в произвольном dir |
| Runtime на target (`python3 --version`) | modern-синтаксис падает на старом Python |
| Health-probe канала до пакета | деградированный language server, зависший auth |
| Фактическая роль исполнителя | рецензент ≠ кодер: ревью да, фича нет |

Пакетный enqueue — только после одной успешной тестовой задачи через тот же канал.
Тестовая задача заодно даёт замер времени для ETA пакета.

## §5. Бриф (шаблон)

```
КОНТЕКСТ: {2-4 строки: система, цель, границы}
ЭТАЛОН: {готовый пример результата на 1 реальном входе}
ЗАПРЕТЫ: {3-7 конкретных: форматы, файлы-не-трогать, no _fixed/_final, no новых файлов}
ЗАДАЧА: {императив + входы + куда положить результат}
ACCEPTANCE: {команда/grep, которой результат будет проверен}
```

## §6. Post-verify

- Self-report «done» / зелёный статус runner'а = claim, не факт. Формальный FAIL
  (timeout) тоже ≠ реальный FAIL. Верифицируй по файлам: `ls`, `grep`, тесты, diff
  против эталона.
- Прогони acceptance-команду сам.
- Wiring-задача → прочитай runtime-consumer: читает ли он ИМЕННО записанное поле.
- Расхождение → чини БРИФ и перезапускай, не дочинивай руками молча.

## Известные грабли

- Permission gate: «агент ничего не сделал» — отсутствие прав, не тупость
- Один файл = частичный канон → исполнитель нарушил невидимое правило
- Без эталона → формат из чужого training
- Деградированный канал: зависание списали на сложность задачи, причина — language
  server; probe + рестарт канала ДО смены модели/аккаунта

## FORBIDDEN

- Dispatch без эталона в брифе
- Пакетный enqueue без тестовой задачи
- Принимать self-report как верификацию
- Выдумывать результат acceptance-команды (no-fabricated-evidence)
- Молча дочинивать результат руками вместо фикса брифа

## Hard fail

- Бриф без секций ЭТАЛОН и ACCEPTANCE → пожелание, не делегация
- «Готово» при непройденной acceptance-команде → false done
- Preflight пропущен для нового канала → результат непредсказуем by design
