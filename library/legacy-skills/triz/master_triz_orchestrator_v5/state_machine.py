"""
TRIZ Orchestrator v5 — State Machine

Main pipeline controller. Executes skills step by step,
enforcing micro-chains via Python code and checking gateways
via JSON checklists.

Flow: task → discovery/triage → skeleton_map → step-by-step execution
"""

import json
import logging
import re
from dataclasses import dataclass, field
from enum import Enum
from functools import lru_cache
from pathlib import Path

from .triage_agent import (
    TriageResult,
    call_llm,
    extract_json,
    get_skeleton_map,
    reformulate_task,
    triage_with_discovery,
)
from .validators import MicroChainViolation, SessionState, validate_skill_call

logger = logging.getLogger(__name__)

MAX_BACKTRACKS_PER_PHASE = 2
MAX_BACKTRACKS_TOTAL = 3
TRIZ_SKILLS_DIR = Path(__file__).resolve().parent.parent
SKILL_CATALOG_PATH = Path(__file__).resolve().parent / "skill_catalog.yaml"
TOKEN_WORD_CHARS = "0-9A-Za-zА-Яа-яЁё_"


class Phase(Enum):
    ANALYSIS = "analysis"
    MODELING = "modeling"
    SYNTHESIS = "synthesis"
    DONE = "done"


ANALYSIS_SKILLS = {
    "@akts",
    "@causal_analysis",
    "@flow_analysis",
    "@functional_analysis",
    "@value_analysis",
    "@structural_analysis",
    "@diversion_analysis",
    "@avf",
    "@afd_failure_predictor",
    "@inconsistent_parameters",
    "@principle_comparison",
    "@problem_formulator",
    "@problem_map",
    "@socratic",
    "@stpa_analysis",
    "@system_operator",
    "@s_curve",
    "@zrts",
    "@kt_is_is_not",
    "@causal_loop_diagram",
    "@limits_strategy",
    "@benchmarking",
    "@patent_claims",
    "@triz_troubleshooter",
}

MODELING_SKILLS = {
    "@oz_ov",
    "@resource_analysis",
    "@ikr",
    "@contradictions",
    "@vepoli",
    "@arip",
    "@mmch",
    "@trimming",
    "@morphological_analysis",
    "@chemical_triz",
}

SYNTHESIS_SKILLS = {
    "@forty_principles",
    "@standards",
    "@effects",
    "@fos",
    "@reverse_fos",
    "@oas_transfer",
    "@dynamization",
    "@ariz",
    "@inversion",
    "@antisystem",
    "@pn_eco_innovation",
    "@critic",
    "@final_triz_report",
    "@rtv",
    "@case_logger",
    "@robinson",
    "@goldfish",
    "@dnd",
}

CATALOG_PHASE_ALIASES: dict[str, Phase] = {
    "formulation": Phase.ANALYSIS,
    "analysis": Phase.ANALYSIS,
    "modeling": Phase.MODELING,
    "synthesis": Phase.SYNTHESIS,
    "utility": Phase.SYNTHESIS,
    "meta": Phase.SYNTHESIS,
}


@dataclass
class StepResult:
    """Result of a single skill execution."""

    skill: str
    output: str
    artifacts: dict = field(default_factory=dict)
    confidence: float = 0.7
    gate_passed: bool = True
    warnings: list[str] = field(default_factory=list)


@dataclass
class PipelineResult:
    """Result of a complete pipeline run."""

    task: str
    triage: TriageResult
    steps: list[StepResult] = field(default_factory=list)
    map_content: str = ""
    final_output: str = ""
    backtracks: int = 0
    state: SessionState = field(default_factory=SessionState)
    formulated_task: str | None = None
    gateway_events: list[str] = field(default_factory=list)


@dataclass
class SkeletonSkill:
    """A concrete skill step from a skeleton map."""

    skill: str


@dataclass
class SkeletonBranch:
    """A selectable branch under a skeleton-map gateway."""

    label: str
    items: list["SkeletonItem"] = field(default_factory=list)
    stop_after: bool = False


@dataclass
class SkeletonGateway:
    """A decision point embedded in a skeleton map."""

    question: str
    branches: list[SkeletonBranch] = field(default_factory=list)


SkeletonItem = SkeletonSkill | SkeletonGateway


SKILL_STEP_PROMPT = """Ты — TRIZ-эксперт, выполняющий следующий шаг оркестратора.

## Контекст задачи:
{task}

## Текущий скилл:
{skill}

## Состояние сессии:
{session_state}

## Что уже сделано:
{previous_context}

## Канонические инструкции скилла:
{skill_instructions}

## Дополнительные указания оркестратора:
{additional_guidance}

## Требования к ответу:
1. Работай по канонике скилла, а не по общим советам.
2. Дай конкретный результат, который поможет следующему шагу.
3. Если данных мало — пометь [ASSUME] и укажи, что проверить.
4. Верни артефакты, которыми сможет пользоваться gateway или следующий скилл.

## Ответь в формате JSON:
```json
{{
  "skill": "{skill}",
  "result": "Подробный результат анализа...",
  "artifacts": {{
    "key_finding": "Главное открытие",
    "next_action": "Рекомендация для следующего шага"
  }},
  "confidence": 0.8
}}
```
"""

GATEWAY_PROMPT = """Ты — Gateway-валидатор. Проверь, можно ли перейти к следующей фазе.

## Задача:
{task}

## Текущая фаза: {phase}

## Результаты текущей фазы:
{phase_results}

## Чек-лист для {phase}:
{checklist}

## Ответь в JSON:
```json
{{
  "gate_passed": true,
  "checklist_results": {{
    "item1": true,
    "item2": false
  }},
  "missing": ["что не хватает, если gate_passed = false"],
  "recommendation": "backtrack / continue / done"
}}
```
"""

SKELETON_GATEWAY_PROMPT = """Ты — Skeleton Gateway маршрутизатор TRIZ-карты.

Выбери ровно одну ветку карты, которую нужно выполнить дальше.

## Задача:
{task}

## Что уже сделано:
{previous_context}

## Вопрос gateway:
{question}

## Ветки:
{branches}

## Ответь в JSON:
```json
{{
  "branch_index": 1,
  "branch_label": "краткая метка выбранной ветки",
  "confidence": 0.8,
  "reasoning": "почему эта ветка подходит"
}}
```
"""

GATEWAY_CHECKLISTS = {
    Phase.ANALYSIS: [
        "Корневая причина ИЛИ главное противоречие идентифицировано",
        "ОЗ-ОВ (оперативная зона и время) определены",
        "Ресурсы инвентаризированы",
    ],
    Phase.MODELING: [
        "ТП ИЛИ ФП ИЛИ Веполь построен",
        "ИКР сформулирован",
        "Модель проходит Gate Check",
    ],
    Phase.SYNTHESIS: [
        "Есть ≥1 конкретная концепция",
        "Концепция проверена критиком",
        "Нет kill-факторов",
    ],
}


def _compact_text(text: str, limit: int = 3500) -> str:
    text = text.strip()
    if len(text) <= limit:
        return text
    return f"{text[:limit].rstrip()}\n...[truncated]"


def _session_state_summary(state: SessionState) -> str:
    called = ", ".join(state.called_skills) if state.called_skills else "ничего"
    artifacts = ", ".join(sorted(state.artifacts)) if state.artifacts else "нет"
    return f"- called_skills: {called}\n- artifact_keys: {artifacts}"


def load_skill_instructions(skill: str) -> str:
    """Load a compact slice of the real skill instructions."""
    skill_id = skill.lstrip("@")
    core_path = TRIZ_SKILLS_DIR / skill_id / "core_instructions.md"
    if not core_path.exists():
        return f"Используй каноническую методику {skill} и верни проверяемый результат."
    return _compact_text(core_path.read_text(encoding="utf-8"))


@lru_cache(maxsize=1)
def _load_catalog_phase_map() -> dict[str, Phase]:
    """Load phase hints from skill_catalog.yaml without requiring PyYAML."""
    if not SKILL_CATALOG_PATH.exists():
        return {}

    phases: dict[str, Phase] = {}
    current_skill: str | None = None

    for line in SKILL_CATALOG_PATH.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue

        if line == line.lstrip() and stripped.endswith(":"):
            current_skill = stripped[:-1].strip()
            continue

        if current_skill is None or not line.startswith("  phase:"):
            continue

        raw_phase = line.split(":", 1)[1].split("#", 1)[0].strip()
        raw_phase = raw_phase.removeprefix("[").removesuffix("]")
        for token in raw_phase.split(","):
            phase = CATALOG_PHASE_ALIASES.get(token.strip().strip("'\""))
            if phase is not None:
                phases[f"@{current_skill}"] = phase
                break

    return phases


def infer_phase(skill: str) -> Phase:
    """Infer orchestration phase for a skill."""
    if skill in ANALYSIS_SKILLS:
        return Phase.ANALYSIS
    if skill in MODELING_SKILLS:
        return Phase.MODELING
    if skill in SYNTHESIS_SKILLS:
        return Phase.SYNTHESIS
    catalog_phase = _load_catalog_phase_map().get(skill)
    if catalog_phase is not None:
        return catalog_phase
    return Phase.ANALYSIS


def parse_skeleton_map_skills(map_content: str) -> list[str]:
    """Extract skill names from a skeleton map."""
    skills = re.findall(r"@(\w+)", map_content)
    seen: set[str] = set()
    unique: list[str] = []
    for skill in skills:
        tagged = f"@{skill}"
        if tagged not in seen:
            seen.add(tagged)
            unique.append(tagged)
    return unique


def parse_skeleton_map_plan(map_content: str) -> list[SkeletonItem]:
    """Parse a markdown skeleton map into trunk skills and explicit gateways."""
    code_lines = _extract_skeleton_code_lines(map_content)
    items, _ = _parse_skeleton_items(code_lines, 0, 0)
    return items


def _has_skeleton_gateway_markup(map_content: str) -> bool:
    return "⛔ GATEWAY:" in map_content


def _extract_skeleton_code_lines(map_content: str) -> list[str]:
    lines: list[str] = []
    in_code_block = False
    for line in map_content.splitlines():
        if line.strip().startswith("```"):
            in_code_block = not in_code_block
            continue
        if in_code_block and line.strip():
            lines.append(line.rstrip())
    return lines


def _skeleton_line_content(line: str) -> str:
    content = line.strip()
    while content.startswith("│"):
        content = content[1:].lstrip()
    return content


def _skeleton_line_level(line: str) -> int:
    content = _skeleton_line_content(line)
    marker_positions = [
        position
        for position in (
            line.find("├─"),
            line.find("└─"),
            line.find("⛔ GATEWAY:"),
            line.find(content),
        )
        if position >= 0
    ]
    marker_position = min(marker_positions) if marker_positions else 0
    prefix = line[:marker_position]
    indent = len(line) - len(line.lstrip(" "))
    pipe_depth = prefix.count("│")
    indent_depth = 0 if indent <= 2 else 1 + ((indent - 4) // 4)
    return max(pipe_depth, indent_depth)


def _is_skeleton_branch_line(line: str) -> bool:
    return _skeleton_line_content(line).startswith(("├─", "└─"))


def _is_skeleton_gateway_line(line: str) -> bool:
    return _skeleton_line_content(line).startswith("⛔ GATEWAY:")


def _parse_skeleton_items(
    lines: list[str],
    index: int,
    level: int,
) -> tuple[list[SkeletonItem], int]:
    items: list[SkeletonItem] = []

    while index < len(lines):
        line = lines[index]
        line_level = _skeleton_line_level(line)
        if line_level < level:
            break
        if line_level > level:
            nested_items, index = _parse_skeleton_items(lines, index, line_level)
            items.extend(nested_items)
            continue
        if _is_skeleton_branch_line(line):
            break
        if _is_skeleton_gateway_line(line):
            gateway, index = _parse_skeleton_gateway(lines, index, level)
            items.append(gateway)
            continue

        items.extend(SkeletonSkill(skill) for skill in _extract_skeleton_skills(line))
        index += 1

    return items, index


def _parse_skeleton_gateway(
    lines: list[str],
    index: int,
    level: int,
) -> tuple[SkeletonGateway, int]:
    content = _skeleton_line_content(lines[index])
    question = content.split("GATEWAY:", 1)[1].strip()
    gateway = SkeletonGateway(question=question)
    index += 1

    while index < len(lines):
        if _skeleton_line_level(lines[index]) != level:
            break
        if not _is_skeleton_branch_line(lines[index]):
            break
        branch, index = _parse_skeleton_branch(lines, index, level)
        gateway.branches.append(branch)

    return gateway, index


def _parse_skeleton_branch(
    lines: list[str],
    index: int,
    level: int,
) -> tuple[SkeletonBranch, int]:
    content = _skeleton_line_content(lines[index])
    body = content.split("─", 1)[1].strip()
    if "→" in body:
        label, remainder = [part.strip() for part in body.split("→", 1)]
    else:
        label, remainder = body, body

    branch = SkeletonBranch(
        label=label,
        items=[SkeletonSkill(skill) for skill in _extract_skeleton_skills(remainder)],
        stop_after="СТОП" in body.upper(),
    )
    index += 1

    if index < len(lines) and _skeleton_line_level(lines[index]) > level:
        nested_items, index = _parse_skeleton_items(lines, index, level + 1)
        branch.items.extend(nested_items)

    return branch, index


def _extract_skeleton_skills(text: str) -> list[str]:
    return [f"@{skill}" for skill in re.findall(r"@(\w+)", text)]


def execute_skill(
    skill: str,
    task: str,
    state: SessionState,
    previous_context: str,
    additional_guidance: str = "",
    **llm_kwargs,
) -> StepResult:
    """Execute a single skill via LLM call with validation."""
    warnings = validate_skill_call(skill, state)
    prompt = SKILL_STEP_PROMPT.format(
        task=task,
        skill=skill,
        session_state=_session_state_summary(state),
        previous_context=previous_context or "Это первый шаг.",
        skill_instructions=load_skill_instructions(skill),
        additional_guidance=additional_guidance or "Нет.",
    )

    response = call_llm(prompt, **llm_kwargs)

    try:
        data = extract_json(response)
    except (ValueError, json.JSONDecodeError):
        data = {"result": response, "confidence": 0.5, "artifacts": {}}

    raw_artifacts = data.get("artifacts", {})
    artifacts = raw_artifacts if isinstance(raw_artifacts, dict) else {}

    result = StepResult(
        skill=skill,
        output=data.get("result", response),
        artifacts=artifacts,
        confidence=data.get("confidence", 0.5),
        warnings=warnings,
    )

    state.record_result(skill, result.artifacts, result.output)

    return result


def check_gateway(
    task: str,
    phase: Phase,
    phase_results: list[StepResult],
    **llm_kwargs,
) -> dict:
    """Check if the current phase gate is passed."""
    checklist = GATEWAY_CHECKLISTS.get(phase, [])
    results_text = "\n".join(
        f"- {result.skill}: {result.output[:200]}..."
        for result in phase_results
    )
    checklist_text = "\n".join(f"- [ ] {item}" for item in checklist)

    prompt = GATEWAY_PROMPT.format(
        task=task,
        phase=phase.value,
        phase_results=results_text,
        checklist=checklist_text,
    )

    response = call_llm(prompt, **llm_kwargs)

    try:
        return extract_json(response)
    except (ValueError, json.JSONDecodeError):
        return {"gate_passed": True, "recommendation": "continue"}


def _skipped_step(skill: str, error: Exception) -> StepResult:
    return StepResult(
        skill=skill,
        output=f"SKIPPED: {error}",
        warnings=[str(error)],
        gate_passed=False,
    )


def _append_context(previous_context: str, skill: str, step: StepResult) -> str:
    fragment = f"\n{skill}: {step.output[:300]}"
    return f"{previous_context}{fragment}" if previous_context else fragment.lstrip()


def choose_skeleton_branch(
    task: str,
    gateway: SkeletonGateway,
    previous_context: str,
    **llm_kwargs,
) -> SkeletonBranch:
    """Choose one branch for a skeleton-map gateway."""
    if not gateway.branches:
        raise ValueError(f"Skeleton gateway has no branches: {gateway.question}")

    branch_text = "\n".join(
        f"{index}. {branch.label}: {_skeleton_item_summary(branch.items)}"
        f"{' [STOP]' if branch.stop_after else ''}"
        for index, branch in enumerate(gateway.branches, 1)
    )
    prompt = SKELETON_GATEWAY_PROMPT.format(
        task=task,
        previous_context=previous_context or "Это первый skeleton-gateway.",
        question=gateway.question,
        branches=branch_text,
    )

    try:
        data = extract_json(call_llm(prompt, **llm_kwargs))
    except (ValueError, json.JSONDecodeError):
        return _fallback_skeleton_branch(gateway)

    branch = _branch_from_gateway_response(gateway, data)
    return branch or _fallback_skeleton_branch(gateway)


def _skeleton_item_summary(items: list[SkeletonItem]) -> str:
    skills = [item.skill for item in items if isinstance(item, SkeletonSkill)]
    return " → ".join(skills) if skills else "СТОП"


def _branch_from_gateway_response(
    gateway: SkeletonGateway,
    data: dict,
) -> SkeletonBranch | None:
    raw_index = data.get("branch_index")
    if isinstance(raw_index, int) and 1 <= raw_index <= len(gateway.branches):
        return gateway.branches[raw_index - 1]
    if isinstance(raw_index, str) and raw_index.strip().isdigit():
        branch_index = int(raw_index.strip())
        if 1 <= branch_index <= len(gateway.branches):
            return gateway.branches[branch_index - 1]

    raw_label = str(data.get("branch_label") or "").strip().casefold()
    if not raw_label:
        return None
    matches: list[SkeletonBranch] = []
    for branch in gateway.branches:
        label = branch.label.strip().casefold()
        if _branch_label_matches(raw_label, label):
            matches.append(branch)
    return matches[0] if len(matches) == 1 else None


def _branch_label_matches(raw_label: str, label: str) -> bool:
    if raw_label == label:
        return True
    return _label_prefix_matches(raw_label, label) or _label_prefix_matches(label, raw_label)


def _label_prefix_matches(prefix: str, value: str) -> bool:
    if not prefix or not value.startswith(prefix):
        return False
    if len(value) == len(prefix):
        return True
    return not re.match(rf"[{TOKEN_WORD_CHARS}]", value[len(prefix)])


def _fallback_skeleton_branch(gateway: SkeletonGateway) -> SkeletonBranch:
    for branch in gateway.branches:
        if branch.items and not branch.stop_after:
            return branch
    for branch in gateway.branches:
        if branch.items:
            return branch
    return gateway.branches[0]


def suggest_recovery_skills(phase: Phase, gateway_result: dict, state: SessionState) -> list[str]:
    """Infer the smallest useful recovery chain when a gateway fails."""
    missing = " ".join(str(item) for item in gateway_result.get("missing") or [])
    recommendation = str(gateway_result.get("recommendation") or "")
    text = f"{missing} {recommendation}".lower()
    suggestions: list[str] = []

    def has_token(token: str) -> bool:
        pattern = rf"(?<![{TOKEN_WORD_CHARS}]){re.escape(token)}(?![{TOKEN_WORD_CHARS}])"
        return bool(re.search(pattern, text, re.IGNORECASE))

    def has_any_token(*tokens: str) -> bool:
        return any(has_token(token) for token in tokens)

    if phase == Phase.ANALYSIS:
        if "mpv" in text or "метрик" in text:
            suggestions.append("@akts")
        if "причин" in text:
            suggestions.append("@causal_analysis")
        if "противореч" in text:
            suggestions.append("@contradictions")
    elif phase == Phase.MODELING:
        if "оператив" in text or has_any_token("оз", "ов", "oz", "ov"):
            suggestions.append("@oz_ov")
        if "ресурс" in text:
            if not state.oz_ov_done:
                suggestions.append("@oz_ov")
            suggestions.append("@resource_analysis")
        if has_any_token("икр", "ikr", "ifr") or "идеальный конечный результат" in text:
            suggestions.append("@ikr")
        if "вепол" in text:
            suggestions.append("@vepoli")
        if "противореч" in text or has_any_token("тп", "фп", "tp", "fp", "tc", "pc"):
            suggestions.append("@contradictions")
    elif phase == Phase.SYNTHESIS:
        if "критик" in text:
            suggestions.append("@critic")
        if "концеп" in text or "решени" in text:
            if state.vepol_built:
                suggestions.append("@standards")
            elif state.contradiction_formulated:
                suggestions.append("@forty_principles")
            else:
                suggestions.append("@effects")

    unique: list[str] = []
    for skill in suggestions:
        if skill in unique:
            continue
        if state.has_called(skill):
            continue
        unique.append(skill)
    return unique


def _evaluate_gateway(
    task: str,
    phase: Phase,
    phase_results: list[StepResult],
    result: PipelineResult,
    phase_backtracks: dict[Phase, int],
    **llm_kwargs,
) -> list[str]:
    gateway = check_gateway(task, phase, phase_results, **llm_kwargs)
    result.gateway_events.append(
        f"{phase.value}: "
        f"{'pass' if gateway.get('gate_passed', True) else 'fail'} / "
        f"{gateway.get('recommendation', 'continue')}"
    )

    if gateway.get("gate_passed", True):
        return []

    result.backtracks += 1
    phase_backtracks[phase] = phase_backtracks.get(phase, 0) + 1
    phase_results[-1].gate_passed = False

    missing = gateway.get("missing") or []
    if missing:
        phase_results[-1].warnings.append(f"Gateway failed: {'; '.join(missing)}")

    if result.backtracks > MAX_BACKTRACKS_TOTAL:
        return []
    if phase_backtracks[phase] > MAX_BACKTRACKS_PER_PHASE:
        return []

    recovery_skills = suggest_recovery_skills(phase, gateway, result.state)
    if recovery_skills:
        phase_results[-1].warnings.append(
            f"Gateway recovery inserted: {', '.join(recovery_skills)}"
        )
    return recovery_skills


def _execute_sequence(
    skills: list[str],
    task: str,
    result: PipelineResult,
    previous_context: str,
    **llm_kwargs,
) -> str:
    queue = list(skills)
    phase_backtracks = {
        Phase.ANALYSIS: 0,
        Phase.MODELING: 0,
        Phase.SYNTHESIS: 0,
    }
    current_phase: Phase | None = None
    phase_results: list[StepResult] = []
    index = 0

    while index < len(queue):
        skill = queue[index]
        step_phase = infer_phase(skill)
        if current_phase is None:
            current_phase = step_phase
        elif step_phase != current_phase:
            current_phase = step_phase
            phase_results = []

        try:
            step = execute_skill(
                skill=skill,
                task=task,
                state=result.state,
                previous_context=previous_context,
                **llm_kwargs,
            )
        except MicroChainViolation as error:
            step = _skipped_step(skill, error)

        result.steps.append(step)
        phase_results.append(step)
        previous_context = _append_context(previous_context, skill, step)

        next_phase = infer_phase(queue[index + 1]) if index + 1 < len(queue) else Phase.DONE
        if current_phase != Phase.DONE and next_phase != current_phase:
            recovery_skills = _evaluate_gateway(
                task=task,
                phase=current_phase,
                phase_results=phase_results,
                result=result,
                phase_backtracks=phase_backtracks,
                **llm_kwargs,
            )
            if recovery_skills:
                queue[index + 1:index + 1] = recovery_skills
            else:
                current_phase = None
                phase_results = []

        index += 1

    return previous_context


def _execute_skeleton_plan(
    items: list[SkeletonItem],
    task: str,
    result: PipelineResult,
    previous_context: str,
    skip_skills: set[str] | None = None,
    **llm_kwargs,
) -> str:
    queue = list(items)
    skipped = skip_skills or set()
    phase_backtracks = {
        Phase.ANALYSIS: 0,
        Phase.MODELING: 0,
        Phase.SYNTHESIS: 0,
    }
    current_phase: Phase | None = None
    phase_results: list[StepResult] = []
    index = 0

    while index < len(queue):
        item = queue[index]
        if isinstance(item, SkeletonGateway):
            branch = choose_skeleton_branch(task, item, previous_context, **llm_kwargs)
            result.gateway_events.append(f"skeleton: {item.question} -> {branch.label}")
            insertion = list(branch.items)
            queue[index + 1:index + 1] = insertion
            if branch.stop_after:
                del queue[index + 1 + len(insertion):]
            index += 1
            continue

        skill = item.skill
        if skill in skipped:
            index += 1
            continue

        step_phase = infer_phase(skill)
        if current_phase is None:
            current_phase = step_phase
        elif step_phase != current_phase:
            current_phase = step_phase
            phase_results = []

        try:
            step = execute_skill(
                skill=skill,
                task=task,
                state=result.state,
                previous_context=previous_context,
                **llm_kwargs,
            )
        except MicroChainViolation as error:
            step = _skipped_step(skill, error)

        result.steps.append(step)
        phase_results.append(step)
        previous_context = _append_context(previous_context, skill, step)

        next_phase = _next_known_skeleton_phase(queue, index)
        if (
            next_phase is not None
            and current_phase != Phase.DONE
            and next_phase != current_phase
        ):
            recovery_skills = _evaluate_gateway(
                task=task,
                phase=current_phase,
                phase_results=phase_results,
                result=result,
                phase_backtracks=phase_backtracks,
                **llm_kwargs,
            )
            if recovery_skills:
                queue[index + 1:index + 1] = [
                    SkeletonSkill(skill) for skill in recovery_skills
                ]
            else:
                current_phase = None
                phase_results = []

        index += 1

    return previous_context


def _next_known_skeleton_phase(
    queue: list[SkeletonItem],
    index: int,
) -> Phase | None:
    for item in queue[index + 1:]:
        if isinstance(item, SkeletonGateway):
            return None
        return infer_phase(item.skill)
    return Phase.DONE


def run_pipeline(task: str, **llm_kwargs) -> PipelineResult:
    """
    Execute the full TRIZ orchestrator v5 pipeline.

    Steps:
    1. Discovery + Triage: classify task → map
    2. If needed, execute discovery methods and reformulate the task
    3. Load skeleton map → extract skill sequence
    4. Execute each skill step-by-step with validation
    5. Check gateways between phases and inject minimal recovery chains

    Returns:
        PipelineResult with all steps and final output
    """
    triage_result, discovery = triage_with_discovery(task, **llm_kwargs)
    provisional_triage = triage_result or TriageResult(
        map_code="DISCOVERY",
        map_name="Discovery Pending",
        confidence=0.0,
        reasoning="Task requires problem formulation before map selection.",
    )
    result = PipelineResult(task=task, triage=provisional_triage)

    execution_task = task
    previous_context = ""

    if discovery:
        logger.info(
            "Task is vague. Running discovery chain for scenario '%s' (confidence: %.2f)",
            discovery.category,
            discovery.confidence,
        )
        discovery_skills = [f"@{method}" for method in discovery.methods]
        previous_context = _execute_sequence(
            discovery_skills,
            task,
            result,
            previous_context,
            **llm_kwargs,
        )

        discovery_outputs = [
            step.output
            for step in result.steps
            if step.skill in discovery_skills and not step.output.startswith("SKIPPED:")
        ]
        execution_task = reformulate_task(task, discovery, discovery_outputs, **llm_kwargs)
        result.formulated_task = execution_task
        triage_result, _ = triage_with_discovery(
            task,
            formulated_task=execution_task,
            **llm_kwargs,
        )
        if triage_result is not None:
            result.triage = triage_result
    elif triage_result is not None:
        result.triage = triage_result

    result.map_content = get_skeleton_map(result.triage.map_code) or ""
    skeleton_plan = parse_skeleton_map_plan(result.map_content)
    skills = parse_skeleton_map_skills(result.map_content)
    if discovery:
        executed_discovery_skills = {f"@{method}" for method in discovery.methods}
        skills = [skill for skill in skills if skill not in executed_discovery_skills]
    else:
        executed_discovery_skills = set()

    if skeleton_plan:
        _execute_skeleton_plan(
            skeleton_plan,
            execution_task,
            result,
            previous_context,
            skip_skills=executed_discovery_skills,
            **llm_kwargs,
        )
    elif skills:
        if _has_skeleton_gateway_markup(result.map_content):
            result.gateway_events.append(
                f"skeleton: malformed gateway map for code {result.triage.map_code}; "
                "flat fallback skipped"
            )
        else:
            _execute_sequence(skills, execution_task, result, previous_context, **llm_kwargs)

    result.final_output = _build_routing_output(result)
    return result


def _build_routing_output(result: PipelineResult) -> str:
    """Build human-readable routing output for comparison with v4.2."""
    lines = [
        "## Routing Report (Orchestrator v5)",
        "",
        f"### 1. Выбранная карта: {result.triage.map_code} ({result.triage.map_name})",
        f"**Обоснование:** {result.triage.reasoning}",
        f"**Уверенность:** {result.triage.confidence}",
    ]

    if result.formulated_task:
        lines.extend([
            "",
            "### 1a. Сформулированная задача после discovery:",
            result.formulated_task,
        ])

    lines.extend([
        "",
        "### 2. Порядок вызовов скиллов:",
    ])

    for index, step in enumerate(result.steps, 1):
        status = "✅" if step.gate_passed else "⚠️"
        lines.append(f"{index}. {status} **{step.skill}** (confidence: {step.confidence})")
        if step.output and not step.output.startswith("SKIPPED"):
            lines.append(f"   → {step.output[:150]}...")
        for warning in step.warnings:
            lines.append(f"   ⚠️ {warning}")

    lines.extend([
        "",
        "### 3. Hard Micro-Chains:",
        f"Все проверены программно. Нарушений: "
        f"{sum(1 for step in result.steps if not step.gate_passed)}",
        "",
        "### 4. Gateway-логика:",
    ])

    if result.gateway_events:
        lines.extend(f"- {event}" for event in result.gateway_events)
    else:
        lines.append("- Gateway boundary не срабатывал (одна фаза или пустой маршрут).")

    return "\n".join(lines)
