"""
TRIZ Orchestrator v5 — Micro-Chain & Anti-Trigger Validators

Programmatic enforcement of TRIZ skill ordering rules.
In v4.2 these were embedded in the prompt text.
In v5 they are Python code with hard assertions.
"""

import re
from dataclasses import dataclass, field

TOKEN_WORD_CHARS = "0-9A-Za-zА-Яа-яЁё_"


# ──────────────────────────────────────────────────────────
# Hard Micro-Chains: skill B can only run AFTER skill A
# ──────────────────────────────────────────────────────────

HARD_MICRO_CHAINS: dict[str, list[str]] = {
    # skill -> list of skills that MUST have run before it
    "@trimming": ["@functional_analysis", "@flow_analysis", "@value_analysis"],  # any one
    "@forty_principles": ["@contradictions"],
    "@standards": ["@vepoli"],
    "@resource_analysis": ["@oz_ov"],
}

# Micro-chains where the requirement is ANY (not ALL)
MICRO_CHAINS_ANY: set[str] = {"@trimming"}

# Micro-chains where the requirement is ALL
MICRO_CHAINS_ALL: set[str] = {"@forty_principles", "@standards", "@resource_analysis"}


# ──────────────────────────────────────────────────────────
# Anti-Trigger Matrix: when NOT to call a skill
# ──────────────────────────────────────────────────────────

ANTI_TRIGGERS: dict[str, str] = {
    "@forty_principles": "no_contradiction_formulated",
    "@effects": "no_function_or_ikr",
    "@ariz": "task_solvable_by_single_tool",
    "@trimming": "no_analysis_completed",
    "@fos": "function_not_abstracted",
    "@vepoli": "no_interaction_data",
    "@standards": "no_vepol_model",
    "@chemical_triz": "no_chemistry_domain",
}


@dataclass
class SessionState:
    """Tracks what skills have been called and what artifacts exist."""

    called_skills: list[str] = field(default_factory=list)
    artifacts: dict[str, object] = field(default_factory=dict)

    # Flags set by skill outputs
    fa_done: bool = False
    fap_done: bool = False       # flow analysis done
    fsa_done: bool = False       # value analysis done
    contradiction_formulated: bool = False
    vepol_built: bool = False
    oz_ov_done: bool = False
    function_abstracted: bool = False
    interaction_data: bool = False
    ikr_formulated: bool = False
    simple_solution: bool = False
    chemistry_domain: bool = False

    def has_called(self, skill: str) -> bool:
        return skill in self.called_skills

    def has_any(self, *flags: str) -> bool:
        return any(getattr(self, flag, False) for flag in flags)

    def record_call(self, skill: str) -> None:
        if skill not in self.called_skills:
            self.called_skills.append(skill)

    def record_result(self, skill: str, artifacts: object, output: str | None) -> None:
        """Record a skill result and set state flags only from validated evidence."""
        self.record_call(skill)
        safe_artifacts = artifacts if isinstance(artifacts, dict) else {}
        if safe_artifacts:
            self.artifacts[skill] = safe_artifacts
        self._update_flags_from_result(skill, safe_artifacts, output or "")

    def _update_flags_from_result(self, skill: str, artifacts: dict, output: str) -> None:
        """Auto-update flags from concrete artifacts/output markers, not invocation alone."""
        keys = {str(key).lower() for key in artifacts}
        values_text = " ".join(str(value) for value in artifacts.values())
        text = f"{output}\n{values_text}".lower()

        if skill == "@functional_analysis":
            if (
                {"action", "object"} <= keys
                or {"функция", "объект"} <= keys
                or _has_token(text, "action")
                and _has_token(text, "object")
                or _has_stem(text, "функци")
                or _has_token(text, "function")
            ):
                self.fa_done = True
                self.function_abstracted = True
                self.interaction_data = True
        elif skill == "@flow_analysis":
            if (
                _has_token(text, "flow")
                or _has_stem(text, "поток")
                or _has_token(text, "throughput")
            ):
                self.fap_done = True
                self.interaction_data = True
        elif skill == "@value_analysis":
            if (
                _has_token(text, "value")
                or _has_token(text, "cost")
                or _has_stem(text, "ценност")
            ):
                self.fsa_done = True
        elif skill == "@contradictions":
            if (
                {"tp", "fp"} & keys
                or {"tc", "pc"} & keys
                or {"тп", "фп"} & keys
                or _has_token(text, "tp")
                or _has_token(text, "fp")
                or _has_token(text, "tc")
                or _has_token(text, "pc")
                or _has_token(text, "тп")
                or _has_token(text, "фп")
                or "technical contradiction" in text
                or "physical contradiction" in text
                or "техническое противоречие" in text
                or "физическое противоречие" in text
            ):
                self.contradiction_formulated = True
        elif skill == "@vepoli":
            if (
                {"s1", "s2"} <= keys
                or {"в1", "в2"} <= keys
                or _has_token(text, "s1")
                and _has_token(text, "s2")
                or _has_token(text, "в1")
                and _has_token(text, "в2")
                or "su-field" in text
                or _has_stem(text, "вепол")
                or _has_stem(text, "vepol")
            ):
                self.vepol_built = True
                self.interaction_data = True
        elif skill == "@oz_ov":
            if (
                {"operational_zone", "operational_time"} <= keys
                or {"oz", "ov"} <= keys
                or {"оз", "ов"} <= keys
                or "operational zone" in text
                and "operational time" in text
                or "оперативная зона" in text
                and "оперативное время" in text
                or _has_token(text, "оз")
                and _has_token(text, "ов")
            ):
                self.oz_ov_done = True
        elif skill == "@ikr":
            if (
                {"ikr", "ifr", "икр"} & keys
                or _has_token(text, "ikr")
                or _has_token(text, "ifr")
                or _has_token(text, "икр")
                or "идеальный конечный результат" in text
                or "ideal final result" in text
            ):
                self.ikr_formulated = True
        elif skill == "@fos":
            if (
                _has_token(text, "function")
                or _has_stem(text, "функци")
                or _has_stem(text, "abstract")
            ):
                self.function_abstracted = True
        elif skill == "@chemical_triz":
            if any(
                _has_stem(text, stem)
                for stem in ("chem", "хим", "reaction", "реакци")
            ):
                self.chemistry_domain = True


def _has_token(text: str, token: str) -> bool:
    pattern = rf"(?<![{TOKEN_WORD_CHARS}]){re.escape(token)}(?![{TOKEN_WORD_CHARS}])"
    return bool(re.search(pattern, text, re.IGNORECASE))


def _has_stem(text: str, stem: str) -> bool:
    return bool(re.search(rf"(?<![0-9A-Za-zА-Яа-яЁё_]){re.escape(stem)}", text, re.IGNORECASE))


class MicroChainViolation(Exception):
    """Raised when a Hard Micro-Chain rule is violated."""

    def __init__(self, skill: str, required: list[str], mode: str = "any"):
        self.skill = skill
        self.required = required
        self.mode = mode
        msg = (
            f"Micro-Chain violation: {skill} requires "
            f"{'any of' if mode == 'any' else 'all of'} "
            f"{required} to run first"
        )
        super().__init__(msg)


class AntiTriggerViolation(Exception):
    """Raised when a skill is called in violation of Anti-Trigger rules."""

    def __init__(self, skill: str, reason: str):
        self.skill = skill
        self.reason = reason
        super().__init__(f"Anti-Trigger violation: {skill} — {reason}")


def validate_micro_chains(skill: str, state: SessionState) -> None:
    """
    Check if calling `skill` violates any Hard Micro-Chain rules.

    Raises:
        MicroChainViolation: if the skill cannot be called yet
    """
    required = HARD_MICRO_CHAINS.get(skill)
    if required is None:
        return  # No constraints

    if skill in MICRO_CHAINS_ANY:
        # At least ONE of the required skills must have been called
        if not any(state.has_called(r) for r in required):
            raise MicroChainViolation(skill, required, mode="any")
    else:
        # ALL required skills must have been called
        missing = [r for r in required if not state.has_called(r)]
        if missing:
            raise MicroChainViolation(skill, missing, mode="all")


def validate_anti_triggers(skill: str, state: SessionState) -> str | None:
    """
    Check if calling `skill` violates Anti-Trigger rules.

    Returns:
        None if OK, or string reason if violation detected.
    """
    trigger = ANTI_TRIGGERS.get(skill)
    if trigger is None:
        return None

    checks: dict[str, bool] = {
        "no_contradiction_formulated": not state.contradiction_formulated,
        "no_function_or_ikr": not (state.fa_done or state.ikr_formulated),
        "task_solvable_by_single_tool": state.simple_solution,
        "no_analysis_completed": not state.has_any("fa_done", "fap_done", "fsa_done"),
        "function_not_abstracted": not state.function_abstracted,
        "no_interaction_data": not state.interaction_data,
        "no_vepol_model": not state.vepol_built,
        "no_chemistry_domain": not state.chemistry_domain,
    }

    if checks.get(trigger, False):
        return trigger

    return None


def validate_skill_call(skill: str, state: SessionState) -> list[str]:
    """
    Full validation of a skill call.

    Returns:
        List of warning messages (empty if no issues).

    Raises:
        MicroChainViolation: for hard constraint violations
    """
    warnings: list[str] = []

    # Hard check — raises exception
    validate_micro_chains(skill, state)

    # Soft check — returns warning
    anti_reason = validate_anti_triggers(skill, state)
    if anti_reason:
        warnings.append(f"Anti-Trigger warning for {skill}: {anti_reason}")

    return warnings
