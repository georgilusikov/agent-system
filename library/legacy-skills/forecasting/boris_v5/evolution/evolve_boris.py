#!/usr/bin/env python3
"""
🧬 Boris Evolution System
Дарвиновская эволюция оркестратора Boris через мутации и отбор.

Использование:
    python evolve_boris.py --generations 10 --population 6

Принцип работы:
1. Популяция вариантов Boris (разные промпты/инструкции)
2. Каждый вариант прогоняется на benchmark задачах
3. Fitness = качество отчёта по метрикам
4. Отбор лучших + мутации через агентов (Elena, Xerox, VANECHKA)
5. Новое поколение
"""

import os
import json
import yaml
import random
import hashlib
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Callable
from pathlib import Path
from datetime import datetime

# ============================================
# DATA STRUCTURES
# ============================================

@dataclass
class BorisVariant:
    """Один вариант Boris (генотип)"""
    id: str
    prompt_additions: List[str]  # Добавки к base prompt
    mutator_history: List[str]   # Какие мутаторы применялись
    fitness: float = 0.0
    generation: int = 0
    parent_ids: List[str] = field(default_factory=list)

    def to_prompt(self, base_prompt: str) -> str:
        """Собирает полный промпт из базы + добавок"""
        additions = "\n\n".join(self.prompt_additions)
        return f"{base_prompt}\n\n## Дополнительные инструкции (эволюция)\n\n{additions}"


@dataclass
class TestCase:
    """Тестовый кейс для оценки Boris"""
    id: str
    input: str
    expected_sections: List[str]
    golden_insights: List[str]


@dataclass
class EvaluationResult:
    """Результат оценки одного варианта на одном тесте"""
    variant_id: str
    test_id: str
    output: str
    scores: Dict[str, float]
    total_fitness: float
    found_sections: List[str]
    found_insights: List[str]
    penalties: List[str]


# ============================================
# MUTATORS (Агенты как улучшатели)
# ============================================

class Mutator:
    """Базовый класс мутатора"""

    def __init__(self, name: str, focus: str, weight: float):
        self.name = name
        self.focus = focus
        self.weight = weight

    def mutate(self, variant: BorisVariant) -> BorisVariant:
        """Применяет мутацию к варианту"""
        raise NotImplementedError


class ElenaTRIZMutator(Mutator):
    """Мутатор через Elena ТРИЗ"""

    TRIZ_ADDITIONS = [
        """### ТРИЗ-усиление (Elena)
- При анализе ВСЕГДА ищи противоречия: что нужно улучшить И что при этом ухудшается
- Формулируй TC (техническое противоречие) в формате: "Если [улучшим X], то [ухудшится Y]"
- Для каждого TC предлагай 2-3 принципа разрешения из 40 принципов ТРИЗ
- Используй IKR (идеальный конечный результат): "Система САМА [делает функцию], используя [бесплатные ресурсы]"
""",
        """### Ресурсный анализ (Elena)
- Найди 5+ скрытых ресурсов в системе (время, пространство, информация, энергия, вещество)
- Для каждого ресурса: как его можно использовать бесплатно?
- Найди "мусор" системы — что выбрасывается, но может быть полезно?
""",
        """### Trimming (Elena)
- Какие компоненты можно убрать, передав их функции другим?
- Какую функцию можно передать надсистеме бесплатно?
- Какой компонент "паразит" — потребляет ресурсы, но не даёт ценности?
""",
    ]

    def mutate(self, variant: BorisVariant) -> BorisVariant:
        addition = random.choice(self.TRIZ_ADDITIONS)
        new_variant = BorisVariant(
            id=f"{variant.id}_elena_{random.randint(1000, 9999)}",
            prompt_additions=variant.prompt_additions + [addition],
            mutator_history=variant.mutator_history + ["elena_triz"],
            generation=variant.generation + 1,
            parent_ids=[variant.id]
        )
        return new_variant


class XeroxCompetitiveMutator(Mutator):
    """Мутатор через Xerox конкурентный анализ"""

    COMPETITIVE_ADDITIONS = [
        """### Конкурентный анализ (Xerox)
- Для КАЖДОГО конкурента построй: Features Matrix, Pricing Tiers, Tech Stack
- Найди "дыры" — что конкуренты НЕ делают, но клиенты хотят
- Определи: лидер копируем или обходим? Почему?
- Anti-system: кто может "убить" этот рынок? (платформы, регуляторы, замена)
""",
        """### Benchmark Patterns (Xerox)
- Найди 3+ аналога в других индустриях (что похоже по PoA?)
- Для каждого аналога: что сработало, что провалилось, почему
- Какой паттерн успеха можно перенести?
""",
        """### Pricing Intelligence (Xerox)
- Собери pricing всех конкурентов: Free/Starter/Pro/Agency/Enterprise
- Вычисли: средняя цена сегмента, WTP ceiling, price anchoring
- Где "премиум gap" — можно брать больше за уникальность?
""",
    ]

    def mutate(self, variant: BorisVariant) -> BorisVariant:
        addition = random.choice(self.COMPETITIVE_ADDITIONS)
        new_variant = BorisVariant(
            id=f"{variant.id}_xerox_{random.randint(1000, 9999)}",
            prompt_additions=variant.prompt_additions + [addition],
            mutator_history=variant.mutator_history + ["xerox_competitive"],
            generation=variant.generation + 1,
            parent_ids=[variant.id]
        )
        return new_variant


class VanechkaJTBDMutator(Mutator):
    """Мутатор через VANECHKA JTBD"""

    JTBD_ADDITIONS = [
        """### JTBD Deep Dive (VANECHKA)
- Найди 3 уровня Job: Functional → Emotional → Social
- Для каждого Job: что "нанимают" сейчас? Почему "увольняют"?
- 4 Forces: Push (что отталкивает от текущего), Pull (что притягивает к новому),
  Anxiety (страхи перед новым), Habit (инерция текущего)
- Вердикт: Push + Pull > Anxiety + Habit? Если нет — STOP или Pivot
""",
        """### Switching Cost Analysis (VANECHKA)
- Какова реальная стоимость переключения? (время, деньги, данные, привычки)
- Что "держит" в текущем решении? (lock-in, network effects, sunk cost)
- Как снизить switching cost до нуля?
""",
        """### Non-Consumption (VANECHKA)
- Кто НЕ использует существующие решения и почему?
- Какие ограничения (деньги, время, навыки, доступ) мешают?
- Как сделать решение доступным для non-consumers?
""",
    ]

    def mutate(self, variant: BorisVariant) -> BorisVariant:
        addition = random.choice(self.JTBD_ADDITIONS)
        new_variant = BorisVariant(
            id=f"{variant.id}_vanechka_{random.randint(1000, 9999)}",
            prompt_additions=variant.prompt_additions + [addition],
            mutator_history=variant.mutator_history + ["vanechka_jtbd"],
            generation=variant.generation + 1,
            parent_ids=[variant.id]
        )
        return new_variant


class NapoleonUXMutator(Mutator):
    """Мутатор через Napoleon UX (Execution Pilot)"""

    UX_ADDITIONS = [
        """### Report Clarity (Napoleon)
- Каждый раздел начинается с 1-sentence summary (BLUF - Bottom Line Up Front)
- Используй bullet points, не сплошной текст
- Таблицы для сравнений, mermaid для flows
- Verdict ВСЕГДА в начале, reasoning после
""",
        """### Actionability (Napoleon)
- Каждый вывод → конкретное действие (кто, что, когда, как измерить)
- Experiments должны иметь: гипотеза, метрика, срок, owner
- Next Steps: 3 уровня (immediate/short-term/long-term)
""",
        """### Evidence Discipline (Napoleon)
- КАЖДОЕ утверждение помечай: [OBS] [DATA] [REF] [DERIVE] [ASSUME] [SPEC]
- [ASSUME] без теста → снижает Confidence на 5%
- Все числа должны иметь источник или пометку [ASSUME]
""",
    ]

    def mutate(self, variant: BorisVariant) -> BorisVariant:
        addition = random.choice(self.UX_ADDITIONS)
        new_variant = BorisVariant(
            id=f"{variant.id}_napoleon_{random.randint(1000, 9999)}",
            prompt_additions=variant.prompt_additions + [addition],
            mutator_history=variant.mutator_history + ["napoleon_ux"],
            generation=variant.generation + 1,
            parent_ids=[variant.id]
        )
        return new_variant


# ============================================
# FITNESS EVALUATION
# ============================================

class FitnessEvaluator:
    """Оценщик качества отчёта Boris"""

    def __init__(self, weights: Dict[str, float], penalties: Dict[str, int]):
        self.weights = weights
        self.penalties = penalties

    def evaluate(self, output: str, test_case: TestCase) -> EvaluationResult:
        """Оценивает один output на одном тесте"""
        scores = {}
        found_sections = []
        found_insights = []
        penalty_list = []

        # 1. Completeness: все секции заполнены
        for section in test_case.expected_sections:
            if section.lower() in output.lower() or self._fuzzy_match(section, output):
                found_sections.append(section)
        scores['completeness'] = len(found_sections) / len(test_case.expected_sections)

        # 2. Evidence tags
        evidence_tags = ['[OBS]', '[DATA]', '[REF]', '[DERIVE]', '[ASSUME]', '[SPEC]']
        tag_count = sum(output.count(tag) for tag in evidence_tags)
        scores['evidence_tags'] = min(1.0, tag_count / 10)  # 10+ тегов = max

        # 3. Actionability
        action_keywords = ['next step', 'эксперимент', 'experiment', 'тест', 'измерить',
                          'metric', 'срок', 'владелец', 'owner', 'действие']
        action_count = sum(1 for kw in action_keywords if kw.lower() in output.lower())
        scores['actionability'] = min(1.0, action_count / 5)

        # 4. Insight quality (golden insights found)
        for insight in test_case.golden_insights:
            if self._fuzzy_match(insight, output):
                found_insights.append(insight)
        scores['insight_quality'] = len(found_insights) / len(test_case.golden_insights) if test_case.golden_insights else 0.5

        # 5. Structure (шаблон соблюдён)
        structure_markers = ['## ', '### ', '| ', '- ', '```', 'mermaid']
        structure_count = sum(output.count(m) for m in structure_markers)
        scores['structure'] = min(1.0, structure_count / 20)

        # Apply penalties
        total_penalty = 0
        if 'verdict' not in output.lower() and 'go' not in output.lower():
            total_penalty += self.penalties.get('no_verdict', 0)
            penalty_list.append('no_verdict')
        if 'эксперимент' not in output.lower() and 'experiment' not in output.lower():
            total_penalty += self.penalties.get('no_experiments', 0)
            penalty_list.append('no_experiments')

        # Calculate total fitness
        weighted_score = sum(scores[k] * self.weights.get(k, 0) for k in scores)
        total_fitness = max(0, weighted_score * 100 + total_penalty)

        return EvaluationResult(
            variant_id="",  # Fill in later
            test_id=test_case.id,
            output=output,
            scores=scores,
            total_fitness=total_fitness,
            found_sections=found_sections,
            found_insights=found_insights,
            penalties=penalty_list
        )

    def _fuzzy_match(self, needle: str, haystack: str) -> bool:
        """Нечёткий поиск — ищем ключевые слова"""
        keywords = needle.lower().split()
        # Если половина слов найдена — считаем match
        found = sum(1 for kw in keywords if kw in haystack.lower())
        return found >= len(keywords) * 0.5


# ============================================
# EVOLUTION ENGINE
# ============================================

class BorisEvolution:
    """Основной движок эволюции"""

    def __init__(self, config_path: str):
        with open(config_path) as f:
            self.config = yaml.safe_load(f)

        self.population: List[BorisVariant] = []
        self.test_cases: List[TestCase] = []
        self.mutators: List[Mutator] = []
        self.evaluator: FitnessEvaluator = None
        self.best_ever: Optional[BorisVariant] = None
        self.history: List[Dict] = []

        self._setup()

    def _setup(self):
        """Инициализация компонентов"""
        # Mutators
        self.mutators = [
            ElenaTRIZMutator("elena_triz", "ТРИЗ", 0.25),
            XeroxCompetitiveMutator("xerox_competitive", "Конкуренты", 0.20),
            VanechkaJTBDMutator("vanechka_jtbd", "JTBD", 0.25),
            NapoleonUXMutator("napoleon_ux", "UX", 0.15),
        ]

        # Test cases
        for tc_config in self.config['benchmark']['test_cases']:
            self.test_cases.append(TestCase(
                id=tc_config['id'],
                input=tc_config['input'],
                expected_sections=tc_config['expected_sections'],
                golden_insights=tc_config['golden_insights']
            ))

        # Evaluator
        self.evaluator = FitnessEvaluator(
            weights=self.config['fitness']['weights'],
            penalties=self.config['fitness']['penalties']
        )

    def initialize_population(self) -> List[BorisVariant]:
        """Создаёт начальную популяцию"""
        population = []
        pop_size = self.config['population']['size']

        for i in range(pop_size):
            # Каждый вариант стартует с одной случайной мутацией
            mutator = random.choice(self.mutators)
            base_variant = BorisVariant(
                id=f"v0_{i}",
                prompt_additions=[],
                mutator_history=[],
                generation=0
            )
            mutated = mutator.mutate(base_variant)
            mutated.generation = 0  # Reset to gen 0
            population.append(mutated)

        return population

    def evaluate_population(self, population: List[BorisVariant]) -> List[BorisVariant]:
        """Оценивает fitness всей популяции"""
        for variant in population:
            total_fitness = 0
            for test_case in self.test_cases:
                # В реальности тут будет вызов LLM с промптом варианта
                # Сейчас симулируем на основе истории мутаций
                simulated_output = self._simulate_output(variant, test_case)
                result = self.evaluator.evaluate(simulated_output, test_case)
                total_fitness += result.total_fitness

            variant.fitness = total_fitness / len(self.test_cases)

        return population

    def _simulate_output(self, variant: BorisVariant, test_case: TestCase) -> str:
        """
        Симуляция output Boris (в реальности — вызов LLM).

        Качество зависит от комбинации мутаторов:
        - elena_triz → лучше contradictions, IKR
        - xerox → лучше competitive analysis
        - vanechka → лучше JTBD, 4 Forces
        - strategist → лучше structure, evidence
        """
        # Базовый output
        output_parts = [
            f"# Boris Analysis: {test_case.id}",
            "## Verdict: CONDITIONAL GO",
            ""
        ]

        # Добавляем секции в зависимости от мутаторов
        if "elena_triz" in variant.mutator_history:
            output_parts.extend([
                "## System Map с 6+ надсистемами",
                "Надсистемы: Платформы, Регуляторы, AI-сервисы, Конкуренты, Пользователи, Инвесторы [OBS]",
                "",
                "## TC/PC противоречия",
                "TC: Если увеличим автоматизацию, ухудшится контроль качества [DERIVE]",
                "Принципы разрешения: 1) Разделение во времени, 2) Вынос в надсистему",
                ""
            ])

        if "xerox_competitive" in variant.mutator_history:
            output_parts.extend([
                "## Конкурентный анализ",
                "| Конкурент | Price | Features |",
                "| Blotato | $29-499 | 71 |",
                "| Repurpose | $35-180 | 100 |",
                "",
                "Незанятая ниша: Hardware anti-ban [DERIVE]",
                "Русскоязычный рынок недообслужен (только SMMBox) [OBS]",
                ""
            ])

        if "vanechka_jtbd" in variant.mutator_history:
            output_parts.extend([
                "## JTBD Analysis",
                "Job: Сэкономить время на постинге",
                "4 Forces:",
                "- Push: 4-6ч/день на ручной постинг [ASSUME]",
                "- Pull: 1 клик → все платформы",
                "- Anxiety: Забанят аккаунт?",
                "- Habit: Уже использую Buffer",
                ""
            ])

        if "napoleon_ux" in variant.mutator_history:
            output_parts.extend([
                "## Risk Register",
                "| Risk | Prob | Impact | Mitigation |",
                "| API блокировки | 5/5 | 5/5 | Hardware подход |",
                "",
                "## Next Steps",
                "1. **Immediate:** Тест hardware MVP (2 недели, метрика: uptime)",
                "2. **Short-term:** Валидация WTP (1 месяц, 50 интервью)",
                "",
                "## Experiments",
                "- Эксперимент 1: Fake door test на hardware, метрика: signups, срок: 1 неделя [ASSUME→TEST]",
                ""
            ])

        # S-curve и сценарии всегда
        output_parts.extend([
            "## S-curve позиция",
            "Стадия: Growth → Early Maturity [DATA]",
            "",
            "## Base/Bull/Bear сценарии",
            "- Base (50%): Стабильный рост 15%/год",
            "- Bull (30%): AI прорыв, рынок 2x",
            "- Bear (20%): Платформы ужесточают API — главный риск [DERIVE]",
            ""
        ])

        return "\n".join(output_parts)

    def select(self, population: List[BorisVariant]) -> List[BorisVariant]:
        """Турнирный отбор лучших"""
        sorted_pop = sorted(population, key=lambda v: v.fitness, reverse=True)
        elite_count = self.config['population']['elite_count']

        # Элита проходит без изменений
        selected = sorted_pop[:elite_count]

        # Остальные через турнир
        tournament_size = self.config['operators']['selection']['tournament_size']
        while len(selected) < len(population) // 2:
            tournament = random.sample(population, tournament_size)
            winner = max(tournament, key=lambda v: v.fitness)
            if winner not in selected:
                selected.append(winner)

        return selected

    def crossover(self, parent_a: BorisVariant, parent_b: BorisVariant) -> BorisVariant:
        """Скрещивание двух вариантов"""
        # Берём половину промпт-добавок от каждого родителя
        mid_a = len(parent_a.prompt_additions) // 2
        mid_b = len(parent_b.prompt_additions) // 2

        child_additions = parent_a.prompt_additions[:mid_a] + parent_b.prompt_additions[mid_b:]
        child_history = list(set(parent_a.mutator_history + parent_b.mutator_history))

        return BorisVariant(
            id=f"cross_{parent_a.id}_{parent_b.id}_{random.randint(1000, 9999)}",
            prompt_additions=child_additions,
            mutator_history=child_history,
            generation=max(parent_a.generation, parent_b.generation) + 1,
            parent_ids=[parent_a.id, parent_b.id]
        )

    def evolve(self) -> BorisVariant:
        """Основной цикл эволюции"""
        generations = self.config['population']['generations']
        pop_size = self.config['population']['size']
        mutation_rate = self.config['population']['mutation_rate']

        # Инициализация
        self.population = self.initialize_population()
        self.population = self.evaluate_population(self.population)

        for gen in range(generations):
            print(f"\n{'='*50}")
            print(f"Generation {gen + 1}/{generations}")
            print(f"{'='*50}")

            # Отбор
            survivors = self.select(self.population)

            # Обновление лучшего
            best = max(self.population, key=lambda v: v.fitness)
            if not self.best_ever or best.fitness > self.best_ever.fitness:
                self.best_ever = best
                print(f"🏆 New best! Fitness: {best.fitness:.2f}")
                print(f"   Mutators: {best.mutator_history}")

            # Статистика
            avg_fitness = sum(v.fitness for v in self.population) / len(self.population)
            print(f"📊 Best: {best.fitness:.2f} | Avg: {avg_fitness:.2f}")

            self.history.append({
                'generation': gen + 1,
                'best_fitness': best.fitness,
                'avg_fitness': avg_fitness,
                'best_id': best.id,
                'best_mutators': best.mutator_history
            })

            # Создание нового поколения
            new_population = survivors.copy()

            while len(new_population) < pop_size:
                if random.random() < mutation_rate:
                    # Мутация
                    parent = random.choice(survivors)
                    mutator = random.choice(self.mutators)
                    child = mutator.mutate(parent)
                else:
                    # Кроссовер
                    parent_a, parent_b = random.sample(survivors, 2)
                    child = self.crossover(parent_a, parent_b)

                new_population.append(child)

            # Оценка нового поколения
            self.population = self.evaluate_population(new_population)

        return self.best_ever

    def save_results(self, output_dir: str):
        """Сохраняет результаты эволюции"""
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # История
        with open(f"{output_dir}/evolution_history_{timestamp}.json", "w") as f:
            json.dump(self.history, f, indent=2, ensure_ascii=False)

        # Лучший вариант
        if self.best_ever:
            best_data = {
                'id': self.best_ever.id,
                'fitness': self.best_ever.fitness,
                'generation': self.best_ever.generation,
                'mutator_history': self.best_ever.mutator_history,
                'prompt_additions': self.best_ever.prompt_additions
            }
            with open(f"{output_dir}/best_variant_{timestamp}.json", "w") as f:
                json.dump(best_data, f, indent=2, ensure_ascii=False)

        print(f"\n✅ Results saved to {output_dir}")


# ============================================
# MAIN
# ============================================

def main():
    import argparse

    parser = argparse.ArgumentParser(description="Boris Evolution System")
    parser.add_argument("--config", default="config.json", help="Path to config")
    parser.add_argument("--generations", type=int, help="Override generations count")
    parser.add_argument("--population", type=int, help="Override population size")
    args = parser.parse_args()

    # Resolve config path
    script_dir = Path(__file__).parent
    config_path = script_dir / args.config

    print("🧬 Boris Evolution System")
    print("=" * 50)

    # Initialize
    evolution = BorisEvolution(str(config_path))

    # Override config if needed
    if args.generations:
        evolution.config['population']['generations'] = args.generations
    if args.population:
        evolution.config['population']['size'] = args.population

    # Run evolution
    best = evolution.evolve()

    # Results
    print("\n" + "=" * 50)
    print("🏆 EVOLUTION COMPLETE")
    print("=" * 50)
    print(f"Best Variant: {best.id}")
    print(f"Fitness: {best.fitness:.2f}")
    print(f"Mutator DNA: {' → '.join(best.mutator_history)}")
    print(f"\nPrompt Additions:")
    for i, addition in enumerate(best.prompt_additions, 1):
        print(f"  {i}. {addition[:100]}...")

    # Save
    output_dir = script_dir / "runs"
    evolution.save_results(str(output_dir))


if __name__ == "__main__":
    main()
