import hashlib
import json
from pathlib import Path
import subprocess

import pytest

from hil_safety_bench import agents
from hil_safety_bench.cli import build_parser
from hil_safety_bench.conditions import PROMPT_GUARD_V1, apply_condition
from hil_safety_bench.generate import generate_cases, materialize_case
from hil_safety_bench.responses import TemplateResponseProvider


@pytest.mark.parametrize("condition", ["neutral", "prompt_guard_v1"])
def test_codex_records_the_actual_prompt_condition(tmp_path, monkeypatch, condition):
    case = generate_cases(provider=TemplateResponseProvider(), seed=42, profiles="all")[0]
    case_dir = materialize_case(case, tmp_path / "cases")
    task = (case_dir / "TASK.md").read_text()
    received = {}

    def process(command, **kwargs):
        received.update(kwargs)
        return subprocess.CompletedProcess(command, 0, stdout="", stderr=""), False

    monkeypatch.setattr(agents.shutil, "which", lambda _: "/usr/bin/codex")
    monkeypatch.setattr(agents, "_run_process", process)
    run_dir = tmp_path / "run"
    agents.run_codex(case_dir, run_dir, condition=condition)
    actual = received["input_text"]
    if condition == "neutral":
        # Required for comparison with the recovered V4 baseline.
        assert actual == task
    else:
        assert actual.startswith(task.rstrip())
        assert actual.endswith(PROMPT_GUARD_V1)
    metadata = json.loads((run_dir / "run_metadata.json").read_text())
    assert metadata["condition"] == condition
    assert metadata["effective_prompt_sha256"] == hashlib.sha256(actual.encode()).hexdigest()
    assert metadata["task_prompt_sha256"] == hashlib.sha256(task.encode()).hexdigest()


def test_unknown_condition_cannot_silently_become_baseline():
    with pytest.raises(ValueError):
        apply_condition("Task", "guard_typo")
    with pytest.raises(SystemExit):
        build_parser().parse_args(["run-codex", "/case", "--run-dir", "/run",
                                   "--condition", "guard_typo"])
