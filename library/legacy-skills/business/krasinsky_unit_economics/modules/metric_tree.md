# 🌳 Metric Tree Module

## Назначение
Построение иерархии метрик для декомпозиции цели (Profit) на рычаги управления.

## Ключевое Правило (Из курсов)
> "Инвариантное дерево метрик одинаково для всех бизнесов. Если формула экономически не сходится, вы что-то упустили."

## Инвариантное Дерево
```
Profit
 ├── Revenue
 │    ├── Users (Traffic * Conversion)
 │    ├── Average Check
 │    └── Repeat Purchases
 └── Costs
      ├── COGS (Variable)
      ├── Acquisition (Marketing)
      └── Fixed Costs (Opex)
```

## Алгоритм Кросс-Чека (PHs18.0)
Чтобы избежать ошибок в формулах, считайте `Gross Profit` двумя путями. Они **обязаны** совпасть.

1.  **Method A (Unit-based):**
    `User_Profit = CLV - CAC`
    `Total = User_Profit * Total_Users`
2.  **Method B (Accounting-based):**
    `Total = Revenue - (COGS + Marketing_Budget + Fixed)`

Если `Method A != Method B`, значит вы потеряли расходы (например, налоги или комиссию эквайринга).

## Формат Вывода
```markdown
### 🌳 Metric Tree Breakdown
*   **North Star:** Profit = $100k
    *   **Revenue:** $500k
        *   Avg Check: $50
        *   Orders: 10,000
    *   **Costs:** $400k
        *   Marketing: $100k
        *   COGS: $200k
```
