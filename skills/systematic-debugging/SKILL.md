---
name: systematic-debugging
description: 'MERGED into /debug on 2026-10-01 (round-2 evals: no delta vs baseline). Use /debug instead — the escalation protocol and techniques live there.'
---

# Systematic Debugging — merged into /debug

Этот скилл **влит в `/debug`** 2026-10-01.

Основание: эвалы раунда 2 аудита скиллов (2026-10-01) — ни systematic-debugging,
ни debug не показали положительной дельты к baseline на задачах поиска корневых
причин; держать два отдельных скилла нечем обосновать.

Куда переехало содержимое:
- **Escalation «3+ неудачных фикса → вопрос архитектуре»** → `/debug` § «Escalation»
- **Рационализации** («emergency, нет времени», «ещё одна попытка») → `/debug` § «Escalation»
- **Диагностика на границах компонентов** → `/debug` § «Петля обратной связи»
- Техники остались файлами в этом каталоге и подключены из `/debug`:
  `root-cause-tracing.md`, `defense-in-depth.md`, `condition-based-waiting.md`
  (+ `find-polluter.sh`, примеры)

Используй `/debug`. Этот файл — указатель; каталог с техниками не удалён.
