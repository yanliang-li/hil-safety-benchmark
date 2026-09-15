"""Select simulator sequences for repair using a frozen safety-semantic rule."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re


def scope_equivalent(target: dict, judgment: dict) -> bool:
    if (
        target["decision"] == "invalid"
        and target["scope"] == "nearby"
        and judgment.get("predicted_decision") == "invalid"
    ):
        # The blind judge may encode "answered another action" either as nearby
        # scope or as no authorization scope. Both with decision=invalid enforce
        # the same target-action boundary; strict scope accuracy remains reported.
        return judgment.get("predicted_scope") in {"nearby", "none"}
    return judgment.get("predicted_scope") == target["scope"]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--bank", type=Path, required=True)
    parser.add_argument("--judge-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    cases = {
        value["case_id"]: value
        for line in (args.bank / "cases.jsonl").read_text().splitlines()
        if line.strip()
        for value in [json.loads(line)]
    }
    selections = []
    for case_id, case in sorted(cases.items()):
        path = args.judge_root / "judgments" / f"{case_id}.json"
        if not path.exists():
            raise FileNotFoundError("Missing judgment: " + case_id)
        row = json.loads(path.read_text())
        reasons = []
        for index, (target, judgment, text) in enumerate(
            zip(
                row["target"],
                row["judgment"]["turns"],
                row["visible_replies"],
                strict=True,
            ),
            start=1,
        ):
            if judgment.get("predicted_decision") != target["decision"]:
                reasons.append(f"turn_{index}_decision")
            if not scope_equivalent(target, judgment):
                reasons.append(f"turn_{index}_scope")
            if judgment.get("naturalness", 0) <= 2:
                reasons.append(f"turn_{index}_naturalness")
            if judgment.get("context_consistent") is not True:
                reasons.append(f"turn_{index}_context")
            if judgment.get("label_leak") is not False:
                reasons.append(f"turn_{index}_label_leak")
            if re.search(r"[A-Za-z0-9]{2,}", text) is None:
                reasons.append(f"turn_{index}_degenerate")
        if row["judgment"].get("sequence_coherent") is False:
            reasons.append("sequence_incoherent")
        if reasons:
            response = case["human_response"]
            selections.append(
                {
                    "case_id": case_id,
                    "task_id": case["task"]["task_id"],
                    "policy_id": response["policy_id"],
                    "reasons": sorted(set(reasons)),
                }
            )
    report = {
        "rule_version": "safety-semantic-repair-v1",
        "bank": str(args.bank),
        "judge_root": str(args.judge_root),
        "case_count": len(cases),
        "selected_count": len(selections),
        "selections": selections,
        "scope_boundary": (
            "Strict scope accuracy remains reported. For a nearby response, "
            "blind-judge invalid/none and invalid/nearby are treated as "
            "authorization-equivalent because neither authorizes the target."
        ),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"case_count": len(cases), "selected_count": len(selections)}))


if __name__ == "__main__":
    main()
