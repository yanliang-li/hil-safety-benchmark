"""Combine standard and targeted InterveneBench integration preflights.

The standard preflight must cover every experimental condition.  At most one
registered wall-clock timeout may be replaced by an exact targeted retry;
the targeted preflight must otherwise pass in full and exercise a native
second simulator turn.  No safety outcome from either preflight is an
experimental estimate.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load(path: Path) -> dict:
    return json.loads(path.read_text())


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def job_key(job: dict) -> tuple[str, str, str]:
    return (job["task_id"], job["response_policy"], job["condition"])


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--standard-plan", type=Path, required=True)
    parser.add_argument("--standard-audit", type=Path, required=True)
    parser.add_argument("--targeted-plan", type=Path, required=True)
    parser.add_argument("--targeted-audit", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    standard_plan = load(args.standard_plan)
    standard_audit = load(args.standard_audit)
    targeted_plan = load(args.targeted_plan)
    targeted_audit = load(args.targeted_audit)
    violations: list[str] = []

    if standard_plan.get("profile") not in {
        "standard",
        "standard_v2",
        "standard_v3",
        "standard_v4",
        "standard_v5",
        "standard_v6",
    }:
        violations.append("standard_profile_mismatch")
    if targeted_plan.get("profile") not in {
        "targeted",
        "targeted_v2",
        "targeted_v3",
        "targeted_v4",
        "targeted_v5",
        "targeted_v6",
    }:
        violations.append("targeted_profile_mismatch")
    for field in (
        "bank_manifest_sha256",
        "bank_cases_sha256",
        "image_id",
        "actor",
        "reviewer_model",
        "source_sha256",
    ):
        if standard_plan.get(field) != targeted_plan.get(field):
            violations.append(field + "_mismatch")

    expected_conditions = set(standard_plan.get("conditions", []))
    observed_conditions = set(standard_audit.get("condition_counts", {}))
    if observed_conditions != expected_conditions:
        violations.append("standard_condition_coverage_mismatch")
    # Prefer a fully passing standard suite. A single registered timeout is
    # admissible only when its exact task/policy/condition tuple is completed
    # in the targeted supplement.
    standard_violations = standard_audit.get("violations", [])
    missing = [
        item for item in standard_violations if item.endswith(":missing_result")
    ]
    standard_complete = (
        standard_audit.get("status") == "pass"
        and not standard_violations
        and standard_audit.get("audited_runs")
        == len(standard_plan.get("jobs", []))
    )
    if standard_complete:
        missing_run_id = None
        retry_job = None
    elif len(standard_violations) == 1 and len(missing) == 1:
        missing_run_id = missing[0].split(":", 1)[0]
        retry_job = {
            job["run_id"]: job for job in standard_plan.get("jobs", [])
        }.get(missing_run_id)
        if standard_audit.get("audited_runs") != len(
            standard_plan.get("jobs", [])
        ) - 1:
            violations.append("standard_valid_run_count_mismatch")
    else:
        violations.append("standard_failure_not_single_missing_result")
        missing_run_id = None
        retry_job = None

    if not standard_complete and retry_job is None:
        violations.append("standard_failed_job_not_found")
    elif retry_job is not None:
        folder = ROOT / "runs" / retry_job["stage"] / retry_job["run_id"]
        status_path = folder / "attempt_status.json"
        metadata_path = folder / "run_metadata.json"
        if not status_path.exists() or not metadata_path.exists():
            violations.append("standard_timeout_evidence_missing")
        else:
            status = load(status_path)
            metadata = load(metadata_path)
            if status.get("completed") is not False:
                violations.append("standard_replaced_attempt_not_failed")
            if metadata.get("timed_out") is not True:
                violations.append("standard_replaced_attempt_not_timeout")
            if status.get("event_count", 0) <= 0:
                violations.append("standard_replaced_attempt_no_events")

        targeted_by_key = {
            job_key(job): job for job in targeted_plan.get("jobs", [])
        }
        replacement = targeted_by_key.get(job_key(retry_job))
        targeted_rows = {
            row["run_id"]: row for row in targeted_audit.get("rows", [])
        }
        if replacement is None or replacement["run_id"] not in targeted_rows:
            violations.append("exact_targeted_retry_missing")

    if targeted_audit.get("status") != "pass":
        violations.append("targeted_audit_failed")
    if targeted_audit.get("violations"):
        violations.append("targeted_audit_has_violations")
    if targeted_audit.get("audited_runs") != len(targeted_plan.get("jobs", [])):
        violations.append("targeted_run_count_mismatch")
    advanced = targeted_audit.get("advanced_turn_runs", [])
    if not advanced:
        violations.append("native_second_turn_not_exercised")

    report = {
        "status": "pass" if not violations else "fail",
        "standard": {
            "plan_sha256": sha256(args.standard_plan),
            "audit_sha256": sha256(args.standard_audit),
            "planned_runs": len(standard_plan.get("jobs", [])),
            "audited_runs": standard_audit.get("audited_runs"),
            "replaced_timeout_run_id": missing_run_id,
        },
        "targeted": {
            "plan_sha256": sha256(args.targeted_plan),
            "audit_sha256": sha256(args.targeted_audit),
            "planned_runs": len(targeted_plan.get("jobs", [])),
            "audited_runs": targeted_audit.get("audited_runs"),
            "advanced_turn_runs": sorted(advanced),
        },
        "conditions_covered": sorted(observed_conditions),
        "source_sha256": standard_plan.get("source_sha256", {}),
        "bank_manifest_sha256": standard_plan.get("bank_manifest_sha256"),
        "bank_cases_sha256": standard_plan.get("bank_cases_sha256"),
        "violations": sorted(set(violations)),
        "scope": (
            "Integration and provenance gate only. Any admitted replacement "
            "must be an explicitly reported timeout, not a selective outcome "
            "retry; no preflight safety result enters formal estimates."
        ),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"status": report["status"], "violations": len(violations)}))
    if violations:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
