import importlib.util
import json
from pathlib import Path
import shutil
from types import SimpleNamespace

import pytest

PROJECT = Path(__file__).parents[1]
spec = importlib.util.spec_from_file_location("gpt_pilot", PROJECT / "scripts/gpt_pilot.py")
pilot = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pilot)


@pytest.fixture
def mini_suite(tmp_path, monkeypatch):
    root = tmp_path / "project"
    source = root / "src/hil_safety_bench"
    source.mkdir(parents=True)
    (source / "example.py").write_text("VERSION = 1\n")
    for case in (PROJECT / "data/cases").glob("product_draft_delivery__*"):
        shutil.copytree(case, root / "data/cases" / case.name)
    monkeypatch.setattr(pilot, "ROOT", root)
    return root


def freeze(root):
    output = root / "manifest.json"
    pilot.freeze(SimpleNamespace(output=output, seed=42, model="gpt-5.6-luna"))
    return json.loads(output.read_text())


def test_frozen_manifest_preserves_four_replies_and_rejects_data_drift(mini_suite):
    manifest = freeze(mini_suite)
    assert manifest["case_count"] == 4
    assert manifest["task_count"] == 1
    assert {c["response_category"] for c in manifest["cases"]} == set(pilot.CATEGORIES)
    pilot.validate(manifest)
    case = manifest["cases"][0]["case_id"]
    (mini_suite / "data/cases" / case / "workspace/source/notes.md").write_text("Changed data\n")
    with pytest.raises(ValueError, match="Data drift"):
        pilot.validate(manifest)


def test_frozen_manifest_rejects_source_drift(mini_suite):
    manifest = freeze(mini_suite)
    (mini_suite / "src/hil_safety_bench/example.py").write_text("VERSION = 2\n")
    with pytest.raises(ValueError, match="Source drift"):
        pilot.validate(manifest)


def test_partial_response_pair_is_rejected_before_freezing(mini_suite):
    case = next((mini_suite / "data/cases").glob("*__ambiguous__*"))
    shutil.rmtree(case)
    with pytest.raises(ValueError, match="Incomplete/duplicate"):
        freeze(mini_suite)


def test_task_changes_between_reply_variants_are_rejected(mini_suite):
    path = next((mini_suite / "data/cases").glob("*__ambiguous__*/.benchmark/case.json"))
    case = json.loads(path.read_text())
    case["task"]["benign_goal"] = "A different task"
    path.write_text(json.dumps(case))
    with pytest.raises(ValueError, match="Task content changes"):
        freeze(mini_suite)
