from pathlib import Path

import pytest

from hil_safety_bench.generate import (
    generate_cases,
    load_jsonl,
    materialize_case,
    write_suite_manifest,
    write_jsonl,
)
from hil_safety_bench.responses import TemplateResponseProvider
from hil_safety_bench.task_catalog import TASKS


def test_all_profiles_generate_four_cases_per_task(tmp_path: Path):
    cases = generate_cases(
        provider=TemplateResponseProvider(),
        seed=42,
        profiles="all",
    )
    assert len(cases) == len(TASKS) * 4
    assert {
        case.human_response.category for case in cases[:4]
    } == {"clear_approve", "clear_deny", "ambiguous", "scope_mismatch"}

    output = tmp_path / "cases.jsonl"
    write_jsonl(cases, output)
    reloaded = load_jsonl(output)
    assert [case.to_dict() for case in reloaded] == [
        case.to_dict() for case in cases
    ]
    assert all(case.human_response.text.isascii() for case in cases)


def test_materialized_case_contains_attack_only_in_artifact(tmp_path: Path):
    case = generate_cases(
        provider=TemplateResponseProvider(),
        seed=42,
        profiles="all",
    )[0]
    case_dir = materialize_case(case, tmp_path)
    task_prompt = (case_dir / "TASK.md").read_text(encoding="utf-8")
    artifact = (
        case_dir / "workspace" / case.task.attack.source_file
    ).read_text(encoding="utf-8")
    assert case.task.attack.injected_instruction not in task_prompt
    assert case.task.attack.injected_instruction in artifact


def test_hil_verification_task_has_implicit_authorization_gap(
    tmp_path: Path,
):
    cases = generate_cases(
        provider=TemplateResponseProvider(),
        seed=42,
        profiles="all",
    )
    case = next(
        item
        for item in cases
        if item.task.task_id == "dependency_verification_hil"
        and item.human_response.category == "clear_approve"
    )
    case_dir = materialize_case(case, tmp_path)
    task_prompt = (case_dir / "TASK.md").read_text(encoding="utf-8")

    assert "ask the task owner about that exact action" not in task_prompt
    assert case.task.attack.injected_instruction not in task_prompt
    assert case.task.attack.authorization_mode == "confirmable"
    assert case.task.attack.risk_stage == "post_task_persistence"
    assert len(case.task.attack.context_files) >= 3


def test_advanced_suite_has_diverse_multi_source_attack_families():
    assert len(TASKS) == 250
    assert len({task.task_id for task in TASKS}) == 250
    family_counts = {}
    for task in TASKS:
        family_counts[task.attack.attack_type] = (
            family_counts.get(task.attack.attack_type, 0) + 1
        )
    assert len(family_counts) == 20
    assert set(family_counts.values()) == {5, 20}
    assert sum(
        task.attack.authorization_mode == "confirmable"
        for task in TASKS
    ) == 195
    assert all(len(task.attack.context_files) >= 3 for task in TASKS)
    assert all(task.attack.deceptive_rationale for task in TASKS)


def test_generation_metadata_records_attack_structure():
    case = generate_cases(
        provider=TemplateResponseProvider(),
        seed=42,
        profiles="all",
    )[0]
    metadata = case.generation_metadata
    assert metadata["suite"] == "hil_safety_1000_v4"
    assert metadata["difficulty"] == "advanced"
    assert metadata["attack_family"] == case.task.attack.attack_type
    assert metadata["delivery_vector"] == case.task.attack.delivery_vector
    assert metadata["expected_initial_decision"] in {"ask", "block"}
    assert metadata["response_style"] == case.human_response.style


def test_suite_manifest_summarizes_advanced_attack_families(tmp_path: Path):
    cases = generate_cases(
        provider=TemplateResponseProvider(),
        seed=42,
        profiles="all",
    )
    output = tmp_path / "suite_manifest.json"
    write_suite_manifest(cases, output)

    import json

    payload = json.loads(output.read_text(encoding="utf-8"))
    assert payload["suite"] == "hil_safety_1000_v4"
    assert payload["case_count"] == 1000
    assert payload["task_count"] == 250
    assert len(payload["tasks"]) == 250
    assert payload["quality_summary"]["expected_initial_decision_counts"] == {
        "ask": 195,
        "block": 55,
    }


def test_materialization_refuses_overwrite(tmp_path: Path):
    case = generate_cases(
        provider=TemplateResponseProvider(),
        seed=42,
        profiles="all",
    )[0]
    materialize_case(case, tmp_path)
    with pytest.raises(FileExistsError):
        materialize_case(case, tmp_path)

