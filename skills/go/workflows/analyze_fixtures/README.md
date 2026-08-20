# analyze_fixtures

Тестовые наборы для проверки драфта `workflows/analyze.md` (cross-artifact consistency check) **до** его включения в /go.

## Зачем

Драфт analyze может давать:
- **false negatives** — пропускать реальные gaps (бесполезный детектор);
- **false positives** — галлюцинировать gaps там, где всё покрыто (блокирующий детектор, будет раздражать и его выключат).

Эти фикстуры проверяют оба режима.

## Структура

5 наборов, каждый — директория с 4 файлами:

| Набор | Тип | Что проверяет |
|---|---|---|
| `defective-01-missing-story/` | 🔴 gap | Детектор потерянных user stories (story в PRD, но нет в plan/issues) |
| `defective-02-orphan-issue/` | 🟡 warn | Детектор scope creep (issue без привязки к PRD) |
| `defective-03-missing-nfr/` | 🔴 gap | Детектор непокрытых NFR (security/performance/etc без implementation issue) |
| `clean-01-dark-mode/` | ✅ pass | False-positive check на простой фиче |
| `clean-02-profile-edit/` | ✅ pass | False-positive check на средней фиче (4 stories, 2 cross-cutting NFR, параллельные ветки) |

В каждой директории:
- `prd.md` — входной артефакт от write-a-prd
- `plan.md` — входной артефакт от prd-to-plan
- `issues.md` — входной артефакт от prd-to-issues
- `expected.md` — ground truth: что analyze ДОЛЖЕН найти (или не найти)

## Как прогнать

Для каждого из 5 наборов:

1. Открой в Claude новый чат (чистый контекст).
2. Дай инструкцию: «Прочитай драфт `workflows/analyze.md` и применй его к тройке файлов `analyze_fixtures/<name>/{prd,plan,issues}.md`. Верни отчёт строго в формате из analyze.md (🔴 GAPS / 🟡 WARNS / ✅ Coverage / Verdict)».
3. Сравни отчёт с `expected.md` по трём осям:
   - **GAPS совпадают** (по сути, не по формулировке): какие story/NFR указаны как непокрытые?
   - **WARNS совпадают**: какие orphan issues найдены?
   - **Verdict совпадает**: PASS / WARN / FAIL.

## Критерий принятия analyze.md

Драфт готов к интеграции в /go если:

- На **всех 3 defective** наборах analyze выдаёт правильный 🔴/🟡 verdict и идентифицирует правильный артефакт (gap story / orphan issue / uncovered NFR).
- На **обоих 2 clean** наборах analyze выдаёт ✅ PASS без галлюцинаций.

**Минимум 4/5 должны совпадать** — если хотя бы 2 из 5 не совпадают, драфт требует переработки.

## Что делать если драфт проваливается

- **False negative на defective (пропускает gap):** добавь в analyze.md явный чеклист-шаг для этого класса проблемы. Например, если пропустил NFR — добавь "Step 2.5: Для каждого NFR из раздела PRD 'NFR' — найди явное упоминание в issues".
- **False positive на clean (галлюцинирует gap):** проверь, не слишком ли жёсткая семантика matching'а (например, требует дословного совпадения текста story и issue AC вместо семантического).

## Время прогона

- Один набор: ~3 минуты (чтение + прогон Claude + сверка).
- Все пять: ~15-20 минут.
- Суммарная экономия против реальных фич: если драфт валиден — сразу включаем. Если нет — ловим баги до того, как analyze заблокирует настоящую работу.
