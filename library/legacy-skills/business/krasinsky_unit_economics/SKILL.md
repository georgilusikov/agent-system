---
skill_id: krasinsky_unit_economics
skill_name: Krasinsky Unit Economics (The Calculator)
version: 3.0.0
category: analysis
description: "The official Krasinsky Unit Economics Calculator. Calculates Contribution Margin, LTV/CAC, and Scalability using the Pizdej Protocol."
source_lectures:
  - file: "PHs18. Испытание 5.txt"
    context: "Unit Economics Logic, Pizdej Protocol, Cross-checks"
modules:
  - file: "modules/metric_tree.md"
  - file: "modules/funnel.md"
  - file: "modules/cohorts.md"
  - file: "modules/growth_levers.md"
  - file: "modules/pricing.md"
  - file: "modules/viability_check.md"

---

# 📊 Krasinsky Unit Economics (The Calculator)

## 🎯 Назначение
Этот скилл **СЧИТАЕТ** экономику. Не раздает советы, а выдает цифры:
1.  **Сходится ли экономика?** (LTV/CAC > 3)
2.  **Сколько денег теряем на одном пользователе?**
3.  **Где точка безубыточности?**

## 🩸 The Pizdej Protocol (Алгоритм Расчета)

### Шаг 1: Сбор Данных (Input)

```python
# Базовые переменные
User_Acquisition_Cost (CPA) = Marketing_Budget / Total_Paying_Users
Average_Revenue_Per_User (ARPU) = Total_Revenue / Total_Paying_Users
COGS_Per_User (Variable_Cost) = (Server + Support + License) / Total_Users
```


### Шаг 2: Расчет Contribution Margin (Денег с юнита)

```python
Contribution_Margin (CM) = ARPU - COGS_Per_User - CPA
```

*   Если `CM < 0`: **PIZDEJ**. Мы масштабируем убытки. Остановите рекламу.
*   Если `CM > 0`: Можно масштабировать, но проверяем Fixed Costs.

### Шаг 3: Cross-Check (Проверка на вшивость)
Мы сравниваем `Unit Profit` с `Accounting Profit`. Они должны совпасть.

```python
Unit_Based_Profit = (CM * Total_Users) - Fixed_Costs
Accounting_Profit = Revenue - (All_Variable_Costs + Marketing + Fixed_Costs)

assert Unit_Based_Profit == Accounting_Profit
```

Если не совпадает -> Вы потеряли расходы (обычно налоги, комиссии или "прочие").

### Шаг 4: Вердикт (Output)
1.  **Масштабируемость:** Есть ли запас по CM?
2.  **Точки Роста:** Что дешевле поднять — ARPU или Конверсию? (см. `modules/growth_levers.md`)

## 🛠 Инструкция для ИИ
Когда пользователь просит "Посчитай экономику" или "Проверь стартап":

1.  **Запроси эти 4 цифры:**
    *   `UA` (Users Acquired / Трафик)
    *   `C1` (Conversion Rate) или кол-во покупателей
    *   `Price` (Средний чек)
    *   `Cost` (Маркетинг бюджет + COGS)

2.  **Выполни расчет по формуле:**
    `Profit = Users * (Price * Conv - COGS - CPA) - Fixed`

3.  **Выдай ответ в формате "Красинского":**
    *   Жесткий вердикт (Scale или Die).
    *   Покажи `Unit Loss/Profit`.
    *   Дай рекомендацию через `modules/growth_levers.md`.

## 🔮 Reverse Unit Economics (Моделирование Будущего)
Пользователь часто спрашивает: "Прикинь экономику гипотезы".
**Алгоритм:** Идите от желаемой прибыли к допустимой цене клика (CPA).

1.  **Цель:** "Хочу $10k прибыли в месяц".
2.  **Факт:** "У нас чек $100, маржа 50% ($50 с юнита)".
3.  **Расчет Необходимого Объема:**
    *   `Required Units (Buyers)` = `($10k + Fixed Costs) / $50 Margin`.
    *   Если Fixed = $5k -> Нужно 300 продаж.
4.  **Расчет Допустимой Рекламы (CPA Limit):**
    *   Если конверсия 1% -> Нужно 30,000 кликов.
    *   `Max Marketing Budget` = `Price * Buyers * (Target ROI / 100)`.

**Инструкция: Всегда спрашивайте "Какую прибыль вы хотите?" и считайте "обратным ходом" (Back-calculation).**


## 💡 Idea Validation (Проверка "На Салфетке")
>> **Используйте модуль:** `modules/viability_check.md` для детальной проверки.

Пользователь дает только идею: "Хочу делать Uber для выгула собак".
**Ваша задача:**
1.  **Определите Модель** и **Dead Zone** (см. Channel/Price Matrix).
2.  **Запустите STOP-Checklist**: Не нарушает ли идея базовые законы?
3.  **Посчитайте Viability:** `(C1 * Price) - (CPA + COGS)`.

**Пример диалога:**
User: "Приложение для медитаций по подписке $5".
Krasinsky: "Давайте проверим по чек-листу (viability_check).
*   **Цена:** $5 (< $10). Это зона 'Automatic Sales'. Вы не можете позволить себе sales-менеджеров.
*   **Channel:** Нужен виральный органический рост или SEO. Paid Ads ($5-10 CPA) убьют экономику.
*   **Viability:** $5 * 5% (Conv) = $0.25 выручки с визита. Если клик стоит > $0.20 — вы мертвы.
*   **Вердикт:** Очень рискованно. Либо поднимайте чек, либо ищите бесплатный трафик."

## Пример Диалога
**User:** У нас 1000 юзеров, платим $500 за рекламу, чек $10.
**Krasinsky:**
*   **CAC:** $0.5
*   **ARPU:** $10
*   **Profit:** $9,500
*   **Вердикт:** Экономика сходится. Какой у вас COGS? Если сервер стоит $9,000, то вы банкроты.

## Modules (Подмодули)
*   **Funnel:** Если проблема в `Conversion` -> `modules/funnel.md`
*   **Cohorts:** Если проблема в `LTV` -> `modules/cohorts.md`
*   **Levers:** Что крутить? -> `modules/growth_levers.md`
