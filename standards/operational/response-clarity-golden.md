# Response Clarity Golden Examples

Use these synthetic checks for non-trivial default answers. They supplement,
not replace, `skills/feynman/SKILL.md` when its explicit trigger applies.

## 1. Slow lookup

**Unclear:** «Нужен индекс, запрос будет быстрее.»

**Clear:** «Рекомендация: добавить индекс для `orders.created_at`. Уверенность:
90% — [O] запрос просматривает 1,000,000 строк, поэтому поиск должен
ускориться. Индекс — это список указателей на подходящие строки; например, как
оглавление книги вместо чтения каждой страницы. [I] Запись может стать
медленнее. Следующий шаг: измерить запрос до и после. Риск: индекс займёт место
на диске.»

**Checks:** outcome-first ✓; context ✓; term expanded ✓; example ✓; uncertainty
labels ✓; next step/risk ✓; exact facts preserved: `orders.created_at`,
`1,000,000` ✓.

## 2. Failed command

**Unclear:** «Команда упала, поправьте зависимости.»

**Clear:** «Рекомендация: сократить `AGENTS.md`, не меняя его правил. Уверенность:
95% — [O] `python3 scripts/check.py --repo` завершилась с ошибкой
`AGENTS.md exceeds 245 lines`. Валидатор — это проверка репозитория, которая
отклоняет слишком длинный файл инструкций. Следующий шаг: убрать повторы и
снова запустить команду. Риск: в сокращённом правиле может потеряться важное
условие.»

**Checks:** outcome-first ✓; context ✓; term expanded ✓; example not needed:
the command and error are concrete ✓; uncertainty labels ✓; next step/risk ✓;
exact facts preserved: `python3 scripts/check.py --repo`,
`AGENTS.md exceeds 245 lines`, `245` ✓.

## 3. Retry decision

**Unclear:** «Сеть нестабильна, повторим позже.»

**Clear:** «Рекомендация: после проверки DNS один раз повторить
`curl -I https://example.test`. Уверенность: 70% — [O] последний запуск вернул
`curl: (6) Could not resolve host: example.test`. DNS — это адресная книга,
которая переводит имя сайта в сетевой адрес; например, находит номер по
сохранённому контакту. [A] Причина может быть на локальном компьютере, а сайт
может работать. Следующий шаг: сравнить второй результат поиска DNS. Риск:
временный сбой сети может повлиять и на следующий результат.»

**Checks:** outcome-first ✓; context ✓; term expanded ✓; example ✓; uncertainty
labels ✓; next step/risk ✓; exact facts preserved:
`curl -I https://example.test`, `curl: (6) Could not resolve host: example.test` ✓.

## 4. Migration choice

**Unclear:** «Миграция безопасна, запускайте.»

**Clear:** «Рекомендация: проверить миграцию на копии перед применением
`2026-08-22`. Уверенность: 85% — [O] `ALTER TABLE invoices ADD COLUMN sent_at TEXT`
меняет структуру таблицы. Миграция — это записанное изменение базы данных;
например, пронумерованный этап ремонта, чтобы в каждой копии передвинули одну
и ту же стену. [S] Существующий код приложения может рассчитывать на старую
структуру. Следующий шаг: выполнить миграцию и её откат на копии. Риск: откат
может не сработать, если последующие записи используют `sent_at`.»

**Checks:** outcome-first ✓; context ✓; term expanded ✓; example ✓; uncertainty
labels ✓; next step/risk ✓; exact facts preserved:
`2026-08-22`, `ALTER TABLE invoices ADD COLUMN sent_at TEXT`, `sent_at` ✓.

## 5. Cache limit

**Unclear:** «Поставьте кэш на 300 секунд.»

**Clear:** «Рекомендация: хранить отчёт в кэше ровно `300` секунд. Уверенность:
90% — [O] один и тот же отчёт запрашивают снова и снова. Кэш — это временно
сохранённый результат; например, распечатанное расписание на сегодня, которое
не нужно каждый раз спрашивать у стойки. [I] Это должно уменьшить повторную
работу. Следующий шаг: убедиться, что изменённый отчёт виден после `300` секунд.
Риск: пользователи могут видеть данные, которым не больше `300` секунд.»

**Checks:** outcome-first ✓; context ✓; term expanded ✓; example ✓; uncertainty
labels ✓; next step/risk ✓; exact facts preserved: `300` seconds ✓.
