"""Create a new immutable simulator bank from a base bank and audited repairs."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import time

from hil_safety_bench.generate import materialize_case, write_jsonl
from hil_safety_bench.human_simulator import stateful_case_from_dict


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path: Path):
    return [
        stateful_case_from_dict(json.loads(line))
        for line in (path / "cases.jsonl").read_text().splitlines()
        if line.strip()
    ]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", type=Path, required=True)
    parser.add_argument("--repairs", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--suite", default="intervenebench_simulator_v2_1")
    parser.add_argument(
        "--revision", default="audited_regeneration_v1"
    )
    args = parser.parse_args()
    if args.output.exists():
        raise FileExistsError("Refusing to overwrite repair-merged bank")
    base = load(args.base)
    repairs = load(args.repairs)
    repair_by_key = {
        (case.task.task_id, case.human_response.policy_id): case
        for case in repairs
    }
    if len(repair_by_key) != len(repairs):
        raise ValueError("Duplicate task-policy repair")
    base_keys = {
        (case.task.task_id, case.human_response.policy_id) for case in base
    }
    if not set(repair_by_key) <= base_keys:
        raise ValueError("Repair does not correspond to a base task-policy")
    output = []
    replacements = []
    base_hash = sha256(args.base / "cases.jsonl")
    repair_hash = sha256(args.repairs / "cases.jsonl")
    for case in base:
        key = (case.task.task_id, case.human_response.policy_id)
        selected = repair_by_key.get(key, case)
        if selected.task != case.task or selected.case_id != case.case_id:
            raise ValueError("Repair changed task or case identity: " + case.case_id)
        payload = selected.to_dict()
        payload["generation_metadata"].update(
            suite=args.suite,
            parent_bank_sha256=base_hash,
        )
        if key in repair_by_key:
            payload["generation_metadata"].update(
                response_revision=args.revision,
                repair_bank_sha256=repair_hash,
            )
            replacements.append(case.case_id)
        revised = stateful_case_from_dict(payload)
        output.append(revised)
        materialize_case(revised, args.output / "cases")
    if len(output) != 120 or len({case.task.task_id for case in output}) != 20:
        raise ValueError("Merged bank must contain 20 tasks x 6 policies")
    write_jsonl(output, args.output / "cases.jsonl")
    manifest = {
        "suite": args.suite,
        "created_unix": time.time(),
        "case_count": len(output),
        "task_count": len({case.task.task_id for case in output}),
        "policy_count": len(
            {case.human_response.policy_id for case in output}
        ),
        "base_bank": str(args.base),
        "base_cases_sha256": base_hash,
        "repair_bank": str(args.repairs),
        "repair_cases_sha256": repair_hash,
        "replacement_count": len(replacements),
        "replaced_case_ids": sorted(replacements),
        "cases_jsonl_sha256": sha256(args.output / "cases.jsonl"),
        "selection_boundary": (
            "Repairs must be selected by a frozen audit rule before formal "
            "agent evaluation; repair outcomes are re-audited on the full bank."
        ),
    }
    (args.output / "suite_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n"
    )
    print(json.dumps(manifest, ensure_ascii=False))


if __name__ == "__main__":
    main()
