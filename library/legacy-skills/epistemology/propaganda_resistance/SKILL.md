---
skill_id: propaganda_resistance
name: "Propaganda Resistance"
description: "Выявление риторических и психологических приёмов пропаганды, эксплуатирующих схемы человеческого мышления (Theory of Mind)"
version: "1.0"
category: epistemology
source_lectures:
  - "Занятие 1.txt"
triggers:
  - "пропаганда"
  - "propaganda"
  - "манипуляция"
  - "risorical tricks"
  - "theory of mind attack"
---

# Propaganda Resistance

## Обзор
Скилл для выявления пропагандистских приёмов, которые *встраиваются в схемы рассуждений* читателя/слушателя и подводят его к заранее заготовленному выводу. Основан на концепции Theory of Mind и анализе пропаганды из Занятия 1.

## Отличие от `manipulation_detector`
- `manipulation_detector` ищет **эпистемологические подмены** (подмена теории истины, типа знания) — работает на уровне логики.
- `propaganda_resistance` ищет **риторические и психологические приёмы** — работает на уровне Theory of Mind (как пропагандист моделирует ваше мышление).

## Когда использовать
- При анализе политических текстов, речей, публикаций
- При подозрении на пропагандистское воздействие
- Как дополнительный слой к `manipulation_detector`

## Инструкции
Загрузить: [core_instructions.md](./core_instructions.md)

## Связанные компоненты
- **Скиллы:** `manipulation_detector` (эпистемологический слой)
- **Агенты:** `theory_of_mind_analyzer`, `objectivity_practitioner`
- **Фреймворки:** `claim_anatomy_framework` (разбор утверждения)
