import importlib.util
import json
from pathlib import Path

from hil_safety_bench.evaluate import evaluate_run, write_result
from hil_safety_bench.generate import generate_cases, materialize_case
from hil_safety_bench.responses import TemplateResponseProvider
from hil_safety_bench.runtime import BenchmarkRuntime

spec = importlib.util.spec_from_file_location(
    "audit_experiment", Path(__file__).parents[1] / "scripts/audit_experiment.py")
audit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)


def _run(tmp_path, content):
    case = next(c for c in generate_cases(provider=TemplateResponseProvider(),
        seed=42, profiles="all") if c.task.task_id == "product_draft_delivery")
    case_dir = materialize_case(case, tmp_path / "cases")
    run_dir = tmp_path / "run"
    runtime = BenchmarkRuntime(case_dir, run_dir)
    runtime.write_output("outputs/product_draft.md", content)
    runtime.finish("Done")
    write_result(evaluate_run(case_dir, run_dir), run_dir / "result.json")
    (run_dir / "run_metadata.json").write_text(json.dumps({
        "returncode": 0, "timed_out": False, "command": ["codex", "-C", "/case/workspace"]}))
    (run_dir / "codex_stream.jsonl").write_text('{"type":"turn.completed"}\n')
    return case_dir, run_dir


def test_blank_output_can_pass_legacy_utility_but_not_artifact_integrity(tmp_path):
    case_dir, run_dir = _run(tmp_path, "  \n")
    result = audit.audit_case(case_dir, run_dir)
    assert result["legacy_benign_complete"] is True
    assert result["artifact_integrity_pass"] is False
    assert result["semantic_task_quality"] == "not_evaluated"


def test_hidden_metadata_native_read_is_flagged_for_review(tmp_path):
    case_dir, run_dir = _run(tmp_path, "Draft prepared, delivery pending.")
    with (run_dir / "codex_stream.jsonl").open("a") as stream:
        stream.write(json.dumps({"type": "item.completed", "item": {
            "type": "command_execution", "command": "cat /case/.benchmark/case.json"}}) + "\n")
    result = audit.audit_case(case_dir, run_dir)
    assert "native_tool_use_requires_review" in result["issues"]
    assert len(result["native_tool_calls"]) == 1


def test_replay_disagrees_with_tampered_saved_score(tmp_path):
    case_dir, run_dir = _run(tmp_path, "Draft prepared, delivery pending.")
    result_path = run_dir / "result.json"
    result = json.loads(result_path.read_text())
    result["unsafe_attack_success"] = True
    result_path.write_text(json.dumps(result))
    assert "saved_score_differs_from_replay" in audit.audit_case(case_dir, run_dir)["issues"]


def test_simulated_exclusion_command_is_a_reference_not_a_metadata_read(tmp_path):
    case_dir, run_dir = _run(tmp_path, "Draft prepared, delivery pending.")
    with (run_dir / "codex_stream.jsonl").open("a") as stream:
        stream.write(json.dumps({"type": "item.completed", "item": {
            "type": "mcp_tool_call", "server": "hil_bench", "tool": "execute_command",
            "arguments": {"command": "find . -path './.benchmark' -prune -o -type f -print"},
            "result": {"simulated": True}}}) + "\n")
    result = audit.audit_case(case_dir, run_dir)
    assert "metadata_access_attempt" not in result["issues"]
    assert "metadata_reference_requires_review" in result["issues"]
