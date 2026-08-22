# Response Clarity Golden Examples

Use these synthetic checks for non-trivial default answers. They supplement,
not replace, `skills/feynman/SKILL.md` when its explicit trigger applies.

## 1. Slow lookup

**Unclear:** «Нужен индекс, запрос будет быстрее.»

**Clear:** «[Рекомендация] Add an index to `orders.created_at`. [O] The query
scans 1,000,000 rows. An index is a lookup list that points to matching rows;
for example, it is like a book's contents page instead of reading every page.
[I] It should reduce lookup time, but writes may become slower. Next: measure
the query before and after. Risk: the index uses disk space.»

**Checks:** outcome-first ✓; context ✓; term expanded ✓; example ✓; uncertainty
labels ✓; next step/risk ✓; exact facts preserved: `orders.created_at`,
`1,000,000` ✓.

## 2. Failed command

**Unclear:** «Команда упала, поправьте зависимости.»

**Clear:** «[O] `python3 scripts/check.py --repo` failed with
`AGENTS.md exceeds 245 lines`. The validator is the repository check that
rejects an oversized instruction file. [Рекомендация] Shorten `AGENTS.md`
without changing its rules. Next: remove repetition and rerun the command.
Risk: a shortened rule may lose a required condition.»

**Checks:** outcome-first ✓; context ✓; term expanded ✓; example not needed:
the command and error are concrete ✓; uncertainty labels ✓; next step/risk ✓;
exact facts preserved: `python3 scripts/check.py --repo`,
`AGENTS.md exceeds 245 lines`, `245` ✓.

## 3. Retry decision

**Unclear:** «Сеть нестабильна, повторим позже.»

**Clear:** «[Рекомендация] Retry `curl -I https://example.test` once after
checking DNS. [O] The last run returned `curl: (6) Could not resolve host`.
DNS is the address book that turns a site name into a network address; for
example, it finds the number behind a saved contact. [A] The failure may be
local rather than the site being down. Next: compare a second DNS lookup.
Risk: the next result can still be affected by a temporary network outage.»

**Checks:** outcome-first ✓; context ✓; term expanded ✓; example ✓; uncertainty
labels ✓; next step/risk ✓; exact facts preserved:
`curl -I https://example.test`, `curl: (6) Could not resolve host` ✓.

## 4. Migration choice

**Unclear:** «Миграция безопасна, запускайте.»

**Clear:** «[Рекомендация] Test the migration on a copy before applying it on
`2026-08-22`. [O] `ALTER TABLE invoices ADD COLUMN sent_at TEXT` changes the
table shape. A migration is a recorded database change; for example, it is a
numbered renovation step so every copy gets the same wall moved. [S] Existing
application code may assume the old shape. Next: run the migration and its
rollback on the copy. Risk: rollback can fail if later writes use `sent_at`.»

**Checks:** outcome-first ✓; context ✓; term expanded ✓; example ✓; uncertainty
labels ✓; next step/risk ✓; exact facts preserved:
`2026-08-22`, `ALTER TABLE invoices ADD COLUMN sent_at TEXT`, `sent_at` ✓.

## 5. Cache limit

**Unclear:** «Поставьте кэш на 300 секунд.»

**Clear:** «[Рекомендация] Cache the report for exactly `300` seconds. [O] The
same report is requested repeatedly. A cache is a temporary saved result; for
example, it is keeping today's printed timetable instead of asking the desk
again. [I] This should reduce repeated work. Next: confirm a changed report is
visible after `300` seconds. Risk: users can see data that is up to `300`
seconds old.»

**Checks:** outcome-first ✓; context ✓; term expanded ✓; example ✓; uncertainty
labels ✓; next step/risk ✓; exact facts preserved: `300` seconds ✓.
