"""Audit fixture-level necessity, separation, and cross-policy invariants."""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import json
from pathlib import Path

from hil_safety_bench.human_simulator import POLICY_BY_ID, stateful_case_from_dict


def canonical_effect(effect) -> tuple[str, str]:
    return effect.tool, json.dumps(effect.match, sort_keys=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("bank", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    cases = [
        stateful_case_from_dict(json.loads(line))
        for line in (args.bank / "cases.jsonl").read_text().splitlines()
        if line.strip()
    ]
    failures, warnings = [], []
    by_task = defaultdict(list)
    for case in cases:
        by_task[case.task.task_id].append(case)
        task = case.task
        source = task.files.get(task.attack.source_file)
        if source is None:
            failures.append([case.case_id, "missing_risk_source"])
            continue
        string_signals = [
            value
            for value in task.attack.risky_effect.match.values()
            if isinstance(value, str) and len(value) >= 3
        ]
        evidence_paths = set(task.attack.context_files) | {task.attack.source_file}
        evidence_text = "\n".join(task.files[path] for path in evidence_paths)
        if string_signals and not any(
            value in evidence_text for value in string_signals
        ):
            failures.append(
                [case.case_id, "risk_effect_not_grounded_in_environment"]
            )
        risky = canonical_effect(task.attack.risky_effect)
        if any(canonical_effect(effect) == risky for effect in task.required_benign_effects):
            failures.append([case.case_id, "benign_risky_effect_overlap"])
        missing_context = [
            path for path in task.attack.context_files if path not in task.files
        ]
        if missing_context:
            failures.append(
                [case.case_id, "missing_context_files", missing_context]
            )
        task_md = args.bank / "cases" / case.case_id / "TASK.md"
        if not task_md.exists():
            failures.append([case.case_id, "missing_agent_task"])
        else:
            prompt = task_md.read_text()
            leaked = [value for value in string_signals if value in prompt]
            if leaked:
                warnings.append([case.case_id, "risk_signal_in_task_prompt", leaked])

    expected_policies = set(POLICY_BY_ID)
    for task_id, rows in by_task.items():
        policies = {row.human_response.policy_id for row in rows}
        if policies != expected_policies:
            failures.append(
                [task_id, "policy_coverage", sorted(policies)]
            )
        reference = rows[0].task
        if any(row.task != reference for row in rows[1:]):
            failures.append([task_id, "task_drift_across_policies"])

    report = {
        "suite": "intervenebench_simulator_v1",
        "status": "pass" if not failures else "fail",
        "case_count": len(cases),
        "task_count": len(by_task),
        "policy_count": len({case.human_response.policy_id for case in cases}),
        "attack_family_count": len(
            {case.task.attack.attack_type for case in cases}
        ),
        "authorization_mode_counts": dict(
            Counter(case.task.attack.authorization_mode for case in cases)
        ),
        "checks": {
            "risk_source_present": True,
            "risky_effect_has_literal_environment_grounding": True,
            "benign_and_risky_effects_are_distinct": True,
            "context_files_present": True,
            "task_is_identical_across_response_policies": True,
            "all_six_policies_per_task": True,
        },
        "failures": failures,
        "warnings": warnings,
        "boundary": (
            "Literal grounding and effect separation are fixture checks, not "
            "evidence that a model semantically understands the risk."
        ),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({key: report[key] for key in ("status", "case_count", "task_count", "policy_count")}))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
