"""Create a small integration preflight spanning every dialogue/control branch."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import random
import time

from hil_safety_bench.human_simulator import stateful_case_from_dict


ROOT = Path(__file__).resolve().parents[1]
IMAGE_ID = "sha256:cef9c75343a0fd7f84e735ae4002a69b8d812d9becf3175bf029504852030c46"


STANDARD_SPECS = (
    ("incident_draft_delivery", "direct_approve", "neutral"),
    ("incident_draft_delivery", "direct_approve", "prompt_guard_v1"),
    ("incident_draft_delivery", "direct_approve", "sail_hil"),
    ("incident_draft_delivery", "direct_deny", "sail_hil"),
    ("incident_draft_delivery", "direct_deny", "sail_hil_no_recovery"),
    ("incident_draft_delivery", "uncertain_then_approve", "risk_oracle"),
    ("incident_draft_delivery", "uncertain_then_approve", "sail_hil"),
    (
        "incident_draft_delivery",
        "uncertain_then_approve",
        "sail_hil_no_controller_clarification",
    ),
    ("incident_draft_delivery", "uncertain_then_deny", "sail_hil"),
    ("incident_draft_delivery", "scope_repair_then_approve", "sail_hil"),
    (
        "incident_draft_delivery",
        "scope_repair_then_approve",
        "sail_hil_no_controller_clarification",
    ),
    ("incident_draft_delivery", "persistent_uncertainty", "sail_hil"),
    ("incident_draft_delivery", "direct_approve", "sail_hil_no_human"),
    ("data_import_cleanup", "direct_approve", "neutral"),
    ("data_import_cleanup", "direct_approve", "prompt_guard_v1"),
    ("data_import_cleanup", "direct_approve", "risk_oracle"),
    ("data_import_cleanup", "direct_approve", "sail_hil"),
    ("data_import_cleanup", "persistent_uncertainty", "sail_hil"),
)

TARGETED_SPECS = (
    # Fresh retry for the one standard-preflight upstream timeout.
    ("incident_draft_delivery", "uncertain_then_approve", "risk_oracle"),
    # Tasks whose trusted goal requires resolving an authorization decision.
    (
        "analytics_dashboard__state_transition",
        "scope_repair_then_approve",
        "sail_hil",
    ),
    (
        "analytics_dashboard__state_transition",
        "scope_repair_then_approve",
        "sail_hil_no_controller_clarification",
    ),
    (
        "analytics_dashboard__state_transition",
        "uncertain_then_approve",
        "sail_hil",
    ),
    (
        "campaign_preview__retention_commit",
        "uncertain_then_approve",
        "sail_hil",
    ),
    (
        "campaign_preview__retention_commit",
        "persistent_uncertainty",
        "sail_hil",
    ),
    (
        "release_candidate__workspace_replication",
        "scope_repair_then_approve",
        "sail_hil",
    ),
    (
        "employee_survey__resource_budget",
        "scope_repair_then_approve",
        "sail_hil",
    ),
    (
        "supplier_review__secret_bundle",
        "direct_approve",
        "sail_hil",
    ),
)

# Final integration set. It retains every distinct branch that produced useful
# protocol evidence and replaces two actor-loop-prone duplicates with a stable
# controller-origin clarification probe. Preflight outcomes are never estimates.
TARGETED_V4_SPECS = (
    ("incident_draft_delivery", "uncertain_then_approve", "risk_oracle"),
    (
        "analytics_dashboard__state_transition",
        "scope_repair_then_approve",
        "sail_hil",
    ),
    (
        "analytics_dashboard__state_transition",
        "scope_repair_then_approve",
        "sail_hil_no_controller_clarification",
    ),
    (
        "analytics_dashboard__state_transition",
        "uncertain_then_approve",
        "sail_hil",
    ),
    (
        "campaign_preview__retention_commit",
        "persistent_uncertainty",
        "sail_hil",
    ),
    (
        "employee_survey__resource_budget",
        "scope_repair_then_approve",
        "sail_hil",
    ),
    ("supplier_review__secret_bundle", "direct_approve", "sail_hil"),
    ("data_import_cleanup", "direct_approve", "sail_hil"),
)

TARGETED_V5_SPECS = tuple(
    spec
    for spec in TARGETED_V4_SPECS
    if spec[0] != "employee_survey__resource_budget"
)

PROFILES = {
    "standard": (2026091407, STANDARD_SPECS),
    "targeted": (2026091408, TARGETED_SPECS),
    # Fresh identities after the SAIL-HIL reviewer completion budget and the
    # native-agent wall-clock allowance were revised from preflight evidence.
    "standard_v2": (2026091409, STANDARD_SPECS),
    "targeted_v2": (2026091410, TARGETED_SPECS),
    # Final identities after aligning reply selection with the evaluator's
    # latest-pre-effect state rule and adding task-clustered result intervals.
    "standard_v3": (2026091411, STANDARD_SPECS),
    "targeted_v3": (2026091412, TARGETED_SPECS),
    "standard_v4": (2026091413, STANDARD_SPECS),
    "targeted_v4": (2026091414, TARGETED_V4_SPECS),
    "standard_v5": (2026091415, STANDARD_SPECS),
    "targeted_v5": (2026091416, TARGETED_V5_SPECS),
    "standard_v6": (2026091417, STANDARD_SPECS),
    "targeted_v6": (2026091418, TARGETED_V5_SPECS),
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def relative_hashes(root: Path) -> dict[str, str]:
    return {
        str(path.relative_to(root)): sha256(path)
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--bank", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--profile", choices=tuple(PROFILES), default="standard")
    args = parser.parse_args()
    args.bank = args.bank.resolve()
    args.output = args.output.resolve()
    seed, specs = PROFILES[args.profile]
    cases = [
        stateful_case_from_dict(json.loads(line))
        for line in (args.bank / "cases.jsonl").read_text().splitlines()
        if line.strip()
    ]
    bank_manifest = json.loads((args.bank / "suite_manifest.json").read_text())
    lookup = {
        (case.task.task_id, case.human_response.policy_id): case
        for case in cases
    }
    selected_keys = {(task_id, policy) for task_id, policy, _ in specs}
    chosen = [lookup[key] for key in sorted(selected_keys)]
    case_rows = []
    for case in sorted(chosen, key=lambda item: item.case_id):
        case_root = args.bank / "cases" / case.case_id
        case_rows.append(
            {
                "case_id": case.case_id,
                "task_id": case.task.task_id,
                "attack_family": case.task.attack.attack_type,
                "authorization_mode": case.task.attack.authorization_mode,
                "response_policy": case.human_response.policy_id,
                "case_root": str((args.bank / "cases").relative_to(ROOT)),
                "files": relative_hashes(case_root),
            }
        )
    case_by_key = {
        (row["task_id"], row["response_policy"]): row for row in case_rows
    }
    jobs = []
    for index, (task_id, policy, condition) in enumerate(specs, start=1):
        case = case_by_key[(task_id, policy)]
        digest = hashlib.sha256(
            f"{seed}:{index}:{case['case_id']}:{condition}".encode()
        ).hexdigest()[:16]
        jobs.append(
            {
                "run_id": f"iv1pf_{digest}",
                "stage": "preflight",
                "agent": "codex",
                "model": "glm-5.2",
                "condition": condition,
                "repeat": 1,
                "case_id": case["case_id"],
                "task_id": task_id,
                "response_policy": policy,
                "case_root": case["case_root"],
                "image_id": IMAGE_ID,
                "timeout": 900,
            }
        )
    random.Random(seed).shuffle(jobs)
    source_paths = []
    for folder in (
        ROOT / "src/hil_safety_bench",
        ROOT / "scripts/hil_guard_v3",
        ROOT / "scripts/hil_guard_v4",
        ROOT / "scripts/hil_guard_hil",
    ):
        source_paths.extend(
            path
            for path in folder.rglob("*.py")
            if "__pycache__" not in path.parts
        )
    source_paths.extend(
        [
            ROOT / "scripts/api_experiment/run_case.py",
            ROOT / "scripts/hermes_experiment/run_case.py",
            ROOT / "scripts/launch_intervene_formal.py",
            ROOT / "scripts/analyze_intervene_formal.py",
            ROOT / "scripts/prepare_intervene_preflight.py",
            ROOT / "scripts/audit_intervene_preflight.py",
        ]
    )
    plan = {
        "suite": f"{bank_manifest['suite']}_preflight",
        "created_unix": time.time(),
        "profile": args.profile,
        "seed": seed,
        "independent_unit": "integration case; excluded from formal estimates",
        "repeats": 1,
        "conditions": sorted({job["condition"] for job in jobs}),
        "main_conditions": [],
        "diagnostic_conditions": ["risk_oracle"],
        "actor": {"agent": "codex", "model": "glm-5.2"},
        "reviewer_model": "deepseek-v4-flash",
        "image_id": IMAGE_ID,
        "bank": str(args.bank.relative_to(ROOT)),
        "bank_manifest_sha256": sha256(args.bank / "suite_manifest.json"),
        "bank_cases_sha256": sha256(args.bank / "cases.jsonl"),
        "cases": case_rows,
        "jobs": jobs,
        "total_planned_runs": len(jobs),
        "source_sha256": {
            str(path.relative_to(ROOT)): sha256(path)
            for path in sorted(set(source_paths))
        },
        "acceptance_scope": (
            "Integration only: route identity, runtime state progression, guard "
            "protocol validity, evaluator replay, and artifact completeness. "
            "No preflight outcome enters a paper estimate."
        ),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(plan, indent=2) + "\n")
    print(json.dumps({"jobs": len(jobs), "cases": len(case_rows)}))


if __name__ == "__main__":
    main()
