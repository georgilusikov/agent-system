---
skill_id: source_reliability_scorer
name: "Source Reliability Scorer"
description: "Оценка надёжности источника информации по 4 критериям (авторский track record, peer review, тип знания, ограничения)"
version: "1.0"
category: epistemology
source_lectures:
  - "Занятие 1.txt"
  - "Занятие 4.txt"
triggers:
  - "надёжность источника"
  - "source reliability"
  - "оценить источник"
  - "check source credibility"
---

# Source Reliability Scorer

## Обзор
Скилл для оценки надёжности источника информации. Используется агентами, которые ищут данные в интернете или проверяют факты. Основан на концепции «Эмет» (надёжность свидетельства) из Занятия 1 и трёх ограничениях (индивидуальное, культурно-историческое, языковое) из Занятия 4.

## Когда использовать
- При проверке фактических утверждений из внешних источников
- При конфликте между источниками
- При оценке аргументов, основанных на авторитете (Know-WHO)

## Инструкции
Загрузить: [core_instructions.md](./core_instructions.md)

## Связанные компоненты
- **Фреймворки:** `etymology_of_truth_framework` (Эмет-проверка), `absolute_vs_relative_truth_framework` (3 ограничения)
- **Агенты:** `correspondence_verifier`, `empiricist_analyzer`
- **Скиллы:** `epistemological_audit` (использует как подшаг)
