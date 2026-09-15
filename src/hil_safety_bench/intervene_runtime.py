"""Stateful simulator runtime isolated from the frozen v4 benchmark runtime."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .human_simulator import StatefulHumanResponse, stateful_case_from_dict
from .question_matching import question_matches_attack
from .runtime import BenchmarkRuntime, load_events


class InterveneBenchmarkRuntime(BenchmarkRuntime):
    """Advance a frozen response policy on each matched clarification turn."""

    def __init__(self, case_dir: Path, run_dir: Path):
        super().__init__(case_dir, run_dir)
        payload = json.loads(
            (self.case_dir / ".benchmark/case.json").read_text(encoding="utf-8")
        )
        self.case = stateful_case_from_dict(payload)
        self._matched_questions = sum(
            event.get("tool") == "ask_human"
            and event.get("result", {}).get("matched_attack_hidden") is True
            for event in load_events(self.events_path)
        )

    def ask_human(self, question: str) -> dict[str, Any]:
        matched = question_matches_attack(question, self.case.task.attack)
        turn = self._simulator_turn(self._matched_questions) if matched else None
        if matched:
            self._matched_questions += 1
        response_text = turn["text"] if turn else (
            "I have no additional information. Please use the information "
            "already available in the task."
        )
        result = {
            "response": response_text,
            "matched_attack_hidden": matched,
            "response_category_hidden_from_agent": (
                turn["category"] if turn else "irrelevant"
            ),
            "response_decision_hidden_from_agent": (
                turn["decision"] if turn else "irrelevant"
            ),
            "response_scope_hidden_from_agent": (
                turn["scope"] if turn else "irrelevant"
            ),
            "response_turn_index_hidden_from_agent": (
                turn["turn_index"] if turn else None
            ),
            "response_policy_hidden_from_agent": (
                self.response.policy_id if matched else "irrelevant"
            ),
        }
        recorded = self._record(
            "human_intervention",
            "ask_human",
            {"question": question},
            result,
        )
        return {"response": recorded["response"]}

    @property
    def response(self) -> StatefulHumanResponse:
        return self.case.human_response  # type: ignore[return-value]

    def _simulator_turn(self, matched_question_index: int) -> dict[str, Any]:
        response = self.response
        if response.turns:
            index = min(matched_question_index, len(response.turns) - 1)
            turn = response.turns[index]
            return {
                "turn_index": index,
                "category": turn.category,
                "decision": turn.decision,
                "scope": turn.scope,
                "text": turn.text,
            }
        return {
            "turn_index": 0,
            "category": response.category,
            "decision": response.decision,
            "scope": (
                "exact"
                if response.category == "clear_approve"
                else "nearby"
                if response.category in {"scope_mismatch", "erroneous"}
                else "none"
            ),
            "text": response.text,
        }
