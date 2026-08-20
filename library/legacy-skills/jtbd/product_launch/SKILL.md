---
skill_id: product_launch
name: Product Launch Agent (VANECHKA3000)
description: >
  Конвертирует результаты JTBD (Jobs-to-be-Done) исследований, Сегментацию и Графы Работ
  в готовую стратегию запуска продукта (Go-To-Market, GTM).
author: georgijlusikov
version: 1.0
domain: business/product
category: jtbd
triggers:
  - "product launch"
  - "запуск продукта"
  - "GTM strategy"
  - "go-to-market"
  - "VANECHKA"
dependencies:
  - jtbd/segmentation_b2c
  - jtbd/segmentation_b2b
  - jtbd/job_graph
category: jtbd
---

# Product Launch Agent (VANECHKA3000)

Этот навык основан на фреймворке В. Замесина и превращает сырые данные продуктовых исследований в action-план для маркетинга и продаж.

## Когда использовать
- У вас есть валидированный сегмент и Граф Работ (Core Job, разрывы, точка А/Б).
- Вы готовитесь к релизу (MVP или новой фичи).
- Вам нужно составить лендинг, рекламные месседжи или стратегию дистрибуции.
- Текущие каналы привлечения не работают (высокий CAC) и нужен рестарт на базе jtbd.

## Инструкции по запуску
Передайте агенту результаты предыдущих шагов (из `segmentation_b2c/b2b` или `job_graph`), а также описание текущего состояния продукта. Агент сгенерирует 4-этапную стратегию: Позиционирование, Каналы (Спусковые крючки), Месседжинг и План Экспериментов (A/B тесты гипотез).
