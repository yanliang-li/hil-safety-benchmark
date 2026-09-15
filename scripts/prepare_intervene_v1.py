"""Freeze a new task-ID holdout for the interaction-focused study."""
from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path

from hil_safety_bench.task_catalog import TASKS


ROOT = Path(__file__).resolve().parents[1]


def stable_key(seed: int, family: str, task_id: str) -> str:
    return hashlib.sha256(f"{seed}:{family}:{task_id}".encode()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--prior-split",
        type=Path,
        default=ROOT / "experiments/sail-v4-20260913/split_manifest.json",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "experiments/intervene-v1-20260914/split_manifest.json",
    )
    parser.add_argument("--seed", type=int, default=2026091401)
    parser.add_argument("--per-family", type=int, default=1)
    args = parser.parse_args()
    prior = json.loads(args.prior_split.read_text())
    exposed = set(prior.get("previous_real_model_tasks", []))
    exposed.update(
        item["task_id"] for item in prior.get("heldout_cases", [])
    )
    by_family = defaultdict(list)
    for task in TASKS:
        if task.task_id not in exposed:
            by_family[task.attack.attack_type].append(task)
    selected = []
    for family in sorted(by_family):
        eligible = sorted(
            by_family[family],
            key=lambda task: stable_key(args.seed, family, task.task_id),
        )
        if len(eligible) < args.per_family:
            raise ValueError(f"Not enough unexposed tasks for {family}")
        selected.extend(eligible[: args.per_family])
    payload = {
        "suite": "intervenebench_simulator_v1",
        "seed": args.seed,
        "selection": (
            "Lowest SHA256(seed:family:task_id) among task IDs absent from "
            "all prior real-model development and SAIL-v4 holdout exposure."
        ),
        "independent_unit": "task_id",
        "per_family": args.per_family,
        "prior_exposed_task_count": len(exposed),
        "selected_task_count": len(selected),
        "attack_family_count": len(by_family),
        "authorization_mode_counts": dict(
            Counter(task.attack.authorization_mode for task in selected)
        ),
        "domain_counts": dict(Counter(task.domain for task in selected)),
        "selected_tasks": [
            {
                "task_id": task.task_id,
                "attack_family": task.attack.attack_type,
                "domain": task.domain,
                "authorization_mode": task.attack.authorization_mode,
                "selection_key": stable_key(
                    args.seed,
                    task.attack.attack_type,
                    task.task_id,
                ),
            }
            for task in selected
        ],
        "boundary": (
            "Task IDs are held out from prior real-model runs but reuse known "
            "generator families; this is not an unseen-family split."
        ),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2) + "\n")
    print(json.dumps({
        "output": str(args.output),
        "selected_task_count": len(selected),
        "attack_family_count": len(by_family),
    }))


if __name__ == "__main__":
    main()
