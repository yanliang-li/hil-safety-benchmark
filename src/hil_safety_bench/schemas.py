from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Literal


ResponseCategory = Literal[
    "clear_approve",
    "clear_deny",
    "ambiguous",
    "scope_mismatch",
    # Accepted only for loading legacy v2 artifacts.
    "erroneous",
]
Decision = Literal["approve", "deny", "unclear", "invalid"]
AuthorizationMode = Literal["confirmable", "prohibited"]


@dataclass(frozen=True)
class EffectSpec:
    tool: str
    match: dict[str, str]
    description: str


@dataclass(frozen=True)
class AttackSpec:
    attack_type: str
    source_file: str
    injected_instruction: str
    authorization_mode: AuthorizationMode
    risky_effect: EffectSpec
    risk_summary: str
    delivery_vector: str = "workspace_artifact"
    context_files: tuple[str, ...] = ()
    deceptive_rationale: str = ""
    risk_stage: str = "execution"


@dataclass(frozen=True)
class TaskTemplate:
    task_id: str
    title: str
    domain: str
    benign_goal: str
    files: dict[str, str]
    attack: AttackSpec
    required_benign_effects: tuple[EffectSpec, ...]
    policy_notes: tuple[str, ...] = ()


@dataclass(frozen=True)
class HumanResponse:
    category: ResponseCategory
    decision: Decision
    clarity_score: float
    text: str
    seed: int
    provider: str
    model: str | None = None
    style: str = "unspecified"


@dataclass(frozen=True)
class BenchmarkCase:
    case_id: str
    task: TaskTemplate
    human_response: HumanResponse
    generation_metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class Event:
    sequence: int
    timestamp: str
    event_type: str
    tool: str
    arguments: dict[str, Any]
    result: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def effect_from_dict(data: dict[str, Any]) -> EffectSpec:
    return EffectSpec(
        tool=data["tool"],
        match=dict(data.get("match", {})),
        description=data["description"],
    )


def task_from_dict(data: dict[str, Any]) -> TaskTemplate:
    attack_data = data["attack"]
    attack = AttackSpec(
        attack_type=attack_data["attack_type"],
        source_file=attack_data["source_file"],
        injected_instruction=attack_data["injected_instruction"],
        authorization_mode=attack_data["authorization_mode"],
        risky_effect=effect_from_dict(attack_data["risky_effect"]),
        risk_summary=attack_data["risk_summary"],
        delivery_vector=attack_data.get(
            "delivery_vector",
            "workspace_artifact",
        ),
        context_files=tuple(attack_data.get("context_files", [])),
        deceptive_rationale=attack_data.get("deceptive_rationale", ""),
        risk_stage=attack_data.get("risk_stage", "execution"),
    )
    return TaskTemplate(
        task_id=data["task_id"],
        title=data["title"],
        domain=data["domain"],
        benign_goal=data["benign_goal"],
        files=dict(data["files"]),
        attack=attack,
        required_benign_effects=tuple(
            effect_from_dict(item) for item in data["required_benign_effects"]
        ),
        policy_notes=tuple(data.get("policy_notes", [])),
    )


def case_from_dict(data: dict[str, Any]) -> BenchmarkCase:
    response_data = data["human_response"]
    return BenchmarkCase(
        case_id=data["case_id"],
        task=task_from_dict(data["task"]),
        human_response=HumanResponse(
            category=response_data["category"],
            decision=response_data["decision"],
            clarity_score=float(response_data["clarity_score"]),
            text=response_data["text"],
            seed=int(response_data["seed"]),
            provider=response_data["provider"],
            model=response_data.get("model"),
            style=response_data.get("style", "unspecified"),
        ),
        generation_metadata=dict(data.get("generation_metadata", {})),
    )
