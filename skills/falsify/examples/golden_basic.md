# Golden: /falsify basic — учебный CLI-скрипт «готов к раздаче»

Эталонный вывод `/falsify` на безопасном учебном кейсе (без PII, без реальных клиентов).
Назначение: regression seed формата — любое изменение SKILL.md проверяется прогоном
против этого файла (`0-how-to-write-skills` §6 шаг 5.5). Показывает PARTIAL-ветку:
§10.5 обязателен, §8 Design Injection обязателен.

**Claim под фальсификацию:** «Скрипт `wordcount.py` готов к раздаче участникам курса —
запускается одной командой, без внешних зависимостей, на любом их файле».

---

```text
FALSIFY
```

## §0. Input Checklist

- [x] Есть конкретный claim (не «сделать хороший скрипт»)
- [x] Доступен SoT: `examples/wordcount.py`, `README.md`, терминал
- [x] Сформулировано 4 наблюдаемых ожидания ДО сбора фактов
- [x] Critical-stakes: раздача 40 участникам, откат = потеря занятия
- [x] Проверена `~/.claude/memory/incidents/`

`/anti-bias` применён к ожиданиям: автор скрипта = автор ожиданий → риск подгонки,
поэтому E03/E04 сформулированы как «что сломает», а не «что подтвердит».

## §1. Expectations table (E-ID)

| E-ID — название | Что должно быть истинно | Где подтверждать (SoT) | Next action if unmet | Effort (0-100) |
|---|---|---|---|---|
| E01 — запуск одной командой | `python3 wordcount.py sample.txt` печатает счётчик и завершается кодом 0 | Bash, stdout + `echo $?` | Починить точку входа `main(argv)`, повторить прогон | 0 |
| E02 — нет внешних зависимостей | В файле нет импортов вне stdlib | `grep -n "^import\|^from" wordcount.py` | Заменить внешний импорт на stdlib-аналог | 0 |
| E03 — пустой файл не роняет | На файле в 0 байт печатает `0`, а не traceback | Bash: `: > empty.txt && python3 wordcount.py empty.txt` | Добавить guard clause на пустой вход + тест | 0 |
| E04 — отсутствующий файл даёт понятную ошибку | Печатает одну строку с путём, exit code 2, без traceback | Bash: `python3 wordcount.py nope.txt; echo $?` | Обернуть чтение в `except FileNotFoundError` → сообщение + exit 2 | 0 |

Camera test: каждое ожидание = наблюдаемый stdout/exit code, не «скрипт удобный».

## §2. Precedent scan + actual evidence

### §2.1 Precedent scan

```bash
ls ~/.claude/memory/incidents/ 2>/dev/null
grep -ril "cli\|traceback" ~/.claude/memory/incidents/ 2>/dev/null | head -5
```

Precedent scan: найден 1 похожий инцидент — «раздали скрипт, у половины участников
traceback на своих данных, занятие потеряно». Сигнал: ошибка повторяется на классе
«тестировали только на своём файле» → §8 усиливает существующее правило, а не создаёт новое.

### §2.2 Gather actual

| E-ID | Actual (наблюдение) |
|---|---|
| E01 | `python3 wordcount.py sample.txt` → `words: 128`, `echo $?` → `0`. Прогон в этой сессии. |
| E02 | `grep -n "^import\|^from"` → `1:import sys`, `2:from pathlib import Path`. Оба stdlib. |
| E03 | `: > empty.txt && python3 wordcount.py empty.txt` → `words: 0`, exit `0`. |
| E04 | `python3 wordcount.py nope.txt` → `Traceback (most recent call last): … FileNotFoundError: [Errno 2] … 'nope.txt'`, exit `1`. Ожидался exit 2 и одна строка. |

### §2.3 Runtime Verification Gate

Claim про запускаемый скрипт → RUNTIME обязателен. Выполнено: 4 живых прогона через Bash,
stdout и exit code показаны выше дословно. Файлов-на-месте как evidence не использовалось.

### §2.5 Склейки данных

Не применяется: в claim нет join/merge/склейки сущностей по ключам.

## §3. Gap table (G-ID)

| G-ID — название | E-ID ref | Expected | Actual | Gap type | Severity | Root Cause (1 строка) | Fix | Next action if unmet | Effort |
|---|---|---|---|---|---|---|---|---|---|
| G01 — traceback на отсутствующем файле | E04 | одна строка + exit 2 | traceback `FileNotFoundError`, exit 1 | execution | high | чтение файла не обёрнуто, ошибочный путь не считался «нормальным входом» | `try/except FileNotFoundError` → `print(f"нет файла: {path}", file=sys.stderr)`, `return 2` | Если traceback остаётся — проверить, что `main` возвращает код, а не `raise` | 0 |
| G02 — тест-набор не покрывает чужие входы | E03, E04 | негативные кейсы в тестах | тестов нет, проверка только руками в этой сессии | feedback | medium | автор проверял на своём файле, класс «чужой вход» не был наблюдаем | добавить `--self-test` со случаями: пустой файл, отсутствующий файл, каталог вместо файла | Если `--self-test` зелёный, но участник падает — расширить набор его случаем | 0 |

### §3.1 Gap count

```text
Gap count
- total: 2
- open: 2
- partial: 0
- closed: 0
- highest severity: 3/5
```

## §4. 5 Whys для top-1 critical gap

Top-1 по severity: **G01 — traceback на отсутствующем файле**.

```
1. Почему участник видит traceback? → чтение идёт напрямую `Path(argv[1]).read_text()` (wordcount.py:14), без except
2. Почему без except? → ошибочный путь не входил в список входов, которые автор считал возможными
3. Почему не входил? → все прогоны делались на одном файле `sample.txt`, лежащем рядом со скриптом
4. Почему на одном файле? → нет `--self-test`, проверка = ручной запуск «работает ли вообще»
5. Почему нет --self-test? → в чек-листе готовности скрипта не было пункта про smoke на негативных входах ← корневая, процессная
```

## §6. Causal chain

```
Симптом → Промежуточная причина → Процессный дефект → Корневая причина → Design Injection
traceback у участника → нет обработки FileNotFoundError → тестировали одним ручным прогоном на своём файле → в критерии готовности не заложен smoke на негативных входах → пункт про --self-test в Definition of Done
```

`primary chain` одна, конкурирующих ветвей нет → §5 пропущен.

## §7. Blast radius

| Зона | Статус | Что проверить | Кто проверяет |
|---|---|---|---|
| `wordcount.py` подсчёт слов | не сломано | прогон на `sample.txt`: `words: 128` не изменился после фикса | agent |
| README с инструкцией запуска | требует проверки | упомянут ли exit code 2 как штатный | agent |
| Раздаточный архив курса | требует проверки | пересобран ли после фикса | owner |

## §8. Design Injection Point

```
Where: ~/.claude/skills/0-how-to-write-skills/SKILL.md
Section: Definition of Done
Text to inject: каждый scripts/*.py в скилле имеет --self-test (smoke без внешних deps)
Why this prevents recurrence: класс «проверял только на своём входе» перестаёт быть невидимым — smoke обязан покрыть негативный вход, иначе DoD не закрыт
```

Инъекция усиливает существующий пункт DoD, а не создаёт новую сущность (см. §2.1: ошибка повторяется).

## §9. Next-Action Digest

| P-ID — шаг | Closes gaps | Effort | Actor | Зачем первый |
|---|---|---|---|---|
| P01 — обернуть чтение в except + exit 2 | G01 | 0 | agent | снимает high-severity, разблокирует раздачу |
| P02 — добавить `--self-test` с 3 негативными входами | G02 | 0 | agent | закрывает feedback-gap, без него G01 вернётся |
| P03 — пересобрать раздаточный архив | — | 20 | owner | участники получают исправленную версию |

## §10. Verdict

**PARTIAL** — met 3/4 E-ID (E01, E02, E03), 0 critical, 1 high-gap с планом closure.

```
Уверенность: 70% → 88% — 4 живых прогона с показанным stdout и exit code; остаток
неопределённости: не проверен вход «каталог вместо файла» и не проверена кодировка
не-UTF-8 файла участника
```

## §10.5 Новая рабочая гипотеза

| Новая гипотеза | Чем лучше объясняет наблюдённые gaps | Что её опровергнет следующим |
|---|---|---|
| Скрипт корректен на «своём» входе автора и падает на любом входе, который автор не пробовал (отсутствующий файл, каталог, не-UTF-8) | Объясняет и G01, и G02 одной причиной — узкий набор проверенных входов, а не отдельный дефект | Прогон `--self-test` на 3 негативных входах: если все три дают одну строку и код 2 — гипотеза опровергнута |

## §11. Handoff

PARTIAL, severity high → JSONL incident + запуск P01/P02:

```bash
~/.claude/bin/log-incident.sh --kind falsify --severity medium --source /falsify \
  --target "skills/0-how-to-write-skills/SKILL.md" \
  --summary "CLI без smoke на негативных входах: traceback вместо сообщения"
```

```text
FALSIFY_FINAL: PARTIAL
```
