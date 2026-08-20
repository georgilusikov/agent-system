# Куда pull'ить skills (meta v3.1)

**Стержень:** Outcome Designer (что закрываем) + Goldratt (куда бить) + TRIZ (как менять).
JTBD-сценариум — опционально.

## В meta (delegate)

| Skill / agent | Pull когда | Слой |
|---------------|------------|------|
| **outcome-designer** | outcome, тикет-output, что получу, зачем задача | Q1 **core** |
| **1-critical-chain-design** | всё P0, план от конца, одно constraint | Q3 **core** |
| **leverage** | bottleneck, что тормозит целое, рычаг | Q3 **core** |
| **/triz** | упрости, FA, trim, ТП, ИКР, pre-mortem, C8 | Q4 |
| **anti-bias** | Choose ONE / trade-off | Q5 |
| **pizdej** | claims, что упустил | Q5 |
| **falsify** | релизить / опровергни | Q5 |
| **check** | Expected State vs артефакт | Q5 |
| **graphify** | код: что вызывает / поток | Q2 |
| **jtbd-scenarium-create** | только scenarium продукта/оффера | Q1 opt |
| **jtbd_triz_bridge** | явный JTBD↔TRIZ / силы прогресса | glue opt |

## Не в meta (прямой skill-routing)

| Skill | Почему |
|-------|--------|
| goal-plan, goal-king | волны / контракт делегирования |
| implement, writing-plans, delegate | delivery |
| debug | RCA бага |
| go | engineering start |
| bouncer, fusion | внешний second opinion / multi-model |
| prioritize | ранжирование **готового** списка (после leverage map) |
| handoff, teach, visual-explainer, … | другие jobs |
| Elena/Boris MCP | heavy only |

## Типичные «общие задачи» для eval (что меряем)

| Класс | Вопрос | Ожидаемый pull | Что улучшает meta |
|-------|--------|----------------|-------------------|
| **Aim** | Всё важно / куда бить | critical-chain / leverage | Фокус vs «улучши 10 вещей» |
| **Outcome** | Тикет = output only | outcome-designer | Output≠outcome, chain |
| **Aim+Change** | Горлышко + как упростить | pipeline P0/P3 + triz | Связка aim→change |
| Decision | N options | anti-bias | (уже есть T3) |
| Claims | production-ready? | pizdej | (T7) |
| Contradiction | A и B | triz | (T2) |
| Product who | для кого / scenarium | jtbd-scenarium **редко** | Не default |

## Не путать

| Похоже | Развести |
|--------|----------|
| leverage vs critical-chain | система thrash → leverage; план/шаги задачи → chain |
| outcome-designer vs jtbd-scenarium | задача/тикет → OD; продукт-оффер 9 частей → scenarium |
| unclear C8 vs OD | «физика симптомов» → C8; «зачем тикет» → OD |
| leverage vs prioritize | сначала constraint, потом rank списка |
