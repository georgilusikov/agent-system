---
skill_id: ab_testing_calculator
name: ab_testing_calculator
description: |
  Use when designing or evaluating A/B tests: calculate sample size, MDE, confidence intervals, statistical significance, and decide go/no-go.
  Based on PHs18 frequentist methodology + IS-RICE quick-eval framework.
  Output MUST include:
    - Acceptance table (E-ID rows, R6-compliant) перед запуском теста
    - Sample size + MDE calculation row (power-aware при launch decision)
    - Confidence interval analysis [O] (observed metric ± CI)
    - Power + significance verdict
    - Decision rubric: ship / iterate / kill
    - Calibrated confidence (до → после)
  Trigger phrases: "ab test", "split test", "MDE", "sample size", "конверсия", "стат значимость", "доверительный интервал", "тест разделения трафика"
category: business
triggers:
  - "ab test"
  - "split test"
  - "MDE"
  - "sample size"
  - "конверсия"
  - "стат значимость"
  - "доверительный интервал"
  - "тест разделения трафика"
dependencies: []
---

# A/B Testing Calculator

## Назначение
Frequentist расчёт A/B тестов: sample size, MDE, CI, статзначимость + бизнес-вердикт ship / iterate / kill. Не доказывает гипотезу — показывает только различие двух наборов данных.

## §0. Input checklist (preconditions)
- [ ] Определена baseline metric + observation window
- [ ] Определена target metric + business floor (что считаем "достаточным" эффектом)
- [ ] Известен доступный sample size или трафик в неделю
- [ ] Заданы α (по умолчанию 0.05) и power 1−β (по умолчанию 0.8)
- [ ] Определены stop-criteria (по выборке / по времени / sequential)
- [ ] Доступны raw logs (не только агрегаты) — для перерасчёта по сегментам

Если хоть один пункт `[ ]` не закрыт → не запускай расчёт, добери данные.

**R7 precedent scan:** not applicable — pure capability skill, no design injection produced. Скилл не порождает RCA-инциденты.

## §1. Quick decision flow (3 questions)
1. **Есть ли данные baseline?** → нет → переключись в IS-RICE качественную оценку (см. §6 cross-refs). Есть → шаг 2.
2. **Достижим ли MDE в доступном трафике за разумный срок?** → нет → уменьшай scope (1 сегмент, 1 метрика) или собирай больше данных. Да → шаг 3.
3. **Перекрывает ли CI зону "нет эффекта"?** → да → продолжай тест ИЛИ ship+monitor если cost ожидания > cost ошибки. Нет → принимай решение по верхней границе CI.

## §2. Calculator inputs / outputs
**Inputs:** baseline conversion rate `p`, MDE (absolute pp), α (default 0.05 → Z=1.96), power 1−β (default 0.8).
**Outputs:** required sample per arm `n`, total sample `2n`, time-to-result = `2n / weekly_traffic`.

### §2.1 Quick CI-only sample size (sanity check, не для launch)
`n ≈ Z² × p × (1−p) / MDE²`. Это нижняя оценка: учитывает только α, не учитывает power 1−β. Quick CI-only формула систематически недооценивает требуемую выборку для launch decision; масштаб зависит от power level (~3-4× при power=0.8, например baseline p=5%, MDE=0.5pp, α=0.05 → 7 300 vs 29 800 на вариант).

### §2.2 Power-aware sample size (mandatory for launch decisions)
`n = (Z_{α/2} + Z_{1-β})² × 2 × p × (1−p) / MDE²`, где `Z_{1-β} = 0.84` для power 0.8, `Z_{1-β} = 1.28` для power 0.9. Подробный вывод + worked examples + терминология SD vs SE: см. `references/methodology.md §2`.

Минимум выборки на вариант: **10 000** (правило из источника). Меньше — CI слишком широкий.

## §3. Acceptance table (Krasinsky R4/R6 — обязательна ДО запуска теста)

| E-ID — название | Что должно быть истинно | Где подтверждать (SoT) | Next action if unmet | Actor | Effort (0-100) |
|---|---|---|---|---|---|
| E01 — sample size sufficient | `n_per_arm ≥ max(10 000, power-aware n)` | calculator output + traffic dashboard | увеличить window / уменьшить число сегментов / переключиться на IS-RICE | analyst | 30 |
| E02 — MDE достижим в окне | `expected_effect ≥ MDE при доступном n` | расчёт §2.2 + сравнение с гипотезой | укрупнить scope гипотезы или увеличить трафик | analyst | 40 |
| E03 — α/power заданы явно | `α=0.05, power=0.8` указаны до запуска (не подбираются после) | планировочный документ / тикет | зафиксировать значения, добавить в pre-registration | owner | 20 |
| E04 — non-normal caveat проверен | для AOV / revenue / heavy-tail метрик — bootstrap CI или log-transform; для конверсии normal-approximation OK | обзор распределения метрики (histogram + skewness) | переключиться на bootstrap / Mann-Whitney / log-CI; см. methodology.md §9 | analyst | 60 |
| E05 — segmentation plan | заранее зафиксированы критические сегменты (Desktop/Mobile, гео, источник трафика) и multiple-comparison correction | планировочный документ + список сегментов | зафиксировать сегменты ДО запуска (anti-p-hacking); применить Bonferroni/BH | analyst | 50 |
| E06 — independence обеспечена | агрегация per-user (не per-transaction), исключены сотрудники, учтены аннуляции | spec на ETL агрегаций + segmentor config | переписать агрегацию per-user; добавить фильтры сотрудников и аннуляций | analyst+eng | 70 |

Если хоть один E-ID имеет `Next action if unmet` неснятым — тест не запускается.

## §3.5 Output template (после прогона теста)

| Метрика — название | Baseline [O] | Observed [O] | CI (95%) | MDE | Verdict |
|---|---|---|---|---|---|
| M1 — конверсия | p_A% | p_B% | ±x pp | ±y pp | ship / iterate / kill |
| M2 — средний чек | $A | $B | ±$ | ±$ | ship / iterate / kill |
| M3 — выручка/user | $A | $B | ±$ | ±$ | ship / iterate / kill |
| M4 — sample/power [O] | n_per_arm, achieved power | required n | — | — | sufficient / underpowered |

**Verdict rubric:**
- `ship` — `|Δ| > MDE` И статзначимо (Z>1.96 или p<α) И триада метрик согласована (конверсия+чек+выручка не противоречат) И achieved power ≥ 0.8.
- `iterate` — статзначимо, но Δ близко к MDE ИЛИ один сегмент противоречит aggregated ИЛИ underpowered.
- `kill` — `|Δ| < MDE` ИЛИ выборка недостаточна ИЛИ выручка падает при росте конверсии.

**Calibrated confidence:** `Уверенность: X% → Y% — [причина]`. Тег источников: `[O]`/`[I]`/`[A]` для ключевых утверждений.

## §4. FORBIDDEN
- Решение на основе только p-value без MDE и CI.
- Stop тест на первом peek значимости (sequential без α-correction).
- Игнор practical significance (статзначимо ≠ бизнес-значимо).
- Cite confidence без проверки sample size + MDE.
- Verdict только по конверсии без триады (конверсия + средний чек + выручка).
- Sample size < 10 000 на вариант без явной оговорки про сниженную мощность.
- Apply normal-approximation CI к AOV / revenue / heavy-tail метрикам без ЦПТ-проверки и non-normal caveat (см. `references/methodology.md §9`).
- Использовать per-transaction агрегацию когда один user может дать N покупок (зависимые наблюдения). Только per-user агрегация.
- Решение без raw logs (нельзя пересчитать по сегментам — не decision-ready).
- В сегментах не учтены outliers / аннуляции / сотрудники.

## §5. Hard fail
Output считается невыполненным, если:
- Нет §3 acceptance table с колонками `Что должно быть истинно`, `Где подтверждать`, `Next action if unmet`, `Actor`, `Effort (0-100)`.
- Нет §3.5 output table или она без MDE / без CI / без power-row.
- Output без явного MDE.
- Verdict без calibrated confidence.
- Recommendation `ship` без CI и проверки overlap с зоной "нет эффекта".
- Только агрегированный результат без разреза по критическим сегментам (Desktop/Mobile, география, источник трафика) при доступных данных.
- Sample size посчитан только §2.1 (CI-only) для launch decision — обязан быть §2.2 power-aware.
- Heavy-tail метрика (AOV / revenue) обработана normal-approximation без bootstrap / log-transform.

## §6. Cross-references (active)
- `references/methodology.md` — полные формулы (включая SD vs SE clarification §2), worked examples, common mistakes, ЦПТ caveat (§9), провенанс источников.
- `_provenance/AGENT.original.md` — оригинальный AGENT.md для аудита.

### §6.1 Future cross-refs (planned, not yet committed)
- `_agent_shared/skills/business/isrice_prioritizer/` — qualitative path когда нет данных (IS-RICE). **Status:** stub (только AGENT.md без SKILL.md). До завершения R9 миграции этого скилла — использовать материал AGENT.md вручную.
- `_agent_shared/skills/business/funnel_analyzer/` — upstream метрическое дерево. **Status:** planned R9 wave-2, ещё не создан.
