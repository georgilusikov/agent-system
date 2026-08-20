"""
TRIZ Orchestrator v5 — Triage Agent

Micro-agent that classifies a task into one of 14 skeleton maps.
Makes a single, focused LLM call with a minimal prompt (~50 lines).
Returns structured JSON: {map, confidence, reasoning}.

Includes Formulation Gate (v5.1): if input is vague,
runs Problem Discovery sub-orchestrator first.
"""

import json
import os
import re
from dataclasses import dataclass
from pathlib import Path

import requests

from ..problem_discovery.discovery_router import (
    DiscoveryResult,
    S6_FORMULATED,
    classify as discovery_classify,
)

# Maps directory
SKELETON_MAPS_DIR = Path(__file__).parent / "skeleton_maps"
DEFAULT_LLM_MAX_TOKENS = 4000

TRIAGE_PROMPT = """Ты — TRIZ Triage Agent. Твоя ЕДИНСТВЕННАЯ задача — классифицировать задачу пользователя.

## 14 карт маршрутизации:

| Код | Название | Триггеры |
|-----|----------|----------|
| А | Investigation | Авария, брак, причина неизвестна, "почему?" |
| Б | Optimization | Дорого, лишнее, снизить себестоимость, КПД |
| В | Strategy | Прорыв, невозможное, эволюционный барьер |
| Г | Diagnostic | Аудит, риски, уязвимости, проверка системы |
| Д | Predictive | Прогноз, S-кривая, следующее поколение |
| Е | ARIZ Deep | Тупик, ВСЕ попытки провалились, глубокий анализ |
| Ж | Express | СРОЧНО, за 1 час, emergency, быстро |
| З | Chemistry | Химия, вещество, материал, реакция |
| И | Patent | Патент, IP, обойти патент, изобретение |
| К | Education | Обучение, тренинг, упражнения, РТВ |
| Л | Feature Transfer | Аналог из другой отрасли, бенчмаркинг, перенос |
| М | Process | Процесс, поток, bottleneck, конвейер, логистика |
| Н | FMEA | Надёжность, FMEA, сценарии отказов |
| DC | Dynamic Constructor | Не подходит ни одна карта, мультидоменная задача |

## Задача пользователя:
{task}

## Ответь СТРОГО в JSON:
```json
{{
  "map": "А",
  "map_name": "Investigation",
  "confidence": 0.85,
  "reasoning": "Краткое обоснование на 1-2 предложения"
}}
```

Верни ТОЛЬКО JSON, без другого текста.
"""

FORMULATION_PROMPT = """Ты — TRIZ Problem Formulation Compiler.

Твоя задача — превратить исходную задачу и результаты discovery-методов
в одну компактную постановку проблемы для повторного triage.

## Исходная задача:
{task}

## Сценарий discovery:
{category}

## Обоснование discovery:
{reasoning}

## Результаты discovery:
{discovery_outputs}

## Требования:
1. Зафиксируй одну главную проблему, а не список тем.
2. Если причина уже локализована — явно назови её.
3. Если есть противоречие/барьер — сформулируй его одной фразой.
4. Если данных не хватает — пометь [ASSUME] и укажи, что проверить.
5. Верни 4 коротких блока:
   - MPV / целевая метрика
   - Главный негативный эффект
   - Главный барьер / причина / противоречие
   - Вопрос для следующего этапа

Верни только сформулированную постановку, без Markdown fences и без пояснений о процессе.
"""


@dataclass
class TriageResult:
    """Result of task classification."""

    map_code: str
    map_name: str
    confidence: float
    reasoning: str

    @classmethod
    def from_json(cls, data: dict) -> "TriageResult":
        return cls(
            map_code=data["map"],
            map_name=data.get("map_name", "Unknown"),
            confidence=data.get("confidence", 0.5),
            reasoning=data.get("reasoning", ""),
        )


def _env_int(name: str, default: int) -> int:
    try:
        return int(os.getenv(name, str(default)))
    except ValueError:
        return default


def call_llm(
    prompt: str,
    api_base: str | None = None,
    api_key: str | None = None,
    model: str | None = None,
    max_tokens: int | None = None,
) -> str:
    """Call LLM API and return text response."""
    base = api_base or os.getenv("TRIZ_API_BASE", "https://api.x.ai/v1")
    key = api_key or os.getenv("TRIZ_API_KEY", os.getenv("XAI_API_KEY", ""))
    mdl = model or os.getenv("TRIZ_MODEL", "grok-3-mini")
    token_limit = max_tokens if max_tokens is not None else _env_int(
        "TRIZ_MAX_TOKENS",
        DEFAULT_LLM_MAX_TOKENS,
    )

    resp = requests.post(
        f"{base}/chat/completions",
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        json={
            "model": mdl,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.1,
            "max_tokens": token_limit,
        },
        timeout=60,
    )
    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]["content"]


def extract_json(text: str) -> dict:
    """Extract JSON from LLM response (handles markdown fences)."""
    # Try to find JSON in code blocks
    match = re.search(r"```(?:json)?\s*\n?(.*?)\n?```", text, re.DOTALL)
    if match:
        return json.loads(match.group(1).strip())

    # Try raw JSON
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        return json.loads(match.group(0))

    raise ValueError(f"No JSON found in response: {text[:200]}")


def get_skeleton_map(map_code: str) -> str | None:
    """Load skeleton map file content for a given map code."""
    code_to_file = {
        "А": "a_investigation.md", "Б": "b_optimization.md",
        "В": "c_strategy.md", "Г": "d_diagnostic.md",
        "Д": "e_predictive.md", "Е": "f_ariz_deep.md",
        "Ж": "g_express.md", "З": "h_chemistry.md",
        "И": "i_patent.md", "К": "k_education.md",
        "Л": "l_feature_transfer.md", "М": "m_process.md",
        "Н": "n_fmea.md", "DC": "x_dynamic_constructor.md",
    }
    filename = code_to_file.get(map_code)
    if not filename:
        return None

    filepath = SKELETON_MAPS_DIR / filename
    if filepath.exists():
        return filepath.read_text(encoding="utf-8")

    return None


def triage(task: str, **llm_kwargs) -> TriageResult:
    """
    Classify a task into one of 14 skeleton maps.

    Args:
        task: User's problem description
        **llm_kwargs: Optional api_base, api_key, model

    Returns:
        TriageResult with map, confidence, reasoning
    """
    prompt = TRIAGE_PROMPT.format(task=task)
    response = call_llm(prompt, **llm_kwargs)
    data = extract_json(response)
    return TriageResult.from_json(data)


def triage_with_discovery(
    task: str,
    formulated_task: str | None = None,
    **llm_kwargs,
) -> tuple[TriageResult | None, DiscoveryResult | None]:
    """
    Formulation Gate + Triage.

    First checks if the task is formulated or vague via discovery_router.
    If formulated → runs standard triage.
    If vague → returns discovery result with recommended methods.

    Args:
        task: User's raw problem description.
        formulated_task: Reformulated problem statement produced by discovery.
            When provided, discovery is bypassed and triage runs on the formulated task.
        **llm_kwargs: Optional api_base, api_key, model overrides.

    Returns:
        Tuple of (TriageResult or None, DiscoveryResult or None).
        If discovery was needed, TriageResult is None until the caller reformulates
        the task and re-runs triage on the formulated version.
        If task was formulated, DiscoveryResult is None.
    """
    if formulated_task is not None:
        return triage(formulated_task, **llm_kwargs), None

    try:
        discovery = discovery_classify(task, **llm_kwargs)
    except Exception:
        # If discovery fails, fall through to standard triage
        import logging
        logging.getLogger(__name__).warning(
            "Discovery router failed, falling through to standard triage"
        )
        return triage(task, **llm_kwargs), None

    if discovery.category == S6_FORMULATED:
        # Task is already formulated, run standard triage
        return triage(task, **llm_kwargs), None

    # Task is vague — defer map selection until discovery methods
    # reformulate the problem statement for a second triage pass.
    return None, discovery


def reformulate_task(
    task: str,
    discovery: DiscoveryResult,
    discovery_outputs: list[str],
    **llm_kwargs,
) -> str:
    """
    Compile discovery outputs into a compact, triage-ready problem statement.

    Falls back to the latest discovery output when the extra formulation call fails.
    """
    cleaned_outputs = [output.strip() for output in discovery_outputs if output and output.strip()]
    if not cleaned_outputs:
        return task

    prompt = FORMULATION_PROMPT.format(
        task=task,
        category=discovery.category,
        reasoning=discovery.reasoning or "Не указано",
        discovery_outputs="\n\n---\n\n".join(cleaned_outputs[-3:]),
    )

    try:
        response = call_llm(prompt, **llm_kwargs).strip()
    except Exception:
        response = ""

    if response:
        return response

    fallback = cleaned_outputs[-1]
    if fallback.startswith(task):
        return fallback
    return f"{task}\n\nDiscovery findings:\n{fallback}"
