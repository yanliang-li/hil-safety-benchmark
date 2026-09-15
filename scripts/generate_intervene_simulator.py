"""Generate, cache and materialize the frozen stateful simulator bank."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import time

from hil_safety_bench.generate import materialize_case, write_jsonl
from hil_safety_bench.human_simulator import (
    POLICIES,
    POLICY_BY_ID,
    OpenAICompatibleSimulatorProvider,
    TemplateSimulatorProvider,
    generate_simulator_cases,
    stateful_case_from_dict,
)
from hil_safety_bench.schemas import BenchmarkCase
from hil_safety_bench.task_catalog import TASKS


ROOT = Path(__file__).resolve().parents[1]


def save(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")
    temporary.replace(path)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def expected_case_id(task_id: str, policy_id: str, seed: int) -> str:
    index = [policy.policy_id for policy in POLICIES].index(policy_id)
    return f"{task_id}__sim_{policy_id}__s{seed + index}"


def materialize(case: BenchmarkCase, cases_root: Path) -> None:
    destination = cases_root / case.case_id
    if destination.exists():
        existing = stateful_case_from_dict(
            json.loads((destination / ".benchmark/case.json").read_text())
        )
        if existing.to_dict() != case.to_dict():
            raise ValueError(f"Materialized case differs: {case.case_id}")
        return
    materialize_case(case, cases_root)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--split-manifest", type=Path, required=True)
    parser.add_argument("--output-root", type=Path, required=True)
    parser.add_argument(
        "--provider", choices=("template", "contextual"), required=True
    )
    parser.add_argument("--base-url")
    parser.add_argument("--model", default="deepseek-v4-flash")
    parser.add_argument("--seed", type=int, default=2026091402)
    parser.add_argument("--suite", default="intervenebench_simulator_v1")
    parser.add_argument("--task-id", action="append", dest="task_ids")
    parser.add_argument(
        "--selection",
        type=Path,
        help="JSON report containing exact task_id/policy_id selections",
    )
    parser.add_argument(
        "--policy",
        action="append",
        choices=tuple(POLICY_BY_ID),
        dest="policies",
    )
    parser.add_argument("--limit", type=int)
    args = parser.parse_args()
    if args.provider == "contextual" and not args.base_url:
        raise ValueError("--base-url is required for contextual generation")
    split = json.loads(args.split_manifest.read_text())
    selected_ids = [item["task_id"] for item in split["selected_tasks"]]
    if args.task_ids:
        unknown = sorted(set(args.task_ids) - set(selected_ids))
        if unknown:
            raise ValueError("Unknown --task-id values: " + ", ".join(unknown))
        selected_ids = [task_id for task_id in selected_ids if task_id in args.task_ids]
    task_by_id = {task.task_id: task for task in TASKS}
    tasks = [task_by_id[task_id] for task_id in selected_ids]
    policies = args.policies or [policy.policy_id for policy in POLICIES]
    provider = (
        TemplateSimulatorProvider()
        if args.provider == "template"
        else OpenAICompatibleSimulatorProvider(
            base_url=args.base_url,
            model=args.model,
        )
    )
    response_root = args.output_root / "response_cache"
    cases_root = args.output_root / "cases"
    planned = [(task, policy_id) for task in tasks for policy_id in policies]
    if args.selection:
        selection = json.loads(args.selection.read_text())
        selected_pairs = {
            (item["task_id"], item["policy_id"])
            for item in selection["selections"]
        }
        available_pairs = {
            (task.task_id, policy_id) for task, policy_id in planned
        }
        if not selected_pairs <= available_pairs:
            raise ValueError("Selection contains unavailable task-policy pairs")
        planned = [
            (task, policy_id)
            for task, policy_id in planned
            if (task.task_id, policy_id) in selected_pairs
        ]
    if args.limit is not None:
        planned = planned[: args.limit]
    progress_path = args.output_root / "generation_progress.json"
    cases = []
    started = time.time()
    for index, (task, policy_id) in enumerate(planned, start=1):
        case_id = expected_case_id(task.task_id, policy_id, args.seed)
        cache = response_root / f"{case_id}.json"
        try:
            if cache.exists():
                case = stateful_case_from_dict(json.loads(cache.read_text()))
            else:
                expected_seed = args.seed + [
                    policy.policy_id for policy in POLICIES
                ].index(policy_id)
                case = generate_simulator_cases(
                    provider=provider,
                    seed=expected_seed,
                    tasks=[task],
                    policy_ids=[policy_id],
                    suite=args.suite,
                )[0]
                # A one-policy call uses policy index zero; normalize only the
                # recorded suite seed so generation order cannot change identity.
                payload = case.to_dict()
                payload["generation_metadata"]["base_seed"] = args.seed
                case = stateful_case_from_dict(payload)
                save(cache, case.to_dict())
            if case.case_id != case_id:
                raise ValueError(f"Unexpected case identity: {case.case_id}")
            materialize(case, cases_root)
            cases.append(case)
            save(
                progress_path,
                {
                    "provider": args.provider,
                    "model": provider.model,
                    "planned": len(planned),
                    "completed": len(cases),
                    "last_case_id": case.case_id,
                    "started_unix": started,
                    "checked_unix": time.time(),
                    "status": "running" if index < len(planned) else "complete",
                },
            )
        except Exception as error:
            save(
                progress_path,
                {
                    "provider": args.provider,
                    "model": provider.model,
                    "planned": len(planned),
                    "completed": len(cases),
                    "failed_case_id": case_id,
                    "error_type": type(error).__name__,
                    "error": str(error)[:300],
                    "started_unix": started,
                    "checked_unix": time.time(),
                    "status": "failed",
                },
            )
            raise
    jsonl = args.output_root / "cases.jsonl"
    write_jsonl(cases, jsonl)
    manifest = {
        "suite": args.suite,
        "provider": args.provider,
        "model": provider.model,
        "seed": args.seed,
        "task_count": len({case.task.task_id for case in cases}),
        "case_count": len(cases),
        "policies": list(
            dict.fromkeys(case.human_response.policy_id for case in cases)
        ),
        "split_manifest": str(args.split_manifest),
        "split_manifest_sha256": sha256(args.split_manifest),
        "cases_jsonl_sha256": sha256(jsonl),
        "semantic_contract": (
            "Policy labels are construction targets. Model-graded and human "
            "validation are reported separately; labels alone do not establish realism."
        ),
    }
    save(args.output_root / "suite_manifest.json", manifest)
    print(json.dumps(manifest))


if __name__ == "__main__":
    main()
