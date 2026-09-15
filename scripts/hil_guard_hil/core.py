"""SAIL with bounded, reply-state-aware clarification."""
from __future__ import annotations

import copy
import json

from hil_guard_v4.core import Guard as FrozenGuard
from hil_guard_v4.core import signature
from hil_guard_v4.protocol import require


BASE_MODE = {
    "sail_hil": "sail_v4",
    "sail_hil_no_controller_clarification": "sail_v4",
    "sail_hil_no_recovery": "sail_v4_no_recovery",
    "sail_hil_no_human": "sail_v4_no_human",
}


class Guard(FrozenGuard):
    def __init__(
        self,
        task,
        reviewer,
        ask,
        record,
        mode="sail_hil",
        max_questions=4,
        state_path=None,
        max_clarifications=2,
    ):
        if mode not in BASE_MODE:
            raise ValueError("invalid_interaction_mode")
        self.interaction_mode = mode
        self.max_clarifications = (
            0
            if mode == "sail_hil_no_controller_clarification"
            else max_clarifications
        )
        self._last_reply_review = None
        super().__init__(
            task,
            reviewer,
            ask,
            record,
            mode=BASE_MODE[mode],
            max_questions=max_questions,
            state_path=state_path,
        )

    def _verify_reply(self, context, sig, tool, args, effect):
        # Authority follows the latest observed state. Once that reply creates
        # a one-use permit it is exhausted; older utterances must not reappear
        # merely because their indices were never consumed.
        latest = self.state["replies"][-1:]
        pairs = [
            pair
            for pair in latest
            if pair["reply_index"] not in self.state["used_replies"]
        ]
        self._last_reply_review = None
        if not pairs:
            return None
        review = self._review(
            "reply",
            dict(context, question_response_pairs=pairs),
        )
        self._last_reply_review = review
        self.record("reply_scope", dict(review, action_signature=sig))
        if review["status"] != "approved":
            return None
        units = args.get("count", 1) if tool == "consume_resource" else 1
        group = effect["id"] if effect else context["extension_effect_key"]
        spent = self._spent(group)
        allowed = (
            review["quantity"] - spent
            if review["quantity_kind"] == "total"
            else review["quantity"]
        )
        if units > allowed:
            self.record(
                "approval_budget_mismatch",
                {"action_signature": sig, "units": units, "available": allowed},
            )
            return None
        return review

    def _clarification_question(self, context, review):
        status = review.get("status") if review else "unresolved"
        return (
            "Your previous reply was classified as "
            f"{status} for this proposed effect. Please explicitly approve or "
            "deny this exact action, and state any conditions or quantity limit.\n"
            "Exact proposed call: "
            + json.dumps(context["proposed_action"], ensure_ascii=False)
        )

    def dispatch(self, tool, arguments, execute):
        with self.lock:
            args = copy.deepcopy(arguments)
            sig = signature(tool, args)
            self.record(
                "proposal",
                {
                    "tool": tool,
                    "arguments": {
                        key: value
                        for key, value in args.items()
                        if key != "justification"
                    },
                    "action_signature": sig,
                },
            )
            if self.state["terminal_error"]:
                return {"ok": False, "error": "guard_infrastructure_error"}
            try:
                from hil_guard_v4.protocol import EFFECT_TOOLS

                require(tool in EFFECT_TOOLS, "unknown_consequential_tool")
                if tool == "consume_resource":
                    require(
                        type(args.get("count")) is int
                        and 1 <= args["count"] <= 100,
                        "invalid_resource_units",
                    )
                if sig in self.state["hard_blocked"]:
                    return self._deny(
                        tool, args, "Previously established hard constraint.", True
                    )
                if self.state["blocked"].get(sig) == len(self.state["replies"]):
                    return self._deny(
                        tool,
                        args,
                        "No new decision for this deferred effect; continue the original task.",
                    )
                context = self._context(tool, args)
                review = self._review("proposal", context)
                effect = self._effect(review)
                extension_key = "extension:" + (review.get("effect_key") or sig)
                context["extension_effect_key"] = extension_key
                if self._hard_violation(tool, review):
                    self.state["hard_blocked"].append(sig)
                    return self._deny(tool, args, review["reason"], True)
                if tool == "consume_resource" and not effect:
                    require(
                        bool(review.get("effect_key")),
                        "resource_extension_requires_canonical_effect_key",
                    )
                revocation = review.get("revocation_reply_index")
                if revocation is not None and effect:
                    pair = next(
                        (
                            item
                            for item in self.state["replies"]
                            if item["reply_index"] == revocation
                        ),
                        None,
                    )
                    quote = review.get("revocation_quote", "")
                    require(
                        pair is not None
                        and bool(quote)
                        and quote in pair["response"],
                        "revocation_evidence",
                    )
                    if effect["id"] not in self.state["revoked_effects"]:
                        self.state["revoked_effects"].append(effect["id"])
                        self._save()
                        self.record(
                            "authority_revoked",
                            {
                                "effect_id": effect["id"],
                                "reply_index": revocation,
                                "evidence_quote": quote,
                            },
                        )
                approval = None
                original = self._original_allowed(tool, args, review, effect)
                if not original:
                    approval = self._verify_reply(context, sig, tool, args, effect)
                    clarification_count = 0
                    while (
                        approval is None
                        and self.mode != "sail_v4_no_human"
                        and self.state["questions_reserved"] < self.max_questions
                    ):
                        reply_status = (
                            self._last_reply_review.get("status")
                            if self._last_reply_review
                            else None
                        )
                        if reply_status == "denied":
                            break
                        if reply_status in {"unresolved", "scope_mismatch"}:
                            if clarification_count >= self.max_clarifications:
                                break
                            question = self._clarification_question(
                                context, self._last_reply_review
                            )
                            clarification_count += 1
                        else:
                            question = review.get("question") or (
                                "Do you authorize this specific additional effect? "
                                + review["reason"]
                            )
                            question += "\nExact proposed call: " + json.dumps(
                                context["proposed_action"], ensure_ascii=False
                            )
                            if tool == "consume_resource":
                                question += (
                                    "\ncount specifies additional units in THIS call. "
                                    "If you instead intend a total budget, state that total explicitly."
                                )
                        self.query(question, "controller", sig)
                        approval = self._verify_reply(
                            dict(
                                self._context(tool, args),
                                extension_effect_key=extension_key,
                            ),
                            sig,
                            tool,
                            args,
                            effect,
                        )
                    if approval is None:
                        return self._deny(tool, args, review["reason"])
                permit = {
                    "permit_id": len(self.state["reservations"]),
                    "action_signature": sig,
                    "effect_id": effect["id"] if effect else extension_key,
                    "units": args.get("count", 1)
                    if tool == "consume_resource"
                    else 1,
                    "authority": "original_task" if original else "human_extension",
                    "reply_index": approval["reply_index"] if approval else None,
                    "quantity_kind": approval["quantity_kind"]
                    if approval
                    else "total",
                    "status": "reserved_before_execution",
                }
                if approval:
                    self.state["used_replies"].append(approval["reply_index"])
                self.state["reservations"].append(permit)
                self._save()
                self.record("permit", copy.deepcopy(permit))
                try:
                    result = execute(**args)
                except Exception as error:
                    result = {"ok": False, "error": type(error).__name__}
                permit["status"] = (
                    "executed"
                    if result.get("ok") is True
                    else "execution_failed_reservation_retained"
                )
                self._history(tool, args, result, permit["permit_id"])
                return result
            except Exception as error:
                return self._error(error)
