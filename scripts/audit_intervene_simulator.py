"""Deterministic audit and blinded annotation sampling for simulator banks."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import random
import re
from collections import Counter, defaultdict
from pathlib import Path

from hil_safety_bench.human_simulator import POLICY_BY_ID, stateful_case_from_dict


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def tokens(text: str) -> list[str]:
    return re.findall(r"[a-z0-9@._/-]+", text.lower())


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("bank", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--annotation-csv", type=Path, required=True)
    parser.add_argument("--annotation-per-policy", type=int, default=10)
    parser.add_argument("--annotation-seed", type=int, default=2026091403)
    args = parser.parse_args()
    cases_path = args.bank / "cases.jsonl"
    cases = [
        stateful_case_from_dict(json.loads(line))
        for line in cases_path.read_text().splitlines()
        if line.strip()
    ]
    violations = []
    policy_counts = Counter()
    task_policies = defaultdict(set)
    texts = []
    all_tokens = []
    bigrams = []
    rows_by_policy = defaultdict(list)
    for case in cases:
        response = case.human_response
        policy = POLICY_BY_ID.get(response.policy_id)
        if policy is None:
            violations.append([case.case_id, "unknown_policy"])
            continue
        policy_counts[policy.policy_id] += 1
        task_policies[case.task.task_id].add(policy.policy_id)
        if len(response.turns) != len(policy.turns):
            violations.append([case.case_id, "turn_count"])
        for index, (actual, expected) in enumerate(
            zip(response.turns, policy.turns, strict=False)
        ):
            if (
                actual.category,
                actual.decision,
                actual.scope,
            ) != (expected.category, expected.decision, expected.scope):
                violations.append([case.case_id, f"turn_{index}_contract"])
            if not actual.text.strip() or len(actual.text) > 600:
                violations.append([case.case_id, f"turn_{index}_length"])
            if any(
                marker in actual.text.lower()
                for marker in (
                    "policy_id",
                    "response category",
                    "benchmark label",
                    "fixed generation seed",
                )
            ):
                violations.append([case.case_id, f"turn_{index}_label_leak"])
            texts.append(actual.text)
            words = tokens(actual.text)
            all_tokens.extend(words)
            bigrams.extend(zip(words, words[1:]))
        turns = list(response.turns)
        rows_by_policy[policy.policy_id].append(
            {
                "case_id": case.case_id,
                "task_id": case.task.task_id,
                "domain": case.task.domain,
                "attack_family": case.task.attack.attack_type,
                "authorization_mode": case.task.attack.authorization_mode,
                "original_task": case.task.benign_goal,
                "proposed_action": case.task.attack.injected_instruction,
                "turn_1": turns[0].text if turns else "",
                "turn_2": turns[1].text if len(turns) > 1 else "",
            }
        )
    expected_policies = set(POLICY_BY_ID)
    for task_id, observed in task_policies.items():
        if observed != expected_policies:
            violations.append([task_id, "incomplete_policy_block"])
    text_counts = Counter(texts)
    report = {
        "bank": str(args.bank),
        "cases_jsonl_sha256": sha256(cases_path),
        "case_count": len(cases),
        "task_count": len(task_policies),
        "policy_counts": dict(policy_counts),
        "turn_count": len(texts),
        "unique_response_rate": len(text_counts) / len(texts) if texts else 0,
        "duplicate_response_count": sum(
            count - 1 for count in text_counts.values() if count > 1
        ),
        "distinct_1": len(set(all_tokens)) / len(all_tokens) if all_tokens else 0,
        "distinct_2": len(set(bigrams)) / len(bigrams) if bigrams else 0,
        "construction_contract_violations": violations,
        "construction_contract_pass": not violations,
        "interpretation_boundary": (
            "Construction checks and lexical diversity do not establish human "
            "realism or semantic fidelity; those require blinded annotation."
        ),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + "\n")
    rng = random.Random(args.annotation_seed)
    annotation_rows = []
    for policy_id in sorted(rows_by_policy):
        candidates = list(rows_by_policy[policy_id])
        rng.shuffle(candidates)
        annotation_rows.extend(candidates[: args.annotation_per_policy])
    rng.shuffle(annotation_rows)
    args.annotation_csv.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "annotation_id",
        "original_task",
        "proposed_action",
        "turn_1",
        "turn_2",
        "annotator_decision_turn_1",
        "annotator_scope_turn_1",
        "annotator_decision_turn_2",
        "annotator_scope_turn_2",
        "naturalness_1_5",
        "sequence_coherent_yes_no",
        "notes",
    ]
    with args.annotation_csv.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for index, row in enumerate(annotation_rows, start=1):
            writer.writerow(
                {
                    "annotation_id": f"H{index:03d}",
                    "original_task": row["original_task"],
                    "proposed_action": row["proposed_action"],
                    "turn_1": row["turn_1"],
                    "turn_2": row["turn_2"],
                }
            )
    key_path = args.annotation_csv.with_name(
        args.annotation_csv.stem + "_private_key.json"
    )
    key_path.write_text(
        json.dumps(
            {
                f"H{index:03d}": {
                    key: row[key]
                    for key in (
                        "case_id",
                        "task_id",
                        "attack_family",
                        "authorization_mode",
                    )
                }
                | {
                    "target_policy": next(
                        policy_id
                        for policy_id, candidates in rows_by_policy.items()
                        if row in candidates
                    )
                }
                for index, row in enumerate(annotation_rows, start=1)
            },
            indent=2,
        )
        + "\n"
    )
    print(json.dumps(report))


if __name__ == "__main__":
    main()
