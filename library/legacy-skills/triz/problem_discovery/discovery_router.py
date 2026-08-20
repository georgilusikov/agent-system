"""
Problem Discovery — Discovery Router v2

Pre-triage layer that classifies user input into 6 scenarios
and routes to chains of existing TRIZ skills for problem-finding.

Scenarios:
    S1 VAGUE_SITUATION   — vague/fuzzy input → @socratic → @problem_map → @problem_formulator
    S2 INVESTIGATION     — failure/defect, cause unknown → @kt_is_is_not → @causal_analysis
    S3 RISK_PROACTIVE    — find risks before they happen → @diversion_analysis → @afd_failure_predictor
    S4 INEFFICIENCY      — slow/expensive/low KPD → @functional_analysis → @flow_analysis
    S5 STRATEGIC          — is it worth developing? → @s_curve → @limits_strategy → @system_operator
    S6 FORMULATED        — already has TP/FP → bypass to main triage
"""

import json
import logging
import os
import re
from dataclasses import dataclass, field
from pathlib import Path

import requests

logger = logging.getLogger(__name__)
TRIZ_SKILLS_DIR = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------------------------
# Scenarios (6 categories)
# ---------------------------------------------------------------------------

S1_VAGUE_SITUATION = "VAGUE_SITUATION"
S2_INVESTIGATION = "INVESTIGATION"
S3_RISK_PROACTIVE = "RISK_PROACTIVE"
S4_INEFFICIENCY = "INEFFICIENCY"
S5_STRATEGIC = "STRATEGIC"
S6_FORMULATED = "FORMULATED"

VALID_SCENARIOS = {
    S1_VAGUE_SITUATION,
    S2_INVESTIGATION,
    S3_RISK_PROACTIVE,
    S4_INEFFICIENCY,
    S5_STRATEGIC,
    S6_FORMULATED,
}

# Skill chains for each scenario (ordered — execute left to right)
SCENARIO_TO_SKILLS: dict[str, list[str]] = {
    S1_VAGUE_SITUATION: ["socratic", "problem_map", "problem_formulator"],
    S2_INVESTIGATION: ["kt_is_is_not", "causal_analysis"],
    S3_RISK_PROACTIVE: ["diversion_analysis", "afd_failure_predictor"],
    S4_INEFFICIENCY: ["functional_analysis", "flow_analysis"],
    S5_STRATEGIC: ["s_curve", "limits_strategy", "system_operator"],
    S6_FORMULATED: [],  # bypass — no pre-processing needed
}

SAFE_FALLBACK_CHAIN = ["socratic", "problem_map", "problem_formulator"]

# Human-readable descriptions
SCENARIO_DESCRIPTIONS: dict[str, str] = {
    S1_VAGUE_SITUATION: "Расплывчатая ситуация → уточнение + карта проблемы + формулировка АРИЗ",
    S2_INVESTIGATION: "Расследование отказа → контрастная матрица + поиск причин",
    S3_RISK_PROACTIVE: "Проактивный поиск рисков → диверсионный анализ + AFD",
    S4_INEFFICIENCY: "Неэффективность процесса → ФА + потоковый анализ",
    S5_STRATEGIC: "Стратегический анализ → S-кривая + пределы + системный оператор",
    S6_FORMULATED: "Задача сформулирована → bypass в main triage",
}


# Alternative skills that can be substituted in each scenario
SCENARIO_ALTERNATIVES: dict[str, list[str]] = {
    S1_VAGUE_SITUATION: ["system_operator", "avf"],
    S2_INVESTIGATION: ["triz_troubleshooter", "inconsistent_parameters"],
    S3_RISK_PROACTIVE: ["stpa_analysis"],
    S4_INEFFICIENCY: [
        "informational_flow_analysis",
        "structural_analysis",
        "trimming",
        "causal_loop_diagram",
    ],
    S5_STRATEGIC: ["resource_analysis"],
    S6_FORMULATED: [],
}

PRIMARY_ROUTE_OVERRIDES: dict[str, dict[str, object]] = {
    S3_RISK_PROACTIVE: {
        "primary_route": "stpa_analysis",
        "methods": ["stpa_analysis", "problem_formulator"],
        "default_methods": ["diversion_analysis", "afd_failure_predictor"],
        "alternatives": ["diversion_analysis", "afd_failure_predictor"],
        "description": "Проактивный поиск рисков в контуре управления → STPA + формулировка проблемы",
        "signal_patterns": [
            r"\bcontrol loop\b",
            r"\bfeedback\b",
            r"\binterlock\b",
            r"\bunsafe control action\b",
            r"\buca\b",
            r"\bcontroller\b",
            r"\bactuator\b",
            r"\bsensor\b",
            r"\boperator\b",
            r"\bplc\b",
            r"\balarm\b",
            r"\bsoftware\b",
            r"контур\w*\s+управ",
            r"обратн\w*\s+связ",
            r"блокиров",
            r"датчик",
            r"контроллер",
            r"оператор",
            r"исполнител",
            r"плк",
            r"сигнал тревог",
        ],
        "default_signal_patterns": [
            r"\bsabotage\b",
            r"\bweaponiz",
            r"\bmisuse\b",
            r"\bcontamin",
            r"\bcorrosion\b",
            r"\bfatigue\b",
            r"\bresonance\b",
            r"\bvibration\b",
            r"\bhidden defect\b",
            r"\bdelayed defect\b",
            r"\bspecial conditions\b",
            r"\bresource\b",
            r"\battack\b",
            r"диверс",
            r"саботаж",
            r"скрыт\w*\s+дефект",
            r"отложенн\w*\s+брак",
            r"ресурс\w*",
            r"корроз",
            r"усталост",
            r"резонанс",
            r"вибрац",
            r"загрязн",
            r"особ\w*\s+услов",
        ],
        "default_route_hints": ["default", "diversion_analysis", "afd_failure_predictor", "unsure"],
        "min_hits": 2,
        "signal_delta": 1,
        "reason_suffix": "Primary path promoted to STPA because control-loop hazard signals were detected.",
    },
    S4_INEFFICIENCY: {
        "primary_route": "causal_loop_diagram",
        "methods": ["causal_loop_diagram", "problem_formulator"],
        "alternatives": [
            "functional_analysis",
            "flow_analysis",
            "informational_flow_analysis",
            "structural_analysis",
            "trimming",
        ],
        "description": "Хроническая неэффективность с feedback loops → CLD + формулировка проблемы",
        "signal_patterns": [
            r"\bfeedback loop\b",
            r"\breinforcing\b",
            r"\bbalancing\b",
            r"\bbacklog\b",
            r"\brework\b",
            r"\bfirefighting\b",
            r"\boscillat",
            r"\bdelay\b",
            r"\blag\b",
            r"\bleverage\b",
            r"\bqueue\b",
            r"\brecurr",
            r"\bkeeps coming back\b",
            r"повторя",
            r"снова",
            r"опять",
            r"петл",
            r"задерж",
            r"очеред",
            r"передел",
            r"rebound",
            r"локальн\w*\s+оптимизац",
            r"не держ",
            r"возвраща",
        ],
        "default_route_hints": ["default", "functional_analysis", "flow_analysis", "unsure"],
        "min_hits": 2,
        "reason_suffix": "Primary path promoted to causal loop analysis because recurring feedback-loop signals were detected.",
    },
}

# ---------------------------------------------------------------------------
# LLM Prompt — 6-scenario classification
# ---------------------------------------------------------------------------

DISCOVERY_PROMPT = """\
Ты — Problem Discovery Router. Твоя задача — классифицировать вход пользователя \
в один из 6 сценариев для выбора метода поиска проблемы.

## 6 сценариев:

| Сценарий | Код | Признаки |
|----------|-----|----------|
| Расплывчатая ситуация | VAGUE_SITUATION | Описана система, но проблема нечёткая, \
несколько переплетённых проблем, нет явного противоречия, «плохо работает» |
| Расследование отказа | INVESTIGATION | Что-то сломалось/испортилось, причина неизвестна, \
отклонение от нормы, «раньше работало — теперь нет», дефект |
| Проактивный поиск рисков | RISK_PROACTIVE | Как может сломаться? Какие уязвимости? \
Pre-mortem, надёжность, профилактика отказов |
| Неэффективность процесса | INEFFICIENCY | Медленно, дорого, низкий КПД, узкое место, \
bottleneck, потери, Muda |
| Стратегический анализ | STRATEGIC | Стоит ли развивать систему? Устарела? На каком \
этапе S-кривой? Предел развития? Инвестировать или заменить? |
| Задача сформулирована | FORMULATED | Есть чёткое ТП-1/ТП-2 или ФП, известна \
конфликтующая пара, причина/следствие описаны |

## Правила классификации:
1. Если есть ТП-1/ТП-2 или явное противоречие → FORMULATED
2. Если «сломалось/дефект» + причина неизвестна → INVESTIGATION
3. Если «как может сломаться» / «риски» / «надёжность» → RISK_PROACTIVE
4. Если «медленно/дорого/КПД/bottleneck» → INEFFICIENCY
5. Если «стоит ли развивать/устарело/S-кривая» → STRATEGIC
6. Во всех остальных случаях → VAGUE_SITUATION (безопасный default)

## Дополнительный route hint внутри сценария:
- Для `RISK_PROACTIVE`:
  - `stpa_analysis` если риск связан с controller / operator / feedback / interlock /
    unsafe control action / timing / software safety
  - `diversion_analysis` если это общий pre-mortem / sabotage / weaponization /
    поиск уязвимостей через ресурсы
  - `default` только если остаётся сомнение между ними
- Для `INEFFICIENCY`:
  - `causal_loop_diagram` если проблема recurring, есть delays / rework / backlog /
    rebound / reinforcing or balancing loops / local fixes do not hold
  - `default` если это обычный bottleneck / waste / flow / functional diagnosis
- Для остальных сценариев всегда возвращай `default`

## Задача пользователя:
{task}

## Ответь СТРОГО в JSON:
```json
{{
  "scenario": "VAGUE_SITUATION",
  "confidence": 0.85,
  "reasoning": "Краткое обоснование на 1-2 предложения",
  "primary_route_hint": "default"
}}
```

Верни ТОЛЬКО JSON, без другого текста.
"""


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

@dataclass
class DiscoveryResult:
    """Result of problem discovery classification."""

    category: str
    confidence: float
    reasoning: str
    methods: list[str]
    description: str = ""
    alternatives: list[str] = field(default_factory=list)
    primary_route: str | None = None
    primary_signal_hits: int = 0
    llm_route_hint: str | None = None
    route_selection_source: str = "scenario_default"

    @classmethod
    def from_json(cls, data: dict) -> "DiscoveryResult":
        """Create DiscoveryResult from parsed JSON."""
        scenario = data.get("scenario", S1_VAGUE_SITUATION)
        if scenario not in VALID_SCENARIOS:
            logger.warning("Unknown scenario '%s', defaulting to VAGUE_SITUATION", scenario)
            scenario = S1_VAGUE_SITUATION

        try:
            confidence = float(data.get("confidence", 0.5))
        except (TypeError, ValueError):
            confidence = 0.5

        methods = list(SCENARIO_TO_SKILLS.get(scenario, SAFE_FALLBACK_CHAIN))
        alternatives = _filter_executable_skills(SCENARIO_ALTERNATIVES.get(scenario, []))

        if scenario != S6_FORMULATED and (
            confidence < 0.6 or not _is_valid_skill_chain(methods)
        ):
            logger.warning(
                "Discovery router fell back to safe S1 chain (scenario=%s, confidence=%.2f, methods=%s)",
                scenario,
                confidence,
                methods,
            )
            scenario = S1_VAGUE_SITUATION
            confidence = max(confidence, 0.5)
            methods = SAFE_FALLBACK_CHAIN.copy()
            alternatives = _filter_executable_skills(SCENARIO_ALTERNATIVES.get(scenario, []))

        return cls(
            category=scenario,
            confidence=confidence,
            reasoning=data.get("reasoning", ""),
            methods=methods,
            description=SCENARIO_DESCRIPTIONS.get(scenario, ""),
            alternatives=alternatives,
        )


def _skill_is_executable(skill_id: str) -> bool:
    """Return True when a skill exists as a normal top-level executable skill."""
    skill_dir = TRIZ_SKILLS_DIR / skill_id
    return (
        skill_dir.is_dir()
        and (skill_dir / "SKILL.md").exists()
        and (skill_dir / "core_instructions.md").exists()
        and (skill_dir / "validators" / "gate_check.md").exists()
    )


def _filter_executable_skills(skill_ids: list[str]) -> list[str]:
    """Drop phantom or non-executable skills from discovery metadata."""
    return [skill_id for skill_id in skill_ids if _skill_is_executable(skill_id)]


def _is_valid_skill_chain(methods: list[str]) -> bool:
    """Validate that a discovery chain is non-empty and fully executable."""
    return bool(methods) and all(_skill_is_executable(skill_id) for skill_id in methods)


def _count_signal_hits(text: str, patterns: list[str]) -> int:
    """Count distinct route-signal regex hits in task text."""
    return sum(1 for pattern in patterns if re.search(pattern, text, re.IGNORECASE))


def _normalize_route_hint(raw_hint: object) -> str | None:
    """Normalize optional route hint returned by the discovery LLM."""
    if raw_hint is None:
        return None
    hint = str(raw_hint).strip().lower()
    if not hint:
        return None
    return hint


def _promote_primary_route(
    result: DiscoveryResult,
    override: dict[str, object],
    signal_hits: int,
    source: str,
) -> DiscoveryResult:
    """Apply a validated primary-route override."""
    methods = list(override["methods"])
    result.methods = methods
    result.alternatives = _filter_executable_skills(list(override["alternatives"]))
    result.description = str(override["description"])
    result.primary_route = str(override["primary_route"])
    result.primary_signal_hits = signal_hits
    result.route_selection_source = source
    reason_suffix = str(override["reason_suffix"])
    result.reasoning = f"{result.reasoning} {reason_suffix}".strip()
    return result


def _apply_primary_route_overrides(
    task: str,
    data: dict,
    result: DiscoveryResult,
) -> DiscoveryResult:
    """Promote specialized primary routes inside a scenario using hints plus signals."""
    override = PRIMARY_ROUTE_OVERRIDES.get(result.category)
    if not override or result.category == S6_FORMULATED:
        return result

    signal_text = "\n".join(part for part in [task, result.reasoning] if part).strip()
    signal_hits = _count_signal_hits(signal_text, list(override["signal_patterns"]))
    min_hits = int(override["min_hits"])
    strong_min_hits = max(min_hits + 1, 3)
    default_signal_hits = _count_signal_hits(
        signal_text,
        list(override.get("default_signal_patterns", [])),
    )
    signal_delta = int(override.get("signal_delta", 1))
    llm_route_hint = _normalize_route_hint(data.get("primary_route_hint"))
    result.llm_route_hint = llm_route_hint

    methods = list(override["methods"])
    if not _is_valid_skill_chain(methods):
        logger.warning(
            "Primary route override for %s ignored because chain is not executable: %s",
            result.category,
            methods,
        )
        return result

    primary_route = str(override["primary_route"])
    default_route_hints = {
        str(value).strip().lower() for value in override.get("default_route_hints", ["default"])
    }

    if default_signal_hits >= min_hits and default_signal_hits >= signal_hits + signal_delta:
        result.route_selection_source = "default_signal_route"
        return result

    if signal_hits >= min_hits and signal_hits >= default_signal_hits + signal_delta:
        return _promote_primary_route(result, override, signal_hits, "signal_override")

    if llm_route_hint == primary_route:
        return _promote_primary_route(result, override, signal_hits, "llm_hint")

    if llm_route_hint in default_route_hints:
        if signal_hits >= strong_min_hits:
            return _promote_primary_route(result, override, signal_hits, "signal_override")
        result.route_selection_source = "llm_default"
        return result

    return result


# ---------------------------------------------------------------------------
# LLM call (reuses same pattern as triage_agent.py)
# ---------------------------------------------------------------------------

def _call_llm(
    prompt: str,
    api_base: str | None = None,
    api_key: str | None = None,
    model: str | None = None,
) -> str:
    """Call LLM API and return text response."""
    base = api_base or os.getenv("TRIZ_API_BASE", "https://api.x.ai/v1")
    key = api_key or os.getenv("TRIZ_API_KEY", os.getenv("XAI_API_KEY", ""))
    mdl = model or os.getenv("TRIZ_MODEL", "grok-3-mini")

    resp = requests.post(
        f"{base}/chat/completions",
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        json={
            "model": mdl,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.1,
            "max_tokens": 300,
        },
        timeout=60,
    )
    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]["content"]


def _extract_json(text: str) -> dict:
    """Extract JSON from LLM response (handles markdown fences)."""
    match = re.search(r"```(?:json)?\s*\n?(.*?)\n?```", text, re.DOTALL)
    if match:
        return json.loads(match.group(1).strip())

    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        return json.loads(match.group(0))

    raise ValueError(f"No JSON found in response: {text[:200]}")


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def classify(task: str, **llm_kwargs: str | None) -> DiscoveryResult:
    """
    Classify a task into one of 6 scenarios and determine skill chain.

    Args:
        task: User's raw problem description.
        **llm_kwargs: Optional api_base, api_key, model overrides.

    Returns:
        DiscoveryResult with scenario, confidence, skill chain, and alternatives.
    """
    prompt = DISCOVERY_PROMPT.format(task=task)
    response = _call_llm(prompt, **llm_kwargs)
    data = _extract_json(response)
    result = DiscoveryResult.from_json(data)
    result = _apply_primary_route_overrides(task, data, result)
    logger.info(
        "Discovery: %s (confidence=%.2f, skills=%s, alt=%s, primary=%s, hits=%s, hint=%s, source=%s)",
        result.category,
        result.confidence,
        result.methods,
        result.alternatives,
        result.primary_route,
        result.primary_signal_hits,
        result.llm_route_hint,
        result.route_selection_source,
    )
    return result


def is_formulated(task: str, **llm_kwargs: str | None) -> bool:
    """Quick check: is the task already formulated?"""
    result = classify(task, **llm_kwargs)
    return result.category == S6_FORMULATED
"""
Discovery router — Python-native pre-triage for Problem Discovery sub-orchestrator.
"""
