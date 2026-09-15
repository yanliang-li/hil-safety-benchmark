"""Analyze InterveneBench formal runs with task-clustered paired intervals."""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import json
import math
from pathlib import Path
import random

from hil_safety_bench.intervene_evaluate import (
    InterveneCaseResult,
    aggregate_intervene,
)


ROOT = Path(__file__).resolve().parents[1]
REPAIRABLE = {
    "uncertain_then_approve",
    "uncertain_then_deny",
    "scope_repair_then_approve",
}


def repeat_summary(rows: list[dict], expected_repeats: int) -> dict:
    groups = defaultdict(list)
    for row in rows:
        groups[(row["task_id"], row["response_policy"])].append(row)
    complete = [
        values
        for values in groups.values()
        if len({value["repeat"] for value in values}) == expected_repeats
    ]
    if not complete:
        return {
            "expected_repeats": expected_repeats,
            "complete_task_policy_groups": 0,
            "benign_pass_at_k": None,
            "joint_safe_utility_pass_at_k": None,
            "safety_consistency_at_k": None,
        }

    def rate(predicate) -> float:
        return sum(bool(predicate(group)) for group in complete) / len(complete)

    return {
        "expected_repeats": expected_repeats,
        "complete_task_policy_groups": len(complete),
        "independent_task_clusters": len(
            {group[0]["task_id"] for group in complete}
        ),
        "benign_pass_at_k": rate(
            lambda group: any(row["result"]["benign_task_complete"] for row in group)
        ),
        "joint_safe_utility_pass_at_k": rate(
            lambda group: any(row["result"]["joint_safe_utility"] for row in group)
        ),
        "safety_consistency_at_k": rate(
            lambda group: all(
                not row["result"]["unsafe_attack_success"] for row in group
            )
        ),
        "unit_note": (
            "Each row is one task-policy group; task_id remains the independent "
            "cluster for inferential intervals."
        ),
    }


def save(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def percentile(values: list[float], probability: float) -> float:
    ordered = sorted(values)
    position = (len(ordered) - 1) * probability
    lower = math.floor(position)
    upper = math.ceil(position)
    if lower == upper:
        return ordered[lower]
    return ordered[lower] * (upper - position) + ordered[upper] * (position - lower)


def paired(
    rows: list[dict],
    left: str,
    right: str,
    metric: str,
    bootstrap: int,
    seed: int,
    policies: set[str] | None = None,
) -> dict:
    selected = [
        row
        for row in rows
        if row["condition"] in {left, right}
        and (policies is None or row["response_policy"] in policies)
        and row["result"].get(metric) is not None
    ]
    values = {
        condition: {
            (
                row["task_id"],
                row["response_policy"],
                row["repeat"],
            ): row["result"][metric]
            for row in selected
            if row["condition"] == condition
        }
        for condition in (left, right)
    }
    keys = sorted(set(values[left]) & set(values[right]))
    clusters = defaultdict(list)
    for key in keys:
        clusters[key[0]].append(
            float(values[right][key]) - float(values[left][key])
        )
    cluster_ids = sorted(clusters)
    if not cluster_ids:
        return {
            "left": left,
            "right": right,
            "difference_definition": "right minus left",
            "metric": metric,
            "matched_case_repeat_pairs": 0,
            "task_clusters": 0,
            "estimate": None,
            "task_cluster_bootstrap_95": None,
            "bootstrap_draws": 0,
            "bootstrap_seed": seed,
        }
    # task_id is the independent unit. Average policies and repeats within each
    # task before estimating or resampling so partially observed tasks cannot
    # receive more weight merely because they have more scorable episodes.
    cluster_means = {
        task_id: sum(task_values) / len(task_values)
        for task_id, task_values in clusters.items()
    }
    rng = random.Random(seed)
    draws = []
    for _ in range(bootstrap):
        sampled = [rng.choice(cluster_ids) for _ in cluster_ids]
        sample = [cluster_means[cluster] for cluster in sampled]
        draws.append(sum(sample) / len(sample))
    estimate = sum(cluster_means.values()) / len(cluster_means)
    return {
        "left": left,
        "right": right,
        "difference_definition": "right minus left",
        "metric": metric,
        "matched_case_repeat_pairs": len(keys),
        "task_clusters": len(cluster_ids),
        "cluster_weighting": "equal-weight task means",
        "estimate": estimate,
        "task_cluster_bootstrap_95": (
            [percentile(draws, 0.025), percentile(draws, 0.975)]
            if draws
            else None
        ),
        "bootstrap_draws": bootstrap,
        "bootstrap_seed": seed,
    }


def clustered_rate(
    rows: list[dict],
    metric: str,
    bootstrap: int,
    seed: int,
) -> dict:
    """Estimate a valid-run rate with equal-weight task-cluster intervals."""
    clusters = defaultdict(list)
    for row in rows:
        value = row["result"].get(metric)
        if value is not None:
            clusters[row["task_id"]].append(float(value))
    cluster_ids = sorted(clusters)
    if not cluster_ids:
        return {
            "metric": metric,
            "task_clusters": 0,
            "valid_episodes": 0,
            "estimate": None,
            "task_cluster_bootstrap_95": None,
            "bootstrap_draws": 0,
            "bootstrap_seed": seed,
        }
    means = {
        task_id: sum(values) / len(values)
        for task_id, values in clusters.items()
    }
    rng = random.Random(seed)
    draws = []
    for _ in range(bootstrap):
        sample = [means[rng.choice(cluster_ids)] for _ in cluster_ids]
        draws.append(sum(sample) / len(sample))
    return {
        "metric": metric,
        "task_clusters": len(cluster_ids),
        "valid_episodes": sum(len(values) for values in clusters.values()),
        "cluster_weighting": "equal-weight task means",
        "estimate": sum(means.values()) / len(means),
        "task_cluster_bootstrap_95": [
            percentile(draws, 0.025),
            percentile(draws, 0.975),
        ],
        "bootstrap_draws": bootstrap,
        "bootstrap_seed": seed,
        "missing_outcomes_excluded": True,
    }


def failure_category(folder: Path, status: dict) -> str:
    if status.get("guard_invalid"):
        return "guard_invalid"
    if status.get("oom_killed"):
        return "oom_killed"
    if status.get("scheduler_failure"):
        return "scheduler_" + str(status["scheduler_failure"])
    metadata = folder / "run_metadata.json"
    if metadata.exists():
        meta = json.loads(metadata.read_text())
        if meta.get("timed_out"):
            return "agent_timeout"
        if meta.get("runner_error"):
            return "runner_error"
        if meta.get("returncode") not in (None, 0):
            return "agent_nonzero"
        if not meta.get("successful_termination"):
            return "no_successful_termination"
    return "unclassified"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("plan", type=Path)
    parser.add_argument("--output-root", type=Path, required=True)
    parser.add_argument("--bootstrap", type=int, default=10000)
    parser.add_argument("--bootstrap-seed", type=int, default=2026091405)
    args = parser.parse_args()
    plan = json.loads(args.plan.read_text())
    rows, attempts = [], []
    for job in plan["jobs"]:
        folder = ROOT / "runs" / job["stage"] / job["run_id"]
        status_path = folder / "attempt_status.json"
        if not status_path.exists():
            attempts.append(dict(job, status="pending"))
            continue
        status = json.loads(status_path.read_text())
        result_path = folder / "result.json"
        if status.get("completed") and result_path.exists():
            result = InterveneCaseResult(**json.loads(result_path.read_text()))
            row = {
                "run_id": job["run_id"],
                "condition": job["condition"],
                "repeat": job["repeat"],
                "case_id": job["case_id"],
                "task_id": job["task_id"],
                "response_policy": job["response_policy"],
                "result": result.to_dict(),
            }
            rows.append(row)
            attempts.append(dict(job, status="valid"))
        else:
            attempts.append(
                dict(
                    job,
                    status="failed",
                    failure_category=failure_category(folder, status),
                )
            )
    by_condition = {}
    condition_intervals = {}
    pass_at_repeats = {}
    sensitivity = {}
    failures = {}
    for condition in plan["conditions"]:
        valid_rows = [row for row in rows if row["condition"] == condition]
        result_objects = [InterveneCaseResult(**row["result"]) for row in valid_rows]
        by_condition[condition] = aggregate_intervene(result_objects)
        condition_intervals[condition] = {
            metric: clustered_rate(
                valid_rows,
                metric,
                args.bootstrap,
                args.bootstrap_seed + 100 + index,
            )
            for index, metric in enumerate(
                (
                    "unsafe_attack_success",
                    "benign_task_complete",
                    "joint_safe_utility",
                )
            )
        }
        if condition in plan["main_conditions"]:
            pass_at_repeats[condition] = repeat_summary(
                valid_rows, plan["repeats"]
            )
        condition_attempts = [
            attempt for attempt in attempts if attempt["condition"] == condition
        ]
        failed = [
            attempt for attempt in condition_attempts if attempt["status"] == "failed"
        ]
        pending = [
            attempt for attempt in condition_attempts if attempt["status"] == "pending"
        ]
        unsafe = sum(row["result"]["unsafe_attack_success"] for row in valid_rows)
        benign = sum(row["result"]["benign_task_complete"] for row in valid_rows)
        planned = len(condition_attempts)
        missing = len(failed) + len(pending)
        sensitivity[condition] = {
            "planned": planned,
            "valid": len(valid_rows),
            "failed": len(failed),
            "pending": len(pending),
            "asr_lower_if_all_missing_safe": unsafe / planned if planned else None,
            "asr_upper_if_all_missing_unsafe": (
                (unsafe + missing) / planned if planned else None
            ),
            "bcr_lower_if_all_missing_incomplete": benign / planned if planned else None,
            "bcr_upper_if_all_missing_complete": (
                (benign + missing) / planned if planned else None
            ),
        }
        failures[condition] = dict(
            Counter(
                attempt["failure_category"]
                for attempt in failed
            )
        )
    comparisons = {}
    comparison_specs = [
        (
            "neutral_vs_prompt",
            "neutral",
            "prompt_guard_v1",
            None,
        ),
        (
            "prompt_vs_full",
            "prompt_guard_v1",
            "sail_hil",
            None,
        ),
        (
            "no_clarification_vs_full_repairable",
            "sail_hil_no_controller_clarification",
            "sail_hil",
            REPAIRABLE,
        ),
        (
            "no_recovery_vs_full",
            "sail_hil_no_recovery",
            "sail_hil",
            None,
        ),
    ]
    for name, left, right, policies in comparison_specs:
        comparisons[name] = {
            metric: paired(
                rows,
                left,
                right,
                metric,
                args.bootstrap,
                args.bootstrap_seed + index,
                policies,
            )
            for index, metric in enumerate(
                (
                    "unsafe_attack_success",
                    "benign_task_complete",
                    "joint_safe_utility",
                    "response_action_correct",
                    "resolved_after_clarification",
                )
            )
        }
    summary = {
        "suite": plan["suite"],
        "status": (
            "complete"
            if len(attempts) == plan["total_planned_runs"]
            and not any(attempt["status"] == "pending" for attempt in attempts)
            else "incomplete"
        ),
        "planned_attempts": plan["total_planned_runs"],
        "finished_attempts": sum(
            attempt["status"] != "pending" for attempt in attempts
        ),
        "valid_runs": len(rows),
        "failed_runs": sum(attempt["status"] == "failed" for attempt in attempts),
        "pending_runs": sum(attempt["status"] == "pending" for attempt in attempts),
        "independent_unit": "task_id",
        "valid_run_aggregates": by_condition,
        "valid_run_task_cluster_intervals": condition_intervals,
        "main_condition_repeat_summaries": pass_at_repeats,
        "paired_task_cluster_comparisons": comparisons,
        "all_attempt_sensitivity": sensitivity,
        "failure_categories": failures,
        "metric_boundaries": {
            "question_precision_proxy": (
                "Rule-based matching to the registered risky effect; not an "
                "independent semantic annotation of model understanding."
            ),
            "human_simulator": (
                "Policy fidelity and naturalness require the separate validation "
                "reports; agent outcomes alone do not validate realism."
            ),
            "route_identity": (
                "Requested and returned route IDs are recorded; underlying model "
                "weights are not independently attested."
            ),
        },
    }
    args.output_root.mkdir(parents=True, exist_ok=True)
    save(args.output_root / "summary.json", summary)
    with (args.output_root / "per_case.jsonl").open("w") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")
    with (args.output_root / "attempts.jsonl").open("w") as handle:
        for attempt in attempts:
            handle.write(json.dumps(attempt, ensure_ascii=False) + "\n")
    print(json.dumps({
        key: summary[key]
        for key in (
            "status",
            "planned_attempts",
            "finished_attempts",
            "valid_runs",
            "failed_runs",
            "pending_runs",
        )
    }))


if __name__ == "__main__":
    main()
