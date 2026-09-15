"""Audit native-agent InterveneBench preflight artifacts and route identity."""
from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE_ROOT = Path(
    "/home/root123/hil-api-experiments-20260912/gateway_evidence"
)
DIRECT_CONDITIONS = {"neutral", "prompt_guard_v1", "risk_oracle"}
HIDDEN_MARKERS = (
    "response_decision_hidden_from_agent",
    "response_scope_hidden_from_agent",
    "response_policy_hidden_from_agent",
    "matched_attack_hidden",
)
RESULT_FIELDS = {
    "case_id",
    "task_id",
    "response_policy",
    "unsafe_attack_success",
    "benign_task_complete",
    "joint_safe_utility",
    "response_action_correct",
    "matched_reply_count_before_effect",
    "clarification_turns",
    "resolved_after_clarification",
}


def load_json(path: Path) -> dict:
    return json.loads(path.read_text())


def evidence_violations(run_id: str, expected_model: str) -> list[str]:
    root = EVIDENCE_ROOT / run_id
    paths = sorted(root.glob("request_*.json")) if root.exists() else []
    if not paths:
        return ["missing_gateway_evidence"]
    violations = []
    for path in paths:
        row = load_json(path)
        if row.get("run_id") != run_id:
            violations.append("gateway_run_id_mismatch")
        if row.get("state") != "complete" or row.get("http_status") != 200:
            violations.append("gateway_request_incomplete")
        if row.get("transport_retries") != 0:
            violations.append("gateway_transport_retry")
        returned = row.get("returned_models")
        if returned != [expected_model]:
            violations.append("gateway_returned_model_mismatch")
    return sorted(set(violations))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("plan", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    plan = load_json(args.plan)
    violations = []
    warnings = []
    rows = []
    advanced_turn_runs = []
    wrapper_normalized_reviews = 0
    corrected_review_errors = 0
    guard_modes = set()
    condition_counts = Counter()
    for job in plan["jobs"]:
        prefix = job["run_id"] + ":"
        folder = ROOT / "runs" / job["stage"] / job["run_id"]
        status_path = folder / "attempt_status.json"
        metadata_path = folder / "run_metadata.json"
        result_path = folder / "result.json"
        for path, label in (
            (status_path, "missing_attempt_status"),
            (metadata_path, "missing_run_metadata"),
            (result_path, "missing_result"),
            (folder / "framework_config.json", "missing_framework_config"),
            (folder / "events.jsonl", "missing_events"),
        ):
            if not path.exists():
                violations.append(prefix + label)
        if not all(path.exists() for path in (status_path, metadata_path, result_path)):
            continue
        status = load_json(status_path)
        metadata = load_json(metadata_path)
        result = load_json(result_path)
        condition_counts[job["condition"]] += 1
        if status.get("completed") is not True:
            violations.append(prefix + "attempt_not_completed")
        expected_meta = {
            "agent": job["agent"],
            "requested_model": job["model"],
            "condition": job["condition"],
            "run_id": job["run_id"],
            "repeat": job["repeat"],
        }
        for field, expected in expected_meta.items():
            if metadata.get(field) != expected:
                violations.append(prefix + "metadata_" + field + "_mismatch")
        if not metadata.get("scorable") or not metadata.get("successful_termination"):
            violations.append(prefix + "run_not_scorable")
        if metadata.get("timed_out") or metadata.get("guard_invalid"):
            violations.append(prefix + "runtime_or_guard_failure")
        if metadata.get("real_credential_in_agent_container") is not False:
            violations.append(prefix + "credential_boundary_failure")
        if result.get("case_id") != job["case_id"]:
            violations.append(prefix + "result_case_mismatch")
        if result.get("task_id") != job["task_id"]:
            violations.append(prefix + "result_task_mismatch")
        if result.get("response_policy") != job["response_policy"]:
            violations.append(prefix + "result_policy_mismatch")
        missing_fields = sorted(RESULT_FIELDS - set(result))
        if missing_fields:
            violations.append(prefix + "missing_result_fields:" + ",".join(missing_fields))
        actor_stdout = (folder / "agent_stdout.log")
        if actor_stdout.exists():
            visible = actor_stdout.read_text(errors="replace")
            if any(marker in visible for marker in HIDDEN_MARKERS):
                violations.append(prefix + "hidden_label_exposed_to_actor")
        events = []
        events_path = folder / "events.jsonl"
        if events_path.exists():
            try:
                events = [
                    json.loads(line)
                    for line in events_path.read_text().splitlines()
                    if line.strip()
                ]
            except (ValueError, TypeError):
                violations.append(prefix + "invalid_event_log")
        if any(
            event.get("tool") == "ask_human"
            and event.get("result", {}).get(
                "response_turn_index_hidden_from_agent"
            )
            == 1
            for event in events
        ):
            advanced_turn_runs.append(job["run_id"])
        violations.extend(
            prefix + item
            for item in evidence_violations(job["run_id"], job["model"])
        )
        if job["condition"] in DIRECT_CONDITIONS:
            if metadata.get("guard_model") is not None:
                violations.append(prefix + "unexpected_guard_model")
        else:
            if metadata.get("guard_model") != plan["reviewer_model"]:
                violations.append(prefix + "guard_model_mismatch")
            guard_path = folder / "guard_events.jsonl"
            review_requests = []
            if not guard_path.exists():
                violations.append(prefix + "missing_guard_events")
            else:
                try:
                    guard_events = [
                        json.loads(line)
                        for line in guard_path.read_text().splitlines()
                        if line.strip()
                    ]
                except (ValueError, TypeError):
                    guard_events = []
                    violations.append(prefix + "invalid_guard_events")
                starts = [
                    event
                    for event in guard_events
                    if event.get("event") == "controller_started"
                ]
                if len(starts) != 1 or starts[0].get("mode") != job["condition"]:
                    violations.append(prefix + "controller_start_mismatch")
                else:
                    guard_modes.add(starts[0]["mode"])
                if any(
                    event.get("event") in {"guard_error", "review_error"}
                    for event in guard_events
                ):
                    violations.append(prefix + "guard_error_event")
                review_requests = [
                    event
                    for event in guard_events
                    if event.get("event") == "review_request"
                ]
                wrapper_normalized_reviews += sum(
                    event.get("event") == "review"
                    and event.get("protocol_wrapper_normalized") is True
                    for event in guard_events
                )
                corrected_review_errors += sum(
                    event.get("event") == "review_protocol_error"
                    and event.get("terminal") is False
                    for event in guard_events
                )
                if any(
                    event.get("max_tokens") != 8192
                    for event in review_requests
                ):
                    violations.append(prefix + "reviewer_budget_mismatch")
            guard_evidence = EVIDENCE_ROOT / (job["run_id"] + "_guard")
            if review_requests and not guard_evidence.exists():
                violations.append(prefix + "missing_guard_gateway_evidence")
            elif guard_evidence.exists():
                violations.extend(
                    prefix + "guard_" + item
                    for item in evidence_violations(
                        job["run_id"] + "_guard", plan["reviewer_model"]
                    )
                )
        rows.append(
            {
                "run_id": job["run_id"],
                "condition": job["condition"],
                "case_id": job["case_id"],
                "event_count": len(events),
                "clarification_turns": result.get("clarification_turns"),
                "scorable": metadata.get("scorable"),
            }
        )
    expected_conditions = set(plan["conditions"])
    if set(condition_counts) != expected_conditions:
        violations.append("condition_coverage_mismatch")
    expected_guard_modes = expected_conditions - DIRECT_CONDITIONS
    if guard_modes != expected_guard_modes:
        violations.append("guard_mode_coverage_mismatch")
    if not advanced_turn_runs:
        warnings.append(
            "No native-agent preflight advanced to turn 2; deterministic runtime "
            "tests cover state progression, but add a targeted native preflight "
            "before formal execution if clarification was not exercised."
        )
    report = {
        "status": "pass" if not violations else "fail",
        "suite": plan["suite"],
        "planned_runs": len(plan["jobs"]),
        "audited_runs": len(rows),
        "condition_counts": dict(sorted(condition_counts.items())),
        "guard_modes_observed": sorted(guard_modes),
        "advanced_turn_runs": sorted(advanced_turn_runs),
        "wrapper_normalized_reviews": wrapper_normalized_reviews,
        "corrected_review_errors": corrected_review_errors,
        "violations": sorted(set(violations)),
        "warnings": warnings,
        "rows": rows,
        "scope": (
            "Integration and provenance audit only; preflight safety outcomes "
            "are excluded from formal estimates."
        ),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(
        json.dumps(
            {
                "status": report["status"],
                "audited_runs": len(rows),
                "violations": len(report["violations"]),
                "warnings": len(warnings),
            }
        )
    )
    if violations:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
